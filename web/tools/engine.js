"use strict";

/* Client for the PDF engine (PyMuPDF in a Web Worker, see /worker.js).
   Used by the tools that need more than pdf-lib can do. It starts on first use. */
(function () {
  const lang = document.documentElement.lang === "en" ? "en" : "sv";
  const state = { worker: null, starting: null, pending: new Map(), nextId: 1, onProgress: null };

  function start() {
    if (state.starting) return state.starting;
    state.starting = new Promise((resolve, reject) => {
      const worker = new Worker("/worker.js");
      state.worker = worker;
      worker.onmessage = ({ data }) => {
        if (data.type === "progress") return state.onProgress && state.onProgress(data.key);
        if (data.type === "ready") return resolve();
        if (data.type === "fatal") {
          const err = new Error(data.text);
          for (const p of state.pending.values()) p.reject(err);
          state.pending.clear();
          return reject(err);
        }
        const entry = state.pending.get(data.id);
        if (!entry) return;
        state.pending.delete(data.id);
        if (data.error !== undefined) {
          const err = new Error(data.error);
          err.status = data.status;
          entry.reject(err);
        } else {
          entry.resolve(data);
        }
      };
      worker.onerror = (e) => reject(new Error(e.message || "The PDF engine could not start."));
    });
    return state.starting;
  }

  async function call(path, { method = "GET", json, file } = {}) {
    await start();
    return new Promise((resolve, reject) => {
      const id = state.nextId++;
      state.pending.set(id, { resolve, reject });
      const message = { id, method, url: path, lang };
      if (json !== undefined) message.json = JSON.stringify(json);
      if (file) {
        message.file = file;
        state.worker.postMessage(message, [file.bytes]);
      } else {
        state.worker.postMessage(message);
      }
    });
  }

  window.RTEngine = {
    start, call,
    set onProgress(fn) { state.onProgress = fn; },
    async json(path, opts) { return (await call(path, opts)).data; },
    async bytes(path) { const r = await call(path); return { bytes: new Uint8Array(r.bytes), mime: r.mime, filename: r.filename }; },
  };
})();
