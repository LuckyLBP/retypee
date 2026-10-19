"use strict";

/* Watermark: a line of text across every page, with size, colour, angle and opacity (pdf-lib). */
RT.run(function start() {
  const { t, el } = RT;

  RT.pdfFlow(async ({ file, bytes, doc, pdf, count }) => {
    const o = { text: t("wm_default"), size: 64, opacity: 25, color: "#8a8a8a", angle: 45 };
    const stage = await RT.previewStage(pdf, 1, 340);
    const mark = el("span", { class: "wm-mark" });
    stage.el.append(mark);

    function paint() {
      mark.textContent = o.text || " ";
      mark.style.cssText = `font-size:${o.size * stage.scale}px;opacity:${o.opacity / 100};color:${o.color};transform:translate(-50%,-50%) rotate(${-o.angle}deg)`;
    }

    const text = el("input", { type: "text", class: "range-input", value: o.text, maxlength: "60", autocomplete: "off" });
    text.addEventListener("input", () => ((o.text = text.value), paint()));
    const color = el("input", { type: "color", value: o.color, class: "colorbox" });
    color.addEventListener("input", () => ((o.color = color.value), paint()));
    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("wm_btn") });

    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("div", { class: "split" },
        el("div", { class: "preview" }, stage.el, el("p", { class: "hint", text: t("preview_note") })),
        el("div", { class: "options col" },
          RT.field(t("wm_text"), text),
          RT.rangeField(t("wm_size"), { min: 20, max: 140, value: o.size }, (v) => ((o.size = v), paint()), (v) => `${v} pt`),
          RT.rangeField(t("wm_opacity"), { min: 5, max: 80, value: o.opacity }, (v) => ((o.opacity = v), paint()), (v) => `${v} %`),
          RT.selectField(t("wm_angle"), [["45", t("wm_diag")], ["0", t("wm_flat")]], String(o.angle), (v) => ((o.angle = +v), paint())),
          RT.field(t("wm_color"), color))),
      RT.actionsRow(go, RT.restartButton())
    );
    paint();

    async function run() {
      if (!o.text.trim()) return;
      RT.mount(RT.busy());
      try {
        const font = await doc.embedFont(PDFLib.StandardFonts.HelveticaBold);
        const width = font.widthOfTextAtSize(o.text, o.size);   // throws if a letter is outside the font
        const height = o.size * 0.72;
        const a = (o.angle * Math.PI) / 180;
        const color = RT.hexColor(o.color);
        for (const page of doc.getPages()) {
          const { vw, vh, rot, map } = RT.pageSpace(page);
          // start point so that the text's middle lands in the middle of the page, whatever the angle
          const vx = vw / 2 - (width / 2) * Math.cos(a) + (height / 2) * Math.sin(a);
          const vy = vh / 2 - (width / 2) * Math.sin(a) - (height / 2) * Math.cos(a);
          const p = map(vx, vy);
          page.drawText(o.text, { x: p.x, y: p.y, size: o.size, font, color, opacity: o.opacity / 100, rotate: PDFLib.degrees(o.angle + rot) });
        }
        const out = await doc.save();
        RT.showResult({ blob: RT.saveBlob(out, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("wm_done", { n: count }) });
      } catch (e) {
        RT.fail(/winansi|encode|cannot/i.test(e.message) ? new Error(t("wm_chars")) : e);
      }
    }
  });
});
