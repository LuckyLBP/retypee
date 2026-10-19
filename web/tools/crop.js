"use strict";

/* Crop PDF: drag the edges on the first page; the same margins apply to every page (pdf-lib CropBox). */
RT.run(function start() {
  const { t, el } = RT;

  // Margins as displayed (top, right, bottom, left) -> margins of the page's own, unrotated space.
  function pageMargins(rot, m) {
    if (rot === 90) return { left: m.top, top: m.right, right: m.bottom, bottom: m.left };
    if (rot === 180) return { left: m.right, top: m.bottom, right: m.left, bottom: m.top };
    if (rot === 270) return { left: m.bottom, top: m.left, right: m.top, bottom: m.right };
    return { ...m };
  }

  RT.pdfFlow(async ({ file, bytes, doc, pdf, count }) => {
    const stage = await RT.previewStage(pdf, 1, 420);
    const m = { top: 0, right: 0, bottom: 0, left: 0 };   // points
    const MIN = 40;                                         // keep at least this much page
    const shades = ["top", "right", "bottom", "left"].map((edge) => el("div", { class: `crop-shade ${edge}` }));
    const handles = ["top", "right", "bottom", "left"].map((edge) => el("span", { class: `crop-handle ${edge}`, "data-edge": edge }));
    const frame = el("div", { class: "crop-frame" }, handles);
    stage.el.append(...shades, frame);
    const inputs = {};

    const mm = (pt) => Math.round(((pt * 25.4) / 72) * 10) / 10;
    function paint() {
      const s = stage.scale;
      frame.style.cssText = `left:${m.left * s}px;top:${m.top * s}px;right:${m.right * s}px;bottom:${m.bottom * s}px`;
      shades[0].style.cssText = `left:0;right:0;top:0;height:${m.top * s}px`;
      shades[2].style.cssText = `left:0;right:0;bottom:0;height:${m.bottom * s}px`;
      shades[3].style.cssText = `left:0;top:${m.top * s}px;bottom:${m.bottom * s}px;width:${m.left * s}px`;
      shades[1].style.cssText = `right:0;top:${m.top * s}px;bottom:${m.bottom * s}px;width:${m.right * s}px`;
      for (const e of Object.keys(inputs)) if (document.activeElement !== inputs[e]) inputs[e].value = mm(m[e]);
      go.disabled = !(m.top || m.right || m.bottom || m.left);
    }
    const limit = (edge, value) => {
      const horizontal = edge === "left" || edge === "right";
      const other = horizontal ? (edge === "left" ? m.right : m.left) : edge === "top" ? m.bottom : m.top;
      const room = (horizontal ? stage.vw : stage.vh) - other - MIN;
      return Math.max(0, Math.min(value, room));
    };

    for (const h of handles) {
      h.addEventListener("pointerdown", (e) => {
        e.preventDefault();
        h.setPointerCapture(e.pointerId);
        const edge = h.dataset.edge;
        const move = (ev) => {
          const r = stage.el.getBoundingClientRect();
          const s = stage.scale;
          const v = edge === "top" ? (ev.clientY - r.top) / s : edge === "bottom" ? (r.bottom - ev.clientY) / s : edge === "left" ? (ev.clientX - r.left) / s : (r.right - ev.clientX) / s;
          m[edge] = limit(edge, v);
          paint();
        };
        const up = () => {
          h.removeEventListener("pointermove", move);
          h.removeEventListener("pointerup", up);
        };
        h.addEventListener("pointermove", move);
        h.addEventListener("pointerup", up);
      });
    }

    const field = (edge) => {
      const input = el("input", { type: "number", class: "num", min: "0", step: "1", value: "0" });
      input.addEventListener("input", () => {
        m[edge] = limit(edge, Math.max(0, (+input.value * 72) / 25.4));
        paint();
      });
      inputs[edge] = input;
      return RT.field(t("crop_" + edge), input, el("span", { class: "unit-mm", text: "mm" }));
    };

    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("crop_btn") });
    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("p", { class: "hint", text: t("crop_hint") }),
      el("div", { class: "split" },
        el("div", { class: "preview" }, stage.el),
        el("div", { class: "options col" }, field("top"), field("right"), field("bottom"), field("left"), el("p", { class: "hint", text: t("crop_all", { n: count }) }))),
      RT.actionsRow(go, RT.restartButton())
    );
    paint();

    async function run() {
      RT.mount(RT.busy());
      try {
        let done = 0;
        for (const page of doc.getPages()) {
          const base = page.getCropBox();
          const rot = ((page.getRotation().angle % 360) + 360) % 360;
          const o = pageMargins(rot, m);
          const w = base.width - o.left - o.right;
          const h = base.height - o.top - o.bottom;
          if (w < 20 || h < 20) continue;
          page.setCropBox(base.x + o.left, base.y + o.bottom, w, h);
          done++;
        }
        const out = await doc.save();
        RT.showResult({ blob: RT.saveBlob(out, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("crop_done", { n: done }) });
      } catch (e) {
        RT.fail(e);
      }
    }
  });
});
