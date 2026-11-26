"""Baut das Bild der Startfläche: drei Handy-Screenshots nebeneinander im Rahmen.
Aufruf: python _werkzeuge/hero_bild.py links.jpg mitte.jpg rechts.jpg  -> images/hero-handys.webp
Die Screenshots im Hochformat (etwa 9:19,5). Neue Screenshots einfach hier einsetzen und neu starten."""
import sys
from PIL import Image, ImageDraw

def handy(pfad, breite):
    s = Image.open(pfad).convert("RGB")
    rand = round(breite * 0.032)
    innen_b = breite - 2 * rand
    innen_h = round(innen_b * s.height / s.width)
    s = s.resize((innen_b, innen_h), Image.LANCZOS)
    hoehe = innen_h + 2 * rand
    r_aussen, r_innen = round(breite * 0.14), round(breite * 0.11)
    bild = Image.new("RGBA", (breite, hoehe), (0, 0, 0, 0))
    maske = Image.new("L", (breite, hoehe), 0)
    ImageDraw.Draw(maske).rounded_rectangle((0, 0, breite - 1, hoehe - 1), r_aussen, fill=255)
    bild.paste(Image.new("RGBA", (breite, hoehe), (11, 18, 48, 255)), (0, 0), maske)
    m2 = Image.new("L", s.size, 0)
    ImageDraw.Draw(m2).rounded_rectangle((0, 0, s.width - 1, s.height - 1), r_innen, fill=255)
    bild.paste(s, (rand, rand), m2)
    return bild

def main():
    pfade = sys.argv[1:4]
    W, H = 2560, 760          # Fenster 16:4,75, zeigt das obere Drittel der Handys
    b, abstand = 500, 110
    leinwand = Image.new("RGBA", (W, H), (228, 242, 244, 255))
    x0 = (W - 3 * b - 2 * abstand) // 2
    for i, p in enumerate(pfade):
        h = handy(p, b)
        y = 70 if i != 1 else 40
        leinwand.alpha_composite(h, (x0 + i * (b + abstand), y))
    leinwand.convert("RGB").save("images/hero-handys.webp", quality=84)
    print("images/hero-handys.webp", leinwand.size)

main()
