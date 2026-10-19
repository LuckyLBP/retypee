"""Font matching for edited text.

Order of preference when writing new text:
  1. The font embedded in the PDF, if it has every glyph we need
     (often it does not, because PDFs embed only the letters they use).
  2. A font file with the same name in ./fonts or in the system font folders.
  3. A built-in standard font (Helvetica, Times or Courier) in the right style.
"""

from __future__ import annotations

import io
import json
import os
import platform
import re
import threading
from dataclasses import dataclass
from pathlib import Path

import pymupdf

APP_DIR = Path(__file__).resolve().parent.parent
USER_FONT_DIR = APP_DIR / "fonts"
CACHE_FILE = APP_DIR / ".font-index.json"
FONT_EXTS = {".ttf", ".otf", ".ttc", ".otc"}

SUBSET_PREFIX = re.compile(r"^[A-Z]{6}\+")
STYLE_NOISE = ("regular", "book", "roman", "normal", "mt", "ps", "std")


def strip_subset(name: str) -> str:
    return SUBSET_PREFIX.sub("", name or "")


def norm(name: str) -> str:
    """Lowercase, alphanumerics only, without subset prefix."""
    return re.sub(r"[^a-z0-9]", "", strip_subset(name).lower())


def loose(name: str) -> str:
    """Like norm() but also drops style noise such as 'Regular' or 'MT'."""
    s = norm(name)
    s = re.sub(r"ps(?=(bold|italic|bolditalic)?mt$)", "", s)  # TimesNewRomanPS-BoldMT
    s = re.sub(r"mt$", "", s)
    changed = True
    while changed:
        changed = False
        for word in STYLE_NOISE:
            if s.endswith(word) and len(s) > len(word) + 2:
                s = s[: -len(word)]
                changed = True
    return s


def system_font_dirs() -> list[Path]:
    home = Path.home()
    system = platform.system()
    if system == "Darwin":
        return [
            Path("/System/Library/Fonts"),
            Path("/System/Library/Fonts/Supplemental"),
            Path("/Library/Fonts"),
            home / "Library/Fonts",
        ]
    if system == "Windows":
        windir = Path(os.environ.get("WINDIR", "C:/Windows"))
        local = Path(os.environ.get("LOCALAPPDATA", ""))
        return [windir / "Fonts", local / "Microsoft/Windows/Fonts"]
    return [
        Path("/usr/share/fonts"),
        Path("/usr/local/share/fonts"),
        home / ".fonts",
        home / ".local/share/fonts",
    ]


# --------------------------------------------------------------------------
# Index of local font files: name key -> (path, index inside a collection)
# --------------------------------------------------------------------------

class FontIndex:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._exact: dict[str, tuple[str, int]] = {}
        self._loose: dict[str, tuple[str, int]] = {}
        self._user_fonts: list[dict] = []
        self._ready = False

    def _font_files(self, dirs: list[Path]):
        for d in dirs:
            if not d.is_dir():
                continue
            for root, _, files in os.walk(d):
                for f in files:
                    if Path(f).suffix.lower() in FONT_EXTS:
                        yield Path(root) / f

    @staticmethod
    def _names(path: Path) -> list[tuple[int, list[str], str]]:
        """Return [(index, [name candidates], display name)] for a font file."""
        from fontTools.ttLib import TTCollection, TTFont

        out = []
        try:
            if path.suffix.lower() in (".ttc", ".otc"):
                fonts = TTCollection(str(path), lazy=True).fonts
            else:
                fonts = [TTFont(str(path), lazy=True)]
            for i, font in enumerate(fonts):
                table = font["name"]
                ps = table.getDebugName(6) or ""
                full = table.getDebugName(4) or ""
                fam = table.getDebugName(16) or table.getDebugName(1) or ""
                sub = table.getDebugName(17) or table.getDebugName(2) or ""
                cands = [n for n in (ps, full, fam + sub, fam + "-" + sub) if n]
                out.append((i, cands, full or ps or path.stem))
        except Exception:
            pass
        return out

    def _signature(self) -> str:
        parts = []
        for d in [USER_FONT_DIR, *system_font_dirs()]:
            try:
                parts.append(f"{d}:{d.stat().st_mtime_ns}")
            except OSError:
                pass
        return "|".join(parts)

    def build(self) -> None:
        with self._lock:
            if self._ready:
                return
            sig = self._signature()
            data = None
            if CACHE_FILE.exists():
                try:
                    cached = json.loads(CACHE_FILE.read_text())
                    if cached.get("sig") == sig:
                        data = cached
                except Exception:
                    data = None
            if data is None:
                entries = []
                user_fonts = []
                # User folder first so it wins over system fonts with the same name.
                for is_user, dirs in ((True, [USER_FONT_DIR]), (False, system_font_dirs())):
                    for path in self._font_files(dirs):
                        for idx, cands, display in self._names(path):
                            entries.append([str(path), idx, cands])
                            if is_user:
                                user_fonts.append({"path": str(path), "index": idx, "name": display})
                data = {"sig": sig, "entries": entries, "user": user_fonts}
                try:
                    CACHE_FILE.write_text(json.dumps(data))
                except OSError:
                    pass
            for path, idx, cands in data["entries"]:
                for c in cands:
                    self._exact.setdefault(norm(c), (path, idx))
                    self._loose.setdefault(loose(c), (path, idx))
            self._user_fonts = data["user"]
            self._ready = True

    def lookup(self, pdf_font_name: str) -> tuple[str, int] | None:
        self.build()
        hit = self._exact.get(norm(pdf_font_name)) or self._loose.get(loose(pdf_font_name))
        if hit:
            return hit
        # Metric-compatible stand-ins: same letter widths, near-identical look.
        key = loose(pdf_font_name)
        for original, alias in METRIC_ALIASES:
            if key.startswith(original):
                return self._loose.get(alias + key[len(original):])
        return None

    def user_fonts(self) -> list[dict]:
        self.build()
        return list(self._user_fonts)

    def refresh(self) -> None:
        with self._lock:
            self._ready = False
            self._exact.clear()
            self._loose.clear()
        try:
            CACHE_FILE.unlink()
        except OSError:
            pass
        self.build()


