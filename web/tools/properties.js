"use strict";

/* PDF properties: title, author, subject and keywords (pdf-lib). A separate XMP block, which
   many programs prefer over these fields, is removed so that every program shows the same values. */
RT.run(function start() {
  const { t, el } = RT;

  RT.pdfFlow(async ({ file, bytes, doc, count }) => {
    const known = { title: doc.getTitle() || "", author: doc.getAuthor() || "", subject: doc.getSubject() || "", keywords: doc.getKeywords() || "" };
    const o = { ...known, displayTitle: false };
    try { o.displayTitle = !!doc.catalog.getViewerPreferences()?.getDisplayDocTitle(); } catch { /* not set */ }

    const field = (key, max) => {
      const input = el("input", { type: "text", class: "range-input wide", maxlength: String(max), autocomplete: "off", value: o[key] });
      input.addEventListener("input", () => (o[key] = input.value));
      return RT.field(t("prop_" + key), input);
    };
    const display = el("input", { type: "checkbox", checked: o.displayTitle, onchange: () => (o.displayTitle = display.checked) });
    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("prop_btn") });
    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("p", { class: "hint", text: t("prop_hint") }),
      el("div", { class: "options col props" }, field("title", 200), field("author", 200), field("subject", 300), field("keywords", 300),
        el("label", { class: "check" }, display, el("span", { text: t("prop_display") }))),
      RT.actionsRow(go, RT.restartButton())
    );

    async function run() {
      RT.mount(RT.busy());
      try {
        const info = doc.getInfoDict();
        const set = (key, value) => {
          const name = PDFLib.PDFName.of(key);
          if (value.trim()) info.set(name, PDFLib.PDFHexString.fromText(value.trim()));
          else info.delete(name);
        };
        set("Title", o.title); set("Author", o.author); set("Subject", o.subject); set("Keywords", o.keywords);
        doc.catalog.getOrCreateViewerPreferences().setDisplayDocTitle(o.displayTitle);
        doc.catalog.delete(PDFLib.PDFName.of("Metadata"));
        const out = await doc.save({ updateMetadata: false });
        RT.showResult({ blob: RT.saveBlob(out, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("prop_done") });
      } catch (e) {
        RT.fail(e);
      }
    }
  });
});
