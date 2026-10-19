"""Wave 5 tool pages (image, header and footer, text to PDF, comments, annotate, properties)."""

TOOLS5 = {}

ANNOT_SV = {"annot_Text": "Anteckningar", "annot_Highlight": "Markeringar", "annot_Underline": "Understrykningar", "annot_StrikeOut": "Genomstrykningar",
            "annot_Squiggly": "Vågiga understrykningar", "annot_FreeText": "Textrutor", "annot_Ink": "Frihandsritningar", "annot_Line": "Linjer och pilar",
            "annot_Square": "Rektanglar", "annot_Circle": "Ellipser", "annot_Polygon": "Polygoner", "annot_PolyLine": "Polylinjer", "annot_Stamp": "Stämplar",
            "annot_Caret": "Infogningsmärken", "annot_FileAttachment": "Bifogade filer", "annot_Sound": "Ljudkommentarer", "annot_Redact": "Censurmarkeringar"}
ANNOT_EN = {"annot_Text": "Notes", "annot_Highlight": "Highlights", "annot_Underline": "Underlines", "annot_StrikeOut": "Strikethroughs",
            "annot_Squiggly": "Squiggly underlines", "annot_FreeText": "Text boxes", "annot_Ink": "Freehand drawings", "annot_Line": "Lines and arrows",
            "annot_Square": "Rectangles", "annot_Circle": "Ellipses", "annot_Polygon": "Polygons", "annot_PolyLine": "Polylines", "annot_Stamp": "Stamps",
            "annot_Caret": "Insertion marks", "annot_FileAttachment": "File attachments", "annot_Sound": "Sound comments", "annot_Redact": "Redaction marks"}

# ------------------------------------------------------------------ add image
TOOLS5["add-image"] = {
    "sv": dict(
        title="Lägg till bild i PDF – logotyp eller stämpel | Retypee",
        desc="Lägg en bild, logotyp eller stämpel på en eller alla sidor i en PDF. Dra på plats, ändra storlek och synlighet. Gratis och utan uppladdning.",
        h1="Lägg till en bild i en PDF – *dra den på plats*.",
        lede="Välj en logotyp, stämpel eller bild och dra den dit den ska sitta på sidan. Du ser hur det blir innan du sparar, och allt sker i din webbläsare.",
        steps_h2="Så lägger du till en bild i en PDF",
        steps=[("Öppna PDF-filen och välj bilden.", "JPG, PNG, WebP och de flesta andra bildformat fungerar."),
               ("Placera bilden.", "Dra den på sidan, ändra storleken och hur genomskinlig den ska vara. Välj om den ska sitta på alla sidor."),
               ("Spara.", "Bilden läggs in i en ny PDF.")],
        sections=[
            {"h2": "Vanliga användningar", "ul": [
                "En logotyp i hörnet på alla sidor.",
                "En inskannad underskrift eller ett foto på ett formulär. För en ritad namnteckning finns {{link:sign}}.",
                "En stämpel som GODKÄND, eller en bild som visar vem filen kommer från.",
                "En blek bakgrundsbild bakom innehållet, med låg synlighet."]},
            {"h2": "Bra att veta", "ul": [
                "PNG-bilder med genomskinlig bakgrund behåller genomskinligheten.",
                "Bilden ligger ovanpå sidans innehåll och blir en del av filen.",
                "Stora bilder förminskas till högst 2400 punkter på längsta sidan, vilket räcker för tryck.",
                "Vridna sidor får bilden rätt vänd.",
                "Vill du i stället lägga text över sidorna, använd {{link:watermark}}."]},
        ],
        faq_h2="Vanliga frågor om att lägga till bild i PDF",
        faq=[("Hur lägger jag till en bild i en PDF?", "Öppna filen här, välj bilden och dra den dit den ska sitta. Klicka sedan på Lägg till bilden."),
             ("Kan jag lägga samma logotyp på alla sidor?", "Ja. Kryssa i att bilden ska sitta på alla sidor, så hamnar den på samma plats överallt."),
             ("Behåller en PNG sin genomskinliga bakgrund?", "Ja. Genomskinliga delar av bilden låter sidan under synas."),
             ("Laddas filen eller bilden upp?", "Nej. Allt sker i din webbläsare och varken filen eller bilden lämnar din dator.")],
        related=["watermark", "sign", "page-numbers", "header-footer"],
        ui=dict(ai_btn="Lägg till bilden", ai_choose="Välj bilden som ska läggas på sidorna.", ai_hint="Dra bilden dit den ska sitta. Ändra storlek och synlighet med reglagen.",
                ai_size="Storlek", ai_opacity="Synlighet", ai_all="Sätt bilden på alla sidor", ai_other="Välj en annan bild",
                ai_done="Bilden lades till på {n} {n:sida|sidor}.", out_suffix="med-bild"),
    ),
    "en": dict(
        title="Add Image to PDF – Logo or Stamp | Retypee",
        desc="Put an image, logo or stamp on one or every page of a PDF. Drag it into place, change size and opacity. Free, and nothing is uploaded.",
        h1="Add an image to a PDF – *drag it into place*.",
        lede="Choose a logo, stamp or picture and drag it where it belongs on the page. You see the result before you save, and everything happens in your browser.",
        steps_h2="How to add an image to a PDF",
        steps=[("Open the PDF and choose the image.", "JPG, PNG, WebP and most other image formats work."),
               ("Place the image.", "Drag it on the page, change its size and how see-through it is. Choose whether it goes on every page."),
               ("Save.", "The image is added to a new PDF.")],
        sections=[
            {"h2": "Common uses", "ul": [
                "A logo in the corner of every page.",
                "A scanned signature or a photo on a form. For a drawn signature there is {{link:sign}}.",
                "A stamp such as APPROVED, or a picture showing who the file comes from.",
                "A faint background picture behind the content, with low opacity."]},
            {"h2": "Good to know", "ul": [
                "PNG images with a transparent background keep their transparency.",
                "The image sits on top of the page content and becomes part of the file.",
                "Large images are reduced to at most 2400 points on the longest side, which is plenty for print.",
                "Rotated pages get the image the right way up.",
                "If you want to put text across the pages instead, use {{link:watermark}}."]},
        ],
        faq_h2="Questions about adding an image to a PDF",
        faq=[("How do I add an image to a PDF?", "Open the file here, choose the image and drag it where it belongs. Then click Add the image."),
             ("Can I put the same logo on every page?", "Yes. Tick the box to put the image on every page and it lands in the same place everywhere."),
             ("Does a PNG keep its transparent background?", "Yes. Transparent parts of the image let the page underneath show through."),
             ("Is the file or the image uploaded?", "No. Everything happens in your browser and neither the file nor the image leaves your computer.")],
        related=["watermark", "sign", "page-numbers", "header-footer"],
        ui=dict(ai_btn="Add the image", ai_choose="Choose the image to put on the pages.", ai_hint="Drag the image where it should go. Change size and opacity with the sliders.",
                ai_size="Size", ai_opacity="Opacity", ai_all="Put the image on every page", ai_other="Choose another image",
                ai_done="The image was added to {n} {n:page|pages}.", out_suffix="with-image"),
    ),
}