METRIC_ALIASES = [
    ("arial", "liberationsans"), ("helvetica", "liberationsans"),
    ("timesnewroman", "liberationserif"), ("times", "liberationserif"),
    ("couriernew", "liberationmono"), ("courier", "liberationmono"),
]

FONT_INDEX = FontIndex()
_FILE_FONT_CACHE: dict[tuple[str, int], pymupdf.Font] = {}


def load_font_file(path: str, index: int = 0) -> pymupdf.Font:
    key = (path, index)
    if key not in _FILE_FONT_CACHE:
        if path.lower().endswith((".ttc", ".otc")):
            from fontTools.ttLib import TTCollection

            buf = io.BytesIO()
            TTCollection(path).fonts[index].save(buf)
            _FILE_FONT_CACHE[key] = pymupdf.Font(fontbuffer=buf.getvalue())
        else:
            _FILE_FONT_CACHE[key] = pymupdf.Font(fontfile=path)
    return _FILE_FONT_CACHE[key]


# --------------------------------------------------------------------------
# Built-in fallback fonts
# --------------------------------------------------------------------------

BASE14 = {
    "sans": ("helv", "hebo", "heit", "hebi"),
    "serif": ("tiro", "tibo", "tiit", "tibi"),
    "mono": ("cour", "cobo", "coit", "cobi"),
}
BASE14_LABEL = {"sans": "Helvetica", "serif": "Times", "mono": "Courier"}
SERIF_HINTS = ("times", "serif", "georgia", "garamond", "roman", "cambria", "minion",
               "baskerville", "palatino", "bodoni", "didot", "caslon", "merriweather")
MONO_HINTS = ("mono", "courier", "consol", "menlo", "code")


def style_of(font_name: str, flags: int) -> tuple[bool, bool]:
    n = font_name.lower()
    bold = bool(flags & 16) or any(k in n for k in ("bold", "black", "heavy", "semibold", "demi"))
    italic = bool(flags & 2) or "italic" in n or "oblique" in n
    return bold, italic


def family_of(font_name: str, flags: int) -> str:
    n = font_name.lower()
    if bool(flags & 8) or any(k in n for k in MONO_HINTS):
        return "mono"
    if "sans" not in n and any(k in n for k in SERIF_HINTS):
        return "serif"
    return "sans"


def base14_font(family: str, bold: bool, italic: bool) -> tuple[pymupdf.Font, str]:
    code = BASE14[family][(1 if bold else 0) + (2 if italic else 0)]
    label = BASE14_LABEL[family] + (" Bold" if bold else "") + (" Italic" if italic else "")
    return pymupdf.Font(code), label


STYLE_WORDS = re.compile(r"[-, ]*(bold|italic|oblique|regular|medium|semibold|light|black|heavy|book|roman|mt)+$", re.I)


def styled_names(font_name: str, bold: bool, italic: bool) -> list[str]:
    """Candidate names for the same family in another style, e.g. Arial-BoldMT."""
    family = strip_subset(font_name)
    while True:
        shorter = STYLE_WORDS.sub("", family)
        if shorter == family or not shorter:
            break
        family = shorter
    suffix = ("Bold" if bold else "") + ("Italic" if italic else "") or "Regular"
    return [f"{family}-{suffix}", f"{family}{suffix}", f"{family} {suffix}"] + (
        [family] if suffix == "Regular" else [])


