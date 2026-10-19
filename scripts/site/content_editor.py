"""Landing pages that use the full editor, each aimed at one specific search."""

EDITOR = {}

EDITOR["change-text"] = {
    "sv": dict(
        title="Ändra text i PDF gratis – direkt i webbläsaren | Retypee",
        desc="Ändra text i en befintlig PDF: klicka på orden, skriv det nya och ladda ner. Ingen uppladdning, inget konto och inga vattenstämplar.",
        h1="Ändra text i en PDF – utan att *skapa den på nytt*.",
        lede="Hittade du ett stavfel, fel datum eller fel belopp? Öppna PDF-filen, klicka på raden och skriv rätt. Resten av sidan förblir orörd.",
        steps_h2="Så ändrar du text i en PDF",
        steps=[("Öppna PDF-filen.", "Släpp den på sidan. Varje rad som går att redigera markeras när du håller muspekaren över den."),
               ("Klicka på raden och skriv.", "Skriv den nya texten och tryck Enter. Retypee väljer samma typsnitt, storlek och färg som originalet när det går."),
               ("Ladda ner.", "Spara den ändrade PDF-filen. Allt annat på sidan – bilder, linjer och länkar – är som förut.")],
        sections=[
            {"h2": "Det här kan du ändra", "ul": [
                "Ord och meningar, till exempel ett stavfel eller ett felaktigt namn.",
                "Siffror, datum och belopp.",
                "Typsnitt, storlek och färg på en rad.",
                "Ny text på valfri plats med <em>Lägg till text</em>."]},
            {"h2": "Så fungerar det under huven", "p": [
                "En PDF lagrar inte stycken, bara tecken på fasta positioner. När du ändrar en rad tar Retypee bort just de tecknen och skriver den nya texten på samma baslinje, med samma storlek och färg. Bilder, bakgrunder och linjer under texten rörs inte."]},
            {"h2": "Begränsningar", "ul": [
                "Texten flödar inte om: en längre rad fortsätter längre åt höger. Använd <em>Pressa ihop så den ryms</em> eller korta ner den.",
                "Skannade PDF-filer innehåller bara bilder och måste köras genom OCR först.",
                "Lösenordsskyddade PDF-filer måste låsas upp först."]},
        ],
        faq_h2="Vanliga frågor om att ändra text i PDF",
        faq=[("Hur ändrar jag text i en PDF gratis?", "Öppna filen i Retypee, klicka på raden du vill ändra, skriv den nya texten och ladda ner resultatet. Det kostar inget, kräver inget konto och lägger inga vattenstämplar på sidorna."),
             ("Går det att ändra text i en PDF utan att ladda upp den?", "Ja. Retypee körs i din webbläsare, så filen öppnas och ändras i enhetens minne och skickas aldrig till en server."),
             ("Varför får texten ett annat typsnitt?", "PDF-filer bäddar oftast bara in de bokstäver som används. Saknar originaltypsnittet en bokstav du skriver väljer Retypee ett liknande inbyggt typsnitt. Med <em>Lägg till typsnitt</em> kan du ge den originalfilen för en exakt matchning."),
             ("Kan jag ändra text i en PDF på mobilen?", "Verktyget fungerar i moderna mobilwebbläsare, men det är gjort för att användas med mus och tangentbord.")],
        related=["replace-text", "no-upload", "metadata", "merge"],
    ),
    "en": dict(
        title="Change Text in a PDF Free – In Your Browser | Retypee",
        desc="Change text in an existing PDF: click the words, type the new text and download. No upload, no account and no watermarks.",
        h1="Change text in a PDF – without *recreating it*.",
        lede="Found a typo, a wrong date or a wrong amount? Open the PDF, click the line and type it right. The rest of the page stays untouched.",
        steps_h2="How to change text in a PDF",
        steps=[("Open the PDF.", "Drop it on the page. Every editable line is highlighted when you hover over it."),
               ("Click the line and type.", "Type the new text and press Enter. Retypee uses the same font, size and colour as the original when it can."),
               ("Download.", "Save the changed PDF. Everything else on the page – images, lines and links – stays as it was.")],
        sections=[
            {"h2": "What you can change", "ul": [
                "Words and sentences, such as a typo or a wrong name.",
                "Numbers, dates and amounts.",
                "The font, size and colour of a line.",
                "New text anywhere on the page with <em>Add text</em>."]},
            {"h2": "How it works under the hood", "p": [
                "A PDF does not store paragraphs, only characters at fixed positions. When you change a line, Retypee removes exactly those characters and writes the new text on the same baseline, with the same size and colour. Images, backgrounds and lines under the text are left alone."]},
            {"h2": "Limits", "ul": [
                "Text does not reflow: a longer line runs further to the right. Use <em>Squeeze to fit</em> or shorten it.",
                "Scanned PDFs contain only pictures and need OCR first.",
                "Password-protected PDFs have to be unlocked first."]},
        ],
        faq_h2="Questions about changing text in a PDF",
        faq=[("How do I change text in a PDF for free?", "Open the file in Retypee, click the line you want to change, type the new text and download the result. It costs nothing, needs no account and puts no watermark on the pages."),
             ("Can I change text in a PDF without uploading it?", "Yes. Retypee runs in your browser, so the file is opened and changed in your device's memory and is never sent to a server."),
             ("Why does the text get a different font?", "PDFs usually embed only the letters they use. If the original font lacks a letter you type, Retypee picks a similar built-in font. With <em>Add font</em> you can give it the original file for an exact match."),
             ("Can I change text in a PDF on my phone?", "The tool works in modern mobile browsers, but it is made to be used with a mouse and keyboard.")],
        related=["replace-text", "no-upload", "metadata", "merge"],
    ),
}

