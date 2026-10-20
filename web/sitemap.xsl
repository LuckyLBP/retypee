<?xml version="1.0" encoding="UTF-8"?>
<!-- Renders sitemap.xml as a readable page in a browser. Search engines fetch the XML
     directly and ignore this; it only runs client-side for a human visitor. -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9">
  <xsl:output method="html" encoding="UTF-8" indent="no"/>
  <xsl:template match="/">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <meta name="robots" content="noindex"/>
        <title>Sitemap – Retypee</title>
        <style>
          :root { color-scheme: light dark; --paper: #faf9f6; --card: #fff; --ink: #1b1713; --ink-soft: #6a645b; --line: rgba(27,23,19,.14); --yellow: #f6c945; }
          @media (prefers-color-scheme: dark) { :root { --paper: #15130f; --card: #1f1c17; --ink: #f3f1ec; --ink-soft: #aca89f; --line: rgba(255,255,255,.14); } }
          * { box-sizing: border-box; }
          body { margin: 0; background: var(--paper); color: var(--ink); font: 15px/1.5 -apple-system, "Segoe UI", system-ui, sans-serif; }
          main { max-width: 860px; margin: 0 auto; padding: 32px 20px 64px; }
          h1 { font-size: 22px; margin: 0 0 4px; }
          p.lead { color: var(--ink-soft); margin: 0 0 24px; font-size: 14px; }
          table { width: 100%; border-collapse: collapse; background: var(--card); border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
          th, td { padding: 10px 14px; text-align: left; border-bottom: 1px solid var(--line); font-size: 13.5px; vertical-align: top; }
          th { font-size: 11.5px; text-transform: uppercase; letter-spacing: .04em; color: var(--ink-soft); background: var(--paper); }
          tr:last-child td { border-bottom: 0; }
          td a { color: var(--ink); text-decoration: none; word-break: break-all; }
          td a:hover { text-decoration: underline; }
          .lang { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 600; background: var(--yellow); color: #1b1713; }
          .lang.en { background: var(--line); color: var(--ink); }
          .num { color: var(--ink-soft); }
        </style>
      </head>
      <body>
        <main>
          <h1>Sitemap</h1>
          <p class="lead"><xsl:value-of select="count(s:urlset/s:url)"/> URLs · generated from sitemap.xml</p>
          <table>
            <thead>
              <tr>
                <th>URL</th>
                <th>Language</th>
                <th>Priority</th>
                <th>Last modified</th>
              </tr>
            </thead>
            <tbody>
              <xsl:for-each select="s:urlset/s:url">
                <tr>
                  <td><a href="{s:loc}"><xsl:value-of select="s:loc"/></a></td>
                  <td>
                    <xsl:choose>
                      <xsl:when test="contains(s:loc, '://retypee.se/en/') or s:loc = 'https://retypee.se/en/'">
                        <span class="lang en">EN</span>
                      </xsl:when>
                      <xsl:otherwise>
                        <span class="lang">SV</span>
                      </xsl:otherwise>
                    </xsl:choose>
                  </td>
                  <td class="num"><xsl:value-of select="s:priority"/></td>
                  <td class="num"><xsl:value-of select="s:lastmod"/></td>
                </tr>
              </xsl:for-each>
            </tbody>
          </table>
        </main>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
