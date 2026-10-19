"""Wave 6 tool pages (page order, blank pages, booklet, auto-crop, grayscale, PNG variants)."""
from content_tools import TOOLS as BASE

TOOLS6 = {}

# ------------------------------------------------------------------ reverse
TOOLS6["reverse"] = {
    "sv": dict(
        title="Vänd ordning på PDF-sidor, sätt ihop skanningar | Retypee",
        desc="Vänd sidornas ordning i en PDF, eller sätt ihop framsidor och baksidor efter dubbelsidig skanning med enkelsidig skanner. Gratis, utan uppladdning.",
        h1="Vänd ordningen på sidorna i en PDF – *eller sätt ihop skanningar*.",
        lede="Sista sidan först, eller framsidor och baksidor i rätt följd. Välj hur sidorna ska ordnas så skapas en ny PDF direkt i din webbläsare.",
        steps_h2="Så vänder du ordningen på sidorna",
        steps=[("Öppna PDF-filen.", "Släpp den på sidan."),
               ("Välj omordning.", "Omvänd ordning, eller sätt ihop framsidor och baksidor."),
               ("Skapa och ladda ner.", "Du får en ny PDF med sidorna i den nya ordningen.")],
        sections=[
            {"h2": "Omvänd ordning", "p": [
                "Sista sidan blir första, näst sista blir andra, och så vidare. Det passar när ett dokument har skannats eller sparats baklänges, eller när du ska skriva ut en bunt som ska läggas i omvänd följd."]},
            {"h2": "Sätt ihop framsidor och baksidor", "p": [
                "Har du ett dubbelsidigt original och bara en enkelsidig skanner skannar du först alla framsidor, vänder bunten och skannar baksidorna. Då hamnar baksidorna i omvänd ordning i filen. Det här valet vävar ihop dem: framsida 1, sista sidan, framsida 2, näst sista sidan, och så vidare. Filen behöver ha lika många fram- som baksidor."]},
            {"h2": "Bra att veta", "ul": [
                "Sidornas innehåll och storlek ändras inte, bara ordningen.",
                "Vill du flytta enstaka sidor eller vrida dem, använd {{link:organize}}.",
                "Har du skannat med en kamera, börja med {{link:scan}}.",
                "Inga sidor tas bort. För tomma baksidor finns {{link:blank}}."]},
        ],
        faq_h2="Vanliga frågor om att vända ordningen på PDF-sidor",
        faq=[("Hur vänder jag ordningen på sidorna i en PDF?", "Öppna filen här, välj Omvänd ordning och klicka på Ändra ordningen. Du laddar ner en ny PDF där sista sidan kommer först."),
             ("Hur sätter jag ihop fram- och baksidor från en skanning?", "Välj Sätt ihop framsidor och baksidor. Filen ska ha alla framsidor först och alla baksidor i omvänd ordning efteråt."),
             ("Varför går det inte att sätta ihop min fil?", "Det kräver ett jämnt antal sidor. Har en sida saknats vid skanningen, lägg in en tom sida först med Lägg till tomma sidor."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["organize", "scan", "blank", "add-blank"],
        ui=dict(rv_btn="Ändra ordningen", rv_reverse="Omvänd ordning", rv_reverse_d="Sista sidan blir första sidan, och så vidare.",
                rv_collate="Sätt ihop framsidor och baksidor", rv_collate_d="Filen har alla framsidor först och sedan alla baksidor i omvänd ordning, som efter skanning av ett dubbelsidigt original med en enkelsidig skanner.",
                rv_odd="Det här kräver ett jämnt antal sidor, lika många fram- som baksidor.", rv_order="Ny ordning: {list}", rv_done="{n} {n:sida|sidor} lades i den nya ordningen.", out_suffix="omvand-ordning"),
    ),
    "en": dict(
        title="Reverse PDF Page Order – or Collate Scans | Retypee",
        desc="Reverse the page order of a PDF, or put front and back scans together after double-sided scanning with a single-sided scanner. Free, no upload.",
        h1="Reverse the page order of a PDF – *or collate scans*.",
        lede="Last page first, or fronts and backs in the right sequence. Choose how the pages should be ordered and a new PDF is made right in your browser.",
        steps_h2="How to reverse the order of the pages",
        steps=[("Open the PDF.", "Drop it on the page."),
               ("Choose the reordering.", "Reverse order, or collate fronts and backs."),
               ("Create and download.", "You get a new PDF with the pages in the new order.")],
        sections=[
            {"h2": "Reverse order", "p": [
                "The last page becomes the first, the one before it becomes the second, and so on. It suits a document that was scanned or saved backwards, or a stack that has to be laid out in reverse."]},
            {"h2": "Collate fronts and backs", "p": [
                "If you have a double-sided original and only a single-sided scanner, you scan all the fronts first, flip the stack and scan the backs. The backs then end up in reverse order in the file. This option weaves them together: front 1, the last page, front 2, the one before last, and so on. The file needs as many fronts as backs."]},
            {"h2": "Good to know", "ul": [
                "The content and size of the pages do not change, only the order.",
                "If you want to move single pages or turn them, use {{link:organize}}.",
                "If you scanned with a camera, start with {{link:scan}}.",
                "No pages are removed. For blank backs there is {{link:blank}}."]},
        ],
        faq_h2="Questions about reversing PDF page order",
        faq=[("How do I reverse the order of the pages in a PDF?", "Open the file here, choose Reverse order and click Change the order. You download a new PDF with the last page first."),
             ("How do I put fronts and backs together from a scan?", "Choose Collate fronts and backs. The file should have all the fronts first and all the backs in reverse order after them."),
             ("Why can my file not be collated?", "It needs an even number of pages. If a page was missed in the scan, add a blank one first with Add blank pages."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["organize", "scan", "blank", "add-blank"],
        ui=dict(rv_btn="Change the order", rv_reverse="Reverse order", rv_reverse_d="The last page becomes the first, and so on.",
                rv_collate="Collate fronts and backs", rv_collate_d="The file has all the fronts first and then all the backs in reverse order, as after scanning a double-sided original with a single-sided scanner.",
                rv_odd="This needs an even number of pages, as many fronts as backs.", rv_order="New order: {list}", rv_done="{n} {n:page was|pages were} put in the new order.", out_suffix="reversed"),
    ),
}

# ------------------------------------------------------------------ add blank pages
TOOLS6["add-blank"] = {
    "sv": dict(
        title="Lägg till tomma sidor i PDF – var du vill | Retypee",
        desc="Lägg in tomma sidor i en PDF, till exempel efter varje sida eller före ett kapitel. Du markerar var på miniatyrer. Gratis och utan uppladdning.",
        h1="Lägg till tomma sidor i en PDF – *precis där du vill*.",
        lede="Markera sidorna som en tom sida ska följa efter, eller välj varannan eller varje sida. Du ser alla sidor som miniatyrer.",
        steps_h2="Så lägger du till tomma sidor",
        steps=[("Öppna PDF-filen.", "Sidorna visas som miniatyrer."),
               ("Markera var.", "Klicka på sidorna som en tom sida ska läggas efter, eller använd genvägarna för varje, udda eller jämna sidor."),
               ("Skapa och ladda ner.", "Du får en ny PDF med de tomma sidorna inlagda.")],
        sections=[
            {"h2": "Vanliga användningar", "ul": [
                "En tom sida mellan kapitel, så att varje kapitel börjar på en högersida.",
                "En tom sida efter varje sida, för anteckningar vid utskrift.",
                "Att fylla ut ett dokument till ett jämnt antal sidor inför dubbelsidig utskrift eller ett häfte.",
                "En tom sida först, som försättsblad att fylla i."]},
            {"h2": "Bra att veta", "ul": [
                "Den tomma sidan blir lika stor som sidan den följer efter.",
                "Det går att lägga en tom sida före första sidan med en egen ruta.",
                "Vill du skapa ett häfte, använd {{link:booklet}}, som fyller ut med tomma sidor själv.",
                "Vill du ta bort tomma sidor i stället, använd {{link:blank}}."]},
        ],
        faq_h2="Vanliga frågor om att lägga till tomma sidor i PDF",
        faq=[("Hur lägger jag in en tom sida i en PDF?", "Öppna filen här, klicka på sidan som den tomma sidan ska följa efter och klicka på Lägg till. Du får en ny PDF."),
             ("Kan jag lägga en tom sida efter varje sida?", "Ja. Använd genvägen Efter varje sida, eller Efter udda sidor om du bara vill ha dem då."),
             ("Hur lägger jag en tom sida först?", "Kryssa i Lägg även en tom sida först."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["blank", "organize", "booklet", "reverse"],
        ui=dict(ab_hint="Markera sidorna som en tom sida ska läggas efter.", ab_every="Efter varje sida", ab_odd="Efter udda sidor", ab_even="Efter jämna sidor", ab_clear="Rensa",
                ab_first="Lägg även en tom sida först", ab_btn="Lägg till {n} {n:tom sida|tomma sidor}", ab_summary="{n} {n:tom sida|tomma sidor} läggs till. Nya filen får {total} sidor.",
                ab_none="Markera minst en sida.", ab_done="{n} {n:tom sida|tomma sidor} lades till.", out_suffix="med-tomma-sidor"),
    ),
    "en": dict(
        title="Add Blank Pages to PDF – Where You Want Them | Retypee",
        desc="Insert blank pages in a PDF, for example after every page or before a chapter. You mark the spots on thumbnails. Free, and nothing is uploaded.",
        h1="Add blank pages to a PDF – *exactly where you want them*.",
        lede="Mark the pages a blank page should follow, or choose every other page or every page. You see all the pages as thumbnails.",
        steps_h2="How to add blank pages",
        steps=[("Open the PDF.", "The pages are shown as thumbnails."),
               ("Mark where.", "Click the pages a blank page should follow, or use the shortcuts for every, odd or even pages."),
               ("Create and download.", "You get a new PDF with the blank pages inserted.")],
        sections=[
            {"h2": "Common uses", "ul": [
                "A blank page between chapters, so that each chapter starts on a right-hand page.",
                "A blank page after every page, for notes when printing.",
                "Padding a document to an even number of pages for double-sided printing or a booklet.",
                "A blank page at the start, as a cover to fill in."]},
            {"h2": "Good to know", "ul": [
                "The blank page is as big as the page it follows.",
                "You can add a blank page before the first page with its own box.",
                "If you want to make a booklet, use {{link:booklet}}, which pads with blank pages by itself.",
                "If you want to remove blank pages instead, use {{link:blank}}."]},
        ],
        faq_h2="Questions about adding blank pages to PDFs",
        faq=[("How do I insert a blank page in a PDF?", "Open the file here, click the page the blank page should follow and click Add. You get a new PDF."),
             ("Can I add a blank page after every page?", "Yes. Use the shortcut After every page, or After odd pages if you only want them there."),
             ("How do I add a blank page at the start?", "Tick Also add a blank page first."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["blank", "organize", "booklet", "reverse"],
        ui=dict(ab_hint="Mark the pages a blank page should be added after.", ab_every="After every page", ab_odd="After odd pages", ab_even="After even pages", ab_clear="Clear",
                ab_first="Also add a blank page first", ab_btn="Add {n} blank {n:page|pages}", ab_summary="{n} blank {n:page is|pages are} added. The new file has {total} pages.",
                ab_none="Mark at least one page.", ab_done="{n} blank {n:page was|pages were} added.", out_suffix="with-blanks"),
    ),
}

# ------------------------------------------------------------------ booklet
TOOLS6["booklet"] = {
    "sv": dict(
        title="Skapa häfte av PDF – utskrift som häfte | Retypee",
        desc="Ordna sidorna i en PDF så att de blir ett häfte vid dubbelsidig utskrift. Sidorna läggs två och två på liggande ark. Gratis och utan uppladdning.",
        h1="Skapa ett häfte av en PDF – *skriv ut, vik, klart*.",
        lede="Retypee lägger sidorna två och två på liggande ark i rätt ordning. Skriv ut dubbelsidigt, vik arken på mitten och lägg dem i varandra, så får du ett häfte.",
        steps_h2="Så gör du ett häfte av en PDF",
        steps=[("Öppna PDF-filen.", "Sidantalet fylls ut till ett tal som går att dela med fyra, med tomma sidor sist."),
               ("Välj arkstorlek.", "A4 är vanligast. Varje ark rymmer fyra sidor, två på varje sida av pappret."),
               ("Skapa häftet och skriv ut.", "Skriv ut dubbelsidigt och vänd på kortsidan. Vik arken på mitten och lägg dem i varandra.")],
        sections=[
            {"h2": "Så hänger det ihop", "p": [
                "I ett häfte ligger sidorna inte i läsordning på arken. Första arkets framsida har sista och första sidan bredvid varandra, och baksidan har andra och näst sista. Retypee räknar ut den ordningen åt dig, så att sidorna hamnar rätt när arken är vikta och ilagda."]},
            {"h2": "Utskriftsinställningar", "ul": [
                "Skriv ut på 100 % storlek, utan anpassning, så att sidorna inte skalas om.",
                "Välj dubbelsidig utskrift och vänd på kortsidan.",
                "Ett A4-häfte får A5-sidor. Vill du ha andra storlekar, ändra sidorna först med {{link:resize}}."]},
            {"h2": "Bra att veta", "ul": [
                "Antalet sidor fylls ut till ett tal delbart med fyra. De tomma sidorna hamnar sist, så de blir häftets baksida.",
                "Sidor med olika storlek passas in var och en i sin halva utan att förvrängas.",
                "Vill du i stället ha flera sidor på varje ark utan att vika, använd {{link:nup}}.",
                "Vill du kunna styra var de tomma sidorna hamnar, lägg in dem först med {{link:add-blank}}."]},
        ],
        faq_h2="Vanliga frågor om att göra häfte av PDF",
        faq=[("Hur gör jag ett häfte av en PDF?", "Öppna filen här, välj arkstorlek och klicka på Skapa häfte. Skriv ut den nya filen dubbelsidigt, vik arken på mitten och lägg dem i varandra."),
             ("Hur ska jag ställa in skrivaren?", "Dubbelsidig utskrift och vänd på kortsidan, och skriv ut i verklig storlek utan anpassning."),
             ("Vad händer om sidantalet inte går att dela med fyra?", "Tomma sidor läggs till sist så att antalet går jämnt upp."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["nup", "resize", "add-blank", "organize"],
        ui=dict(bk_btn="Skapa häfte", bk_hint="Sidorna läggs två och två på liggande ark i den ordning som blir ett häfte när du skriver ut dubbelsidigt, viker arken på mitten och lägger dem i varandra. Skriv ut dubbelsidigt och vänd på kortsidan.",
                nup_size="Arkstorlek", bk_info="{n} {n:sida|sidor} blir {sheets} {sheets:ark|ark}. {blank} {blank:tom sida|tomma sidor} läggs till sist.",
                bk_done="Häftet har {sheets} {sheets:ark|ark}, alltså {sides} sidor att skriva ut.", out_suffix="hafte"),
    ),
    "en": dict(
        title="Make a Booklet from a PDF – Print as a Booklet | Retypee",
        desc="Order the pages of a PDF so they make a booklet when printed double-sided. Pages are placed two by two on landscape sheets. Free, no upload.",
        h1="Make a booklet from a PDF – *print, fold, done*.",
        lede="Retypee places the pages two by two on landscape sheets in the right order. Print double-sided, fold the sheets in half and nest them, and you have a booklet.",
        steps_h2="How to make a booklet from a PDF",
        steps=[("Open the PDF.", "The page count is padded to a number divisible by four, with blank pages at the end."),
               ("Choose the sheet size.", "A4 is the most common. Each sheet holds four pages, two on each side of the paper."),
               ("Create the booklet and print.", "Print double-sided and flip on the short edge. Fold the sheets in half and nest them.")],
        sections=[
            {"h2": "How it fits together", "p": [
                "In a booklet the pages do not sit in reading order on the sheets. The front of the first sheet has the last and the first page side by side, and the back has the second and the one before last. Retypee works out that order for you, so the pages end up right once the sheets are folded and nested."]},
            {"h2": "Print settings", "ul": [
                "Print at 100% size, without fitting, so the pages are not rescaled.",
                "Choose double-sided printing and flip on the short edge.",
                "An A4 booklet gets A5 pages. If you want other sizes, change the pages first with {{link:resize}}."]},
            {"h2": "Good to know", "ul": [
                "The page count is padded to a number divisible by four. The blank pages go last, so they become the back of the booklet.",
                "Pages of different sizes are each fitted into their own half without distortion.",
                "If you want several pages on each sheet without folding, use {{link:nup}}.",
                "If you want to control where the blank pages go, insert them first with {{link:add-blank}}."]},
        ],
        faq_h2="Questions about making a booklet from a PDF",
        faq=[("How do I make a booklet from a PDF?", "Open the file here, choose the sheet size and click Make booklet. Print the new file double-sided, fold the sheets in half and nest them."),
             ("How should I set up the printer?", "Double-sided printing, flip on the short edge, and print at actual size without fitting."),
             ("What if the page count is not divisible by four?", "Blank pages are added at the end so that it comes out even."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["nup", "resize", "add-blank", "organize"],
        ui=dict(bk_btn="Make booklet", bk_hint="The pages are placed two by two on landscape sheets in the order that makes a booklet when you print double-sided, fold the sheets in half and nest them. Print double-sided and flip on the short edge.",
                nup_size="Sheet size", bk_info="{n} {n:page becomes|pages become} {sheets} {sheets:sheet|sheets}. {blank} blank {blank:page is|pages are} added at the end.",
                bk_done="The booklet has {sheets} {sheets:sheet|sheets}, so {sides} pages to print.", out_suffix="booklet"),
    ),
}

# ------------------------------------------------------------------ auto crop
TOOLS6["autocrop"] = {
    "sv": dict(
        title="Beskär PDF automatiskt – ta bort vita kanter | Retypee",
        desc="Beskär en PDF automatiskt så att de tomma vita kanterna försvinner. Välj marginal och om alla sidor ska få samma ruta. Gratis, utan uppladdning.",
        h1="Beskär en PDF automatiskt – *ta bort de vita kanterna*.",
        lede="Retypee hittar var innehållet finns på varje sida och klipper bort den tomma ramen runt om. Du ser på första sidan vad som behålls.",
        steps_h2="Så beskär du en PDF automatiskt",
        steps=[("Öppna PDF-filen.", "Sidorna ritas upp och mäts för att hitta innehållet."),
               ("Välj marginal och läge.", "Hur mycket luft som ska bli kvar, och om varje sida beskärs för sig eller alla får samma ruta."),
               ("Beskär och ladda ner.", "Sidorna får den nya storleken i en ny PDF.")],
        sections=[
            {"h2": "Två lägen", "ul": [
                "<em>Anpassa varje sida</em>: varje sida beskärs efter sitt eget innehåll. Bra för enstaka sidor och skannade lösblad.",
                "<em>Samma ruta för alla sidor</em>: rutan rymmer innehållet från alla sidor, så att sidorna förblir lika stora och texten står på samma ställe. Bäst för böcker och rapporter."]},
            {"h2": "Bra att veta", "ul": [
                "Beskärningen döljer området men tar inte bort det ur filen. För att dölja känsligt innehåll på riktigt, använd {{link:redact}}.",
                "Tomma sidor lämnas som de är.",
                "Skannade sidor med skuggor längs kanten kan få en bredare ruta. Rensa dem först med {{link:scan}}, eller beskär för hand med {{link:crop}}.",
                "Vill du ändra sidan till ett visst pappersformat efteråt, använd {{link:resize}}."]},
        ],
        faq_h2="Vanliga frågor om att beskära PDF automatiskt",
        faq=[("Hur beskär jag en PDF automatiskt?", "Öppna filen här, välj marginal och klicka på Beskär automatiskt. Retypee hittar innehållet och klipper bort de tomma kanterna."),
             ("Beskärs alla sidor lika mycket?", "Du väljer. Varje sida kan beskäras för sig, eller så får alla samma ruta."),
             ("Tas det beskurna bort på riktigt?", "Nej. Området döljs men finns kvar i filen. Använd Censurera PDF för känsligt innehåll."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["crop", "resize", "scan", "nup"],
        ui=dict(ac_scanning="Letar efter innehållet… {n} av {total}", ac_empty="Inget innehåll hittades på sidorna. De verkar vara tomma.",
                ac_hint="Retypee hittar var innehållet finns på varje sida och klipper bort den tomma kanten. Den ljusa rutan visar vad som behålls.", preview_note="Så här ser det ut på första sidan.",
                ac_margin="Marginal kvar", ac_mode="Beskärning", ac_each="Anpassa varje sida", ac_same="Samma ruta för alla sidor",
                ac_info="{n} av {total} {total:sida|sidor} beskärs, och ytan minskar med cirka {pct} %.", ac_btn="Beskär automatiskt", ac_done="{n} {n:sida|sidor} beskars.", out_suffix="beskuren"),
    ),
    "en": dict(
        title="Auto-Crop PDF – Remove White Margins | Retypee",
        desc="Crop a PDF automatically so the empty white margins disappear. Choose the margin and whether every page gets the same box. Free, no upload.",
        h1="Auto-crop a PDF – *remove the white margins*.",
        lede="Retypee finds where the content is on each page and trims the empty frame around it. You see on the first page what is kept.",
        steps_h2="How to crop a PDF automatically",
        steps=[("Open the PDF.", "The pages are drawn and measured to find the content."),
               ("Choose margin and mode.", "How much air should be left, and whether each page is cropped by itself or all get the same box."),
               ("Crop and download.", "The pages get the new size in a new PDF.")],
        sections=[
            {"h2": "Two modes", "ul": [
                "<em>Fit each page</em>: each page is cropped to its own content. Good for single pages and scanned loose sheets.",
                "<em>Same box for all pages</em>: the box holds the content of every page, so the pages stay the same size and the text sits in the same place. Best for books and reports."]},
            {"h2": "Good to know", "ul": [
                "Cropping hides the area but does not remove it from the file. To hide sensitive content for good, use {{link:redact}}.",
                "Blank pages are left as they are.",
                "Scanned pages with shadows along the edge can get a wider box. Clean them first with {{link:scan}}, or crop by hand with {{link:crop}}.",
                "If you want to change the page to a particular paper format afterwards, use {{link:resize}}."]},
        ],
        faq_h2="Questions about auto-cropping PDFs",
        faq=[("How do I crop a PDF automatically?", "Open the file here, choose a margin and click Auto-crop. Retypee finds the content and trims the empty edges."),
             ("Are all pages cropped by the same amount?", "You choose. Each page can be cropped by itself, or all can get the same box."),
             ("Is the cropped part really removed?", "No. The area is hidden but stays in the file. Use Redact PDF for sensitive content."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["crop", "resize", "scan", "nup"],
        ui=dict(ac_scanning="Looking for the content… {n} of {total}", ac_empty="No content was found on the pages. They seem to be empty.",
                ac_hint="Retypee finds where the content is on each page and trims the empty edge. The light box shows what is kept.", preview_note="This is how it looks on the first page.",
                ac_margin="Margin to keep", ac_mode="Cropping", ac_each="Fit each page", ac_same="Same box for all pages",
                ac_info="{n} of {total} {total:page is|pages are} cropped, and the area shrinks by about {pct}%.", ac_btn="Auto-crop", ac_done="{n} {n:page was|pages were} cropped.", out_suffix="cropped"),
    ),
}

# ------------------------------------------------------------------ grayscale
TOOLS6["grayscale"] = {
    "sv": dict(
        title="Gör PDF svartvit – gråskala gratis | Retypee",
        desc="Gör en PDF svartvit, alltså i gråtoner, för utskrift. Text, bilder och grafik omvandlas och texten går fortfarande att markera. Gratis, utan uppladdning.",
        h1="Gör en PDF svartvit – *alla färger blir gråtoner*.",
        lede="Spara färgbläck vid utskrift, eller skicka en enhetlig svartvit kopia. Texten finns kvar och går att markera, och inget laddas upp.",
        steps_h2="Så gör du en PDF svartvit",
        steps=[("Öppna PDF-filen.", "Släpp den på sidan."),
               ("Klicka på Gör svartvit.", "Alla färger i text, bilder och grafik blir gråtoner."),
               ("Ladda ner.", "Du ser storleken före och efter.")],
        sections=[
            {"h2": "Det här blir svartvitt", "ul": [
                "Färgad text och rubriker.",
                "Foton och andra bilder.",
                "Diagram, figurer och bakgrunder."]},
            {"h2": "Gråskala är inte rent svartvitt", "p": [
                "Resultatet är gråtoner, som ett svartvitt foto, och inte bara svart och vitt. Det ger läsbara bilder och diagram. Behöver du ren svartvit skanning av text, använd {{link:scan}} och välj Svartvitt."]},
            {"h2": "Bra att veta", "ul": [
                "Texten är kvar som text och går att söka i och markera.",
                "Filen blir ofta mindre, men inte alltid. Vill du krympa den mer, använd {{link:compress}}.",
                "Färgerna går inte att få tillbaka. Spara originalet om du behöver det.",
                "Lösenordsskyddade filer måste låsas upp först, använd {{link:unlock}}.",
                "PDF-motorn (cirka 25 MB) hämtas första gången du använder verktyget."]},
        ],
        faq_h2="Vanliga frågor om att göra PDF svartvit",
        faq=[("Hur gör jag en PDF svartvit?", "Öppna filen här och klicka på Gör svartvit. Du får en kopia där alla färger är gråtoner."),
             ("Försvinner texten?", "Nej. Texten är kvar som text, med gråa tecken i stället för färgade."),
             ("Blir filen mindre?", "Ofta, eftersom bilderna får färre färgkanaler, men det beror på innehållet."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["compress", "scan", "nup", "booklet"],
        ui=dict(gs_btn="Gör svartvit", gs_hint="Alla färger i text, bilder och grafik blir gråtoner. Texten finns kvar och går att markera. Bra för utskrift, och ofta en mindre fil.",
                gs_done="Klart. Storleken gick från {before} till {after}.", out_suffix="gra"),
    ),
    "en": dict(
        title="Convert PDF to Grayscale – Black and White Free | Retypee",
        desc="Turn a PDF black and white, in shades of grey, for printing. Text, images and graphics are converted and the text can still be selected. Free, no upload.",
        h1="Convert a PDF to grayscale – *every colour becomes grey*.",
        lede="Save colour ink when printing, or send a uniform black-and-white copy. The text stays selectable, and nothing is uploaded.",
        steps_h2="How to make a PDF black and white",
        steps=[("Open the PDF.", "Drop it on the page."),
               ("Click Make grayscale.", "Every colour in text, images and graphics becomes a shade of grey."),
               ("Download.", "You see the size before and after.")],
        sections=[
            {"h2": "What turns grey", "ul": [
                "Coloured text and headings.",
                "Photos and other images.",
                "Charts, figures and backgrounds."]},
            {"h2": "Grayscale is not pure black and white", "p": [
                "The result is shades of grey, like a black-and-white photo, not just black and white. That keeps images and charts readable. If you need a pure black-and-white scan of text, use {{link:scan}} and choose Black and white."]},
            {"h2": "Good to know", "ul": [
                "The text stays as text and can be searched and selected.",
                "The file often gets smaller, but not always. If you want to shrink it further, use {{link:compress}}.",
                "The colours cannot be brought back. Keep the original if you need it.",
                "Password-protected files have to be unlocked first, use {{link:unlock}}.",
                "The PDF engine (about 25 MB) is downloaded the first time you use the tool."]},
        ],
        faq_h2="Questions about making a PDF black and white",
        faq=[("How do I make a PDF black and white?", "Open the file here and click Make grayscale. You get a copy where every colour is a shade of grey."),
             ("Does the text disappear?", "No. The text stays as text, with grey characters instead of coloured ones."),
             ("Does the file get smaller?", "Often, because the images have fewer colour channels, but it depends on the content."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["compress", "scan", "nup", "booklet"],
        ui=dict(gs_btn="Make grayscale", gs_hint="Every colour in text, images and graphics becomes a shade of grey. The text stays and can be selected. Good for printing, and often a smaller file.",
                gs_done="Done. The size went from {before} to {after}.", out_suffix="gray"),
    ),
}

# ------------------------------------------------------------------ PNG variants (they run the JPG scripts)
def _png_to_pdf(lang):
    ui = dict(BASE["jpg-to-pdf"][lang]["ui"])
    if lang == "sv":
        return dict(
            title="PNG till PDF – gör bilder till en PDF gratis | Retypee",
            desc="Gör en eller flera PNG-bilder till en PDF. Ordna sidorna, välj A4 eller Letter och behåll genomskinligheten. Gratis, utan uppladdning.",
            h1="PNG till PDF – *samla bilderna i en fil*.",
            lede="Skärmdumpar, grafik och skannade sidor som PNG blir en PDF som är lätt att dela eller skriva ut. Bilderna stannar på din dator.",
            steps_h2="Så gör du PNG-bilder till en PDF",
            steps=[("Välj PNG-bilderna.", "Släpp en eller flera bilder på sidan. Andra bildformat fungerar också."),
                   ("Ordna och välj format.", "Dra bilderna i rätt ordning, välj A4, Letter eller samma storlek som bilden, och en marginal."),
                   ("Skapa PDF.", "Varje bild blir en sida.")],
            sections=[
                {"h2": "Varför PNG", "ul": [
                    "PNG är förlustfritt, så text och skarp grafik i skärmdumpar förblir knivskarpa.",
                    "Genomskinliga PNG-bilder bevaras och visas mot sidans vita bakgrund.",
                    "PNG-filerna läggs in som de är, utan att komprimeras om."]},
                {"h2": "Bra att veta", "ul": [
                    "PNG-bilder kan bli stora i en PDF. Vill du ha en mindre fil, använd {{link:compress}} efteråt.",
                    "Har du foton av papper, ger {{link:scan}} en renare PDF med vitt papper utan skuggor.",
                    "JPG-bilder går lika bra, se {{link:jpg-to-pdf}}.",
                    "Vill du göra tvärtom, finns {{link:pdf-to-png}}."]},
            ],
            faq_h2="Vanliga frågor om PNG till PDF",
            faq=[("Hur gör jag en PNG till PDF?", "Släpp bilden på sidan, välj sidstorlek och klicka på Skapa PDF. Flera bilder blir flera sidor i den ordning du valt."),
                 ("Kan jag slå ihop flera PNG-bilder i en PDF?", "Ja. Lägg till så många du vill och dra dem i rätt ordning."),
                 ("Behåller PNG sin kvalitet?", "Ja. PNG-bilderna läggs in utan att komprimeras om, så skarpa kanter och text förblir skarpa."),
                 ("Laddas bilderna upp?", "Nej. Allt sker i din webbläsare och bilderna lämnar aldrig din dator.")],
            related=["jpg-to-pdf", "scan", "compress", "merge"],
            ui=ui,
        )
    return dict(
        title="PNG to PDF – Turn Images Into a PDF Free | Retypee",
        desc="Turn one or more PNG images into a PDF. Order the pages, choose A4 or Letter and keep transparency. Free, in your browser and without uploading.",
        h1="PNG to PDF – *gather the images in one file*.",
        lede="Screenshots, graphics and scanned pages as PNG become a PDF that is easy to share or print. The images stay on your computer.",
        steps_h2="How to turn PNG images into a PDF",
        steps=[("Choose the PNG images.", "Drop one or more images on the page. Other image formats work too."),
               ("Order and choose the format.", "Drag the images into order, choose A4, Letter or the same size as the image, and a margin."),
               ("Create the PDF.", "Each image becomes a page.")],
        sections=[
            {"h2": "Why PNG", "ul": [
                "PNG is lossless, so text and sharp graphics in screenshots stay crisp.",
                "Transparent PNG images are kept and shown against the white page.",
                "PNG files are put in as they are, without being compressed again."]},
            {"h2": "Good to know", "ul": [
                "PNG images can get large in a PDF. If you want a smaller file, use {{link:compress}} afterwards.",
                "If you have photos of paper, {{link:scan}} gives a cleaner PDF with white paper and no shadows.",
                "JPG images work just as well, see {{link:jpg-to-pdf}}.",
                "If you want to go the other way, there is {{link:pdf-to-png}}."]},
        ],
        faq_h2="Questions about PNG to PDF",
        faq=[("How do I turn a PNG into a PDF?", "Drop the image on the page, choose the page size and click Create PDF. Several images become several pages in the order you chose."),
             ("Can I combine several PNG images in one PDF?", "Yes. Add as many as you like and drag them into the right order."),
             ("Does a PNG keep its quality?", "Yes. PNG images are put in without being compressed again, so sharp edges and text stay sharp."),
             ("Are the images uploaded?", "No. Everything happens in your browser and the images never leave your computer.")],
        related=["jpg-to-pdf", "scan", "compress", "merge"],
        ui=ui,
    )


def _pdf_to_png(lang):
    ui = dict(BASE["pdf-to-jpg"][lang]["ui"])
    ui["variant"] = "png"
    if lang == "sv":
        return dict(
            title="PDF till PNG – spara sidor som PNG-bilder | Retypee",
            desc="Spara sidorna i en PDF som skarpa PNG-bilder. Välj alla sidor eller några, och upplösning. Hämtas som ZIP. Gratis, utan uppladdning.",
            h1="PDF till PNG – *skarpa bilder av sidorna*.",
            lede="Gör en PDF-sida till en PNG-bild som du kan lägga i en presentation, ett dokument eller på webben. Sidorna ritas upp i din webbläsare.",
            steps_h2="Så sparar du PDF-sidor som PNG",
            steps=[("Öppna PDF-filen.", "Släpp den på sidan."),
                   ("Välj sidor och upplösning.", "Alla sidor eller bara några, och låg, normal eller hög upplösning. PNG är redan valt som format."),
                   ("Hämta bilderna.", "En sida blir en PNG-fil. Flera sidor packas i en ZIP.")],
            sections=[
                {"h2": "Varför PNG", "ul": [
                    "PNG är förlustfritt, så text, linjer och diagram förblir knivskarpa.",
                    "Bra för skärmdumpar av dokument, bilder i presentationer och webbsidor.",
                    "Vill du ha mindre filer och sidorna mest är foton, välj JPG i formatlistan."]},
                {"h2": "Bra att veta", "ul": [
                    "Hög upplösning ger stora filer. Normal räcker för skärm, hög är bra för utskrift.",
                    "Sidorna får vit bakgrund, eftersom PDF-sidor inte är genomskinliga.",
                    "Vill du ha bilderna som ligger inbäddade i filen, i originalkvalitet, använd {{link:extract-images}}.",
                    "Vill du göra tvärtom och samla bilder i en PDF, finns {{link:png-to-pdf}}."]},
            ],
            faq_h2="Vanliga frågor om PDF till PNG",
            faq=[("Hur gör jag en PDF till PNG?", "Öppna filen här, välj sidor och upplösning och klicka på Skapa bilder. Du får en PNG per sida, eller en ZIP om det är flera."),
                 ("Kan jag spara bara en sida?", "Ja. Välj Vissa sidor och skriv till exempel 3, så får du bara den sidan."),
                 ("Vilken upplösning ska jag välja?", "Normal passar skärm och webben. Välj hög om bilden ska skrivas ut eller zoomas in."),
                 ("Laddas filen upp?", "Nej. Sidorna ritas upp i din webbläsare och filen lämnar aldrig din dator.")],
            related=["pdf-to-jpg", "extract-images", "png-to-pdf", "pdf-to-text"],
            ui=ui,
        )
    return dict(
        title="PDF to PNG – Save Pages as PNG Images | Retypee",
        desc="Save the pages of a PDF as sharp PNG images. Choose all pages or some, and the resolution. Downloaded as a ZIP. Free, in your browser and no upload.",
        h1="PDF to PNG – *sharp images of the pages*.",
        lede="Turn a PDF page into a PNG image you can use in a presentation, a document or on the web. The pages are drawn in your browser.",
        steps_h2="How to save PDF pages as PNG",
        steps=[("Open the PDF.", "Drop it on the page."),
               ("Choose pages and resolution.", "All pages or just some, and low, normal or high resolution. PNG is already chosen as the format."),
               ("Get the images.", "One page becomes one PNG file. Several pages are packed in a ZIP.")],
        sections=[
            {"h2": "Why PNG", "ul": [
                "PNG is lossless, so text, lines and charts stay crisp.",
                "Good for screenshots of documents, pictures in presentations and web pages.",
                "If you want smaller files and the pages are mostly photos, choose JPG in the format list."]},
            {"h2": "Good to know", "ul": [
                "High resolution gives large files. Normal is enough for screens, high is good for print.",
                "The pages get a white background, since PDF pages are not transparent.",
                "If you want the images embedded in the file, in original quality, use {{link:extract-images}}.",
                "If you want to go the other way and gather images in a PDF, there is {{link:png-to-pdf}}."]},
        ],
        faq_h2="Questions about PDF to PNG",
        faq=[("How do I turn a PDF into PNG?", "Open the file here, choose pages and resolution and click Create images. You get one PNG per page, or a ZIP if there are several."),
             ("Can I save just one page?", "Yes. Choose Some pages and type for example 3, and you get only that page."),
             ("Which resolution should I choose?", "Normal suits screens and the web. Choose high if the image will be printed or zoomed in."),
             ("Is the file uploaded?", "No. The pages are drawn in your browser and the file never leaves your computer.")],
        related=["pdf-to-jpg", "extract-images", "png-to-pdf", "pdf-to-text"],
        ui=ui,
    )


TOOLS6["png-to-pdf"] = {"sv": _png_to_pdf("sv"), "en": _png_to_pdf("en")}
TOOLS6["pdf-to-png"] = {"sv": _pdf_to_png("sv"), "en": _pdf_to_png("en")}
