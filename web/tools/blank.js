"use strict";

/* Remove blank pages: every page is drawn small and its ink counted. Pages with (almost) none
   are pre-selected, and the visitor can adjust before the new file is made. */
RT.run(function start() {
  const { t, el } = RT;
  const LEVELS = { strict: 0.000005, normal: 0.0003, loose: 0.0012 }; // share of dark pixels still counted as blank

  RT.pdfFlow(async ({ file, bytes, doc, pdf, count }) => {
    RT.mount(RT.busy(t("blank_scanning", { n: 0, total: count })));
    const ink = [];
    for (let n = 1; n <= count; n++) {
      const canvas = await RT.renderPage(pdf, n, 200);
      const { data } = canvas.getContext("2d").getImageData(0, 0, canvas.width, canvas.height);
      let dark = 0;
      for (let i = 0; i < data.length; i += 4) if (data[i] * 0.299 + data[i + 1] * 0.587 + data[i + 2] * 0.114 < 225) dark++;
      ink.push(dark / (canvas.width * canvas.height));
      if (n % 3 === 0) {
        RT.mount(RT.busy(t("blank_scanning", { n, total: count })));
        await new Promise((r) => setTimeout(r)); // let the progress paint
      }
    }

    let level = "normal";
    const blanks = () => ink.map((v, i) => (v <= LEVELS[level] ? i + 1 : 0)).filter(Boolean);
    const summary = el("p", { class: "summary", "aria-live": "polite" });
    const go = el("button", { class: "primary big", type: "button", onclick: run });
    let ranges;
    const grid = RT.pageGrid({
      pdf, count, mode: "select",
      onChange: (s) => {
        const n = s.selected.size;
        go.disabled = n === 0 || n === count;
        go.textContent = t("blank_btn", { n });
        summary.textContent = n === count ? t("delete_all") : t("blank_summary", { n, total: count });
        ranges.sync([...s.selected]);
      },
    });
    ranges = RT.rangeInput({ grid, count, label: t("delete_label"), placeholder: "2, 4-6" });
    const found = el("p", { class: "hint" });
    const choose = (v) => {
      level = v;
      grid.select(blanks());
      found.textContent = blanks().length ? t("blank_found", { n: blanks().length }) : t("blank_none");
    };
    RT.mount(
      RT.fileCard({ file, count, bytes }),
      RT.selectField(t("blank_level"), [["strict", t("blank_strict")], ["normal", t("blank_normal")], ["loose", t("blank_loose")]], level, choose),
      found,
      ranges.el,
      grid.el,
      summary,
      el("div", { class: "actions-row sticky" }, go, RT.restartButton())
    );
    choose(level);

    async function run() {
      const gone = new Set(grid.state.selected);
      RT.mount(RT.busy());
      try {
        const keep = Array.from({ length: count }, (_, i) => i).filter((i) => !gone.has(i + 1));
        const out = await RT.newDoc();
        for (const page of await out.copyPages(doc, keep)) out.addPage(page);
        const saved = await out.save();
        RT.showResult({ blob: RT.saveBlob(saved, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("blank_done", { n: gone.size, left: keep.length }) });
      } catch (e) {
        RT.fail(e);
      }
    }
  });
});
