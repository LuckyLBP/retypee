"""HTML building blocks shared by every page."""
import html
import json
import hashlib
import re
from pathlib import Path

import registry as R
from names import blurb, short
from ui import FREE, PRIVACY, REVIEWS, SHELL

GITHUB = "https://github.com/LuckyLBP/retypee"
SITE_ID = R.BASE + "/#site"
ORG_ID = R.BASE + "/#org"

LIB_SCRIPTS = {
    "pdf-lib": "/vendor/pdf-lib.min.js",
    "fflate": "/vendor/fflate.min.js",
    "pdfjs": "/vendor/pdf.min.js",
    "tesseract": "/vendor/tesseract.min.js",
    "engine": "/tools/engine.js",
}


def esc(s):
    return html.escape(s, quote=True)


def plain(s):
    """Turn a snippet of trusted HTML into plain text (for JSON-LD)."""
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def mark(s):
    """*word* in a heading becomes the yellow highlighter."""
    return re.sub(r"\*(.+?)\*", r'<span class="mark">\1</span>', s)


def asset(name):
    """A stylesheet URL carrying a content hash, so a browser never pairs new markup with a cached old file."""
    digest = hashlib.sha1((Path(__file__).resolve().parents[2] / "web" / name).read_bytes()).hexdigest()[:8]
    return f"/{name}?v={digest}"


def other(lang):
    return "en" if lang == "sv" else "sv"


def switch_href(pid, lang):
    """Link to the same page in the other language. Going to Swedish adds ?lang=sv so the
    English-browser redirect does not bounce the visitor straight back."""
    target = other(lang)
    p = R.path(pid, target)
    return p + "?lang=sv" if target == "sv" else p


# ---------------------------------------------------------------- head

def og_image(lang):
    return f"{R.BASE}/og-image{'' if lang == 'sv' else '-en'}.png"


def breadcrumb_ld(pid, lang):
    items = [{"@type": "ListItem", "position": 1, "name": "Retypee", "item": R.url("home", lang)}]
    if pid != "home":
        if pid != "tools":
            items.append({"@type": "ListItem", "position": 2, "name": short("tools", lang), "item": R.url("tools", lang)})
        items.append({"@type": "ListItem", "position": len(items) + 1, "name": short(pid, lang), "item": R.url(pid, lang)})
    return {"@type": "BreadcrumbList", "@id": R.url(pid, lang) + "#crumbs", "itemListElement": items}


def json_ld(pid, lang, c):
    url = R.url(pid, lang)
    cur = "SEK" if lang == "sv" else "USD"
    graph = [
        {"@type": "Organization", "@id": ORG_ID, "name": "Retypee", "url": R.BASE + "/",
         "logo": {"@type": "ImageObject", "url": R.BASE + "/apple-touch-icon.png", "width": 180, "height": 180},
         "sameAs": [GITHUB]},
        {"@type": "WebSite", "@id": SITE_ID, "url": R.BASE + "/", "name": "Retypee", "inLanguage": ["sv", "en"], "publisher": {"@id": ORG_ID}},
    ]
    kind = R.kind(pid)
    if kind in ("editor", "tool"):
        app = {"@type": "WebApplication", "@id": url + "#app", "name": "Retypee" if pid == "home" else f"{short(pid, lang)} – Retypee",
               "url": url, "description": c["desc"], "inLanguage": lang,
               "applicationCategory": "UtilitiesApplication",
               "operatingSystem": "Valfri modern webbläsare" if lang == "sv" else "Any modern web browser",
               "isAccessibleForFree": True, "publisher": {"@id": ORG_ID}, "isPartOf": {"@id": SITE_ID},
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": cur}}
        if c.get("features"):
            app["featureList"] = c["features"]
        graph.append(app)
        faq = [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in c["faq"]]
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "inLanguage": lang, "mainEntity": faq})
    else:  # hub
        items = []
        for _cid, _label, ids in R.CATEGORIES:
            for i in ids:
                items.append({"@type": "ListItem", "position": len(items) + 1, "url": R.url(i, lang), "name": short(i, lang)})
        graph.append({"@type": "CollectionPage", "@id": url + "#page", "url": url, "name": c["h1"].replace("*", ""), "description": c["desc"],
                      "inLanguage": lang, "isPartOf": {"@id": SITE_ID},
                      "mainEntity": {"@type": "ItemList", "itemListElement": items}})
    if pid != "home":
        graph.append(breadcrumb_ld(pid, lang))
    return '  <script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2) + "\n  </script>\n"


