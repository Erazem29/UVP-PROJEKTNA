import os
import re
from bs4 import BeautifulSoup

MAPA_PODATKI = "podatki"
MAPA_HTML = os.path.join(MAPA_PODATKI, "html")

def izlusci_podatke_iz_html():
    """
    Prebere vse shranjene HTML datoteke v mapi 'podatki/html/'
    in izlušči naslov, izvajalca, leto, žanre, oceno ter število recenzij.
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
            # 1. Izvajalec in Naslov
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

            # 2. Ocena
            ocena_el = vrstica.find("div", class_="scoreValue")
            ocena = ocena_el.text.strip() if ocena_el else None

            # 3. Število recenzij
            reviews_el = vrstica.find("div", class_="scoreText")
            st_recenzij = None
            if reviews_el:
                tekst = reviews_el.text.strip()
                match = re.search(r'([\d,]+)', tekst)
                if match:
                    st_recenzij = match.group(1).replace(",", "")

            # 4. Leto izida
            date_el = vrstica.find("div", class_="albumListDate")
            leto = None
            if date_el:
                match_leto = re.search(r'\b(19\d\d|20\d\d)\b', date_el.text)
                if match_leto:
                    leto = match_leto.group(1)

            # 5. Žanri
            genre_el = vrstica.find("div", class_="albumListGenre")
            zanri = genre_el.text.strip() if genre_el else None

            vsi_albumi.append({
                "izvajalec": izvajalec,
                "naslov": naslov,
                "leto": leto,
                "zanri": zanri,
                "ocena": ocena,
                "st_recenzij": st_recenzij,
            })

    print(f"\nIzluščenje uspešno zaključen!")
    print(f"Skupaj izluščenih albumov: {len(vsi_albumi)}")
    return vsi_albumi

if __name__ == "__main__":
    izlusci_podatke_iz_html()