"use strict";

/* Retype frontend. Talks to the local FastAPI server in app.py. */

const $ = (sel) => document.querySelector(sel);
const ZOOM_STEPS = [0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3];
const FONT_SOURCE = {
  embedded: "taken from the PDF",
  local: "installed on this computer",
  bundled: "a close match",
  standard: "standard fallback",
};

const state = {
  id: null,
  meta: null,
  zoom: 1,
  mode: "edit",
  pages: [],
  fonts: [{ value: "auto", label: "Match original" }],
  editor: null,
  flash: null,
  busy: 0,
  addDefaults: { size: 12, color: "#000000", font: "sans", bold: false, italic: false },
};

const els = {
  desk: $("#desk"),
  empty: $("#empty"),
  drop: $("#drop"),
  pages: $("#pages"),
  tools: $("#tools"),
  fileName: $("#fileName"),
  fileInput: $("#fileInput"),
  openBtn: $("#openBtn"),
  openInput: $("#openInput"),
  downloadBtn: $("#downloadBtn"),
  undoBtn: $("#undoBtn"),
  redoBtn: $("#redoBtn"),
  zoomIn: $("#zoomIn"),
  zoomOut: $("#zoomOut"),
  zoomLabel: $("#zoomLabel"),
  findBtn: $("#findBtn"),
  drawer: $("#drawer"),
  drawerClose: $("#drawerClose"),
  replaceForm: $("#replaceForm"),
  findInput: $("#findInput"),
  replaceInput: $("#replaceInput"),
  caseCheck: $("#caseCheck"),
  wordCheck: $("#wordCheck"),
  fitCheck: $("#fitCheck"),
  matchCount: $("#matchCount"),
  replaceAllBtn: $("#replaceAllBtn"),
  toast: $("#toast"),
  busy: $("#busy"),
};

/* ---------------------------------------------------------------- helpers */

async function api(path, { method = "GET", json, form } = {}) {
  const opts = { method, headers: {} };
  if (json !== undefined) {
    opts.headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(json);
  } else if (form) {
    opts.body = form;
  }
  setBusy(+1);
  try {
    const res = await fetch(path, opts);
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      const err = new Error(data.detail || `Request failed (${res.status}).`);
      err.status = res.status;
      throw err;
    }
    return data;
  } finally {
    setBusy(-1);
  }
}

function setBusy(delta) {
  state.busy = Math.max(0, state.busy + delta);
  els.busy.hidden = state.busy === 0;
}

let toastTimer;
function toast(message, { error = false, detail = "" } = {}) {
  els.toast.textContent = message;
  if (detail) {
    const small = document.createElement("small");
    small.textContent = detail;
    els.toast.appendChild(small);
  }
  els.toast.classList.toggle("error", error);
  els.toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (els.toast.hidden = true), error ? 6500 : 4000);
}

function fail(err) {
  console.error(err);
  toast(err.message || "Something went wrong.", { error: true });
  if (err.status === 409) refreshPages(state.pages.map((_, i) => i));
}

function cssFamily(fontName) {
  const name = (fontName || "").replace(/^[A-Z]{6}\+/, "");
  const lower = name.toLowerCase();
  let generic = "Helvetica, Arial, sans-serif";
  if (/mono|courier|consol|menlo|code/.test(lower)) generic = '"Courier New", monospace';
  else if (!lower.includes("sans") && /times|serif|georgia|garamond|roman|cambria|minion|baskerville|palatino/.test(lower))
    generic = 'Georgia, "Times New Roman", serif';
  const family = name.split(/[-,]/)[0].replace(/(MT|PS)$/g, "").replace(/([a-z])([A-Z])/g, "$1 $2");
  return `"${family}", ${generic}`;
}

const measureCtx = document.createElement("canvas").getContext("2d");
function textWidth(text, input) {
  const cs = getComputedStyle(input);
  measureCtx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
  return measureCtx.measureText(text || " ").width;
}