def head(pid, lang, c):
    kind = R.kind(pid)
    url = R.url(pid, lang)
    og_desc = c.get("og_desc") or c["desc"]
    og_title = c.get("og_title") or c["title"].split(" | ")[0]
    img = og_image(lang)
    css = f'  <link rel="stylesheet" href="{asset("styles.css")}">\n' + ('' if kind == "editor" else f'  <link rel="stylesheet" href="{asset("tools.css")}">\n')
    return f'''<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(c["title"])}</title>
  <meta name="description" content="{esc(c["desc"])}">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="sv" href="{R.url(pid, "sv")}">
  <link rel="alternate" hreflang="en" href="{R.url(pid, "en")}">
  <link rel="alternate" hreflang="x-default" href="{R.url(pid, "sv")}">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#f6f5f1">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Retypee">
  <meta property="og:locale" content="{"sv_SE" if lang == "sv" else "en_US"}">
  <meta property="og:locale:alternate" content="{"en_US" if lang == "sv" else "sv_SE"}">
  <meta property="og:title" content="{esc(og_title)}">
  <meta property="og:description" content="{esc(og_desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{img}">

  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
{css}
{json_ld(pid, lang, c)}</head>
'''


# ---------------------------------------------------------------- header / menu / footer

# A 3x3 grid of dots: the tools menu button.
GRID_ICON = ('<svg class="grid-ic" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true" focusable="false" fill="currentColor">'
             + "".join(f'<circle cx="{4 + 6 * x}" cy="{4 + 6 * y}" r="1.55"/>' for y in range(3) for x in range(3))
             + '</svg>')
GLOBE_ICON = ('<svg class="globe-ic" width="17" height="17" viewBox="0 0 20 20" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" '
              'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="10" r="7.25"/>'
              '<path d="M2.75 10h14.5M10 2.75c2 2.1 3 4.5 3 7.25s-1 5.15-3 7.25c-2-2.1-3-4.5-3-7.25s1-5.15 3-7.25z"/></svg>')


CHECK_ICON = ('<svg viewBox="0 0 20 20" width="16" height="16" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" '
              'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m4.5 10.5 3.5 3.5 7.5-8"/></svg>')

# The GitHub mark (Octicons), linking the repository.
GITHUB_ICON = ('<svg class="gh-ic" width="20" height="20" viewBox="0 0 16 16" aria-hidden="true" focusable="false" fill="currentColor">'
               '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>')


def menu_html(lang):
    t = SHELL[lang]
    cols = []
    for _cid, label, ids in R.CATEGORIES:
        if _cid in R.MENU_HIDDEN:
            continue
        links = "".join(f'<a href="{R.path(i, lang)}">{svg_icon(i)}<span>{esc(short(i, lang))}</span></a>' for i in ids)
        cols.append(f'<div class="menu-col"><p class="menu-h">{esc(label[lang])}</p>{links}</div>')
    return (f'<details class="menu" id="menu"><summary title="{esc(t["menu"])}" aria-label="{esc(t["menu"])}">{GRID_ICON}</summary>'
            f'<div class="menu-panel">{"".join(cols)}'
            f'<a class="menu-all" href="{R.path("tools", lang)}">{esc(t["all_tools"])}<span aria-hidden="true">→</span></a></div></details>')


def brand(pid, lang, with_file_name):
    fn = '\n      <span class="file-name" id="fileName"></span>' if with_file_name else ""
    return f'''    <div class="brand">
      <a class="brand-link" href="{R.path("home", lang)}"><img class="wordmark" src="/wordmark.svg" alt="Retypee" width="103" height="26"></a>
      {fn}
    </div>'''


def lang_link(pid, lang):
    t = SHELL[lang]
    o = other(lang)
    return f'<a class="lang" href="{switch_href(pid, lang)}" hreflang="{o}" lang="{o}" title="{esc(t["lang_title"])}">{GLOBE_ICON}<span>{esc(t["lang_name"])}</span></a>'


