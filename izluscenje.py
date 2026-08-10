import os
import re
from bs4 import BeautifulSoup
import pandas as pd

MAPA_PODATKI = "podatki"
MAPA_HTML = os.path.join(MAPA_PODATKI, "html")

def izlusci_podatke_iz_html():
    """
    Prebere vse shranjene HTML datoteke v mapi 'podatki/html/'
    in izlušči naslov, izvajalca, leto, žanre, oceno ter število recenzij.
    """
    vsi_albumi = []
    
    # Preverimo vse .html datoteke v mapi
    datoteke = [f for f in os.listdir(MAPA_HTML) if f.endswith(".html")]
    datoteke.sort() # Razvrstimo jih po vrstnem redu (stran_01, stran_02...)

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

            # 3. Število recenzij (pogosto piše npr. "1,250 ratings" ali "85 reviews")
            reviews_el = vrstica.find("div", class_="scoreText")
            st_recenzij = None
            if reviews_el:
                tekst = reviews_el.text.strip()
                match = re.search(r'([\d,]+)', tekst)
                if match:
                    st_recenzij = match.group(1).replace(",", "")

            # 4. Datum / Leto izida ali Žanri (če obstajajo v podrobnostih vrstice)
            # Na AOTY je datum pogosto v div.albumListDate ali v podrobnostih pod naslovom
            date_el = vrstica.find("div", class_="albumListDate")
            leto = None
            if date_el:
                match_leto = re.search(r'\b(19\d\d|20\d\d)\b', date_el.text)
                if match_leto:
                    leto = match_leto.group(1)

            # 5. Žanri
            genre_el = vrstica.find("div", class_="albumListGenre")
            zanri = genre_el.text.strip() if genre_el else None

            # Dodamo slovar v seznam
            vsi_albumi.append({
                "izvajalec": izvajalec,
                "naslov": naslov,
                "leto": leto,
                "zanri": zanri,
                "ocena": ocena,
                "st_recenzij": st_recenzij,
            })

    # Pretvorimo v Pandas DataFrame in shranimo v CSV
    df = pd.DataFrame(vsi_albumi)
    
    os.makedirs(MAPA_PODATKI, exist_ok=True)
    pot_csv = os.path.join(MAPA_PODATKI, "albumi.csv")
    df.to_csv(pot_csv, index=False, encoding="utf-8-sig")
    
    print(f"\nIzluščenje uspešno zaključeno!")
    print(f"Skupaj izluščenih albumov: {len(df)}")
    print(f"Shranjeno v '{pot_csv}'.")
    return df

if __name__ == "__main__":
    izlusci_podatke_iz_html()