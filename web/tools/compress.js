"use strict";

/* Compress PDF: smaller images, subset fonts, tidier structure (PyMuPDF engine). */
RT.run(function start() {
  const { t, el } = RT;
  RT.root.addEventListener("pointerover", () => RTEngine.start().catch(() => {}), { once: true });

  async function open(selected) {
    const file = selected[0];
    if (!RT.isPdf(file)) return RT.mount(RT.message(t("err_not_pdf", { name: file.name })), RT.dropzone({ onFiles: open }));
    RT.mount(RT.busy());
    try {
      options(file, await RT.readBytes(file));
    } catch (e) {
      RT.mount(RT.message(e.message), RT.dropzone({ onFiles: open }));
    }
  }

  function options(file, bytes) {
    let level = "medium";
    const choices = ["low", "medium", "high"].map((k) =>
      el("label", { class: "choice" },
        el("input", { type: "radio", name: "level", value: k, checked: k === level, onchange: () => (level = k) }),
        el("span", { class: "choice-body stack" }, el("strong", { text: t("lvl_" + k) }), el("span", { class: "hint", text: t("lvl_" + k + "_d") }))));
    RT.mount(
      RT.fileCard({ file, bytes }),
      el("div", { class: "choices", role: "radiogroup" }, choices),
      RT.actionsRow(el("button", { class: "primary big", type: "button", onclick: run, text: t("shrink_btn") }), RT.restartButton())
    );

    async function run() {
      RTEngine.onProgress = (key) => RT.mount(RT.busy(t(key)));
      RT.mount(RT.busy(t("loading_engine")));
      try {
        const r = await RTEngine.call("/api/compress", { method: "POST", json: { level }, file: { name: file.name, bytes: bytes.slice().buffer } });
        const out = new Uint8Array(r.bytes);
        RT.mount(RT.busy(t("working")));
        if (out.length >= file.size * 0.97) {
          return RT.mount(RT.message(t("no_gain"), "info"), RT.actionsRow(RT.restartButton()));
        }
        const saved = Math.round((1 - out.length / file.size) * 100);
        RT.showResult({
          blob: RT.saveBlob(out, "application/pdf"),
          filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`,
          note: t("compress_done", { before: RT.formatSize(file.size), after: RT.formatSize(out.length), pct: saved }),
        });
      } catch (e) {
        RT.fail(e);
      }
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
