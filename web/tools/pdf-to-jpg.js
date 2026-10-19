"use strict";

/* PDF to JPG: every page (or the pages you choose) becomes an image. */
RT.run(function start() {
  const { t, el } = RT;

  async function open(selected) {
    const file = selected[0];
    if (!RT.isPdf(file)) return RT.mount(RT.message(t("err_not_pdf", { name: file.name })), RT.dropzone({ onFiles: open }));
    RT.mount(RT.busy());
    try {
      const bytes = await RT.readBytes(file);
      const pdf = await RT.openForRender(bytes);
      options(file, pdf, bytes);
    } catch (e) {
      RT.mount(RT.message(e.message), RT.dropzone({ onFiles: open }));
    }
  }

  function options(file, pdf, bytes) {
    const count = pdf.numPages;
    const opt = { format: RT.S.variant === "png" ? "png" : "jpg", dpi: "150", which: "all" }; // the PNG landing page starts on PNG
    const rangeInput = el("input", { type: "text", class: "range-input", placeholder: "1-3, 5", autocomplete: "off", spellcheck: "false", disabled: true });
    const summary = el("p", { class: "summary", "aria-live": "polite" });
    const go = el("button", { class: "primary big", type: "button", onclick: run });

    const pick = (name, label, choices) => {
      const input = el("select", { onchange: () => (opt[name] = input.value) }, choices.map(([v, text]) => el("option", { value: v, selected: v === opt[name], text })));
      return el("label", { class: "field inline" }, el("span", { text: label }), input);
    };
    const pages = () => (opt.which === "all" ? Array.from({ length: count }, (_, i) => i + 1) : (() => { const r = RT.parseRanges(rangeInput.value, count); return r && r.length ? RT.expand(r).sort((a, b) => a - b) : null; })());
    const update = () => {
      rangeInput.disabled = opt.which !== "range";
      const p = pages();
      go.disabled = !p;
      go.textContent = t("jpg_btn", { n: p ? p.length : 0 });
      summary.textContent = p ? "" : t("err_ranges", { n: count });
    };
    rangeInput.addEventListener("input", update);
    const which = el("select", { onchange: () => ((opt.which = which.value), update()) }, [["all", t("jpg_all")], ["range", t("jpg_range")]].map(([v, text]) => el("option", { value: v, text })));

    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("div", { class: "options" },
        pick("format", t("jpg_format"), [["jpg", "JPG"], ["png", "PNG"]]),
        pick("dpi", t("jpg_quality"), [["96", t("q_low")], ["150", t("q_normal")], ["200", t("q_high")]]),
        el("label", { class: "field inline" }, el("span", { text: t("jpg_pages") }), which, rangeInput)),
      summary,
      el("div", { class: "actions-row" }, go, el("button", { class: "tool", type: "button", onclick: () => RT.reset(), text: t("start_over") }))
    );
    update();

    async function run() {
      const list = pages();
      if (!list) return;
      const png = opt.format === "png";
      const ext = png ? "png" : "jpg";
      const base = RT.baseName(file);
      const files = {};
      try {
        for (let i = 0; i < list.length; i++) {
          RT.mount(RT.busy(t("jpg_progress", { n: i + 1, total: list.length })));
          await new Promise((r) => setTimeout(r)); // let the progress text paint
          const page = await pdf.getPage(list[i]);
          const base1 = page.getViewport({ scale: 1 });
          let scale = +opt.dpi / 72;
          scale = Math.min(scale, 6000 / Math.max(base1.width, base1.height), Math.sqrt(36e6 / (base1.width * base1.height)));
          const viewport = page.getViewport({ scale });
          const canvas = el("canvas");
          canvas.width = Math.ceil(viewport.width);
          canvas.height = Math.ceil(viewport.height);
          await page.render({ canvasContext: canvas.getContext("2d"), viewport, background: "white" }).promise;
          const blob = await new Promise((res) => canvas.toBlob(res, png ? "image/png" : "image/jpeg", 0.92));
          files[`${base}-${t("page_word")}-${list[i]}.${ext}`] = new Uint8Array(await blob.arrayBuffer());
          canvas.width = canvas.height = 0;
        }
        const names = Object.keys(files);
        if (names.length === 1) return RT.showResult({ blob: RT.saveBlob(files[names[0]], png ? "image/png" : "image/jpeg"), filename: names[0] });
        if (typeof fflate === "undefined") throw new Error("Library missing: fflate");
        const zip = fflate.zipSync(files, { level: 0 });
        RT.showResult({ blob: RT.saveBlob(zip, "application/zip"), filename: `${base}-${ext}.zip`, note: t("jpg_done", { n: names.length }) });
      } catch (e) {
        RT.fail(e);
      }
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
