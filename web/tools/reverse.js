"use strict";

/* Reverse page order, or put front and back scans together (pdf-lib). */
RT.run(function start() {
  const { t, el } = RT;

  RT.pdfFlow(async ({ file, bytes, doc, count }) => {
    let mode = "reverse";
    const orders = {
      reverse: () => Array.from({ length: count }, (_, i) => count - 1 - i),
      // fronts 1..m, then the backs scanned in reverse: front 1, last page, front 2, last but one ...
      collate: () => Array.from({ length: count }, (_, k) => (k % 2 === 0 ? k / 2 : count - 1 - (k - 1) / 2)),
    };
    const preview = el("p", { class: "summary", "aria-live": "polite" });
    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("rv_btn") });
    const refresh = () => {
      const bad = mode === "collate" && count % 2 !== 0;
      go.disabled = bad || count < 2;
      const o = orders[mode]().map((i) => i + 1);
      preview.textContent = bad ? t("rv_odd") : t("rv_order", { list: o.slice(0, 14).join(", ") + (o.length > 14 ? ", …" : "") });
    };
    const choice = (key) => el("label", { class: "choice" },
      el("input", { type: "radio", name: "mode", value: key, checked: key === mode, onchange: () => ((mode = key), refresh()) }),
      el("span", { class: "choice-body stack" }, el("strong", { text: t("rv_" + key) }), el("span", { class: "hint", text: t("rv_" + key + "_d") })));
    RT.mount(RT.fileCard({ file, count, bytes }), el("div", { class: "choices", role: "radiogroup" }, choice("reverse"), choice("collate")), preview, RT.actionsRow(go, RT.restartButton()));
    refresh();

    async function run() {
      RT.mount(RT.busy());
      try {
        const out = await RT.newDoc();
        for (const page of await out.copyPages(doc, orders[mode]())) out.addPage(page);
        const saved = await out.save();
        RT.showResult({ blob: RT.saveBlob(saved, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("rv_done", { n: count }) });
      } catch (e) {
        RT.fail(e);
      }
    }
  });
});