# ------------------------------------------------------------------ header and footer
TOOLS5["header-footer"] = {
    "sv": dict(
        title="Sidhuvud och sidfot i PDF – sidnummer, datum | Retypee",
        desc="Lägg till sidhuvud och sidfot i en PDF, med sidnummer, datum och filnamn. Stöder löpnummer som Bates-nummer. Gratis och utan uppladdning.",
        h1="Sidhuvud och sidfot i en PDF – *med sidnummer och datum*.",
        lede="Skriv text uppe och nere på alla sidor, till vänster, i mitten och till höger. Sätt in sidnummer, datum och filnamn med en kod, och se resultatet på första sidan.",
        steps_h2="Så lägger du till sidhuvud och sidfot",
        steps=[("Öppna PDF-filen.", "Släpp den på sidan."),
               ("Skriv texterna.", "Sex rutor: vänster, mitten och höger, uppe och nere. Använd koderna för sidnummer, antal sidor, datum och filnamn."),
               ("Lägg till och ladda ner.", "Texten läggs på alla sidor i den nya PDF-filen.")],
        sections=[
            {"h2": "Koderna du kan skriva", "ul": [
                "<em>{n}</em> blir sidnumret.",
                "<em>{total}</em> blir antalet sidor, till exempel i Sida {n} av {total}.",
                "<em>{date}</em> blir dagens datum, i formen ÅÅÅÅ-MM-DD.",
                "<em>{file}</em> blir filens namn utan ändelse."]},
            {"h2": "Löpnummer och Bates-nummer", "p": [
                "Med <em>Första numret</em> och <em>Antal siffror</em> får du löpnummer som ACME-000123, vilket är vanligt när handlingar ska märkas inför en granskning eller ett rättsfall. Skriv ACME-{n}, ange första numret och sex siffror."]},
            {"h2": "Bra att veta", "ul": [
                "Ska du bara ha sidnummer är {{link:page-numbers}} enklare.",
                "Texten skrivs i Helvetica, så bokstäver som å, ä och ö fungerar men emoji gör det inte.",
                "Hoppa över första sidan om försättsbladet ska vara utan.",
                "Har sidorna redan sidhuvud läggs det nya ovanpå. Se till att det inte krockar."]},
        ],
        faq_h2="Vanliga frågor om sidhuvud och sidfot i PDF",
        faq=[("Hur lägger jag till sidfot i en PDF?", "Öppna filen här, skriv texten i någon av rutorna under Sidfot och klicka på Lägg till. Texten hamnar nederst på alla sidor."),
             ("Kan jag få datum och sidnummer automatiskt?", "Ja. Skriv koderna {date} och {n}, så fylls de i på varje sida."),
             ("Kan jag göra Bates-nummer?", "Ja. Skriv till exempel ACME-{n}, välj första numret och antal siffror, så får varje sida ett eget löpnummer."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["page-numbers", "watermark", "add-image", "crop"],
        ui=dict(hf_default="Sida {n} av {total}", hf_btn="Lägg till sidhuvud och sidfot", hf_hint="Skriv text i rutorna. Koder: {n} sidnummer, {total} antal sidor, {date} dagens datum, {file} filnamnet.",
                hf_left="Vänster", hf_middle="Mitten", hf_right="Höger", hf_header="Sidhuvud", hf_footer="Sidfot", hf_size="Textstorlek", hf_margin="Avstånd från kanten (pt)",
                hf_start="Första numret", hf_digits="Antal siffror", hf_color="Färg", hf_skip="Hoppa över första sidan",
                hf_chars="Texten innehåller tecken som inte finns i teckenuppsättningen. Använd bokstäver, siffror och vanliga tecken.", preview_note="Så här ser det ut på första sidan.",
                hf_done="Sidhuvud och sidfot lades till på {n} {n:sida|sidor}.", out_suffix="med-sidfot"),
    ),
    "en": dict(
        title="Header and Footer in PDF – Page Numbers, Date | Retypee",
        desc="Add a header and footer to a PDF, with page numbers, date and file name. Supports running numbers such as Bates numbering. Free, no upload.",
        h1="Header and footer in a PDF – *with page numbers and date*.",
        lede="Write text at the top and bottom of every page, on the left, in the middle and on the right. Insert page number, date and file name with a code, and see the result on the first page.",
        steps_h2="How to add a header and footer",
        steps=[("Open the PDF.", "Drop it on the page."),
               ("Write the texts.", "Six boxes: left, middle and right, top and bottom. Use the codes for page number, page count, date and file name."),
               ("Add and download.", "The text is placed on every page of the new PDF.")],
        sections=[
            {"h2": "The codes you can write", "ul": [
                "<em>{n}</em> becomes the page number.",
                "<em>{total}</em> becomes the number of pages, for example in Page {n} of {total}.",
                "<em>{date}</em> becomes today's date, as YYYY-MM-DD.",
                "<em>{file}</em> becomes the file name without its extension."]},
            {"h2": "Running numbers and Bates numbers", "p": [
                "With <em>First number</em> and <em>Digits</em> you get running numbers such as ACME-000123, which is common when documents are marked for a review or a court case. Write ACME-{n}, set the first number and six digits."]},
            {"h2": "Good to know", "ul": [
                "If you only want page numbers, {{link:page-numbers}} is simpler.",
                "The text is written in Helvetica, so accented letters work but emoji do not.",
                "Skip the first page if the cover page should be left clean.",
                "If the pages already have a header the new one goes on top, so make sure they do not collide."]},
        ],
        faq_h2="Questions about headers and footers in PDFs",
        faq=[("How do I add a footer to a PDF?", "Open the file here, write the text in one of the boxes under Footer and click Add. The text lands at the bottom of every page."),
             ("Can I get the date and page number automatically?", "Yes. Write the codes {date} and {n}, and they are filled in on every page."),
             ("Can I make Bates numbers?", "Yes. Write for example ACME-{n}, choose the first number and the number of digits, and every page gets its own running number."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["page-numbers", "watermark", "add-image", "crop"],
        ui=dict(hf_default="Page {n} of {total}", hf_btn="Add header and footer", hf_hint="Write text in the boxes. Codes: {n} page number, {total} page count, {date} today's date, {file} the file name.",
                hf_left="Left", hf_middle="Middle", hf_right="Right", hf_header="Header", hf_footer="Footer", hf_size="Text size", hf_margin="Distance from the edge (pt)",
                hf_start="First number", hf_digits="Digits", hf_color="Colour", hf_skip="Skip the first page",
                hf_chars="The text contains characters that are not in the character set. Use letters, digits and ordinary symbols.", preview_note="This is how it looks on the first page.",
                hf_done="Header and footer were added to {n} {n:page|pages}.", out_suffix="with-footer"),
    ),
}

# ------------------------------------------------------------------ text to PDF
TOOLS5["text-to-pdf"] = {
    "sv": dict(
        title="Text till PDF – gör text till en PDF gratis | Retypee",
        desc="Skriv eller klistra in text, eller öppna en textfil, och gör den till en PDF med sidor och sidnummer. Gratis, i webbläsaren och utan uppladdning.",
        h1="Text till PDF – *skriv, klistra in, klart*.",
        lede="Skriv eller klistra in text, eller släpp en textfil på sidan, och få en PDF med rätt radbrytning och sidor. Allt görs i din webbläsare.",
        steps_h2="Så gör du text till en PDF",
        steps=[("Skriv eller klistra in texten.", "Eller öppna en .txt-fil, eller släpp den på sidan."),
               ("Välj utseende.", "Typsnitt, textstorlek, pappersstorlek, marginal och om sidorna ska numreras."),
               ("Skapa PDF.", "Raderna bryts efter sidans bredd och texten delas upp på sidor.")],
        sections=[
            {"h2": "Bra för", "ul": [
                "Anteckningar, brev och utkast som ska skickas som PDF.",
                "Loggar och kodutdrag i fast teckenbredd.",
                "Text från en e-post eller ett webbsida som ska sparas."]},
            {"h2": "Det här får du", "p": [
                "Ren text, utan formatering som fet stil, rubriker eller bilder. Tomma rader, indrag och radbrytningar bevaras. Behöver du ett formaterat dokument är ett ordbehandlingsprogram rätt verktyg, men för text som ska bli en enkel PDF går det här snabbare."]},
            {"h2": "Bra att veta", "ul": [
                "Bokstäver som å, ä, ö och é fungerar. Tecken som inte finns i PDF-teckensnitten, till exempel emoji, ersätts med ett frågetecken och du får veta hur många.",
                "Mycket långa ord bryts så att de ryms på raden.",
                "Vill du göra om en bild av text till riktig text, använd {{link:ocr}}.",
                "Har du flera PDF-filer som ska bli en, använd {{link:merge}}."]},
        ],
        faq_h2="Vanliga frågor om text till PDF",
        faq=[("Hur gör jag en textfil till PDF?", "Öppna textfilen här, eller klistra in texten, välj utseende och klicka på Skapa PDF."),
             ("Behålls formateringen?", "Nej. Det blir ren text, med tomma rader, indrag och radbrytningar bevarade men utan fet stil eller rubriker."),
             ("Fungerar svenska bokstäver?", "Ja. Å, ä och ö fungerar i alla tre typsnitten. Emoji och sällsynta tecken ersätts med ett frågetecken."),
             ("Laddas texten upp?", "Nej. PDF-filen skapas i din webbläsare och texten lämnar aldrig din dator.")],
        related=["merge", "ocr", "pdf-to-text", "header-footer"],
        ui=dict(ttp_ph="Skriv eller klistra in text här…", ttp_label="Text som ska bli PDF", ttp_hint="Skriv eller klistra in text, eller öppna en textfil. Du kan också släppa en .txt-fil på sidan.",
                ttp_open="Öppna textfil", ttp_clear="Rensa", ttp_font="Typsnitt", ttp_sans="Sans-serif", ttp_serif="Serif", ttp_mono="Fast teckenbredd", ttp_size="Textstorlek",
                ttp_paper="Pappersstorlek", ttp_margin="Marginal", margin_small="Smal", margin_normal="Normal", margin_big="Bred", ttp_numbers="Sidnummer längst ner",
                ttp_btn="Skapa PDF", ttp_not_text="{name} är ingen textfil.", ttp_done="PDF-filen har {n} {n:sida|sidor}.",
                ttp_replaced="{n} {n:tecken|tecken} som inte finns i PDF-teckensnittet ersattes med ?.", out_name="text"),
    ),
    "en": dict(
        title="Text to PDF – Turn Text Into a PDF Free | Retypee",
        desc="Type or paste text, or open a text file, and turn it into a PDF with pages and page numbers. Free, in your browser and without uploading.",
        h1="Text to PDF – *type, paste, done*.",
        lede="Type or paste text, or drop a text file on the page, and get a PDF with proper line breaks and pages. It all happens in your browser.",
        steps_h2="How to turn text into a PDF",
        steps=[("Type or paste the text.", "Or open a .txt file, or drop it on the page."),
               ("Choose the look.", "Font, text size, paper size, margin and whether the pages are numbered."),
               ("Create the PDF.", "Lines are broken to fit the width of the page and the text is split into pages.")],
        sections=[
            {"h2": "Good for", "ul": [
                "Notes, letters and drafts that should be sent as a PDF.",
                "Logs and code snippets in a fixed-width font.",
                "Text from an email or a web page that should be saved."]},
            {"h2": "What you get", "p": [
                "Plain text, without formatting such as bold, headings or images. Blank lines, indentation and line breaks are kept. If you need a formatted document a word processor is the right tool, but for text that should become a simple PDF this is quicker."]},
            {"h2": "Good to know", "ul": [
                "Letters such as é, ü and ñ work. Characters that are not in the PDF fonts, for example emoji, are replaced by a question mark and you are told how many.",
                "Very long words are broken so they fit on the line.",
                "If you want to turn a picture of text into real text, use {{link:ocr}}.",
                "If you have several PDFs that should become one, use {{link:merge}}."]},
        ],
        faq_h2="Questions about text to PDF",
        faq=[("How do I turn a text file into a PDF?", "Open the text file here, or paste the text, choose the look and click Create PDF."),
             ("Is the formatting kept?", "No. It becomes plain text, with blank lines, indentation and line breaks kept but no bold or headings."),
             ("Do accented letters work?", "Yes. Letters such as é, ü and ñ work in all three fonts. Emoji and rare symbols are replaced by a question mark."),
             ("Is the text uploaded?", "No. The PDF is made in your browser and the text never leaves your computer.")],
        related=["merge", "ocr", "pdf-to-text", "header-footer"],
        ui=dict(ttp_ph="Type or paste text here…", ttp_label="Text to turn into a PDF", ttp_hint="Type or paste text, or open a text file. You can also drop a .txt file on the page.",
                ttp_open="Open a text file", ttp_clear="Clear", ttp_font="Font", ttp_sans="Sans-serif", ttp_serif="Serif", ttp_mono="Fixed width", ttp_size="Text size",
                ttp_paper="Paper size", ttp_margin="Margin", margin_small="Narrow", margin_normal="Normal", margin_big="Wide", ttp_numbers="Page numbers at the bottom",
                ttp_btn="Create PDF", ttp_not_text="{name} is not a text file.", ttp_done="The PDF has {n} {n:page|pages}.",
                ttp_replaced="{n} {n:character|characters} that are not in the PDF font {n:was|were} replaced with ?.", out_name="text"),
    ),
}

# ------------------------------------------------------------------ remove comments
TOOLS5["remove-annots"] = {
    "sv": dict(
        title="Ta bort kommentarer ur PDF – rensa markeringar | Retypee",
        desc="Ta bort kommentarer, markeringar, anteckningar och ritningar ur en PDF innan du delar den. Välj vilka sorter. Gratis och utan uppladdning.",
        h1="Ta bort kommentarer ur en PDF – *rensa innan du delar*.",
        lede="Anteckningar, markeringar och ritningar kan avslöja mer än du tänkt. Retypee visar vilka sorter filen har, och du väljer vad som ska bort.",
        steps_h2="Så tar du bort kommentarer ur en PDF",
        steps=[("Öppna PDF-filen.", "Retypee räknar kommentarerna och visar dem per sort."),
               ("Välj vad som ska bort.", "Alla sorter är förkryssade. Avmarkera det du vill behålla, till exempel markeringarna."),
               ("Ta bort och ladda ner.", "Du får en ny PDF utan de valda kommentarerna.")],
        sections=[
            {"h2": "Det här kan tas bort", "ul": [
                "Anteckningar och textrutor.",
                "Markeringar, understrykningar och genomstrykningar.",
                "Frihandsritningar, linjer, pilar och former.",
                "Stämplar, bifogade filer och ljudkommentarer."]},
            {"h2": "Det här lämnas orört", "ul": [
                "Länkar i dokumentet.",
                "Formulärfält. Vill du låsa dem finns {{link:flatten}}.",
                "Den vanliga texten och bilderna på sidorna."]},
            {"h2": "Bra att veta", "ul": [
                "Kommentarer som är utplattade, alltså inbakade i sidan, är inte kommentarer längre och kan inte tas bort här.",
                "Vill du dölja text för gott, använd {{link:redact}}. Då tas själva texten bort ur filen.",
                "Vill du ta bort författare och datum också, använd {{link:metadata}}.",
                "PDF-motorn (cirka 25 MB) hämtas första gången du använder verktyget."]},
        ],
        faq_h2="Vanliga frågor om att ta bort kommentarer ur PDF",
        faq=[("Hur tar jag bort kommentarer ur en PDF?", "Öppna filen här, välj vilka sorter som ska bort och klicka på Ta bort. Du laddar ner en ren kopia."),
             ("Kan jag behålla markeringarna men ta bort anteckningarna?", "Ja. Avmarkera Markeringar och låt Anteckningar vara kryssad."),
             ("Varför hittas inga kommentarer fast jag ser markeringar?", "Då är markeringarna troligen inbakade i sidan, till exempel efter utplattning, och är inte längre kommentarer."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["metadata", "redact", "flatten", "protect"],
        ui=dict(ra_none="Filen har inga kommentarer, markeringar eller ritningar att ta bort.", ra_hint="Välj vilka sorters kommentarer som ska tas bort. Länkar och formulärfält påverkas inte.",
                ra_btn="Ta bort {n} {n:kommentar|kommentarer}", ra_done="Klart. De valda kommentarerna är borttagna ur filen.", out_suffix="utan-kommentarer", **ANNOT_SV),
    ),
    "en": dict(
        title="Remove Comments from PDF – Clear Markup | Retypee",
        desc="Remove comments, highlights, notes and drawings from a PDF before you share it. Choose which kinds. Free, and nothing is uploaded.",
        h1="Remove comments from a PDF – *clean up before you share*.",
        lede="Notes, highlights and drawings can reveal more than you meant. Retypee shows which kinds the file has, and you choose what goes.",
        steps_h2="How to remove comments from a PDF",
        steps=[("Open the PDF.", "Retypee counts the comments and shows them by kind."),
               ("Choose what to remove.", "Every kind is ticked. Untick what you want to keep, for example the highlights."),
               ("Remove and download.", "You get a new PDF without the chosen comments.")],
        sections=[
            {"h2": "What can be removed", "ul": [
                "Notes and text boxes.",
                "Highlights, underlines and strikethroughs.",
                "Freehand drawings, lines, arrows and shapes.",
                "Stamps, attachments and sound comments."]},
            {"h2": "What is left alone", "ul": [
                "Links in the document.",
                "Form fields. If you want to lock them there is {{link:flatten}}.",
                "The ordinary text and images on the pages."]},
            {"h2": "Good to know", "ul": [
                "Comments that have been flattened, baked into the page, are no longer comments and cannot be removed here.",
                "If you want to hide text for good, use {{link:redact}}. It removes the text itself from the file.",
                "If you want to remove author and dates too, use {{link:metadata}}.",
                "The PDF engine (about 25 MB) is downloaded the first time you use the tool."]},
        ],
        faq_h2="Questions about removing comments from PDFs",
        faq=[("How do I remove comments from a PDF?", "Open the file here, choose which kinds to remove and click Remove. You download a clean copy."),
             ("Can I keep the highlights but remove the notes?", "Yes. Untick Highlights and leave Notes ticked."),
             ("Why are no comments found although I can see highlights?", "The highlights are probably baked into the page, for example after flattening, and are no longer comments."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["metadata", "redact", "flatten", "protect"],
        ui=dict(ra_none="The file has no comments, highlights or drawings to remove.", ra_hint="Choose which kinds of comments to remove. Links and form fields are not affected.",
                ra_btn="Remove {n} {n:comment|comments}", ra_done="Done. The chosen comments are removed from the file.", out_suffix="no-comments", **ANNOT_EN),
    ),
}

# ------------------------------------------------------------------ annotate
TOOLS5["annotate"] = {
    "sv": dict(
        title="Markera och rita i PDF – gratis, utan uppladdning | Retypee",
        desc="Markera text med gult, rita fritt och skriv anteckningar direkt på en PDF. Spara en ny fil. Gratis, i webbläsaren och utan uppladdning.",
        h1="Markera och rita i en PDF – *direkt på sidan*.",
        lede="Markera med överstrykningspenna, rita fritt och skriv anteckningar på sidorna. Allt du gör ligger kvar i den sparade filen, och inget laddas upp.",
        steps_h2="Så markerar och ritar du i en PDF",
        steps=[("Öppna PDF-filen.", "Alla sidor visas under varandra."),
               ("Välj verktyg.", "Markera drar en gul ruta, Rita är en penna, Text sätter en anteckning. Radera tar bort en markering."),
               ("Spara.", "Markeringarna läggs in i en ny PDF.")],
        sections=[
            {"h2": "Verktygen", "ul": [
                "<em>Markera</em>: dra en ruta över texten. Färgen blandas med texten under, så den syns fortfarande.",
                "<em>Rita</em>: frihandsritning i vald färg och tjocklek, bra för pilar och ringar.",
                "<em>Text</em>: klicka där anteckningen ska sitta och skriv. Klicka utanför för att klart.",
                "<em>Radera</em>: klicka på en markering för att ta bort den. <em>Ångra</em> tar bort den senaste."]},
            {"h2": "Bra att veta", "ul": [
                "Markeringarna sparas som ritat innehåll på sidan och syns i alla läsare. De blir inte redigerbara kommentarer.",
                "Markera drar en ruta och följer inte textens rader, så dra över varje rad.",
                "På en pekskärm stoppar ett aktivt verktyg bläddringen på sidan. Välj Bläddra för att scrolla.",
                "Vill du ta bort markeringar i en fil från någon annan, använd {{link:remove-annots}}.",
                "Vill du skriva i ett formulär, använd {{link:fill-form}}."]},
        ],
        faq_h2="Vanliga frågor om att markera och rita i PDF",
        faq=[("Hur markerar jag text i en PDF?", "Öppna filen här, välj Markera och dra en ruta över texten. Klicka sedan på Spara för att få en ny fil."),
             ("Kan jag skriva anteckningar på sidan?", "Ja. Välj Text, klicka där anteckningen ska sitta och skriv."),
             ("Går markeringarna att ta bort efteråt?", "Inte i den sparade filen, eftersom de ritas in på sidan. Medan du arbetar kan du ångra eller radera dem."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["fill-form", "sign", "remove-annots", "redact"],
        ui=dict(an_btn="Spara {n} {n:markering|markeringar}", an_summary="{n} {n:markering|markeringar} gjorda.", an_hl="Markera", an_pen="Rita", an_text="Text", an_erase="Radera", an_view="Bläddra",
                an_undo="Ångra", an_clear="Rensa allt", an_hint="Välj verktyg och arbeta direkt på sidorna. Markera drar en gul ruta, Rita är en penna och Text sätter en anteckning. På en pekskärm stoppar ett aktivt verktyg bläddringen, så välj Bläddra för att scrolla.",
                an_width="Tjocklek", an_thin="Tunn", an_medium="Mellan", an_thick="Tjock", an_size="Textstorlek", an_small="Liten", an_large="Stor", an_text_ph="Skriv text…",
                an_chars="Anteckningen innehåller tecken som inte finns i teckenuppsättningen. Använd bokstäver, siffror och vanliga tecken.", an_done="{n} {n:markering|markeringar} lades in i filen.", out_suffix="markerad"),
    ),
    "en": dict(
        title="Highlight and Draw on PDF – Free, No Upload | Retypee",
        desc="Highlight text in yellow, draw freehand and write notes right on a PDF. Save a new file. Free, in your browser and without uploading.",
        h1="Highlight and draw on a PDF – *right on the page*.",
        lede="Highlight with a marker, draw freehand and write notes on the pages. Everything you do stays in the saved file, and nothing is uploaded.",
        steps_h2="How to highlight and draw on a PDF",
        steps=[("Open the PDF.", "All the pages are shown one under the other."),
               ("Choose a tool.", "Highlight drags a yellow box, Draw is a pen, Text places a note. Erase removes a mark."),
               ("Save.", "The marks are added to a new PDF.")],
        sections=[
            {"h2": "The tools", "ul": [
                "<em>Highlight</em>: drag a box over the text. The colour blends with the text underneath, so it still shows.",
                "<em>Draw</em>: freehand drawing in the chosen colour and thickness, good for arrows and circles.",
                "<em>Text</em>: click where the note should go and type. Click outside when you are done.",
                "<em>Erase</em>: click a mark to remove it. <em>Undo</em> removes the latest one."]},
            {"h2": "Good to know", "ul": [
                "The marks are saved as drawn content on the page and show in every reader. They do not become editable comments.",
                "Highlight drags a box and does not follow the lines of the text, so drag over each line.",
                "On a touch screen an active tool stops the page from scrolling. Choose Scroll to move around.",
                "If you want to remove markup from someone else's file, use {{link:remove-annots}}.",
                "If you want to write in a form, use {{link:fill-form}}."]},
        ],
        faq_h2="Questions about highlighting and drawing on PDFs",
        faq=[("How do I highlight text in a PDF?", "Open the file here, choose Highlight and drag a box over the text. Then click Save to get a new file."),
             ("Can I write notes on the page?", "Yes. Choose Text, click where the note should go and type."),
             ("Can the marks be removed afterwards?", "Not in the saved file, since they are drawn onto the page. While you work you can undo or erase them."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["fill-form", "sign", "remove-annots", "redact"],
        ui=dict(an_btn="Save {n} {n:mark|marks}", an_summary="{n} {n:mark|marks} made.", an_hl="Highlight", an_pen="Draw", an_text="Text", an_erase="Erase", an_view="Scroll",
                an_undo="Undo", an_clear="Clear all", an_hint="Choose a tool and work right on the pages. Highlight drags a yellow box, Draw is a pen and Text places a note. On a touch screen an active tool stops scrolling, so choose Scroll to move around.",
                an_width="Thickness", an_thin="Thin", an_medium="Medium", an_thick="Thick", an_size="Text size", an_small="Small", an_large="Large", an_text_ph="Type text…",
                an_chars="The note contains characters that are not in the character set. Use letters, digits and ordinary symbols.", an_done="{n} {n:mark was|marks were} added to the file.", out_suffix="marked"),
    ),
}

# ------------------------------------------------------------------ properties
TOOLS5["properties"] = {
    "sv": dict(
        title="Redigera PDF-egenskaper – titel, författare m.m. | Retypee",
        desc="Ändra titel, författare, ämne och nyckelord i en PDF. Se vad filen har nu och rensa fält du inte vill dela. Gratis och utan uppladdning.",
        h1="Redigera PDF-egenskaper – *titel, författare och nyckelord*.",
        lede="Titeln visas i fliken, i sökresultat och i filhanteraren. Se vad filen innehåller nu, ändra det och spara. Allt sker i din webbläsare.",
        steps_h2="Så ändrar du egenskaperna i en PDF",
        steps=[("Öppna PDF-filen.", "Fälten visar vad filen har nu."),
               ("Ändra fälten.", "Titel, författare, ämne och nyckelord. Töm ett fält för att ta bort värdet."),
               ("Spara.", "Du får en ny PDF med de nya egenskaperna.")],
        sections=[
            {"h2": "Varför det spelar roll", "ul": [
                "Titeln syns i webbläsarens flik och i sökresultat, så en tydlig titel ser bättre ut än ett filnamn som slutgiltig-v7.",
                "Författaren och programmet kan avslöja mer än du vill. Töm fälten innan du delar filen.",
                "Nyckelord och ämne hjälper sökning i dokumenthantering och arkiv."]},
            {"h2": "Visa titeln i fönstrets rubrik", "p": [
                "Många läsare visar filnamnet i fliken även om filen har en titel. Kryssar du i <em>Visa titeln i fönstrets rubrik</em> ber du läsaren att visa titeln i stället, vilket också gör filen mer tillgänglig."]},
            {"h2": "Bra att veta", "ul": [
                "Ett eventuellt separat XMP-block, som vissa program föredrar, tas bort så att alla visar samma värden.",
                "Vill du rensa allt, inklusive datum och programnamn, använd {{link:metadata}}.",
                "Svenska bokstäver som å, ä och ö fungerar i alla fält.",
                "Innehållet på sidorna påverkas inte."]},
        ],
        faq_h2="Vanliga frågor om PDF-egenskaper",
        faq=[("Hur ändrar jag titeln på en PDF?", "Öppna filen här, skriv den nya titeln i fältet Titel och klicka på Spara egenskaper."),
             ("Hur tar jag bort författarnamnet?", "Töm fältet Författare och spara. För att rensa allt på en gång finns Ta bort metadata."),
             ("Varför visar min läsare ändå gamla uppgifter?", "Filen kan ha ett separat XMP-block med egna värden. Retypee tar bort det vid sparning, så ladda om den nya filen."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["metadata", "remove-annots", "protect", "compress"],
        ui=dict(prop_title="Titel", prop_author="Författare", prop_subject="Ämne", prop_keywords="Nyckelord (separera med komma)", prop_display="Visa titeln i fönstrets rubrik",
                prop_btn="Spara egenskaper", prop_hint="Fälten visar vad filen har nu. Töm ett fält för att ta bort värdet.", prop_done="Egenskaperna är sparade.", out_suffix="egenskaper"),
    ),
    "en": dict(
        title="Edit PDF Properties – Title, Author and More | Retypee",
        desc="Change the title, author, subject and keywords of a PDF. See what the file has now and clear fields you do not want to share. Free, no upload.",
        h1="Edit PDF properties – *title, author and keywords*.",
        lede="The title shows in the tab, in search results and in the file manager. See what the file contains now, change it and save. Everything happens in your browser.",
        steps_h2="How to change the properties of a PDF",
        steps=[("Open the PDF.", "The fields show what the file has now."),
               ("Change the fields.", "Title, author, subject and keywords. Empty a field to remove the value."),
               ("Save.", "You get a new PDF with the new properties.")],
        sections=[
            {"h2": "Why it matters", "ul": [
                "The title shows in the browser tab and in search results, so a clear title looks better than a file name like final-v7.",
                "The author and the program can reveal more than you want. Empty the fields before you share the file.",
                "Keywords and subject help search in document management and archives."]},
            {"h2": "Show the title in the window heading", "p": [
                "Many readers show the file name in the tab even if the file has a title. If you tick <em>Show the title in the window heading</em> you ask the reader to show the title instead, which also makes the file more accessible."]},
            {"h2": "Good to know", "ul": [
                "A separate XMP block, if there is one and some programs prefer it, is removed so that every program shows the same values.",
                "If you want to clear everything, including dates and program name, use {{link:metadata}}.",
                "Accented letters such as é, ü and ñ work in every field.",
                "The content of the pages is not affected."]},
        ],
        faq_h2="Questions about PDF properties",
        faq=[("How do I change the title of a PDF?", "Open the file here, type the new title in the Title field and click Save properties."),
             ("How do I remove the author name?", "Empty the Author field and save. To clear everything at once there is Remove metadata."),
             ("Why does my reader still show the old details?", "The file may have a separate XMP block with its own values. Retypee removes it when saving, so reload the new file."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["metadata", "remove-annots", "protect", "compress"],
        ui=dict(prop_title="Title", prop_author="Author", prop_subject="Subject", prop_keywords="Keywords (separate with commas)", prop_display="Show the title in the window heading",
                prop_btn="Save properties", prop_hint="The fields show what the file has now. Empty a field to remove the value.", prop_done="The properties are saved.", out_suffix="properties"),
    ),
}
