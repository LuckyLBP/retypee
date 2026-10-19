"use strict";

/* Rotate PDF: turn single pages or the whole document. */
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
    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("rotate_btn") });
    const grid = RT.pageGrid({
      pdf, count, mode: "rotate",
      onChange: (s) => {
        const turned = s.rotation.slice(1).filter((r) => r !== 0).length;
        go.disabled = turned === 0;
        summary.textContent = turned ? t("rotate_summary", { n: turned }) : t("rotate_none");
      },
    });
    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("p", { class: "hint", text: t("rotate_hint") }),
      el("div", { class: "toolbar" },
        el("button", { class: "tool", type: "button", onclick: () => grid.turnAll(-90), text: "↺ " + t("rotate_all_left") }),
        el("button", { class: "tool", type: "button", onclick: () => grid.turnAll(90), text: "↻ " + t("rotate_all_right") })),
      grid.el,
      summary,
      el("div", { class: "actions-row sticky" }, go, el("button", { class: "tool", type: "button", onclick: () => RT.reset(), text: t("start_over") }))
    );
    summary.textContent = t("rotate_none");
    go.disabled = true;

    async function run() {
      RT.mount(RT.busy());
      try {
        const pages = doc.getPages();
        pages.forEach((page, i) => {
          const turn = grid.state.rotation[i + 1];
          if (turn) page.setRotation(PDFLib.degrees((page.getRotation().angle + turn + 360) % 360));
        });
        const bytes = await doc.save();
        RT.showResult({ blob: RT.saveBlob(bytes, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf` });
      } catch (e) {
        RT.fail(e);
      }
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
