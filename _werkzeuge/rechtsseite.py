"""Stellt eine alte Rechtsseite (Datenschutz, Impressum; DE oder EN) auf das neue Design um.
Der Text der Seite bleibt unverändert; nur Kopf, Fuß und Stil werden ersetzt.
Aufruf: python _werkzeuge/rechtsseite.py datenschutz/index.html impressum/index.html en/datenschutz/index.html ..."""
import re, sys

for pfad in sys.argv[1:]:
    s = open(pfad, encoding='utf-8').read()
    en = pfad.startswith('en/')
    tiefe = '../../' if en else '../'
    if 'css/seite.css' in s:
        print(pfad, 'schon umgestellt'); continue

    # Kopf: alten Stil raus, Schriften und gemeinsamen Stil rein
    s = re.sub(r'\s*<style>.*?</style>', '', s, count=1, flags=re.S)
    s = s.replace('</head>', f'  <meta name="theme-color" content="#f6fafb">\n  <link rel="stylesheet" href="{tiefe}fonts/fonts.css">\n  <link rel="stylesheet" href="{tiefe}css/seite.css">\n</head>', 1)

    # Sprachlink aus der alten Kopfzeile holen
    m = re.search(r'<div class="top-row">(.*?)</div>', s, flags=re.S)
    alt = m.group(1)
    if en:
        de = re.search(r'<a href="([^"]+)">DE</a>', alt).group(1)
        sprache = f'<a class="zurueck" href="{de}" lang="de">Deutsch</a>'
        zurueck, skip, laden = 'Back to ixilotl.de', 'Skip to content', 'Get it on Google Play'
    else:
        en_link = re.search(r'<a href="([^"]+)">EN</a>', alt).group(1)
        sprache = f'<a class="zurueck" href="{en_link}" lang="en">English</a>'
        zurueck, skip, laden = 'Zurück zu ixilotl.de', 'Zum Inhalt', 'Bei Google Play laden'
    kopf = f'''<a class="skip" href="#inhalt">{skip}</a>
<header class="kopf"><div class="kopf__in">
  <a class="logo" href="../"><img src="{tiefe}images/ixilotl-icon.png" alt="" width="32" height="32">Ixilotl</a>
  <a class="btn" href="https://play.google.com/store/apps/details?id=com.ixilotl.ixilotl">{laden}</a>
</div></header>

<main id="inhalt" class="recht">
<a class="zurueck" href="../">&larr; {zurueck}</a> · {sprache}'''
    s = s.replace(m.group(0), kopf, 1)

    # alte Fußzeile im Text ("Siehe auch ...") entfernen, neuer Fuß
    s = re.sub(r'\s*<p style="margin-top:3em;[^>]*>.*?</p>', '', s, count=1, flags=re.S)
    if en:
        links = '<a href="../impressum/">Legal notice</a><a href="../datenschutz/">Privacy policy</a><a href="../nutzungsbedingungen/">Terms of use</a>'
    else:
        links = '<a href="../impressum/">Impressum</a><a href="../datenschutz/">Datenschutz</a><a href="../nutzungsbedingungen/">Nutzungsbedingungen</a>'
    fuss = f'''
</main>

<footer class="fuss"><div class="fuss__in">
  <span>&copy; 2026 Sumpfsoftwarestudio</span>
  {links}<a href="mailto:support@ixilotl.de">support@ixilotl.de</a>
</div></footer>
</body>'''
    s = s.replace('\n</body>', fuss, 1)
    s = s.replace('class="updated"', 'class="stand"')
    open(pfad, 'w', encoding='utf-8').write(s)
    print(pfad, 'umgestellt')
