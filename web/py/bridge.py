"""Browser entry point. Runs inside Pyodide in a Web Worker.

Mirrors the routes in app.py, minus FastAPI, so the frontend can keep the same
route names. Nothing here touches the network; documents live in memory in
this worker and disappear when the tab closes.
"""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from pdfedit.core import EditorDocument, add_text, edit_unit, replace_text
from pdfedit.fonts import FONT_EXTS, FONT_INDEX, USER_FONT_DIR, font_choices

DOCS: dict[str, EditorDocument] = {}


class ApiError(Exception):
    def __init__(self, status: int, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.detail = detail


def get_doc(doc_id: str) -> EditorDocument:
    ed = DOCS.get(doc_id)
    if ed is None:
        raise ApiError(404, "This document is no longer open. Open it again.")
    return ed


def check_page(ed: EditorDocument, page: int) -> None:
    if not 0 <= page < ed.doc.page_count:
        raise ApiError(400, f"Page {page + 1} does not exist.")


def check_version(ed: EditorDocument, version) -> None:
    if version is not None and version != ed.version:
        raise ApiError(409, "The document changed in the meantime. Reload the page view and try again.")


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
        raise ApiError(422, str(exc)) from exc
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
        raise ApiError(400, "No file received.")
    try:
        ed = EditorDocument(upload, upload_name or "document.pdf")
    except ValueError as exc:
        raise ApiError(400, str(exc)) from exc
    except Exception as exc:
        raise ApiError(400, "This file could not be opened as a PDF.") from exc
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
        raise ApiError(400, "That text is no longer on the page. Reload and try again.")
    unit = units[body["unit"]]
    if not unit.horizontal:
        raise ApiError(422, "Rotated or vertical text cannot be edited yet.")
    result = run_edit(ed, lambda: edit_unit(
        ed.doc, ed.doc[page], unit, body["text"], ed.resolver,
        font=body.get("font"), size=body.get("size"), color=body.get("color"),
        fit=bool(body.get("fit")), bold=body.get("bold"), italic=body.get("italic")))
    return {**ed.meta(), "changedPages": [page],
            "font": {"label": result.font_label, "source": result.font_source}}


def replace(doc_id, body):
    ed = get_doc(doc_id)
    check_version(ed, body.get("version"))
    if not body.get("find"):
        raise ApiError(400, "Type the text you want to find.")
    ed.checkpoint()
    try:
        count, pages = replace_text(ed.doc, body["find"], body.get("replace", ""), ed.resolver,
                                    case_sensitive=bool(body.get("caseSensitive")),
                                    whole_word=bool(body.get("wholeWord")),
                                    fit=bool(body.get("fit")))
    except Exception as exc:
        ed.rollback()
        raise ApiError(422, str(exc)) from exc
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
        raise ApiError(400, "Type some text to add.")
    result = run_edit(ed, lambda: add_text(
        ed.doc, ed.doc[page], body["x"], body["y"], body["text"],
        body.get("size", 12), body.get("color", "#000000"), body.get("font"), ed.resolver,
        bold=bool(body.get("bold")), italic=bool(body.get("italic"))))
    return {**ed.meta(), "changedPages": [page],
            "font": {"label": result.font_label, "source": result.font_source}}


def undo(doc_id):
    ed = get_doc(doc_id)
    if not ed.undo():
        raise ApiError(400, "Nothing to undo.")
    return {**ed.meta(), "changedPages": list(range(ed.doc.page_count))}


def redo(doc_id):
    ed = get_doc(doc_id)
    if not ed.redo():
        raise ApiError(400, "Nothing to redo.")
    return {**ed.meta(), "changedPages": list(range(ed.doc.page_count))}


def download(doc_id, query):
    ed = get_doc(doc_id)
    keep = query.get("keep_metadata") == "true"
    return ("application/pdf", ed.export(strip_metadata=not keep), edited_name(ed.name))


def list_fonts():
    return {"fonts": font_choices()}


def add_font(query, body, upload, upload_name):
    """Keep a font file in this tab's memory so it can be matched and offered."""
    if upload is None:
        raise ApiError(400, "No font file received.")
    name = re.sub(r"[^A-Za-z0-9._-]", "_", Path(upload_name or "font.ttf").name)
    if Path(name).suffix.lower() not in FONT_EXTS:
        raise ApiError(400, "Add a .ttf, .otf or .ttc font file.")
    USER_FONT_DIR.mkdir(parents=True, exist_ok=True)
    path = USER_FONT_DIR / name
    path.write_bytes(upload)
    FONT_INDEX.refresh()
    if not any(f["path"] == str(path) for f in FONT_INDEX.user_fonts()):
        path.unlink(missing_ok=True)
        FONT_INDEX.refresh()
        raise ApiError(400, "That file does not look like a usable font.")
    return {"fonts": font_choices()}


# --------------------------------------------------------------------------
# Dispatcher: called from worker.js
# --------------------------------------------------------------------------

DOC = r"/api/docs/(?P<id>[0-9a-f]+)"
ROUTES = [
    ("POST", r"/api/docs", lambda m, q, b, u, n: open_document(q, b, u, n)),
    ("DELETE", DOC, lambda m, q, b, u, n: close_document(m["id"])),
    ("GET", DOC + r"/pages/(?P<page>\d+)/image", lambda m, q, b, u, n: page_image(m["id"], m["page"], q)),
    ("GET", DOC + r"/pages/(?P<page>\d+)/units", lambda m, q, b, u, n: page_units(m["id"], m["page"])),
    ("POST", DOC + r"/edit", lambda m, q, b, u, n: edit(m["id"], b)),
    ("POST", DOC + r"/replace", lambda m, q, b, u, n: replace(m["id"], b)),
    ("POST", DOC + r"/find", lambda m, q, b, u, n: find(m["id"], b)),
    ("POST", DOC + r"/add-text", lambda m, q, b, u, n: add(m["id"], b)),
    ("POST", DOC + r"/undo", lambda m, q, b, u, n: undo(m["id"])),
    ("POST", DOC + r"/redo", lambda m, q, b, u, n: redo(m["id"])),
    ("GET", DOC + r"/download", lambda m, q, b, u, n: download(m["id"], q)),
    ("GET", r"/api/fonts", lambda m, q, b, u, n: list_fonts()),
    ("POST", r"/api/fonts", lambda m, q, b, u, n: add_font(q, b, u, n)),
]
ROUTES = [(method, re.compile(pattern + "$"), fn) for method, pattern, fn in ROUTES]


def dispatch(method, url, body_json, upload, upload_name):
    """Returns (status, kind, payload, filename).

    kind is "json" (payload is a JSON string), "bytes" (payload is bytes, the
    filename is the download name) or "error" (payload is the message).
    """
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
        raise ApiError(404, f"Unknown route {method} {parts.path}")
    except ApiError as exc:
        return (exc.status, "error", exc.detail, None)
    except Exception as exc:  # engine errors should reach the UI as readable text
        return (500, "error", str(exc) or exc.__class__.__name__, None)
