"use strict";

/* Protect PDF: AES-256 password to open, with optional limits on printing, copying and editing. */
RT.run(function start() {
  const { t, el } = RT;
  RT.root.addEventListener("pointerover", () => RTEngine.start().catch(() => {}), { once: true });

  async function open(selected) {
    const file = selected[0];
    if (!RT.isPdf(file)) return RT.mount(RT.message(t("err_not_pdf", { name: file.name })), RT.dropzone({ onFiles: open }));
    RT.mount(RT.busy());
    try {
      form(file, await RT.readBytes(file));
    } catch (e) {
      RT.mount(RT.message(e.message), RT.dropzone({ onFiles: open }));
    }
  }

  function form(file, bytes) {
    const pw = el("input", { type: "password", class: "range-input", autocomplete: "new-password", maxlength: "64" });
    const again = el("input", { type: "password", class: "range-input", autocomplete: "new-password", maxlength: "64" });
    const show = el("input", { type: "checkbox", onchange: () => (pw.type = again.type = show.checked ? "text" : "password") });
    const box = (label, on) => { const c = el("input", { type: "checkbox", checked: on }); return [c, el("label", { class: "check" }, c, el("span", { text: label }))]; };
    const [print, printL] = box(t("allow_print"), true), [copy, copyL] = box(t("allow_copy"), true), [edit, editL] = box(t("allow_edit"), false);
    const notes = el("div", { class: "notes" });
    RT.mount(
      RT.fileCard({ file, bytes }),
      el("div", { class: "options col" }, RT.field(t("pw"), pw), RT.field(t("pw_again"), again), el("label", { class: "check" }, show, el("span", { text: t("pw_show") }))),
      el("div", { class: "options col" }, el("p", { class: "hint", text: t("allow_title") }), printL, copyL, editL),
      el("p", { class: "msg info", text: t("pw_warning") }),
      notes,
      RT.actionsRow(el("button", { class: "primary big", type: "button", onclick: run, text: t("protect_btn") }), RT.restartButton())
    );

    async function run() {
      if (!pw.value) return notes.replaceChildren(RT.message(t("pw_empty")));
      if (pw.value !== again.value) return notes.replaceChildren(RT.message(t("pw_mismatch")));
      RTEngine.onProgress = (key) => RT.mount(RT.busy(t(key)));
      RT.mount(RT.busy(t("loading_engine")));
      try {
        const r = await RTEngine.call("/api/protect", { method: "POST", json: { password: pw.value, print: print.checked, copy: copy.checked, edit: edit.checked }, file: { name: file.name, bytes: bytes.slice().buffer } });
        RT.showResult({ blob: RT.saveBlob(new Uint8Array(r.bytes), "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("protect_done") });
      } catch (e) {
        RT.fail(e);
      }
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
