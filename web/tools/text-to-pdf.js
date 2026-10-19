"use strict";

/* Text to PDF: type or paste text, or open a .txt file, and get a paginated PDF (pdf-lib).
   Plain text only; letters outside the standard PDF fonts are replaced with "?" and counted. */
RT.run(function start() {
  const { t, el } = RT;
  const o = { font: "Helvetica", size: 11, paper: "a4", margin: 56, numbers: true };
  let name = null;

  const area = el("textarea", { class: "ttp-area", rows: "14", placeholder: t("ttp_ph"), spellcheck: "false", "aria-label": t("ttp_label") });
  const go = el("button", { class: "primary big", type: "button", onclick: build, text: t("ttp_btn") });
  const notes = el("div", { class: "notes" });
  const refresh = () => (go.disabled = !area.value.trim());
  area.addEventListener("input", refresh);

  async function take(files) {
    const f = files[0];
    if (!f) return;
    if (!/\.(txt|md|csv|log|json|xml|html?)$/i.test(f.name) && !f.type.startsWith("text/")) return notes.replaceChildren(RT.message(t("ttp_not_text", { name: f.name })));
    area.value = await f.text();
    name = RT.baseName(f);
    notes.replaceChildren();
    refresh();
  }
  RT.setDropHandler(take);

  const pick = el("input", { type: "file", accept: ".txt,.md,.csv,.log,text/plain", class: "file-input", onchange: () => { take([...pick.files]); pick.value = ""; } });
  RT.mount(
    el("p", { class: "hint", text: t("ttp_hint") }),
    area,
    el("div", { class: "toolbar" }, el("label", { class: "tool as-label" }, t("ttp_open"), pick), el("button", { class: "tool", type: "button", onclick: () => { area.value = ""; name = null; refresh(); }, text: t("ttp_clear") })),
    el("div", { class: "options" },
      RT.selectField(t("ttp_font"), [["Helvetica", t("ttp_sans")], ["TimesRoman", t("ttp_serif")], ["Courier", t("ttp_mono")]], o.font, (v) => (o.font = v)),
      RT.selectField(t("ttp_size"), [["9", "9"], ["11", "11"], ["12", "12"], ["14", "14"], ["16", "16"]], String(o.size), (v) => (o.size = +v)),
      RT.selectField(t("ttp_paper"), [["a4", "A4"], ["letter", "Letter"]], o.paper, (v) => (o.paper = v)),
      RT.selectField(t("ttp_margin"), [["36", t("margin_small")], ["56", t("margin_normal")], ["72", t("margin_big")]], String(o.margin), (v) => (o.margin = +v)),
      el("label", { class: "check" }, el("input", { type: "checkbox", checked: true, onchange: (e) => (o.numbers = e.target.checked) }), el("span", { text: t("ttp_numbers") }))),
    notes,
    RT.actionsRow(go)
  );
  refresh();

  async function build() {
    RT.mount(RT.busy());
    try {
      const doc = await RT.newDoc();
      const font = await doc.embedFont(PDFLib.StandardFonts[o.font]);
      const ok = new Set(font.getCharacterSet());
      let replaced = 0;
      const clean = (s) => [...s].map((c) => (ok.has(c.codePointAt(0)) ? c : (replaced++, "?"))).join("");
      const text = area.value.replace(/\r\n?/g, "\n").replace(/\t/g, "    ").replace(/[\u0000-\u0009\u000b-\u001f]/g, "");
      const [W, H] = RT.SHEETS[o.paper];
      const m = o.margin, lh = o.size * 1.35, maxW = W - 2 * m, bottom = m + (o.numbers ? 10 : 0);

      const wrap = (line) => {
        if (!line.trim()) return [""];
        const out = [];
        let cur = "";
        for (const word of line.split(/(?<= )/)) { // words with their trailing space
          if (font.widthOfTextAtSize((cur + word).trimEnd(), o.size) <= maxW) { cur += word; continue; }
          if (cur) out.push(cur.trimEnd());
          cur = "";
          let rest = word;
          while (font.widthOfTextAtSize(rest.trimEnd(), o.size) > maxW) { // a word longer than the line
            let k = rest.length;
            while (k > 1 && font.widthOfTextAtSize(rest.slice(0, k), o.size) > maxW) k--;
            out.push(rest.slice(0, k));
            rest = rest.slice(k);
          }
          cur = rest;
        }
        if (cur) out.push(cur.trimEnd());
        return out;
      };

      let page = doc.addPage([W, H]);
      let y = H - m - o.size;
      for (const raw of text.split("\n")) {
        for (const line of wrap(clean(raw))) {
          if (y < bottom) { page = doc.addPage([W, H]); y = H - m - o.size; }
          if (line) page.drawText(line, { x: m, y, size: o.size, font });
          y -= lh;
        }
      }
      if (o.numbers) {
        const small = await doc.embedFont(PDFLib.StandardFonts.Helvetica);
        doc.getPages().forEach((p, i) => {
          const s = String(i + 1);
          p.drawText(s, { x: (W - small.widthOfTextAtSize(s, 9)) / 2, y: m / 2, size: 9, font: small, color: PDFLib.rgb(0.4, 0.4, 0.4) });
        });
      }
      const n = doc.getPageCount();
      const out = await doc.save();
      RT.showResult({ blob: RT.saveBlob(out, "application/pdf"), filename: (name || t("out_name")) + ".pdf", note: t("ttp_done", { n }) + (replaced ? " " + t("ttp_replaced", { n: replaced }) : "") });
    } catch (e) {
      RT.fail(e);
    }
  }
});
