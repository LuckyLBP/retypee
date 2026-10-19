"use strict";

/* Header and footer: text at the left, middle and right of the top and bottom of every page (pdf-lib).
   {n} is the page number (with a start value and zero padding, so Bates numbers work), {total} the
   number of pages, {date} today's date and {file} the file name. */
RT.run(function start() {
  const { t, el } = RT;

  RT.pdfFlow(async ({ file, bytes, doc, pdf, count }) => {
    const o = { hl: "", hc: "", hr: "", fl: "", fc: t("hf_default"), fr: "", size: 10, color: "#444444", margin: 30, start: 1, digits: 1, skipFirst: false };
    const today = new Date().toISOString().slice(0, 10);
    const slots = ["hl", "hc", "hr", "fl", "fc", "fr"];

    const fill = (text, i) => {
      const n = o.start + i - (o.skipFirst ? 1 : 0);
      return text.replace(/\{n\}/g, String(n).padStart(o.digits, "0")).replace(/\{total\}/g, String(count)).replace(/\{date\}/g, today).replace(/\{file\}/g, RT.baseName(file));
    };

    const stage = await RT.previewStage(pdf, 1, 340);
    const marks = Object.fromEntries(slots.map((s) => [s, el("span", { class: `hf-mark hf-${s}` })]));
    stage.el.append(...Object.values(marks));
    function paint() {
      for (const s of slots) {
        const m = marks[s];
        m.textContent = o.skipFirst && count > 1 ? "" : fill(o[s], 0);
        const pad = o.margin * stage.scale;
        m.style.cssText = `font-size:${o.size * stage.scale}px;color:${o.color};${s[0] === "h" ? `top:${pad}px` : `bottom:${pad}px`};` +
          (s[1] === "l" ? `left:${pad}px` : s[1] === "r" ? `right:${pad}px` : "left:50%;transform:translateX(-50%)");
      }
    }

    const inputs = Object.fromEntries(slots.map((s) => {
      const i = el("input", { type: "text", class: "range-input", maxlength: "80", autocomplete: "off", value: o[s] });
      i.addEventListener("input", () => ((o[s] = i.value), refresh()));
      return [s, i];
    }));
    const num = (key, min, max) => {
      const i = el("input", { type: "number", class: "num", min, max, value: o[key] });
      i.addEventListener("input", () => { o[key] = Math.max(min, Math.min(max, Math.round(+i.value || min))); paint(); });
      return i;
    };
    const color = el("input", { type: "color", value: o.color, class: "colorbox" });
    color.addEventListener("input", () => ((o.color = color.value), paint()));
    const skip = el("input", { type: "checkbox", onchange: () => ((o.skipFirst = skip.checked), paint()) });
    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("hf_btn") });
    const grid = (a, b, c, row) => el("div", { class: "hf-row" }, el("span", { class: "hf-label", text: t(row) }), inputs[a], inputs[b], inputs[c]);
    const refresh = () => { go.disabled = slots.every((s) => !o[s].trim()); paint(); };

    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("p", { class: "hint", text: t("hf_hint") }),
      el("div", { class: "split" },
        el("div", { class: "preview" }, stage.el, el("p", { class: "hint", text: t("preview_note") })),
        el("div", { class: "options col" },
          el("div", { class: "hf-cols", "aria-hidden": "true" }, el("span"), el("span", { text: t("hf_left") }), el("span", { text: t("hf_middle") }), el("span", { text: t("hf_right") })),
          grid("hl", "hc", "hr", "hf_header"), grid("fl", "fc", "fr", "hf_footer"),
          RT.field(t("hf_size"), num("size", 6, 24)), RT.field(t("hf_margin"), num("margin", 10, 100)),
          RT.field(t("hf_start"), num("start", 0, 999999)), RT.field(t("hf_digits"), num("digits", 1, 8)), RT.field(t("hf_color"), color),
          count > 1 ? el("label", { class: "check" }, skip, el("span", { text: t("hf_skip") })) : null)),
      RT.actionsRow(go, RT.restartButton())
    );
    refresh();

    async function run() {
      RT.mount(RT.busy());
      try {
        const font = await doc.embedFont(PDFLib.StandardFonts.Helvetica);
        const rgb = RT.hexColor(o.color);
        const pages = doc.getPages();
        pages.forEach((page, i) => {
          if (o.skipFirst && i === 0) return;
          const { vw, vh, rot, map } = RT.pageSpace(page);
          for (const s of slots) {
            const text = fill(o[s], i).trim();
            if (!text) continue;
            const w = font.widthOfTextAtSize(text, o.size);   // throws if a letter is outside the font
            const vx = s[1] === "l" ? o.margin : s[1] === "r" ? vw - o.margin - w : (vw - w) / 2;
            const vy = s[0] === "h" ? vh - o.margin - o.size * 0.8 : o.margin;
            const p = map(vx, vy);
            page.drawText(text, { x: p.x, y: p.y, size: o.size, font, color: rgb, rotate: PDFLib.degrees(rot) });
          }
        });
        const out = await doc.save();
        RT.showResult({ blob: RT.saveBlob(out, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("hf_done", { n: o.skipFirst ? count - 1 : count }) });
      } catch (e) {
        RT.fail(/winansi|encode|cannot/i.test(e.message) ? new Error(t("hf_chars")) : e);
      }
    }
  });
});