EDITOR["replace-text"] = {
    "sv": dict(
        title="Ersätt text i PDF – sök och ersätt gratis | Retypee",
        desc="Sök och ersätt text i hela PDF-filen på en gång. Se antalet träffar innan du byter, ångra när du vill. Gratis och utan uppladdning.",
        h1="Sök och ersätt text i en PDF – i *hela filen*.",
        lede="Fel offertnummer på varje sida? Byt det på en gång. Skriv vad du söker och vad det ska bli, så ändras alla träffar.",
        steps_h2="Så ersätter du text i en PDF",
        steps=[("Öppna PDF-filen.", "Släpp den på sidan."),
               ("Tryck Ctrl+F (Cmd+F på Mac).", "Skriv texten du söker och det den ska ersättas med. En räknare visar hur många träffar det finns, och på vilka sidor."),
               ("Klicka på Ersätt alla.", "Alla träffar byts. Är du inte nöjd tar Ångra tillbaka allt, och när det ser rätt ut laddar du ner filen.")],
        sections=[
            {"h2": "Alternativ som hjälper dig att träffa rätt", "ul": [
                "<strong>Matcha versaler</strong> – skilj på ”Faktura” och ”faktura”.",
                "<strong>Hela ord</strong> – byt ”2026” men inte ”20261”.",
                "<strong>Pressa ihop</strong> – krymper längre ersättningstext så att den ryms på raden."]},
            {"h2": "Vanliga användningar", "ul": [
                "Ändra ett fakturanummer, offertnummer eller ordernummer som återkommer på varje sida.",
                "Byta ort, datum eller årtal i ett mall-dokument.",
                "Uppdatera ett företagsnamn eller en adress i ett avtal du själv har skrivit."]},
            {"h2": "Det här bör du veta", "ul": [
                "En träff måste ligga på en rad och i en och samma textstil. Text som är uppdelad på flera rader eller stilar hoppas över.",
                "Vill du bara ändra en enskild förekomst klickar du på just den raden i stället."]},
        ],
        faq_h2="Vanliga frågor om sök och ersätt i PDF",
        faq=[("Kan man sök och ersätta i en PDF?", "Ja. I Retypee trycker du Ctrl+F (Cmd+F på Mac), skriver vad du söker och vad det ska bytas mot, och klickar på Ersätt alla."),
             ("Ändras formateringen när texten ersätts?", "Den nya texten får samma baslinje, typsnitt, storlek och färg som texten den ersätter. Står texten högerjusterad, till exempel ett belopp i en tabell, behålls högerkanten."),
             ("Kan jag ångra en ersättning?", "Ja. Ångra (Ctrl+Z) tar tillbaka hela ersättningen i ett steg, och du kan göra om den med Gör om."),
             ("Hur många träffar kan jag byta på en gång?", "Alla i dokumentet. Retypee visar antalet och vilka sidor de finns på innan du byter.")],
        related=["change-text", "no-upload", "invoice", "metadata"],
    ),
    "en": dict(
        title="Replace Text in a PDF – Free Find and Replace | Retypee",
        desc="Find and replace text across a whole PDF in one go. See the number of matches before you replace, undo any time. Free, no upload.",
        h1="Find and replace text in a PDF – across the *whole file*.",
        lede="Wrong quote number on every page? Change it in one go. Type what you are looking for and what it should become, and every match changes.",
        steps_h2="How to replace text in a PDF",
        steps=[("Open the PDF.", "Drop it on the page."),
               ("Press Ctrl+F (Cmd+F on a Mac).", "Type the text you are looking for and what it should be replaced with. A counter shows how many matches there are, and on which pages."),
               ("Click Replace all.", "Every match changes. If you are not happy, Undo brings everything back, and when it looks right you download the file.")],
        sections=[
            {"h2": "Options that help you hit the right text", "ul": [
                "<strong>Match case</strong> – tell “Invoice” from “invoice”.",
                "<strong>Whole words</strong> – change “2026” but not “20261”.",
                "<strong>Squeeze</strong> – shrinks longer replacement text so it fits on the line."]},
            {"h2": "Common uses", "ul": [
                "Change an invoice, quote or order number that repeats on every page.",
                "Swap a city, date or year in a template document.",
                "Update a company name or address in a contract you wrote yourself."]},
            {"h2": "Good to know", "ul": [
                "A match has to sit on one line in one text style. Text split across lines or styles is skipped.",
                "If you only want to change a single occurrence, click that line instead."]},
        ],
        faq_h2="Questions about find and replace in a PDF",
        faq=[("Can you find and replace in a PDF?", "Yes. In Retypee you press Ctrl+F (Cmd+F on a Mac), type what you are looking for and what to replace it with, and click Replace all."),
             ("Does the formatting change when text is replaced?", "The new text gets the same baseline, font, size and colour as the text it replaces. If the text is right-aligned, such as an amount in a table, the right edge is kept."),
             ("Can I undo a replacement?", "Yes. Undo (Ctrl+Z) brings back the whole replacement in one step, and Redo does it again."),
             ("How many matches can I replace at once?", "All of them in the document. Retypee shows the number and the pages they are on before you replace.")],
        related=["change-text", "no-upload", "invoice", "metadata"],
    ),
}

