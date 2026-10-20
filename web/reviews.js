"use strict";

/* Shows a rating summary (average, star breakdown bars, count) for this tool and sends new
   reviews to /api/reviews (stored as pending until approved, unless 3+ stars auto-approves them).
   Everything the visitor wrote is inserted as text, never as HTML. No reviewer names are displayed. */
(() => {
  const root = document.getElementById("reviews");
  if (!root) return;
  const T = JSON.parse(document.getElementById("rv-strings").textContent);
  const $ = (id) => document.getElementById(id);
  const none = $("rvNone"), summary = $("rvSummary"), avg = $("rvAvg"), starsOut = $("rvStarsOut"), count = $("rvCount");
  const toggle = $("rvToggle"), form = $("rvForm"), msg = $("rvMsg");
  const API = "/api/reviews/";
  const fmt = (s, v) => s.replace(/\{(\w+)\}/g, (_, k) => v[k]);
  let touched = 0;

  const stars = (n) => "★".repeat(n) + "☆".repeat(5 - n);

  /* A trailing "+" must stay a floor (never claim more reviews than really exist), so round down. */
  const displayCount = (n) => (n < 10 ? String(n) : `${Math.floor(n / 10) * 10}+`);

  function render(data) {
    if (!data.count) {
      none.hidden = false;
      summary.hidden = true;
      return;
    }
    none.hidden = true;
    summary.hidden = false;
    avg.textContent = data.average;
    const rounded = Math.round(data.average);
    starsOut.textContent = stars(rounded);
    starsOut.setAttribute("aria-label", fmt(T.star, { n: rounded }));
    count.textContent = data.count === 1 ? T.count_label_1 : fmt(T.count_label, { n: displayCount(data.count) });

    const counts = data.counts || {};
    const max = Math.max(1, ...Object.values(counts));
    for (const n of [5, 4, 3, 2, 1]) {
      const bar = $(`rvBar${n}`);
      if (bar) bar.style.width = `${Math.round(((counts[n] || 0) / max) * 100)}%`;
    }
    addRatingMarkup(data);
  }

  /* Rating markup for search engines, only when there are real approved reviews to base it on. */
  function addRatingMarkup(data) {
    if (data.count < 3 || document.getElementById("rv-ld")) return;
    const h1 = document.querySelector("h1");
    const ld = document.createElement("script");
    ld.type = "application/ld+json";
    ld.id = "rv-ld";
    ld.textContent = JSON.stringify({
      "@context": "https://schema.org", "@type": "WebApplication", name: (h1 ? h1.textContent : document.title).trim().replace(/[.\s]+$/, ""),
      url: location.origin + location.pathname, applicationCategory: "UtilitiesApplication", operatingSystem: "Any",
      offers: { "@type": "Offer", price: "0", priceCurrency: T.lang === "sv" ? "SEK" : "USD" },
      aggregateRating: { "@type": "AggregateRating", ratingValue: data.average, ratingCount: data.count, bestRating: 5, worstRating: 1 },
    });
    document.head.append(ld);
  }

  async function load() {
    try {
      const res = await fetch(`${API}?tool=${encodeURIComponent(T.tool)}`);
      if (!res.ok) throw new Error(res.status);
      render(await res.json());
    } catch {
      none.hidden = false;
      summary.hidden = true;
    }
  }

  toggle.addEventListener("click", () => {
    const show = form.hidden;
    form.hidden = !show;
    toggle.setAttribute("aria-expanded", String(show));
    if (show) form.querySelector('input[name="stars"]')?.focus();
  });

  form.addEventListener("focusin", () => { if (!touched) touched = Date.now(); });
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const f = new FormData(form);
    const n = Number(f.get("stars"));
    msg.classList.remove("error");
    const fail = (text) => { msg.textContent = text; msg.classList.add("error"); };
    if (!n) return fail(T.need_stars);
    const btn = form.querySelector("button[type=submit]");
    btn.disabled = true;
    msg.textContent = T.sending;
    try {
      const res = await fetch(API, {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ tool: T.tool, lang: T.lang, stars: n, name: f.get("name"), website: f.get("website"), fillMs: touched ? Date.now() - touched : 0 }),
      });
      if (!res.ok) throw new Error(res.status);
      form.reset();
      touched = 0;
      msg.textContent = T.thanks;
    } catch {
      fail(T.error);
    } finally {
      btn.disabled = false;
    }
  });

  load();
})();
