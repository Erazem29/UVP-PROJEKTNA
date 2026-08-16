import os
import time
import requests

# Mape za shranjevanje
MAPA_PODATKI = "podatki"
MAPA_HTML = os.path.join(MAPA_PODATKI, "html")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def prenesi_strani(st_strani=20):
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


if __name__ == "__main__":
    prenesi_strani(st_strani=20)