HOME = {'sv': {'h1': 'Redigera text i valfri PDF, direkt i *webbläsaren*.',
        'lede': 'Gratis PDF-redigerare som aldrig laddar upp din fil. Klicka på en rad, skriv, ladda ner.',
        'title': 'Redigera PDF gratis – ändra text utan uppladdning | Retypee',
        'desc': 'Ändra text i en PDF direkt i webbläsaren: klicka på en rad, skriv och ladda ner. Sök och ersätt i hela filen. Gratis, och '
                'din PDF laddas aldrig upp.',
        'og_title': 'Redigera PDF gratis – ändra text utan uppladdning',
        'og_desc': 'Klicka på en rad i din PDF, skriv och ladda ner. Allt sker i webbläsaren, så din fil lämnar aldrig din enhet.',
        'steps_h2': 'Så fungerar det',
        'steps': [('Öppna din PDF.', 'Släpp den på sidan. Varje textrad blir klickbar.'),
                  ('Klicka på en rad och skriv.',
                   'Ändra text, typsnitt, storlek eller färg. Använd Lägg till text för att placera ny text var som helst.'),
                  ('Ladda ner.', 'Du får en vanlig PDF med dina ändringar. Bilder, länkar och formulärfält förblir som de var.')],
        'sections': [{'h2': 'Sök och ersätt',
                      'p': ['Behöver du ändra ett datum, ett namn eller ett fakturanummer som finns på varje sida? Tryck Ctrl/Cmd+F, skriv '
                            'vad du vill hitta och vad det ska bytas mot, så ändrar Retypee alla träffar på en gång. En räknare visar hur '
                            'många träffar det finns innan du bekräftar, och Ångra tar tillbaka allt.']},
                     {'h2': 'Privat från grunden',
                      'p': ['Retypee är en webbsida, men redigeringen sker inte på en server. PDF-motorn (<a '
                            'href="https://pymupdf.readthedocs.io">PyMuPDF</a>) laddas ner till din webbläsare från ett CDN (jsDelivr) – '
                            'bara motorn, aldrig din fil – och din fil öppnas och redigeras i enhetens minne. Ingenting laddas upp eller '
                            'sparas, och när du stänger fliken är filen borta. Du kan kontrollera det i webbläsarens nätverksflik.',
                            'Den nedladdade PDF-filen har dessutom sina metadata borttagna: titel, författare, skapande program, datum och '
                            'fil-ID.']},
                     {'h2': 'Bra att veta',
                      'ul': ['<strong>Texten flödar inte om.</strong> PDF-filer lagrar text på fasta positioner, så rader redigeras en i '
                             'taget. Längre text fortsätter längre åt höger; använd <em>Pressa ihop så den ryms</em> eller korta ner den.',
                             '<strong>Skannade PDF-filer saknar text.</strong> Kör OCR först (till exempel med <code>ocrmypdf</code>) och '
                             'öppna sedan resultatet.',
                             '<strong>Typsnitt kan skilja sig något.</strong> PDF-filer bäddar oftast bara in de bokstäver som används. '
                             'Saknas en bokstav du skriver använder Retypee ett passande inbyggt typsnitt. Använd <em>Lägg till '
                             'typsnitt</em> och ge den originalfilen (<code>.ttf</code> eller <code>.otf</code>) för en exakt matchning.',
                             'Roterad eller lodrät text och lösenordsskyddade PDF-filer stöds inte ännu.']}],
        'faq_h2': 'Vanliga frågor',
        'faq': [('Laddas min PDF upp någonstans?',
                 'Nej. Retypee körs i din webbläsarflik. Din PDF öppnas och redigeras i enhetens minne, och inget skickas till en server '
                 'eller sparas. Det enda som hämtas är själva redigeringsmotorn (från ett CDN), aldrig din fil. När du stänger fliken är '
                 'den glömd.'),
                ('Kan jag redigera en skannad PDF?',
                 'Inte direkt. En skannad PDF är en bild av text, så det finns ingen text att redigera. Kör den genom OCR först (till '
                 'exempel med ocrmypdf) och öppna sedan resultatet i Retypee.'),
                ('Varför ser min redigerade text lite annorlunda ut?',
                 'PDF-filer bäddar oftast bara in de bokstäver som används. Om originaltypsnittet saknar en bokstav du skrivit letar '
                 'Retypee efter samma typsnitt bland dem du lagt till, och använder annars Helvetica, Times eller Courier i närmaste stil. '
                 'Använd Lägg till typsnitt för att ge den originalfilen för en exakt matchning.'),
                ('Behåller den redigerade PDF-filen sina metadata?',
                 'Nej. Den nedladdade filen har sina metadata borttagna: titel, författare, skapande program, datum, XMP-data och fil-ID. '
                 'Det synliga innehållet, bilder, länkar och formulärfält påverkas inte.'),
                ('Flödar längre text om i stycket?',
                 'Nej. PDF-filer lagrar text på fasta positioner, inte som stycken, så rader redigeras en i taget. Om ny text är längre '
                 'fortsätter den längre åt höger; använd Pressa ihop så den ryms eller korta ner den.')]},
 'en': {'h1': 'Edit text in any PDF, right in your *browser*.',
        'lede': 'The free PDF editor that never uploads your file. Click a line, type, download.',
        'title': 'Edit PDF Text Online Free – No Upload | Retypee',
        'desc': 'Edit text in a PDF right in your browser. Click a line, type, download. Find and replace across the whole file. Free, and '
                'your PDF is never uploaded.',
        'og_title': 'Edit PDF Text Online Free – No Upload',
        'og_desc': 'Click a line in your PDF, type, download. It all happens in your browser, so your file never leaves your device.',
        'steps_h2': 'How it works',
        'steps': [('Open your PDF.', 'Drop it on this page. Every line of text becomes clickable.'),
                  ('Click a line and type.', 'Change the text, font, size or colour. Use Add text to put new text anywhere.'),
                  ('Download.', 'You get a normal PDF with your changes. Images, links and form fields stay as they were.')],
        'sections': [{'h2': 'Find and replace',
                      'p': ['Need to change a date, a name or an invoice number that appears on every page? Press Ctrl/Cmd+F, type what to '
                            'find and what to replace it with, and Retypee changes every match in one go. A live counter shows how many '
                            'matches there are before you commit, and Undo brings everything back.']},
                     {'h2': 'Private by design',
                      'p': ['Retypee is a web page, but the editing does not happen on a server. The PDF engine (<a '
                            'href="https://pymupdf.readthedocs.io">PyMuPDF</a>) is downloaded into your browser from a CDN (jsDelivr) – '
                            "only the engine, never your file – and your file is opened and edited in your device's memory. Nothing is "
                            "uploaded or stored, and closing the tab forgets it. You can check this in your browser's network tab.",
                            'The downloaded PDF also has its metadata removed: title, author, creator app, dates, and the file ID.']},
                     {'h2': 'Good to know',
                      'ul': ['<strong>Text does not reflow.</strong> PDFs store text at fixed positions, so lines are edited one at a '
                             'time. Longer text runs further right; use <em>Squeeze to fit</em> or shorten it.',
                             '<strong>Scanned PDFs have no text.</strong> Run OCR first (for example with <code>ocrmypdf</code>), then '
                             'open the result.',
                             '<strong>Fonts may differ slightly.</strong> PDFs usually embed only the letters they use. If a letter you '
                             'type is missing, Retypee uses a fitting built-in font. Use <em>Add font</em> to give it the original '
                             '<code>.ttf</code> or <code>.otf</code> for an exact match.',
                             'Rotated or vertical text and password-protected PDFs are not supported yet.']}],
        'faq_h2': 'Questions',
        'faq': [('Is my PDF uploaded anywhere?',
                 "No. Retypee runs inside your browser tab. Your PDF is opened and edited in your device's memory, and nothing is sent to "
                 'a server or stored. Only the editing engine is downloaded (from a CDN), never your file. Closing the tab forgets it.'),
                ('Can I edit a scanned PDF?',
                 'Not directly. A scanned PDF is a picture of text, so there is no text to edit. Run it through OCR first (for example '
                 'with ocrmypdf) and then open the result in Retypee.'),
                ('Why does my edited text look slightly different?',
                 'PDFs usually embed only the letters they use. If the original font does not contain a letter you typed, Retypee looks '
                 'for the same font among the fonts you added, and otherwise falls back to Helvetica, Times or Courier in the closest '
                 'style. Use Add font to give it the original font file for an exact match.'),
                ('Does the edited PDF keep its metadata?',
                 'No. The downloaded file has its metadata removed: title, author, creator app, dates, XMP data and the file ID. The '
                 'visible content, images, links and form fields are not touched.'),
                ('Will longer text reflow the paragraph?',
                 'No. PDFs store text at fixed positions, not as paragraphs, so lines are edited one at a time. If new text is longer it '
                 'runs further right; use Squeeze to fit or shorten it.')]}}

HOME["sv"]["features"] = ["Redigera text i PDF", "Lägg till text", "Sök och ersätt", "Ångra och gör om", "Egna typsnitt", "Tar bort metadata vid nedladdning"]
HOME["en"]["features"] = ["Edit text in a PDF", "Add text", "Find and replace", "Undo and redo", "Your own fonts", "Removes metadata on download"]
for _l in ("sv", "en"):
    HOME[_l]["related"] = ["merge", "split", "metadata", "jpg-to-pdf"]
