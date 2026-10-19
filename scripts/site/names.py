"""Short names (menu, related cards) and one-line blurbs for every page."""

NAMES = {
    "home":          {"sv": ("Redigera PDF", "Klicka på en rad och ändra texten direkt i PDF-filen."),
                      "en": ("Edit PDF", "Click a line and change the text right in the PDF.")},
    "change-text":   {"sv": ("Ändra text i PDF", "Byt ut ord, siffror och datum i en befintlig PDF."),
                      "en": ("Change text in PDF", "Swap words, numbers and dates in an existing PDF.")},
    "replace-text":  {"sv": ("Ersätt text i PDF", "Sök och ersätt text i hela PDF-filen på en gång."),
                      "en": ("Replace text in PDF", "Find and replace text across a whole PDF in one go.")},
    "no-upload":     {"sv": ("Redigera utan uppladdning", "Redigera en PDF utan att filen lämnar din dator."),
                      "en": ("Edit without uploading", "Edit a PDF without the file leaving your computer.")},
    "invoice":       {"sv": ("Redigera faktura-PDF", "Rätta fel i dina egna fakturor och offerter."),
                      "en": ("Edit invoice PDF", "Fix mistakes in your own invoices and quotes.")},
    "merge":         {"sv": ("Slå ihop PDF", "Sätt ihop flera PDF-filer till en."),
                      "en": ("Merge PDF", "Combine several PDF files into one.")},
    "split":         {"sv": ("Dela PDF", "Dela upp en PDF i flera filer."),
                      "en": ("Split PDF", "Split one PDF into several files.")},
    "delete-pages":  {"sv": ("Radera sidor", "Ta bort sidor du inte vill ha."),
                      "en": ("Delete pages", "Remove the pages you do not want.")},
    "extract-pages": {"sv": ("Extrahera sidor", "Plocka ut valda sidor till en ny PDF."),
                      "en": ("Extract pages", "Pull selected pages into a new PDF.")},
    "rotate":        {"sv": ("Rotera PDF", "Vrid sidor som ligger åt fel håll."),
                      "en": ("Rotate PDF", "Turn pages that face the wrong way.")},
    "jpg-to-pdf":    {"sv": ("JPG till PDF", "Gör en PDF av dina bilder."),
                      "en": ("JPG to PDF", "Turn your images into a PDF.")},
    "pdf-to-jpg":    {"sv": ("PDF till JPG", "Spara PDF-sidor som bilder."),
                      "en": ("PDF to JPG", "Save PDF pages as images.")},
    "metadata":      {"sv": ("Ta bort metadata", "Rensa författare, program och datum ur en PDF."),
                      "en": ("Remove metadata", "Clear author, app and dates from a PDF.")},
    "redact":        {"sv": ("Censurera PDF", "Dölj känslig text och områden på riktigt."),
                      "en": ("Redact PDF", "Black out sensitive text and areas for good.")},
    "page-numbers":  {"sv": ("Sidnummer", "Lägg till sidnummer på varje sida."),
                      "en": ("Page numbers", "Add page numbers to every page.")},
    "watermark":     {"sv": ("Vattenstämpel", "Lägg en text över sidorna."),
                      "en": ("Watermark", "Put text across the pages.")},
    "crop":          {"sv": ("Beskär PDF", "Klipp bort marginaler du inte vill ha."),
                      "en": ("Crop PDF", "Trim the margins you do not want.")},
    "sign":          {"sv": ("Signera PDF", "Rita eller skriv din namnteckning."),
                      "en": ("Sign PDF", "Draw or type your signature.")},
    "organize":      {"sv": ("Organisera PDF", "Ändra ordning, vrid och ta bort sidor."),
                      "en": ("Organize PDF", "Reorder, rotate and delete pages.")},
    "compress":      {"sv": ("Komprimera PDF", "Gör PDF-filen mindre att skicka."),
                      "en": ("Compress PDF", "Make the PDF smaller to send.")},
    "pdf-to-text":   {"sv": ("PDF till text", "Hämta texten ur en PDF."),
                      "en": ("PDF to text", "Get the text out of a PDF.")},
    "protect":       {"sv": ("Skydda PDF", "Lås filen med ett lösenord."),
                      "en": ("Protect PDF", "Lock the file with a password.")},
    "unlock":        {"sv": ("Lås upp PDF", "Ta bort lösenordet från din egen PDF."),
                      "en": ("Unlock PDF", "Remove the password from your own PDF.")},
    "compare":       {"sv": ("Jämför PDF", "Se vad som ändrats mellan två versioner."),
                      "en": ("Compare PDF", "See what changed between two versions.")},
    "tools":         {"sv": ("Alla verktyg", ""), "en": ("All tools", "")},
}


def short(pid, lang):
    return NAMES[pid][lang][0]


def blurb(pid, lang):
    return NAMES[pid][lang][1]
