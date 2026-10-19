"use strict";

/* Resize pages: every page is fitted onto a sheet of the chosen size (pdf-lib). */
RT.run(function start() {
  const { t, el } = RT;

  RT.pdfFlow(async ({ file, bytes, doc, count }) => {
    const o = { size: "a4", turn: "keep", margin: 0 };

    // which sizes the file has now
    const have = new Map();
    for (const page of doc.getPages()) {
      const sp = RT.pageSpace(page);
      const name = RT.sizeName(sp.vw, sp.vh);
      have.set(name, (have.get(name) || 0) + 1);
    }
    const now = [...have].map(([name, n]) => `${n} × ${name}`).join(", ");

    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("rs_btn") });
    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("p", { class: "hint", text: t("rs_now", { sizes: now }) }),
      el("div", { class: "options" },
        RT.selectField(t("rs_size"), [["a4", "A4"], ["a3", "A3"], ["a5", "A5"], ["letter", "Letter"], ["legal", "Legal"]], o.size, (v) => (o.size = v)),
        RT.selectField(t("rs_turn"), [["keep", t("rs_keep")], ["portrait", t("nup_portrait")], ["landscape", t("nup_landscape")]], o.turn, (v) => (o.turn = v)),
        RT.selectField(t("img_margin"), [["0", t("margin_none")], ["18", t("margin_small")], ["36", t("margin_big")]], "0", (v) => (o.margin = +v))),
      RT.actionsRow(go, RT.restartButton())
    );

    async function run() {
      RT.mount(RT.busy());
      try {
        const out = await RT.newDoc();
        const pages = await RT.embedAll(out, doc);
        const [a, b] = RT.SHEETS[o.size];
        for (const src of pages) {
          const landscape = o.turn === "keep" ? src.sp.vw > src.sp.vh : o.turn === "landscape";
          const [W, H] = landscape ? [b, a] : [a, b];
          const sheet = out.addPage([W, H]);
          const k = Math.min((W - 2 * o.margin) / src.sp.vw, (H - 2 * o.margin) / src.sp.vh);
          RT.drawVisible(sheet, src, (W - src.sp.vw * k) / 2, (H - src.sp.vh * k) / 2, k);
        }
        const saved = await out.save();
        RT.showResult({ blob: RT.saveBlob(saved, "application/pdf"), filename: `${RT.baseName(file)}-${o.size.toUpperCase()}.pdf`, note: t("rs_done", { n: count, size: o.size === "letter" ? "Letter" : o.size === "legal" ? "Legal" : o.size.toUpperCase() }) });
      } catch (e) {
        RT.fail(e);
      }
    }
  });
});
