# Retypee: a local PDF text editor

Edit the text in PDFs that "aren't editable". Click a line, type, done. Or run
find and replace across a whole file, from the browser, the command line or
an HTTP call. Everything runs on your own computer with
[PyMuPDF](https://pymupdf.readthedocs.io) (the MuPDF engine).

## Start

Needs Python 3.10 or newer.

```bash
./start.sh          # macOS / Linux  (first run installs everything into .venv)
start.bat           # Windows
```

Then open http://127.0.0.1:8765 (the start script opens it for you).

Manual setup, if you prefer:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Using the editor

- **Edit text**: click any highlighted line, change it, press Enter. You can
  also change font, size, colour, bold and italic, squeeze long text into the
  original width, or delete the line.
- **Add text**: switch to *Add text* (or press `T`) and click where the text should go.
- **Find and replace** (`Ctrl/Cmd+F`): live match count, then *Replace all*.
- **Undo / redo**: `Ctrl/Cmd+Z`, `Ctrl/Cmd+Shift+Z`.
- **Download PDF** saves `<name>-edited.pdf` with its metadata removed (see below).

After each edit a message tells you which font was used:

| Message | Meaning |
|---|---|
| taken from the PDF | The embedded font had every letter you typed. Perfect match. |
| installed on this computer | Same font found in your system fonts or in `fonts/`. Perfect match. |
| standard fallback | Original font not found, so Helvetica, Times or Courier was used in the closest style. Drop the real `.ttf`/`.otf` into `fonts/` to fix it. |

## Metadata

Every downloaded or exported PDF has its metadata removed: title, author,
subject, keywords, the app that created it, dates, XMP metadata on the
document, pages, images and fonts, page thumbnails, comment author names, the
"Written by MuPDF" header, and the file ID (replaced with a new random one).
Text, images, links, form fields and attachments are not touched.

To keep the metadata: `--keep-metadata` on the command line,
`keep_metadata=true` as a form field on `/api/replace`, or
`?keep_metadata=true` on the download URL.

## Automation

### Command line

```bash
# One file
python cli.py replace offer.pdf -r "2026-104=2026-219" -r "Borås=Göteborg"

# Every PDF in a folder, replacements from a JSON file {"old": "new", ...}
python cli.py batch ./in ./out --map replacements.json

# See which text runs a PDF contains (useful when writing a map)
python cli.py inspect offer.pdf
```

Options: `--case-sensitive`, `--whole-word`, `--fit` (squeeze longer text).

### HTTP API (while the app is running)

```bash
curl -F file=@offer.pdf \
     -F 'replacements={"2026-104":"2026-219","Borås":"Göteborg"}' \
     http://127.0.0.1:8765/api/replace -o offer-edited.pdf
```

The response header `X-Replacement-Counts` says how many times each text was
replaced. Optional form fields: `case_sensitive`, `whole_word`, `fit`.
`POST /api/inspect` with a file returns every text run as JSON.
Full API docs: http://127.0.0.1:8765/docs

### From your own code

```python
from pdfedit.core import EditorDocument, replace_text

ed = EditorDocument(open("offer.pdf", "rb").read(), "offer.pdf")
count, pages = replace_text(ed.doc, "2026-104", "2026-219", ed.resolver)
open("offer-edited.pdf", "wb").write(ed.export())
```

## How it works

PDFs don't store paragraphs, only glyphs at fixed positions. So an edit:

1. Finds the run of text (same line, same style) you clicked or matched.
2. Removes only those glyphs with a text-only redaction. Images, lines and
   backgrounds underneath stay untouched.
3. Writes the new text on the same baseline with the same size and colour.
   Unchanged text at the start of a run is left exactly as it was.
4. Keeps the right edge in place for right-aligned columns (prices in tables).

## Web version (static site, no server)

`web/` is the same editor running entirely in the browser: the Python engine
(PyMuPDF) runs under [Pyodide](https://pyodide.org) in a Web Worker, so a PDF
is never uploaded and Vercel only serves static files. The first visit
downloads about 25 MB (cached afterwards).

```bash
scripts/sync-web.sh                  # after editing pdfedit/: copy it into web/py/
cd web && python3 -m http.server 8799   # then open http://localhost:8799
```

- `web/py/bridge.py` mirrors the routes in `app.py`; `web/worker.js` loads
  Pyodide and answers requests from `web/app.js`. If you add a route to
  `app.py`, add it to `bridge.py` too.
- Fonts installed on the visitor's computer can't be read by a web page, so
  the *Add font* button lets them hand the editor a `.ttf`/`.otf` for the tab.
- Languages: Swedish is the main language (`/`), English lives at `/en/`.
  `vercel.json` sends browsers whose language is English from `/` to `/en/`
  (add `?lang=sv` to stay on Swedish); crawlers always get Swedish. The two
  pages are plain HTML (`web/index.html`, `web/en/index.html`), so a text change
  has to be made in both. Messages in the app are in `STRINGS` in `web/app.js`
  and `MESSAGES` in `web/py/bridge.py`.
- Deploy: `vercel.json` serves `web/` as is. Before going live, replace
  `https://retype.example` (both index.html files, sitemap.xml, robots.txt) with the real
  domain.

## Limits worth knowing

- Text doesn't reflow. If new text is longer it runs further right; use
  *Squeeze to fit* or shorten it. Paragraphs are edited line by line.
- Find and replace matches within one line and one style.
- Scanned pages have no text to edit. Run OCR first (for example `ocrmypdf`).
- Rotated or vertical text can't be edited yet (rotated pages are fine).
- Some PDFs (often from Chrome with variable fonts) embed fonts without
  names. Those edits use the standard fallback; use the font menu or `fonts/`
  to pick the right one.
- Password protected PDFs need their password removed first.

## Files

```
app.py            web server + API (FastAPI)
cli.py            command line automation
pdfedit/core.py   editing engine (extract, redact, rewrite, undo)
pdfedit/fonts.py  font matching (embedded, local, fallback)
static/           the web interface
fonts/            put extra font files here
```

## Licence

Retypee is free software under the [GNU Affero General Public License v3.0](LICENSE).
It builds on [PyMuPDF](https://pymupdf.readthedocs.io), which is also AGPL-3.0.
If you run a modified version as a public web service, the AGPL requires you to
offer your users the source code of your version.
