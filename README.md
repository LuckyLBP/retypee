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

| Tool (sv / en) | Engine |
|---|---|
| Redigera PDF / Edit PDF (and four landing pages for specific searches) | PyMuPDF in Pyodide |
| Slå ihop, Dela, Radera sidor, Extrahera sidor, Rotera, Organisera / Merge, Split, Delete pages, Extract pages, Rotate, Organize | pdf-lib (page grids drawn with pdf.js) |
| Sidnummer, Vattenstämpel, Beskär, Signera / Page numbers, Watermark, Crop, Sign | pdf-lib (previews drawn with pdf.js) |
| JPG till PDF / JPG to PDF | pdf-lib |
| PDF till JPG / PDF to JPG | pdf.js, fflate (ZIP) |
| PDF till text, Jämför PDF / PDF to text, Compare PDF | pdf.js (text extraction) |
| Komprimera, Skydda, Lås upp / Compress, Protect, Unlock | PyMuPDF in Pyodide (`/api/compress`, `/api/protect`, `/api/unlock`) |
| Ta bort metadata, Censurera / Remove metadata, Redact | PyMuPDF in Pyodide |

The big libraries load only when someone points at a tool or chooses a file, so a page
is about 100 KB at first. PyMuPDF is about 25 MB and comes from the jsDelivr CDN
(pinned in `web/worker.js`); pdf-lib, pdf.js and fflate are served from `web/vendor/`
(MIT and Apache-2.0, see `web/vendor/LICENSES.txt`). Fonts (Inter) are in `web/fonts/`.

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
`names.py`, write its copy in `content_tools.py` (including the `ui` strings its script shows),
write `web/tools/<id>.js` using the helpers in `web/tools/common.js`, then run
`python3 scripts/build_pages.py`. If it needs PyMuPDF, add a route to `web/py/bridge.py`
(and to `app.py` if the local app should have it too).

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
static/           the local app's web interface
fonts/            put extra font files here (local app)
web/              the static site (generated pages, tools, vendored libraries)
scripts/          page generator (build_pages.py, site/) and sync-web.sh
```

## Licence

Retypee is free software under the [GNU Affero General Public License v3.0](LICENSE).
It builds on [PyMuPDF](https://pymupdf.readthedocs.io), which is also AGPL-3.0.
If you run a modified version as a public web service, the AGPL requires you to
offer your users the source code of your version.
