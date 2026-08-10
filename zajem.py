import os
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

def zajemi_albume(st_strani=20):
    vsi_albumi = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Začenjam zajem {st_strani} strani z AlbumOfTheYear...")

    for stran in range(1, st_strani + 1):
        url = f"https://www.albumoftheyear.org/ratings/6-highest-rated/all/{stran}"
        print(f"Zajemam stran {stran}/{st_strani}: {url}")
        
        odziv = requests.get(url, headers=headers)
        if odziv.status_code != 200:
            print(f"Napaka pri strani {stran}: status {odziv.status_code}")
            continue

        soup = BeautifulSoup(odziv.text, "html.parser")
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

            # 2. Ocena in število ocen (znotraj albumListData ali albumListScore)
            podatki_div = vrstica.find("div", class_="albumListData")
            
            # Ocena kritikov ali uporabnikov
            score_el = vrstica.find("div", class_="albumListScore")
            ocena = score_el.text.strip() if score_el else None

            vsi_albumi.append({
                "izvajalec": izvajalec,
                "naslov": naslov,
                "ocena": ocena,
            })

        # Obvezen premor, da ne preobremenimo strežnika
        time.sleep(1.5)

    df = pd.DataFrame(vsi_albumi)
    
    # Ustvarimo mapo 'podatki', če ne obstaja
    os.makedirs("podatki", exist_ok=True)
    pot_do_datoteke = os.path.join("podatki", "albumi.csv")
    
    df.to_csv(pot_do_datoteke, index=False, encoding="utf-8-sig")
    print(f"\nZajem uspešno zaključen! Shranjeno {len(df)} albumov v '{pot_do_datoteke}'.")

if __name__ == "__main__":
    zajemi_albume(st_strani=20)