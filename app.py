"""Local PDF text editor. Run:  python app.py   then open http://127.0.0.1:8765"""

from __future__ import annotations

import json
import os
import threading
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import quote

import pymupdf
import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from typing import Optional

from pydantic import BaseModel

from pdfedit.core import EditorDocument, add_text, edit_unit, replace_text
from pdfedit.fonts import FONT_INDEX, font_choices

APP_DIR = Path(__file__).resolve().parent
HOST = os.environ.get("PDF_EDITOR_HOST", "127.0.0.1")
PORT = int(os.environ.get("PDF_EDITOR_PORT", "8765"))

@asynccontextmanager
async def lifespan(_app):
    # Scanning installed fonts takes a few seconds the first time; do it in the background.
    threading.Thread(target=FONT_INDEX.build, daemon=True).start()
    yield


app = FastAPI(title="PDF Text Editor", lifespan=lifespan)

# Open documents live in memory for as long as the server runs.
DOCS: dict[str, EditorDocument] = {}
LOCKS: dict[str, threading.Lock] = {}


def get_doc(doc_id: str) -> tuple[EditorDocument, threading.Lock]:
    ed = DOCS.get(doc_id)
    if ed is None:
        raise HTTPException(404, "This document is no longer open. Upload it again.")
    return ed, LOCKS[doc_id]


def check_page(ed: EditorDocument, page: int) -> None:
    if not 0 <= page < ed.doc.page_count:
        raise HTTPException(400, f"Page {page + 1} does not exist.")


def check_version(ed: EditorDocument, version: int | None) -> None:
    if version is not None and version != ed.version:
        raise HTTPException(409, "The document changed in the meantime. Reload the page view and try again.")


def run_edit(ed: EditorDocument, fn):
    """Checkpoint, run an edit, commit. Roll back if it fails."""
    ed.checkpoint()
    try:
        result = fn()
        if getattr(result, "font_source", None) == "unchanged":
            ed.discard_checkpoint()
            return result
    except HTTPException:
        ed.rollback()
        raise
    except Exception as exc:  # surface engine errors as readable messages
        ed.rollback()
        raise HTTPException(422, str(exc)) from exc
    ed.commit()
    return result


# --------------------------------------------------------------------------
# Interactive editor API
# --------------------------------------------------------------------------

@app.post("/api/docs")
async def open_document(file: UploadFile = File(...)):
    data = await file.read()
    try:
        ed = EditorDocument(data, file.filename or "document.pdf")
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    except Exception as exc:
        raise HTTPException(400, "This file could not be opened as a PDF.") from exc
    doc_id = uuid.uuid4().hex[:12]
    DOCS[doc_id] = ed
    LOCKS[doc_id] = threading.Lock()
    return {"id": doc_id, **ed.meta()}


@app.get("/api/docs/{doc_id}")
def document_meta(doc_id: str):
    ed, _ = get_doc(doc_id)
    return {"id": doc_id, **ed.meta()}


@app.delete("/api/docs/{doc_id}")
def close_document(doc_id: str):
    ed = DOCS.pop(doc_id, None)
    LOCKS.pop(doc_id, None)
    if ed:
        ed.doc.close()
    return {"ok": True}


@app.get("/api/docs/{doc_id}/pages/{page}/image")
def page_image(doc_id: str, page: int, zoom: float = 2.0, v: str = ""):
    ed, lock = get_doc(doc_id)
    check_page(ed, page)
    zoom = max(0.25, min(zoom, 6.0))
    with lock:
        png = ed.render(page, zoom)
    return Response(png, media_type="image/png", headers={"Cache-Control": "private, max-age=3600"})


@app.get("/api/docs/{doc_id}/pages/{page}/units")
def page_units(doc_id: str, page: int):
    ed, lock = get_doc(doc_id)
    check_page(ed, page)
    with lock:
        return {"version": ed.version, "units": ed.units_json(page)}