def covers(font: pymupdf.Font, text: str) -> bool:
    return all(font.has_glyph(ord(c)) for c in text if not c.isspace())


# --------------------------------------------------------------------------
# Resolver
# --------------------------------------------------------------------------

@dataclass
class ResolvedFont:
    font: pymupdf.Font
    label: str     # human readable font name
    source: str    # "embedded", "local", "standard"


class FontResolver:
    """Resolves fonts for one open document. Cache is cleared on every change."""

    def __init__(self, doc: pymupdf.Document) -> None:
        self.doc = doc
        self._embedded: dict[tuple[int, str], pymupdf.Font | None] = {}

    def reset(self) -> None:
        self._embedded.clear()

    def _embedded_font(self, page: pymupdf.Page, span_font: str) -> pymupdf.Font | None:
        """The embedded font, if it can be reused safely.

        Only TrueType/OpenType files are reused. Bare CFF and Type1 programs
        extracted from PDFs often lose their metrics or encoding when loaded on
        their own, which draws letters in the wrong place or not at all."""
        key = (page.number, norm(span_font))
        if key in self._embedded:
            return self._embedded[key]
        result = None
        candidates = {xref: ext for xref, ext, _t, basefont, *_ in page.get_fonts(full=True)
                      if norm(basefont) == key[1]}
        # Several different font programs with the same name (common: a
        # TrueType subset and a CFF copy of Arial) make it impossible to tell
        # which one a given line uses, so don't reuse any of them.
        if len(candidates) == 1:
            xref, ext = next(iter(candidates.items()))
            if ext in ("ttf", "otf", "cff"):
                try:
                    _, _, _, buf = self.doc.extract_font(xref)
                    if buf:
                        result = pymupdf.Font(fontbuffer=buf)
                except Exception:
                    result = None
        self._embedded[key] = result
        return result

    @staticmethod
    def _outlines_present(span_font: str, text: str, drawn: set[str] | None) -> bool:
        """Embedded fonts are usually subsets: they keep only the letters the
        PDF uses, often without saying so in their name, while their character
        map can still claim the whole alphabet. So reuse the embedded font only
        for letters the PDF has already drawn with it."""
        if drawn is None:
            return False
        return all(c in drawn for c in text if not c.isspace())

    def resolve(self, page: pymupdf.Page, span_font: str, flags: int,
                old_text: str, new_text: str, override: str | None = None,
                bold: bool | None = None, italic: bool | None = None,
                drawn: set[str] | None = None) -> ResolvedFont:
        orig_bold, orig_italic = style_of(span_font, flags)
        bold = orig_bold if bold is None else bold
        italic = orig_italic if italic is None else italic
        restyled = (bold, italic) != (orig_bold, orig_italic)

        if override and override != "auto":
            if override.startswith("file:"):
                path, _, idx = override[5:].rpartition("#")
                font = load_font_file(path, int(idx or 0))
                return ResolvedFont(font, Path(path).stem, "local")
            if override in BASE14:
                font, label = base14_font(override, bold, italic)
                return ResolvedFont(font, label, "standard")

        if not restyled:
            # 1. Embedded font. It must cover the old text as well, which proves
            #    that its character map is usable and not a raw glyph-id subset.
            emb = self._embedded_font(page, span_font)
            if emb is not None and covers(emb, old_text) and covers(emb, new_text) \
                    and self._outlines_present(span_font, new_text, drawn):
                return ResolvedFont(emb, strip_subset(span_font), "embedded")
            names = [span_font]
        else:
            names = styled_names(span_font, bold, italic)

        # 2. A local font file with the same name (or the same family in the new style).
        for name in names:
            hit = FONT_INDEX.lookup(name)
            if not hit:
                continue
            try:
                font = load_font_file(*hit)
                if covers(font, new_text):
                    return ResolvedFont(font, strip_subset(name), "local")
            except Exception:
                pass

        # 3. Standard font in a matching style.
        font, label = base14_font(family_of(span_font, flags), bold, italic)
        if covers(font, new_text):
            return ResolvedFont(font, label, "standard")
        return ResolvedFont(pymupdf.Font("cjk"), "Droid Sans Fallback", "standard")


def font_choices() -> list[dict]:
    choices = [
        {"value": "auto", "label": "Match original"},
        {"value": "sans", "label": "Helvetica"},
        {"value": "serif", "label": "Times"},
        {"value": "mono", "label": "Courier"},
    ]
    for f in FONT_INDEX.user_fonts():
        choices.append({"value": f"file:{f['path']}#{f['index']}", "label": f["name"]})
    return choices
