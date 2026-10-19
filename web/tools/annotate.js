"use strict";

/* Highlight and draw: a highlighter, a pen and text notes on every page, written into the file with pdf-lib.
   Marks are kept in page points (origin top-left, as displayed) and mapped back onto each page when saving. */
RT.run(function start() {
  const { t, el } = RT;
  const NS = "http://www.w3.org/2000/svg";
  const svgEl = (tag, attrs = {}) => {
    const n = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    return n;
  };
  const PALETTE = { hl: ["#ffe14d", "#7ee08a", "#ff8fc1", "#7cc4ff"], pen: ["#1b1713", "#d12c2c", "#1f3fb8", "#1b8a3a"], text: ["#1b1713", "#d12c2c", "#1f3fb8", "#1b8a3a"] };
  const HL_OPACITY = 0.45;

  RT.pdfFlow(async ({ file, bytes, doc, pdf, count }) => {
    const s = { tool: "hl", color: { hl: PALETTE.hl[0], pen: PALETTE.pen[0], text: PALETTE.text[0] }, width: 3, size: 14 };
    const items = []; // { page, type: "hl" | "pen" | "text", color, ... node }
    const pages = [];
    const width = Math.min(760, Math.max(280, (RT.root.clientWidth || 760) - 40));
    const wrap = el("div", { class: "apages" });
    const summary = el("p", { class: "summary", "aria-live": "polite" });
    const go = el("button", { class: "primary big", type: "button", onclick: run });

    const refresh = () => {
      go.disabled = items.length === 0;
      go.textContent = t("an_btn", { n: items.length });
      summary.textContent = t("an_summary", { n: items.length });
      undo.disabled = items.length === 0;
    };

    function add(item) {
      const p = pages[item.page];
      if (item.type === "hl") {
        const [x0, y0, x1, y1] = item.rect;
        item.node = svgEl("rect", { x: x0, y: y0, width: x1 - x0, height: y1 - y0, fill: item.color, "fill-opacity": HL_OPACITY, class: "a-hl" });
        p.svg.append(item.node);
      } else if (item.type === "pen") {
        item.node = svgEl("polyline", { points: item.points.map((q) => q.join(",")).join(" "), fill: "none", stroke: item.color, "stroke-width": item.width, "stroke-linecap": "round", "stroke-linejoin": "round", class: "a-pen" });
        p.svg.append(item.node);
      } else {
        item.node = el("span", { class: "a-note", text: item.text });
        item.node.style.cssText = `left:${(item.pos[0] / p.vw) * 100}%;top:${(item.pos[1] / p.vh) * 100}%;font-size:${item.size * p.k}px;color:${item.color}`;
        p.layer.append(item.node);
      }
      item.node.addEventListener("pointerdown", (e) => {
        if (s.tool !== "erase") return;
        e.stopPropagation();
        remove(item);
      });
      items.push(item);
      refresh();
    }
    function remove(item) {
      item.node.remove();
      items.splice(items.indexOf(item), 1);
      refresh();
    }

    // ---- pages
    const lazy = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        lazy.unobserve(entry.target);
        entry.target._load().catch(() => {});
      }
    }, { rootMargin: "600px" });

    for (let n = 1; n <= count; n++) {
      const vp = (await pdf.getPage(n)).getViewport({ scale: 1 });
      const p = { vw: vp.width, vh: vp.height, k: width / vp.width, i: n - 1 };
      p.svg = svgEl("svg", { class: "a-svg", viewBox: `0 0 ${p.vw} ${p.vh}` });
      p.layer = el("div", { class: "a-layer" });
      p.box = el("div", { class: "apage", style: `width:${width}px;height:${p.vh * p.k}px` }, p.svg, p.layer);
      p.box._load = async () => {
        const canvas = await RT.renderPage(pdf, n, width * Math.min(2, window.devicePixelRatio || 1));
        canvas.style.cssText = "position:absolute;inset:0;width:100%;height:100%";
        p.box.prepend(canvas);
      };
      pages[p.i] = p;
      wrap.append(el("div", { class: "rwrap" }, el("span", { class: "thumb-label", text: t("page_n", { n }) }), p.box));
      lazy.observe(p.box);
      wirePage(p);
    }

    function wirePage(p) {
      const pt = (e) => {
        const r = p.svg.getBoundingClientRect();
        return [Math.max(0, Math.min(p.vw, ((e.clientX - r.left) / r.width) * p.vw)), Math.max(0, Math.min(p.vh, ((e.clientY - r.top) / r.height) * p.vh))];
      };
      let start = null, ghost = null, points = null;
      p.svg.addEventListener("pointerdown", (e) => {
        if (s.tool !== "hl" && s.tool !== "pen") return;
        p.svg.setPointerCapture(e.pointerId);
        start = pt(e);
        if (s.tool === "hl") ghost = svgEl("rect", { fill: s.color.hl, "fill-opacity": HL_OPACITY });
        else {
          points = [start];
          ghost = svgEl("polyline", { fill: "none", stroke: s.color.pen, "stroke-width": s.width, "stroke-linecap": "round", "stroke-linejoin": "round" });
        }
        p.svg.append(ghost);
      });
      p.svg.addEventListener("pointermove", (e) => {
        if (!start) return;
        const q = pt(e);
        if (s.tool === "hl") {
          ghost.setAttribute("x", Math.min(start[0], q[0])); ghost.setAttribute("y", Math.min(start[1], q[1]));
          ghost.setAttribute("width", Math.abs(q[0] - start[0])); ghost.setAttribute("height", Math.abs(q[1] - start[1]));
        } else if (Math.hypot(q[0] - points[points.length - 1][0], q[1] - points[points.length - 1][1]) > 0.8) {
          points.push(q);
          ghost.setAttribute("points", points.map((x) => x.join(",")).join(" "));
        }
      });
      const end = (e) => {
        if (!start) return;
        const q = pt(e);
        ghost.remove();
        if (s.tool === "hl") {
          const rect = [Math.min(start[0], q[0]), Math.min(start[1], q[1]), Math.max(start[0], q[0]), Math.max(start[1], q[1])];
          if (rect[2] - rect[0] > 3 && rect[3] - rect[1] > 3) add({ page: p.i, type: "hl", color: s.color.hl, rect });
        } else {
          if (points.length === 1) points.push([points[0][0] + 0.1, points[0][1]]); // a tap makes a dot
          add({ page: p.i, type: "pen", color: s.color.pen, width: s.width, points });
        }
        start = ghost = points = null;
      };
      p.svg.addEventListener("click", (e) => { if (s.tool === "text") text(p, pt(e)); }); // after the press, so the browser does not take the focus back
      p.svg.addEventListener("pointerup", end);
      p.svg.addEventListener("pointercancel", () => { ghost && ghost.remove(); start = ghost = points = null; });
    }

    function text(p, [x, y]) {
      const box = el("textarea", { class: "a-edit", rows: "1", placeholder: t("an_text_ph"), "aria-label": t("an_text_ph") });
      box.style.cssText = `left:${(x / p.vw) * 100}%;top:${(y / p.vh) * 100}%;font-size:${s.size * p.k}px;color:${s.color.text}`;
      let done = false;
      const finish = (keep) => {
        if (done) return;
        done = true;
        const value = box.value.replace(/\s+$/, "");
        box.remove();
        if (keep && value.trim()) add({ page: p.i, type: "text", color: s.color.text, size: s.size, pos: [x, y], text: value });
      };
      box.addEventListener("input", () => { box.rows = box.value.split("\n").length; });
      box.addEventListener("blur", () => finish(true));
      box.addEventListener("keydown", (e) => { if (e.key === "Escape") finish(false); });
      p.layer.append(box);
      box.focus();
    }

    // ---- toolbar
    const toolButtons = {};
    const swatches = el("span", { class: "swatches" });
    const widthPick = RT.selectField(t("an_width"), [["1.5", t("an_thin")], ["3", t("an_medium")], ["6", t("an_thick")]], String(s.width), (v) => (s.width = +v));
    const sizePick = RT.selectField(t("an_size"), [["10", t("an_small")], ["14", t("an_medium")], ["20", t("an_large")]], String(s.size), (v) => (s.size = +v));
    function setTool(tool) {
      s.tool = tool;
      for (const [k, b] of Object.entries(toolButtons)) b.setAttribute("aria-pressed", String(k === tool));
      wrap.dataset.tool = tool;
      swatches.replaceChildren(...(PALETTE[tool] || []).map((c) =>
        el("button", { type: "button", class: "swatch", style: `background:${c}`, "aria-label": c, "aria-pressed": String(s.color[tool] === c), onclick: () => { s.color[tool] = c; setTool(tool); } })));
      widthPick.hidden = tool !== "pen";
      sizePick.hidden = tool !== "text";
    }
    for (const [key, label] of [["hl", "an_hl"], ["pen", "an_pen"], ["text", "an_text"], ["erase", "an_erase"], ["view", "an_view"]]) {
      toolButtons[key] = el("button", { type: "button", class: "tool", onclick: () => setTool(key), text: t(label) });
    }
    const undo = el("button", { type: "button", class: "tool", text: t("an_undo"), onclick: () => items.length && remove(items[items.length - 1]) });
    const clear = el("button", { type: "button", class: "tool", text: t("an_clear"), onclick: () => items.slice().forEach(remove) });

    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("p", { class: "hint", text: t("an_hint") }),
      el("div", { class: "toolbar sticky-tools" }, Object.values(toolButtons), swatches, widthPick, sizePick, undo, clear),
      wrap,
      summary,
      el("div", { class: "actions-row sticky" }, go, RT.restartButton())
    );
    setTool("hl");
    refresh();

    async function run() {
      RT.mount(RT.busy());
      try {
        const font = await doc.embedFont(PDFLib.StandardFonts.Helvetica);
        const target = doc.getPages();
        for (const it of items) {
          const page = target[it.page];
          const { vh, rot, map } = RT.pageSpace(page);
          const color = RT.hexColor(it.color);
          if (it.type === "hl") {
            const [x0, y0, x1, y1] = it.rect;
            const p = map(x0, vh - y1);
            page.drawRectangle({ x: p.x, y: p.y, width: x1 - x0, height: y1 - y0, color, opacity: HL_OPACITY, blendMode: PDFLib.BlendMode.Multiply, rotate: PDFLib.degrees(rot) });
          } else if (it.type === "pen") {
            for (let j = 1; j < it.points.length; j++) {
              const a = it.points[j - 1], b = it.points[j];
              page.drawLine({ start: map(a[0], vh - a[1]), end: map(b[0], vh - b[1]), thickness: it.width, color, lineCap: PDFLib.LineCapStyle.Round });
            }
          } else {
            it.text.split("\n").forEach((line, li) => {
              if (!line) return;
              const p = map(it.pos[0], vh - (it.pos[1] + it.size * 0.85 + li * it.size * 1.25));
              page.drawText(line, { x: p.x, y: p.y, size: it.size, font, color, rotate: PDFLib.degrees(rot) });
            });
          }
        }
        const out = await doc.save();
        RT.showResult({ blob: RT.saveBlob(out, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("an_done", { n: items.length }) });
      } catch (e) {
        RT.fail(/winansi|encode|cannot/i.test(e.message) ? new Error(t("an_chars")) : e);
      }
    }
  });
});