class EditRequest(BaseModel):
    version: Optional[int] = None
    page: int
    unit: int
    text: str
    font: Optional[str] = None
    size: Optional[float] = None
    color: Optional[str] = None
    fit: bool = False
    bold: Optional[bool] = None
    italic: Optional[bool] = None


@app.post("/api/docs/{doc_id}/edit")
def edit(doc_id: str, req: EditRequest):
    ed, lock = get_doc(doc_id)
    with lock:
        check_version(ed, req.version)
        check_page(ed, req.page)
        units = ed.units(req.page)
        if not 0 <= req.unit < len(units):
            raise HTTPException(400, "That text is no longer on the page. Reload and try again.")
        unit = units[req.unit]
        if not unit.horizontal:
            raise HTTPException(422, "Rotated or vertical text cannot be edited yet.")
        result = run_edit(ed, lambda: edit_unit(
            ed.doc, ed.doc[req.page], unit, req.text, ed.resolver,
            font=req.font, size=req.size, color=req.color, fit=req.fit,
            bold=req.bold, italic=req.italic))
        return {**ed.meta(), "changedPages": [req.page],
                "font": {"label": result.font_label, "source": result.font_source}}


class ReplaceRequest(BaseModel):
    version: Optional[int] = None
    find: str
    replace: str
    caseSensitive: bool = False
    wholeWord: bool = False
    fit: bool = False


@app.post("/api/docs/{doc_id}/replace")
def replace(doc_id: str, req: ReplaceRequest):
    ed, lock = get_doc(doc_id)
    with lock:
        check_version(ed, req.version)
        if not req.find:
            raise HTTPException(400, "Type the text you want to find.")
        ed.checkpoint()
        try:
            count, pages = replace_text(ed.doc, req.find, req.replace, ed.resolver,
                                        case_sensitive=req.caseSensitive,
                                        whole_word=req.wholeWord, fit=req.fit)
        except Exception as exc:
            ed.rollback()
            raise HTTPException(422, str(exc)) from exc
        if count:
            ed.commit()
        else:
            ed.rollback()  # nothing changed, so do not leave an empty undo step
        return {**ed.meta(), "count": count, "changedPages": pages}


class FindRequest(BaseModel):
    find: str
    caseSensitive: bool = False
    wholeWord: bool = False


@app.post("/api/docs/{doc_id}/find")
def find(doc_id: str, req: FindRequest):
    """Count matches without changing anything (for the live counter)."""
    import re
    ed, lock = get_doc(doc_id)
    if not req.find:
        return {"count": 0, "pages": []}
    pattern = re.escape(req.find)
    if req.wholeWord:
        pattern = rf"(?<!\w){pattern}(?!\w)"
    rx = re.compile(pattern, 0 if req.caseSensitive else re.IGNORECASE)
    total, pages = 0, []
    with lock:
        for pno in range(ed.doc.page_count):
            n = sum(len(rx.findall(u.text)) for u in ed.units(pno) if u.horizontal)
            if n:
                total += n
                pages.append(pno)
    return {"count": total, "pages": pages}


class AddTextRequest(BaseModel):
    version: Optional[int] = None
    page: int
    x: float
    y: float          # baseline, in displayed page coordinates
    text: str
    size: float = 12
    color: str = "#000000"
    font: Optional[str] = None
    bold: bool = False
    italic: bool = False


@app.post("/api/docs/{doc_id}/add-text")
def add(doc_id: str, req: AddTextRequest):
    ed, lock = get_doc(doc_id)
    with lock:
        check_version(ed, req.version)
        check_page(ed, req.page)
        if not req.text.strip():
            raise HTTPException(400, "Type some text to add.")
        result = run_edit(ed, lambda: add_text(ed.doc, ed.doc[req.page], req.x, req.y, req.text,
                                               req.size, req.color, req.font, ed.resolver,
                                               bold=req.bold, italic=req.italic))
        return {**ed.meta(), "changedPages": [req.page],
                "font": {"label": result.font_label, "source": result.font_source}}


