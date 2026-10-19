"use strict";

/* Merge PDF: several files in, one file out (pdf-lib, in the browser). */
RT.run(function start() {
  const { t, el } = RT;
  const files = []; // { file, bytes, count }
  const notes = el("div", { class: "notes" });
  const go = el("button", { class: "primary big", type: "button", onclick: merge });
  let list;

  async function add(selected) {
    notes.replaceChildren(RT.busy());
    const problems = [];
    for (const file of selected) {
      if (!RT.isPdf(file)) {
        problems.push(t("err_not_pdf", { name: file.name }));
        continue;
      }
      try {
        const bytes = await RT.readBytes(file);
        const doc = await RT.loadDoc(bytes);
        const item = { file, bytes, count: doc.getPageCount(), thumb: null };
        files.push(item);
        RT.fileThumb(bytes, 64).then((c) => {
          item.thumb = c;
          if (list) list.repaint();
        });
      } catch (e) {
        problems.push(`${file.name}: ${e.message}`);
      }
    }
    notes.replaceChildren(...problems.map((p) => RT.message(p)));
    if (!files.length) return RT.mount(RT.dropzone({ multiple: true, onFiles: add }), notes); // keep the reasons visible
    show();
  }

  function refresh() {
    go.disabled = files.length < 2;
    go.textContent = t("merge_btn", { n: files.length });
    if (list) notes.querySelectorAll(".hint").forEach((n) => n.remove());
    if (files.length < 2) notes.append(el("p", { class: "hint", text: t("need_two") }));
  }

  function show() {
    if (!files.length) return RT.run(start);
    list = RT.reorderList({
      items: files,
      render: (f) =>
        el("span", { class: "file-main with-thumb" },
          el("span", { class: "fc-thumb small", "aria-hidden": "true" }, f.thumb || el("span", { class: "fc-ext", text: "PDF" })),
          el("span", { class: "fc-text" }, el("strong", { class: "file-name", title: f.file.name, text: f.file.name }), el("span", { class: "file-sub", text: `${RT.pagesLabel(f.count)} · ${RT.formatSize(f.file.size)}` }))),
      onChange: () => {
        if (!files.length) return RT.run(start);
        refresh();
      },
    });
    RT.mount(RT.dropzone({ multiple: true, compact: true, onFiles: add }), list.el, notes, el("div", { class: "actions-row" }, go));
    refresh();
  }

  async function merge() {
    RT.mount(RT.busy());
    try {
      const out = await RT.newDoc();
      for (const f of files) {
        const src = await RT.loadDoc(f.bytes);
        for (const page of await out.copyPages(src, src.getPageIndices())) out.addPage(page);
      }
      const bytes = await out.save();
      RT.showResult({ blob: RT.saveBlob(bytes, "application/pdf"), filename: t("out_name") + ".pdf", note: t("merged_note", { files: files.length, pages: files.reduce((n, f) => n + f.count, 0) }) });
    } catch (e) {
      RT.fail(e);
    }
  }

  RT.setDropHandler(add);
  RT.mount(RT.dropzone({ multiple: true, onFiles: add }));
});
