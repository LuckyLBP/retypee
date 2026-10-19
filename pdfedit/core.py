"""Text editing engine built on PyMuPDF.

PDF text is not stored as paragraphs. It is a list of glyphs drawn at fixed
positions. "Editing" therefore means: remove the original glyphs with a
text-only redaction (images and vector graphics stay untouched), then draw
the new text at the same baseline with the same size, colour and the closest
available font.
"""

from __future__ import annotations

import re
import secrets
from dataclasses import dataclass, field

import pymupdf

from .fonts import FontResolver, ResolvedFont, loose, style_of


# --------------------------------------------------------------------------
# Data structures
# --------------------------------------------------------------------------

@dataclass
class Unit:
    """A run of text on one line that shares one style. The editable thing."""
    id: int
    page: int
    font: str
    size: float
    color: int
    flags: int
    horizontal: bool
    chars: list = field(default_factory=list)  # rawdict chars: {"c","bbox","origin"}

    @property
    def text(self) -> str:
        return "".join(c["c"] for c in self.chars)

    @property
    def bbox(self) -> pymupdf.Rect:
        r = pymupdf.Rect(self.chars[0]["bbox"])
        for c in self.chars[1:]:
            r |= c["bbox"]
        return r

    def to_json(self, matrix: pymupdf.Matrix | None = None) -> dict:
        b = self.bbox * matrix if matrix is not None else self.bbox
        bold, italic = style_of(self.font, self.flags)
        return {
            "id": self.id,
            "text": self.text,
            "bbox": [round(v, 2) for v in (b.x0, b.y0, b.x1, b.y1)],
            "font": self.font,
            "size": round(self.size, 2),
            "color": f"#{self.color:06x}",
            "bold": bold,
            "italic": italic,
            "editable": self.horizontal,
        }


@dataclass
class EditOp:
    unit: Unit
    start: int            # first char that changes; text before it can stay untouched
    new_text: str         # the complete new text of the run
    font: str | None = None   # override: "auto", "sans", "serif", "mono", "file:<path>#<i>"
    size: float | None = None
    color: str | None = None  # "#rrggbb"
    fit: bool = False     # squeeze horizontally if the new text is wider than the old
    bold: bool | None = None    # None keeps the original style
    italic: bool | None = None


@dataclass
class OpResult:
    page: int
    font_label: str
    font_source: str


# --------------------------------------------------------------------------
# Extraction
# --------------------------------------------------------------------------

def _same_style(a: Unit, b: Unit) -> bool:
    """Runs written by this editor get a slightly different font name than the
    original ('Liberation Sans Regular' vs 'LiberationSans'), so compare loosely."""
    same_font = loose(a.font) == loose(b.font) or (
        # Chrome turns some fonts (e.g. variable fonts) into many tiny Type3
        # fonts, one per group of glyphs. Treat them as one font.
        a.font.startswith("Type3") and b.font.startswith("Type3"))
    return same_font and abs(a.size - b.size) < 0.05 and a.color == b.color


def _visible(chars: list) -> list:
    return [c for c in chars if not c["c"].isspace()]


def _first_visible(u: Unit) -> dict:
    v = _visible(u.chars)
    return v[0] if v else u.chars[0]


def _last_visible(u: Unit) -> dict:
    v = _visible(u.chars)
    return v[-1] if v else u.chars[-1]


def _split_at_gaps(run: Unit) -> list[Unit]:
    """Split a run wherever two visible glyphs are far apart (more than about
    one and a half em), which means they belong to different text blocks."""
    if not run.horizontal:
        return [run]
    limit = 1.5 * max(run.size, 1.0)
    pieces, current, last_visible = [], [], None
    for c in run.chars:
        if not c["c"].isspace():
            if last_visible is not None and c["bbox"][0] - last_visible["bbox"][2] > limit:
                pieces.append(current)
                current = []
            last_visible = c
        current.append(c)
    pieces.append(current)
    if len(pieces) == 1:
        return [run]
    return [Unit(id=-1, page=run.page, font=run.font, size=run.size, color=run.color,
                 flags=run.flags, horizontal=True, chars=p) for p in pieces if _visible(p)]