@app.post("/api/docs/{doc_id}/undo")
def undo(doc_id: str):
    ed, lock = get_doc(doc_id)
    with lock:
        if not ed.undo():
            raise HTTPException(400, "Nothing to undo.")
        return {**ed.meta(), "changedPages": list(range(ed.doc.page_count))}


@app.post("/api/docs/{doc_id}/redo")
def redo(doc_id: str):
    ed, lock = get_doc(doc_id)
    with lock:
        if not ed.redo():
            raise HTTPException(400, "Nothing to redo.")
        return {**ed.meta(), "changedPages": list(range(ed.doc.page_count))}


def pdf_response(data: bytes, filename: str, extra_headers: dict | None = None) -> Response:
    headers = {"Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename)}"}
    headers.update(extra_headers or {})
    return Response(data, media_type="application/pdf", headers=headers)


def edited_name(name: str) -> str:
    stem = name[:-4] if name.lower().endswith(".pdf") else name
    return f"{stem}-edited.pdf"


@app.get("/api/docs/{doc_id}/download")
def download(doc_id: str, keep_metadata: bool = False):
    """Metadata is removed by default. Add ?keep_metadata=true to keep it."""
    ed, lock = get_doc(doc_id)
    with lock:
        data = ed.export(strip_metadata=not keep_metadata)
    return pdf_response(data, edited_name(ed.name))


@app.get("/api/fonts")
def fonts():
    return {"fonts": font_choices()}


@app.post("/api/fonts/refresh")
def refresh_fonts():
    FONT_INDEX.refresh()
    return {"fonts": font_choices()}


# --------------------------------------------------------------------------
# Automation API: one request in, edited PDF out
# --------------------------------------------------------------------------

@app.post("/api/replace")
async def replace_once(
    file: UploadFile = File(...),
    replacements: str = Form(..., description='JSON object {"old": "new", ...} or list of [old, new]'),
    case_sensitive: bool = Form(False),
    whole_word: bool = Form(False),
    fit: bool = Form(False),
    keep_metadata: bool = Form(False),
):
    """Example:
    curl -F file=@offer.pdf -F 'replacements={"2026-104":"2026-219"}' \\
         http://127.0.0.1:8765/api/replace -o offer-edited.pdf
    """
    try:
        pairs = json.loads(replacements)
        pairs = list(pairs.items()) if isinstance(pairs, dict) else [tuple(p) for p in pairs]
    except Exception as exc:
        raise HTTPException(400, 'replacements must be JSON, e.g. {"old text": "new text"}') from exc
    try:
        ed = EditorDocument(await file.read(), file.filename or "document.pdf")
    except Exception as exc:
        raise HTTPException(400, f"Could not open the PDF: {exc}") from exc
    counts = {}
    for old, new in pairs:
        n, _ = replace_text(ed.doc, str(old), str(new), ed.resolver,
                            case_sensitive=case_sensitive, whole_word=whole_word, fit=fit)
        counts[str(old)] = n
    data = ed.export(strip_metadata=not keep_metadata)
    ed.doc.close()
    return pdf_response(data, edited_name(ed.name),
                        {"X-Replacement-Counts": quote(json.dumps(counts, ensure_ascii=False))})


@app.post("/api/inspect")
async def inspect(file: UploadFile = File(...)):
    """List every editable text run in a PDF, useful when writing automations."""
    ed = EditorDocument(await file.read(), file.filename or "document.pdf")
    pages = [{"page": p + 1, "units": ed.units_json(p)} for p in range(ed.doc.page_count)]
    ed.doc.close()
    return JSONResponse({"pages": pages})


# --------------------------------------------------------------------------
# Frontend
# --------------------------------------------------------------------------

@app.get("/")
def index():
    return FileResponse(APP_DIR / "static" / "index.html")


app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")


if __name__ == "__main__":
    print(f"\n  Retypee is running at http://{HOST}:{PORT}\n")
    uvicorn.run(app, host=HOST, port=PORT, log_level="warning")
