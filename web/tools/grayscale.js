"use strict";

/* Grayscale: every colour becomes a grey level, text stays text (PyMuPDF engine). */
RT.run(function start() {
  const { t, el } = RT;
  RT.root.addEventListener("pointerover", () => RTEngine.start().catch(() => {}), { once: true });

  async function open(selected) {
    const file = selected[0];
    if (!RT.isPdf(file)) return RT.mount(RT.message(t("err_not_pdf", { name: file.name })), RT.dropzone({ onFiles: open }));
    RT.mount(RT.busy());
    try {
      const bytes = await RT.readBytes(file);
      const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("gs_btn") });
      RT.mount(RT.fileCard({ file, bytes }), el("p", { class: "hint", text: t("gs_hint") }), RT.actionsRow(go, RT.restartButton()));

      async function run() {
        RTEngine.onProgress = (key) => RT.mount(RT.busy(t(key)));
        RT.mount(RT.busy(t("loading_engine")));
        try {
          const r = await RTEngine.call("/api/grayscale", { method: "POST", file: { name: file.name, bytes: bytes.slice().buffer } });
          const out = new Uint8Array(r.bytes);
          RT.showResult({ blob: RT.saveBlob(out, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("gs_done", { before: RT.formatSize(file.size), after: RT.formatSize(out.length) }) });
        } catch (e) {
          RT.mount(RT.message(e.status === 403 ? t("err_encrypted") : e.message), RT.actionsRow(RT.restartButton()));
        }
      }
    } catch (e) {
      RT.mount(RT.message(e.message), RT.dropzone({ onFiles: open }));
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