function renderZoom() {
  const dpr = window.devicePixelRatio || 1;
  return Math.min(4, Math.max(1, Math.round(state.zoom * dpr * 4) / 4));
}

/* ---------------------------------------------------------------- open */

async function openFile(file) {
  if (!file) return;
  if (!/\.pdf$/i.test(file.name) && file.type !== "application/pdf") {
    toast(`"${file.name}" is not a PDF. Choose a file that ends in .pdf.`, { error: true });
    return;
  }
  if (state.meta?.canUndo && !confirm("Open a new file? Changes you have not downloaded will be lost.")) return;
  const form = new FormData();
  form.append("file", file);
  try {
    const data = await api("/api/docs", { method: "POST", form });
    if (state.id) api(`/api/docs/${state.id}`, { method: "DELETE" }).catch(() => {});
    state.id = data.id;
    state.meta = data;
    closeEditor();
    showEditor();
    loadFonts();
  } catch (err) {
    fail(err);
  }
}

async function loadFonts() {
  try {
    const data = await api("/api/fonts");
    state.fonts = data.fonts;
  } catch {
    /* the defaults still work */
  }
}

function showEditor() {
  els.empty.hidden = true;
  els.pages.hidden = false;
  els.tools.hidden = false;
  els.openBtn.hidden = false;
  els.downloadBtn.hidden = false;
  els.fileName.textContent = state.meta.name;
  document.title = `${state.meta.name} · Retype`;
  state.zoom = fitZoom();
  els.zoomLabel.textContent = `${Math.round(state.zoom * 100)}%`;
  buildPages();
  updateMeta(state.meta);
  els.desk.scrollTo(0, 0);
}

function fitZoom() {
  const widest = Math.max(...state.meta.pages.map((p) => p.w));
  const room = els.desk.clientWidth - 120;
  const fit = room / widest;
  const step = [...ZOOM_STEPS].reverse().find((z) => z <= Math.min(fit, 1.5));
  return step || ZOOM_STEPS[0];
}

/* ---------------------------------------------------------------- pages */

const observer = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      const i = Number(entry.target.dataset.index);
      const page = state.pages[i];
      if (!page) continue;
      page.visible = entry.isIntersecting;
      if (page.visible) ensurePage(i);
    }
  },
  { root: els.desk, rootMargin: "800px 0px" }
);

function buildPages() {
  observer.disconnect();
  els.pages.innerHTML = "";
  state.pages = state.meta.pages.map((size, i) => {
    const el = document.createElement("div");
    el.className = "page";
    el.dataset.index = i;
    const num = document.createElement("span");
    num.className = "page-num";
    num.textContent = i + 1;
    const img = document.createElement("img");
    img.alt = `Page ${i + 1}`;
    img.draggable = false;
    const overlay = document.createElement("div");
    overlay.className = "overlay";
    overlay.addEventListener("click", (e) => onPageClick(e, i));
    el.append(num, img, overlay);
    els.pages.appendChild(el);
    const page = { el, img, overlay, size, units: null, rev: 0, imageKey: "", visible: false, loadingUnits: false };
    layoutPage(page);
    observer.observe(el);
    return page;
  });
}

function layoutPage(page) {
  page.el.style.width = `${page.size.w * state.zoom}px`;
  page.el.style.height = `${page.size.h * state.zoom}px`;
}

function ensurePage(i) {
  const page = state.pages[i];
  const key = `${renderZoom()}-${page.rev}`;
  if (page.imageKey !== key) {
    page.imageKey = key;
    const url = `/api/docs/${state.id}/pages/${i}/image?zoom=${renderZoom()}&v=${page.rev}-${state.meta.version}`;
    const pre = new Image();
    pre.onload = () => {
      if (page.imageKey === key) page.img.src = url;
    };
    pre.src = url;
  }
  if (!page.units && !page.loadingUnits) loadUnits(i);
}

