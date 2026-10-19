"use strict";

/* Extract images: every picture in the PDF, in its original quality, as a ZIP (PyMuPDF engine). */
RT.run(function start() {
  const { t, el } = RT;
  RT.root.addEventListener("pointerover", () => RTEngine.start().catch(() => {}), { once: true });

  async function ask(path, file, bytes, json) {
    return RTEngine.call(path, { method: "POST", json, file: { name: file.name, bytes: bytes.slice().buffer } });
  }

  async function open(selected) {
    const file = selected[0];
    if (!RT.isPdf(file)) return RT.mount(RT.message(t("err_not_pdf", { name: file.name })), RT.dropzone({ onFiles: open }));
    RT.mount(RT.busy(t("loading_engine")));
    RTEngine.onProgress = (key) => RT.mount(RT.busy(t(key)));
    try {
      const bytes = await RT.readBytes(file);
      const first = (await ask("/api/images", file, bytes, { min: 0 })).data;
      options(file, bytes, first);
    } catch (e) {
      RT.mount(RT.message(e.status === 403 ? t("err_encrypted") : e.message), RT.dropzone({ onFiles: open }));
    }
  }

  function options(file, bytes, all) {
    let smallest = 100;
    const found = el("p", { class: "summary", "aria-live": "polite" });
    const go = el("button", { class: "primary big", type: "button", onclick: run });
    const sizes = el("div", { class: "options" });

    async function refresh() {
      const r = smallest === 0 ? all : (await ask("/api/images", file, bytes, { min: smallest })).data;
      found.textContent = r.count ? t("img_found", { n: r.count, pages: r.pages }) : t("img_none");
      go.disabled = r.count === 0;
      go.textContent = t("img_get", { n: r.count });
    }
    sizes.append(RT.selectField(t("img_smallest"), [["0", t("img_all")], ["100", t("img_skip_small")], ["300", t("img_only_large")]], "100", (v) => ((smallest = +v), refresh())));
    RT.mount(RT.fileCard({ file, bytes }), el("p", { class: "hint", text: t("img_hint") }), sizes, found, RT.actionsRow(go, RT.restartButton()));
    refresh();

    async function run() {
      RT.mount(RT.busy(t("working")));
      try {
        const r = await ask("/api/extract-images", file, bytes, { min: smallest });
        RT.showResult({ blob: RT.saveBlob(new Uint8Array(r.bytes), "application/zip"), filename: `${RT.baseName(file)}-${t("out_suffix")}.zip`, note: t("img_done") });
      } catch (e) {
        RT.fail(e);
      }
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
