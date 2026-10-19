"use strict";

/* Unlock PDF: take the password and the limits off a file you can open (PyMuPDF engine). */
RT.run(function start() {
  const { t, el } = RT;
  RT.root.addEventListener("pointerover", () => RTEngine.start().catch(() => {}), { once: true });

  async function open(selected) {
    const file = selected[0];
    if (!RT.isPdf(file)) return RT.mount(RT.message(t("err_not_pdf", { name: file.name })), RT.dropzone({ onFiles: open }));
    RTEngine.onProgress = (key) => RT.mount(RT.busy(t(key)));
    RT.mount(RT.busy(t("loading_engine")));
    try {
      const bytes = await RT.readBytes(file);
      const info = await RTEngine.json("/api/pdf-info", { method: "POST", file: { name: file.name, bytes: bytes.slice().buffer } });
      form(file, bytes, info);
    } catch (e) {
      RT.mount(RT.message(e.message), RT.dropzone({ onFiles: open }));
    }
  }

  function form(file, bytes, info, error) {
    const pw = el("input", { type: "password", class: "range-input", autocomplete: "off", maxlength: "64" });
    const notes = el("div", { class: "notes" });
    const nothing = !info.needsPass && !info.limited;
    const go = el("button", { class: "primary big", type: "button", onclick: run, disabled: nothing, text: t("unlock_btn") });
    RT.mount(
      RT.fileCard({ file, count: info.pages || 0, bytes: info.needsPass ? null : bytes }),
      info.needsPass ? el("div", { class: "options col" }, el("p", { class: "hint", text: t("unlock_needs") }), RT.field(t("pw"), pw)) : null,
      !info.needsPass && info.limited ? RT.message(t("unlock_limited"), "info") : null,
      nothing ? RT.message(t("unlock_nothing"), "info") : null,
      notes,
      RT.actionsRow(go, RT.restartButton())
    );
    if (error) notes.append(RT.message(error));
    if (info.needsPass) pw.focus();

    async function run() {
      if (info.needsPass && !pw.value) return notes.replaceChildren(RT.message(t("pw_empty")));
      RT.mount(RT.busy(t("working")));
      try {
        const r = await RTEngine.call("/api/unlock", { method: "POST", json: { password: info.needsPass ? pw.value : undefined }, file: { name: file.name, bytes: bytes.slice().buffer } });
        RT.showResult({ blob: RT.saveBlob(new Uint8Array(r.bytes), "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("unlock_done") });
      } catch (e) {
        if (e.status === 403) return form(file, bytes, info, e.message);
        RT.fail(e);
      }
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
