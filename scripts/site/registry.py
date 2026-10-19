"""Every page on the site, its URL in each language, and where it sits in the menu."""

BASE = "https://retypee.se"
LASTMOD = "2026-10-19"          # bump when page content changes (it feeds sitemap.xml)

# id -> (kind, slug_sv, slug_en, libs)
#   kind "editor": the full editor (web/app.js) with its own landing copy
#   kind "tool":   a single-purpose tool page (web/tools/<id>.js)
#   kind "hub":    the list of all tools
#   libs: scripts a tool page needs, loaded in this order
PAGES = {
    "home":          ("editor", "",                              "",                           []),
    "change-text":   ("editor", "andra-text-i-pdf",              "change-text-in-pdf",         []),
    "replace-text":  ("editor", "ersatt-text-i-pdf",             "replace-text-in-pdf",        []),
    "no-upload":     ("editor", "redigera-pdf-utan-uppladdning", "edit-pdf-without-uploading", []),
    "invoice":       ("editor", "redigera-faktura-pdf",          "edit-invoice-pdf",           []),
    "merge":         ("tool",   "sla-ihop-pdf",                  "merge-pdf",                  ["pdf-lib", "pdfjs"]),
    "split":         ("tool",   "dela-pdf",                      "split-pdf",                  ["pdf-lib", "pdfjs", "fflate"]),
    "delete-pages":  ("tool",   "radera-sidor-pdf",              "delete-pdf-pages",           ["pdf-lib", "pdfjs"]),
    "extract-pages": ("tool",   "extrahera-sidor-pdf",           "extract-pdf-pages",          ["pdf-lib", "pdfjs"]),
    "rotate":        ("tool",   "rotera-pdf",                    "rotate-pdf",                 ["pdf-lib", "pdfjs"]),
    "jpg-to-pdf":    ("tool",   "jpg-till-pdf",                  "jpg-to-pdf",                 ["pdf-lib", "pdfjs"]),
    "pdf-to-jpg":    ("tool",   "pdf-till-jpg",                  "pdf-to-jpg",                 ["pdfjs", "fflate"]),
    "metadata":      ("tool",   "ta-bort-metadata-pdf",          "remove-pdf-metadata",        ["pdf-lib", "pdfjs", "engine"]),
    "redact":        ("tool",   "censurera-pdf",                 "redact-pdf",                 ["pdfjs", "engine"]),
    "page-numbers":  ("tool",   "lagg-till-sidnummer-pdf",       "add-page-numbers-to-pdf",    ["pdf-lib", "pdfjs"]),
    "watermark":     ("tool",   "vattenstampel-pdf",             "watermark-pdf",              ["pdf-lib", "pdfjs"]),
    "crop":          ("tool",   "beskar-pdf",                    "crop-pdf",                   ["pdf-lib", "pdfjs"]),
    "sign":          ("tool",   "signera-pdf",                   "sign-pdf",                   ["pdf-lib", "pdfjs"]),
    "organize":      ("tool",   "organisera-pdf",                "organize-pdf",               ["pdf-lib", "pdfjs"]),
    "compress":      ("tool",   "komprimera-pdf",                "compress-pdf",               ["pdfjs", "engine"]),
    "pdf-to-text":   ("tool",   "pdf-till-text",                 "pdf-to-text",                ["pdfjs"]),
    "protect":       ("tool",   "skydda-pdf",                    "protect-pdf",                ["pdfjs", "engine"]),
    "unlock":        ("tool",   "las-upp-pdf",                   "unlock-pdf",                 ["pdfjs", "engine"]),
    "compare":       ("tool",   "jamfor-pdf",                    "compare-pdf",                ["pdfjs"]),
    "ocr":           ("tool",   "ocr-pdf",                       "ocr-pdf",                    ["pdf-lib", "pdfjs", "tesseract"]),
    "fill-form":     ("tool",   "fyll-i-pdf-formular",           "fill-pdf-form",              ["pdf-lib", "pdfjs"]),
    "scan":          ("tool",   "skanna-till-pdf",               "scan-to-pdf",                ["pdf-lib"]),
    "tools":         ("hub",    "verktyg",                       "tools",                      []),
}

# Menu and hub grouping (mirrors the usual PDF-tool menu).
CATEGORIES = [
    ("edit",     {"sv": "Redigera PDF",  "en": "Edit PDF"},     ["home", "fill-form", "page-numbers", "watermark", "crop", "sign"]),
    ("common",   {"sv": "Vanliga redigeringar", "en": "Common edits"}, ["change-text", "replace-text", "no-upload", "invoice"]),
    ("organize", {"sv": "Organisera PDF", "en": "Organize PDF"}, ["merge", "split", "delete-pages", "extract-pages", "rotate", "organize"]),
    ("convert",  {"sv": "Optimera och omvandla", "en": "Optimize and convert"}, ["compress", "scan", "ocr", "jpg-to-pdf", "pdf-to-jpg", "pdf-to-text"]),
    ("security", {"sv": "PDF-säkerhet",  "en": "PDF security"}, ["metadata", "redact", "protect", "unlock", "compare"]),
]

# Groups that are listed on the hub and in the footer but kept out of the header menu.
MENU_HIDDEN = {"common"}

OUTPUT_ORDER = list(PAGES)


def kind(pid):
    return PAGES[pid][0]


def slug(pid, lang):
    return PAGES[pid][1 if lang == "sv" else 2]


def path(pid, lang):
    """URL path with a trailing slash. Swedish at the root, English under /en/."""
    s = slug(pid, lang)
    if lang == "sv":
        return "/" + (s + "/" if s else "")
    return "/en/" + (s + "/" if s else "")


def url(pid, lang):
    return BASE + path(pid, lang)


def libs(pid):
    return PAGES[pid][3]
