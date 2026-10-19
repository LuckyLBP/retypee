"use strict";

/* Page numbers: choose where and how, see it on the first page, then stamp every page (pdf-lib). */
RT.run(function start() {
  const { t, el } = RT;

  RT.pdfFlow(async ({ file, bytes, doc, pdf, count }) => {
    const MARGIN = 28;
    const o = { pos: "bc", fmt: "n", start: 1, from: 1, size: 11 };
    const stage = await RT.previewStage(pdf, 1, 340);
    const mark = el("span", { class: "pn-mark" });
    stage.el.append(mark);

    const lastNumber = () => o.start + Math.max(0, count - o.from);
    const label = (n) => t("fmt_" + o.fmt, { n, total: lastNumber() });

    function paint() {
      mark.textContent = label(o.start);
      mark.style.fontSize = `${o.size * stage.scale}px`;
      const m = `${MARGIN * stage.scale}px`;
      Object.assign(mark.style, { left: "", right: "", top: "", bottom: "", transform: "" });
      mark.style[o.pos[0] === "t" ? "top" : "bottom"] = m;
      if (o.pos[1] === "l") mark.style.left = m;
      else if (o.pos[1] === "r") mark.style.right = m;
      else Object.assign(mark.style, { left: "50%", transform: "translateX(-50%)" });
    }

    const num = (key, min, max, label_) => {
      const input = el("input", { type: "number", class: "num", min, max, value: o[key] });
      input.addEventListener("input", () => {
        const v = Math.floor(+input.value);
        if (v >= min && v <= max) o[key] = v;
        paint();
      });
      return RT.field(label_, input);
    };
    const positions = ["bl", "bc", "br", "tl", "tc", "tr"].map((p) => [p, t("pos_" + p)]);
    const formats = ["n", "page", "of", "pageof"].map((f) => [f, t("fmt_" + f, { n: 1, total: count })]);

    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("pn_btn") });
    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("div", { class: "split" },
        el("div", { class: "preview" }, stage.el, el("p", { class: "hint", text: t("preview_note") })),
        el("div", { class: "options col" },
          RT.selectField(t("pn_position"), positions, o.pos, (v) => ((o.pos = v), paint())),
          RT.selectField(t("pn_format"), formats, o.fmt, (v) => ((o.fmt = v), paint())),
          num("start", 0, 9999, t("pn_start")),
          num("from", 1, count, t("pn_from")),
          RT.rangeField(t("pn_size"), { min: 8, max: 24, value: o.size }, (v) => ((o.size = v), paint()), (v) => `${v} pt`))),
      RT.actionsRow(go, RT.restartButton())
    );
    paint();

    async function run() {
      RT.mount(RT.busy());
      try {
        const font = await doc.embedFont(PDFLib.StandardFonts.Helvetica);
        doc.getPages().forEach((page, i) => {
          if (i < o.from - 1) return;
          const text = label(o.start + (i - (o.from - 1)));
          const { vw, vh, rot, map } = RT.pageSpace(page);
          const width = font.widthOfTextAtSize(text, o.size);
          const vx = o.pos[1] === "l" ? MARGIN : o.pos[1] === "r" ? vw - MARGIN - width : (vw - width) / 2;
          const vy = o.pos[0] === "b" ? MARGIN : vh - MARGIN - o.size * 0.72;
          const p = map(vx, vy);
          page.drawText(text, { x: p.x, y: p.y, size: o.size, font, color: PDFLib.rgb(0.1, 0.1, 0.1), rotate: PDFLib.degrees(rot) });
        });
        const out = await doc.save();
        RT.showResult({ blob: RT.saveBlob(out, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("pn_done", { n: count - o.from + 1 }) });
      } catch (e) {
        RT.fail(e);
      }
    }
  });
});
