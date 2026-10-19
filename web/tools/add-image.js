"use strict";

/* Add image: a logo, stamp or picture placed on one page or on every page (pdf-lib).
   The picture is dragged into place on a preview of the page. */
RT.run(function start() {
  const { t, el } = RT;
  const looksLikeImage = (f) => f.type.startsWith("image/") || /\.(jpe?g|png|webp|gif|bmp|avif|svg)$/i.test(f.name);

  // Decoded through a canvas, so a phone photo's rotation tag is applied and any format becomes JPEG or PNG.
  async function prepare(file) {
    const url = URL.createObjectURL(file);
    try {
      const img = new Image();
      img.src = url;
      await img.decode();
      const k = Math.min(1, 2400 / Math.max(img.naturalWidth, img.naturalHeight));
      const canvas = el("canvas");
      canvas.width = Math.round(img.naturalWidth * k);
      canvas.height = Math.round(img.naturalHeight * k);
      canvas.getContext("2d").drawImage(img, 0, 0, canvas.width, canvas.height);
      const jpeg = /jpe?g/i.test(file.type) || /\.jpe?g$/i.test(file.name);
      const blob = await new Promise((res) => canvas.toBlob(res, jpeg ? "image/jpeg" : "image/png", 0.92));
      return { bytes: new Uint8Array(await blob.arrayBuffer()), jpeg, url: URL.createObjectURL(blob), aspect: canvas.height / canvas.width };
    } finally {
      URL.revokeObjectURL(url);
    }
  }

  RT.pdfFlow(async ({ file, bytes, doc, pdf, count }) => {
    let pic = null;
    const pos = { fx: 0.62, fy: 0.05, fw: 0.28, opacity: 100, page: 1, all: false };
    let stage = null;
    const img = el("img", { class: "sig-img", alt: "", draggable: "false" });
    const holder = el("div", { class: "preview" });
    const label = el("span", { class: "page-label", "aria-live": "polite" });
    const notes = el("div", { class: "notes" });
    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("ai_btn") });

    const layout = () => {
      if (!stage || !pic) return;
      const w = pos.fw * stage.width;
      img.style.cssText = `width:${w}px;height:${w * pic.aspect}px;left:${pos.fx * stage.width}px;top:${pos.fy * stage.height}px;opacity:${pos.opacity / 100}`;
      label.textContent = `${pos.page} / ${count}`;
    };
    async function show(n) {
      pos.page = n;
      stage = await RT.previewStage(pdf, n, 440);
      stage.el.append(img);
      holder.replaceChildren(stage.el);
      layout();
    }
    img.addEventListener("pointerdown", (e) => {
      e.preventDefault();
      img.setPointerCapture(e.pointerId);
      const r = stage.el.getBoundingClientRect();
      const dx = e.clientX - r.left - pos.fx * stage.width, dy = e.clientY - r.top - pos.fy * stage.height;
      const move = (ev) => {
        const h = pos.fw * stage.width * pic.aspect;
        pos.fx = Math.max(0, Math.min(1 - pos.fw, (ev.clientX - r.left - dx) / stage.width));
        pos.fy = Math.max(0, Math.min(1 - h / stage.height, (ev.clientY - r.top - dy) / stage.height));
        layout();
      };
      const up = () => { img.removeEventListener("pointermove", move); img.removeEventListener("pointerup", up); };
      img.addEventListener("pointermove", move);
      img.addEventListener("pointerup", up);
    });

    async function take(files) {
      const f = files[0];
      if (!looksLikeImage(f)) return notes.replaceChildren(RT.message(t("err_not_image", { name: f.name })));
      try {
        pic = await prepare(f);
      } catch {
        return notes.replaceChildren(RT.message(t("err_not_image", { name: f.name })));
      }
      notes.replaceChildren();
      img.src = pic.url;
      editor();
    }

    function chooser() {
      RT.setDropHandler(take);
      RT.mount(RT.fileCard({ file, count, bytes }), el("p", { class: "hint", text: t("ai_choose") }), RT.dropzone({ kind: "image", onFiles: take }), notes, RT.actionsRow(RT.restartButton()));
    }

    async function editor() {
      const all = el("input", { type: "checkbox", checked: pos.all, onchange: () => (pos.all = all.checked) });
      RT.mount(
        RT.fileCard({ file, count, bytes }),
        el("p", { class: "hint", text: t("ai_hint") }),
        notes,
        el("div", { class: "split" },
          holder,
          el("div", { class: "options col" },
            RT.rangeField(t("ai_size"), { min: 5, max: 90, value: Math.round(pos.fw * 100) }, (v) => ((pos.fw = v / 100), layout()), (v) => `${v} %`),
            RT.rangeField(t("ai_opacity"), { min: 10, max: 100, value: pos.opacity }, (v) => ((pos.opacity = v), layout()), (v) => `${v} %`),
            count > 1 ? el("div", { class: "pager inline" },
              el("button", { type: "button", class: "icon", "aria-label": t("prev_page"), onclick: () => pos.page > 1 && show(pos.page - 1), text: "‹" }), label,
              el("button", { type: "button", class: "icon", "aria-label": t("next_page"), onclick: () => pos.page < count && show(pos.page + 1), text: "›" })) : null,
            count > 1 ? el("label", { class: "check" }, all, el("span", { text: t("ai_all") })) : null,
            el("label", { class: "tool as-label" }, t("ai_other"), el("input", { type: "file", accept: "image/*", class: "file-input", onchange: (e) => e.target.files[0] && take([e.target.files[0]]) })))),
        RT.actionsRow(go, RT.restartButton())
      );
      await show(pos.page);
    }

    async function run() {
      RT.mount(RT.busy());
      try {
        const image = pic.jpeg ? await doc.embedJpg(pic.bytes) : await doc.embedPng(pic.bytes);
        const pages = doc.getPages();
        for (const i of pos.all ? pages.map((_, i) => i) : [pos.page - 1]) {
          const page = pages[i];
          const { vw, vh, rot, map } = RT.pageSpace(page);
          const width = pos.fw * vw, height = width * pic.aspect;
          const p = map(pos.fx * vw, vh - pos.fy * vh - height);
          page.drawImage(image, { x: p.x, y: p.y, width, height, rotate: PDFLib.degrees(rot), opacity: pos.opacity / 100 });
        }
        const out = await doc.save();
        RT.showResult({ blob: RT.saveBlob(out, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("ai_done", { n: pos.all ? count : 1 }) });
      } catch (e) {
        RT.fail(e);
      }
    }

    chooser();
  });
});
