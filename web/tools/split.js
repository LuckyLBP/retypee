"use strict";

/* Split PDF: one file in, several files (or a ZIP) out. */
RT.run(function start() {
  const { t, el } = RT;

  async function open(selected) {
    const file = selected[0];
    if (!RT.isPdf(file)) return RT.mount(RT.message(t("err_not_pdf", { name: file.name })), RT.dropzone({ onFiles: open }));
    RT.mount(RT.busy());
    try {
      const bytes = await RT.readBytes(file);
      const doc = await RT.loadDoc(bytes);
      options(file, bytes, doc.getPageCount());
    } catch (e) {
      RT.mount(RT.message(e.message), RT.dropzone({ onFiles: open }));
    }
  }

  function options(file, bytes, count) {
    const mode = { value: "each" };
    const rangesInput = el("input", { type: "text", class: "range-input", placeholder: "1-3, 4-6, 7-", autocomplete: "off", spellcheck: "false" });
    const everyInput = el("input", { type: "number", min: "1", max: String(count), value: "2", class: "num" });
    const summary = el("p", { class: "summary", "aria-live": "polite" });
    const error = el("div", { class: "notes" });
    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("split_btn") });

    function plan() {
      if (mode.value === "each") return Array.from({ length: count }, (_, i) => [i + 1, i + 1]);
      if (mode.value === "every") {
        const n = Math.max(1, Math.min(count, Math.floor(+everyInput.value) || 0));
        if (!n) return null;
        const out = [];
        for (let i = 1; i <= count; i += n) out.push([i, Math.min(count, i + n - 1)]);
        return out;
      }
      const r = RT.parseRanges(rangesInput.value, count);
      return r && r.length ? r : null;
    }

    function update() {
      rangesInput.disabled = mode.value !== "ranges";
      everyInput.disabled = mode.value !== "every";
      const p = plan();
      go.disabled = !p;
      summary.textContent = p ? (p.length === 1 ? t("split_result_1") : t("split_result", { n: p.length })) : mode.value === "ranges" && rangesInput.value.trim() ? t("err_ranges", { n: count }) : "";
    }

    const radio = (value, label, extra) =>
      el(
        "label",
        { class: "choice" },
        el("input", { type: "radio", name: "mode", value, checked: value === mode.value, onchange: () => ((mode.value = value), update()) }),
        el("span", { class: "choice-body" }, el("span", { text: label }), extra || null)
      );
    rangesInput.addEventListener("input", update);
    everyInput.addEventListener("input", update);

    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("div", { class: "choices", role: "radiogroup" }, radio("each", t("split_each")), radio("ranges", t("split_ranges"), rangesInput), radio("every", t("split_every"), everyInput)),
      summary,
      error,
      el("div", { class: "actions-row" }, go, el("button", { class: "tool", type: "button", onclick: () => RT.reset(), text: t("start_over") }))
    );
    update();

    async function run() {
      const ranges = plan();
      if (!ranges) return;
      RT.mount(RT.busy());
      try {
        const src = await RT.loadDoc(bytes);
        const base = RT.baseName(file);
        const outputs = [];
        for (const [from, to] of ranges) {
          const out = await RT.newDoc();
          const idx = Array.from({ length: to - from + 1 }, (_, i) => from - 1 + i);
          for (const page of await out.copyPages(src, idx)) out.addPage(page);
          outputs.push({ name: `${base}-${from === to ? from : from + "-" + to}.pdf`, bytes: await out.save() });
        }
        if (outputs.length === 1) {
          return RT.showResult({ blob: RT.saveBlob(outputs[0].bytes, "application/pdf"), filename: outputs[0].name });
        }
        needZip();
        const zip = fflate.zipSync(Object.fromEntries(outputs.map((o) => [o.name, o.bytes])), { level: 0 });
        RT.showResult({ blob: RT.saveBlob(zip, "application/zip"), filename: `${base}-${t("zip_suffix")}.zip`, note: t("zip_note", { n: outputs.length }) });
      } catch (e) {
        RT.fail(e);
      }
    }
  }

  function needZip() {
    if (typeof fflate === "undefined") throw new Error("Library missing: fflate");
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
