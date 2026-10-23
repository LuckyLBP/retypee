"use strict";

/* Retypee frontend. Talks to the editing engine (PyMuPDF in Pyodide) running in
   worker.js. Everything happens in this browser tab; nothing is uploaded. */

const $ = (sel) => document.querySelector(sel);

/* ---------------------------------------------------------------- language */

/* Swedish is the main language. The English page (/en/) sets <html lang="en">. */
const LANG = document.documentElement.lang === "en" ? "en" : "sv";
const STRINGS = {
  match_original: ["Match original", "Matcha originalet"],
  ready: ["Ready. Your PDF stays on this device.", "Redo. Din PDF stannar på den här enheten."],
  p_download: ["Downloading the editor engine…", "Hämtar redigeringsmotorn…"],
  p_tools: ["Loading PDF tools…", "Laddar PDF-verktyg…"],
  start_fail: ["The editor could not start: {text}. Reload the page to try again.", "Redigeraren kunde inte starta: {text}. Ladda om sidan och försök igen."],
  start_fail_short: ["The editor could not start: {text}", "Redigeraren kunde inte starta: {text}"],
  not_available: ["The editor is not available.", "Redigeraren är inte tillgänglig."],
  generic_error: ["Something went wrong.", "Något gick fel."],
  not_pdf: ['"{name}" is not a PDF. Choose a file that ends in .pdf.', '"{name}" är ingen PDF. Välj en fil som slutar på .pdf.'],
  confirm_open: ["Open a new file? Changes you have not downloaded will be lost.", "Öppna en ny fil? Ändringar du inte laddat ner går förlorade."],
  loading_open: ["Loading the editor, then opening your PDF…", "Laddar redigeraren och öppnar sedan din PDF…"],
  page_alt: ["Page {n}", "Sida {n}"],
  no_text: ["No editable text on this page. It is probably a scanned image.", "Ingen redigerbar text på den här sidan. Det är troligen en skannad bild."],
  aria_edit: ["Edit text: {text}", "Redigera text: {text}"],
  aria_rotated: ["Rotated text, cannot be edited: {text}", "Roterad text, kan inte redigeras: {text}"],
  rotated: ["Rotated or vertical text cannot be edited yet.", "Roterad eller lodrät text kan inte redigeras ännu."],
  ph_type: ["Type text", "Skriv text"],
  aria_newtext: ["New text", "Ny text"],
  aria_addtext: ["Text to add", "Text att lägga till"],
  unnamed_font: ["unnamed font", "namnlöst typsnitt"],
  orig_meta: ["Original: <b>{font}</b>, {size} pt", "Original: <b>{font}</b>, {size} pt"],
  add_hint: ["Enter adds the text, Esc cancels", "Enter lägger till texten, Esc avbryter"],
  font: ["Font", "Typsnitt"],
  size_aria: ["Font size in points", "Teckenstorlek i punkter"],
  size_title: ["Size (pt)", "Storlek (pt)"],
  color_aria: ["Text colour", "Textfärg"],
  color_title: ["Colour", "Färg"],
  bold: ["Bold", "Fet"],
  italic: ["Italic", "Kursiv"],
  fit: ["Squeeze to fit", "Pressa ihop så den ryms"],
  delete: ["Delete", "Ta bort"],
  cancel: ["Cancel", "Avbryt"],
  apply: ["Apply", "Verkställ"],
  add_text: ["Add text", "Lägg till text"],
  text_added: ["Text added.", "Text tillagd."],
  font_detail: ["Font: {label}", "Typsnitt: {label}"],
  text_deleted: ["Text deleted.", "Text borttagen."],
  fs_embedded: ["taken from the PDF", "hämtat från PDF-filen"],
  fs_local: ["a font you added", "ett typsnitt du lagt till"],
  fs_bundled: ["a close match", "en nära matchning"],
  fs_standard: ["standard fallback", "standardreserv"],
  bundled_detail: ["Not the original font, but one with matching letter widths, so spacing should still line up.", "Inte originaltypsnittet, men ett med matchande teckenbredd, så mellanrummen bör ändå stämma."],
  std_detail: ["The original font was not found. Use Add font to give the editor its .ttf or .otf file for an exact match.", "Originaltypsnittet hittades inte. Använd Lägg till typsnitt för att ge redigeraren dess .ttf- eller .otf-fil för en exakt matchning."],
  saved_with: ["Saved with {label} ({where}).", "Sparad med {label} ({where})."],
  undone: ["Undone.", "Ångrat."],
  redone: ["Redone.", "Gjort om."],
  find_hint: ["Type something to find.", "Skriv något att söka efter."],
  replace_all: ["Replace all", "Ersätt alla"],
  replace_all_n: ["Replace all {n}", "Ersätt alla {n}"],
  no_matches: ["No matches.", "Inga träffar."],
  match_one: ["<b>{n}</b> match on {where}.", "<b>{n}</b> träff på {where}."],
  match_many: ["<b>{n}</b> matches on {where}.", "<b>{n}</b> träffar på {where}."],
  where_page: ["page {p}", "sida {p}"],
  where_pages: ["pages {p}", "sidorna {p}"],
  replaced_one: ["Replaced 1 time.", "Ersatte 1 gång."],
  replaced_many: ["Replaced {n} times.", "Ersatte {n} gånger."],
  none_to_replace: ["No matches to replace.", "Inga träffar att ersätta."],
  downloading: ["Downloading your PDF.", "Laddar ner din PDF."],
  downloading_detail: ["Metadata (author, app, dates) has been removed.", "Metadata (författare, program, datum) har tagits bort."],
  font_added: ["Font added: {name}", "Typsnitt tillagt: {name}"],
  font_added_detail: ["It is used when a PDF asks for it, and appears in the font menu. It is forgotten when you close this tab.", "Det används när en PDF ber om det och finns i typsnittsmenyn. Det glöms när du stänger fliken."],
};
function t(key, vars = {}) {
  const entry = STRINGS[key];
  const text = entry ? entry[LANG === "en" ? 0 : 1] : key;
  return text.replace(/\{(\w+)\}/g, (_, name) => (name in vars ? vars[name] : `{${name}}`));
}
const ZOOM_STEPS = [0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3];
const FONT_SOURCE = { embedded: t("fs_embedded"), local: t("fs_local"), bundled: t("fs_bundled"), standard: t("fs_standard") };

