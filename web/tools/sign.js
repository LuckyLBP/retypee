"use strict";

/* Sign PDF: draw or type a signature, drag it where it belongs, stamp it as an image (pdf-lib).
   This is a visible signature, not a digital certificate. */
RT.run(function start() {
  const { t, el } = RT;
  const W = 520, H = 170;

  // A canvas you can draw on with a mouse, pen or finger.
  function drawPad(getColor) {
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    const canvas = el("canvas", { class: "sig-pad", width: W * dpr, height: H * dpr, style: `width:${W}px;max-width:100%;aspect-ratio:${W}/${H}` });
    const ctx = canvas.getContext("2d");
    ctx.scale(dpr, dpr);
    ctx.lineWidth = 2.6;
    ctx.lineCap = ctx.lineJoin = "round";
    let last = null;
    let touched = false;
    const at = (e) => {
      const r = canvas.getBoundingClientRect();
      return [((e.clientX - r.left) * W) / r.width, ((e.clientY - r.top) * H) / r.height];
    };
    canvas.addEventListener("pointerdown", (e) => {
      e.preventDefault();
      canvas.setPointerCapture(e.pointerId);
      last = at(e);
      ctx.strokeStyle = getColor();
      ctx.beginPath();
      ctx.arc(last[0], last[1], 1.3, 0, 7);
      ctx.fillStyle = getColor();
      ctx.fill();
      touched = true;
    });
    canvas.addEventListener("pointermove", (e) => {
      if (!last) return;
      const p = at(e);
      ctx.strokeStyle = getColor();
      ctx.beginPath();
      ctx.moveTo(last[0], last[1]);
      ctx.lineTo(p[0], p[1]);
      ctx.stroke();
      last = p;
    });
    for (const type of ["pointerup", "pointercancel"]) canvas.addEventListener(type, () => (last = null));
    return { canvas, clear: () => { ctx.clearRect(0, 0, W, H); touched = false; }, isEmpty: () => !touched };
  }

  // Cut the empty margin off a canvas and return it as a PNG with transparent background.
  function trim(canvas) {
    const ctx = canvas.getContext("2d");
    const { width, height } = canvas;
    const data = ctx.getImageData(0, 0, width, height).data;
    let x0 = width, y0 = height, x1 = 0, y1 = 0;
    for (let y = 0; y < height; y++) for (let x = 0; x < width; x++) if (data[(y * width + x) * 4 + 3] > 8) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
    if (x1 <= x0 || y1 <= y0) return null;
    const pad = 6;
    x0 = Math.max(0, x0 - pad); y0 = Math.max(0, y0 - pad); x1 = Math.min(width - 1, x1 + pad); y1 = Math.min(height - 1, y1 + pad);
    const out = el("canvas");
    out.width = x1 - x0 + 1;
    out.height = y1 - y0 + 1;
    out.getContext("2d").drawImage(canvas, x0, y0, out.width, out.height, 0, 0, out.width, out.height);
    return { url: out.toDataURL("image/png"), aspect: out.height / out.width };
  }

  RT.pdfFlow(async ({ file, bytes, doc, pdf, count }) => {
    const state = { color: "#1b1713", mode: "draw", typed: "", font: 0 };
    const FONTS = ['"Snell Roundhand", "Segoe Script", "Brush Script MT", cursive', '"Bradley Hand", "Segoe Print", "Comic Sans MS", cursive', '"Apple Chancery", "Lucida Handwriting", cursive'];
    const colors = [["#1b1713", t("sig_black")], ["#1f3fb8", t("sig_blue")]];

    function makeSignature() {
      const pad = drawPad(() => state.color);
      const typed = el("input", { type: "text", class: "range-input", maxlength: "40", placeholder: t("sig_type_ph"), autocomplete: "off" });
      const preview = el("canvas", { class: "sig-pad", width: W, height: H, style: `width:${W}px;max-width:100%;aspect-ratio:${W}/${H}` });
      const drawText = () => {
        const ctx = preview.getContext("2d");
        ctx.clearRect(0, 0, W, H);
        let size = 96;
        ctx.fillStyle = state.color;
        ctx.textBaseline = "middle";
        do { ctx.font = `${size}px ${FONTS[state.font]}`; size -= 4; } while (ctx.measureText(typed.value).width > W - 30 && size > 24);
        ctx.fillText(typed.value, 15, H / 2);
      };
      typed.addEventListener("input", () => { state.typed = typed.value; drawText(); });
      const area = el("div", { class: "sig-area" });
      const show = () => {
        area.replaceChildren(...(state.mode === "draw"
          ? [pad.canvas, el("p", { class: "hint", text: t("sig_draw_hint") })]
          : [RT.field(t("sig_type"), typed), RT.selectField(t("sig_style"), FONTS.map((_, i) => [String(i), t("sig_style_n", { n: i + 1 })]), String(state.font), (v) => ((state.font = +v), drawText())), preview]));
        tabs.forEach(([m, b]) => b.setAttribute("aria-pressed", String(m === state.mode)));
      };
      const tabs = [["draw", el("button", { type: "button", class: "tool", onclick: () => ((state.mode = "draw"), show()), text: t("sig_tab_draw") })],
                    ["type", el("button", { type: "button", class: "tool", onclick: () => ((state.mode = "type"), show()), text: t("sig_tab_type") })]];
      const colorPick = RT.selectField(t("sig_color"), colors, state.color, (v) => { state.color = v; if (state.mode === "type") drawText(); });
      const note = el("div", { class: "notes" });
      const use = el("button", { class: "primary big", type: "button", text: t("sig_use"), onclick: () => {
        const source = state.mode === "draw" ? pad.canvas : preview;
        if (state.mode === "draw" ? pad.isEmpty() : !typed.value.trim()) return note.replaceChildren(RT.message(t("sig_empty")));
        const sig = trim(source);
        if (!sig) return note.replaceChildren(RT.message(t("sig_empty")));
        place(sig);
      } });
      RT.mount(
        RT.fileCard({ file, count, bytes }),
        el("p", { class: "hint", text: t("sig_step1") }),
        el("div", { class: "toolbar" }, tabs.map(([, b]) => b), colorPick, el("button", { type: "button", class: "tool", onclick: () => { pad.clear(); typed.value = ""; state.typed = ""; drawText(); }, text: t("sig_clear") })),
        area, note,
        RT.actionsRow(use, RT.restartButton())
      );
      show();
    }

    async function place(sig) {
      const pos = { fx: 0.55, fy: 0.78, fw: 0.28, page: 1, all: false };
      let stage = null;
      const img = el("img", { class: "sig-img", src: sig.url, alt: "", draggable: "false" });
      const holder = el("div", { class: "preview" });
      const label = el("span", { class: "page-label", "aria-live": "polite" });
      const layout = () => {
        const w = pos.fw * stage.width;
        img.style.cssText = `width:${w}px;height:${w * sig.aspect}px;left:${pos.fx * stage.width}px;top:${pos.fy * stage.height}px`;
        label.textContent = `${pos.page} / ${count}`;
      };
      async function show(n) {
        pos.page = n;
        stage = await RT.previewStage(pdf, n, 440);
        stage.el.append(img);
        holder.replaceChildren(stage.el);
        layout();
      }
      img.addEventListener("pointerdown", (e) => {
        e.preventDefault();
        img.setPointerCapture(e.pointerId);
        const r = stage.el.getBoundingClientRect();
        const dx = e.clientX - r.left - pos.fx * stage.width, dy = e.clientY - r.top - pos.fy * stage.height;
        const move = (ev) => {
          const h = (pos.fw * stage.width) * sig.aspect;
          pos.fx = Math.max(0, Math.min(1 - pos.fw, (ev.clientX - r.left - dx) / stage.width));
          pos.fy = Math.max(0, Math.min(1 - h / stage.height, (ev.clientY - r.top - dy) / stage.height));
          layout();
        };
        const up = () => { img.removeEventListener("pointermove", move); img.removeEventListener("pointerup", up); };
        img.addEventListener("pointermove", move);
        img.addEventListener("pointerup", up);
      });
      const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("sig_btn") });
      const all = el("input", { type: "checkbox", onchange: () => (pos.all = all.checked) });
      RT.mount(
        RT.fileCard({ file, count, bytes }),
        el("p", { class: "hint", text: t("sig_step2") }),
        el("div", { class: "split" },
          holder,
          el("div", { class: "options col" },
            RT.rangeField(t("sig_size"), { min: 10, max: 60, value: Math.round(pos.fw * 100) }, (v) => ((pos.fw = v / 100), layout()), (v) => `${v} %`),
            count > 1 ? el("div", { class: "pager inline" },
              el("button", { type: "button", class: "icon", "aria-label": t("prev_page"), onclick: () => pos.page > 1 && show(pos.page - 1), text: "‹" }), label,
              el("button", { type: "button", class: "icon", "aria-label": t("next_page"), onclick: () => pos.page < count && show(pos.page + 1), text: "›" })) : null,
            count > 1 ? el("label", { class: "check" }, all, el("span", { text: t("sig_all") })) : null,
            el("button", { type: "button", class: "tool", onclick: makeSignature, text: t("sig_redo") }))),
        RT.actionsRow(go, RT.restartButton())
      );
      await show(1);

      async function run() {
        RT.mount(RT.busy());
        try {
          const png = await doc.embedPng(Uint8Array.from(atob(sig.url.split(",")[1]), (c) => c.charCodeAt(0))); // decoded here: fetching a data: URL is not allowed by the CSP
          const pages = doc.getPages();
          const targets = pos.all ? pages.map((_, i) => i) : [pos.page - 1];
          for (const i of targets) {
            const page = pages[i];
            const { vw, vh, rot, map } = RT.pageSpace(page);
            const width = pos.fw * vw, height = width * sig.aspect;
            const p = map(pos.fx * vw, vh - pos.fy * vh - height);
            page.drawImage(png, { x: p.x, y: p.y, width, height, rotate: PDFLib.degrees(rot) });
          }
          const out = await doc.save();
          RT.showResult({ blob: RT.saveBlob(out, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("sig_done") });
        } catch (e) {
          RT.fail(e);
        }
      }
    }

    makeSignature();
  });
});