def drawn_chars(units: list[Unit]) -> dict[str, set[str]]:
    """Characters already drawn on the page, per font. Glyphs in this set are
    guaranteed to exist in the embedded font."""
    out: dict[str, set[str]] = {}
    for u in units:
        out.setdefault(u.font, set()).update(c["c"] for c in u.chars)
    return out


def extract_units(page: pymupdf.Page) -> list[Unit]:
    raw = page.get_text("rawdict", flags=pymupdf.TEXT_PRESERVE_LIGATURES
                        | pymupdf.TEXT_PRESERVE_WHITESPACE | pymupdf.TEXT_MEDIABOX_CLIP)

    # 1. Collect every span as a run.
    runs: list[Unit] = []
    for block in raw["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            dx, dy = line["dir"]
            horizontal = abs(dx - 1) < 1e-3 and abs(dy) < 1e-3
            for span in line["spans"]:
                if span["chars"]:
                    runs.append(Unit(id=-1, page=page.number, font=span["font"], size=span["size"],
                                     color=span["color"], flags=span["flags"],
                                     horizontal=horizontal, chars=list(span["chars"])))

    # 1b. Split runs at wide gaps. Some PDFs put text from separate columns in
    #     one span (padded with spaces); those must stay separate edit units.
    runs = [piece for r in runs for piece in _split_at_gaps(r)]

    # 2. Join runs that continue each other on the same baseline. Edited text
    #    lands in its own block, so this is what keeps an edited line in one piece.
    def baseline(u: Unit) -> float:
        return u.chars[0]["origin"][1]

    by_baseline = sorted((r for r in runs if r.horizontal), key=baseline)
    lines: list[list[Unit]] = []
    for run in by_baseline:
        if lines and abs(baseline(lines[-1][0]) - baseline(run)) < 0.5:
            lines[-1].append(run)
        else:
            lines.append([run])
    merged: list[Unit] = []
    for line_runs in lines:
        line_runs.sort(key=lambda r: r.chars[0]["bbox"][0])
        prev = None
        for run in line_runs:
            if prev is not None and _same_style(prev, run):
                gap = _first_visible(run)["bbox"][0] - _last_visible(prev)["bbox"][2]
                if -0.5 * run.size < gap < 0.6 * run.size:
                    last, first = prev.chars[-1], run.chars[0]
                    if gap > 0.15 * run.size and not last["c"].isspace() and not first["c"].isspace():
                        # Words placed apart without a space glyph: add a virtual
                        # space so search and editing see "12 500", not "12500".
                        prev.chars.append({
                            "c": " ",
                            "origin": (last["bbox"][2], last["origin"][1]),
                            "bbox": (last["bbox"][2], last["bbox"][1], first["bbox"][0], last["bbox"][3]),
                        })
                    prev.chars.extend(run.chars)
                    continue
            merged.append(run)
            prev = run
    merged.extend(r for r in runs if not r.horizontal)

    # 3. Trim surrounding whitespace and number the units in reading order.
    units: list[Unit] = []
    for u in merged:
        chars = u.chars
        while chars and chars[0]["c"].isspace():
            chars = chars[1:]
        while chars and chars[-1]["c"].isspace():
            chars = chars[:-1]
        if chars:
            u.chars = chars
            units.append(u)
    units.sort(key=lambda u: (round(u.bbox.y0 / 3), u.bbox.x0))
    for i, u in enumerate(units):
        u.id = i
    return units


# --------------------------------------------------------------------------
# Editing
# --------------------------------------------------------------------------

def _hex_to_rgb(value: str) -> tuple[float, float, float]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _int_to_rgb(value: int) -> tuple[float, float, float]:
    return ((value >> 16) & 255) / 255, ((value >> 8) & 255) / 255, (value & 255) / 255


def _redact_rect(chars: list) -> pymupdf.Rect:
    """A rectangle covering the given chars but only the middle of the first
    and last glyph, so neighbouring glyphs that touch the box survive."""
    first, last = pymupdf.Rect(chars[0]["bbox"]), pymupdf.Rect(chars[-1]["bbox"])
    r = pymupdf.Rect(chars[0]["bbox"])
    for c in chars[1:]:
        r |= c["bbox"]
    h = r.height
    return pymupdf.Rect(first.x0 + first.width * 0.35, r.y0 + h * 0.3,
                        last.x1 - last.width * 0.35, r.y1 - h * 0.3)


def _right_aligned(unit: Unit, others: list[Unit]) -> bool:
    """True when the run sits in a right-aligned column (typical for prices):
    a neighbouring line ends at the same x but starts somewhere else, and no
    neighbouring line starts at the same x (that would be a left-aligned block,
    like the lines of an address)."""
    b = unit.bbox
    baseline = unit.chars[0]["origin"][1]
    reach = 3.5 * max(unit.size, 1.0)
    right_match = False
    for o in others:
        if o is unit or not o.horizontal or abs(o.size - unit.size) > 0.5:
            continue
        ob = o.bbox
        same_line = abs(o.chars[0]["origin"][1] - baseline) < 1.0
        if same_line:
            # Continues a label on its left ("Invoice no: <run>"): stay anchored left.
            if b.x0 - unit.size <= ob.x1 <= b.x0 + 1:
                return False
            continue
        if abs(ob.y0 - b.y0) > reach:
            continue
        if abs(ob.x0 - b.x0) < 1.0:
            return False
        if abs(ob.x1 - b.x1) < 1.0 and abs(ob.x0 - b.x0) > 2.0:
            right_match = True
    return right_match


def apply_ops(doc: pymupdf.Document, page: pymupdf.Page, ops: list[EditOp],
              resolver: FontResolver, page_units: list[Unit] | None = None) -> list[OpResult]:
    """Apply several edits on one page: redact all old text in one pass, then
    write all new text."""
    if page_units is None:
        page_units = extract_units(page)
    drawn = drawn_chars(page_units)
    plans = []
    for op in ops:
        u = op.unit
        if not u.horizontal:
            raise ValueError("Rotated or vertical text cannot be edited yet.")
        # Resolve the font before redacting, while the original font is still in use.
        rf: ResolvedFont = resolver.resolve(page, u.font, u.flags, u.text, op.new_text, op.font,
                                            bold=op.bold, italic=op.italic,
                                            drawn=drawn.get(u.font, set()))
        start = max(0, min(op.start, len(u.chars), len(op.new_text)))
        right = _right_aligned(u, page_units)
        if (rf.source != "embedded" or op.size or op.color or (op.font and op.font != "auto")
                or op.bold is not None or op.italic is not None or right):
            # The new glyphs will look different from the original ones (or the
            # whole run has to move), so rewrite the whole run.
            start = 0
        old_tail = u.chars[start:]
        if start < len(u.chars):
            origin = pymupdf.Point(u.chars[start]["origin"])
        else:  # appending at the end of the run
            last = u.chars[-1]
            origin = pymupdf.Point(last["bbox"][2], last["origin"][1])
        old_width = (pymupdf.Rect(old_tail[-1]["bbox"]).x1 - origin.x) if old_tail else 0
        if right and old_tail:
            # Keep the right edge where it was.
            size = float(op.size or u.size)
            width = rf.font.text_length(op.new_text, fontsize=size)
            if op.fit and width > old_width > 0:
                width = max(old_width, width * 0.5)
            origin = pymupdf.Point(u.bbox.x1 - width, origin.y)
        plans.append((op, rf, origin, old_tail, op.new_text[start:], old_width))

    for op, _, _, old_tail, _, _ in plans:
        # Skip whitespace-only tails; there is nothing visible to remove.
        visible = [c for c in old_tail if not c["c"].isspace()]
        if visible:
            page.add_redact_annot(_redact_rect(visible), fill=False, cross_out=False)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)

    results = []
    for op, rf, origin, _, text, old_width in plans:
        if text.strip():
            size = float(op.size or op.unit.size)
            color = _hex_to_rgb(op.color) if op.color else _int_to_rgb(op.unit.color)
            tw = pymupdf.TextWriter(page.rect)
            tw.append(origin, text, font=rf.font, fontsize=size)
            morph = None
            if op.fit and old_width > 0:
                new_width = rf.font.text_length(text, fontsize=size)
                if new_width > old_width:
                    scale = max(old_width / new_width, 0.5)
                    morph = (origin, pymupdf.Matrix(scale, 1))
            tw.write_text(page, color=color, morph=morph)
        results.append(OpResult(page.number, rf.label, rf.source))
    resolver.reset()
    return results


