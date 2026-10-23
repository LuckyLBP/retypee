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
| a close match | A metric-compatible stand-in bundled in `fonts-bundled/` for a font the app can't read from your system (Arial, Times New Roman, Courier New, Calibri, Cambria and Georgia all have one). Same letter widths as the original, so spacing still lines up, but not a pixel-identical match. |
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

`web/` is Retypee running entirely in the browser, so files are never uploaded and
Vercel only serves static files. It has the editor plus a set of single-purpose PDF
tools, each with its own Swedish and English landing page.

```bash
scripts/sync-web.sh                      # after editing pdfedit/: copy it into web/py/
python3 scripts/build_pages.py           # after editing page copy or layout: regenerate web/
python3 scripts/build_pages.py --check   # exit 1 if the generated pages are out of date
cd web && python3 -m http.server 8799    # then open http://localhost:8799
```

### Tools

Forty-one tool pages (and the editor), each with its own Swedish and English landing page.
Everything runs in the visitor's browser; nothing is uploaded.

| Group | Tools | Engine |
|---|---|---|
| Edit | Edit PDF (plus four landing pages for specific searches) | PyMuPDF in Pyodide |
| | Fill in form | pdf-lib forms API, fields laid over pdf.js pages |
| | Highlight and draw, Add image, Header and footer, Page numbers, Watermark, Sign | pdf-lib; marks are kept in displayed page points and mapped back per page, so rotated pages stay right |
| Organize | Merge, Split, Delete pages, Extract pages, Rotate, Organize | pdf-lib (page grids drawn with pdf.js) |
| | Remove blank pages | counts ink in a small pdf.js render, then pdf-lib |
| | Reverse order (and collate front/back scans), Add blank pages | pdf-lib |
| Format and print | Crop, Auto-crop | pdf-lib crop box; auto-crop finds the ink in a pdf.js render |
| | Resize pages, Pages per sheet, Booklet | pdf-lib; embedded pages are drawn as displayed (`RT.embedAll` / `RT.drawVisible`) |
| | Grayscale, Compress | PyMuPDF in Pyodide (`/api/grayscale`, `/api/compress`) |
| Convert | JPG to PDF, PNG to PDF, Text to PDF, Scan to PDF | pdf-lib; scanning cleans photos on a canvas (shadow removal, black and white) |
| | PDF to JPG, PDF to PNG | pdf.js, fflate (ZIP) |
| | PDF to text, Extract images, OCR PDF | pdf.js text; PyMuPDF (`/api/images`, `/api/extract-images`); tesseract.js (WebAssembly core and language data from jsDelivr, cached by the browser) with invisible text added by pdf-lib |
| Security and repair | Remove metadata, Edit properties, Redact | PyMuPDF (redact, metadata); pdf-lib (properties) |
| | Flatten, Remove comments | PyMuPDF (`/api/flatten`, `/api/strip-annots`; kinds come from `/api/pdf-info`) |
| | Protect, Unlock, Compare, Repair | PyMuPDF (`/api/protect`, `/api/unlock`, `/api/repair`); pdf.js text for compare |

PNG to PDF and PDF to PNG are landing pages that run the JPG tools' scripts (`SCRIPT_OF` in
`scripts/site/registry.py`); PDF to PNG starts on PNG through the page's `variant` string.

The big libraries load only when someone points at a tool or chooses a file, so a page
is about 100 KB at first. PyMuPDF is about 25 MB and comes from the jsDelivr CDN
(pinned in `web/worker.js`); pdf-lib, pdf.js, fflate and the tesseract.js scripts are served from `web/vendor/`
(MIT and Apache-2.0, see `web/vendor/LICENSES.txt`). Fonts (Inter, Caveat) for the site itself are
in `web/fonts/`; the font-matching stand-ins the editor can draw with (Arimo, Tinos, Cousine, Carlito,
Caladea, Gelasio — all SIL Open Font License) are in `fonts-bundled/`, one licence file per family.

### How the pages are made

The pages are generated, and the generated HTML is committed, so Vercel needs no build step.

- `scripts/site/registry.py`: every page, its Swedish and English URL, and its menu group.
- `scripts/site/content_*.py`: all copy (title, description, headings, steps, FAQ) in both
  languages. `{{link:page-id}}` in a string becomes a link to that page.
- `scripts/site/layout.py` and `scripts/build_pages.py`: head, structured data, header
  with the tools menu, footer, and the page bodies. The script also writes `web/sitemap.xml`
  and the language redirects in `vercel.json`.
- Each page's FAQ in the structured data is built from its visible FAQ, so they always match.

