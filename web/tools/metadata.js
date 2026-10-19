"use strict";

/* Remove metadata: show what a PDF reveals about its author, then strip it for good.
   Reading uses pdf-lib; the thorough removal (info, XMP, file ID, thumbnails, ...) uses the
   PyMuPDF engine that also powers the editor. */
RT.run(function start() {
  const { t, el } = RT;

  // Begin fetching the engine as soon as someone points at the page, so it is ready on time.
  RT.root.addEventListener("pointerover", () => RTEngine.start().catch(() => {}), { once: true });

  const fmtDate = (d) => (d ? d.toISOString().replace("T", " ").slice(0, 16) + " UTC" : "");

  function read(doc) {
    const xmp = doc.catalog.has(PDFLib.PDFName.of("Metadata"));
    return [
      [t("f_title"), doc.getTitle() || ""],
      [t("f_author"), doc.getAuthor() || ""],
      [t("f_subject"), doc.getSubject() || ""],
      [t("f_keywords"), doc.getKeywords() || ""],
      [t("f_creator"), doc.getCreator() || ""],
      [t("f_producer"), doc.getProducer() || ""],
      [t("f_created"), fmtDate(doc.getCreationDate())],
      [t("f_modified"), fmtDate(doc.getModificationDate())],
      [t("f_xmp"), xmp ? t("yes") : ""],
    ];
  }

  function table(rows, caption) {
    return el("table", { class: "meta-table" },
      el("caption", { text: caption }),
      el("tbody", {}, rows.map(([k, v]) => el("tr", {}, el("th", { scope: "row", text: k }), el("td", { class: v ? "" : "none", text: v || "—" })))));
  }

  async function open(selected) {
    const file = selected[0];
    if (!RT.isPdf(file)) return RT.mount(RT.message(t("err_not_pdf", { name: file.name })), RT.dropzone({ onFiles: open }));
    RT.mount(RT.busy());
    try {
      const bytes = await RT.readBytes(file);
      let before = null;
      try {
        before = read(await RT.loadDoc(bytes));
      } catch (e) {
        if (e.message === t("err_encrypted")) throw e; // cannot be cleaned here either
      }
      review(file, bytes, before);
    } catch (e) {
      RT.mount(RT.message(e.message), RT.dropzone({ onFiles: open }));
    }
  }

  function review(file, bytes, before) {
    const hasAny = before ? before.some(([, v]) => v) : true;
    RT.mount(
      RT.fileCard({ file, bytes }),
      before ? table(before, t("meta_before")) : RT.message(t("meta_unreadable"), "info"),
      before && !hasAny ? el("p", { class: "hint", text: t("meta_none") }) : null,
      el("div", { class: "actions-row" },
        el("button", { class: "primary big", type: "button", onclick: run, text: t("meta_btn") }),
        el("button", { class: "tool", type: "button", onclick: () => RT.reset(), text: t("start_over") }))
    );

    async function run() {
      RTEngine.onProgress = (key) => RT.mount(RT.busy(t(key)));
      RT.mount(RT.busy(t("loading_engine")));
      try {
        const opened = await RTEngine.json("/api/docs", { method: "POST", file: { name: file.name, bytes: bytes.slice().buffer } });
        const out = await RTEngine.bytes(`/api/docs/${opened.id}/download`);
        RTEngine.json(`/api/docs/${opened.id}`, { method: "DELETE" }).catch(() => {});
        let after = null;
        try {
          after = read(await RT.loadDoc(out.bytes));
        } catch {
          /* the file is still fine; we just cannot show the table */
        }
        RT.showResult({
          blob: RT.saveBlob(out.bytes, "application/pdf"),
          filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`,
          note: t("meta_done"),
          extra: after ? table(after, t("meta_after")) : null,
        });
      } catch (e) {
        RT.fail(e);
      }
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