def edit_unit(doc, page, unit: Unit, new_text: str, resolver: FontResolver,
              font: str | None = None, size: float | None = None,
              color: str | None = None, fit: bool = False,
              bold: bool | None = None, italic: bool | None = None) -> OpResult:
    old = unit.text
    style_change = bool((font and font != "auto") or size or color
                        or bold is not None or italic is not None)
    if old == new_text and not style_change:
        return OpResult(page.number, "", "unchanged")
    start = 0
    while start < min(len(old), len(new_text)) and old[start] == new_text[start]:
        start += 1
    op = EditOp(unit=unit, start=start, new_text=new_text, font=font, size=size, color=color,
                fit=fit, bold=bold, italic=italic)
    return apply_ops(doc, page, [op], resolver)[0]


def replace_text(doc: pymupdf.Document, find: str, replace: str, resolver: FontResolver,
                 case_sensitive: bool = False, whole_word: bool = False, fit: bool = False,
                 pages: list[int] | None = None) -> tuple[int, list[int]]:
    """Find and replace inside text runs. Returns (count, changed page numbers).
    A match must sit inside one run of same-styled text on one line."""
    if not find:
        return 0, []
    pattern = re.escape(find)
    if whole_word:
        pattern = rf"(?<!\w){pattern}(?!\w)"
    rx = re.compile(pattern, 0 if case_sensitive else re.IGNORECASE)
    total, changed = 0, []
    for pno in pages if pages is not None else range(doc.page_count):
        page = doc[pno]
        ops = []
        units = extract_units(page)
        for u in units:
            if not u.horizontal:
                continue
            text = u.text
            matches = list(rx.finditer(text))
            if not matches:
                continue
            new_text = rx.sub(lambda m: replace, text)
            ops.append(EditOp(unit=u, start=matches[0].start(), new_text=new_text, fit=fit))
            total += len(matches)
        if ops:
            apply_ops(doc, page, ops, resolver, page_units=units)
            changed.append(pno)
    return total, changed


