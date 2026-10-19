"use strict";

/* Retypee: runs the Python editing engine (PyMuPDF) in the browser through Pyodide.
   The page talks to it with the same routes the local server uses. Nothing
   leaves the device: documents only exist in this worker's memory. */

const PYODIDE_VERSION = "0.29.0";
const PYODIDE_BASE = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;
const PY_FILES = ["pdfedit/__init__.py", "pdfedit/core.py", "pdfedit/fonts.py", "bridge.py"];

importScripts(`${PYODIDE_BASE}pyodide.js`);

let dispatch = null;

async function boot() {
  post({ type: "progress", text: "Downloading the editor engine…" });
  const pyodide = await loadPyodide({ indexURL: PYODIDE_BASE });
  post({ type: "progress", text: "Loading PDF tools…" });
  await pyodide.loadPackage(["pymupdf", "fonttools"]);

  const home = pyodide.FS.cwd();
  pyodide.FS.mkdirTree(`${home}/pdfedit`);
  pyodide.FS.mkdirTree(`${home}/fonts`);
  await Promise.all(
    PY_FILES.map(async (file) => {
      const res = await fetch(new URL(`py/${file}`, self.location.href));
      if (!res.ok) throw new Error(`Could not load ${file}.`);
      pyodide.FS.writeFile(`${home}/${file}`, await res.text());
    })
  );
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
