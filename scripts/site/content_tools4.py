"""Wave 4 tool pages (blank pages, pages per sheet, resize, images, repair, flatten)."""

TOOLS4 = {}

# ------------------------------------------------------------------ blank pages
TOOLS4["blank"] = {
    "sv": dict(
        title="Ta bort tomma sidor ur PDF – automatiskt | Retypee",
        desc="Hitta och ta bort tomma sidor i en PDF automatiskt, till exempel efter dubbelsidig skanning. Gratis, i webbläsaren och utan uppladdning.",
        h1="Ta bort tomma sidor ur en PDF – *automatiskt*.",
        lede="Retypee ritar upp varje sida och mäter hur mycket som står på den. Sidor utan innehåll markeras åt dig, och du bestämmer vilka som försvinner.",
        steps_h2="Så tar du bort tomma sidor",
        steps=[("Öppna PDF-filen.", "Alla sidor kontrolleras direkt i webbläsaren."),
               ("Kontrollera markeringen.", "Tomma sidor är redan markerade. Ändra känsligheten, eller klicka på sidor för att lägga till eller ta bort markeringar."),
               ("Ta bort och ladda ner.", "Du får en ny PDF utan de markerade sidorna.")],
        sections=[
            {"h2": "När det här behövs", "ul": [
                "Efter dubbelsidig skanning, när baksidorna är tomma.",
                "När ett dokument har fått extra sidbrytningar.",
                "När en export har lämnat tomma sidor mellan kapitlen."]},
            {"h2": "Så avgörs om en sida är tom", "p": [
                "Sidan ritas upp i liten storlek och andelen mörka punkter räknas. Tre nivåer finns. <em>Bara helt tomma</em> kräver en ren sida. <em>Normal</em> bortser från små märken som ett sidnummer. <em>Tillåtande</em> passar skannade sidor med brus och skuggor från papperet."]},
            {"h2": "Bra att veta", "ul": [
                "Du ser alla sidor som miniatyrer och har alltid sista ordet.",
                "De borttagna sidorna lämnar inga spår i den nya filen.",
                "Vill du ta bort bestämda sidor utan automatik, använd {{link:delete-pages}}.",
                "Har sidorna kommit i fel ordning, använd {{link:organize}}."]},
        ],
        faq_h2="Vanliga frågor om tomma sidor i PDF",
        faq=[("Hur tar jag bort tomma sidor ur en PDF?", "Öppna filen här. Tomma sidor markeras automatiskt, och du klickar på Ta bort för att få en ny PDF utan dem."),
             ("Varför hittades inga tomma sidor?", "Skannade sidor har ofta brus som ser ut som innehåll. Välj nivån Tillåtande, eller markera sidorna själv."),
             ("Kan en sida med bara ett sidnummer räknas som tom?", "Ja, på nivån Normal. Vill du behålla sådana sidor väljer du Bara helt tomma."),
             ("Laddas filen upp?", "Nej. Sidorna kontrolleras i din webbläsare och filen lämnar aldrig din dator.")],
        related=["delete-pages", "scan", "organize", "compress"],
        ui=dict(blank_scanning="Letar tomma sidor… {n} av {total}", blank_level="Känslighet", blank_strict="Bara helt tomma", blank_normal="Normal (bortser från små märken)",
                blank_loose="Tillåtande (skannade sidor med brus)", blank_found="{n} {n:tom sida hittades|tomma sidor hittades}. De är redan markerade.",
                blank_none="Inga tomma sidor hittades. Prova en högre känslighet, eller markera sidor själv.", blank_btn="Ta bort {n} {n:sida|sidor}",
                blank_summary="{n} av {total} {total:sida|sidor} tas bort.", delete_all="Du kan inte ta bort alla sidor.", delete_label="Sidor som tas bort",
                blank_done="{n} {n:sida|sidor} togs bort. {left} {left:sida|sidor} kvar.", out_suffix="utan-tomma-sidor"),
    ),
    "en": dict(
        title="Remove Blank Pages from PDF – Automatically | Retypee",
        desc="Find and remove blank pages in a PDF automatically, for example after double-sided scanning. Free, in your browser and without uploading.",
        h1="Remove blank pages from a PDF – *automatically*.",
        lede="Retypee draws every page and measures how much is on it. Pages with no content are marked for you, and you decide which ones go.",
        steps_h2="How to remove blank pages",
        steps=[("Open the PDF.", "Every page is checked right in your browser."),
               ("Check the marking.", "Blank pages are already marked. Change the sensitivity, or click pages to add or remove marks."),
               ("Remove and download.", "You get a new PDF without the marked pages.")],
        sections=[
            {"h2": "When you need this", "ul": [
                "After double-sided scanning, when the backs are empty.",
                "When a document has picked up extra page breaks.",
                "When an export has left blank pages between chapters."]},
            {"h2": "How a page is judged blank", "p": [
                "The page is drawn small and the share of dark dots is counted. There are three levels. <em>Completely blank only</em> needs a clean page. <em>Normal</em> ignores small marks such as a page number. <em>Forgiving</em> suits scanned pages with noise and shadows from the paper."]},
            {"h2": "Good to know", "ul": [
                "You see every page as a thumbnail and always have the last word.",
                "The removed pages leave no trace in the new file.",
                "If you want to remove specific pages without the automatic part, use {{link:delete-pages}}.",
                "If the pages came out in the wrong order, use {{link:organize}}."]},
        ],
        faq_h2="Questions about blank pages in PDFs",
        faq=[("How do I remove blank pages from a PDF?", "Open the file here. Blank pages are marked automatically, and you click Remove to get a new PDF without them."),
             ("Why were no blank pages found?", "Scanned pages often have noise that looks like content. Choose the Forgiving level, or mark the pages yourself."),
             ("Can a page with only a page number count as blank?", "Yes, on the Normal level. If you want to keep such pages, choose Completely blank only."),
             ("Is the file uploaded?", "No. The pages are checked in your browser and the file never leaves your computer.")],
        related=["delete-pages", "scan", "organize", "compress"],
        ui=dict(blank_scanning="Looking for blank pages… {n} of {total}", blank_level="Sensitivity", blank_strict="Completely blank only", blank_normal="Normal (ignores small marks)",
                blank_loose="Forgiving (scanned pages with noise)", blank_found="{n} blank {n:page was|pages were} found. {n:It is|They are} already marked.",
                blank_none="No blank pages were found. Try a higher sensitivity, or mark pages yourself.", blank_btn="Remove {n} {n:page|pages}",
                blank_summary="{n} of {total} {total:page|pages} will be removed.", delete_all="You cannot remove every page.", delete_label="Pages to remove",
                blank_done="{n} {n:page was|pages were} removed. {left} {left:page is|pages are} left.", out_suffix="no-blank-pages"),
    ),
}

