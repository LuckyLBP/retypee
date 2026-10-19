"use strict";

/* OCR: makes a scanned PDF searchable. Each page is drawn, read by Tesseract (WebAssembly, in a
   worker) and the words are laid back over the page as invisible text, so the scan looks the same. */
RT.run(function start() {
  const { t, el } = RT;

  const LANGS = [["swe", "Svenska"], ["eng", "English"], ["nor", "Norsk"], ["dan", "Dansk"], ["fin", "Suomi"], ["deu", "Deutsch"], ["fra", "Français"], ["spa", "Español"]];
  const CORE = "https://cdn.jsdelivr.net/npm/tesseract.js-core@5.1.0";
  const langPath = (l) => `https://cdn.jsdelivr.net/npm/@tesseract.js-data/${l}/4.0.0_best_int`;
  const DPI = 200;

  RT.pdfFlow(async ({ file, bytes, doc, pdf, count }) => {
    const o = { lang: document.documentElement.lang === "sv" ? "swe" : "eng", all: false };

    // pages that already carry text are left alone unless the visitor asks otherwise
    const hasText = [];
    const known = (async () => {
      for (let n = 1; n <= count; n++) hasText.push((await (await pdf.getPage(n)).getTextContent()).items.some((i) => i.str.trim()));
      return hasText.filter(Boolean).length;
    })();
    const info = el("p", { class: "hint" });
    known.then((n) => (info.textContent = n ? t("ocr_has_text", { n, total: count }) : "")).catch(() => {});

    const all = el("input", { type: "checkbox", onchange: () => (o.all = all.checked) });
    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("ocr_btn") });
    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("div", { class: "options col" },
        RT.selectField(t("ocr_lang"), LANGS, o.lang, (v) => (o.lang = v)),
        el("label", { class: "check" }, all, el("span", { text: t("ocr_all") })),
        info,
        el("p", { class: "hint", text: t("ocr_dl_note") })),
      RT.actionsRow(go, RT.restartButton())
    );

    async function run() {
      let cancelled = false;
      let worker = null;
      const label = el("span", { text: t("ocr_loading") });
      const bar = el("progress", { max: "100", value: "0", class: "ocr-bar" });
      const cancel = el("button", { class: "tool", type: "button", text: t("cancel"), onclick: () => { cancelled = true; worker && worker.terminate(); RT.reset(); } });
      RT.mount(el("div", { class: "busy-card stack" }, el("span", { class: "spinner", "aria-hidden": "true" }), label, bar, cancel));

      try {
        await known;
        const todo = [];
        for (let n = 1; n <= count; n++) if (o.all || !hasText[n - 1]) todo.push(n);
        if (!todo.length) return RT.mount(RT.message(t("ocr_nothing_to_do"), "info"), RT.actionsRow(RT.restartButton()));

        let done = 0;
        const logger = (m) => {
          if (/loading|initializing/.test(m.status)) { label.textContent = t("ocr_loading"); return; }
          if (m.status === "recognizing text") bar.value = ((done + m.progress) / todo.length) * 100;
        };
        try {
          worker = await Tesseract.createWorker(o.lang, 1, {
            workerPath: location.origin + "/vendor/tesseract-worker.min.js",
            workerBlobURL: false,
            corePath: CORE,
            langPath: langPath(o.lang),
            logger,
          });
        } catch (e) {
          if (cancelled) return;
          console.error(e);
          throw new Error(t("ocr_download_fail"));
        }

        const font = await doc.embedFont(PDFLib.StandardFonts.Helvetica);
        const ok = new Set(font.getCharacterSet());
        const pages = doc.getPages();
        let words = 0;
        for (const n of todo) {
          if (cancelled) return;
          label.textContent = t("ocr_page", { n: done + 1, total: todo.length });
          const page = await pdf.getPage(n);
          const base = page.getViewport({ scale: 1 });
          const k = Math.min(DPI / 72, 3200 / Math.max(base.width, base.height));
          const viewport = page.getViewport({ scale: k });
          const canvas = el("canvas");
          canvas.width = Math.ceil(viewport.width);
          canvas.height = Math.ceil(viewport.height);
          await page.render({ canvasContext: canvas.getContext("2d"), viewport }).promise;
          const { data } = await worker.recognize(canvas);
          if (cancelled) return;

          const target = pages[n - 1];
          const sp = RT.pageSpace(target);
          const fx = sp.vw / canvas.width, fy = sp.vh / canvas.height;
          target.pushOperators(PDFLib.pushGraphicsState(), PDFLib.setTextRenderingMode(PDFLib.TextRenderingMode.Invisible));
          for (const w of data.words || []) {
            const text = [...w.text].filter((c) => ok.has(c.codePointAt(0))).join("").trim();
            if (!text || w.confidence < 20) continue;
            const wid = (w.bbox.x1 - w.bbox.x0) * fx, hei = (w.bbox.y1 - w.bbox.y0) * fy;
            if (wid <= 0 || hei <= 0) continue;
            const size = Math.min(Math.max(wid / font.widthOfTextAtSize(text, 1), hei * 0.5), hei * 2);
            const p = sp.map(w.bbox.x0 * fx, sp.vh - w.bbox.y1 * fy + size * 0.2);
            target.drawText(text, { x: p.x, y: p.y, size, font, rotate: PDFLib.degrees(sp.rot) });
            words++;
          }
          target.pushOperators(PDFLib.popGraphicsState());
          canvas.width = canvas.height = 0;
          done++;
          bar.value = (done / todo.length) * 100;
        }
        await worker.terminate();
        worker = null;
        if (!words) return RT.mount(RT.message(t("ocr_no_words"), "info"), RT.actionsRow(RT.restartButton()));

        const out = await doc.save();
        RT.showResult({
          blob: RT.saveBlob(out, "application/pdf"),
          filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`,
          note: t("ocr_done", { n: todo.length, words }) + (todo.length < count ? " " + t("ocr_skipped", { n: count - todo.length }) : ""),
        });
      } catch (e) {
        worker && worker.terminate();
        RT.fail(e);
      }
    }
  });
});
