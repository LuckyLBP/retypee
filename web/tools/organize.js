"use strict";

/* Organize PDF: drag pages into a new order, turn them, or take them out (pdf-lib). */
RT.run(function start() {
  const { t, el } = RT;

  RT.pdfFlow(async ({ file, bytes, doc, pdf, count }) => {
    const items = Array.from({ length: count }, (_, i) => ({ n: i + 1, rot: 0, gone: false }));
    const grid = el("div", { class: "grid organize", role: "list" });
    const summary = el("p", { class: "summary", "aria-live": "polite" });
    const go = el("button", { class: "primary big", type: "button", onclick: run });
    const cells = new Map();
    const io = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        io.unobserve(entry.target);
        const item = items.find((x) => x.n === +entry.target.dataset.page);
        RT.renderPage(pdf, item.n, 220).then((c) => { cells.get(item).thumb.replaceChildren(c); turn(item); }).catch(() => {});
      }
    }, { rootMargin: "400px" });

    function turn(item) {
      const cell = cells.get(item);
      const c = cell.thumb.querySelector("canvas");
      if (!c) return;
      let k = 1;
      if (item.rot % 180) k = Math.min(cell.thumb.clientWidth / c.offsetHeight, cell.thumb.clientHeight / c.offsetWidth, 1);
      c.style.transform = `rotate(${item.rot}deg) scale(${k})`;
    }

    function refresh() {
      const kept = items.filter((x) => !x.gone).length;
      go.disabled = kept === 0;
      go.textContent = t("org_btn");
      summary.textContent = kept === count && items.every((x, i) => x.n === i + 1 && !x.rot) ? t("org_none") : t("org_summary", { n: kept });
      if (kept === count && items.every((x, i) => x.n === i + 1 && !x.rot)) go.disabled = true;
      items.forEach((it, i) => { cells.get(it).num.textContent = i + 1; });
    }

    function move(from, to) {
      if (to < 0 || to >= items.length || from === to) return;
      const [it] = items.splice(from, 1);
      items.splice(to, 0, it);
      items.forEach((x) => grid.append(cells.get(x).el)); // re-append in the new order; nothing is redrawn
      refresh();
    }

    let dragFrom = null;
    for (const it of items) {
      const thumb = el("div", { class: "thumb" });
      const num = el("span", { class: "thumb-label" });
      const btn = (label, text, fn) => el("button", { type: "button", class: "icon", title: label, "aria-label": label, onclick: fn, text });
      const cell = el("div", { class: "cell", role: "listitem", draggable: "true", "data-page": it.n },
        thumb, num,
        el("span", { class: "turn" },
          btn(t("move_left"), "←", () => move(items.indexOf(it), items.indexOf(it) - 1)),
          btn(t("rotate_left"), "↺", () => { it.rot = (it.rot + 270) % 360; turn(it); refresh(); }),
          btn(t("rotate_right"), "↻", () => { it.rot = (it.rot + 90) % 360; turn(it); refresh(); }),
          btn(t("remove"), "✕", () => { it.gone = !it.gone; cell.classList.toggle("gone", it.gone); refresh(); }),
          btn(t("move_right"), "→", () => move(items.indexOf(it), items.indexOf(it) + 1))));
      cells.set(it, { el: cell, thumb, num });
      cell.addEventListener("dragstart", (e) => { dragFrom = items.indexOf(it); e.dataTransfer.effectAllowed = "move"; e.dataTransfer.setData("text/plain", ""); cell.classList.add("dragging"); });
      cell.addEventListener("dragend", () => { cell.classList.remove("dragging"); dragFrom = null; });
      cell.addEventListener("dragover", (e) => { if (dragFrom != null) e.preventDefault(); });
      cell.addEventListener("drop", (e) => { if (dragFrom == null) return; e.preventDefault(); move(dragFrom, items.indexOf(it)); });
      grid.append(cell);
      io.observe(cell);
    }

    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("p", { class: "hint", text: t("org_hint") }),
      grid, summary,
      el("div", { class: "actions-row sticky" }, go, RT.restartButton())
    );
    refresh();

    async function run() {
      RT.mount(RT.busy());
      try {
        const keep = items.filter((x) => !x.gone);
        const out = await RT.newDoc();
        const copies = await out.copyPages(doc, keep.map((x) => x.n - 1));
        copies.forEach((page, i) => {
          if (keep[i].rot) page.setRotation(PDFLib.degrees((page.getRotation().angle + keep[i].rot) % 360));
          out.addPage(page);
        });
        const bytesOut = await out.save();
        RT.showResult({ blob: RT.saveBlob(bytesOut, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t("org_done", { n: keep.length }) });
      } catch (e) {
        RT.fail(e);
      }
    }
  });
});