def add_text(doc, page: pymupdf.Page, x: float, y: float, text: str, size: float,
             color: str, font: str | None, resolver: FontResolver,
             bold: bool = False, italic: bool = False) -> OpResult:
    """Add new text with its baseline at (x, y), given in displayed page
    coordinates (that is, after page rotation)."""
    choice = font if font and font != "auto" else "sans"
    rf = resolver.resolve(page, "Helvetica", 0, "", text, choice, bold=bold, italic=italic)
    point = pymupdf.Point(x, y) * page.derotation_matrix
    tw = pymupdf.TextWriter(page.rect)
    tw.append(point, text, font=rf.font, fontsize=size)
    morph = (point, pymupdf.Matrix(page.rotation)) if page.rotation else None
    tw.write_text(page, color=_hex_to_rgb(color or "#000000"), morph=morph)
    return OpResult(page.number, rf.label, rf.source)


def remove_metadata(doc: pymupdf.Document) -> None:
    """Remove information about who made the PDF and how: the document info
    (title, author, subject, keywords, creator app, producer, dates), XMP
    metadata on the document and on every object (pages, images, fonts),
    page thumbnails, and the author names on comments and annotations.
    Text, images, links, forms and attachments are left alone."""
    doc.scrub(metadata=True, xml_metadata=True, thumbnails=True, reset_responses=True,
              attached_files=False, clean_pages=False, embedded_files=False,
              hidden_text=False, javascript=False, redactions=False,
              remove_links=False, reset_fields=False)
    doc.set_metadata({})
    for xref in range(1, doc.xref_length()):
        try:
            for key in ("Metadata", "PieceInfo", "LastModified"):
                if doc.xref_get_key(xref, key)[0] != "null":
                    doc.xref_set_key(xref, key, "null")
        except Exception:
            continue
    for page in doc:
        for annot in page.annots() or []:
            try:
                info = annot.info
                if info.get("title") or info.get("subject"):
                    annot.set_info(title="", subject="")
                    annot.update()
            except Exception:
                continue
    root = doc.pdf_catalog()
    # "Info" in the catalog is not standard, but some writers put a copy there.
    for key in ("Metadata", "PieceInfo", "Info"):
        if doc.xref_get_key(root, key)[0] != "null":
            doc.xref_set_key(root, key, "null")


