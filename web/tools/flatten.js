"use strict";

/* Flatten PDF: comments, highlights and form fields become ordinary page content (PyMuPDF engine). */
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
    const o = { annots: info.annots > 0, widgets: info.widgets > 0 };
    if (!info.annots && !info.widgets) return RT.mount(RT.fileCard({ file, bytes, count: info.pages }), RT.message(t("flat_nothing"), "info"), RT.actionsRow(RT.restartButton()));
    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("flat_btn") });
    const box = (key, count, label) => {
      const input = el("input", { type: "checkbox", checked: count > 0, disabled: count === 0, onchange: () => { o[key] = input.checked; go.disabled = !o.annots && !o.widgets; } });
      return el("label", { class: "check" }, input, el("span", { text: t(label, { n: count }) }));
    };
    RT.mount(
      RT.fileCard({ file, bytes, count: info.pages }),
      el("p", { class: "hint", text: t("flat_hint") }),
      el("div", { class: "options col" }, box("annots", info.annots, "flat_annots"), box("widgets", info.widgets, "flat_widgets")),
      RT.actionsRow(go, RT.restartButton())
    );

    async function run() {
      RT.mount(RT.busy(t("working")));
      try {
        const r = await RTEngine.call("/api/flatten", { method: "POST", json: { annots: o.annots, widgets: o.widgets }, file: { name: file.name, bytes: bytes.slice().buffer } });
        RT.showResult({ blob: RT.saveBlob(new Uint8Array(r.bytes), "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("flat_done") });
      } catch (e) {
        RT.fail(e);
      }
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
