"use strict";

/* Auto-crop: find where the ink is on each page and trim the empty margin (pdf-lib, via the crop box). */
RT.run(function start() {
  const { t, el } = RT;

  RT.pdfFlow(async ({ file, bytes, doc, pdf, count }) => {
    RT.mount(RT.busy(t("ac_scanning", { n: 0, total: count })));
    // where the ink is, per page, in displayed points (origin top-left); null for an empty page
    const found = [];
    for (let n = 1; n <= count; n++) {
      const canvas = await RT.renderPage(pdf, n, 700);
      const sp = RT.pageSpace(doc.getPage(n - 1));
      const { data } = canvas.getContext("2d").getImageData(0, 0, canvas.width, canvas.height);
      let x0 = canvas.width, y0 = canvas.height, x1 = -1, y1 = -1;
      for (let y = 0; y < canvas.height; y++) {
        for (let x = 0; x < canvas.width; x++) {
          const i = (y * canvas.width + x) * 4;
          if (data[i] * 0.299 + data[i + 1] * 0.587 + data[i + 2] * 0.114 < 240) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
        }
      }
      const k = sp.vw / canvas.width;
      found.push(x1 < 0 ? null : [x0 * k, y0 * k, (x1 + 1) * k, (y1 + 1) * k]);
      if (n % 4 === 0) { RT.mount(RT.busy(t("ac_scanning", { n, total: count }))); await new Promise((r) => setTimeout(r)); }
    }
    if (found.every((f) => !f)) return RT.mount(RT.fileCard({ file, count, bytes }), RT.message(t("ac_empty"), "info"), RT.actionsRow(RT.restartButton()));

    const o = { margin: 5, same: false };
    const MM = 72 / 25.4;
    const spaces = doc.getPages().map((p) => RT.pageSpace(p));

    // the rectangle to keep on a page, in displayed points
    function target(i) {
      let f = found[i];
      if (o.same) {
        const all = found.filter(Boolean);
        f = [Math.min(...all.map((b) => b[0])), Math.min(...all.map((b) => b[1])), Math.max(...all.map((b) => b[2])), Math.max(...all.map((b) => b[3]))];
      }
      if (!f) return null;
      const m = o.margin * MM, sp = spaces[i];
      return [Math.max(0, f[0] - m), Math.max(0, f[1] - m), Math.min(sp.vw, f[2] + m), Math.min(sp.vh, f[3] + m)];
    }

    const stage = await RT.previewStage(pdf, 1, 340);
    stage.el.style.overflow = "hidden";
    const frame = el("div", { class: "ac-box" });
    stage.el.append(frame);
    const info = el("p", { class: "summary", "aria-live": "polite" });
    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("ac_btn") });
    function paint() {
      const r = target(0);
      frame.hidden = !r;
      if (r) frame.style.cssText = `left:${r[0] * stage.scale}px;top:${r[1] * stage.scale}px;width:${(r[2] - r[0]) * stage.scale}px;height:${(r[3] - r[1]) * stage.scale}px`;
      let before = 0, after = 0, n = 0;
      spaces.forEach((sp, i) => { const r2 = target(i); before += sp.vw * sp.vh; if (r2) { after += (r2[2] - r2[0]) * (r2[3] - r2[1]); n++; } else after += sp.vw * sp.vh; });
      info.textContent = t("ac_info", { n, total: count, pct: Math.round((1 - after / before) * 100) });
    }
    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("p", { class: "hint", text: t("ac_hint") }),
      el("div", { class: "split" },
        el("div", { class: "preview" }, stage.el, el("p", { class: "hint", text: t("preview_note") })),
        el("div", { class: "options col" },
          RT.selectField(t("ac_margin"), [["0", "0 mm"], ["5", "5 mm"], ["10", "10 mm"], ["20", "20 mm"]], String(o.margin), (v) => ((o.margin = +v), paint())),
          RT.selectField(t("ac_mode"), [["each", t("ac_each")], ["same", t("ac_same")]], "each", (v) => ((o.same = v === "same"), paint())),
          info)),
      RT.actionsRow(go, RT.restartButton())
    );
    paint();

    async function run() {
      RT.mount(RT.busy());
      try {
        let done = 0;
        doc.getPages().forEach((page, i) => {
          const r = target(i);
          if (!r) return;
          const sp = spaces[i];
          const a = sp.map(r[0], sp.vh - r[3]), b = sp.map(r[2], sp.vh - r[1]);
          const w = Math.abs(b.x - a.x), h = Math.abs(b.y - a.y);
          if (w < 20 || h < 20) return;
          page.setCropBox(Math.min(a.x, b.x), Math.min(a.y, b.y), w, h);
          done++;
        });
        const out = await doc.save();
        RT.showResult({ blob: RT.saveBlob(out, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("ac_done", { n: done }) });
      } catch (e) {
        RT.fail(e);
      }
    }
  });
});