# ------------------------------------------------------------------ pages per sheet
TOOLS4["nup"] = {
    "sv": dict(
        title="Flera sidor per ark i PDF – 2, 4, 6 eller 9 | Retypee",
        desc="Lägg 2, 4, 6 eller 9 PDF-sidor på varje ark och spara papper vid utskrift. Välj pappersstorlek och ram. Gratis och utan uppladdning.",
        h1="Flera sidor per ark – *spara papper* vid utskrift.",
        lede="Lägg 2, 4, 6 eller 9 sidor på varje ark. Du ser hur arket delas upp medan du väljer, och ny PDF skapas direkt i webbläsaren.",
        steps_h2="Så lägger du flera sidor på ett ark",
        steps=[("Öppna PDF-filen.", "Släpp den på sidan."),
               ("Välj upplägg.", "Hur många sidor per ark, pappersstorlek, riktning och om varje sida ska ha en tunn ram."),
               ("Skapa och ladda ner.", "Sidorna läggs ut rad för rad. Du får en ny PDF med färre ark.")],
        sections=[
            {"h2": "Bra för", "ul": [
                "Att skriva ut föreläsningsbilder, två eller sex på varje ark.",
                "Att läsa igenom ett långt dokument på lite papper.",
                "Att få en överblick över alla sidor på ett ark."]},
            {"h2": "Så läggs sidorna ut", "p": [
                "Sidorna placeras från vänster till höger, rad för rad. Med automatisk riktning väljer Retypee stående eller liggande ark, och den rutnätsindelning som ger störst sidor. Två stående sidor hamnar alltså bredvid varandra på ett liggande ark."]},
            {"h2": "Bra att veta", "ul": [
                "Sidor med olika storlek passas in var och en i sin ruta utan att förvrängas.",
                "Vridna sidor visas rätt väg.",
                "Texten blir mindre, så med 9 sidor per ark kan småtext vara svår att läsa.",
                "Behöver du bara ändra pappersstorlek, använd {{link:resize}}.",
                "Vill du ändra sidornas ordning först, använd {{link:organize}}."]},
        ],
        faq_h2="Vanliga frågor om flera sidor per ark",
        faq=[("Hur skriver jag ut flera sidor per ark från en PDF?", "Öppna filen här, välj hur många sidor du vill ha per ark och klicka på Skapa ark. Skriv sedan ut den nya PDF-filen som vanligt."),
             ("Vilka upplägg finns?", "2, 4, 6 och 9 sidor per ark, på A4, Letter eller A3, stående eller liggande."),
             ("Blir sidorna förvrängda?", "Nej. Varje sida skalas med bibehållna proportioner och centreras i sin ruta."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["resize", "organize", "split", "merge"],
        ui=dict(nup_btn="Skapa ark", nup_per="Sidor per ark", nup_size="Arkstorlek", nup_turn="Arkets riktning", nup_auto="Automatiskt", nup_portrait="Stående",
                nup_landscape="Liggande", nup_border="Tunn ram runt varje sida", nup_info="{pages} {pages:sida|sidor} blir {sheets} {sheets:ark|ark}.",
                nup_done="{n} {n:sida|sidor} lades på {sheets} {sheets:ark|ark}.", out_suffix="flera-per-ark"),
    ),
    "en": dict(
        title="Multiple Pages per Sheet PDF – 2, 4, 6 or 9 | Retypee",
        desc="Put 2, 4, 6 or 9 PDF pages on each sheet and save paper when printing. Choose paper size and border. Free, and nothing is uploaded.",
        h1="Multiple pages per sheet – *save paper* when printing.",
        lede="Put 2, 4, 6 or 9 pages on each sheet. You see how the sheet is divided while you choose, and the new PDF is made right in your browser.",
        steps_h2="How to put several pages on one sheet",
        steps=[("Open the PDF.", "Drop it on the page."),
               ("Choose the layout.", "How many pages per sheet, paper size, direction and whether each page gets a thin border."),
               ("Create and download.", "The pages are laid out row by row. You get a new PDF with fewer sheets.")],
        sections=[
            {"h2": "Good for", "ul": [
                "Printing lecture slides, two or six to a sheet.",
                "Reading through a long document on little paper.",
                "Getting an overview of every page on one sheet."]},
            {"h2": "How the pages are laid out", "p": [
                "The pages are placed from left to right, row by row. With automatic direction Retypee chooses a portrait or landscape sheet, and the grid that gives the biggest pages. Two portrait pages therefore end up side by side on a landscape sheet."]},
            {"h2": "Good to know", "ul": [
                "Pages of different sizes are each fitted into their own cell without distortion.",
                "Rotated pages are shown the right way up.",
                "The text gets smaller, so with 9 pages per sheet small print can be hard to read.",
                "If you only need to change the paper size, use {{link:resize}}.",
                "If you want to change the order of the pages first, use {{link:organize}}."]},
        ],
        faq_h2="Questions about multiple pages per sheet",
        faq=[("How do I print several pages per sheet from a PDF?", "Open the file here, choose how many pages you want per sheet and click Create sheets. Then print the new PDF as usual."),
             ("Which layouts are there?", "2, 4, 6 and 9 pages per sheet, on A4, Letter or A3, portrait or landscape."),
             ("Do the pages get distorted?", "No. Each page is scaled in proportion and centred in its cell."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["resize", "organize", "split", "merge"],
        ui=dict(nup_btn="Create sheets", nup_per="Pages per sheet", nup_size="Sheet size", nup_turn="Sheet direction", nup_auto="Automatic", nup_portrait="Portrait",
                nup_landscape="Landscape", nup_border="Thin border around each page", nup_info="{pages} {pages:page becomes|pages become} {sheets} {sheets:sheet|sheets}.",
                nup_done="{n} {n:page was|pages were} put on {sheets} {sheets:sheet|sheets}.", out_suffix="multi-up"),
    ),
}

# ------------------------------------------------------------------ resize pages
TOOLS4["resize"] = {
    "sv": dict(
        title="Ändra sidstorlek i PDF – till A4, Letter m.fl. | Retypee",
        desc="Gör om alla sidor i en PDF till A4, A3, A5, Letter eller Legal. Innehållet skalas utan att förvrängas. Gratis och utan uppladdning.",
        h1="Ändra sidstorlek i en PDF – *till A4* eller annan storlek.",
        lede="Blandade sidstorlekar eller fel pappersformat? Retypee passar in varje sida på ett ark av den storlek du väljer, utan att förvränga innehållet.",
        steps_h2="Så ändrar du sidstorlek i en PDF",
        steps=[("Öppna PDF-filen.", "Du ser vilka storlekar sidorna har nu."),
               ("Välj ny storlek.", "A4, A3, A5, Letter eller Legal, och om sidornas riktning ska behållas."),
               ("Ändra och ladda ner.", "Varje sida skalas så att den får plats och centreras på arket.")],
        sections=[
            {"h2": "Vanliga användningar", "ul": [
                "Göra en amerikansk Letter-PDF till A4 före utskrift.",
                "Få alla sidor i en sammanslagen fil lika stora.",
                "Förstora ett A5-häfte till A4 eller tvärtom."]},
            {"h2": "Så skalas sidorna", "p": [
                "Varje sida förstoras eller förminskas så att hela sidan syns, med bibehållna proportioner, och placeras mitt på det nya arket. Skiljer sig formatet blir det vita kanter. Inget beskärs."]},
            {"h2": "Bra att veta", "ul": [
                "Liggande sidor förblir liggande om du inte väljer annat.",
                "Du kan lägga till en marginal runt innehållet.",
                "Text och grafik behåller sin kvalitet, eftersom sidorna skalas som vektorer.",
                "Vill du klippa bort kanter i stället, använd {{link:crop}}.",
                "Flera sidor på ett ark? Använd {{link:nup}}."]},
        ],
        faq_h2="Vanliga frågor om att ändra sidstorlek",
        faq=[("Hur gör jag om en PDF till A4?", "Öppna filen här, välj A4 och klicka på Ändra sidstorlek. Varje sida skalas in på ett A4-ark."),
             ("Förvrängs innehållet?", "Nej. Proportionerna bevaras, och om formatet skiljer sig får sidan vita kanter."),
             ("Kan jag göra alla sidor liggande?", "Ja. Välj Liggande under Riktning, annars behåller varje sida sin riktning."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["nup", "crop", "merge", "compress"],
        ui=dict(rs_btn="Ändra sidstorlek", rs_now="Sidorna är nu: {sizes}.", rs_size="Ny storlek", rs_turn="Riktning", rs_keep="Behåll varje sidas riktning",
                nup_portrait="Stående", nup_landscape="Liggande", img_margin="Marginal", margin_none="Ingen", margin_small="Liten", margin_big="Stor",
                rs_done="{n} {n:sida|sidor} har nu storleken {size}.", out_suffix="omskalad"),
    ),
    "en": dict(
        title="Resize PDF Pages – to A4, Letter and More | Retypee",
        desc="Turn every page of a PDF into A4, A3, A5, Letter or Legal. The content is scaled without distortion. Free, and nothing is uploaded.",
        h1="Resize the pages of a PDF – *to A4* or another size.",
        lede="Mixed page sizes or the wrong paper format? Retypee fits every page onto a sheet of the size you choose, without distorting the content.",
        steps_h2="How to change the page size of a PDF",
        steps=[("Open the PDF.", "You see which sizes the pages have now."),
               ("Choose the new size.", "A4, A3, A5, Letter or Legal, and whether the direction of the pages is kept."),
               ("Resize and download.", "Each page is scaled to fit and centred on the sheet.")],
        sections=[
            {"h2": "Common uses", "ul": [
                "Turn a US Letter PDF into A4 before printing.",
                "Make every page of a merged file the same size.",
                "Enlarge an A5 booklet to A4 or the other way round."]},
            {"h2": "How the pages are scaled", "p": [
                "Each page is enlarged or reduced so the whole page shows, in proportion, and placed in the middle of the new sheet. If the format differs you get white edges. Nothing is cropped."]},
            {"h2": "Good to know", "ul": [
                "Landscape pages stay landscape unless you choose otherwise.",
                "You can add a margin around the content.",
                "Text and graphics keep their quality, because the pages are scaled as vectors.",
                "If you want to cut away edges instead, use {{link:crop}}.",
                "Several pages on one sheet? Use {{link:nup}}."]},
        ],
        faq_h2="Questions about resizing PDF pages",
        faq=[("How do I turn a PDF into A4?", "Open the file here, choose A4 and click Resize pages. Each page is scaled onto an A4 sheet."),
             ("Is the content distorted?", "No. The proportions are kept, and if the format differs the page gets white edges."),
             ("Can I make every page landscape?", "Yes. Choose Landscape under Direction, otherwise each page keeps its direction."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["nup", "crop", "merge", "compress"],
        ui=dict(rs_btn="Resize pages", rs_now="The pages are now: {sizes}.", rs_size="New size", rs_turn="Direction", rs_keep="Keep each page's direction",
                nup_portrait="Portrait", nup_landscape="Landscape", img_margin="Margin", margin_none="None", margin_small="Small", margin_big="Large",
                rs_done="{n} {n:page is|pages are} now {size}.", out_suffix="resized"),
    ),
}

# ------------------------------------------------------------------ extract images
TOOLS4["extract-images"] = {
    "sv": dict(
        title="Extrahera bilder ur PDF – hämta alla bilder | Retypee",
        desc="Hämta alla bilder ur en PDF i originalkvalitet som en ZIP-fil. Hoppa över små ikoner. Gratis, i webbläsaren och utan uppladdning.",
        h1="Extrahera bilder ur en PDF – *i originalkvalitet*.",
        lede="Hämta fotona och bilderna som ligger i en PDF, utan att göra skärmdumpar. Du får dem som en ZIP-fil, precis som de är lagrade i dokumentet.",
        steps_h2="Så hämtar du bilderna ur en PDF",
        steps=[("Öppna PDF-filen.", "Retypee räknar bilderna i filen."),
               ("Välj storlek.", "Hoppa över små bilder, ofta ikoner och dekorationer, eller hämta bara de stora."),
               ("Hämta ZIP-filen.", "Alla bilderna ligger i en ZIP, namngivna efter sidan de satt på.")],
        sections=[
            {"h2": "Så fungerar det", "p": [
                "En PDF lagrar sina bilder som egna objekt. Retypee läser dem direkt ur filen. JPEG-bilder kopieras tecken för tecken, utan att komprimeras om, så kvaliteten är exakt den i dokumentet. Bilder med genomskinlighet, och färgformat som webbläsare inte visar, sparas som PNG."]},
            {"h2": "Det här får du inte", "ul": [
                "Sidor som är inskannade är en enda bild per sida, och det är den du får. För sidor som bilder, använd {{link:pdf-to-jpg}}.",
                "Diagram och logotyper ritade som vektorer är inte bilder och följer inte med.",
                "Samma bild som används på flera sidor hämtas bara en gång."]},
            {"h2": "Bra att veta", "ul": [
                "Bilderna heter bild-sida-nummer, till exempel bild-3-1.jpg.",
                "Lösenordsskyddade filer måste låsas upp först, använd {{link:unlock}}.",
                "PDF-motorn (cirka 25 MB) hämtas första gången du använder verktyget."]},
        ],
        faq_h2="Vanliga frågor om att hämta bilder ur PDF",
        faq=[("Hur får jag ut bilderna ur en PDF?", "Öppna filen här, välj storlek och klicka på Hämta bilderna som ZIP. Du får alla bilder i originalkvalitet."),
             ("Blir bildkvaliteten sämre?", "Nej. JPEG-bilder kopieras direkt ur filen utan att komprimeras om."),
             ("Varför hittades inga bilder?", "Dokumentet kanske bara har text och vektorgrafik. Har du sänkt gränsen för små bilder kan du prova Alla bilder."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["pdf-to-jpg", "compress", "ocr", "pdf-to-text"],
        ui=dict(img_hint="Alla bilder i filen hämtas i originalkvalitet. Bilder med genomskinlighet sparas som PNG.", img_smallest="Storlek", img_all="Alla bilder",
                img_skip_small="Hoppa över små (under 100 px, ofta ikoner)", img_only_large="Bara stora (över 300 px)", img_found="{n} {n:bild|bilder} hittades på {pages} {pages:sida|sidor}.",
                img_none="Inga bilder av den storleken hittades.", img_get="Hämta {n} {n:bild|bilder} som ZIP", img_done="Bilderna ligger i ZIP-filen.", out_suffix="bilder"),
    ),
    "en": dict(
        title="Extract Images from PDF – Get Every Picture | Retypee",
        desc="Get every image out of a PDF in original quality as a ZIP file. Skip tiny icons. Free, in your browser and without uploading.",
        h1="Extract images from a PDF – *in original quality*.",
        lede="Get the photos and pictures inside a PDF without taking screenshots. You get them as a ZIP file, exactly as they are stored in the document.",
        steps_h2="How to get the images out of a PDF",
        steps=[("Open the PDF.", "Retypee counts the images in the file."),
               ("Choose a size.", "Skip small images, often icons and decorations, or get only the large ones."),
               ("Get the ZIP.", "All the images are in a ZIP, named after the page they were on.")],
        sections=[
            {"h2": "How it works", "p": [
                "A PDF stores its images as separate objects. Retypee reads them straight from the file. JPEG images are copied byte for byte, without being compressed again, so the quality is exactly what is in the document. Images with transparency, and colour formats browsers cannot show, are saved as PNG."]},
            {"h2": "What you do not get", "ul": [
                "Scanned pages are a single image per page, and that is what you get. For pages as pictures, use {{link:pdf-to-jpg}}.",
                "Charts and logos drawn as vectors are not images and do not come along.",
                "The same image used on several pages is only extracted once."]},
            {"h2": "Good to know", "ul": [
                "The images are named image-page-number, for example image-3-1.jpg.",
                "Password-protected files have to be unlocked first, use {{link:unlock}}.",
                "The PDF engine (about 25 MB) is downloaded the first time you use the tool."]},
        ],
        faq_h2="Questions about getting images out of PDFs",
        faq=[("How do I get the images out of a PDF?", "Open the file here, choose a size and click Get the images as ZIP. You get every image in original quality."),
             ("Does the image quality get worse?", "No. JPEG images are copied straight out of the file without being compressed again."),
             ("Why were no images found?", "The document may only have text and vector graphics. If you set a limit for small images, try All images."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["pdf-to-jpg", "compress", "ocr", "pdf-to-text"],
        ui=dict(img_hint="Every image in the file is extracted in original quality. Images with transparency are saved as PNG.", img_smallest="Size", img_all="All images",
                img_skip_small="Skip small ones (under 100 px, often icons)", img_only_large="Only large ones (over 300 px)", img_found="{n} {n:image was|images were} found on {pages} {pages:page|pages}.",
                img_none="No images of that size were found.", img_get="Get {n} {n:image|images} as ZIP", img_done="The images are in the ZIP file.", out_suffix="images"),
    ),
}

# ------------------------------------------------------------------ repair
TOOLS4["repair"] = {
    "sv": dict(
        title="Reparera PDF – rädda en fil som inte går att öppna | Retypee",
        desc="Reparera en trasig PDF som inte går att öppna eller visar fel. Filen läses i webbläsaren och laddas aldrig upp. Gratis.",
        h1="Reparera en PDF – *rädda filen* som inte går att öppna.",
        lede="Avbruten nedladdning, trasig bilaga eller felmeddelande i läsaren? Retypee läser filen på det tillåtande sättet, bygger upp strukturen på nytt och sparar en ren kopia.",
        steps_h2="Så reparerar du en PDF",
        steps=[("Öppna den trasiga PDF-filen.", "Retypee kontrollerar om filen är skadad och hur många sidor som går att läsa."),
               ("Reparera.", "Strukturen byggs upp på nytt utifrån de sidor som finns kvar."),
               ("Ladda ner.", "Du får en ny, ren PDF som öppnas som vanligt.")],
        sections=[
            {"h2": "Det här kan repareras", "ul": [
                "Filer som blivit avklippta, till exempel av en avbruten nedladdning eller överföring.",
                "Filer med trasig innehållsförteckning (xref), som läsare klagar på.",
                "Filer som sparats av program med buggar."]},
            {"h2": "Det här kan inte repareras", "ul": [
                "Sidor vars innehåll helt saknas. Du får de sidor som går att läsa.",
                "Filer som inte är PDF, eller som är helt förstörda.",
                "Lösenordsskyddade filer behöver först låsas upp med {{link:unlock}}."]},
            {"h2": "Bra att veta", "ul": [
                "Originalet ändras aldrig. Du laddar ner en kopia.",
                "Är filen inte skadad får du ändå en ren, omskriven kopia, ibland med mindre filstorlek.",
                "Vill du göra den ännu mindre, använd {{link:compress}}.",
                "PDF-motorn (cirka 25 MB) hämtas första gången du använder verktyget."]},
        ],
        faq_h2="Vanliga frågor om att reparera PDF",
        faq=[("Hur reparerar jag en PDF som inte går att öppna?", "Öppna filen här och klicka på Reparera och spara. Retypee bygger upp filen på nytt och du laddar ner en fungerande kopia."),
             ("Kan alla trasiga PDF-filer repareras?", "Nej. Är filen avklippt eller har trasig struktur går det ofta bra, men sidor vars innehåll saknas går inte att få tillbaka."),
             ("Ändras min originalfil?", "Nej. Du får en ny kopia och originalet rörs inte."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["compress", "unlock", "merge", "pdf-to-text"],
        ui=dict(repair_fail="Filen är för skadad för att kunna repareras.", repair_was_broken="Filen var skadad, men Retypee kunde läsa {n} {n:sida|sidor} och bygga upp den på nytt.",
                repair_looks_fine="Filen verkar inte vara skadad ({n} {n:sida|sidor}). Du kan ändå spara en ren kopia.", repair_btn="Reparera och spara",
                repair_done="{n} {n:sida|sidor} räddades. Ny filstorlek: {size}.", out_suffix="reparerad"),
    ),
    "en": dict(
        title="Repair PDF – Rescue a File That Will Not Open | Retypee",
        desc="Repair a broken PDF that will not open or shows errors. The file is read in your browser and never uploaded. Free.",
        h1="Repair a PDF – *rescue the file* that will not open.",
        lede="An interrupted download, a broken attachment or an error message in the reader? Retypee reads the file the forgiving way, rebuilds the structure and saves a clean copy.",
        steps_h2="How to repair a PDF",
        steps=[("Open the broken PDF.", "Retypee checks whether the file is damaged and how many pages can be read."),
               ("Repair.", "The structure is rebuilt from the pages that are left."),
               ("Download.", "You get a new, clean PDF that opens as usual.")],
        sections=[
            {"h2": "What can be repaired", "ul": [
                "Files that were cut short, for example by an interrupted download or transfer.",
                "Files with a broken index (xref) that readers complain about.",
                "Files saved by programs with bugs."]},
            {"h2": "What cannot be repaired", "ul": [
                "Pages whose content is missing altogether. You get the pages that can be read.",
                "Files that are not PDFs, or that are completely destroyed.",
                "Password-protected files first need unlocking with {{link:unlock}}."]},
            {"h2": "Good to know", "ul": [
                "The original is never changed. You download a copy.",
                "If the file is not damaged you still get a clean, rewritten copy, sometimes with a smaller file size.",
                "If you want to make it smaller still, use {{link:compress}}.",
                "The PDF engine (about 25 MB) is downloaded the first time you use the tool."]},
        ],
        faq_h2="Questions about repairing PDFs",
        faq=[("How do I repair a PDF that will not open?", "Open the file here and click Repair and save. Retypee rebuilds the file and you download a working copy."),
             ("Can every broken PDF be repaired?", "No. If the file was cut short or has a broken structure it often works, but pages whose content is missing cannot be brought back."),
             ("Is my original file changed?", "No. You get a new copy and the original is not touched."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["compress", "unlock", "merge", "pdf-to-text"],
        ui=dict(repair_fail="The file is too damaged to repair.", repair_was_broken="The file was damaged, but Retypee could read {n} {n:page|pages} and rebuild it.",
                repair_looks_fine="The file does not seem to be damaged ({n} {n:page|pages}). You can still save a clean copy.", repair_btn="Repair and save",
                repair_done="{n} {n:page was|pages were} rescued. New file size: {size}.", out_suffix="repaired"),
    ),
}

# ------------------------------------------------------------------ flatten
TOOLS4["flatten"] = {
    "sv": dict(
        title="Platta ut PDF – gör kommentarer och fält fasta | Retypee",
        desc="Platta ut en PDF så att kommentarer, markeringar och ifyllda formulärfält blir en fast del av sidorna. Gratis och utan uppladdning.",
        h1="Platta ut en PDF – *gör kommentarer och fält fasta*.",
        lede="Efter utplattningen är kommentarer, markeringar och ifyllda formulärfält en del av sidan och går inte längre att ändra. Det passar när du ska skicka in eller arkivera filen.",
        steps_h2="Så plattar du ut en PDF",
        steps=[("Öppna PDF-filen.", "Retypee räknar kommentarerna och formulärfälten i filen."),
               ("Välj vad som ska plattas ut.", "Kommentarer och markeringar, formulärfält, eller båda."),
               ("Platta ut och ladda ner.", "Du får en ny PDF där det du valde är en del av sidorna.")],
        sections=[
            {"h2": "Varför platta ut", "ul": [
                "Ett ifyllt formulär ska skickas in och inte kunna ändras.",
                "Markeringar och kommentarer ska synas i alla läsare och vid utskrift.",
                "Filen ska arkiveras i ett slutligt skick."]},
            {"h2": "Skillnaden mot att låsa", "p": [
                "Ett lösenord eller en begränsning kan tas bort av den som har verktygen. Utplattade fält är i stället ritade på sidan. Fälten finns inte längre, bara det de visade. Den som vill ändra måste redigera själva sidan."]},
            {"h2": "Bra att veta", "ul": [
                "Utplattningen går inte att ångra. Spara originalfilen om du behöver fälten igen.",
                "Länkar i dokumentet påverkas inte.",
                "Har du inte fyllt i formuläret än, använd {{link:fill-form}} först. Där finns även ett val för att platta ut direkt.",
                "Lösenordsskyddade filer måste låsas upp först, använd {{link:unlock}}.",
                "PDF-motorn (cirka 25 MB) hämtas första gången du använder verktyget."]},
        ],
        faq_h2="Vanliga frågor om att platta ut PDF",
        faq=[("Vad betyder det att platta ut en PDF?", "Kommentarer, markeringar och formulärfält ritas in i själva sidan. De syns likadant men går inte längre att ändra."),
             ("Hur plattar jag ut ett ifyllt formulär?", "Öppna filen här, kryssa i formulärfält och klicka på Platta ut PDF. Du får en kopia där svaren är fasta."),
             ("Går det att ångra?", "Nej. Spara originalfilen om du vill kunna ändra svaren senare."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["fill-form", "protect", "redact", "sign"],
        ui=dict(flat_nothing="Filen har inga kommentarer, markeringar eller formulärfält att platta ut.", flat_hint="Välj vad som ska bli en fast del av sidorna.",
                flat_annots="Kommentarer och markeringar ({n})", flat_widgets="Formulärfält ({n})", flat_btn="Platta ut PDF",
                flat_done="Klart. Det du valde är nu en del av sidorna och går inte att ändra.", out_suffix="utplattad"),
    ),
    "en": dict(
        title="Flatten PDF – Make Comments and Fields Permanent | Retypee",
        desc="Flatten a PDF so comments, highlights and filled-in form fields become a permanent part of the pages. Free, and nothing is uploaded.",
        h1="Flatten a PDF – *make comments and fields permanent*.",
        lede="After flattening, comments, highlights and filled-in form fields are part of the page and can no longer be changed. It suits a file you are about to send in or archive.",
        steps_h2="How to flatten a PDF",
        steps=[("Open the PDF.", "Retypee counts the comments and form fields in the file."),
               ("Choose what to flatten.", "Comments and highlights, form fields, or both."),
               ("Flatten and download.", "You get a new PDF where what you chose is part of the pages.")],
        sections=[
            {"h2": "Why flatten", "ul": [
                "A filled-in form is going to be sent in and must not be changeable.",
                "Highlights and comments should show in every reader and when printed.",
                "The file is being archived in its final state."]},
            {"h2": "How it differs from locking", "p": [
                "A password or a restriction can be removed by anyone with the tools. Flattened fields are instead drawn on the page. The fields no longer exist, only what they showed. Whoever wants to change them has to edit the page itself."]},
            {"h2": "Good to know", "ul": [
                "Flattening cannot be undone. Keep the original file if you need the fields again.",
                "Links in the document are not affected.",
                "If you have not filled in the form yet, use {{link:fill-form}} first. It also has an option to flatten straight away.",
                "Password-protected files have to be unlocked first, use {{link:unlock}}.",
                "The PDF engine (about 25 MB) is downloaded the first time you use the tool."]},
        ],
        faq_h2="Questions about flattening PDFs",
        faq=[("What does it mean to flatten a PDF?", "Comments, highlights and form fields are drawn into the page itself. They look the same but can no longer be changed."),
             ("How do I flatten a filled-in form?", "Open the file here, tick form fields and click Flatten PDF. You get a copy where the answers are fixed."),
             ("Can it be undone?", "No. Keep the original file if you want to change the answers later."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["fill-form", "protect", "redact", "sign"],
        ui=dict(flat_nothing="The file has no comments, highlights or form fields to flatten.", flat_hint="Choose what should become a permanent part of the pages.",
                flat_annots="Comments and highlights ({n})", flat_widgets="Form fields ({n})", flat_btn="Flatten PDF",
                flat_done="Done. What you chose is now part of the pages and cannot be changed.", out_suffix="flattened"),
    ),
}