ICONS = {
    "rail": '<path d="M4 5.5A1.5 1.5 0 0 1 5.5 4h9A1.5 1.5 0 0 1 16 5.5v9a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 4 14.5zM8.5 4v12"/>',
    "edit": '<path d="M7 4h6M10 4v12M7 16h6"/>',
    "add": '<path d="M3.5 5h9M8 5v9M13.5 14h4M15.5 12v4"/>',
    "search": '<circle cx="9" cy="9" r="4.8"/><path d="m12.6 12.6 4 4"/>',
    "undo": '<path d="M7.5 4 4 7.5 7.5 11M4.5 7.5h7a4.5 4.5 0 0 1 0 9H9"/>',
    "redo": '<path d="M12.5 4 16 7.5 12.5 11M15.5 7.5h-7a4.5 4.5 0 0 0 0 9H11"/>',
    "minus": '<path d="M5 10h10"/>',
    "plus": '<path d="M5 10h10M10 5v10"/>',
    "fit": '<path d="M3.5 10h13M6.5 7 3.5 10l3 3M13.5 7l3 3-3 3"/>',
    "prev": '<path d="m12 5-5 5 5 5"/>',
    "next": '<path d="m8 5 5 5-5 5"/>',
    "font": '<path d="M2.5 16 7 4.5 11.5 16M4.2 12.2h5.6M13.5 16l2.5-6 2.5 6M14.4 14h3.2"/>',
    "open": '<path d="M3.5 7V5.5A1.5 1.5 0 0 1 5 4h3l1.5 2H15A1.5 1.5 0 0 1 16.5 7.5v7A1.5 1.5 0 0 1 15 16H5a1.5 1.5 0 0 1-1.5-1.5z"/>',
    "download": '<path d="M10 3.5v9M6.5 9.5 10 13l3.5-3.5M4 16.5h12"/>',
    "close": '<path d="m5.5 5.5 9 9m0-9-9 9"/>',
}


def icon(name):
    return f'<svg viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'


def header_editor(pid, lang):
    t = SHELL[lang]
    return f'''  <header class="bar">
{brand(pid, lang, True)}
    <div class="actions">
      <label class="tool" id="openBtn" hidden>{icon("open")}<span>{esc(t["open_another"])}</span>
        <input type="file" accept="application/pdf,.pdf" id="openInput" class="file-input">
      </label>
      <button class="primary" id="downloadBtn" hidden>{icon("download")}<span>{esc(t["download"])}</span></button>
      <span class="sep bar-sep" aria-hidden="true"></span>
      {lang_link(pid, lang)}
      {menu_html(lang)}
    </div>
  </header>
'''


def toolbar(lang):
    """The floating pill above the document: tools, undo, zoom and page navigation."""
    t = SHELL[lang]
    return f'''      <div class="toolbar-wrap">
        <div class="tools" id="tools" role="toolbar" aria-label="{esc(t["tool_group"])}" hidden>
          <button class="icon" id="railBtn" aria-pressed="true" title="{esc(t["rail_toggle"])}" aria-label="{esc(t["rail_toggle"])}">{icon("rail")}</button>
          <span class="sep" aria-hidden="true"></span>
          <div class="segmented" role="radiogroup" aria-label="{esc(t["tool_group"])}">
            <button class="seg" role="radio" aria-checked="true" data-mode="edit" title="{esc(t["edit_title"])}">{icon("edit")}<span class="label">{esc(t["edit_text"])}</span></button>
            <button class="seg" role="radio" aria-checked="false" data-mode="add" title="{esc(t["add_title"])}">{icon("add")}<span class="label">{esc(t["add_text"])}</span></button>
          </div>
          <button class="tool" id="findBtn" title="{esc(t["find_title"])}">{icon("search")}<span class="label">{esc(t["find"])}</span></button>
          <label class="icon" id="fontBtn" title="{esc(t["add_font_title"])}">{icon("font")}<span class="sr-only">{esc(t["add_font"])}</span>
            <input type="file" accept=".ttf,.otf,.ttc,font/ttf,font/otf" id="fontInput" class="file-input">
          </label>
          <span class="sep" aria-hidden="true"></span>
          <button class="icon" id="undoBtn" title="{esc(t["undo_title"])}" aria-label="{esc(t["undo"])}" disabled>{icon("undo")}</button>
          <button class="icon" id="redoBtn" title="{esc(t["redo_title"])}" aria-label="{esc(t["redo"])}" disabled>{icon("redo")}</button>
          <span class="sep sep-zoom" aria-hidden="true"></span>
          <div class="zoom">
            <button class="icon" id="zoomOut" aria-label="{esc(t["zoom_out"])}">{icon("minus")}</button>
            <span id="zoomLabel" class="zoom-label">100%</span>
            <button class="icon" id="zoomIn" aria-label="{esc(t["zoom_in"])}">{icon("plus")}</button>
            <button class="icon" id="zoomFit" title="{esc(t["fit_width"])}" aria-label="{esc(t["fit_width"])}">{icon("fit")}</button>
          </div>
          <span class="sep sep-pager" aria-hidden="true"></span>
          <div class="pager">
            <button class="icon" id="prevPage" title="{esc(t["prev_page"])}" aria-label="{esc(t["prev_page"])}">{icon("prev")}</button>
            <span id="pageLabel" class="page-label" aria-live="polite"></span>
            <button class="icon" id="nextPage" title="{esc(t["next_page"])}" aria-label="{esc(t["next_page"])}">{icon("next")}</button>
          </div>
        </div>
      </div>
'''


