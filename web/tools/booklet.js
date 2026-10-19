"use strict";

/* Booklet: pages are put two to a landscape sheet in the order that, printed double-sided and folded,
   reads as a booklet (pdf-lib). The page count is rounded up to a multiple of four with blank pages. */
RT.run(function start() {
  const { t, el } = RT;

  RT.pdfFlow(async ({ file, bytes, doc, count }) => {
    const o = { size: "a4", gap: 0 };
    const total = Math.ceil(count / 4) * 4;
    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("bk_btn") });
    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("p", { class: "hint", text: t("bk_hint") }),
      el("div", { class: "options" }, RT.selectField(t("nup_size"), [["a4", "A4"], ["letter", "Letter"], ["a3", "A3"]], o.size, (v) => (o.size = v))),
      el("p", { class: "summary", text: t("bk_info", { n: count, sheets: total / 4, blank: total - count }) }),
      RT.actionsRow(go, RT.restartButton())
    );

    async function run() {
      RT.mount(RT.busy());
      try {
        const out = await RT.newDoc();
        const pages = await RT.embedAll(out, doc);
        const [a, b] = RT.SHEETS[o.size];
        const W = b, H = a; // landscape sheets, one page on each half
        const m = 14;
        const side = (left, right) => {
          const sheet = out.addPage([W, H]);
          [[left, 0], [right, W / 2]].forEach(([idx, x0]) => {
            const src = pages[idx]; // undefined = a blank page
            if (!src) return;
            const k = Math.min((W / 2 - 2 * m) / src.sp.vw, (H - 2 * m) / src.sp.vh);
            RT.drawVisible(sheet, src, x0 + (W / 2 - src.sp.vw * k) / 2, (H - src.sp.vh * k) / 2, k);
          });
        };
        for (let s = 0; s < total / 4; s++) {
          side(total - 1 - 2 * s, 2 * s);       // outside of the sheet
          side(2 * s + 1, total - 2 - 2 * s);   // inside of the sheet
        }
        const saved = await out.save();
        RT.showResult({ blob: RT.saveBlob(saved, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("bk_done", { sheets: total / 4, sides: total / 2 }) });
      } catch (e) {
        RT.fail(e);
      }
    }
  });
});