async function loadUnits(i) {
  const page = state.pages[i];
  page.loadingUnits = true;
  try {
    const data = await api(`/api/docs/${state.id}/pages/${i}/units`);
    page.units = data.units;
    renderUnits(i);
  } catch (err) {
    fail(err);
  } finally {
    page.loadingUnits = false;
  }
}

function renderUnits(i) {
  const page = state.pages[i];
  const z = state.zoom;
  page.overlay.innerHTML = "";
  page.el.querySelector(".page-note")?.remove();
  if (!page.units) return;
  if (page.units.length === 0) {
    const note = document.createElement("div");
    note.className = "page-note";
    note.textContent = "No editable text on this page. It is probably a scanned image.";
    page.el.appendChild(note);
    return;
  }
  const frag = document.createDocumentFragment();
  for (const u of page.units) {
    const [x0, y0, x1, y1] = u.bbox;
    const b = document.createElement("button");
    b.type = "button";
    b.className = "unit" + (u.editable ? "" : " locked");
    b.style.left = `${(x0 - 1) * z}px`;
    b.style.top = `${y0 * z}px`;
    b.style.width = `${(x1 - x0 + 2) * z}px`;
    b.style.height = `${(y1 - y0) * z}px`;
    b.setAttribute("aria-label", u.editable ? `Edit text: ${u.text}` : `Rotated text, cannot be edited: ${u.text}`);
    if (!u.editable) b.title = "Rotated or vertical text cannot be edited yet.";
    b.addEventListener("click", (e) => {
      e.stopPropagation();
      if (state.mode !== "edit") return;
      if (!u.editable) {
        toast("Rotated or vertical text cannot be edited yet.", { error: true });
        return;
      }
      openEditor(i, u);
    });
    if (state.flash && state.flash.page === i) {
      const { x, y } = state.flash;
      if (x >= x0 - 2 && x <= x1 + 2 && y >= y0 - 2 && y <= y1 + 2) b.classList.add("flash");
    }
    frag.appendChild(b);
  }
  page.overlay.appendChild(frag);
}

function refreshPages(indices) {
  for (const i of indices) {
    const page = state.pages[i];
    if (!page) continue;
    page.rev += 1;
    page.units = null;
    if (page.visible) ensurePage(i);
  }
}

function updateMeta(meta) {
  state.meta = { ...state.meta, ...meta };
  els.undoBtn.disabled = !state.meta.canUndo;
  els.redoBtn.disabled = !state.meta.canRedo;
}

function applyChange(data, flash) {
  state.flash = flash || null;
  updateMeta(data);
  refreshPages(data.changedPages || []);
  if (!els.drawer.hidden) countMatches();
  setTimeout(() => (state.flash = null), 1500);
}

/* ---------------------------------------------------------------- editor */

function closeEditor() {
  state.editor?.el.remove();
  state.editor = null;
}

function fontOptions(selected) {
  return state.fonts
    .map((f) => `<option value="${escapeAttr(f.value)}"${f.value === selected ? " selected" : ""}>${escapeHtml(f.label)}</option>`)
    .join("");
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}
const escapeAttr = escapeHtml;

/**
 * Build the in-place editor. `spec` describes what is being edited:
 *   { kind: "edit", page, unit }  or  { kind: "add", page, x, y } (x, y in PDF points)
 */
