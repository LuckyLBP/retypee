"use strict";

/* Extract pages: pick the pages you want, get them as a new PDF. */
RT.run(function start() {
  const { t, el } = RT;

  async function open(selected) {
    const file = selected[0];
    if (!RT.isPdf(file)) return RT.mount(RT.message(t("err_not_pdf", { name: file.name })), RT.dropzone({ onFiles: open }));
    RT.mount(RT.busy());
    try {
      const bytes = await RT.readBytes(file);
      const doc = await RT.loadDoc(bytes);
      const count = doc.getPageCount();
      const pdf = await RT.openForRender(bytes);
      editor(file, doc, count, pdf, bytes);
    } catch (e) {
      RT.mount(RT.message(e.message), RT.dropzone({ onFiles: open }));
    }
  }

  function editor(file, doc, count, pdf, bytes) {
    const summary = el("p", { class: "summary", "aria-live": "polite" });
    const go = el("button", { class: "primary big", type: "button", onclick: run });
    let ranges;
    const grid = RT.pageGrid({
      pdf, count, mode: "select",
      onChange: (s) => {
        const n = s.selected.size;
        go.disabled = n === 0;
        go.textContent = t("extract_btn", { n });
        summary.textContent = t("extract_summary", { n, total: count });
        ranges.sync([...s.selected]);
      },
    });
    ranges = RT.rangeInput({ grid, count, label: t("extract_label"), placeholder: "1, 3-5" });
    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("p", { class: "hint", text: t("extract_hint") }),
      el("div", { class: "toolbar" }, el("button", { class: "tool", type: "button", onclick: () => grid.selectAll(), text: t("select_all") }), el("button", { class: "tool", type: "button", onclick: () => grid.select([]), text: t("select_none") })),
      ranges.el,
      grid.el,
      summary,
      el("div", { class: "actions-row sticky" }, go, el("button", { class: "tool", type: "button", onclick: () => RT.reset(), text: t("start_over") }))
    );
    grid.select([]);

    async function run() {
      const keep = [...grid.state.selected].sort((a, b) => a - b);
      RT.mount(RT.busy());
      try {
        const out = await RT.newDoc();
        for (const page of await out.copyPages(doc, keep.map((n) => n - 1))) out.addPage(page);
        const bytes = await out.save();
        RT.showResult({ blob: RT.saveBlob(bytes, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("extract_done", { n: keep.length }) });
      } catch (e) {
        RT.fail(e);
      }
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