const state = {
  id: null,
  meta: null,
  zoom: 1,
  mode: "edit",
  pages: [],
  fonts: [{ value: "auto", label: t("match_original") }],
  editor: null,
  flash: null,
  busy: 0,
  railOpen: true,
  current: -1,
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
  engineStatus: $("#engineStatus"),
  fontInput: $("#fontInput"),
  fontBtn: $("#fontBtn"),
  rail: $("#rail"),
  railList: $("#railList"),
  railBtn: $("#railBtn"),
  prevPage: $("#prevPage"),
  nextPage: $("#nextPage"),
  pageLabel: $("#pageLabel"),
  zoomFit: $("#zoomFit"),
};

/* ---------------------------------------------------------------- helpers */

/* The engine runs in a Web Worker. Requests use the same routes the local
   server has, so the rest of this file does not care where the work happens. */

const engine = { worker: null, pending: new Map(), nextId: 1, ready: false };

function startEngine() {
  const worker = new Worker("/worker.js");
  engine.worker = worker;
  worker.onmessage = ({ data }) => {
    if (data.type === "progress") return setEngineStatus(t(data.key));
    if (data.type === "ready") {
      engine.ready = true;
      return setEngineStatus(t("ready"));
    }
    if (data.type === "fatal") {
      setEngineStatus(t("start_fail", { text: data.text }), true);
      for (const { reject } of engine.pending.values()) reject(new Error(t("not_available")));
      engine.pending.clear();
      return;
    }
    const entry = engine.pending.get(data.id);
    if (!entry) return;
    engine.pending.delete(data.id);
    if (data.error !== undefined) {
      const err = new Error(data.error);
      err.status = data.status;
      entry.reject(err);
    } else {
      entry.resolve(data);
    }
  };
  worker.onerror = (e) => setEngineStatus(t("start_fail_short", { text: e.message }), true);
}

function setEngineStatus(text, error = false) {
  els.engineStatus.textContent = text;
  els.engineStatus.classList.remove("idle");
  els.engineStatus.classList.toggle("error", error);
  els.engineStatus.classList.toggle("ready", engine.ready && !error);
}

function callEngine(path, { method = "GET", json, file } = {}) {
  ensureEngine();
  return new Promise((resolve, reject) => {
    const id = engine.nextId++;
    engine.pending.set(id, { resolve, reject });
    const message = { id, method, url: path, lang: LANG };
    if (json !== undefined) message.json = JSON.stringify(json);
    if (file) {
      message.file = file;
      engine.worker.postMessage(message, [file.bytes]);
    } else {
      engine.worker.postMessage(message);
    }
  });
}

