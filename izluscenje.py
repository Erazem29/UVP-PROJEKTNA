import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

MAPA_PODATKI = "podatki"
MAPA_HTML = os.path.join(MAPA_PODATKI, "html")

PLATFORME_VZORCI = {
    "open.spotify.com": "Spotify",
    "music.apple.com": "Apple Music",
    "geo.music.apple.com": "Apple Music",
    "soundcloud.com": "SoundCloud",
    "bandcamp.com": "Bandcamp",
    "amazon.com": "Amazon",
    "amzn.to": "Amazon (Vinyl)",
}


def izlusci_podatke_iz_html():
    """
    Prebere vse shranjene HTML datoteke v mapi 'podatki/html/'
    in izlušči naslov, izvajalca, celoten datum izida, žanre, oceno,
    število recenzij ter platforme, na katerih je album na voljo.
    Vrača seznam slovarjev.
    """
    vsi_albumi = []

    datoteke = [f for f in os.listdir(MAPA_HTML) if f.endswith(".html")]
    datoteke.sort()

    print(f"Začenjam obdelavo {len(datoteke)} HTML datotek...")

    for ime_datoteke in datoteke:
        pot = os.path.join(MAPA_HTML, ime_datoteke)

        with open(pot, "r", encoding="utf-8") as f:
            vsebina = f.read()

        soup = BeautifulSoup(vsebina, "html.parser")
        vrstice = soup.find_all("div", class_="albumListRow")

        for vrstica in vrstice:
            naslov_el = vrstica.find("h2", class_="albumListTitle")
            povezava = naslov_el.find("a") if naslov_el else None

            if povezava:
                polno_ime = povezava.text.strip()
                if " - " in polno_ime:
                    izvajalec, naslov = polno_ime.split(" - ", 1)
                else:
                    izvajalec, naslov = "Neznano", polno_ime
            else:
                izvajalec, naslov = "Neznano", "Neznano"

            ocena_el = vrstica.find("div", class_="scoreValue")
            ocena = ocena_el.text.strip() if ocena_el else None

            reviews_el = vrstica.find("div", class_="scoreText")
            st_recenzij = None
            if reviews_el:
                tekst = reviews_el.text.strip()
                match = re.search(r'([\d,]+)', tekst)
                if match:
                    st_recenzij = match.group(1).replace(",", "")

            date_el = vrstica.find("div", class_="albumListDate")
            datum_izida, leto, mesec = None, None, None
            if date_el:
                besedilo = date_el.text.strip()
                try:
                    datum_izida = datetime.strptime(besedilo, "%B %d, %Y")
                    leto = datum_izida.year
                    mesec = datum_izida.month
                except ValueError:
                    match_leto = re.search(r'\b(19\d\d|20\d\d)\b', besedilo)
                    if match_leto:
                        leto = int(match_leto.group(1))

            genre_el = vrstica.find("div", class_="albumListGenre")
            if genre_el:
                genre_povezave = genre_el.find_all("a")
                zanri = ", ".join(a.text.strip() for a in genre_povezave) if genre_povezave else None
            else:
                zanri = None

            platforme = set()
            for a in vrstica.find_all("a", href=True):
                href = a["href"]
                for vzorec, ime_platforme in PLATFORME_VZORCI.items():
                    if vzorec in href:
                        platforme.add(ime_platforme)
                        break
            platforme_niz = ", ".join(sorted(platforme)) if platforme else None

            vsi_albumi.append({
                "izvajalec": izvajalec,
                "naslov": naslov,
                "datum_izida": datum_izida.strftime("%Y-%m-%d") if datum_izida else None,
                "leto": leto,
                "mesec": mesec,
                "zanri": zanri,
                "ocena": ocena,
                "st_recenzij": st_recenzij,
                "platforme": platforme_niz,
            })

    print(f"\nIzluščenje uspešno zaključeno!")
    print(f"Skupaj izluščenih albumov: {len(vsi_albumi)}")
    return vsi_albumi


if __name__ == "__main__":
    izlusci_podatke_iz_html()