function buildEditor(spec) {
  closeEditor();
  const z = state.zoom;
  const page = state.pages[spec.page];
  const isEdit = spec.kind === "edit";
  const u = spec.unit;

  const size = isEdit ? u.size : state.addDefaults.size;
  const color = isEdit ? u.color : state.addDefaults.color;
  const left = isEdit ? u.bbox[0] : spec.x;
  const top = isEdit ? u.bbox[1] : spec.y;
  const height = isEdit ? u.bbox[3] - u.bbox[1] : size * 1.25;

  const el = document.createElement("div");
  el.className = "editor";
  el.style.left = `${left * z - 2}px`;
  el.style.top = `${top * z}px`;
  el.addEventListener("click", (e) => e.stopPropagation());

  const input = document.createElement("input");
  input.className = "editor-input";
  input.type = "text";
  input.spellcheck = false;
  input.value = isEdit ? u.text : "";
  input.placeholder = isEdit ? "" : "Type text";
  input.setAttribute("aria-label", isEdit ? "New text" : "Text to add");
  input.style.height = `${height * z}px`;
  input.style.fontSize = `${size * z}px`;
  input.style.fontFamily = cssFamily(isEdit ? u.font : "Helvetica");
  input.style.color = color;

  const panel = document.createElement("div");
  panel.className = "editor-panel";
  const fontValue = isEdit ? "auto" : state.addDefaults.font;
  const meta = isEdit
    ? `Original: <b>${escapeHtml(u.font.startsWith("Type3") ? "unnamed font" : u.font.replace(/^[A-Z]{6}\+/, ""))}</b>, ${Math.round(u.size * 10) / 10} pt`
    : "Enter adds the text, Esc cancels";
  panel.innerHTML = `
    <div class="editor-row">
      <select data-k="font" aria-label="Font">${fontOptions(fontValue)}</select>
      <input data-k="size" type="number" min="2" max="400" step="0.5" value="${Math.round(size * 10) / 10}" aria-label="Font size in points" title="Size (pt)">
      <input data-k="color" type="color" value="${color}" aria-label="Text colour" title="Colour">
      <button type="button" class="toggle" data-k="bold" aria-pressed="${isEdit ? u.bold : state.addDefaults.bold}" title="Bold" aria-label="Bold"><b>B</b></button>
      <button type="button" class="toggle" data-k="italic" aria-pressed="${isEdit ? u.italic : state.addDefaults.italic}" title="Italic" aria-label="Italic"><i>I</i></button>
      ${isEdit ? `<label class="inline-check"><input data-k="fit" type="checkbox"> Squeeze to fit</label>` : ""}
    </div>
    <div class="editor-row">
      <span class="editor-meta">${meta}</span>
      ${isEdit ? `<button type="button" class="ghost danger" data-a="delete">Delete</button>` : ""}
      <button type="button" class="ghost" data-a="cancel">Cancel</button>
      <button type="button" class="primary" data-a="apply">${isEdit ? "Apply" : "Add text"}</button>
    </div>
  `;
  el.append(input, panel);
  page.el.appendChild(el);

  const minWidth = isEdit ? (u.bbox[2] - u.bbox[0]) * z + 6 : 160;
  const resize = () => {
    input.style.width = `${Math.max(minWidth, textWidth(input.value, input) + 10)}px`;
  };
  resize();
  input.addEventListener("input", resize);

  // Live preview of size and colour while the panel is open.
  const field = (k) => panel.querySelector(`[data-k="${k}"]`);
  field("size").addEventListener("input", () => {
    const v = parseFloat(field("size").value);
    if (v > 0) {
      input.style.fontSize = `${v * z}px`;
      input.style.height = `${Math.max(height, v * 1.2) * z}px`;
      resize();
    }
  });
  field("color").addEventListener("input", () => (input.style.color = field("color").value));
  const pressed = (k) => field(k).getAttribute("aria-pressed") === "true";
  const applyStyle = () => {
    input.style.fontWeight = pressed("bold") ? "700" : "400";
    input.style.fontStyle = pressed("italic") ? "italic" : "normal";
    resize();
  };
  for (const k of ["bold", "italic"]) {
    field(k).addEventListener("click", () => {
      field(k).setAttribute("aria-pressed", String(!pressed(k)));
      applyStyle();
      input.focus();
    });
  }
  applyStyle();

  // Keep the panel on the page: below the text, or above it near the bottom.
  const panelTop = input.offsetHeight + 8;
  panel.style.top = `${panelTop}px`;
  requestAnimationFrame(() => {
    const pageRect = page.el.getBoundingClientRect();
    const pr = panel.getBoundingClientRect();
    if (pr.right > pageRect.right - 8) {
      panel.style.left = `${Math.min(-2, pageRect.right - 8 - pr.right)}px`;
    }
    if (pr.bottom > pageRect.bottom && top * z > pr.height + 16) {
      panel.style.top = `${-pr.height - 8}px`;
    }
  });

  const editor = { el, input, panel, spec, field, pressed };
  state.editor = editor;

  panel.addEventListener("click", (e) => {
    const action = e.target.closest("[data-a]")?.dataset.a;
    if (action === "cancel") closeEditor();
    if (action === "apply") commitEditor();
    if (action === "delete") commitEditor({ deleteText: true });
  });
  el.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      e.preventDefault();
      closeEditor();
    } else if (e.key === "Enter" && e.target.tagName !== "BUTTON") {
      e.preventDefault();
      commitEditor();
    }
  });

  input.focus();
  if (isEdit) input.select();
  return editor;
}

