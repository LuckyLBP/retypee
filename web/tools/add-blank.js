"use strict";

/* Add blank pages: pick the pages that a blank page should follow (pdf-lib). */
RT.run(function start() {
  const { t, el } = RT;

  RT.pdfFlow(async ({ file, bytes, doc, pdf, count }) => {
    let first = false;
    const summary = el("p", { class: "summary", "aria-live": "polite" });
    const go = el("button", { class: "primary big", type: "button", onclick: run });
    const grid = RT.pageGrid({ pdf, count, mode: "select", onChange: () => refresh() });
    const refresh = () => {
      const n = grid.state.selected.size + (first ? 1 : 0);
      go.disabled = n === 0;
      go.textContent = t("ab_btn", { n });
      summary.textContent = n ? t("ab_summary", { n, total: count + n }) : t("ab_none");
    };
    const quick = (label, pick) => el("button", { type: "button", class: "tool", text: label, onclick: () => grid.select(pick) });
    const range = (f) => Array.from({ length: count }, (_, i) => i + 1).filter(f);
    const firstBox = el("input", { type: "checkbox", onchange: () => ((first = firstBox.checked), refresh()) });
    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("p", { class: "hint", text: t("ab_hint") }),
      el("div", { class: "toolbar" }, quick(t("ab_every"), range(() => true)), quick(t("ab_odd"), range((n) => n % 2 === 1)), quick(t("ab_even"), range((n) => n % 2 === 0)), quick(t("ab_clear"), []),
        el("label", { class: "check" }, firstBox, el("span", { text: t("ab_first") }))),
      grid.el,
      summary,
      el("div", { class: "actions-row sticky" }, go, RT.restartButton())
    );
    grid.select([]);

    async function run() {
      RT.mount(RT.busy());
      try {
        const out = await RT.newDoc();
        const copies = await out.copyPages(doc, Array.from({ length: count }, (_, i) => i));
        const blank = (i) => { const sp = RT.pageSpace(doc.getPage(i)); out.addPage([sp.vw, sp.vh]); }; // as big as the page it follows
        if (first) blank(0);
        copies.forEach((page, i) => {
          out.addPage(page);
          if (grid.state.selected.has(i + 1)) blank(i);
        });
        const n = grid.state.selected.size + (first ? 1 : 0);
        const saved = await out.save();
        RT.showResult({ blob: RT.saveBlob(saved, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("ab_done", { n }) });
      } catch (e) {
        RT.fail(e);
      }
    }
  });
});
