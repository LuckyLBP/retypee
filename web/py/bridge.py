"""Browser entry point. Runs inside Pyodide in a Web Worker.

Mirrors the routes in app.py, minus FastAPI, so the frontend can keep the same
route names. Nothing here touches the network; documents live in memory in
this worker and disappear when the tab closes.
"""

from __future__ import annotations

import io
import json
import re
import secrets
import uuid
import zipfile
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pymupdf

from pdfedit.core import EditorDocument, add_text, edit_unit, replace_text
from pdfedit.fonts import FONT_EXTS, FONT_INDEX, USER_FONT_DIR, font_choices

DOCS: dict[str, EditorDocument] = {}


# --------------------------------------------------------------------------
# Messages. Swedish is the main language; the page sends lang="en" for /en/.
# --------------------------------------------------------------------------

LANG = "sv"

MESSAGES = {
    "doc_closed": ("This document is no longer open. Open it again.", "Dokumentet är inte längre öppet. Öppna det igen."),
    "no_page": ("Page {n} does not exist.", "Sida {n} finns inte."),
    "version": ("The document changed in the meantime. Reload the page view and try again.", "Dokumentet ändrades under tiden. Ladda om sidvyn och försök igen."),
    "no_file": ("No file received.", "Ingen fil mottogs."),
    "open_fail": ("This file could not be opened as a PDF.", "Filen kunde inte öppnas som PDF."),
    "text_gone": ("That text is no longer on the page. Reload and try again.", "Texten finns inte längre på sidan. Ladda om och försök igen."),
    "rotated": ("Rotated or vertical text cannot be edited yet.", "Roterad eller lodrät text kan inte redigeras ännu."),
    "find_empty": ("Type the text you want to find.", "Skriv texten du vill hitta."),
    "add_empty": ("Type some text to add.", "Skriv den text du vill lägga till."),
    "nothing_undo": ("Nothing to undo.", "Inget att ångra."),
    "nothing_redo": ("Nothing to redo.", "Inget att göra om."),
    "no_font": ("No font file received.", "Ingen typsnittsfil mottogs."),
    "bad_ext": ("Add a .ttf, .otf or .ttc font file.", "Lägg till en .ttf-, .otf- eller .ttc-fil."),
    "bad_font": ("That file does not look like a usable font.", "Filen verkar inte vara ett fungerande typsnitt."),
    "needs_password": ("This PDF needs a password.", "Den här PDF-filen kräver ett lösenord."),
    "wrong_password": ("That password is not correct.", "Lösenordet stämmer inte."),
    "pw_empty": ("Type a password first.", "Skriv ett lösenord först."),
    "redact_empty": ("Draw a box or search for text to redact first.", "Rita en ruta eller sök efter text som ska censureras först."),
    "route": ("Unknown route {method} {path}", "Okänd adress {method} {path}"),
    "no_images": ("No images were found in this PDF.", "Inga bilder hittades i den här PDF-filen."),
    "repair_fail": ("This file is too damaged to repair.", "Filen är för skadad för att kunna repareras."),
}

# Messages raised by the shared engine (pdfedit/core.py), which stays English-only.
ENGINE_SV = {
    "Rotated or vertical text cannot be edited yet.": "Roterad eller lodrät text kan inte redigeras ännu.",
    "This PDF is password protected. Remove the password first.": "PDF-filen är lösenordsskyddad. Ta bort lösenordet först.",
    "This file is not a PDF.": "Filen är ingen PDF.",
}


def M(key: str, **fmt) -> str:
    en, sv = MESSAGES[key]
    return (en if LANG == "en" else sv).format(**fmt)


def tr(text: str) -> str:
    """Translate a message from the shared engine."""
    return text if LANG == "en" else ENGINE_SV.get(text, text)


def font_label(label: str) -> str:
    """Swedish names for the style words in font labels such as 'Times Bold Italic'."""
    if LANG == "en":
        return label
    return label.replace(" Bold", " Fet").replace(" Italic", " Kursiv")


def font_list() -> list[dict]:
    fonts = font_choices()
    if LANG != "en":
        for f in fonts:
            if f["value"] == "auto":
                f["label"] = "Matcha originalet"
    return fonts


