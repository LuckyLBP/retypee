"use strict";

/* Remove comments: delete notes, highlights, drawings and stamps, all of them or chosen kinds (PyMuPDF engine).
   Links and form fields are left alone. */
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
      const info = (await RTEngine.call("/api/pdf-info", { method: "POST", file: { name: file.name, bytes: bytes.slice().buffer } })).data;
      if (info.needsPass) throw new Error(t("err_encrypted"));
      choose(file, bytes, info);
    } catch (e) {
      RT.mount(RT.message(e.message), RT.dropzone({ onFiles: open }));
    }
  }

  function choose(file, bytes, info) {
    const kinds = Object.entries(info.annotTypes || {});
    if (!kinds.length) return RT.mount(RT.fileCard({ file, bytes, count: info.pages }), RT.message(t("ra_none"), "info"), RT.actionsRow(RT.restartButton()));
    const on = new Set(kinds.map(([k]) => k));
    const go = el("button", { class: "primary big", type: "button", onclick: run });
    const refresh = () => {
      const n = kinds.filter(([k]) => on.has(k)).reduce((sum, [, c]) => sum + c, 0);
      go.disabled = n === 0;
      go.textContent = t("ra_btn", { n });
    };
    const boxes = kinds.map(([k, c]) => {
      const input = el("input", { type: "checkbox", checked: true, onchange: () => { input.checked ? on.add(k) : on.delete(k); refresh(); } });
      return el("label", { class: "check" }, input, el("span", { text: `${t("annot_" + k) === "annot_" + k ? k : t("annot_" + k)} (${c})` }));
    });
    RT.mount(RT.fileCard({ file, bytes, count: info.pages }), el("p", { class: "hint", text: t("ra_hint") }), el("div", { class: "options col" }, boxes), RT.actionsRow(go, RT.restartButton()));
    refresh();

    async function run() {
      RT.mount(RT.busy(t("working")));
      try {
        const all = on.size === kinds.length;
        const r = await RTEngine.call("/api/strip-annots", { method: "POST", json: all ? {} : { types: [...on] }, file: { name: file.name, bytes: bytes.slice().buffer } });
        RT.showResult({ blob: RT.saveBlob(new Uint8Array(r.bytes), "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("ra_done") });
      } catch (e) {
        RT.fail(e);
      }
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
