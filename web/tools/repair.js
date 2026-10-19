"use strict";

/* Repair PDF: the engine reads the file the lenient way, rebuilds a broken structure and saves it clean. */
RT.run(function start() {
  const { t, el } = RT;
  RT.root.addEventListener("pointerover", () => RTEngine.start().catch(() => {}), { once: true });

  async function open(selected) {
    const file = selected[0];
    if (!RT.isPdf(file)) return RT.mount(RT.message(t("err_not_pdf", { name: file.name })), RT.dropzone({ onFiles: open }));
    RT.mount(RT.busy(t("loading_engine")));
    RTEngine.onProgress = (key) => RT.mount(RT.busy(t(key)));
    try {
      const bytes = await RT.readBytes(file);
      let info;
      try {
        info = (await RTEngine.call("/api/pdf-info", { method: "POST", file: { name: file.name, bytes: bytes.slice().buffer } })).data;
      } catch (e) {
        if (e.status === 400) throw new Error(t("repair_fail"));
        throw e;
      }
      if (info.needsPass) throw new Error(t("err_encrypted"));
      const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("repair_btn") });
      RT.mount(
        RT.fileCard({ file, bytes, count: info.pages }),
        RT.message(info.repaired ? t("repair_was_broken", { n: info.pages }) : t("repair_looks_fine", { n: info.pages }), info.repaired ? "info" : "info"),
        RT.actionsRow(go, RT.restartButton())
      );

      async function run() {
        RT.mount(RT.busy(t("working")));
        try {
          const r = await RTEngine.call("/api/repair", { method: "POST", file: { name: file.name, bytes: bytes.slice().buffer } });
          const out = new Uint8Array(r.bytes);
          RT.showResult({ blob: RT.saveBlob(out, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("repair_done", { n: info.pages, size: RT.formatSize(out.length) }) });
        } catch (e) {
          RT.fail(e);
        }
      }
    } catch (e) {
      RT.mount(RT.message(e.message), RT.dropzone({ onFiles: open }));
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