def rail(lang):
    t = SHELL[lang]
    return f'''    <aside class="rail" id="rail" aria-label="{esc(t["rail_title"])}" hidden>
      <div class="rail-list" id="railList"></div>
    </aside>
'''


def header_plain(pid, lang):
    return f'''  <header class="bar">
{brand(pid, lang, False)}
    <div class="actions">
      {lang_link(pid, lang)}
      {menu_html(lang)}
    </div>
  </header>
'''


FOOT_LINKS = ["merge", "split", "compress", "sign", "change-text"]


def footer(pid, lang):
    t = SHELL[lang]
    links = "".join(f'<a href="{R.path(i, lang)}">{esc(short(i, lang))}</a>' for i in FOOT_LINKS)
    return f'''        <footer class="site-foot">
          <div class="foot-top">
            <div class="foot-brand">
              <a href="{R.path("home", lang)}"><img class="wordmark" src="/wordmark.svg" alt="Retypee" width="83" height="21"></a>
              <p>{esc(t["footer_tag"])}</p>
            </div>
            <a class="badge" href="https://pohlare.com" rel="noopener"><img src="/pohlare.png" alt="" width="44" height="44"><span><small>{esc(t["made_by"])}</small><strong>{esc(t["made_by_name"])}</strong></span></a>
          </div>
          <nav class="foot-links" aria-label="{esc(t["menu"])}">{links}<a class="all" href="{R.path("tools", lang)}">{esc(t["all_tools_link"])} →</a></nav>
          <div class="foot-line">
            <span>{esc(t["free_open"])}</span>
            <div class="foot-actions">
              <a class="gh" href="{GITHUB}" rel="noopener" title="GitHub" aria-label="{esc(t["source"])} (GitHub)">{GITHUB_ICON}</a>
              {lang_link(pid, lang)}
            </div>
          </div>
        </footer>
'''


# ---------------------------------------------------------------- body pieces

def sections_html(sections):
    out = []
    for s in sections:
        parts = [f'          <h2>{s["h2"]}</h2>']
        for p in s.get("p", []):
            parts.append(f"          <p>{p}</p>")
        if s.get("ul"):
            parts.append("          <ul>" + "".join(f"\n            <li>{li}</li>" for li in s["ul"]) + "\n          </ul>")
        out.append("        <section>\n" + "\n".join(parts) + "\n        </section>\n")
    return "\n".join(out)


def steps_html(c):
    lis = "".join(f"\n            <li><strong>{a}</strong><p>{b}</p></li>" for a, b in c["steps"])
    return f'''        <section>
          <h2>{c["steps_h2"]}</h2>
          <ol class="steps">{lis}
          </ol>
        </section>
'''


def faq_html(c):
    items = "".join(f"""
          <details>
            <summary>{q}</summary>
            <p>{a}</p>
          </details>""" for q, a in c["faq"])
    return f'''        <section class="faq">
          <h2>{c["faq_h2"]}</h2>{items}
        </section>
'''


