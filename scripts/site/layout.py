"""HTML building blocks shared by every page."""
import html
import json
import re

import registry as R
from names import blurb, short
from ui import PRIVACY, SHELL

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
               "applicationCategory": "BusinessApplication",
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
    css = '  <link rel="stylesheet" href="/styles.css">\n' + ('' if kind == "editor" else '  <link rel="stylesheet" href="/tools.css">\n')
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

def menu_html(lang):
    t = SHELL[lang]
    cols = []
    for _cid, label, ids in R.CATEGORIES:
        if _cid in R.MENU_HIDDEN:
            continue
        links = "".join(f'<a href="{R.path(i, lang)}">{esc(short(i, lang))}</a>' for i in ids)
        cols.append(f'<div class="menu-col"><p class="menu-h">{esc(label[lang])}</p>{links}</div>')
    return (f'<details class="menu" id="menu"><summary>{esc(t["menu"])}</summary>'
            f'<div class="menu-panel">{"".join(cols)}'
            f'<a class="menu-all" href="{R.path("tools", lang)}">{esc(t["all_tools"])} →</a></div></details>')


def brand(pid, lang, with_file_name):
    fn = '\n      <span class="file-name" id="fileName"></span>' if with_file_name else ""
    return f'''    <div class="brand">
      <a class="brand-link" href="{R.path("home", lang)}"><img class="wordmark" src="/wordmark.svg" alt="Retypee" width="103" height="26"></a>
      {menu_html(lang)}{fn}
    </div>'''


def lang_link(pid, lang):
    t = SHELL[lang]
    o = other(lang)
    return f'<a class="lang" href="{switch_href(pid, lang)}" hreflang="{o}" lang="{o}" title="{esc(t["lang_title"])}">{esc(t["lang_name"])}</a>'


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
    "close": '<path d="m5.5 5.5 9 9m0-9-9 9"/>',
}


def icon(name):
    return f'<svg viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'


def header_editor(pid, lang):
    t = SHELL[lang]
    return f'''  <header class="bar">
{brand(pid, lang, True)}
    <div class="actions">
      {lang_link(pid, lang)}
      <label class="tool" id="fontBtn" title="{esc(t["add_font_title"])}">{esc(t["add_font"])}
        <input type="file" accept=".ttf,.otf,.ttc,font/ttf,font/otf" id="fontInput" class="file-input">
      </label>
      <label class="tool" id="openBtn" hidden>{esc(t["open_another"])}
        <input type="file" accept="application/pdf,.pdf" id="openInput" class="file-input">
      </label>
      <button class="primary" id="downloadBtn" hidden>{esc(t["download"])}</button>
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
    </div>
  </header>
'''


def footer(pid, lang):
    t = SHELL[lang]
    cols = []
    for _cid, label, ids in R.CATEGORIES:
        lis = "".join(f'<li><a href="{R.path(i, lang)}">{esc(short(i, lang))}</a></li>' for i in ids)
        cols.append(f'<div class="foot-col"><p class="foot-h">{esc(label[lang])}</p><ul>{lis}</ul></div>')
    return f'''        <footer class="site-foot">
          <div class="foot-top">
            <div class="foot-brand">
              <a href="{R.path("home", lang)}"><img class="wordmark" src="/wordmark.svg" alt="Retypee" width="83" height="21"></a>
              <p>{esc(t["footer_tag"])}</p>
            </div>
            <nav class="foot-cols" aria-label="{esc(t["menu"])}">{"".join(cols)}</nav>
          </div>
          <div class="foot-line">
            <span>{esc(t["free_open"])}</span>
            <a href="{GITHUB}">{esc(t["source"])}</a>
            {lang_link(pid, lang)}
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


def privacy_html(lang):
    p = PRIVACY[lang]
    return f'''        <section>
          <h2>{p["h2"]}</h2>
          <p>{p["p"]}</p>
        </section>
'''


def related_html(pid, lang, ids):
    t = SHELL[lang]
    cards = "".join(
        f'\n            <a class="card" href="{R.path(i, lang)}"><strong>{esc(short(i, lang))}</strong><span>{esc(blurb(i, lang))}</span></a>'
        for i in ids if i != pid)
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