**Adding a tool:** add it to `PAGES` in `registry.py` (and to `CATEGORIES`), give it a name in
`names.py`, write its copy in a `content_tools*.py` file (including the `ui` strings its script
shows; a page only sees `TOOL_UI` in `ui.py` and its own `ui` block, so strings are not shared
between tools), write `web/tools/<id>.js` using the helpers in `web/tools/common.js`, then run
`python3 scripts/build_pages.py` (`--check` fails when the committed pages are stale). If it needs PyMuPDF, add a route to `web/py/bridge.py`
(and to `app.py` if the local app should have it too).

### Icons

Every page has an icon from [Lucide](https://lucide.dev) (ISC licence), shown in the menu, on the
hub and related-tool cards, and above each tool's title. `ICON_OF` in `scripts/site/registry.py` names
the Lucide icon for each page; `python3 scripts/fetch_icons.py` downloads those icons (at the pinned
`LUCIDE` version) into one sprite, `web/icons.svg`, which is committed and cached. Pages reference it
with `<use href="/icons.svg#i-<page id>">`, so the icons follow the text colour. A new page needs an
`ICON_OF` entry (the script stops if one is missing), then rerun the script and the page generator.

### Languages

Swedish is the main language (`/`), English lives at `/en/`. Every page has a twin in the
other language, linked with `hreflang`. `vercel.json` sends browsers whose language is
English from a Swedish page to its English twin (add `?lang=sv` to stay on Swedish);
crawlers always get Swedish. Messages in the editor are in `STRINGS` in `web/app.js` and
`MESSAGES` in `web/py/bridge.py`; messages in the tools come from each page's `ui` block.

### Notes

- `web/py/bridge.py` mirrors the routes in `app.py`; `web/worker.js` loads Pyodide and
  answers requests from `web/app.js` and `web/tools/engine.js`.
- Fonts installed on the visitor's computer can't be read by a web page, so the editor's
  *Add font* button lets them hand it a `.ttf`/`.otf` for the tab.
- Deploy: `vercel.json` serves `web/` as is (output directory `web`, no build step).
  The live domain is `retypee.se`.
- The privacy statements on the pages (no cookies, no tracking scripts) are true today.
  If analytics is added, update them.
- Security headers are in `vercel.json`, including a Content-Security-Policy: scripts only
  from the site and `cdn.jsdelivr.net` (plus `wasm-unsafe-eval` for Pyodide and Tesseract),
  no inline scripts, no `eval`. Keep it in mind when adding code: no inline handlers, and do
  not `fetch` `data:` URLs (`connect-src` does not allow them).
- Accessibility: file inputs are visually hidden but stay in the tab order (a `hidden`
  attribute would make them unreachable by keyboard), and the tool pages pass an axe-core
  audit (WCAG 2 A/AA) in their empty and loaded states, in light and dark mode.
- Errors from libraries are never shown as they come: a file that will not open gets one
  translated message (`RT.friendly`), and tools were checked against empty, corrupt and
  zero-page files.

### Going live checklist

1. Google Search Console: add the **Domain property** (DNS TXT record), submit
   `https://retypee.se/sitemap.xml`, request indexing for the home pages and the tools hub.
2. Bing Webmaster Tools: import the site from Search Console.
3. On GitHub, set the repo website to `https://retypee.se` and add topics.
4. After deploying, check on the live site: a Swedish page with an English browser
   language redirects to its `/en/` twin, a crawler without a language header gets Swedish,
   and every page is served with the trailing slash its canonical URL uses.

## Limits worth knowing

- Text doesn't reflow. If new text is longer it runs further right; use
  *Squeeze to fit* or shorten it. Paragraphs are edited line by line.
- Find and replace matches within one line and one style.
- Scanned pages have no text to edit. Run OCR first (the OCR PDF tool on the site, or `ocrmypdf` locally).
- Rotated or vertical text can't be edited yet (rotated pages are fine).
- Some PDFs (often from Chrome with variable fonts) embed fonts without
  names. Those edits use the standard fallback; use the font menu or `fonts/`
  to pick the right one.
- Password protected PDFs need their password removed first (the Unlock PDF tool does it).
- The tools handle large files well (a 300-page PDF takes a few seconds), but everything lives in the browser's memory, so very large files are limited by the device.

## Files

```
app.py            web server + API (FastAPI)
cli.py            command line automation
pdfedit/core.py   editing engine (extract, redact, rewrite, undo)
pdfedit/fonts.py  font matching (embedded, local, bundled, fallback)
static/           the local app's web interface
fonts/            put extra font files here (local app)
fonts-bundled/    metric-compatible stand-ins shipped with the app (OFL)
web/              the static site (generated pages, tools, vendored libraries)
scripts/          page generator (build_pages.py, site/) and sync-web.sh
```

## Licence

Retypee is free software under the [GNU Affero General Public License v3.0](LICENSE).
It builds on [PyMuPDF](https://pymupdf.readthedocs.io), which is also AGPL-3.0.
If you run a modified version as a public web service, the AGPL requires you to
offer your users the source code of your version.