def free_row(lang):
    """The three promises as a row of yellow ticks, shown right under the drop zone."""
    items = "".join(f"<li>{CHECK_ICON}{esc(c)}</li>" for c in FREE[lang]["chips"])
    return f'<ul class="free-row">{items}</ul>'


def free_html(lang):
    f = FREE[lang]
    chips = "".join(f"<li>{CHECK_ICON}{esc(c)}</li>" for c in f["chips"])
    return f'''        <section class="free">
          <h2>{f["h2"]}</h2>
          <p>{f["p"]}</p>
          <ul class="chips">{chips}</ul>
        </section>
'''


def reviews_html(pid, lang):
    r = REVIEWS[lang]
    stars_input = "".join(f'<input type="radio" class="sr-only" name="stars" id="rv-s{n}" value="{n}"><label for="rv-s{n}" title="{esc(r["star"].format(n=n))}"><span class="sr-only">{esc(r["star"].format(n=n))}</span>★</label>' for n in (5, 4, 3, 2, 1))
    bars = "".join(f'<li><span class="rv-bar-track"><span class="rv-bar-fill" id="rvBar{n}"></span></span><span class="rv-bar-label">{n}.0 ★</span></li>' for n in (5, 4, 3, 2, 1))
    strings = json.dumps({**r, "tool": pid, "lang": lang}, ensure_ascii=False)
    return f'''        <section class="reviews" id="reviews" data-tool="{pid}">
          <h2>{esc(r["h2"])}</h2>
          <p class="rv-none" id="rvNone" hidden>{esc(r["none"])}</p>
          <div class="rv-summary" id="rvSummary" hidden>
            <div class="rv-score">
              <span class="rv-avg" id="rvAvg"></span>
              <div class="rv-score-side">
                <span class="rv-stars-out" id="rvStarsOut" role="img"></span>
                <p class="rv-count" id="rvCount"></p>
              </div>
            </div>
            <ul class="rv-bars" id="rvBars">{bars}</ul>
          </div>
          <button type="button" class="rv-toggle" id="rvToggle" aria-expanded="false" aria-controls="rvForm">{esc(r["form_h"])}</button>
          <form class="rv-form" id="rvForm" novalidate hidden>
            <fieldset class="rv-stars"><legend>{esc(r["stars"])}</legend>{stars_input}</fieldset>
            <label class="field"><span>{esc(r["name"])}</span><input type="text" name="name" maxlength="40" autocomplete="off"></label>
            <input class="rv-trap" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
            <div class="rv-actions"><button class="primary" type="submit">{esc(r["submit"])}</button><p class="rv-msg" id="rvMsg" role="status" aria-live="polite"></p></div>
            <p class="note">{esc(r["note"])}</p>
          </form>
          <script type="application/json" id="rv-strings">{strings}</script>
        </section>
'''


def privacy_html(lang):
    p = PRIVACY[lang]
    return f'''        <section>
          <h2>{p["h2"]}</h2>
          <p>{p["p"]}</p>
        </section>
'''


def svg_icon(pid, cls="ic"):
    """A tool's icon from the sprite (web/icons.svg); decorative, so hidden from assistive tech."""
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="/icons.svg#i-{pid}"/></svg>'


def card_html(i, lang, indent):
    return (f'\n{indent}<a class="card" href="{R.path(i, lang)}"><span class="card-ic">{svg_icon(i)}</span>'
            f'<strong>{esc(short(i, lang))}</strong><span>{esc(blurb(i, lang))}</span></a>')


def related_html(pid, lang, ids):
    t = SHELL[lang]
    cards = "".join(card_html(i, lang, "            ") for i in ids if i != pid)
    return f'''        <section class="related">
          <h2>{esc(t["related"])}</h2>
          <p>{esc(t["related_lead"])}</p>
          <div class="cards">{cards}
          </div>
        </section>
'''


def crumbs_html(pid, lang):
    t = SHELL[lang]
    mid = "" if pid == "tools" else f'<a href="{R.path("tools", lang)}">{esc(short("tools", lang))}</a><span aria-hidden="true">›</span>'
    return (f'<nav class="crumbs" aria-label="{esc(t["crumbs"])}"><a href="{R.path("home", lang)}">{esc(t["home_crumb"])}</a>'
            f'<span aria-hidden="true">›</span>{mid}<span aria-current="page">{esc(short(pid, lang))}</span></nav>')