EDITOR["no-upload"] = {
    "sv": dict(
        title="Redigera PDF utan uppladdning – privat och gratis | Retypee",
        desc="Redigera PDF-filer utan att de lämnar din dator. Allt sker i webbläsaren – ingen server, inget konto, ingen lagring. Gratis.",
        h1="Redigera PDF *utan att ladda upp* den.",
        lede="De flesta PDF-verktyg på nätet skickar din fil till en server. Retypee gör det inte: filen öppnas och redigeras i din webbläsare och stannar hos dig.",
        steps_h2="Så fungerar det utan uppladdning",
        steps=[("Motorn laddas ner, inte din fil.", "När du börjar använda Retypee hämtas redigeringsmotorn (cirka 25 MB första gången, sedan sparas den i webbläsaren). Din PDF skickas ingenstans."),
               ("Filen öppnas i enhetens minne.", "Texten läses och ändras lokalt med PyMuPDF, som körs i webbläsaren via WebAssembly."),
               ("Du sparar en ny fil.", "Resultatet laddas ner direkt till din dator. När du stänger fliken är allt borta.")],
        sections=[
            {"h2": "Varför spelar det roll?", "p": [
                "PDF-filer innehåller ofta personuppgifter: avtal, löner, fakturor, intyg. Skickar du dem till en tjänst på nätet måste du lita på hur de hanteras, hur länge de sparas och vem som kan komma åt dem. Om filen aldrig lämnar din enhet finns inget att lita på – och inget att radera efteråt."]},
            {"h2": "Så kan du kontrollera det själv", "p": [
                "Öppna webbläsarens utvecklarverktyg (F12), gå till fliken Nätverk och redigera en PDF. Du ser att den enda trafiken är motorn som hämtas första gången. Din fil syns inte i någon förfrågan.",
                "Koden är öppen källkod (AGPL-3.0), så du kan granska den också: <a href=\"https://github.com/LuckyLBP/retypee\">källkoden finns på GitHub</a>."]},
            {"h2": "Vad som ändå hämtas", "p": [
                "Redigeringsmotorn (PyMuPDF) hämtas från ett CDN (jsDelivr). Typsnittet och sidan kommer från vår egen server. Sidan sätter inga cookies och använder inga spårningsskript."]},
        ],
        faq_h2="Vanliga frågor om integritet",
        faq=[("Är det säkert att redigera känsliga dokument här?", "Filen lämnar aldrig din dator, så den kan inte läcka från en server. Du bör ändå följa dina egna regler för känsliga dokument och använda en enhet du litar på."),
             ("Fungerar det utan internet?", "Inte ännu. Motorn hämtas när du använder sidan. Vill du ha en helt lokal lösning kan du köra Retypee på din egen dator med källkoden från GitHub."),
             ("Varför tar sidan en stund att starta första gången?", "Redigeringsmotorn är cirka 25 MB. Den hämtas bara första gången, sedan sparas den i webbläsaren."),
             ("Sparas mina filer någonstans?", "Nej. Filen finns bara i flikens minne och försvinner när du stänger fliken.")],
        related=["change-text", "metadata", "merge", "redact"],
    ),
    "en": dict(
        title="Edit PDF Without Uploading – Private and Free | Retypee",
        desc="Edit PDF files without them leaving your computer. Everything happens in the browser – no server, no account, no storage. Free.",
        h1="Edit a PDF *without uploading* it.",
        lede="Most online PDF tools send your file to a server. Retypee does not: the file is opened and edited in your browser and stays with you.",
        steps_h2="How it works without an upload",
        steps=[("The engine is downloaded, not your file.", "When you start using Retypee, the editing engine is fetched (about 25 MB the first time, then it is cached in your browser). Your PDF is sent nowhere."),
               ("The file is opened in your device's memory.", "The text is read and changed locally with PyMuPDF, which runs in the browser through WebAssembly."),
               ("You save a new file.", "The result is downloaded straight to your computer. When you close the tab, everything is gone.")],
        sections=[
            {"h2": "Why does it matter?", "p": [
                "PDFs often contain personal data: contracts, salaries, invoices, certificates. If you send them to an online service you have to trust how they are handled, how long they are kept and who can reach them. If the file never leaves your device there is nothing to trust – and nothing to delete afterwards."]},
            {"h2": "How you can check it yourself", "p": [
                "Open your browser's developer tools (F12), go to the Network tab and edit a PDF. The only traffic you will see is the engine being fetched the first time. Your file does not appear in any request.",
                "The code is open source (AGPL-3.0), so you can read it too: <a href=\"https://github.com/LuckyLBP/retypee\">the source is on GitHub</a>."]},
            {"h2": "What is still downloaded", "p": [
                "The editing engine (PyMuPDF) is fetched from a CDN (jsDelivr). The font and the page come from our own server. The page sets no cookies and uses no tracking scripts."]},
        ],
        faq_h2="Questions about privacy",
        faq=[("Is it safe to edit sensitive documents here?", "The file never leaves your computer, so it cannot leak from a server. You should still follow your own rules for sensitive documents and use a device you trust."),
             ("Does it work offline?", "Not yet. The engine is fetched when you use the page. If you want a fully local setup you can run Retypee on your own computer with the source code from GitHub."),
             ("Why does the page take a moment to start the first time?", "The editing engine is about 25 MB. It is only downloaded the first time, then it is cached in your browser."),
             ("Are my files stored anywhere?", "No. The file exists only in the memory of the tab and disappears when you close it.")],
        related=["change-text", "metadata", "merge", "redact"],
    ),
}