function openEditor(pageIndex, unit) {
  buildEditor({ kind: "edit", page: pageIndex, unit });
}

function openAddEditor(pageIndex, x, y) {
  buildEditor({ kind: "add", page: pageIndex, x, y });
}

async function commitEditor({ deleteText = false } = {}) {
  const ed = state.editor;
  if (!ed) return;
  const { spec, input, field, pressed } = ed;
  const bold = pressed("bold");
  const italic = pressed("italic");
  const text = deleteText ? "" : input.value;
  const font = field("font").value;
  const size = parseFloat(field("size").value);
  const color = field("color").value.toLowerCase();

  try {
    if (spec.kind === "edit") {
      const u = spec.unit;
      const body = { version: state.meta.version, page: spec.page, unit: u.id, text };
      if (font && font !== "auto") body.font = font;
      if (size > 0 && Math.abs(size - u.size) > 0.05) body.size = size;
      if (color !== u.color.toLowerCase()) body.color = color;
      if (field("fit")?.checked) body.fit = true;
      if (bold !== u.bold) body.bold = bold;
      if (italic !== u.italic) body.italic = italic;
      const styleChanged = body.font || body.size || body.color || "bold" in body || "italic" in body;
      if (text === u.text && !styleChanged) {
        closeEditor();
        return;
      }
      const data = await api(`/api/docs/${state.id}/edit`, { method: "POST", json: body });
      closeEditor();
      applyChange(data, { page: spec.page, x: u.bbox[0] + 1, y: (u.bbox[1] + u.bbox[3]) / 2 });
      announceFont(deleteText ? null : data.font, deleteText);
    } else {
      if (!text.trim()) {
        input.focus();
        return;
      }
      state.addDefaults = { size: size || 12, color, font: font === "auto" ? "sans" : font, bold, italic };
      const baseline = spec.y + (size || 12) * 0.82;
      const body = { version: state.meta.version, page: spec.page, x: spec.x, y: baseline, text, size: size || 12, color, font, bold, italic };
      const data = await api(`/api/docs/${state.id}/add-text`, { method: "POST", json: body });
      closeEditor();
      applyChange(data, { page: spec.page, x: spec.x + 1, y: spec.y + (size || 12) / 2 });
      toast("Text added.", { detail: `Font: ${data.font.label}` });
    }
  } catch (err) {
    fail(err);
  }
}

function announceFont(font, deleted) {
  if (deleted) return toast("Text deleted.");
  if (!font || font.source === "unchanged") return;
  const where = FONT_SOURCE[font.source] || font.source;
  const detail =
    font.source === "standard" ? "The original font was not found. Put its .ttf or .otf file in the fonts folder for an exact match."
    : font.source === "bundled" ? "Not the original font, but one with matching letter widths, so spacing should still line up."
    : "";
  toast(`Saved with ${font.label} (${where}).`, { detail });
}

