"use strict";

/* PDF to text: the words of a PDF as a .txt or .md file (pdf.js). */
RT.run(function start() {
  const { t, el } = RT;

  async function pageRows(pdf, n) {
    const content = await (await pdf.getPage(n)).getTextContent();
    const items = content.items.filter((i) => i.str && i.str.trim()).map((i) => ({ s: i.str, x: i.transform[4], y: i.transform[5], h: i.height || 10, w: i.width || 0 }));
    items.sort((p, q) => q.y - p.y || p.x - q.x);
    const rows = [];
    for (const it of items) {
      const row = rows[rows.length - 1];
      if (row && Math.abs(row.y - it.y) <= Math.max(2, it.h * 0.4)) row.items.push(it);
      else rows.push({ y: it.y, items: [it] });
    }
    return rows.map((r) => {
      r.items.sort((p, q) => p.x - q.x);
      let text = "";
      r.items.forEach((it, i) => {
        const prev = r.items[i - 1];
        text += i && it.x - (prev.x + prev.w) > it.h * 0.15 ? " " + it.s : it.s;
      });
      return { text: text.replace(/\s+/g, " ").trim(), size: Math.max(...r.items.map((i) => i.h)), y: r.y };
    }).filter((r) => r.text);
  }

  async function open(selected) {
    const file = selected[0];
    if (!RT.isPdf(file)) return RT.mount(RT.message(t("err_not_pdf", { name: file.name })), RT.dropzone({ onFiles: open }));
    RT.mount(RT.busy());
    try {
      const bytes = await RT.readBytes(file);
      const pdf = await RT.openForRender(bytes);
      options(file, bytes, pdf);
    } catch (e) {
      RT.mount(RT.message(e.message), RT.dropzone({ onFiles: open }));
    }
  }

  function options(file, bytes, pdf) {
    const o = { format: "txt", pages: false };
    const pages = el("input", { type: "checkbox", onchange: () => (o.pages = pages.checked) });
    const go = el("button", { class: "primary big", type: "button", onclick: run, text: t("txt_btn") });
    RT.mount(
      RT.fileCard({ file, count: pdf.numPages, bytes }),
      el("div", { class: "options" }, RT.selectField(t("txt_format"), [["txt", t("txt_plain")], ["md", t("txt_md")]], o.format, (v) => (o.format = v)), el("label", { class: "check" }, pages, el("span", { text: t("txt_pages") }))),
      RT.actionsRow(go, RT.restartButton())
    );

    async function run() {
      RT.mount(RT.busy());
      try {
        const all = [];
        for (let n = 1; n <= pdf.numPages; n++) all.push(await pageRows(pdf, n));
        const sizes = all.flat().map((r) => r.size).sort((a, b) => a - b);
        if (!sizes.length) return RT.mount(RT.message(t("txt_none")), el("div", { class: "actions-row" }, RT.restartButton()));
        const body = sizes[Math.floor(sizes.length / 2)];
        const md = o.format === "md";
        const chunks = all.map((rows, i) => {
          const out = [];
          let prevY = null, prevSize = body;
          rows.forEach((r) => {
            const gap = prevY == null ? 0 : prevY - r.y;
            const heading = md && r.size >= body * 1.25 ? (r.size >= body * 1.6 ? "# " : "## ") : "";
            if (prevY != null && (gap > Math.max(prevSize, r.size) * 1.7 || heading)) out.push("");
            out.push(heading + r.text);
            prevY = r.y;
            prevSize = r.size;
          });
          return (o.pages ? (md ? `\n---\n*${t("page_n", { n: i + 1 })}*\n\n` : `\n--- ${t("page_n", { n: i + 1 })} ---\n\n`) : "") + out.join("\n");
        });
        const text = chunks.join("\n\n").replace(/\n{3,}/g, "\n\n").trim() + "\n";
        const ext = md ? "md" : "txt";
        RT.showResult({
          blob: new Blob([text], { type: md ? "text/markdown;charset=utf-8" : "text/plain;charset=utf-8" }),
          filename: `${RT.baseName(file)}.${ext}`,
          note: t("txt_done", { n: pdf.numPages }),
          extra: el("pre", { class: "text-preview", text: text.slice(0, 700) + (text.length > 700 ? "…" : "") }),
        });
      } catch (e) {
        RT.fail(e);
      }
    }
  }

  RT.setDropHandler(open);
  RT.mount(RT.dropzone({ onFiles: open }));
});
