"use strict";

/* Scan to PDF: photos of paper become a clean document. Each page can be left as photographed,
   evened out (shadows gone, paper white) or turned black and white, then everything is joined into one PDF. */
RT.run(function start() {
  const { t, el } = RT;
  const items = []; // { file, url, img, rot, canvas }
  const opts = { filter: "clean", size: "a4", margin: "none" };
  const notes = el("div", { class: "notes" });
  const go = el("button", { class: "primary big", type: "button", onclick: build });
  const SIZES = { a4: [595.28, 841.89], letter: [612, 792] };
  const MARGINS = { none: 0, small: 24 };
  const looksLikeImage = (f) => f.type.startsWith("image/") || /\.(jpe?g|png|webp|gif|bmp|avif|heic|heif)$/i.test(f.name);

  /* ---------------------------------------------------------------- image processing */

  // The photo, turned by `rot` degrees and scaled so its long side is at most maxSide.
  function draw(it, maxSide) {
    const w0 = it.img.naturalWidth, h0 = it.img.naturalHeight;
    const k = Math.min(1, maxSide / Math.max(w0, h0));
    const sideways = it.rot % 180 !== 0;
    const canvas = el("canvas");
    canvas.width = Math.max(1, Math.round((sideways ? h0 : w0) * k));
    canvas.height = Math.max(1, Math.round((sideways ? w0 : h0) * k));
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    ctx.fillStyle = "#fff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.translate(canvas.width / 2, canvas.height / 2);
    ctx.rotate((it.rot * Math.PI) / 180);
    ctx.drawImage(it.img, (-w0 * k) / 2, (-h0 * k) / 2, w0 * k, h0 * k);
    return canvas;
  }

  // Grey levels divided by the local paper brightness: shadows and uneven light disappear, then
  // the contrast is stretched. "bw" goes one step further and keeps only black and white.
  function enhance(canvas, mode) {
    const w = canvas.width, h = canvas.height;
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    const img = ctx.getImageData(0, 0, w, h);
    const px = img.data;
    const grey = new Float32Array(w * h);
    for (let i = 0, p = 0; i < grey.length; i++, p += 4) grey[i] = 0.299 * px[p] + 0.587 * px[p + 1] + 0.114 * px[p + 2];

    // box blur through an integral image gives the local average
    const W = w + 1;
    const sum = new Float64Array(W * (h + 1));
    for (let y = 0; y < h; y++) {
      let row = 0;
      for (let x = 0; x < w; x++) {
        row += grey[y * w + x];
        sum[(y + 1) * W + x + 1] = sum[y * W + x + 1] + row;
      }
    }
    const r = Math.max(8, Math.round(Math.max(w, h) / 24));
    for (let y = 0; y < h; y++) {
      const y0 = Math.max(0, y - r), y1 = Math.min(h, y + r + 1);
      for (let x = 0; x < w; x++) {
        const x0 = Math.max(0, x - r), x1 = Math.min(w, x + r + 1);
        const mean = (sum[y1 * W + x1] - sum[y0 * W + x1] - sum[y1 * W + x0] + sum[y0 * W + x0]) / ((x1 - x0) * (y1 - y0));
        const ratio = grey[y * w + x] / Math.max(mean, 1);
        const v = mode === "bw" ? (ratio < 0.86 ? 0 : 255) : Math.max(0, Math.min(255, (255 * (ratio - 0.3)) / 0.6));
        const p = (y * w + x) * 4;
        px[p] = px[p + 1] = px[p + 2] = v;
      }
    }
    ctx.putImageData(img, 0, 0);
    return canvas;
  }

  function render(it, maxSide) {
    const canvas = draw(it, maxSide);
    return opts.filter === "original" ? canvas : enhance(canvas, opts.filter);
  }

  function paintThumb(it) {
    const c = render(it, 220);
    it.thumb.width = c.width;
    it.thumb.height = c.height;
    it.thumb.getContext("2d").drawImage(c, 0, 0);
  }

  /* ---------------------------------------------------------------- list screen */

  function loadImage(url) {
    const img = new Image();
    img.src = url;
    return img.decode().then(() => img);
  }

  async function add(selected) {
    notes.replaceChildren(RT.busy());
    const problems = [];
    for (const file of selected) {
      if (!looksLikeImage(file)) {
        problems.push(t("err_not_image", { name: file.name }));
        continue;
      }
      const url = URL.createObjectURL(file);
      try {
        const img = await loadImage(url);
        const it = { file, url, img, rot: 0, thumb: el("canvas", { class: "scan-thumb" }) };
        items.push(it);
        paintThumb(it);
      } catch {
        URL.revokeObjectURL(url);
        problems.push(t("err_not_image", { name: file.name }));
      }
    }
    notes.replaceChildren(...problems.map((p) => RT.message(p)));
    if (!items.length) return RT.mount(intake(false), notes);
    show();
  }

  // the drop zone, plus a camera button on phones and tablets
  function intake(compact) {
    const cam = el("input", { type: "file", accept: "image/*", capture: "environment", hidden: true });
    cam.addEventListener("change", () => { const f = [...cam.files]; cam.value = ""; if (f.length) add(f); });
    const touch = window.matchMedia && matchMedia("(pointer: coarse)").matches;
    return el("div", { class: "intake" },
      RT.dropzone({ kind: "image", multiple: true, compact, onFiles: add }),
      touch ? el("label", { class: "tool camera" }, t("scan_camera"), cam) : null);
  }

  function refresh() {
    go.disabled = items.length === 0;
    go.textContent = t("scan_btn", { n: items.length });
  }

  function show() {
    const list = RT.reorderList({
      items,
      render: (it) =>
        el("span", { class: "file-main with-thumb" }, it.thumb,
          el("span", { class: "fc-text" },
            el("strong", { class: "file-name", title: it.file.name, text: it.file.name }),
            el("span", { class: "scan-turn" },
              el("button", { type: "button", class: "icon", title: t("rotate_left"), "aria-label": t("rotate_left"), onclick: () => { it.rot = (it.rot + 270) % 360; paintThumb(it); }, text: "↺" }),
              el("button", { type: "button", class: "icon", title: t("rotate_right"), "aria-label": t("rotate_right"), onclick: () => { it.rot = (it.rot + 90) % 360; paintThumb(it); }, text: "↻" })))),
      onChange: () => (items.length ? refresh() : RT.run(start)),
    });
    RT.mount(
      intake(true),
      list.el,
      notes,
      el("div", { class: "options" },
        RT.selectField(t("scan_filter"), [["clean", t("scan_clean")], ["bw", t("scan_bw")], ["original", t("scan_original")]], opts.filter, (v) => { opts.filter = v; items.forEach(paintThumb); }),
        RT.selectField(t("img_size"), [["a4", "A4"], ["letter", "Letter"], ["fit", t("size_fit")]], opts.size, (v) => (opts.size = v)),
        RT.selectField(t("img_margin"), [["none", t("margin_none")], ["small", t("margin_small")]], opts.margin, (v) => (opts.margin = v))),
      RT.actionsRow(go)
    );
    refresh();
  }

  /* ---------------------------------------------------------------- build */

  async function build() {
    RT.mount(RT.busy());
    try {
      const doc = await RT.newDoc();
      const m = MARGINS[opts.margin];
      const png = opts.filter === "bw";
      for (const it of items) {
        await new Promise((r) => setTimeout(r, 0)); // let the busy card paint between pages
        const canvas = render(it, 2400);
        const blob = await new Promise((res) => canvas.toBlob(res, png ? "image/png" : "image/jpeg", 0.82));
        const bytes = new Uint8Array(await blob.arrayBuffer());
        const image = png ? await doc.embedPng(bytes) : await doc.embedJpg(bytes);
        const { width: w, height: h } = canvas;
        let pw, ph;
        if (opts.size === "fit") {
          const k = Math.min(0.36, 1000 / Math.max(w, h));
          pw = w * k + 2 * m;
          ph = h * k + 2 * m;
        } else {
          [pw, ph] = SIZES[opts.size];
          if (w > h) [pw, ph] = [ph, pw];
        }
        const page = doc.addPage([pw, ph]);
        const k = Math.min((pw - 2 * m) / w, (ph - 2 * m) / h);
        page.drawImage(image, { x: (pw - w * k) / 2, y: (ph - h * k) / 2, width: w * k, height: h * k });
      }
      const out = await doc.save();
      RT.showResult({ blob: RT.saveBlob(out, "application/pdf"), filename: t("out_name") + ".pdf", note: t("scan_done", { n: items.length }) });
    } catch (e) {
      RT.fail(e);
    }
  }

  RT.setDropHandler(add);
  RT.mount(intake(false));
});
