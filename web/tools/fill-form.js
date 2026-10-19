"use strict";

/* Fill in a PDF form: the fields are laid over the page as real inputs, and written back
   with pdf-lib. Optionally the result is flattened so the answers can no longer be changed. */
RT.run(function start() {
  const { t, el } = RT;

  RT.pdfFlow(async ({ file, bytes, doc, pdf, count }) => {
    let form, fields;
    try {
      form = doc.getForm();
      fields = form.getFields();
    } catch (e) {
      throw RT.friendly(e);
    }
    const kindOf = (f) =>
      f instanceof PDFLib.PDFTextField ? "text" :
      f instanceof PDFLib.PDFCheckBox ? "check" :
      f instanceof PDFLib.PDFRadioGroup ? "radio" :
      f instanceof PDFLib.PDFDropdown ? "drop" :
      f instanceof PDFLib.PDFOptionList ? "drop" : null;
    const usable = fields.filter((f) => kindOf(f));
    if (!usable.length) return RT.mount(RT.message(t("ff_none"), "info"), RT.actionsRow(RT.restartButton()));

    // which page each widget sits on (the page's own annotation list is the reliable source)
    const pageOf = new Map();
    doc.getPages().forEach((p, i) => {
      const annots = p.node.Annots();
      for (let j = 0; annots && j < annots.size(); j++) pageOf.set(String(annots.get(j)), i);
    });

    const states = usable.map((field) => {
      const kind = kindOf(field);
      const st = { field, kind, readOnly: field.isReadOnly(), inputs: [], value: "" };
      if (kind === "text") st.value = field.getText() || "";
      else if (kind === "check") st.value = field.isChecked();
      else if (kind === "radio") st.value = field.getSelected() || "";
      else st.value = field.getSelected()[0] || "";
      if (kind === "drop") st.options = field.getOptions();
      const options = kind === "radio" ? field.getOptions() : [];
      st.widgets = field.acroField.getWidgets().map((w, i) => ({
        rect: w.getRectangle(),
        page: pageOf.get(String(doc.context.getObjectRef(w.dict))),
        on: kind === "radio" ? options[i] ?? (w.getOnValue() ? w.getOnValue().decodeText() : null) : null, // widget i is option i
      }));
      return st;
    });
    const set = (st, v, from) => {
      st.value = v;
      for (const input of st.inputs) if (input !== from) input.sync();
    };

    function control(st, w, box) {
      const label = String(st.field.getName()).replace(/[._]+/g, " ");
      const common = { "aria-label": label, title: label };
      let input;
      if (st.kind === "text") {
        const multi = st.field.isMultiline();
        input = el(multi ? "textarea" : "input", { ...common, class: "ff-input", ...(multi ? {} : { type: st.field.isPassword() ? "password" : "text" }), autocomplete: "off", spellcheck: "false" });
        const max = st.field.getMaxLength();
        if (max) input.maxLength = max;
        input.style.fontSize = multi ? "13px" : `${Math.max(11, Math.min(16, box.h * 0.6))}px`;
        input.addEventListener("input", () => set(st, input.value, input));
        input.sync = () => (input.value = st.value);
      } else if (st.kind === "check" || st.kind === "radio") {
        const radio = st.kind === "radio";
        input = el("input", { ...common, type: radio ? "radio" : "checkbox", class: "ff-input ff-tick" });
        input.addEventListener("change", () => set(st, radio ? w.on : input.checked, input));
        input.sync = () => (input.checked = radio ? st.value === w.on : st.value === true);
        const s = Math.min(box.w, box.h);
        box = { x: box.x + (box.w - s) / 2, y: box.y + (box.h - s) / 2, w: s, h: s };
        if (radio && w.on) input.title = `${label}: ${w.on}`;
      } else {
        const opts = st.options.includes(st.value) || !st.value ? st.options : [...st.options, st.value];
        input = el("select", { ...common, class: "ff-input" }, el("option", { value: "", text: "" }), opts.map((o) => el("option", { value: o, text: o })));
        input.style.fontSize = `${Math.max(11, Math.min(15, box.h * 0.6))}px`;
        input.addEventListener("change", () => set(st, input.value, input));
        input.sync = () => (input.value = st.value);
      }
      if (st.readOnly) input.disabled = true;
      input.style.cssText += `;left:${box.x}px;top:${box.y}px;width:${box.w}px;height:${box.h}px`;
      input.sync();
      st.inputs.push(input);
      return input;
    }

    const byPage = new Map();
    for (const st of states) for (const w of st.widgets) if (w.page != null) (byPage.get(w.page) || byPage.set(w.page, []).get(w.page)).push([st, w]);
    const unplaced = states.filter((st) => st.widgets.every((w) => w.page == null));

    const pages = el("div", { class: "ff-pages" });
    for (const idx of [...byPage.keys()].sort((a, b) => a - b)) {
      const stage = await RT.previewStage(pdf, idx + 1, 680);
      const sp = RT.pageSpace(doc.getPage(idx));
      for (const [st, w] of byPage.get(idx)) {
        const a = sp.unmap(w.rect.x, w.rect.y), b = sp.unmap(w.rect.x + w.rect.width, w.rect.y + w.rect.height);
        const k = stage.scale;
        stage.el.append(control(st, w, { x: Math.min(a.x, b.x) * k, y: (sp.vh - Math.max(a.y, b.y)) * k, w: Math.abs(b.x - a.x) * k, h: Math.abs(b.y - a.y) * k }));
      }
      pages.append(el("figure", { class: "ff-page" }, stage.el, count > 1 ? el("figcaption", { class: "hint", text: t("ff_page", { n: idx + 1 }) }) : null));
    }

    const flatten = el("input", { type: "checkbox" });
    const go = el("button", { class: "primary big", type: "button", onclick: save, text: t("ff_btn") });
    RT.mount(
      RT.fileCard({ file, count, bytes }),
      el("p", { class: "hint", text: t("ff_hint", { n: states.length }) }),
      unplaced.length ? RT.message(t("ff_unplaced", { n: unplaced.length }), "info") : null,
      pages,
      el("label", { class: "check" }, flatten, el("span", { text: t("ff_flatten") })),
      RT.actionsRow(go, RT.restartButton())
    );

    const problem = (e) => RT.fail(/winansi|encode/i.test(e.message) ? new Error(t("ff_chars")) : e);

    function save() {
      RT.mount(RT.busy());
      try {
        for (const st of states) {
          if (st.readOnly) continue;
          const f = st.field;
          if (st.kind === "text") f.setText(st.value || undefined);
          else if (st.kind === "check") st.value ? f.check() : f.uncheck();
          else if (st.value) f.select(st.value);
          else f.clear();
        }
        if (flatten.checked) {
          form.flatten();
          // flatten() leaves references to the deleted widgets in each page's annotation list
          for (const page of doc.getPages()) {
            const annots = page.node.Annots();
            for (let i = (annots ? annots.size() : 0) - 1; i >= 0; i--) if (!doc.context.lookup(annots.get(i))) annots.remove(i);
          }
        }
        doc.save().then((out) =>
          RT.showResult({ blob: RT.saveBlob(out, "application/pdf"), filename: `${RT.baseName(file)}-${t("out_suffix")}.pdf`, note: t(flatten.checked ? "ff_done_flat" : "ff_done") })
        ).catch(problem);
      } catch (e) {
        problem(e);
      }
    }
  });
});