function onPageClick(e, i) {
  if (state.mode === "add") {
    const rect = state.pages[i].el.getBoundingClientRect();
    const x = (e.clientX - rect.left) / state.zoom;
    const y = (e.clientY - rect.top) / state.zoom - state.addDefaults.size * 0.6;
    openAddEditor(i, x, Math.max(0, y));
  } else {
    closeEditor();
  }
}

/* ---------------------------------------------------------------- modes, zoom, history */

function setMode(mode) {
  state.mode = mode;
  closeEditor();
  document.body.classList.toggle("mode-add", mode === "add");
  for (const b of document.querySelectorAll(".seg")) b.setAttribute("aria-checked", String(b.dataset.mode === mode));
}

function setZoom(z) {
  if (!state.meta) return;
  closeEditor();
  const desk = els.desk;
  const ratioY = desk.scrollTop / Math.max(1, desk.scrollHeight);
  state.zoom = z;
  els.zoomLabel.textContent = `${Math.round(z * 100)}%`;
  for (let i = 0; i < state.pages.length; i++) {
    layoutPage(state.pages[i]);
    renderUnits(i);
    if (state.pages[i].visible) ensurePage(i);
  }
  desk.scrollTop = ratioY * desk.scrollHeight;
}

function stepZoom(dir) {
  const i = ZOOM_STEPS.findIndex((z) => z >= state.zoom - 1e-6);
  const next = ZOOM_STEPS[Math.max(0, Math.min(ZOOM_STEPS.length - 1, (i < 0 ? ZOOM_STEPS.length - 1 : i) + dir))];
  setZoom(next);
}

async function history(kind) {
  if (!state.id) return;
  closeEditor();
  try {
    const data = await api(`/api/docs/${state.id}/${kind}`, { method: "POST" });
    applyChange(data);
    toast(kind === "undo" ? "Undone." : "Redone.");
  } catch (err) {
    if (err.status !== 400) fail(err);
  }
}

/* ---------------------------------------------------------------- find and replace */

function openDrawer() {
  if (!state.id) return;
  closeEditor();
  els.drawer.hidden = false;
  document.body.classList.add("with-drawer");
  els.findBtn.setAttribute("aria-pressed", "true");
  els.findInput.focus();
  els.findInput.select();
  countMatches();
}

function closeDrawer() {
  els.drawer.hidden = true;
  document.body.classList.remove("with-drawer");
  els.findBtn.setAttribute("aria-pressed", "false");
}

let countTimer;
let countSeq = 0;
function countMatches() {
  clearTimeout(countTimer);
  countTimer = setTimeout(async () => {
    const find = els.findInput.value;
    const seq = ++countSeq;
    if (!find) {
      els.matchCount.textContent = "Type something to find.";
      els.replaceAllBtn.disabled = true;
      els.replaceAllBtn.textContent = "Replace all";
      return;
    }
    try {
      const data = await api(`/api/docs/${state.id}/find`, {
        method: "POST",
        json: { find, caseSensitive: els.caseCheck.checked, wholeWord: els.wordCheck.checked },
      });
      if (seq !== countSeq) return;
      if (data.count === 0) {
        els.matchCount.textContent = "No matches.";
      } else {
        const pages = data.pages.map((p) => p + 1);
        const where = pages.length === 1 ? `page ${pages[0]}` : `pages ${pages.slice(0, 8).join(", ")}${pages.length > 8 ? "…" : ""}`;
        els.matchCount.innerHTML = `<b>${data.count}</b> ${data.count === 1 ? "match" : "matches"} on ${where}.`;
      }
      els.replaceAllBtn.disabled = data.count === 0;
      els.replaceAllBtn.textContent = data.count ? `Replace all ${data.count}` : "Replace all";
    } catch (err) {
      fail(err);
    }
  }, 220);
}