async function api(path, options = {}) {
  setBusy(+1);
  try {
    return (await callEngine(path, options)).data;
  } finally {
    setBusy(-1);
  }
}

/* Binary results: page images and the edited PDF. */
async function apiBytes(path) {
  const { bytes, mime, filename } = await callEngine(path);
  return { blob: new Blob([bytes], { type: mime }), filename };
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
  toast(err.message || t("generic_error"), { error: true });
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
    toast(t("not_pdf", { name: file.name }), { error: true });
    return;
  }
  if (state.meta?.canUndo && !confirm(t("confirm_open"))) return;
  try {
    if (!engine.ready) setEngineStatus(t("loading_open"));
    const bytes = await file.arrayBuffer();
    const data = await api("/api/docs", { method: "POST", file: { name: file.name, bytes } });
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
  document.body.classList.add("has-doc");
  els.empty.hidden = true;
  els.pages.hidden = false;
  els.tools.hidden = false;
  state.railOpen = window.innerWidth >= 1100;
  applyRail();
  els.openBtn.hidden = false;
  els.downloadBtn.hidden = false;
  els.fileName.textContent = state.meta.name;
  document.title = `${state.meta.name} · Retypee`;
  state.zoom = fitZoom();
  els.zoomLabel.textContent = `${Math.round(state.zoom * 100)}%`;
  buildPages();
  updateMeta(state.meta);
  els.desk.scrollTo(0, 0);
  state.current = -1;
  updateCurrent();
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
  railObserver.disconnect();
  for (const old of state.pages) {
    if (old.imageUrl) URL.revokeObjectURL(old.imageUrl);
    if (old.rail?.url) URL.revokeObjectURL(old.rail.url);
  }
  els.pages.innerHTML = "";
  els.railList.innerHTML = "";
  state.pages = state.meta.pages.map((size, i) => {
    const el = document.createElement("div");
    el.className = "page";
    el.dataset.index = i;
    const num = document.createElement("span");
    num.className = "page-num";
    num.textContent = i + 1;
    const img = document.createElement("img");
    img.alt = t("page_alt", { n: i + 1 });
    img.draggable = false;
    const overlay = document.createElement("div");
    overlay.className = "overlay";
    overlay.addEventListener("click", (e) => onPageClick(e, i));
    el.append(num, img, overlay);
    els.pages.appendChild(el);
    const page = { el, img, overlay, size, units: null, rev: 0, imageKey: "", imageUrl: "", visible: false, loadingUnits: false, rail: null };
    layoutPage(page);
    observer.observe(el);
    page.rail = buildRailItem(i, size);
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
    const path = `/api/docs/${state.id}/pages/${i}/image?zoom=${renderZoom()}&v=${page.rev}-${state.meta.version}`;
    apiBytes(path)
      .then(({ blob }) => {
        if (page.imageKey !== key) return;
        const url = URL.createObjectURL(blob);
        page.img.src = url;
        if (page.imageUrl) URL.revokeObjectURL(page.imageUrl);
        page.imageUrl = url;
      })
      .catch((err) => {
        if (page.imageKey === key) page.imageKey = "";
        fail(err);
      });
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
    note.textContent = t("no_text");
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
    b.setAttribute("aria-label", u.editable ? t("aria_edit", { text: u.text }) : t("aria_rotated", { text: u.text }));
    if (!u.editable) b.title = t("rotated");
    b.addEventListener("click", (e) => {
      e.stopPropagation();
      if (state.mode !== "edit") return;
      if (!u.editable) {
        toast(t("rotated"), { error: true });
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

/* ---------------------------------------------------------------- page rail and navigation */

const railObserver = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) if (entry.isIntersecting) loadThumb(Number(entry.target.dataset.index));
  },
  { root: els.rail, rootMargin: "400px 0px" }
);

function buildRailItem(i, size) {
  const item = document.createElement("button");
  item.type = "button";
  item.className = "rail-item";
  item.dataset.index = i;
  item.setAttribute("aria-label", t("page_alt", { n: i + 1 }));
  const thumb = document.createElement("span");
  thumb.className = "rail-thumb";
  thumb.style.aspectRatio = `${size.w} / ${size.h}`;
  const img = document.createElement("img");
  img.alt = "";
  img.draggable = false;
  thumb.appendChild(img);
  const num = document.createElement("span");
  num.className = "rail-num";
  num.textContent = i + 1;
  item.append(thumb, num);
  item.addEventListener("click", () => goToPage(i));
  els.railList.appendChild(item);
  railObserver.observe(item);
  return { item, img, key: "", url: "" };
}

function loadThumb(i) {
  const page = state.pages[i];
  if (!page?.rail || els.rail.hidden) return;
  const key = `${page.rev}-${state.meta.version}`;
  if (page.rail.key === key) return;
  page.rail.key = key;
  const zoom = Math.min(1, (160 * (window.devicePixelRatio || 1)) / page.size.w).toFixed(2);
  apiBytes(`/api/docs/${state.id}/pages/${i}/image?zoom=${zoom}`)
    .then(({ blob }) => {
      if (page.rail.key !== key) return;
      const url = URL.createObjectURL(blob);
      page.rail.img.src = url;
      if (page.rail.url) URL.revokeObjectURL(page.rail.url);
      page.rail.url = url;
    })
    .catch(() => {
      if (page.rail.key === key) page.rail.key = "";
    });
}

function applyRail() {
  els.rail.hidden = !state.railOpen;
  els.railBtn.setAttribute("aria-pressed", String(state.railOpen));
  if (state.railOpen) for (let i = 0; i < state.pages.length; i++) if (state.pages[i].rail) loadThumb(i);
}

// Which page is in view? The first one that still has a good part below the toolbar.
function updateCurrent() {
  if (!state.pages.length) return;
  const line = els.desk.getBoundingClientRect().top + 96;
  let current = state.pages.length - 1;
  for (let i = 0; i < state.pages.length; i++) {
    if (state.pages[i].el.getBoundingClientRect().bottom > line + 40) {
      current = i;
      break;
    }
  }
  setCurrent(current);
}

function setCurrent(i) {
  if (state.current === i) return;
  state.current = i;
  els.pageLabel.textContent = `${i + 1} / ${state.pages.length}`;
  state.pages.forEach((p, j) => p.rail?.item.classList.toggle("active", j === i));
  els.prevPage.disabled = i <= 0;
  els.nextPage.disabled = i >= state.pages.length - 1;
  if (!els.rail.hidden) state.pages[i].rail.item.scrollIntoView({ block: "nearest" });
}

function goToPage(i) {
  const page = state.pages[Math.max(0, Math.min(state.pages.length - 1, i))];
  if (page) page.el.scrollIntoView({ block: "start", behavior: "smooth" });
}

function refreshPages(indices) {
  for (const i of indices) {
    const page = state.pages[i];
    if (!page) continue;
    page.rev += 1;
    page.units = null;
    if (page.visible) ensurePage(i);
    if (page.rail) {
      page.rail.key = "";
      railObserver.unobserve(page.rail.item);
      railObserver.observe(page.rail.item); // fires again with the current visibility
    }
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
  input.placeholder = isEdit ? "" : t("ph_type");
  input.setAttribute("aria-label", isEdit ? t("aria_newtext") : t("aria_addtext"));
  input.style.height = `${height * z}px`;
  input.style.fontSize = `${size * z}px`;
  input.style.fontFamily = cssFamily(isEdit ? u.font : "Helvetica");
  input.style.color = color;

  const panel = document.createElement("div");
  panel.className = "editor-panel";
  const fontValue = isEdit ? "auto" : state.addDefaults.font;
  const meta = isEdit
    ? t("orig_meta", { font: escapeHtml(u.font.startsWith("Type3") ? t("unnamed_font") : u.font.replace(/^[A-Z]{6}\+/, "")), size: Math.round(u.size * 10) / 10 })
    : t("add_hint");
  panel.innerHTML = `
    <div class="editor-row">
      <select data-k="font" aria-label="${t("font")}">${fontOptions(fontValue)}</select>
      <input data-k="size" type="number" min="2" max="400" step="0.5" value="${Math.round(size * 10) / 10}" aria-label="${t("size_aria")}" title="${t("size_title")}">
      <input data-k="color" type="color" value="${color}" aria-label="${t("color_aria")}" title="${t("color_title")}">
      <button type="button" class="toggle" data-k="bold" aria-pressed="${isEdit ? u.bold : state.addDefaults.bold}" title="${t("bold")}" aria-label="${t("bold")}"><b>B</b></button>
      <button type="button" class="toggle" data-k="italic" aria-pressed="${isEdit ? u.italic : state.addDefaults.italic}" title="${t("italic")}" aria-label="${t("italic")}"><i>I</i></button>
      ${isEdit ? `<label class="inline-check"><input data-k="fit" type="checkbox"> ${t("fit")}</label>` : ""}
    </div>
    <div class="editor-row">
      <span class="editor-meta">${meta}</span>
      ${isEdit ? `<button type="button" class="ghost danger" data-a="delete">${t("delete")}</button>` : ""}
      <button type="button" class="ghost" data-a="cancel">${t("cancel")}</button>
      <button type="button" class="primary" data-a="apply">${isEdit ? t("apply") : t("add_text")}</button>
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
      toast(t("text_added"), { detail: t("font_detail", { label: data.font.label }) });
    }
  } catch (err) {
    fail(err);
  }
}

function announceFont(font, deleted) {
  if (deleted) return toast(t("text_deleted"));
  if (!font || font.source === "unchanged") return;
  const where = FONT_SOURCE[font.source] || font.source;
  const detail =
    font.source === "standard" ? t("std_detail")
    : font.source === "bundled" ? t("bundled_detail")
    : "";
  toast(t("saved_with", { label: font.label, where }), { detail });
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
  updateCurrent();
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
    toast(kind === "undo" ? t("undone") : t("redone"));
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
      els.matchCount.textContent = t("find_hint");
      els.replaceAllBtn.disabled = true;
      els.replaceAllBtn.textContent = t("replace_all");
      return;
    }
    try {
      const data = await api(`/api/docs/${state.id}/find`, {
        method: "POST",
        json: { find, caseSensitive: els.caseCheck.checked, wholeWord: els.wordCheck.checked },
      });
      if (seq !== countSeq) return;
      if (data.count === 0) {
        els.matchCount.textContent = t("no_matches");
      } else {
        const pages = data.pages.map((p) => p + 1);
        const where = pages.length === 1 ? t("where_page", { p: pages[0] }) : t("where_pages", { p: `${pages.slice(0, 8).join(", ")}${pages.length > 8 ? "…" : ""}` });
        els.matchCount.innerHTML = t(data.count === 1 ? "match_one" : "match_many", { n: data.count, where });
      }
      els.replaceAllBtn.disabled = data.count === 0;
      els.replaceAllBtn.textContent = data.count ? t("replace_all_n", { n: data.count }) : t("replace_all");
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
    toast(data.count ? (data.count === 1 ? t("replaced_one") : t("replaced_many", { n: data.count })) : t("none_to_replace"));
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
els.downloadBtn.addEventListener("click", async () => {
  if (!state.id) return;
  try {
    setBusy(+1);
    const { blob, filename } = await apiBytes(`/api/docs/${state.id}/download`);
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 10000);
    toast(t("downloading"), { detail: t("downloading_detail") });
  } catch (err) {
    fail(err);
  } finally {
    setBusy(-1);
  }
});
els.fontInput.addEventListener("change", async () => {
  const font = els.fontInput.files[0];
  els.fontInput.value = "";
  if (!font) return;
  try {
    const bytes = await font.arrayBuffer();
    const data = await api("/api/fonts", { method: "POST", file: { name: font.name, bytes } });
    state.fonts = data.fonts;
    toast(t("font_added", { name: font.name }), { detail: t("font_added_detail") });
  } catch (err) {
    fail(err);
  }
});
els.undoBtn.addEventListener("click", () => history("undo"));
els.redoBtn.addEventListener("click", () => history("redo"));
els.zoomIn.addEventListener("click", () => stepZoom(+1));
els.zoomOut.addEventListener("click", () => stepZoom(-1));
els.zoomFit.addEventListener("click", () => state.meta && setZoom(fitZoom()));
els.railBtn.addEventListener("click", () => {
  state.railOpen = !state.railOpen;
  applyRail();
  updateCurrent();
});
els.prevPage.addEventListener("click", () => goToPage(state.current - 1));
els.nextPage.addEventListener("click", () => goToPage(state.current + 1));
let scrollTick = false;
els.desk.addEventListener(
  "scroll",
  () => {
    if (scrollTick) return;
    scrollTick = true;
    requestAnimationFrame(() => {
      scrollTick = false;
      updateCurrent();
    });
  },
  { passive: true }
);
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

/* The engine is about 25 MB, so it starts when the visitor shows intent, not on
   page load. That keeps the first view light for people and for crawlers. */
let engineStarted = false;
function ensureEngine() {
  if (engineStarted) return;
  engineStarted = true;
  setEngineStatus(t("p_download"));
  startEngine();
}
for (const type of ["pointerover", "pointerdown", "focusin", "touchstart"]) {
  els.drop.addEventListener(type, ensureEngine, { once: true, passive: true });
}
els.fontBtn.addEventListener("pointerdown", ensureEngine, { once: true });
window.addEventListener("dragenter", ensureEngine, { once: true });