# --------------------------------------------------------------------------
# Document session with undo / redo
# --------------------------------------------------------------------------

class EditorDocument:
    MAX_HISTORY = 50

    def __init__(self, data: bytes, name: str) -> None:
        self.name = name
        self.doc = pymupdf.open(stream=data, filetype="pdf")
        if self.doc.needs_pass:
            raise ValueError("This PDF is password protected. Remove the password first.")
        if not self.doc.is_pdf:
            raise ValueError("This file is not a PDF.")
        self.resolver = FontResolver(self.doc)
        self.version = 0
        self._undo: list[bytes] = []
        self._redo: list[bytes] = []
        self._units_cache: dict[tuple[int, int], list[Unit]] = {}

    # -- state --------------------------------------------------------------
    def _reload(self, data: bytes) -> None:
        self.doc.close()
        self.doc = pymupdf.open(stream=data, filetype="pdf")
        self.resolver = FontResolver(self.doc)

    def checkpoint(self) -> None:
        self._undo.append(self.doc.tobytes())
        if len(self._undo) > self.MAX_HISTORY:
            self._undo.pop(0)
        self._redo.clear()

    def commit(self) -> None:
        self.version += 1
        self._units_cache.clear()

    def discard_checkpoint(self) -> None:
        """Drop the last checkpoint when an edit turned out to change nothing."""
        if self._undo:
            self._undo.pop()

    def rollback(self) -> None:
        """Restore the last checkpoint after a failed edit."""
        if self._undo:
            self._reload(self._undo.pop())
        self._units_cache.clear()

    def undo(self) -> bool:
        if not self._undo:
            return False
        self._redo.append(self.doc.tobytes())
        self._reload(self._undo.pop())
        self.commit()
        return True

    def redo(self) -> bool:
        if not self._redo:
            return False
        self._undo.append(self.doc.tobytes())
        self._reload(self._redo.pop())
        self.commit()
        return True

    # -- reading ------------------------------------------------------------
    def meta(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "pages": [{"w": round(p.rect.width, 2), "h": round(p.rect.height, 2)} for p in self.doc],
            "canUndo": bool(self._undo),
            "canRedo": bool(self._redo),
        }

    def units(self, pno: int) -> list[Unit]:
        key = (self.version, pno)
        if key not in self._units_cache:
            self._units_cache[key] = extract_units(self.doc[pno])
        return self._units_cache[key]

    def units_json(self, pno: int) -> list[dict]:
        matrix = self.doc[pno].rotation_matrix
        return [u.to_json(matrix) for u in self.units(pno)]

    def render(self, pno: int, zoom: float) -> bytes:
        pix = self.doc[pno].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
        return pix.tobytes("png")

    def export(self, strip_metadata: bool = True) -> bytes:
        """Final PDF: embedded fonts are subset to keep the file small, and
        metadata is removed unless strip_metadata is False."""
        out = pymupdf.open(stream=self.doc.tobytes(), filetype="pdf")
        try:
            out.subset_fonts()
        except Exception:
            pass
        if strip_metadata:
            remove_metadata(out)
        # garbage=4 also drops objects that only the removed metadata used.
        no_new_id = False
        if strip_metadata:
            # Both parts of the file ID are replaced; the first part normally
            # stays the same for life and could link the file to the original.
            new_id = secrets.token_hex(16).upper()
            out.xref_set_key(-1, "ID", f"[<{new_id}><{new_id}>]")
            no_new_id = True
        data = out.tobytes(garbage=4 if strip_metadata else 3, deflate=True, no_new_id=no_new_id)
        out.close()
        if strip_metadata:
            # Blank the "% Written by MuPDF" header comment, same length so
            # every byte offset in the file stays valid.
            data = re.sub(rb"%[^\n]*MuPDF[^\n]*", lambda m: b"%" + b" " * (len(m.group()) - 1),
                          data, count=1)
        return data
