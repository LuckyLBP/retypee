"use strict";

/* Delete pages: pick the pages you do not want, get the rest as a new PDF. */
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
        go.disabled = n === 0 || n === count;
        go.textContent = t("delete_btn", { n });
        summary.textContent = n === count ? t("delete_all") : t("delete_summary", { n, total: count });
        ranges.sync([...s.selected]);
      },
    });
    ranges = RT.rangeInput({ grid, count, label: t("delete_label"), placeholder: "2, 4-6" });
    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("p", { class: "hint", text: t("delete_hint") }),
      ranges.el,
      grid.el,
      summary,
      el("div", { class: "actions-row sticky" }, go, el("button", { class: "tool", type: "button", onclick: () => RT.reset(), text: t("start_over") }))
    );
    grid.select([]);

    async function run() {
      const doomed = [...grid.state.selected].sort((a, b) => b - a);
      RT.mount(RT.busy());
      try {
        // Build the new file from the pages that stay, so removed pages leave no trace in it.
        const gone = new Set(doomed);
        const keep = Array.from({ length: count }, (_, i) => i).filter((i) => !gone.has(i + 1));
        const out = await RT.newDoc();
        for (const page of await out.copyPages(doc, keep)) out.addPage(page);
        const bytes = await out.save();
        RT.showResult({ blob: RT.saveBlob(bytes, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("delete_done", { n: doomed.length, left: count - doomed.length }) });
      } catch (e) {
        RT.fail(e);
      }
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
