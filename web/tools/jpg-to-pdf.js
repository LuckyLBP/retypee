"use strict";

/* JPG to PDF: images in, one PDF out. JPEG and PNG files are embedded as they are;
   everything else (WebP, GIF, rotated phone photos) is redrawn through a canvas first. */
RT.run(function start() {
  const { t, el } = RT;
  const items = []; // { file, url, w, h }
  const opts = { size: "a4", margin: "small" };
  const notes = el("div", { class: "notes" });
  const go = el("button", { class: "primary big", type: "button", onclick: build });
  let list;

  const SIZES = { a4: [595.28, 841.89], letter: [612, 792] };
  const MARGINS = { none: 0, small: 28, big: 57 };

  const looksLikeImage = (f) => f.type.startsWith("image/") || /\.(jpe?g|png|webp|gif|bmp|avif|heic|heif)$/i.test(f.name);

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
        items.push({ file, url, w: img.naturalWidth, h: img.naturalHeight });
      } catch {
        URL.revokeObjectURL(url);
        problems.push(t("err_not_image", { name: file.name }));
      }
    }
    notes.replaceChildren(...problems.map((p) => RT.message(p)));
    if (!items.length) return RT.mount(RT.dropzone({ kind: "image", multiple: true, onFiles: add }), notes); // keep the reasons visible
    show();
  }

  function refresh() {
    go.disabled = items.length === 0;
    go.textContent = t("img_btn", { n: items.length });
  }

  function select(name, label, choices) {
    const input = el("select", { onchange: () => (opts[name] = input.value) }, choices.map(([v, text]) => el("option", { value: v, selected: v === opts[name], text })));
    return el("label", { class: "field inline" }, el("span", { text: label }), input);
  }

  function show() {
    if (!items.length) return RT.run(start);
    list = RT.reorderList({
      items,
      render: (it) =>
        el("span", { class: "file-main with-thumb" }, el("img", { class: "file-thumb", src: it.url, alt: "" }),
          el("span", { class: "fc-text" }, el("strong", { class: "file-name", title: it.file.name, text: it.file.name }), el("span", { class: "file-sub", text: `${it.w} × ${it.h} px · ${RT.formatSize(it.file.size)}` }))),
      onChange: () => (items.length ? refresh() : RT.run(start)),
    });
    RT.mount(
      RT.dropzone({ kind: "image", multiple: true, compact: true, onFiles: add }),
      list.el,
      notes,
      el("div", { class: "options" },
        select("size", t("img_size"), [["a4", "A4"], ["letter", "Letter"], ["fit", t("size_fit")]]),
        select("margin", t("img_margin"), [["none", t("margin_none")], ["small", t("margin_small")], ["big", t("margin_big")]])),
      el("div", { class: "actions-row" }, go)
    );
    refresh();
  }

  // Orientation tag of a JPEG (1 = upright). Phone photos are often stored sideways with a tag.
  function exifOrientation(b) {
    if (b[0] !== 0xff || b[1] !== 0xd8) return 1;
    for (let i = 2; i + 4 < b.length && b[i] === 0xff; ) {
      const marker = b[i + 1];
      const len = (b[i + 2] << 8) | b[i + 3];
      if (marker === 0xe1 && b[i + 4] === 0x45 && b[i + 5] === 0x78 && b[i + 6] === 0x69 && b[i + 7] === 0x66) {
        const tiff = i + 10;
        const le = b[tiff] === 0x49;
        const u16 = (o) => (le ? b[o] | (b[o + 1] << 8) : (b[o] << 8) | b[o + 1]);
        const u32 = (o) => (le ? (b[o] | (b[o + 1] << 8) | (b[o + 2] << 16) | (b[o + 3] << 24)) >>> 0 : ((b[o] << 24) | (b[o + 1] << 16) | (b[o + 2] << 8) | b[o + 3]) >>> 0);
        const ifd = tiff + u32(tiff + 4);
        const n = u16(ifd);
        for (let k = 0; k < n; k++) {
          const e = ifd + 2 + k * 12;
          if (u16(e) === 0x0112) return u16(e + 8);
        }
        return 1;
      }
      i += 2 + len;
    }
    return 1;
  }

  async function viaCanvas(it, asPng) {
    const img = await loadImage(it.url);
    const canvas = el("canvas");
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    const ctx = canvas.getContext("2d");
    if (!asPng) {
      ctx.fillStyle = "#fff";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
    ctx.drawImage(img, 0, 0);
    const blob = await new Promise((res) => canvas.toBlob(res, asPng ? "image/png" : "image/jpeg", 0.92));
    return { bytes: new Uint8Array(await blob.arrayBuffer()), png: asPng, w: canvas.width, h: canvas.height };
  }

  async function embed(doc, it) {
    const bytes = await RT.readBytes(it.file);
    const isJpeg = bytes[0] === 0xff && bytes[1] === 0xd8;
    const isPng = bytes[0] === 0x89 && bytes[1] === 0x50;
    try {
      if (isJpeg && exifOrientation(bytes) === 1) return { image: await doc.embedJpg(bytes), w: it.w, h: it.h };
      if (isPng) return { image: await doc.embedPng(bytes), w: it.w, h: it.h };
    } catch {
      /* fall through to the canvas route */
    }
    const c = await viaCanvas(it, false);
    return { image: await doc.embedJpg(c.bytes), w: c.w, h: c.h };
  }

  async function build() {
    RT.mount(RT.busy());
    try {
      const doc = await RT.newDoc();
      const m = MARGINS[opts.margin];
      for (const it of items) {
        const { image, w, h } = await embed(doc, it);
        let pw, ph;
        if (opts.size === "fit") {
          const k = Math.min(0.48, 1400 / Math.max(w, h));
          pw = w * k + 2 * m;
          ph = h * k + 2 * m;
        } else {
          [pw, ph] = SIZES[opts.size];
          if (w > h) [pw, ph] = [ph, pw];
        }
        const page = doc.addPage([pw, ph]);
        const k = Math.min((pw - 2 * m) / w, (ph - 2 * m) / h);
        const dw = w * k;
        const dh = h * k;
        page.drawImage(image, { x: (pw - dw) / 2, y: (ph - dh) / 2, width: dw, height: dh });
      }
      const bytes = await doc.save();
      RT.showResult({ blob: RT.saveBlob(bytes, "application/pdf"), filename: t("out_name") + ".pdf", note: t("img_done", { n: items.length }) });
    } catch (e) {
      RT.fail(e);
    }
  }

  RT.setDropHandler(add);
  RT.mount(RT.dropzone({ kind: "image", multiple: true, onFiles: add }));
});
