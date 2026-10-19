"use strict";

/* Shared pieces for the single-purpose tool pages (merge, split, rotate, ...).
   Everything runs in this browser tab; files are never uploaded. */

(function () {
  const S = JSON.parse(document.getElementById("rt-strings").textContent);
  const root = document.getElementById("workbench");

  /* ---------------------------------------------------------------- basics */

  // {name} is replaced by the value; {name:one|other} picks a word by the number ("1 page", "2 pages").
  function t(key, vars = {}) {
    const text = key in S ? S[key] : key;
    return String(text).replace(/\{(\w+)(?::([^|}]*)\|([^}]*))?\}/g, (whole, name, one, other) => {
      if (!(name in vars)) return whole;
      if (one !== undefined) return Number(vars[name]) === 1 ? one : other;
      return vars[name];
    });
  }

  function el(tag, props = {}, ...kids) {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(props)) {
      if (v == null || v === false) continue;
      if (k === "class") node.className = v;
      else if (k === "text") node.textContent = v;
      else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
      else if (v === true) node.setAttribute(k, "");
      else node.setAttribute(k, v);
    }
    for (const kid of kids.flat()) if (kid != null && kid !== false) node.append(kid.nodeType ? kid : document.createTextNode(kid));
    return node;
  }

  function formatSize(bytes) {
    return bytes < 1024 * 1024 ? t("size_kb", { n: Math.max(1, Math.round(bytes / 1024)) }) : t("size_mb", { n: (bytes / 1024 / 1024).toFixed(1) });
  }

  const isPdf = (f) => /\.pdf$/i.test(f.name) || f.type === "application/pdf";
  const baseName = (f) => f.name.replace(/\.[^.]+$/, "");
  const pagesLabel = (n) => (n === 1 ? t("pages_1") : t("pages_n", { n }));

  let startFn = null;
  let dropHandler = null;

  function mount(...nodes) {
    root.replaceChildren(...nodes.flat().filter(Boolean));
  }

  function reset() {
    if (startFn) startFn();
    root.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }

  /* ---------------------------------------------------------------- messages and busy state */

  function message(text, kind = "error") {
    return el("p", { class: `msg ${kind}`, role: kind === "error" ? "alert" : "status", text });
  }

  function busy(text) {
    return el("div", { class: "busy-card", role: "status" }, el("span", { class: "spinner", "aria-hidden": "true" }), el("span", { text: text || t("working") }));
  }

  function fail(e) {
    console.error(e);
    mount(message(t("err", { msg: (e && e.message) || String(e) })), el("button", { class: "tool", type: "button", onclick: reset, text: t("start_over") }));
  }

  function friendly(e) {
    const m = String((e && e.message) || e);
    if (/encrypt|password/i.test(m)) return new Error(t("err_encrypted"));
    return new Error(m.length < 140 && !/\bat\b.*:\d+/.test(m) ? m : t("err_read"));
  }

  /* ---------------------------------------------------------------- drop zone */

  function dropzone({ kind = "pdf", multiple = false, onFiles, compact = false }) {
    const accept = kind === "image" ? "image/*" : "application/pdf,.pdf";
    const input = el("input", { type: "file", accept, multiple, hidden: true });
    const titleKey = kind === "image" ? "drop_images" : multiple ? "drop_pdfs" : "drop_pdf";
    const chooseKey = kind === "image" ? "choose_images" : multiple ? "choose_pdfs" : "choose_pdf";
    const label = el(
      "label",
      { class: "drop" + (compact ? " compact" : "") },
      el("strong", { text: compact ? t("add_more") : t(titleKey) }),
      compact ? null : el("span", { class: "drop-hint", text: t(multiple ? "or_many" : "or_one") }),
      el("span", { class: "primary as-button", text: compact ? t(chooseKey) : t(chooseKey) }),
      input
    );
    const take = (files) => {
      const list = [...files];
      if (list.length) onFiles(multiple ? list : [list[0]]);
    };
    input.addEventListener("change", () => {
      take(input.files);
      input.value = "";
    });
    label.addEventListener("dragover", (e) => {
      e.preventDefault();
      label.classList.add("over");
    });
    label.addEventListener("dragleave", () => label.classList.remove("over"));
    label.addEventListener("drop", (e) => {
      e.preventDefault();
      e.stopPropagation();
      label.classList.remove("over");
      take(e.dataTransfer.files);
    });
    return label;
  }

  // Dropping a file next to the drop zone should use it, not make the browser open it.
  window.addEventListener("dragover", (e) => e.preventDefault());
  window.addEventListener("drop", (e) => {
    e.preventDefault();
    const files = [...(e.dataTransfer?.files || [])];
    if (files.length && dropHandler) dropHandler(files);
  });

  /* ---------------------------------------------------------------- files and results */

  // First page of a PDF as a small canvas, or null when it cannot be drawn.
  async function fileThumb(bytes, width = 72) {
    try {
      const pdf = await openForRender(bytes);
      const canvas = await renderPage(pdf, 1, width * Math.min(2, window.devicePixelRatio || 1));
      canvas.style.width = "100%";
      canvas.style.height = "auto";
      pdf.destroy();
      return canvas;
    } catch {
      return null;
    }
  }

  function thumbBox(extraClass = "") {
    return el("span", { class: `fc-thumb ${extraClass}`.trim(), "aria-hidden": "true" }, el("span", { class: "fc-ext", text: "PDF" }));
  }

  // A PDF shown as a card: first-page preview, name, page count and size.
  function fileCard({ file, count, bytes }) {
    const thumb = thumbBox();
    if (bytes) fileThumb(bytes, 72).then((c) => c && thumb.replaceChildren(c));
    const meta = [count ? pagesLabel(count) : null, formatSize(file.size)].filter(Boolean).join(" · ");
    return el("div", { class: "fc" }, thumb, el("span", { class: "fc-text" }, el("strong", { class: "fc-name", title: file.name, text: file.name }), el("span", { class: "fc-meta", text: meta })));
  }

  const CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>';
  const DOWNLOAD = '<svg viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10 3.5v9M6.5 9.5 10 13l3.5-3.5M4 16h12"/></svg>';

  function resultPreview(blob) {
    const box = thumbBox("big");
    if (blob.type === "application/pdf") {
      blob.arrayBuffer().then((b) => fileThumb(new Uint8Array(b), 120)).then((c) => c && box.replaceChildren(c));
    } else if (blob.type.startsWith("image/")) {
      box.replaceChildren(el("img", { src: URL.createObjectURL(blob), alt: "" }));
    } else {
      box.classList.add("zip");
      box.replaceChildren(el("span", { class: "fc-ext", text: "ZIP" }));
    }
    return box;
  }

  function showResult({ blob, filename, note, extra }) {
    const url = URL.createObjectURL(blob);
    const link = el("a", { class: "primary big", href: url, download: filename });
    link.insertAdjacentHTML("beforeend", DOWNLOAD);
    link.append(t("download"));
    const check = el("span", { class: "result-check", "aria-hidden": "true" });
    check.innerHTML = CHECK;
    const next = (S.next || []).map((n) => el("a", { class: "chip", href: n.href, text: n.label }));
    mount(
      el(
        "div",
        { class: "result" },
        check,
        el("p", { class: "result-title", text: t("done") }),
        el("p", { class: "result-note", text: note || t("done_note") }),
        el(
          "div",
          { class: "result-file" },
          resultPreview(blob),
          el("span", { class: "fc-text" }, el("strong", { class: "fc-name", title: filename, text: filename }), el("span", { class: "fc-meta", text: formatSize(blob.size) })),
          link
        ),
        extra || null,
        el("div", { class: "result-actions" }, el("button", { class: "tool", type: "button", onclick: reset, text: t("start_over") })),
        next.length ? el("p", { class: "result-next" }, t("continue_with") + " ", next) : null
      )
    );
    link.focus();
  }

  const saveBlob = (bytes, type) => new Blob([bytes], { type });

  /* ---------------------------------------------------------------- PDF helpers */

  function needLib(name) {
    if (typeof window[name] === "undefined") throw new Error("Library missing: " + name);
  }

  // pdf-lib, pdf.js and fflate are large, so they load when the visitor first shows intent
  // (pointing at the tool, choosing a file) rather than with the page.
  let libsPromise = null;
  function libs() {
    if (!libsPromise) {
      libsPromise = Promise.all(
        (S.libs || []).map(
          (src) =>
            new Promise((resolve, reject) => {
              const tag = document.createElement("script");
              tag.src = src;
              tag.onload = resolve;
              tag.onerror = () => reject(new Error("Could not load " + src));
              document.head.append(tag);
            })
        )
      );
    }
    return libsPromise;
  }
  for (const type of ["pointerover", "focusin", "touchstart"]) root.addEventListener(type, () => libs().catch(() => {}), { once: true, passive: true });

  async function readBytes(file) {
    return new Uint8Array(await file.arrayBuffer());
  }

  async function loadDoc(bytes) {
    await libs();
    needLib("PDFLib");
    try {
      return await PDFLib.PDFDocument.load(bytes, { updateMetadata: false });
    } catch (e) {
      throw friendly(e);
    }
  }

  // New documents carry no producer or dates of their own.
  async function newDoc() {
    await libs();
    needLib("PDFLib");
    return PDFLib.PDFDocument.create({ updateMetadata: false });
  }

  let pdfjsReady = false;
  function pdfjs() {
    needLib("pdfjsLib");
    if (!pdfjsReady) {
      pdfjsLib.GlobalWorkerOptions.workerSrc = "/vendor/pdf.worker.min.js";
      pdfjsReady = true;
    }
    return pdfjsLib;
  }

  async function openForRender(bytes) {
    await libs();
    try {
      return await pdfjs().getDocument({ data: bytes.slice() }).promise;
    } catch (e) {
      throw friendly(e);
    }
  }

  async function renderPage(pdf, number, width) {
    const page = await pdf.getPage(number);
    const base = page.getViewport({ scale: 1 });
    const viewport = page.getViewport({ scale: width / base.width });
    const canvas = el("canvas");
    canvas.width = Math.ceil(viewport.width);
    canvas.height = Math.ceil(viewport.height);
    await page.render({ canvasContext: canvas.getContext("2d"), viewport }).promise;
    return canvas;
  }

  /* ---------------------------------------------------------------- placing things on a page */

  // pdf-lib draws in the page's own (unrotated) space. This turns a point on the page as it is
  // DISPLAYED (origin bottom-left) into that space, so text and images land right on rotated pages.
  function pageSpace(page) {
    const box = page.getCropBox();
    const rot = ((page.getRotation().angle % 360) + 360) % 360;
    const W = box.width, H = box.height;
    const sideways = rot % 180 !== 0;
    const map = (vx, vy) => {
      const [x, y] = rot === 0 ? [vx, vy] : rot === 90 ? [W - vy, vx] : rot === 180 ? [W - vx, H - vy] : [vy, H - vx];
      return { x: box.x + x, y: box.y + y };
    };
    // the other way round: a point in the page's own space -> where it shows up (origin bottom-left)
    const unmap = (px, py) => {
      const x = px - box.x, y = py - box.y;
      return rot === 0 ? { x, y } : rot === 90 ? { x: y, y: W - x } : rot === 180 ? { x: W - x, y: H - y } : { x: H - y, y: x };
    };
    return { vw: sideways ? H : W, vh: sideways ? W : H, rot, map, unmap, box };
  }

  const hexColor = (hex) => {
    const n = parseInt(hex.replace("#", ""), 16);
    return PDFLib.rgb(((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255);
  };

  // A page drawn at a given CSS width, ready for things to be laid on top of it.
  async function previewStage(pdf, number, width) {
    width = Math.min(width, Math.max(240, (root.clientWidth || 400) - 40)); // never wider than the workbench
    const page = await pdf.getPage(number);
    const pts = page.getViewport({ scale: 1 });
    const canvas = await renderPage(pdf, number, width * Math.min(2, window.devicePixelRatio || 1));
    const height = Math.round((width * pts.height) / pts.width);
    canvas.style.cssText = `display:block;width:${width}px;height:${height}px`;
    const stage = el("div", { class: "stage", style: `width:${width}px;height:${height}px` }, canvas);
    return { el: stage, width, height, scale: width / pts.width, vw: pts.width, vh: pts.height };
  }

  function field(label, input, extra) {
    return el("label", { class: "field inline" }, el("span", { text: label }), input, extra || null);
  }

  function selectField(label, choices, value, onChange) {
    const input = el("select", { onchange: () => onChange(input.value) }, choices.map(([v, text]) => el("option", { value: v, selected: v === value, text })));
    return field(label, input);
  }

  function rangeField(label, { min, max, step = 1, value }, onInput, format = (v) => v) {
    const out = el("output", { class: "range-out", text: format(value) });
    const input = el("input", { type: "range", min, max, step, value, class: "slider" });
    input.addEventListener("input", () => {
      out.textContent = format(+input.value);
      onInput(+input.value);
    });
    return field(label, input, out);
  }

  /* ---------------------------------------------------------------- page ranges: "1-3, 5, 8-" */

  function parseRanges(text, count) {
    const out = [];
    for (const raw of String(text).split(/[,;\s]+/).filter(Boolean)) {
      const m = raw.match(/^(\d*)\s*[-–]\s*(\d*)$/);
      let from, to;
      if (m && (m[1] || m[2])) {
        from = m[1] ? +m[1] : 1;
        to = m[2] ? +m[2] : count;
      } else if (/^\d+$/.test(raw)) {
        from = to = +raw;
      } else {
        return null;
      }
      if (from < 1 || to < from || to > count) return null;
      out.push([from, to]);
    }
    return out;
  }

  const expand = (ranges) => [...new Set(ranges.flatMap(([a, b]) => Array.from({ length: b - a + 1 }, (_, i) => a + i)))];

  function compact(pages) {
    const sorted = [...pages].sort((a, b) => a - b);
    const parts = [];
    for (let i = 0; i < sorted.length; ) {
      let j = i;
      while (j + 1 < sorted.length && sorted[j + 1] === sorted[j] + 1) j++;
      parts.push(j > i ? `${sorted[i]}-${sorted[j]}` : String(sorted[i]));
      i = j + 1;
    }
    return parts.join(", ");
  }

  /* ---------------------------------------------------------------- page grid (thumbnails you can select or turn) */

  function pageGrid({ pdf, count, mode, onChange }) {
    const state = { selected: new Set(), rotation: new Array(count + 1).fill(0) };
    const grid = el("div", { class: "grid", role: "list" });
    const cells = [];
    const io = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          io.unobserve(entry.target);
          const cell = cells[+entry.target.dataset.page];
          renderPage(pdf, +entry.target.dataset.page, 220)
            .then((canvas) => {
              cell.thumb.replaceChildren(canvas);
              paint(+entry.target.dataset.page);
            })
            .catch(() => cell.thumb.classList.add("failed"));
        }
      },
      { rootMargin: "400px" }
    );

    const changed = () => onChange && onChange(state);

    const toggle = (n) => {
      if (state.selected.has(n)) state.selected.delete(n);
      else state.selected.add(n);
      paint(n);
      changed();
    };

    const paint = (n) => {
      const cell = cells[n];
      const on = state.selected.has(n);
      cell.item.classList.toggle("selected", on);
      cell.item.setAttribute("aria-pressed", String(on));
      const canvas = cell.thumb.querySelector("canvas");
      if (canvas) {
        const turn = state.rotation[n];
        let k = 1;
        if (turn % 180) k = Math.min(cell.thumb.clientWidth / canvas.offsetHeight, cell.thumb.clientHeight / canvas.offsetWidth, 1);
        canvas.style.transform = `rotate(${turn}deg) scale(${k})`;
      }
    };

    for (let n = 1; n <= count; n++) {
      const thumb = el("div", { class: "thumb" });
      const label = el("span", { class: "thumb-label", text: t("page_n", { n }) });
      const kids = [thumb, label];
      let item;
      if (mode === "rotate") {
        const turn = (delta) => {
          state.rotation[n] = (state.rotation[n] + delta + 360) % 360;
          paint(n);
          changed();
        };
        kids.push(
          el(
            "span",
            { class: "turn" },
            el("button", { type: "button", class: "icon", "aria-label": `${t("rotate_left")} (${t("page_n", { n })})`, title: t("rotate_left"), onclick: () => turn(-90), text: "↺" }),
            el("button", { type: "button", class: "icon", "aria-label": `${t("rotate_right")} (${t("page_n", { n })})`, title: t("rotate_right"), onclick: () => turn(90), text: "↻" })
          )
        );
        item = el("div", { class: "cell", role: "listitem", "data-page": n }, kids);
      } else {
        item = el("button", { type: "button", class: "cell", role: "listitem", "aria-pressed": "false", "data-page": n, onclick: () => toggle(n) }, kids);
      }
      cells[n] = { item, thumb };
      grid.append(item);
      io.observe(item);
    }

    return {
      el: grid,
      state,
      select(pages) {
        state.selected = new Set(pages);
        for (let n = 1; n <= count; n++) paint(n);
        changed();
      },
      selectAll() {
        this.select(Array.from({ length: count }, (_, i) => i + 1));
      },
      turnAll(delta) {
        for (let n = 1; n <= count; n++) state.rotation[n] = (state.rotation[n] + delta + 360) % 360;
        for (let n = 1; n <= count; n++) paint(n);
        changed();
      },
    };
  }

  // A text box such as "2, 4-6" that stays in step with the grid's selection.
  function rangeInput({ grid, count, label, placeholder }) {
    const input = el("input", { type: "text", class: "range-input", inputmode: "numeric", autocomplete: "off", spellcheck: "false", placeholder });
    const wrap = el("label", { class: "field inline" }, el("span", { text: label }), input);
    input.addEventListener("input", () => {
      const ranges = parseRanges(input.value, count);
      input.classList.toggle("bad", input.value.trim() !== "" && !ranges);
      if (ranges) grid.select(expand(ranges));
    });
    return {
      el: wrap,
      sync(selected) {
        if (document.activeElement !== input) input.value = compact(selected);
      },
    };
  }

  /* ---------------------------------------------------------------- reorderable list (merge, images) */

  function reorderList({ items, render, onChange }) {
    const list = el("ol", { class: "files" });
    function paint() {
      list.replaceChildren(
        ...items.map((item, i) =>
          el(
            "li",
            { class: "file", draggable: "true", "data-i": i },
            el("span", { class: "file-n", text: i + 1 }),
            render(item, i),
            el(
              "span",
              { class: "file-actions" },
              el("button", { type: "button", class: "icon", title: t("up"), "aria-label": t("up"), disabled: i === 0, onclick: () => move(i, i - 1), text: "↑" }),
              el("button", { type: "button", class: "icon", title: t("down"), "aria-label": t("down"), disabled: i === items.length - 1, onclick: () => move(i, i + 1), text: "↓" }),
              el("button", { type: "button", class: "icon", title: t("remove"), "aria-label": t("remove"), onclick: () => remove(i), text: "✕" })
            )
          )
        )
      );
      onChange && onChange(items);
    }
    function move(from, to) {
      if (to < 0 || to >= items.length) return;
      items.splice(to, 0, items.splice(from, 1)[0]);
      paint();
    }
    function remove(i) {
      items.splice(i, 1);
      paint();
    }
    let dragFrom = null;
    list.addEventListener("dragstart", (e) => {
      const li = e.target.closest("li");
      if (!li) return;
      dragFrom = +li.dataset.i;
      e.dataTransfer.effectAllowed = "move";
      e.dataTransfer.setData("text/plain", "");
    });
    list.addEventListener("dragover", (e) => {
      if (dragFrom != null) e.preventDefault();
    });
    list.addEventListener("drop", (e) => {
      const li = e.target.closest("li");
      if (dragFrom == null || !li) return;
      e.preventDefault();
      e.stopPropagation();
      move(dragFrom, +li.dataset.i);
      dragFrom = null;
    });
    paint();
    return { el: list, repaint: paint, items };
  }

  /* ---------------------------------------------------------------- open one PDF, then hand over */

  // Reads the file, loads it for editing (pdf-lib) and for drawing (pdf.js), and calls onReady.
  function pdfFlow(onReady) {
    async function open(selected) {
      const file = selected[0];
      if (!isPdf(file)) return mount(message(t("err_not_pdf", { name: file.name })), dropzone({ onFiles: open }));
      mount(busy());
      try {
        const bytes = await readBytes(file);
        const doc = await loadDoc(bytes);
        const pdf = await openForRender(bytes);
        await onReady({ file, bytes, doc, pdf, count: doc.getPageCount() });
      } catch (e) {
        mount(message(e.message), dropzone({ onFiles: open }));
      }
    }
    dropHandler = open;
    mount(dropzone({ onFiles: open }));
  }

  const actionsRow = (...kids) => el("div", { class: "actions-row" }, ...kids);
  const restartButton = () => el("button", { class: "tool", type: "button", onclick: () => reset(), text: t("start_over") });

  /* ---------------------------------------------------------------- public API */

  window.RT = {
    t, el, S, root, mount, reset, message, busy, fail, friendly, formatSize, isPdf, baseName, pagesLabel,
    dropzone, showResult, fileCard, fileThumb, saveBlob, readBytes, loadDoc, newDoc, pdfjs, openForRender, renderPage,
    parseRanges, expand, compact, pageGrid, rangeInput, reorderList, libs, pageSpace, hexColor, previewStage, field, selectField, rangeField, pdfFlow, actionsRow, restartButton,
    setDropHandler: (fn) => (dropHandler = fn),
    run(fn) {
      startFn = fn;
      fn();
    },
  };
})();
