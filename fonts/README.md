# Your own fonts

Put `.ttf`, `.otf` or `.ttc` files here.

- When a PDF uses a font that is not installed on your computer, the editor
  looks here for a file with the same name. Adding the right font file gives
  an exact match instead of the Helvetica, Times or Courier fallback.
- Fonts in this folder also show up in the font menu in the editor.

After adding fonts, restart the app, or call `POST /api/fonts/refresh`.
