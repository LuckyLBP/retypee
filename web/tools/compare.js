"use strict";

/* Compare PDF: pull the text out of two versions and show what was added and removed (pdf.js). */
RT.run(function start() {
  const { t, el } = RT;
  const slots = { a: null, b: null }; // { file, pdf, bytes }

  // Text of one page as lines, in reading order.
  async function pageLines(pdf, n) {
    const content = await (await pdf.getPage(n)).getTextContent();
    const items = content.items.filter((i) => i.str && i.str.trim()).map((i) => ({ s: i.str, x: i.transform[4], y: i.transform[5], h: i.height || 10 }));
    items.sort((p, q) => q.y - p.y || p.x - q.x);
    const rows = [];
    for (const it of items) {
      const row = rows[rows.length - 1];
      if (row && Math.abs(row.y - it.y) <= Math.max(2, it.h * 0.4)) row.items.push(it);
      else rows.push({ y: it.y, items: [it] });
    }
    return rows.map((r) => r.items.sort((p, q) => p.x - q.x).map((i) => i.s).join(" ").replace(/\s+/g, " ").trim()).filter(Boolean);
  }

  async function allLines(pdf) {
    const out = [];
    for (let n = 1; n <= pdf.numPages; n++) for (const text of await pageLines(pdf, n)) out.push({ text, page: n });
    return out;
  }

  // Line diff: trim what both share, then longest-common-subsequence on the rest.
  function diffLines(a, b) {
    const same = (x, y) => x.text === y.text;
    let s = 0;
    while (s < a.length && s < b.length && same(a[s], b[s])) s++;
    let e = 0;
    while (e < a.length - s && e < b.length - s && same(a[a.length - 1 - e], b[b.length - 1 - e])) e++;
    const A = a.slice(s, a.length - e), B = b.slice(s, b.length - e);
    if (A.length * B.length > 16e6) return null;
    const n = A.length, m = B.length, w = m + 1, L = new Uint16Array((n + 1) * w);
    for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--) L[i * w + j] = same(A[i], B[j]) ? L[(i + 1) * w + j + 1] + 1 : Math.max(L[(i + 1) * w + j], L[i * w + j + 1]);
    const ops = a.slice(0, s).map((x) => ({ t: "=", line: x }));
    let i = 0, j = 0;
    while (i < n && j < m) {
      if (same(A[i], B[j])) { ops.push({ t: "=", line: B[j] }); i++; j++; }
      else if (L[(i + 1) * w + j] >= L[i * w + j + 1]) ops.push({ t: "-", line: A[i++] });
      else ops.push({ t: "+", line: B[j++] });
    }
    while (i < n) ops.push({ t: "-", line: A[i++] });
    while (j < m) ops.push({ t: "+", line: B[j++] });
    return ops.concat(b.slice(b.length - e).map((x) => ({ t: "=", line: x })));
  }

  function slot(key, title) {
    const body = el("div", { class: "cmp-slot" });
    const draw = () => {
      const s = slots[key];
      body.replaceChildren(el("p", { class: "cmp-title", text: title }), s ? RT.fileCard({ file: s.file, count: s.pdf.numPages, bytes: s.bytes }) : RT.dropzone({ compact: true, onFiles: (f) => load(key, f[0], draw) }));
    };
    draw();
    return { el: body, draw };
  }

  async function load(key, file, draw) {
    if (!RT.isPdf(file)) return RT.mount(RT.message(t("err_not_pdf", { name: file.name })), ...layout());
    try {
      const bytes = await RT.readBytes(file);
      slots[key] = { file, bytes, pdf: await RT.openForRender(bytes) };
      draw();
      go.disabled = !(slots.a && slots.b);
    } catch (e) {
      RT.mount(RT.message(e.message), ...layout());
    }
  }

  const go = el("button", { class: "primary big", type: "button", disabled: true, onclick: run, text: t("cmp_btn") });
  const a = slot("a", t("cmp_a")), b = slot("b", t("cmp_b"));
  const layout = () => [el("div", { class: "cmp-slots" }, a.el, b.el), RT.actionsRow(go)];

  async function run() {
    RT.mount(RT.busy());
    try {
      const [la, lb] = [await allLines(slots.a.pdf), await allLines(slots.b.pdf)];
      if (!la.length || !lb.length) return RT.mount(RT.message(t("cmp_notext")), el("div", { class: "actions-row" }, RT.restartButton()));
      const ops = diffLines(la, lb);
      if (!ops) return RT.mount(RT.message(t("cmp_toobig")), el("div", { class: "actions-row" }, RT.restartButton()));
      const removed = ops.filter((o) => o.t === "-").length, added = ops.filter((o) => o.t === "+").length;
      const list = el("div", { class: "diff" });
      let showAll = false;
      const paint = () => {
        const rows = [];
        ops.forEach((o, i) => {
          const near = ops.slice(Math.max(0, i - 1), i + 2).some((x) => x.t !== "=");
          if (o.t === "=" && !showAll && !near) return;
          const mark = o.t === "-" ? "−" : o.t === "+" ? "+" : "";
          rows.push(el("div", { class: `diff-row ${o.t === "-" ? "del" : o.t === "+" ? "add" : "same"}` }, el("span", { class: "diff-mark", text: mark }), el("span", { class: "diff-page", text: o.line.page }), el("span", { class: "diff-text", text: o.line.text })));
        });
        list.replaceChildren(...(rows.length ? rows : [el("p", { class: "hint", text: t("cmp_identical") })]));
      };
      const toggle = el("input", { type: "checkbox", onchange: () => ((showAll = toggle.checked), paint()) });
      paint();
      RT.mount(
        el("div", { class: "cmp-summary" }, el("strong", { text: removed || added ? t("cmp_found") : t("cmp_identical") }), el("span", { class: "del-count", text: t("cmp_removed", { n: removed }) }), el("span", { class: "add-count", text: t("cmp_added", { n: added }) })),
        el("label", { class: "check" }, toggle, el("span", { text: t("cmp_all") })),
        list,
        el("p", { class: "hint", text: t("cmp_note") }),
        RT.actionsRow(RT.restartButton())
      );
    } catch (e) {
      RT.fail(e);
    }
  }

  RT.setDropHandler((files) => {
    const key = !slots.a ? "a" : "b";
    load(key, files[0], key === "a" ? a.draw : b.draw);
  });
  RT.mount(...layout());
});
