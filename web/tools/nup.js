"use strict";

/* Pages per sheet: two, four, six or nine pages on each sheet (pdf-lib). */
RT.run(function start() {
  const { t, el } = RT;

  RT.pdfFlow(async ({ file, bytes, doc, count }) => {
    const first = RT.pageSpace(doc.getPage(0));
    const o = { per: 2, size: "a4", turn: "auto", border: true, margin: 18 };
    const GAP = 10;

    // columns x rows (and the sheet's orientation) that give the biggest pages
    function plan() {
      const base = RT.SHEETS[o.size];
      const grids = { 2: [[2, 1], [1, 2]], 4: [[2, 2]], 6: [[3, 2], [2, 3]], 9: [[3, 3]] }[o.per];
      const turns = o.turn === "auto" ? ["portrait", "landscape"] : [o.turn];
      let best = null;
      for (const turn of turns) {
        const [W, H] = turn === "portrait" ? base : [base[1], base[0]];
        for (const [cols, rows] of grids) {
          const cw = (W - 2 * o.margin - (cols - 1) * GAP) / cols, ch = (H - 2 * o.margin - (rows - 1) * GAP) / rows;
          const k = Math.min(cw / first.vw, ch / first.vh);
          if (!best || k > best.k) best = { W, H, cols, rows, cw, ch, k };
        }
      }
      return best;
    }

    const sketch = el("div", { class: "nup-sketch", "aria-hidden": "true" });
    const info = el("p", { class: "hint" });
    function paint() {
      const p = plan();
      sketch.style.cssText = `aspect-ratio:${p.W}/${p.H};grid-template-columns:repeat(${p.cols},1fr);grid-template-rows:repeat(${p.rows},1fr)`;
      sketch.replaceChildren(...Array.from({ length: p.cols * p.rows }, (_, i) => el("span", { text: i + 1 })));
      info.textContent = t("nup_info", { sheets: Math.ceil(count / o.per), pages: count });
    }

    const border = el("input", { type: "checkbox", checked: true, onchange: () => ((o.border = border.checked), paint()) });
    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("nup_btn") });
    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("div", { class: "split" },
        el("div", { class: "preview" }, sketch, info),
        el("div", { class: "options col" },
          RT.selectField(t("nup_per"), [["2", "2"], ["4", "4"], ["6", "6"], ["9", "9"]], "2", (v) => ((o.per = +v), paint())),
          RT.selectField(t("nup_size"), [["a4", "A4"], ["letter", "Letter"], ["a3", "A3"]], o.size, (v) => ((o.size = v), paint())),
          RT.selectField(t("nup_turn"), [["auto", t("nup_auto")], ["portrait", t("nup_portrait")], ["landscape", t("nup_landscape")]], o.turn, (v) => ((o.turn = v), paint())),
          el("label", { class: "check" }, border, el("span", { text: t("nup_border") })))),
      RT.actionsRow(go, RT.restartButton())
    );
    paint();

    async function run() {
      RT.mount(RT.busy());
      try {
        const out = await RT.newDoc();
        const pages = await RT.embedAll(out, doc);
        const p = plan();
        for (let i = 0; i < count; i += o.per) {
          const sheet = out.addPage([p.W, p.H]);
          for (let j = 0; j < o.per && i + j < count; j++) {
            const src = pages[i + j];
            const col = j % p.cols, row = Math.floor(j / p.cols);
            const cx = o.margin + col * (p.cw + GAP), cy = p.H - o.margin - (row + 1) * p.ch - row * GAP;
            const k = Math.min(p.cw / src.sp.vw, p.ch / src.sp.vh);
            const x = cx + (p.cw - src.sp.vw * k) / 2, y = cy + (p.ch - src.sp.vh * k) / 2;
            RT.drawVisible(sheet, src, x, y, k);
            if (o.border) sheet.drawRectangle({ x, y, width: src.sp.vw * k, height: src.sp.vh * k, borderColor: PDFLib.rgb(0.55, 0.55, 0.55), borderWidth: 0.5 });
          }
        }
        const saved = await out.save();
        RT.showResult({ blob: RT.saveBlob(saved, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("nup_done", { n: count, sheets: Math.ceil(count / o.per) }) });
      } catch (e) {
        RT.fail(e);
      }
    }
  });
});
