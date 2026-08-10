import os
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Mape za shranjevanje
MAPA_PODATKI = "podatki"
MAPA_HTML = os.path.join(MAPA_PODATKI, "html")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def prenesi_strani(st_strani=20):
    """Prenese posamezne HTML strani in jih shrani lokalno v mapo."""
    os.makedirs(MAPA_HTML, exist_ok=True)
    print(f"Začenjam prenos {st_strani} HTML strani...")

    for stran in range(1, st_strani + 1):
        pot_datoteke = os.path.join(MAPA_HTML, f"stran_{stran:02d}.html")
        
        # Če je stran že prenesena, jo preskočimo
        if os.path.exists(pot_datoteke):
            print(f"Stran {stran} je že prenesena, preskakujem.")
            continue

        url = f"https://www.albumoftheyear.org/ratings/6-highest-rated/all/{stran}"
        print(f"Prenašam stran {stran}/{st_strani}: {url}")
        
        odziv = requests.get(url, headers=HEADERS)
        if odziv.status_code == 200:
            with open(pot_datoteke, "w", encoding="utf-8") as f:
                f.write(odziv.text)
        else:
            print(f"Napaka pri strani {stran}: status {odziv.status_code}")

        time.sleep(1.2)


def obdelaj_strani(st_strani=20):
    """Prebere lokalne HTML datoteke in izlušči podatke v CSV datoteko."""
    vsi_albumi = []
    print("\nZačenjam obdelavo lokalnih HTML datotek...")

    for stran in range(1, st_strani + 1):
        pot_datoteke = os.path.join(MAPA_HTML, f"stran_{stran:02d}.html")
        
        if not os.path.exists(pot_datoteke):
            continue

        with open(pot_datoteke, "r", encoding="utf-8") as f:
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

            vsi_albumi.append({
                "izvajalec": izvajalec,
                "naslov": naslov,
                "ocena": ocena,
            })

    df = pd.DataFrame(vsi_albumi)
    
    os.makedirs(MAPA_PODATKI, exist_ok=True)
    pot_csv = os.path.join(MAPA_PODATKI, "albumi.csv")
    df.to_csv(pot_csv, index=False, encoding="utf-8-sig")
    print(f"Zajem in obdelava zaključena! Shranjeno {len(df)} albumov v '{pot_csv}'.")


if __name__ == "__main__":
    prenesi_strani(st_strani=20)
    obdelaj_strani(st_strani=20)