EDITOR["invoice"] = {
    "sv": dict(
        title="Redigera faktura-PDF – rätta fel i egna fakturor | Retypee",
        desc="Rätta ett fakturanummer, datum eller belopp i din egen faktura- eller offert-PDF. Gratis, i webbläsaren och utan uppladdning.",
        h1="Rätta fel i din faktura- eller offert-*PDF*.",
        lede="Skrev du fel fakturanummer eller förfallodatum? Öppna PDF-filen, rätta raden och ladda ner. Din faktura lämnar aldrig din dator.",
        steps_h2="Så rättar du en faktura-PDF",
        steps=[("Öppna fakturan.", "Släpp PDF-filen på sidan."),
               ("Rätta uppgiften.", "Klicka på raden – till exempel fakturanummer, datum eller kontaktuppgift – och skriv rätt. Använd Sök och ersätt om samma uppgift finns på flera ställen."),
               ("Ladda ner och kontrollera.", "Spara den rättade filen och läs igenom den innan du skickar den.")],
        sections=[
            {"h2": "Bra användningar", "ul": [
                "Rätta ett stavfel i en offert innan du skickar den.",
                "Byta fakturanummer, referens eller betalningsvillkor som skrivits fel.",
                "Uppdatera adress eller bankgiro i dina egna dokumentmallar."]},
            {"h2": "Redigera bara dina egna dokument", "p": [
                "Verktyget är till för att rätta fel i dokument du själv har rätt att ändra. Att ändra en faktura eller ett annat dokument för att vilseleda någon är olagligt, oavsett vilket verktyg som används.",
                "Är fakturan redan skickad eller bokförd bör du i stället skicka en ny faktura eller en kreditfaktura. Fråga din revisor om du är osäker."]},
            {"h2": "Tips för bästa resultat", "ul": [
                "Är fakturan skapad i ett bokföringsprogram är det oftast bäst att rätta uppgiften där och exportera en ny PDF.",
                "Högerjusterade belopp i tabeller behåller sin högerkant när du byter siffror.",
                "Typsnittet kan skilja sig något om originalet saknar bokstäver du skriver."]},
        ],
        faq_h2="Vanliga frågor om att redigera fakturor",
        faq=[("Kan jag ändra en faktura i PDF-format?", "Ja, om du har rätt att ändra den. Öppna filen i Retypee, klicka på texten du vill rätta och ladda ner den ändrade PDF-filen. Ändra inte ett dokument för att vilseleda någon."),
             ("Laddas min faktura upp till en server?", "Nej. Retypee körs i din webbläsare, så fakturan öppnas och ändras på din egen enhet och skickas aldrig någonstans."),
             ("Vad gör jag om fakturan redan är skickad?", "Skicka i så fall en ny faktura eller en kreditfaktura i stället för att byta ut den skickade filen, och fråga din revisor om du är osäker."),
             ("Går det att ändra belopp och summor?", "Du kan ändra siffrorna som text, men Retypee räknar inte om några summor åt dig. Kontrollera att delsummor, moms och totalbelopp stämmer innan du skickar.")],
        related=["replace-text", "change-text", "metadata", "merge"],
    ),
    "en": dict(
        title="Edit Invoice PDF – Fix Your Own Invoices | Retypee",
        desc="Fix an invoice number, date or amount in your own invoice or quote PDF. Free, in your browser and without uploading.",
        h1="Fix mistakes in your invoice or quote *PDF*.",
        lede="Typed the wrong invoice number or due date? Open the PDF, fix the line and download. Your invoice never leaves your computer.",
        steps_h2="How to fix an invoice PDF",
        steps=[("Open the invoice.", "Drop the PDF on the page."),
               ("Fix the detail.", "Click the line – an invoice number, a date or a contact detail, for example – and type it right. Use Find and replace if the same detail appears in several places."),
               ("Download and check.", "Save the corrected file and read it through before you send it.")],
        sections=[
            {"h2": "Good uses", "ul": [
                "Fix a typo in a quote before you send it.",
                "Change an invoice number, reference or payment terms that were written wrong.",
                "Update an address or bank details in your own document templates."]},
            {"h2": "Only edit your own documents", "p": [
                "This tool is for fixing mistakes in documents you have the right to change. Altering an invoice or any other document to mislead someone is illegal, whatever tool is used.",
                "If the invoice has already been sent or booked, send a new invoice or a credit note instead. Ask your accountant if you are unsure."]},
            {"h2": "Tips for the best result", "ul": [
                "If the invoice was made in accounting software, it is usually best to fix the detail there and export a new PDF.",
                "Right-aligned amounts in tables keep their right edge when you change the digits.",
                "The font may differ slightly if the original lacks letters you type."]},
        ],
        faq_h2="Questions about editing invoices",
        faq=[("Can I change an invoice in PDF format?", "Yes, if you have the right to change it. Open the file in Retypee, click the text you want to fix and download the changed PDF. Do not change a document to mislead anyone."),
             ("Is my invoice uploaded to a server?", "No. Retypee runs in your browser, so the invoice is opened and changed on your own device and is never sent anywhere."),
             ("What should I do if the invoice has already been sent?", "Send a new invoice or a credit note instead of swapping the file you sent, and ask your accountant if you are unsure."),
             ("Can I change amounts and totals?", "You can change the digits as text, but Retypee does not recalculate any totals for you. Check that subtotals, VAT and the total amount add up before you send it.")],
        related=["replace-text", "change-text", "metadata", "merge"],
    ),
}
