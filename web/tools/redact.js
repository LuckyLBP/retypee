"use strict";

/* Redact PDF: draw boxes or search for text; the text and image pixels under the boxes are
   removed from the file by the PyMuPDF engine (true redaction, not a black rectangle on top). */
RT.run(function start() {
  const { t, el } = RT;
  RT.root.addEventListener("pointerover", () => RTEngine.start().catch(() => {}), { once: true });

  async function open(selected) {
    const file = selected[0];
    if (!RT.isPdf(file)) return RT.mount(RT.message(t("err_not_pdf", { name: file.name })), RT.dropzone({ onFiles: open }));
    RTEngine.onProgress = (key) => RT.mount(RT.busy(t(key)));
    RT.mount(RT.busy(t("loading_engine")));
    try {
      const bytes = await file.arrayBuffer();
      const preview = new Uint8Array(bytes.slice(0)); // the engine takes the original buffer
      const doc = await RTEngine.json("/api/docs", { method: "POST", file: { name: file.name, bytes } });
      workspace(file, doc, preview);
    } catch (e) {
      RT.mount(RT.message(e.message), RT.dropzone({ onFiles: open }));
    }
  }

  function workspace(file, doc, preview) {
    const boxes = []; // { page, rect: [x0, y0, x1, y1] in page points, kind: "drawn" | "found", node }
    const queries = [];
    const summary = el("p", { class: "summary", "aria-live": "polite" });
    const status = el("div", { class: "notes" });
    const go = el("button", { class: "primary big", type: "button", onclick: run });
    const search = el("input", { type: "text", class: "range-input", placeholder: t("redact_search_ph"), autocomplete: "off", spellcheck: "false" });
    const pagesEl = el("div", { class: "rpages" });
    const width = Math.min(760, Math.max(280, (RT.root.clientWidth || 760) - 40));
    const layers = [];
    let scales = [];

    function refresh() {
      go.disabled = boxes.length === 0;
      go.textContent = t("redact_btn", { n: boxes.length });
      summary.textContent = t("redact_summary", { n: boxes.length });
    }

    function addBox(page, rect, kind) {
      const k = scales[page];
      const node = el("div", { class: `rbox ${kind}` }, el("button", { type: "button", class: "rbox-x", title: t("redact_remove"), "aria-label": t("redact_remove"), text: "✕" }));
      const item = { page, rect, kind, node };
      node.style.cssText = `left:${rect[0] * k}px;top:${rect[1] * k}px;width:${(rect[2] - rect[0]) * k}px;height:${(rect[3] - rect[1]) * k}px`;
      node.querySelector("button").addEventListener("pointerdown", (e) => e.stopPropagation());
      node.querySelector("button").addEventListener("click", () => {
        boxes.splice(boxes.indexOf(item), 1);
        node.remove();
        refresh();
      });
      layers[page].append(node);
      boxes.push(item);
      refresh();
    }

    // Created before the loop that observes the pages.
    const lazy = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        lazy.unobserve(entry.target);
        entry.target._load().catch(() => {});
      }
    }, { rootMargin: "600px" });

    doc.pages.forEach((p, i) => {
      const k = width / p.w;
      scales[i] = k;
      const img = el("img", { alt: t("page_n", { n: i + 1 }), draggable: "false" });
      const layer = el("div", { class: "rlayer" });
      layers[i] = layer;
      const page = el("div", { class: "rpage", style: `width:${p.w * k}px;height:${p.h * k}px` }, img, layer);
      pagesEl.append(el("div", { class: "rwrap" }, el("span", { class: "thumb-label", text: t("page_n", { n: i + 1 }) }), page));
      page._load = async () => {
        const zoom = Math.min(3, k * (window.devicePixelRatio || 1));
        const r = await RTEngine.bytes(`/api/docs/${doc.id}/pages/${i}/image?zoom=${zoom.toFixed(2)}`);
        img.src = URL.createObjectURL(new Blob([r.bytes], { type: r.mime }));
      };
      // draw a box by dragging
      let start = null, ghost = null;
      layer.addEventListener("pointerdown", (e) => {
        if (e.target !== layer) return;
        const b = layer.getBoundingClientRect();
        start = [e.clientX - b.left, e.clientY - b.top];
        ghost = el("div", { class: "rbox drawn ghost" });
        layer.append(ghost);
        layer.setPointerCapture(e.pointerId);
      });
      layer.addEventListener("pointermove", (e) => {
        if (!start) return;
        const b = layer.getBoundingClientRect();
        const x = Math.min(Math.max(e.clientX - b.left, 0), b.width), y = Math.min(Math.max(e.clientY - b.top, 0), b.height);
        ghost.style.cssText = `left:${Math.min(start[0], x)}px;top:${Math.min(start[1], y)}px;width:${Math.abs(x - start[0])}px;height:${Math.abs(y - start[1])}px`;
      });
      const end = (e) => {
        if (!start) return;
        const b = layer.getBoundingClientRect();
        const x = Math.min(Math.max(e.clientX - b.left, 0), b.width), y = Math.min(Math.max(e.clientY - b.top, 0), b.height);
        const [x0, x1, y0, y1] = [Math.min(start[0], x), Math.max(start[0], x), Math.min(start[1], y), Math.max(start[1], y)];
        ghost.remove();
        start = ghost = null;
        if (x1 - x0 > 4 && y1 - y0 > 4) addBox(i, [x0 / k, y0 / k, x1 / k, y1 / k], "drawn");
      };
      layer.addEventListener("pointerup", end);
      layer.addEventListener("pointercancel", () => { ghost && ghost.remove(); start = ghost = null; });
      page.dataset.i = i;
      lazy.observe(page);
    });

    async function find() {
      const text = search.value.trim();
      if (!text) return;
      status.replaceChildren(RT.busy());
      try {
        const r = await RTEngine.json(`/api/docs/${doc.id}/search-rects`, { method: "POST", json: { text } });
        for (const b of boxes.filter((x) => x.kind === "found" && x.query === text)) { b.node.remove(); boxes.splice(boxes.indexOf(b), 1); }
        r.rects.forEach((x) => { addBox(x.page, x.rect, "found"); boxes[boxes.length - 1].query = text; });
        if (r.rects.length && !queries.includes(text)) queries.push(text);
        status.replaceChildren(RT.message(r.rects.length ? t("redact_found", { n: r.rects.length }) : t("redact_none_found"), r.rects.length ? "info" : "error"));
      } catch (e) {
        status.replaceChildren(RT.message(e.message));
      }
    }
    search.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); find(); } });

    RT.mount(
      RT.fileCard({ file, count: doc.pages.length, bytes: preview }),
      el("p", { class: "hint", text: t("redact_hint") }),
      el("div", { class: "toolbar" },
        el("label", { class: "field inline" }, el("span", { text: t("redact_search") }), search),
        el("button", { class: "tool", type: "button", onclick: find, text: t("redact_find") }),
        el("button", { class: "tool", type: "button", onclick: () => { boxes.splice(0).forEach((b) => b.node.remove()); queries.length = 0; status.replaceChildren(); refresh(); }, text: t("redact_clear") })),
      status,
      pagesEl,
      summary,
      el("div", { class: "actions-row sticky" }, go, el("button", { class: "tool", type: "button", onclick: () => { RTEngine.json(`/api/docs/${doc.id}`, { method: "DELETE" }).catch(() => {}); RT.reset(); }, text: t("start_over") }))
    );
    refresh();

    async function run() {
      RT.mount(RT.busy(t("working")));
      try {
        await RTEngine.json(`/api/docs/${doc.id}/redact`, { method: "POST", json: { rects: boxes.map((b) => ({ page: b.page, rect: b.rect })) } });
        const checks = [];
        for (const q of queries) {
          const r = await RTEngine.json(`/api/docs/${doc.id}/search-rects`, { method: "POST", json: { text: q } });
          checks.push(el("li", { text: t("redact_check_item", { text: q, n: r.rects.length }) }));
        }
        const out = await RTEngine.bytes(`/api/docs/${doc.id}/download`);
        RTEngine.json(`/api/docs/${doc.id}`, { method: "DELETE" }).catch(() => {});
        RT.showResult({
          blob: RT.saveBlob(out.bytes, "application/pdf"),
          filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`,
          note: t("redact_done"),
          extra: checks.length ? el("div", { class: "checks-box" }, el("strong", { text: t("redact_check") }), el("ul", {}, checks)) : null,
        });
      } catch (e) {
        RT.fail(e);
      }
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
