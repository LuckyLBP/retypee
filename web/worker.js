"use strict";

/* Retypee: runs the Python editing engine (PyMuPDF) in the browser through Pyodide.
   The page talks to it with the same routes the local server uses. Nothing
   leaves the device: documents only exist in this worker's memory. */

const PYODIDE_VERSION = "0.29.0";
const PYODIDE_BASE = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;
const PY_FILES = ["pdfedit/__init__.py", "pdfedit/core.py", "pdfedit/fonts.py", "bridge.py"];

// Metric-compatible stand-ins for fonts most real PDFs use (Arial, Times New Roman, Courier
// New, Calibri, Cambria, Georgia) but the browser has no way to read from the host OS, unlike
// the local app. Kept in sync with fonts-bundled/ by scripts/sync-web.sh.
const BUNDLED_FONTS = Object.entries({
  arimo: "Arimo", tinos: "Tinos", cousine: "Cousine", carlito: "Carlito", caladea: "Caladea", gelasio: "Gelasio",
}).flatMap(([dir, family]) => ["Regular", "Bold", "Italic", "BoldItalic"].map((style) => `${dir}/${family}-${style}.ttf`));

importScripts(`${PYODIDE_BASE}pyodide.js`);

let dispatch = null;

async function boot() {
  post({ type: "progress", key: "p_download" });
  const pyodide = await loadPyodide({ indexURL: PYODIDE_BASE });
  post({ type: "progress", key: "p_tools" });
  await pyodide.loadPackage(["pymupdf", "fonttools"]);

  const home = pyodide.FS.cwd();
  pyodide.FS.mkdirTree(`${home}/pdfedit`);
  pyodide.FS.mkdirTree(`${home}/fonts`);
  pyodide.FS.mkdirTree(`${home}/fonts-bundled`);
  await Promise.all([
    ...PY_FILES.map(async (file) => {
      const res = await fetch(new URL(`py/${file}`, self.location.href));
      if (!res.ok) throw new Error(`Could not load ${file}.`);
      pyodide.FS.writeFile(`${home}/${file}`, await res.text());
    }),
    ...BUNDLED_FONTS.map(async (rel) => {
      const res = await fetch(new URL(`py/fonts-bundled/${rel}`, self.location.href));
      if (!res.ok) throw new Error(`Could not load font ${rel}.`);
      const bytes = new Uint8Array(await res.arrayBuffer());
      pyodide.FS.writeFile(`${home}/fonts-bundled/${rel.split("/")[1]}`, bytes);
    }),
  ]);
  dispatch = pyodide.pyimport("bridge").dispatch;
  post({ type: "ready" });
}

function post(message, transfer = []) {
  self.postMessage(message, transfer);
}

async function handle({ id, method, url, json, file, lang }) {
  await ready;
  // undefined (not null) reaches Python as None.
  const upload = file ? new Uint8Array(file.bytes) : undefined;
  const proxy = dispatch(method, url, json, upload, file?.name, lang);
  let status, kind, payload, filename;
  try {
    [status, kind, payload, filename] = proxy.toJs();
  } finally {
    proxy.destroy();
  }
  if (kind === "json") return post({ id, status, data: JSON.parse(payload) });
  if (kind === "error") return post({ id, status, error: payload });
  // Binary result (page image or the edited PDF). Copy out of the Wasm heap.
  const bytes = new Uint8Array(payload).buffer;
  post({ id, status, bytes, mime: kind, filename }, [bytes]);
}

const ready = boot().catch((err) => {
  console.error(err);
  post({ type: "fatal", text: err.message || String(err) });
  throw err;
});
ready.catch(() => {});

self.onmessage = (event) => {
  handle(event.data).catch((err) => {
    post({ id: event.data.id, status: 500, error: err.message || String(err) });
  });
};
