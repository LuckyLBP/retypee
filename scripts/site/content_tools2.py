"""Wave 2 tool pages. Same shape as content_tools.py."""

TOOLS2 = {}

# ------------------------------------------------------------------ compress
TOOLS2["compress"] = {
    "sv": dict(
        title="Komprimera PDF – gör filen mindre gratis | Retypee",
        desc="Gör en PDF mindre så den går att mejla. Välj nivå och se hur mycket du sparar. Gratis, i webbläsaren och utan att filen laddas upp.",
        h1="Komprimera en PDF – *utan att ladda upp den*.",
        lede="Stora PDF-filer fastnar i mejlen. Retypee sänker bildernas upplösning och städar filens struktur, och du ser hur mycket mindre den blev.",
        steps_h2="Så komprimerar du en PDF",
        steps=[("Öppna PDF-filen.", "Släpp den på sidan."),
               ("Välj nivå.", "Bästa kvalitet ger en måttlig besparing. Minsta fil sänker bildernas upplösning mest."),
               ("Komprimera och ladda ner.", "Du ser storleken före och efter. Blir filen inte märkbart mindre får du veta det, i stället för en onödig fil.")],
        sections=[
            {"h2": "Vad som blir mindre", "ul": [
                "Stora bilder får lägre upplösning och JPEG-kvalitet.",
                "Typsnitt som bara används delvis krymps till de tecken som behövs.",
                "Filens struktur städas och packas om."]},
            {"h2": "Så mycket kan du spara", "p": [
                "Det beror på innehållet. Skannade dokument och PDF-filer med stora foton krymper mest, ofta till en tiondel eller mindre. En PDF som mest består av text är redan liten och sparar bara några procent."]},
            {"h2": "Bra att veta", "ul": [
                "Bilder komprimeras med förlust. Skärpan minskar, mest på nivån Minsta fil.",
                "Text och vektorgrafik påverkas inte.",
                "Lösenordsskyddade PDF-filer måste låsas upp först, använd {{link:unlock}}.",
                "PDF-motorn (cirka 25 MB) hämtas första gången du använder verktyget."]},
        ],
        faq_h2="Vanliga frågor om att komprimera PDF",
        faq=[("Hur komprimerar jag en PDF utan att förlora kvalitet?", "Börja med nivån Bästa kvalitet. Den sänker bara bilder som är onödigt skarpa för skärm och e-post. Text och grafik ändras inte."),
             ("Varför blev min PDF knappt mindre?", "Då består den troligen mest av text, eller har redan hårt komprimerade bilder. Retypee säger till i stället för att ge dig en fil som inte är mindre."),
             ("Hur mycket kan en PDF komprimeras?", "En skannad PDF kan krympa till en tiondel eller mindre. En vanlig textfil sparar bara några procent."),
             ("Laddas min PDF upp?", "Nej. Komprimeringen sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["merge", "split", "metadata", "protect"],
        ui=dict(lvl_low="Bästa kvalitet", lvl_low_d="Måttlig besparing. Bilder sänks till cirka 150 dpi.",
                lvl_medium="Balanserad", lvl_medium_d="Bra besparing. Bilder sänks till cirka 110 dpi.",
                lvl_high="Minsta fil", lvl_high_d="Störst besparing. Bilder sänks till cirka 72 dpi och blir mindre skarpa.",
                shrink_btn="Komprimera", no_gain="Filen blev inte märkbart mindre. Den är redan väl komprimerad, prova en kraftigare nivå.",
                compress_done="Från {before} till {after}, {pct} % mindre.", out_suffix="komprimerad"),
    ),
    "en": dict(
        title="Compress PDF – Make It Smaller Free | Retypee",
        desc="Make a PDF smaller so it can be emailed. Pick a level and see how much you save. Free, in your browser and without uploading.",
        h1="Compress a PDF – *without uploading it*.",
        lede="Big PDFs get stuck in email. Retypee lowers the resolution of the images and tidies the file's structure, and you see how much smaller it got.",
        steps_h2="How to compress a PDF",
        steps=[("Open the PDF.", "Drop it on the page."),
               ("Choose a level.", "Best quality gives a moderate saving. Smallest file lowers the image resolution the most."),
               ("Compress and download.", "You see the size before and after. If the file does not get noticeably smaller you are told, instead of getting a pointless file.")],
        sections=[
            {"h2": "What gets smaller", "ul": [
                "Large images get a lower resolution and JPEG quality.",
                "Fonts that are only partly used are cut down to the characters needed.",
                "The structure of the file is tidied and repacked."]},
            {"h2": "How much you can save", "p": [
                "It depends on the content. Scanned documents and PDFs with big photos shrink the most, often to a tenth or less. A PDF that is mostly text is already small and saves only a few percent."]},
            {"h2": "Good to know", "ul": [
                "Images are compressed with some loss. They get less sharp, most on the Smallest file level.",
                "Text and vector graphics are not affected.",
                "Password-protected PDFs have to be unlocked first, use {{link:unlock}}.",
                "The PDF engine (about 25 MB) is downloaded the first time you use the tool."]},
        ],
        faq_h2="Questions about compressing PDFs",
        faq=[("How do I compress a PDF without losing quality?", "Start with the Best quality level. It only lowers images that are needlessly sharp for screens and email. Text and graphics are not changed."),
             ("Why did my PDF hardly get smaller?", "It probably consists mostly of text, or its images are already heavily compressed. Retypee tells you instead of handing you a file that is not smaller."),
             ("How much can a PDF be compressed?", "A scanned PDF can shrink to a tenth or less. An ordinary text file only saves a few percent."),
             ("Is my PDF uploaded?", "No. The compression happens in your browser and the file never leaves your computer.")],
        related=["merge", "split", "metadata", "protect"],
        ui=dict(lvl_low="Best quality", lvl_low_d="Moderate saving. Images are lowered to about 150 dpi.",
                lvl_medium="Balanced", lvl_medium_d="Good saving. Images are lowered to about 110 dpi.",
                lvl_high="Smallest file", lvl_high_d="Biggest saving. Images are lowered to about 72 dpi and get less sharp.",
                shrink_btn="Compress", no_gain="The file did not get noticeably smaller. It is already well compressed, try a stronger level.",
                compress_done="From {before} to {after}, {pct} % smaller.", out_suffix="compressed"),
    ),
}

# ------------------------------------------------------------------ protect
TOOLS2["protect"] = {
    "sv": dict(
        title="Skydda PDF med lösenord – gratis och privat | Retypee",
        desc="Lås en PDF med ett lösenord (AES-256). Välj om utskrift, kopiering och redigering ska vara tillåtet. Gratis och utan uppladdning.",
        h1="Skydda en PDF med *lösenord*.",
        lede="Lösenordet sätts i din webbläsare, så varken filen eller lösenordet skickas någonstans. Den som öppnar filen måste skriva lösenordet.",
        steps_h2="Så lösenordsskyddar du en PDF",
        steps=[("Öppna PDF-filen.", "Släpp den på sidan."),
               ("Välj lösenord och regler.", "Skriv lösenordet två gånger och bestäm om utskrift, kopiering och redigering ska vara tillåtet."),
               ("Skydda och ladda ner.", "Du får en ny PDF som kräver lösenord för att öppnas.")],
        sections=[
            {"h2": "Så fungerar skyddet", "p": [
                "Filen krypteras med AES-256, den starkaste kryptering PDF-formatet stöder. Utan lösenordet går den inte att öppna. Reglerna för utskrift, kopiering och redigering följs av de flesta PDF-läsare, men de är inget fullgott skydd mot den som redan har lösenordet."]},
            {"h2": "Tänk på det här", "ul": [
                "Lösenordet kan inte återställas. Glömmer du det går filen inte att öppna, så spara det på ett säkert ställe.",
                "Välj ett långt lösenord som inte är ett ord ur en ordlista.",
                "Behåll originalfilen om du kan behöva den utan lösenord.",
                "Skicka lösenordet på en annan väg än filen."]},
            {"h2": "Bra att veta", "ul": [
                "En PDF som redan har lösenord måste först låsas upp, använd {{link:unlock}}.",
                "PDF-motorn (cirka 25 MB) hämtas första gången du använder verktyget."]},
        ],
        faq_h2="Vanliga frågor om att skydda PDF",
        faq=[("Hur lösenordsskyddar jag en PDF?", "Öppna filen här, skriv ett lösenord två gånger och klicka på Skydda PDF. Du laddar ner en ny fil som kräver lösenordet för att öppnas."),
             ("Vilken kryptering används?", "AES-256, den starkaste som PDF-formatet stöder."),
             ("Kan någon gissa mitt lösenord?", "Ett långt, slumpmässigt lösenord är i praktiken omöjligt att gissa fram. Ett kort eller vanligt ord kan gissas, så välj ett långt."),
             ("Laddas filen eller lösenordet upp?", "Nej. Allt sker i din webbläsare och varken filen eller lösenordet lämnar din dator.")],
        related=["unlock", "metadata", "redact", "compress"],
        ui=dict(allow_title="Vad får den som öppnar filen göra?", allow_print="Skriva ut", allow_copy="Kopiera text och bilder", allow_edit="Ändra och kommentera",
                pw="Lösenord", pw_again="Lösenord igen", pw_show="Visa lösenordet",
                pw_warning="Lösenordet kan inte återställas. Spara det på ett säkert ställe, annars går filen inte att öppna.",
                pw_empty="Skriv ett lösenord först.", pw_mismatch="Lösenorden är inte likadana.",
                protect_btn="Skydda PDF", protect_done="Filen är krypterad med AES-256 och kräver lösenord för att öppnas.", out_suffix="skyddad"),
    ),
    "en": dict(
        title="Protect PDF with a Password – Free and Private | Retypee",
        desc="Lock a PDF with a password (AES-256). Choose whether printing, copying and editing are allowed. Free, and nothing is uploaded.",
        h1="Protect a PDF with a *password*.",
        lede="The password is set in your browser, so neither the file nor the password is sent anywhere. Whoever opens the file has to type the password.",
        steps_h2="How to password-protect a PDF",
        steps=[("Open the PDF.", "Drop it on the page."),
               ("Choose a password and rules.", "Type the password twice and decide whether printing, copying and editing are allowed."),
               ("Protect and download.", "You get a new PDF that needs the password to open.")],
        sections=[
            {"h2": "How the protection works", "p": [
                "The file is encrypted with AES-256, the strongest encryption the PDF format supports. Without the password it cannot be opened. The rules for printing, copying and editing are followed by most PDF readers, but they are no real protection against someone who already has the password."]},
            {"h2": "Keep this in mind", "ul": [
                "The password cannot be recovered. If you forget it the file cannot be opened, so keep it somewhere safe.",
                "Choose a long password that is not a word from a dictionary.",
                "Keep the original file if you may need it without a password.",
                "Send the password a different way than the file."]},
            {"h2": "Good to know", "ul": [
                "A PDF that already has a password has to be unlocked first, use {{link:unlock}}.",
                "The PDF engine (about 25 MB) is downloaded the first time you use the tool."]},
        ],
        faq_h2="Questions about protecting PDFs",
        faq=[("How do I password-protect a PDF?", "Open the file here, type a password twice and click Protect PDF. You download a new file that needs the password to open."),
             ("Which encryption is used?", "AES-256, the strongest the PDF format supports."),
             ("Can someone guess my password?", "A long, random password is practically impossible to guess. A short or common word can be guessed, so choose a long one."),
             ("Is the file or the password uploaded?", "No. Everything happens in your browser and neither the file nor the password leaves your computer.")],
        related=["unlock", "metadata", "redact", "compress"],
        ui=dict(allow_title="What may the person who opens the file do?", allow_print="Print", allow_copy="Copy text and images", allow_edit="Edit and comment",
                pw="Password", pw_again="Password again", pw_show="Show the password",
                pw_warning="The password cannot be recovered. Keep it somewhere safe, otherwise the file cannot be opened.",
                pw_empty="Type a password first.", pw_mismatch="The passwords do not match.",
                protect_btn="Protect PDF", protect_done="The file is encrypted with AES-256 and needs the password to open.", out_suffix="protected"),
    ),
}

# ------------------------------------------------------------------ unlock
TOOLS2["unlock"] = {
    "sv": dict(
        title="Lås upp PDF – ta bort lösenord och begränsningar | Retypee",
        desc="Ta bort lösenordet eller begränsningarna från en PDF du kan öppna. Gratis, i webbläsaren och utan att filen laddas upp.",
        h1="Lås upp en PDF – *ta bort lösenordet*.",
        lede="Trött på att skriva lösenordet varje gång? Ange det en gång så får du en kopia utan lösenord. Allt sker på din egen enhet.",
        steps_h2="Så låser du upp en PDF",
        steps=[("Öppna PDF-filen.", "Retypee ser om den kräver lösenord eller har begränsningar."),
               ("Skriv lösenordet.", "Behövs det visas ett fält. Har filen bara begränsningar, till exempel mot utskrift, behövs inget lösenord."),
               ("Lås upp och ladda ner.", "Du får en kopia utan lösenord och begränsningar.")],
        sections=[
            {"h2": "Bara för filer du får öppna", "p": [
                "Om filen har ett lösenord måste du känna till det. Verktyget knäcker inga lösenord. Använd det för dina egna filer eller dokument du har rätt att ändra, och respektera upphovsrätt och andras begränsningar."]},
            {"h2": "Det här tas bort", "ul": [
                "Lösenordet för att öppna filen, om du anger det.",
                "Begränsningar mot utskrift, kopiering och redigering."]},
            {"h2": "Bra att veta", "ul": [
                "Fel lösenord ger ett meddelande och du kan prova igen utan att börja om.",
                "Efter upplåsningen fungerar alla andra verktyg, till exempel {{link:merge}} och {{link:home}}.",
                "PDF-motorn (cirka 25 MB) hämtas första gången du använder verktyget."]},
        ],
        faq_h2="Vanliga frågor om att låsa upp PDF",
        faq=[("Hur tar jag bort lösenordet från en PDF?", "Öppna filen här, skriv lösenordet och klicka på Lås upp PDF. Du får en kopia som kan öppnas utan lösenord."),
             ("Kan ni låsa upp en PDF där jag glömt lösenordet?", "Nej. Verktyget kan inte gissa eller knäcka lösenord. Du måste känna till det."),
             ("Varför kan jag inte skriva ut eller kopiera från min PDF?", "Filen har troligen begränsningar. Läs in den här så tas de bort, om du har rätt att ändra filen."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och varken filen eller lösenordet lämnar din dator.")],
        related=["protect", "merge", "home", "compress"],
        ui=dict(unlock_needs="Den här filen kräver ett lösenord för att öppnas.", unlock_limited="Filen har begränsningar, till exempel mot utskrift eller kopiering. De tas bort.",
                unlock_nothing="Den här filen har inget lösenord och inga begränsningar.", unlock_btn="Lås upp PDF", unlock_done="Lösenordet och begränsningarna är borttagna.",
                pw="Lösenord", pw_empty="Skriv lösenordet först.", out_suffix="upplåst"),
    ),
    "en": dict(
        title="Unlock PDF – Remove Password and Restrictions | Retypee",
        desc="Remove the password or the restrictions from a PDF you can open. Free, in your browser and without uploading the file.",
        h1="Unlock a PDF – *remove the password*.",
        lede="Tired of typing the password every time? Enter it once and get a copy without one. Everything happens on your own device.",
        steps_h2="How to unlock a PDF",
        steps=[("Open the PDF.", "Retypee sees whether it needs a password or has restrictions."),
               ("Type the password.", "If one is needed a field appears. If the file only has restrictions, such as against printing, no password is needed."),
               ("Unlock and download.", "You get a copy without a password or restrictions.")],
        sections=[
            {"h2": "Only for files you may open", "p": [
                "If the file has a password you have to know it. The tool does not crack passwords. Use it for your own files or documents you have the right to change, and respect copyright and other people's restrictions."]},
            {"h2": "What gets removed", "ul": [
                "The password to open the file, if you enter it.",
                "Restrictions against printing, copying and editing."]},
            {"h2": "Good to know", "ul": [
                "A wrong password gives a message and you can try again without starting over.",
                "After unlocking, every other tool works, for example {{link:merge}} and {{link:home}}.",
                "The PDF engine (about 25 MB) is downloaded the first time you use the tool."]},
        ],
        faq_h2="Questions about unlocking PDFs",
        faq=[("How do I remove the password from a PDF?", "Open the file here, type the password and click Unlock PDF. You get a copy that opens without a password."),
             ("Can you unlock a PDF whose password I forgot?", "No. The tool cannot guess or crack passwords. You have to know it."),
             ("Why can't I print or copy from my PDF?", "The file probably has restrictions. Load it here and they are removed, if you have the right to change the file."),
             ("Is the file uploaded?", "No. Everything happens in your browser and neither the file nor the password leaves your computer.")],
        related=["protect", "merge", "home", "compress"],
        ui=dict(unlock_needs="This file needs a password to open.", unlock_limited="The file has restrictions, such as against printing or copying. They are removed.",
                unlock_nothing="This file has no password and no restrictions.", unlock_btn="Unlock PDF", unlock_done="The password and the restrictions are removed.",
                pw="Password", pw_empty="Type the password first.", out_suffix="unlocked"),
    ),
}

# ------------------------------------------------------------------ page numbers
TOOLS2["page-numbers"] = {
    "sv": dict(
        title="Lägg till sidnummer i PDF – gratis | Retypee",
        desc="Lägg till sidnummer i en PDF. Välj plats, format och startnummer och se hur det blir innan du sparar. Gratis och utan uppladdning.",
        h1="Lägg till sidnummer i en PDF – *välj plats och format*.",
        lede="Se hur numret hamnar på första sidan medan du ställer in det. Sedan numreras alla sidor på en gång.",
        steps_h2="Så lägger du till sidnummer",
        steps=[("Öppna PDF-filen.", "Släpp den på sidan."),
               ("Ställ in sidnumret.", "Välj var det ska sitta, om det ska stå som ”3”, ”Sida 3” eller ”Sida 3 av 8”, vilket nummer du börjar på och från vilken sida."),
               ("Numrera och ladda ner.", "Alla sidor får sitt nummer i den nya PDF-filen.")],
        sections=[
            {"h2": "Vanliga val", "ul": [
                "Sida X av Y för rapporter och avtal.",
                "Börja på sida 2 om försättsbladet inte ska ha något nummer: sätt <em>Börja på sida</em> till 2.",
                "Nere i mitten är vanligast. Uppe till höger passar brev."]},
            {"h2": "Bra att veta", "ul": [
                "Numret skrivs in som text med typsnittet Helvetica.",
                "Vridna sidor får numret rätt vänt.",
                "Har sidorna redan nummer läggs det nya ovanpå. Ta bort de gamla med {{link:redact}} om de ska bort.",
                "Vill du ordna sidorna först, använd {{link:organize}}."]},
        ],
        faq_h2="Vanliga frågor om sidnummer i PDF",
        faq=[("Hur lägger jag till sidnummer i en PDF?", "Öppna filen, välj plats och format, och klicka på Lägg till sidnummer. Alla sidor numreras på en gång."),
             ("Kan jag börja numrera på sida 2?", "Ja. Sätt <em>Börja på sida</em> till 2 så får försättsbladet inget nummer. Du kan också välja vilket nummer som är det första."),
             ("Kan jag ändra storlek och placering?", "Ja. Välj en av sex platser och en storlek mellan 8 och 24 punkter. Förhandsvisningen visar resultatet på första sidan."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["watermark", "organize", "merge", "crop"],
        ui=dict(preview_note="Så här ser det ut på första sidan.", pn_btn="Lägg till sidnummer", pn_position="Plats", pn_format="Format", pn_start="Första numret", pn_from="Börja på sida", pn_size="Storlek",
                pos_bl="Nere till vänster", pos_bc="Nere i mitten", pos_br="Nere till höger", pos_tl="Uppe till vänster", pos_tc="Uppe i mitten", pos_tr="Uppe till höger",
                fmt_n="{n}", fmt_page="Sida {n}", fmt_of="{n} / {total}", fmt_pageof="Sida {n} av {total}",
                pn_done="{n} {n:sida|sidor} numrerades.", out_suffix="numrerad"),
    ),
    "en": dict(
        title="Add Page Numbers to a PDF – Free | Retypee",
        desc="Add page numbers to a PDF. Choose position, format and start number and see the result before you save. Free, and nothing is uploaded.",
        h1="Add page numbers to a PDF – *choose where and how*.",
        lede="See where the number lands on the first page while you set it up. Then every page is numbered in one go.",
        steps_h2="How to add page numbers",
        steps=[("Open the PDF.", "Drop it on the page."),
               ("Set up the number.", "Choose where it goes, whether it reads “3”, “Page 3” or “Page 3 of 8”, which number to start on and from which page."),
               ("Number and download.", "Every page gets its number in the new PDF.")],
        sections=[
            {"h2": "Common choices", "ul": [
                "Page X of Y for reports and contracts.",
                "Start on page 2 if the cover page should have no number: set <em>Start on page</em> to 2.",
                "Bottom centre is the most common. Top right suits letters."]},
            {"h2": "Good to know", "ul": [
                "The number is written as text in the Helvetica font.",
                "Rotated pages get the number the right way up.",
                "If the pages already have numbers the new one goes on top. Remove the old ones with {{link:redact}} if they should go.",
                "If you want to put the pages in order first, use {{link:organize}}."]},
        ],
        faq_h2="Questions about page numbers in PDFs",
        faq=[("How do I add page numbers to a PDF?", "Open the file, choose position and format, and click Add page numbers. Every page is numbered in one go."),
             ("Can I start numbering on page 2?", "Yes. Set <em>Start on page</em> to 2 and the cover page gets no number. You can also choose which number comes first."),
             ("Can I change the size and position?", "Yes. Choose one of six positions and a size between 8 and 24 points. The preview shows the result on the first page."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["watermark", "organize", "merge", "crop"],
        ui=dict(preview_note="This is how it looks on the first page.", pn_btn="Add page numbers", pn_position="Position", pn_format="Format", pn_start="First number", pn_from="Start on page", pn_size="Size",
                pos_bl="Bottom left", pos_bc="Bottom centre", pos_br="Bottom right", pos_tl="Top left", pos_tc="Top centre", pos_tr="Top right",
                fmt_n="{n}", fmt_page="Page {n}", fmt_of="{n} / {total}", fmt_pageof="Page {n} of {total}",
                pn_done="{n} {n:page was|pages were} numbered.", out_suffix="numbered"),
    ),
}

# ------------------------------------------------------------------ watermark
TOOLS2["watermark"] = {
    "sv": dict(
        title="Vattenstämpel på PDF – lägg text över sidorna | Retypee",
        desc="Lägg en text som UTKAST eller KONFIDENTIELLT över alla sidor i en PDF. Välj storlek, färg och synlighet. Gratis och utan uppladdning.",
        h1="Lägg en *vattenstämpel* på din PDF.",
        lede="Markera dokumentet som utkast eller konfidentiellt. Du ser stämpeln på första sidan innan du sparar.",
        steps_h2="Så lägger du en vattenstämpel på en PDF",
        steps=[("Öppna PDF-filen.", "Släpp den på sidan."),
               ("Skriv och ställ in.", "Skriv texten och välj storlek, färg, synlighet och om den ska ligga snett eller rakt."),
               ("Stämpla och ladda ner.", "Texten läggs mitt på varje sida.")],
        sections=[
            {"h2": "Vanliga stämplar", "ul": [
                "UTKAST för dokument som inte är klara.",
                "KONFIDENTIELLT för känsliga dokument.",
                "KOPIA så att ingen tar en kopia för originalet.",
                "Mottagarens namn, för att visa vem filen är till."]},
            {"h2": "Bra att veta", "ul": [
                "Stämpeln ligger ovanpå sidans innehåll och är en del av filen. Den går inte att stänga av i läsaren.",
                "En vattenstämpel är ingen säkerhet. Den som vill kan ta bort den med ett redigeringsprogram.",
                "Bara tecken ur standardteckenuppsättningen stöds, alltså bokstäver (även å, ä, ö), siffror och vanliga tecken. Emoji går inte.",
                "För ett litet nummer i hörnet i stället, använd {{link:page-numbers}}."]},
        ],
        faq_h2="Vanliga frågor om vattenstämplar i PDF",
        faq=[("Hur lägger jag en vattenstämpel på en PDF?", "Öppna filen, skriv texten, välj storlek och färg och klicka på Lägg på vattenstämpel. Den hamnar mitt på varje sida."),
             ("Kan jag göra stämpeln genomskinlig?", "Ja. Med reglaget Synlighet väljer du mellan 5 och 80 procent, så att texten under syns."),
             ("Går det att ta bort stämpeln efteråt?", "Inte med det här verktyget. Spara originalfilen om du vill kunna ändra eller göra en ny version."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["page-numbers", "metadata", "protect", "redact"],
        ui=dict(preview_note="Så här ser det ut på första sidan.", wm_default="KONFIDENTIELLT", wm_btn="Lägg på vattenstämpel", wm_text="Text", wm_size="Storlek", wm_opacity="Synlighet",
                wm_angle="Riktning", wm_diag="Snett (45°)", wm_flat="Rakt", wm_color="Färg",
                wm_chars="Texten innehåller tecken som inte finns i teckenuppsättningen. Använd bokstäver, siffror och vanliga tecken.",
                wm_done="Vattenstämpeln lades på {n} {n:sida|sidor}.", out_suffix="stämplad"),
    ),
    "en": dict(
        title="Watermark PDF – Put Text Across the Pages | Retypee",
        desc="Put a text such as DRAFT or CONFIDENTIAL across every page of a PDF. Choose size, colour and opacity. Free, and nothing is uploaded.",
        h1="Put a *watermark* on your PDF.",
        lede="Mark the document as a draft or confidential. You see the stamp on the first page before you save.",
        steps_h2="How to watermark a PDF",
        steps=[("Open the PDF.", "Drop it on the page."),
               ("Type and set up.", "Type the text and choose size, colour, opacity and whether it runs diagonally or straight."),
               ("Stamp and download.", "The text is placed in the middle of every page.")],
        sections=[
            {"h2": "Common stamps", "ul": [
                "DRAFT for documents that are not finished.",
                "CONFIDENTIAL for sensitive documents.",
                "COPY so nobody mistakes a copy for the original.",
                "The recipient's name, to show who the file is for."]},
            {"h2": "Good to know", "ul": [
                "The stamp sits on top of the page content and is part of the file. It cannot be switched off in the reader.",
                "A watermark is not security. Anyone who wants to can remove it with an editing program.",
                "Only characters from the standard character set are supported: letters, digits and ordinary symbols. Emoji do not work.",
                "For a small number in the corner instead, use {{link:page-numbers}}."]},
        ],
        faq_h2="Questions about watermarking PDFs",
        faq=[("How do I put a watermark on a PDF?", "Open the file, type the text, choose size and colour and click Add watermark. It lands in the middle of every page."),
             ("Can I make the stamp see-through?", "Yes. The Opacity slider goes from 5 to 80 percent, so the page underneath shows through."),
             ("Can the stamp be removed afterwards?", "Not with this tool. Keep the original file if you want to change it or make a new version."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["page-numbers", "metadata", "protect", "redact"],
        ui=dict(preview_note="This is how it looks on the first page.", wm_default="CONFIDENTIAL", wm_btn="Add watermark", wm_text="Text", wm_size="Size", wm_opacity="Opacity",
                wm_angle="Direction", wm_diag="Diagonal (45°)", wm_flat="Straight", wm_color="Colour",
                wm_chars="The text contains characters that are not in the character set. Use letters, digits and ordinary symbols.",
                wm_done="The watermark was added to {n} {n:page|pages}.", out_suffix="watermarked"),
    ),
}

# ------------------------------------------------------------------ crop
TOOLS2["crop"] = {
    "sv": dict(
        title="Beskär PDF – klipp bort marginaler gratis | Retypee",
        desc="Beskär en PDF genom att dra i kanterna eller skriva marginaler i millimeter. Gäller alla sidor. Gratis och utan uppladdning.",
        h1="Beskär en PDF – *dra i kanterna*.",
        lede="Ta bort vita marginaler eller en rand du inte vill ha. Du ser beskärningen på första sidan, och samma mått används på alla sidor.",
        steps_h2="Så beskär du en PDF",
        steps=[("Öppna PDF-filen.", "Släpp den på sidan."),
               ("Dra i kanterna.", "Dra i de gula handtagen på första sidan, eller skriv marginalerna i millimeter."),
               ("Beskär och ladda ner.", "Alla sidor beskärs lika mycket.")],
        sections=[
            {"h2": "Vanliga användningar", "ul": [
                "Ta bort vita kanter runt skannade sidor.",
                "Klippa bort sidhuvud eller sidfot.",
                "Låta en tabell eller figur fylla sidan."]},
            {"h2": "Bra att veta", "ul": [
                "Beskärningen ändrar vad som visas, inte vad som finns i filen. Innehåll utanför kanten ligger kvar. Behöver du ta bort något för gott, använd {{link:redact}}.",
                "Alla sidor beskärs med samma marginaler. Sidor som skulle bli för små hoppas över.",
                "Vridna sidor beskärs åt rätt håll, så kanterna följer det du ser.",
                "Vill du ta bort hela sidor i stället, använd {{link:delete-pages}}."]},
        ],
        faq_h2="Vanliga frågor om att beskära PDF",
        faq=[("Hur beskär jag en PDF?", "Öppna filen, dra i kanterna på första sidan eller skriv marginalerna, och klicka på Beskär PDF."),
             ("Tas det beskurna bort på riktigt?", "Nej. Beskärningen döljer området, men innehållet finns kvar i filen. För känsligt innehåll, använd Censurera PDF."),
             ("Kan jag beskära olika mycket på olika sidor?", "Inte i den här versionen. Samma marginaler används på alla sidor."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["page-numbers", "rotate", "redact", "organize"],
        ui=dict(crop_hint="Dra i de gula handtagen på första sidan, eller skriv marginalerna i millimeter.", crop_top="Upptill", crop_right="Till höger", crop_bottom="Nedtill", crop_left="Till vänster",
                crop_all="Samma marginaler används på alla {n} {n:sida|sidor}.", crop_btn="Beskär PDF", crop_done="{n} {n:sida|sidor} beskars.", out_suffix="beskuren"),
    ),
    "en": dict(
        title="Crop PDF – Trim Margins Free | Retypee",
        desc="Crop a PDF by dragging the edges or typing margins in millimetres. Applies to every page. Free, and nothing is uploaded.",
        h1="Crop a PDF – *drag the edges*.",
        lede="Remove white margins or a strip you do not want. You see the crop on the first page, and the same measurements are used on every page.",
        steps_h2="How to crop a PDF",
        steps=[("Open the PDF.", "Drop it on the page."),
               ("Drag the edges.", "Drag the yellow handles on the first page, or type the margins in millimetres."),
               ("Crop and download.", "Every page is cropped by the same amount.")],
        sections=[
            {"h2": "Common uses", "ul": [
                "Remove white borders around scanned pages.",
                "Cut off a header or footer.",
                "Let a table or figure fill the page."]},
            {"h2": "Good to know", "ul": [
                "Cropping changes what is shown, not what is in the file. Content outside the edge stays in the file. If you need to remove something for good, use {{link:redact}}.",
                "Every page is cropped with the same margins. Pages that would become too small are skipped.",
                "Rotated pages are cropped the right way round, so the edges follow what you see.",
                "If you want to remove whole pages instead, use {{link:delete-pages}}."]},
        ],
        faq_h2="Questions about cropping PDFs",
        faq=[("How do I crop a PDF?", "Open the file, drag the edges on the first page or type the margins, and click Crop PDF."),
             ("Is the cropped part really removed?", "No. Cropping hides the area, but the content stays in the file. For sensitive content, use Redact PDF."),
             ("Can I crop different amounts on different pages?", "Not in this version. The same margins are used on every page."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["page-numbers", "rotate", "redact", "organize"],
        ui=dict(crop_hint="Drag the yellow handles on the first page, or type the margins in millimetres.", crop_top="Top", crop_right="Right", crop_bottom="Bottom", crop_left="Left",
                crop_all="The same margins are used on all {n} {n:page|pages}.", crop_btn="Crop PDF", crop_done="{n} {n:page was|pages were} cropped.", out_suffix="cropped"),
    ),
}

# ------------------------------------------------------------------ sign
TOOLS2["sign"] = {
    "sv": dict(
        title="Signera PDF – rita eller skriv din namnteckning | Retypee",
        desc="Signera en PDF: rita eller skriv din namnteckning och placera den där den ska sitta. Gratis och utan uppladdning.",
        h1="Signera en PDF – *rita eller skriv* din namnteckning.",
        lede="Skapa en namnteckning, dra den på plats och spara. Filen och din signatur stannar på din dator.",
        steps_h2="Så signerar du en PDF",
        steps=[("Skapa signaturen.", "Rita med mus eller finger, eller skriv ditt namn i en handskriftsstil."),
               ("Placera den.", "Dra signaturen dit den ska sitta, ändra storleken och välj sida."),
               ("Signera och ladda ner.", "Signaturen läggs in i den nya PDF-filen.")],
        sections=[
            {"h2": "Det här är en synlig signatur", "p": [
                "Signaturen läggs in som en bild på sidan. Det är som att skriva under på papper och skanna in det, inte en digital signatur med certifikat eller BankID. För avtal som kräver kvalificerad elektronisk underskrift behövs en särskild tjänst."]},
            {"h2": "Bra att veta", "ul": [
                "Signaturen sparas inte någonstans. Du skapar den på nytt nästa gång.",
                "Du kan sätta samma signatur på alla sidor, till exempel för att parafera.",
                "På en pekskärm blir det mest naturligt att rita med fingret.",
                "Vill du fylla i text i dokumentet först, använd {{link:home}}."]},
        ],
        faq_h2="Vanliga frågor om att signera PDF",
        faq=[("Är en signatur här juridiskt giltig?", "Det beror på dokumentet. En enkel bildsignatur duger för många vardagliga avtal, men inte där lagen kräver kvalificerad elektronisk signatur. Fråga mottagaren om du är osäker."),
             ("Sparas min signatur?", "Nej. Den finns bara i din webbläsare medan du arbetar och försvinner när du stänger fliken."),
             ("Kan jag signera flera sidor?", "Ja. Kryssa i att signaturen ska sättas på alla sidor, eller signera en sida i taget."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och varken filen eller signaturen lämnar din dator.")],
        related=["home", "page-numbers", "merge", "protect"],
        ui=dict(sig_black="Svart", sig_blue="Blå", sig_type_ph="Skriv ditt namn", sig_draw_hint="Rita din namnteckning i rutan.", sig_type="Namn", sig_style="Stil", sig_style_n="Stil {n}",
                sig_tab_draw="Rita", sig_tab_type="Skriv", sig_color="Färg", sig_empty="Skapa en signatur först.", sig_use="Använd den här signaturen", sig_clear="Rensa",
                sig_step1="Steg 1: Skapa din signatur.", sig_step2="Steg 2: Dra signaturen dit den ska sitta.", sig_size="Storlek", sig_all="Sätt den på alla sidor",
                sig_redo="Ändra signatur", sig_btn="Signera PDF", sig_done="Signaturen lades till i dokumentet.", out_suffix="signerad"),
    ),
    "en": dict(
        title="Sign PDF – Draw or Type Your Signature | Retypee",
        desc="Sign a PDF: draw or type your signature and place it where it belongs. Free, and nothing is uploaded.",
        h1="Sign a PDF – *draw or type* your signature.",
        lede="Make a signature, drag it into place and save. The file and your signature stay on your computer.",
        steps_h2="How to sign a PDF",
        steps=[("Make the signature.", "Draw with a mouse or finger, or type your name in a handwriting style."),
               ("Place it.", "Drag the signature where it should go, change its size and choose the page."),
               ("Sign and download.", "The signature is added to the new PDF.")],
        sections=[
            {"h2": "This is a visible signature", "p": [
                "The signature is added as an image on the page. It is like signing on paper and scanning it, not a digital signature with a certificate or an eID. For contracts that require a qualified electronic signature you need a dedicated service."]},
            {"h2": "Good to know", "ul": [
                "The signature is not saved anywhere. You make it again next time.",
                "You can put the same signature on every page, for example to initial a document.",
                "On a touch screen, drawing with your finger feels the most natural.",
                "If you want to fill in text in the document first, use {{link:home}}."]},
        ],
        faq_h2="Questions about signing PDFs",
        faq=[("Is a signature made here legally valid?", "It depends on the document. A simple image signature is fine for many everyday agreements, but not where the law requires a qualified electronic signature. Ask the recipient if you are unsure."),
             ("Is my signature saved?", "No. It only exists in your browser while you work and disappears when you close the tab."),
             ("Can I sign several pages?", "Yes. Tick the box to put the signature on every page, or sign one page at a time."),
             ("Is the file uploaded?", "No. Everything happens in your browser and neither the file nor the signature leaves your computer.")],
        related=["home", "page-numbers", "merge", "protect"],
        ui=dict(sig_black="Black", sig_blue="Blue", sig_type_ph="Type your name", sig_draw_hint="Draw your signature in the box.", sig_type="Name", sig_style="Style", sig_style_n="Style {n}",
                sig_tab_draw="Draw", sig_tab_type="Type", sig_color="Colour", sig_empty="Make a signature first.", sig_use="Use this signature", sig_clear="Clear",
                sig_step1="Step 1: Make your signature.", sig_step2="Step 2: Drag the signature where it should go.", sig_size="Size", sig_all="Put it on every page",
                sig_redo="Change signature", sig_btn="Sign PDF", sig_done="The signature was added to the document.", out_suffix="signed"),
    ),
}

# ------------------------------------------------------------------ organize
TOOLS2["organize"] = {
    "sv": dict(
        title="Organisera PDF – ändra ordning på sidor gratis | Retypee",
        desc="Dra sidorna i en ny ordning, vrid dem eller ta bort dem, allt i en vy. Gratis, i webbläsaren och utan uppladdning.",
        h1="Organisera en PDF – *dra sidorna* på plats.",
        lede="Se alla sidor som miniatyrer. Flytta, vrid och ta bort tills det ser rätt ut, och spara sedan en ny PDF.",
        steps_h2="Så ändrar du ordningen på sidorna i en PDF",
        steps=[("Öppna PDF-filen.", "Sidorna visas som miniatyrer."),
               ("Dra, vrid och ta bort.", "Dra en sida till en ny plats eller använd pilarna. Vrid med ↺ och ↻, och ta bort med ✕."),
               ("Spara.", "Du får en ny PDF med sidorna i den ordning du valt.")],
        sections=[
            {"h2": "Vanliga användningar", "ul": [
                "Flytta en bilaga till rätt plats.",
                "Vända skannade sidor som hamnat fel och ta bort en tom sida i samma veva.",
                "Sätta rätt ordning efter att du slagit ihop filer med {{link:merge}}."]},
            {"h2": "Bra att veta", "ul": [
                "Klicka på ✕ igen för att ta tillbaka en borttagen sida.",
                "Originalfilen ändras inte. Du laddar ner en ny.",
                "Behöver du bara vrida eller bara ta bort sidor finns enklare verktyg: {{link:rotate}} och {{link:delete-pages}}.",
                "Lösenordsskyddade PDF-filer måste låsas upp först."]},
        ],
        faq_h2="Vanliga frågor om att organisera PDF",
        faq=[("Hur ändrar jag ordningen på sidorna i en PDF?", "Öppna filen, dra sidorna till rätt plats och klicka på Spara ny PDF."),
             ("Kan jag ta bort och vrida sidor samtidigt?", "Ja. Varje sida har knappar för att vrida och ta bort, och allt sparas i en och samma ny fil."),
             ("Fungerar det på mobilen?", "Dra och släpp fungerar bäst med mus. På pekskärm använder du pilknapparna under varje sida."),
             ("Laddas filen upp?", "Nej. Allt sker i din webbläsare och filen lämnar aldrig din dator.")],
        related=["merge", "rotate", "delete-pages", "split"],
        ui=dict(org_btn="Spara ny PDF", org_none="Flytta, vrid eller ta bort en sida för att fortsätta.", org_summary="{n} {n:sida|sidor} i den nya filen.",
                org_hint="Dra sidorna i ny ordning, eller använd knapparna under varje sida.", org_done="Den nya filen har {n} {n:sida|sidor}.", out_suffix="omordnad"),
    ),
    "en": dict(
        title="Organize PDF – Reorder Pages Free | Retypee",
        desc="Drag pages into a new order, turn them or remove them, all in one view. Free, in your browser and without uploading.",
        h1="Organize a PDF – *drag the pages* into place.",
        lede="See every page as a thumbnail. Move, turn and remove until it looks right, then save a new PDF.",
        steps_h2="How to reorder the pages in a PDF",
        steps=[("Open the PDF.", "The pages are shown as thumbnails."),
               ("Drag, turn and remove.", "Drag a page to a new place or use the arrows. Turn with ↺ and ↻, and remove with ✕."),
               ("Save.", "You get a new PDF with the pages in the order you chose.")],
        sections=[
            {"h2": "Common uses", "ul": [
                "Move an attachment to the right place.",
                "Turn scanned pages that came out wrong and remove a blank page while you are at it.",
                "Put things in the right order after merging files with {{link:merge}}."]},
            {"h2": "Good to know", "ul": [
                "Click ✕ again to bring a removed page back.",
                "The original file is not changed. You download a new one.",
                "If you only need to turn or only remove pages there are simpler tools: {{link:rotate}} and {{link:delete-pages}}.",
                "Password-protected PDFs have to be unlocked first."]},
        ],
        faq_h2="Questions about organizing PDFs",
        faq=[("How do I change the order of pages in a PDF?", "Open the file, drag the pages into place and click Save new PDF."),
             ("Can I remove and turn pages at the same time?", "Yes. Every page has buttons to turn and remove it, and everything is saved in one new file."),
             ("Does it work on a phone?", "Drag and drop works best with a mouse. On a touch screen use the arrow buttons under each page."),
             ("Is the file uploaded?", "No. Everything happens in your browser and the file never leaves your computer.")],
        related=["merge", "rotate", "delete-pages", "split"],
        ui=dict(org_btn="Save new PDF", org_none="Move, turn or remove a page to continue.", org_summary="{n} {n:page|pages} in the new file.",
                org_hint="Drag the pages into a new order, or use the buttons under each page.", org_done="The new file has {n} {n:page|pages}.", out_suffix="reordered"),
    ),
}

# ------------------------------------------------------------------ compare
TOOLS2["compare"] = {
    "sv": dict(
        title="Jämför PDF – se vad som ändrats i texten | Retypee",
        desc="Jämför två versioner av en PDF och se vilka rader som lagts till eller tagits bort. Gratis, i webbläsaren och utan uppladdning.",
        h1="Jämför två PDF-filer – *se vad som ändrats*.",
        lede="Välj originalet och den ändrade versionen. Retypee visar rad för rad vad som tagits bort och vad som lagts till.",
        steps_h2="Så jämför du två PDF-filer",
        steps=[("Välj de två filerna.", "Släpp originalet till vänster och den nya versionen till höger."),
               ("Jämför.", "Texten i båda läses ut och jämförs rad för rad."),
               ("Läs ändringarna.", "Borttaget visas i rött och tillagt i grönt, med sidnummer. Slå på Visa all text för att se hela dokumentet.")],
        sections=[
            {"h2": "Det här jämförs", "ul": [
                "Texten på sidorna, rad för rad.",
                "Sidnummer visas för varje rad så att du hittar rätt."]},
            {"h2": "Det här jämförs inte", "ul": [
                "Layout, färger och bilder. Bara text.",
                "Skannade sidor utan text. Kör OCR först.",
                "Filer som är helt olika. Då får du ett meddelande i stället för en lång lista."]},
            {"h2": "Bra att veta", "ul": [
                "Ingenting sparas eller laddas upp. Resultatet finns bara på skärmen.",
                "Har du ändrat ett enda ord markeras hela raden.",
                "Vill du själv ändra texten i en fil, använd {{link:replace-text}}."]},
        ],
        faq_h2="Vanliga frågor om att jämföra PDF",
        faq=[("Hur jämför jag två PDF-filer?", "Släpp originalet och den ändrade versionen på sidan och klicka på Jämför. Du ser vilka rader som tagits bort och lagts till."),
             ("Kan jag jämföra bilder och layout?", "Nej, bara texten jämförs."),
             ("Varför säger den att ingen text hittades?", "Då är sidorna troligen skannade bilder utan text. De behöver OCR innan de går att jämföra."),
             ("Laddas filerna upp?", "Nej. Allt sker i din webbläsare och filerna lämnar aldrig din dator.")],
        related=["replace-text", "merge", "pdf-to-text", "metadata"],
        ui=dict(cmp_a="Original", cmp_b="Ändrad version", cmp_btn="Jämför", cmp_notext="Ingen text hittades i en av filerna. Är sidorna skannade bilder behöver de OCR först.",
                cmp_toobig="Filerna skiljer sig för mycket för att jämföras rad för rad.", cmp_removed="{n} {n:rad|rader} borttagna", cmp_added="{n} {n:rad|rader} tillagda",
                cmp_found="Ändringar hittades", cmp_identical="Texten är identisk.", cmp_all="Visa all text", cmp_note="Bara texten jämförs. Layout, färger och bilder ingår inte."),
    ),
    "en": dict(
        title="Compare PDF – See What Changed in the Text | Retypee",
        desc="Compare two versions of a PDF and see which lines were added or removed. Free, in your browser and without uploading.",
        h1="Compare two PDFs – *see what changed*.",
        lede="Choose the original and the changed version. Retypee shows line by line what was removed and what was added.",
        steps_h2="How to compare two PDFs",
        steps=[("Choose the two files.", "Drop the original on the left and the new version on the right."),
               ("Compare.", "The text of both is read out and compared line by line."),
               ("Read the changes.", "Removed lines are shown in red and added lines in green, with page numbers. Turn on Show all text to see the whole document.")],
        sections=[
            {"h2": "What is compared", "ul": [
                "The text on the pages, line by line.",
                "A page number is shown for every line so you can find the place."]},
            {"h2": "What is not compared", "ul": [
                "Layout, colours and images. Text only.",
                "Scanned pages without text. Run OCR first.",
                "Files that are completely different. You get a message instead of a long list."]},
            {"h2": "Good to know", "ul": [
                "Nothing is saved or uploaded. The result only exists on the screen.",
                "If you changed a single word the whole line is marked.",
                "If you want to change the text in a file yourself, use {{link:replace-text}}."]},
        ],
        faq_h2="Questions about comparing PDFs",
        faq=[("How do I compare two PDFs?", "Drop the original and the changed version on the page and click Compare. You see which lines were removed and added."),
             ("Can I compare images and layout?", "No, only the text is compared."),
             ("Why does it say no text was found?", "The pages are probably scanned images without text. They need OCR before they can be compared."),
             ("Are the files uploaded?", "No. Everything happens in your browser and the files never leave your computer.")],
        related=["replace-text", "merge", "pdf-to-text", "metadata"],
        ui=dict(cmp_a="Original", cmp_b="Changed version", cmp_btn="Compare", cmp_notext="No text was found in one of the files. If the pages are scanned images they need OCR first.",
                cmp_toobig="The files differ too much to be compared line by line.", cmp_removed="{n} {n:line|lines} removed", cmp_added="{n} {n:line|lines} added",
                cmp_found="Changes found", cmp_identical="The text is identical.", cmp_all="Show all text", cmp_note="Only the text is compared. Layout, colours and images are not included."),
    ),
}

# ------------------------------------------------------------------ PDF to text
TOOLS2["pdf-to-text"] = {
    "sv": dict(
        title="PDF till text – hämta texten ur en PDF gratis | Retypee",
        desc="Hämta texten ur en PDF som .txt eller Markdown, med rubriker och stycken. Gratis, i webbläsaren och utan uppladdning.",
        h1="PDF till text – *hämta orden* ur dokumentet.",
        lede="Spara texten från en PDF som vanlig textfil eller Markdown. Filen läses i din webbläsare och laddas inte upp.",
        steps_h2="Så hämtar du texten ur en PDF",
        steps=[("Öppna PDF-filen.", "Släpp den på sidan."),
               ("Välj format.", "Vanlig text behåller raderna som i PDF-filen. Markdown försöker känna igen rubriker och stycken."),
               ("Hämta texten.", "Du får en fil och ser början av texten direkt.")],
        sections=[
            {"h2": "Bra för", "ul": [
                "Att kopiera text till ett annat dokument.",
                "Att söka i eller bearbeta texten i ett annat program.",
                "Att få innehållet i en form som skärmläsare och AI-verktyg hanterar väl."]},
            {"h2": "Bra att veta", "ul": [
                "Bara text som finns i filen hämtas. Skannade sidor är bilder och saknar text, så kör OCR först.",
                "Markdown-rubriker gissas utifrån textstorlek, så kontrollera resultatet.",
                "Tabeller blir rader med text, inte tabeller.",
                "Vill du ha sidorna som bilder i stället, använd {{link:pdf-to-jpg}}."]},
        ],
        faq_h2="Vanliga frågor om PDF till text",
        faq=[("Hur hämtar jag texten ur en PDF?", "Öppna filen, välj format och klicka på Hämta texten. Du laddar ner en .txt- eller .md-fil."),
             ("Varför blir texten tom?", "Då är sidorna troligen skannade bilder. De har ingen text att hämta och behöver OCR först."),
             ("Behålls tabeller och bilder?", "Nej. Bara texten hämtas. Tabeller blir rader med text och bilder tas inte med."),
             ("Laddas filen upp?", "Nej. Texten läses ut i din webbläsare och filen lämnar aldrig din dator.")],
        related=["pdf-to-jpg", "compare", "home", "metadata"],
        ui=dict(txt_btn="Hämta texten", txt_format="Format", txt_plain="Vanlig text (.txt)", txt_md="Markdown (.md)", txt_pages="Markera var sidorna börjar",
                txt_none="Ingen text hittades. Är sidorna skannade bilder behöver de OCR först.", txt_done="Texten från {n} {n:sida|sidor} är hämtad."),
    ),
    "en": dict(
        title="PDF to Text – Get the Text Out of a PDF Free | Retypee",
        desc="Get the text out of a PDF as .txt or Markdown, with headings and paragraphs. Free, in your browser and without uploading.",
        h1="PDF to text – *get the words* out of the document.",
        lede="Save the text of a PDF as a plain text file or Markdown. The file is read in your browser and is not uploaded.",
        steps_h2="How to get the text out of a PDF",
        steps=[("Open the PDF.", "Drop it on the page."),
               ("Choose a format.", "Plain text keeps the lines as they are in the PDF. Markdown tries to recognise headings and paragraphs."),
               ("Get the text.", "You get a file and see the start of the text straight away.")],
        sections=[
            {"h2": "Good for", "ul": [
                "Copying text into another document.",
                "Searching or processing the text in another program.",
                "Getting the content in a form that screen readers and AI tools handle well."]},
            {"h2": "Good to know", "ul": [
                "Only text that exists in the file is extracted. Scanned pages are images without text, so run OCR first.",
                "Markdown headings are guessed from the size of the text, so check the result.",
                "Tables become lines of text, not tables.",
                "If you want the pages as images instead, use {{link:pdf-to-jpg}}."]},
        ],
        faq_h2="Questions about PDF to text",
        faq=[("How do I get the text out of a PDF?", "Open the file, choose a format and click Get the text. You download a .txt or .md file."),
             ("Why is the text empty?", "The pages are probably scanned images. They have no text to extract and need OCR first."),
             ("Are tables and images kept?", "No. Only the text is extracted. Tables become lines of text and images are left out."),
             ("Is the file uploaded?", "No. The text is read out in your browser and the file never leaves your computer.")],
        related=["pdf-to-jpg", "compare", "home", "metadata"],
        ui=dict(txt_btn="Get the text", txt_format="Format", txt_plain="Plain text (.txt)", txt_md="Markdown (.md)", txt_pages="Mark where the pages begin",
                txt_none="No text was found. If the pages are scanned images they need OCR first.", txt_done="The text from {n} {n:page|pages} was extracted."),
    ),
}
