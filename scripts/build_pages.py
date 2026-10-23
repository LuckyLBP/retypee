#!/usr/bin/env python3
"""Build the static pages in web/ from scripts/site/.

    python3 scripts/build_pages.py            write pages, sitemap.xml and the redirects in vercel.json
    python3 scripts/build_pages.py --check    exit 1 if anything on disk is out of date

Output is plain HTML that is committed, so Vercel needs no build step.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WEB = os.path.join(ROOT, "web")
sys.path.insert(0, os.path.join(HERE, "site"))

import layout as L          # noqa: E402
import registry as R        # noqa: E402
from content import CONTENT  # noqa: E402
from names import blurb, short  # noqa: E402
from ui import SHELL, TOOL_UI  # noqa: E402

LANGS = ("sv", "en")


def out_path(pid, lang):
    parts = [WEB] + (["en"] if lang == "en" else []) + ([R.slug(pid, lang)] if R.slug(pid, lang) else []) + ["index.html"]
    return os.path.join(*parts)


# ---------------------------------------------------------------- page bodies

def hero(c, extra=""):
    return f'''      <div class="hero">
        <h1>{L.mark(c["h1"])}</h1>
        <p class="lede">{c["lede"]}</p>
{extra}      </div>
'''


def drop_block(lang):
    t = SHELL[lang]
    return f'''
        <label class="drop" id="drop">
          <strong>{t["drop_title"]}</strong>
          <span class="drop-hint">{t["drop_hint"]}</span>
          <span class="primary as-button">{t["choose"]}</span>
          <input type="file" accept="application/pdf,.pdf" id="fileInput" class="file-input">
        </label>
        {L.free_row(lang)}
        <p class="engine-status idle" id="engineStatus" role="status" aria-live="polite">{t["status_idle"]}</p>
'''


def editor_page(pid, lang, c):
    t = SHELL[lang]
    info = [L.steps_html(c), L.sections_html(c["sections"]), L.free_html(lang), L.reviews_html(pid, lang), L.related_html(pid, lang, c.get("related", [])),
            L.faq_html(c), L.footer(pid, lang)]
    return f'''<!doctype html>
<html lang="{lang}">
{L.head(pid, lang, c)}<body>
{L.header_editor(pid, lang)}
  <div class="workspace" id="workspace">
{L.rail(lang)}    <main class="desk" id="desk">
{L.toolbar(lang)}
    <section class="empty" id="empty">
{hero(c, drop_block(lang))}
      <div class="info">
{chr(10).join(info)}      </div>
    </section>

    <div class="pages" id="pages" hidden></div>
    </main>
  </div>

  <aside class="drawer" id="drawer" aria-labelledby="drawerTitle" hidden>
    <div class="drawer-head">
      <h2 id="drawerTitle">{t["drawer_title"]}</h2>
      <button class="icon" id="drawerClose" aria-label="{t["close"]}">{L.icon("close")}</button>
    </div>
    <form id="replaceForm" class="drawer-body" autocomplete="off">
      <label class="field">
        <span>{t["find_label"]}</span>
        <input id="findInput" type="text" spellcheck="false">
      </label>
      <label class="field">
        <span>{t["replace_label"]}</span>
        <input id="replaceInput" type="text" spellcheck="false">
      </label>
      <div class="checks">
        <label><input type="checkbox" id="caseCheck"> {t["case"]}</label>
        <label><input type="checkbox" id="wordCheck"> {t["word"]}</label>
        <label><input type="checkbox" id="fitCheck"> {t["fit"]}</label>
      </div>
      <p class="match-count" id="matchCount" aria-live="polite">{t["find_hint"]}</p>
      <button class="primary wide" id="replaceAllBtn" type="submit" disabled>{t["replace_all"]}</button>
      <p class="note">{t["drawer_note"]}</p>
    </form>
  </aside>

  <div class="toast" id="toast" role="status" aria-live="polite" hidden></div>
  <div class="busy" id="busy" hidden><span></span></div>

  <script src="/site.js" defer></script>
  <script src="/reviews.js" defer></script>
  <script src="/app.js"></script>
</body>
</html>
'''


def tool_page(pid, lang, c):
    t = SHELL[lang]
    # The big libraries (pdf-lib, pdf.js, fflate) load when the visitor shows intent, not with the page.
    heavy = [L.LIB_SCRIPTS[x] for x in R.libs(pid) if x != "engine"]
    strings = {**TOOL_UI[lang], **c.get("ui", {}), "lang": lang, "libs": heavy,
               "next": [{"href": R.path(i, lang), "label": L.short(i, lang)} for i in c.get("related", []) if i != pid][:3]}
    libs = "".join(f'  <script src="{L.LIB_SCRIPTS[x]}" defer></script>\n' for x in R.libs(pid) if x == "engine")
    info = [L.steps_html(c), L.sections_html(c["sections"]), L.free_html(lang), L.reviews_html(pid, lang), L.privacy_html(lang),
            L.related_html(pid, lang, c.get("related", [])), L.faq_html(c), L.footer(pid, lang)]
    return f'''<!doctype html>
<html lang="{lang}">
{L.head(pid, lang, c)}<body class="tool-page">
{L.header_plain(pid, lang)}
  <main id="main">
    <div class="hero compact">
      {L.crumbs_html(pid, lang)}
      <span class="page-ic" {L.tape_vars(pid)}>{L.svg_icon(pid)}</span>
      <h1>{L.mark(c["h1"])}</h1>
      <p class="lede">{c["lede"]}</p>
    </div>

    <section class="workbench" id="workbench" aria-live="polite" data-tool="{pid}">
      <noscript><p class="noscript">{t["noscript"]}</p></noscript>
    </section>
    {L.free_row(lang)}

    <div class="info">
{chr(10).join(info)}    </div>
  </main>

  <script type="application/json" id="rt-strings">{json.dumps(strings, ensure_ascii=False)}</script>
  <script src="/site.js" defer></script>
  <script src="/reviews.js" defer></script>
{libs}  <script src="/tools/common.js" defer></script>
  <script src="/tools/{R.script(pid)}.js" defer></script>
</body>
</html>
'''


def hub_page(pid, lang, c):
    t = SHELL[lang]
    groups = []
    for _cid, label, ids in R.CATEGORIES:
        cards = "".join(L.card_html(i, lang, "          ") for i in ids)
        groups.append(f'''        <section>
          <h2>{L.esc(label[lang])}</h2>
          <div class="cards">{cards}
          </div>
        </section>
''')
    return f'''<!doctype html>
<html lang="{lang}">
{L.head(pid, lang, c)}<body class="tool-page">
{L.header_plain(pid, lang)}
  <main id="main">
    <div class="hero compact">
      {L.crumbs_html(pid, lang)}
      <span class="page-ic" {L.tape_vars(pid)}>{L.svg_icon(pid)}</span>
      <h1>{L.mark(c["h1"])}</h1>
      <p class="lede">{c["lede"]}</p>
      {L.free_row(lang)}
    </div>

    <div class="info">
{chr(10).join(groups)}
{L.free_html(lang)}
{L.privacy_html(lang)}
{L.footer(pid, lang)}    </div>
  </main>

  <script src="/site.js" defer></script>
</body>
</html>
'''


def resolve(value, lang):
    """Replace {{link:page-id}} in any string of the copy with a real link to that page."""
    if isinstance(value, str):
        return re.sub(r"\{\{link:([a-z-]+)\}\}", lambda m: f'<a href="{R.path(m.group(1), lang)}">{L.short(m.group(1), lang)}</a>', value)
    if isinstance(value, dict):
        return {k: resolve(v, lang) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return type(value)(resolve(v, lang) for v in value)
    return value


RENDER = {"editor": editor_page, "tool": tool_page, "hub": hub_page}


# ---------------------------------------------------------------- sitemap and redirects

def sitemap(ids):
    urls = []
    for pid in ids:
        for lang in LANGS:
            alts = "".join(
                f'\n    <xhtml:link rel="alternate" hreflang="{a}" href="{R.url(pid, a)}"/>' for a in LANGS
            ) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{R.url(pid, "sv")}"/>'
            prio = "1.0" if (pid == "home" and lang == "sv") else ("0.8" if pid in ("home", "tools") else "0.6")
            urls.append(f"  <url>\n    <loc>{R.url(pid, lang)}</loc>{alts}\n    <lastmod>{R.LASTMOD}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{prio}</priority>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<?xml-stylesheet type="text/xsl" href="/sitemap.xsl"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")


def llms_txt(ids):
    """A plain-English index of the site for LLMs (https://llmstxt.org), in the one canonical
    language the convention expects. Built from the same tool list as the sitemap and the menu,
    so it can't drift out of sync with what the site actually has."""
    home = CONTENT["home"]["en"]
    lines = ["# Retypee", "", f"> {home['desc']}", "",
              "Every tool runs client-side in the browser (WebAssembly); no file is ever uploaded to a server. "
              "Free, with no account, no credit card and no usage limit. Open source (AGPL-3.0)."]
    for _cid, label, pids in R.CATEGORIES:
        rows = [f"- [{short(pid, 'en')}]({R.url(pid, 'en')}): {blurb(pid, 'en')}" for pid in pids if pid in ids]
        if rows:
            lines += ["", f"## {label['en']}", ""] + rows
    lines += ["", "## Docs", "",
              f"- [All tools]({R.url('tools', 'en')}): Full index of every PDF tool on the site.",
              f"- [Source code]({L.GITHUB}): AGPL-3.0, the same engine that runs in the browser.",
              "", "## Optional", "",
              f"- [Svenska]({R.url('home', 'sv')}): Swedish version of the site, same tools."]
    return "\n".join(lines) + "\n"


def redirects(ids):
    """English-language browsers landing on a Swedish page go to its English twin (?lang=sv opts out)."""
    rules = []
    for pid in ids:
        rules.append({
            "source": R.path(pid, "sv"),
            "has": [{"type": "header", "key": "accept-language", "value": "^en.*"}],
            "missing": [{"type": "query", "key": "lang"}],
            "destination": R.path(pid, "en"),
            "permanent": False,
        })
    return rules


# ---------------------------------------------------------------- main

def build():
    files = {}
    ids = []
    for pid in R.OUTPUT_ORDER:
        if pid not in CONTENT:
            print(f"  (skipping {pid}: no content yet)")
            continue
        ids.append(pid)
        for lang in LANGS:
            files[out_path(pid, lang)] = RENDER[R.kind(pid)](pid, lang, resolve(CONTENT[pid][lang], lang))
    files[os.path.join(WEB, "sitemap.xml")] = sitemap(ids)
    files[os.path.join(WEB, "llms.txt")] = llms_txt(ids)
    # The pages that may take reviews; api/reviews.js refuses any other tool id.
    files[os.path.join(ROOT, "api", "_tools.json")] = json.dumps([i for i in ids if R.kind(i) != "hub"]) + "\n"
    vpath = os.path.join(ROOT, "vercel.json")
    vercel = json.load(open(vpath))
    vercel["redirects"] = redirects(ids)
    files[vpath] = json.dumps(vercel, ensure_ascii=False, indent=2) + "\n"
    return files


def main():
    files = build()
    if "--check" in sys.argv:
        stale = [p for p, s in files.items() if not os.path.exists(p) or open(p).read() != s]
        for p in stale:
            print("out of date:", os.path.relpath(p, ROOT))
        sys.exit(1 if stale else 0)
    for p, s in files.items():
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(s)
    print(f"wrote {len(files)} files")


if __name__ == "__main__":
    main()