async function replaceAll(e) {
  e.preventDefault();
  const find = els.findInput.value;
  if (!find) return;
  try {
    const data = await api(`/api/docs/${state.id}/replace`, {
      method: "POST",
      json: {
        version: state.meta.version,
        find,
        replace: els.replaceInput.value,
        caseSensitive: els.caseCheck.checked,
        wholeWord: els.wordCheck.checked,
        fit: els.fitCheck.checked,
      },
    });
    applyChange(data);
    toast(data.count ? `Replaced ${data.count} ${data.count === 1 ? "time" : "times"}.` : "No matches to replace.");
  } catch (err) {
    fail(err);
  }
}

/* ---------------------------------------------------------------- wiring */

els.fileInput.addEventListener("change", () => {
  openFile(els.fileInput.files[0]);
  els.fileInput.value = "";
});
els.openInput.addEventListener("change", () => {
  openFile(els.openInput.files[0]);
  els.openInput.value = "";
});
els.downloadBtn.addEventListener("click", () => {
  if (!state.id) return;
  window.location.href = `/api/docs/${state.id}/download`;
  toast("Downloading your PDF.", { detail: "Metadata (author, app, dates) has been removed." });
});
els.undoBtn.addEventListener("click", () => history("undo"));
els.redoBtn.addEventListener("click", () => history("redo"));
els.zoomIn.addEventListener("click", () => stepZoom(+1));
els.zoomOut.addEventListener("click", () => stepZoom(-1));
els.findBtn.addEventListener("click", () => (els.drawer.hidden ? openDrawer() : closeDrawer()));
els.drawerClose.addEventListener("click", closeDrawer);
els.replaceForm.addEventListener("submit", replaceAll);
for (const el of [els.findInput, els.caseCheck, els.wordCheck]) {
  el.addEventListener("input", countMatches);
  el.addEventListener("change", countMatches);
}
for (const b of document.querySelectorAll(".seg")) b.addEventListener("click", () => setMode(b.dataset.mode));

// Drag and drop anywhere on the window.
let dragDepth = 0;
window.addEventListener("dragenter", (e) => {
  if (!e.dataTransfer?.types.includes("Files")) return;
  dragDepth++;
  els.desk.classList.add("over");
});
window.addEventListener("dragleave", () => {
  dragDepth = Math.max(0, dragDepth - 1);
  if (!dragDepth) els.desk.classList.remove("over");
});
window.addEventListener("dragover", (e) => e.preventDefault());
window.addEventListener("drop", (e) => {
  e.preventDefault();
  dragDepth = 0;
  els.desk.classList.remove("over");
  openFile(e.dataTransfer?.files?.[0]);
});

window.addEventListener("keydown", (e) => {
  const typing = e.target.closest("input, select, textarea");
  const mod = e.metaKey || e.ctrlKey;
  if (e.key === "Escape") {
    if (state.editor) closeEditor();
    else if (!els.drawer.hidden) closeDrawer();
    return;
  }
  if (mod && e.key.toLowerCase() === "f" && state.id) {
    e.preventDefault();
    openDrawer();
    return;
  }
  if (typing) return;
  if (mod && e.key.toLowerCase() === "z") {
    e.preventDefault();
    history(e.shiftKey ? "redo" : "undo");
  } else if (mod && e.key.toLowerCase() === "y") {
    e.preventDefault();
    history("redo");
  } else if (!mod && state.id && e.key.toLowerCase() === "e") {
    setMode("edit");
  } else if (!mod && state.id && e.key.toLowerCase() === "t") {
    setMode("add");
  }
});

window.addEventListener("beforeunload", (e) => {
  if (state.meta?.canUndo) {
    e.preventDefault();
    e.returnValue = "";
  }
});

let resizeTimer;
window.addEventListener("resize", () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    if (state.editor) closeEditor();
  }, 150);
});