class ApiError(Exception):
    def __init__(self, status: int, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.detail = detail


def get_doc(doc_id: str) -> EditorDocument:
    ed = DOCS.get(doc_id)
    if ed is None:
        raise ApiError(404, M("doc_closed"))
    return ed


def check_page(ed: EditorDocument, page: int) -> None:
    if not 0 <= page < ed.doc.page_count:
        raise ApiError(400, M("no_page", n=page + 1))


def check_version(ed: EditorDocument, version) -> None:
    if version is not None and version != ed.version:
        raise ApiError(409, M("version"))


def run_edit(ed: EditorDocument, fn):
    """Checkpoint, run an edit, commit. Roll back if it fails."""
    ed.checkpoint()
    try:
        result = fn()
        if getattr(result, "font_source", None) == "unchanged":
            ed.discard_checkpoint()
            return result
    except ApiError:
        ed.rollback()
        raise
    except Exception as exc:
        ed.rollback()
        raise ApiError(422, tr(str(exc))) from exc
    ed.commit()
    return result


def edited_name(name: str) -> str:
    stem = name[:-4] if name.lower().endswith(".pdf") else name
    return f"{stem}-edited.pdf"


# --------------------------------------------------------------------------
# Routes. Each takes (match groups..., query, body) and returns a dict (JSON)
# or a (mime, bytes, filename) tuple.
# --------------------------------------------------------------------------

def open_document(query, body, upload, upload_name):
    if upload is None:
        raise ApiError(400, M("no_file"))
    try:
        ed = EditorDocument(upload, upload_name or "document.pdf")
    except ValueError as exc:
        raise ApiError(400, tr(str(exc))) from exc
    except Exception as exc:
        raise ApiError(400, M("open_fail")) from exc
    doc_id = uuid.uuid4().hex[:12]
    DOCS[doc_id] = ed
    return {"id": doc_id, **ed.meta()}


def close_document(doc_id):
    ed = DOCS.pop(doc_id, None)
    if ed:
        ed.doc.close()
    return {"ok": True}


def page_image(doc_id, page, query):
    ed = get_doc(doc_id)
    page = int(page)
    check_page(ed, page)
    zoom = max(0.25, min(float(query.get("zoom", 2.0)), 6.0))
    return ("image/png", ed.render(page, zoom), None)


def page_units(doc_id, page):
    ed = get_doc(doc_id)
    page = int(page)
    check_page(ed, page)
    return {"version": ed.version, "units": ed.units_json(page)}


def edit(doc_id, body):
    ed = get_doc(doc_id)
    check_version(ed, body.get("version"))
    page = body["page"]
    check_page(ed, page)
    units = ed.units(page)
    if not 0 <= body["unit"] < len(units):
        raise ApiError(400, M("text_gone"))
    unit = units[body["unit"]]
    if not unit.horizontal:
        raise ApiError(422, M("rotated"))
    result = run_edit(ed, lambda: edit_unit(
        ed.doc, ed.doc[page], unit, body["text"], ed.resolver,
        font=body.get("font"), size=body.get("size"), color=body.get("color"),
        fit=bool(body.get("fit")), bold=body.get("bold"), italic=body.get("italic")))
    return {**ed.meta(), "changedPages": [page],
            "font": {"label": font_label(result.font_label), "source": result.font_source}}


def replace(doc_id, body):
    ed = get_doc(doc_id)
    check_version(ed, body.get("version"))
    if not body.get("find"):
        raise ApiError(400, M("find_empty"))
    ed.checkpoint()
    try:
        count, pages = replace_text(ed.doc, body["find"], body.get("replace", ""), ed.resolver,
                                    case_sensitive=bool(body.get("caseSensitive")),
                                    whole_word=bool(body.get("wholeWord")),
                                    fit=bool(body.get("fit")))
    except Exception as exc:
        ed.rollback()
        raise ApiError(422, tr(str(exc))) from exc
    if count:
        ed.commit()
    else:
        ed.rollback()  # nothing changed, so do not leave an empty undo step
    return {**ed.meta(), "count": count, "changedPages": pages}


def find(doc_id, body):
    """Count matches without changing anything (for the live counter)."""
    ed = get_doc(doc_id)
    if not body.get("find"):
        return {"count": 0, "pages": []}
    pattern = re.escape(body["find"])
    if body.get("wholeWord"):
        pattern = rf"(?<!\w){pattern}(?!\w)"
    rx = re.compile(pattern, 0 if body.get("caseSensitive") else re.IGNORECASE)
    total, pages = 0, []
    for pno in range(ed.doc.page_count):
        n = sum(len(rx.findall(u.text)) for u in ed.units(pno) if u.horizontal)
        if n:
            total += n
            pages.append(pno)
    return {"count": total, "pages": pages}


def add(doc_id, body):
    ed = get_doc(doc_id)
    check_version(ed, body.get("version"))
    page = body["page"]
    check_page(ed, page)
    if not body.get("text", "").strip():
        raise ApiError(400, M("add_empty"))
    result = run_edit(ed, lambda: add_text(
        ed.doc, ed.doc[page], body["x"], body["y"], body["text"],
        body.get("size", 12), body.get("color", "#000000"), body.get("font"), ed.resolver,
        bold=bool(body.get("bold")), italic=bool(body.get("italic"))))
    return {**ed.meta(), "changedPages": [page],
            "font": {"label": font_label(result.font_label), "source": result.font_source}}


def search_rects(doc_id, body):
    """Where does this text appear? Rectangles are in displayed page coordinates, like the units."""
    ed = get_doc(doc_id)
    text = (body.get("text") or "").strip()
    if not text:
        raise ApiError(400, M("find_empty"))
    out = []
    for pno in range(ed.doc.page_count):
        page = ed.doc[pno]
        matrix = page.rotation_matrix
        for hit in page.search_for(text):
            r = hit * matrix
            out.append({"page": pno, "rect": [round(r.x0, 2), round(r.y0, 2), round(r.x1, 2), round(r.y1, 2)]})
    return {"rects": out}


def redact(doc_id, body):
    """Remove the text and image pixels under each rectangle (true redaction, not a cover-up)."""
    ed = get_doc(doc_id)
    check_version(ed, body.get("version"))
    items = body.get("rects") or []
    if not items:
        raise ApiError(400, M("redact_empty"))

    def work():
        touched = set()
        for item in items:
            check_page(ed, item["page"])
            page = ed.doc[item["page"]]
            rect = pymupdf.Rect(*item["rect"]) * page.derotation_matrix
            rect.normalize()
            page.add_redact_annot(rect, fill=(0, 0, 0))
            touched.add(item["page"])
        for pno in touched:
            ed.doc[pno].apply_redactions()

    run_edit(ed, work)
    return {**ed.meta(), "count": len(items)}


# ---- one-shot tools: a PDF goes in with the request, a new PDF comes out ---------------

COMPRESS_LEVELS = {"low": (150, 72), "medium": (110, 65), "high": (72, 50)}   # (target dpi, JPEG quality)


def open_pdf(data, password=None):
    """Open a PDF from bytes. A password-protected file needs the right password."""
    try:
        doc = pymupdf.open(stream=data, filetype="pdf")
    except Exception as exc:
        raise ApiError(400, M("open_fail")) from exc
    if doc.needs_pass:
        if password is None:
            raise ApiError(403, M("needs_password"))
        if not doc.authenticate(password):
            raise ApiError(403, M("wrong_password"))
    return doc


NOT_COMMENTS = ("Link", "Widget", "Popup")   # links and form fields are not comments


def annot_types(doc):
    """How many annotations of each kind the file has, e.g. {"Highlight": 3, "Text": 1}."""
    counts = {}
    for page in doc:
        for a in (page.annots() or []):
            name = a.type[1]
            if name not in NOT_COMMENTS:
                counts[name] = counts.get(name, 0) + 1
    return counts


def pdf_info(q, body, upload, upload_name):
    if upload is None:
        raise ApiError(400, M("no_file"))
    try:
        doc = pymupdf.open(stream=upload, filetype="pdf")
    except Exception as exc:
        raise ApiError(400, M("open_fail")) from exc
    wanted = pymupdf.PDF_PERM_PRINT | pymupdf.PDF_PERM_COPY | pymupdf.PDF_PERM_MODIFY
    limited = (not doc.needs_pass) and doc.permissions != -1 and (doc.permissions & wanted) != wanted
    types, widgets = {}, 0
    if not doc.needs_pass:
        types = annot_types(doc)
        for page in doc:
            widgets += sum(1 for _ in (page.widgets() or []))
    annots = sum(types.values())
    return {"needsPass": bool(doc.needs_pass), "encrypted": bool(doc.is_encrypted), "limited": bool(limited),
            "pages": 0 if doc.needs_pass else doc.page_count, "repaired": bool(doc.is_repaired),
            "annots": annots, "annotTypes": types, "widgets": widgets}


def compress(q, body, upload, upload_name):
    """Smaller file: lower the resolution of large images, subset fonts and tidy the structure."""
    if upload is None:
        raise ApiError(400, M("no_file"))
    dpi, quality = COMPRESS_LEVELS.get(body.get("level"), COMPRESS_LEVELS["medium"])
    doc = open_pdf(upload)
    try:
        doc.rewrite_images(dpi_threshold=dpi + 20, dpi_target=dpi, quality=quality)
    except Exception:
        pass  # an engine without this feature, or an odd image: the structural savings still apply
    try:
        doc.subset_fonts()
    except Exception:
        pass
    data = doc.tobytes(garbage=4, deflate=True, deflate_images=True, deflate_fonts=True, clean=True, use_objstms=1)
    return ("application/pdf", data, None)


def protect(q, body, upload, upload_name):
    """AES-256 password to open. The owner password is random, so nobody can lift the limits."""
    if upload is None:
        raise ApiError(400, M("no_file"))
    password = body.get("password") or ""
    if not password:
        raise ApiError(400, M("pw_empty"))
    doc = open_pdf(upload)
    perm = pymupdf.PDF_PERM_ACCESSIBILITY
    if body.get("print", True):
        perm |= pymupdf.PDF_PERM_PRINT | pymupdf.PDF_PERM_PRINT_HQ
    if body.get("copy", True):
        perm |= pymupdf.PDF_PERM_COPY
    if body.get("edit", False):
        perm |= pymupdf.PDF_PERM_MODIFY | pymupdf.PDF_PERM_ANNOTATE | pymupdf.PDF_PERM_FORM | pymupdf.PDF_PERM_ASSEMBLE
    data = doc.tobytes(encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw=password, owner_pw=secrets.token_urlsafe(18),
                       permissions=perm, garbage=3, deflate=True)
    return ("application/pdf", data, None)


def unlock(q, body, upload, upload_name):
    """Remove the password and the limits from a file the user can open."""
    if upload is None:
        raise ApiError(400, M("no_file"))
    doc = open_pdf(upload, body.get("password"))
    data = doc.tobytes(encryption=pymupdf.PDF_ENCRYPT_NONE, garbage=3, deflate=True)
    return ("application/pdf", data, None)


def undo(doc_id):
    ed = get_doc(doc_id)
    if not ed.undo():
        raise ApiError(400, M("nothing_undo"))
    return {**ed.meta(), "changedPages": list(range(ed.doc.page_count))}


def redo(doc_id):
    ed = get_doc(doc_id)
    if not ed.redo():
        raise ApiError(400, M("nothing_redo"))
    return {**ed.meta(), "changedPages": list(range(ed.doc.page_count))}


def download(doc_id, query):
    ed = get_doc(doc_id)
    keep = query.get("keep_metadata") == "true"
    return ("application/pdf", ed.export(strip_metadata=not keep), edited_name(ed.name))


def list_fonts():
    return {"fonts": font_list()}


def add_font(query, body, upload, upload_name):
    """Keep a font file in this tab's memory so it can be matched and offered."""
    if upload is None:
        raise ApiError(400, M("no_font"))
    name = re.sub(r"[^A-Za-z0-9._-]", "_", Path(upload_name or "font.ttf").name)
    if Path(name).suffix.lower() not in FONT_EXTS:
        raise ApiError(400, M("bad_ext"))
    USER_FONT_DIR.mkdir(parents=True, exist_ok=True)
    path = USER_FONT_DIR / name
    path.write_bytes(upload)
    FONT_INDEX.refresh()
    if not any(f["path"] == str(path) for f in FONT_INDEX.user_fonts()):
        path.unlink(missing_ok=True)
        FONT_INDEX.refresh()
        raise ApiError(400, M("bad_font"))
    return {"fonts": font_list()}


# --------------------------------------------------------------------------
# Dispatcher: called from worker.js
# --------------------------------------------------------------------------

DOC = r"/api/docs/(?P<id>[0-9a-f]+)"
def strip_annots(q, body, upload, upload_name):
    """Delete comments, highlights, drawings and stamps (all of them, or just the listed kinds)."""
    if upload is None:
        raise ApiError(400, M("no_file"))
    doc = open_pdf(upload, body.get("password"))
    kinds = body.get("types")
    for page in doc:
        for a in list(page.annots() or []):
            name = a.type[1]
            if name not in NOT_COMMENTS and (not kinds or name in kinds):
                page.delete_annot(a)
    return ("application/pdf", doc.tobytes(garbage=3, deflate=True), None)


def repair(q, body, upload, upload_name):
    """Open the file the lenient way (MuPDF rebuilds a broken structure) and write it out clean."""
    if upload is None:
        raise ApiError(400, M("no_file"))
    try:
        doc = pymupdf.open(stream=upload, filetype="pdf")
        if doc.needs_pass:
            raise ApiError(403, M("needs_password"))
        if doc.page_count == 0:
            raise ValueError("no pages")
        for number in range(doc.page_count):
            doc.load_page(number)
    except ApiError:
        raise
    except Exception as exc:
        raise ApiError(400, M("repair_fail")) from exc
    return ("application/pdf", doc.tobytes(garbage=4, clean=True, deflate=True), None)


def flatten(q, body, upload, upload_name):
    """Turn comments, highlights and form fields into ordinary page content."""
    if upload is None:
        raise ApiError(400, M("no_file"))
    doc = open_pdf(upload, body.get("password"))
    doc.bake(annots=bool(body.get("annots", True)), widgets=bool(body.get("widgets", True)))
    return ("application/pdf", doc.tobytes(garbage=3, deflate=True), None)


def image_refs(doc, smallest):
    """Every distinct image in the file, once, skipping the ones smaller than `smallest` pixels."""
    seen, refs = set(), []
    for page in doc:
        for img in page.get_images(full=True):
            xref, smask, w, h = img[0], img[1], img[2], img[3]
            if xref in seen or min(w, h) < smallest:
                continue
            seen.add(xref)
            refs.append({"xref": xref, "smask": smask, "page": page.number + 1, "w": w, "h": h})
    return refs


def images_list(q, body, upload, upload_name):
    if upload is None:
        raise ApiError(400, M("no_file"))
    doc = open_pdf(upload, body.get("password"))
    refs = image_refs(doc, int(body.get("min", 0)))
    return {"count": len(refs), "pages": len({r["page"] for r in refs}), "items": [{"page": r["page"], "w": r["w"], "h": r["h"]} for r in refs]}


def extract_images(q, body, upload, upload_name):
    """All images as a ZIP. JPEGs are copied byte for byte; masks, CMYK and other formats become PNG."""
    if upload is None:
        raise ApiError(400, M("no_file"))
    doc = open_pdf(upload, body.get("password"))
    prefix = "image" if LANG == "en" else "bild"
    out, per_page = io.BytesIO(), {}
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for r in image_refs(doc, int(body.get("min", 0))):
            try:
                info = doc.extract_image(r["xref"])
                plain = r["smask"] == 0 and info["ext"] in ("jpeg", "png") and info["colorspace"] in (1, 3)
                if plain:
                    data, ext = info["image"], "jpg" if info["ext"] == "jpeg" else "png"
                else:
                    pix = pymupdf.Pixmap(doc, r["xref"])
                    if pix.colorspace is not None and pix.colorspace.n != 3 and pix.colorspace.n != 1:
                        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
                    if r["smask"] and not pix.alpha:
                        pix = pymupdf.Pixmap(pix, pymupdf.Pixmap(doc, r["smask"]))
                    data, ext = pix.tobytes("png"), "png"
            except Exception:
                continue
            n = per_page[r["page"]] = per_page.get(r["page"], 0) + 1
            z.writestr(f"{prefix}-{r['page']}-{n}.{ext}", data)
    if not per_page:
        raise ApiError(404, M("no_images"))
    return ("application/zip", out.getvalue(), None)


ROUTES = [
    ("POST", r"/api/docs", lambda m, q, b, u, n: open_document(q, b, u, n)),
    ("DELETE", DOC, lambda m, q, b, u, n: close_document(m["id"])),
    ("GET", DOC + r"/pages/(?P<page>\d+)/image", lambda m, q, b, u, n: page_image(m["id"], m["page"], q)),
    ("GET", DOC + r"/pages/(?P<page>\d+)/units", lambda m, q, b, u, n: page_units(m["id"], m["page"])),
    ("POST", DOC + r"/edit", lambda m, q, b, u, n: edit(m["id"], b)),
    ("POST", DOC + r"/replace", lambda m, q, b, u, n: replace(m["id"], b)),
    ("POST", DOC + r"/find", lambda m, q, b, u, n: find(m["id"], b)),
    ("POST", DOC + r"/add-text", lambda m, q, b, u, n: add(m["id"], b)),
    ("POST", r"/api/pdf-info", lambda m, q, b, u, n: pdf_info(q, b, u, n)),
    ("POST", r"/api/compress", lambda m, q, b, u, n: compress(q, b, u, n)),
    ("POST", r"/api/protect", lambda m, q, b, u, n: protect(q, b, u, n)),
    ("POST", r"/api/unlock", lambda m, q, b, u, n: unlock(q, b, u, n)),
    ("POST", r"/api/repair", lambda m, q, b, u, n: repair(q, b, u, n)),
    ("POST", r"/api/flatten", lambda m, q, b, u, n: flatten(q, b, u, n)),
    ("POST", r"/api/strip-annots", lambda m, q, b, u, n: strip_annots(q, b, u, n)),
    ("POST", r"/api/images", lambda m, q, b, u, n: images_list(q, b, u, n)),
    ("POST", r"/api/extract-images", lambda m, q, b, u, n: extract_images(q, b, u, n)),
    ("POST", DOC + r"/search-rects", lambda m, q, b, u, n: search_rects(m["id"], b)),
    ("POST", DOC + r"/redact", lambda m, q, b, u, n: redact(m["id"], b)),
    ("POST", DOC + r"/undo", lambda m, q, b, u, n: undo(m["id"])),
    ("POST", DOC + r"/redo", lambda m, q, b, u, n: redo(m["id"])),
    ("GET", DOC + r"/download", lambda m, q, b, u, n: download(m["id"], q)),
    ("GET", r"/api/fonts", lambda m, q, b, u, n: list_fonts()),
    ("POST", r"/api/fonts", lambda m, q, b, u, n: add_font(q, b, u, n)),
]
ROUTES = [(method, re.compile(pattern + "$"), fn) for method, pattern, fn in ROUTES]


def dispatch(method, url, body_json, upload, upload_name, lang=None):
    """Returns (status, kind, payload, filename).

    kind is "json" (payload is a JSON string), "bytes" (payload is bytes, the
    filename is the download name) or "error" (payload is the message).
    """
    global LANG
    LANG = "en" if lang == "en" else "sv"
    parts = urlsplit(url)
    query = {k: v[0] for k, v in parse_qs(parts.query).items()}
    # JS null arrives as a JsNull object rather than None, so treat both as absent.
    body = json.loads(body_json) if isinstance(body_json, str) and body_json else {}
    upload = bytes(upload.to_py()) if hasattr(upload, "to_py") else None
    upload_name = upload_name if isinstance(upload_name, str) else None
    try:
        for route_method, rx, fn in ROUTES:
            m = rx.match(parts.path)
            if route_method == method and m:
                result = fn(m.groupdict(), query, body, upload, upload_name)
                if isinstance(result, tuple):
                    mime, data, filename = result
                    return (200, mime, data, filename)
                return (200, "json", json.dumps(result), None)
        raise ApiError(404, M("route", method=method, path=parts.path))
    except ApiError as exc:
        return (exc.status, "error", exc.detail, None)
    except Exception as exc:  # engine errors should reach the UI as readable text
        return (500, "error", tr(str(exc)) or exc.__class__.__name__, None)
