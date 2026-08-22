# Analiza najbolje ocenjenih albumov (AlbumOfTheYear)

Projektna naloga pri predmetu Uvod v programiranje. Program zajame podatke o 1000 najbolje ocenjenih albumih vseh časov s spletne strani [AlbumOfTheYear](https://www.albumoftheyear.org/ratings/6-highest-rated/all/1) (izvajalec, naslov, datum izida, žanri, kritiška ocena, število recenzij, platforme dostopnosti) ter izvede statistično analizo in vizualizacijo podatkov.

## Struktura projekta

- `zajem.py` – Prenaša HTML strani s spleta in jih lokalno shranjuje v `podatki/html/`.
- `izluscenje.py` – Parsira podatke (izvajalec, naslov, datum izida, žanri, ocena, št. recenzij, platforme) iz lokalnih HTML datotek.
- `naredi_csv.py` – Zapisuje izluščene podatke v `podatki/albumi.csv`.
- `main.py` – Glavna skripta, ki povezuje celoten cevovod (pipeline).
- `analiza.ipynb` – Jupyter zvezek z analizo in vizualizacijo podatkov.
- `podatki/` – Mapa s shranjenimi HTML datotekami (`html/`) in končno CSV datoteko (`albumi.csv`).
- `uporaba-ui.md` – Dokumentacija uporabe orodij umetne inteligence pri nastajanju projekta.

## Namestitev

1. **Ustvarite in aktivirajte virtualno okolje:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   (na macOS/Linux: `source venv/bin/activate`)

2. **Namestite potrebne knjižnice:**
   ```bash
   pip install requests beautifulsoup4 pandas matplotlib jupyter
   ```

## Zagon

Celoten cevovod (zajem HTML-ja → izluščenje podatkov → shranjevanje v CSV) poženete z:

```bash
python main.py
```

Privzeto se zajame 40 strani (1000 albumov). Neobvezni argumenti:

- `-p N` / `--pages N` – zajemi N strani namesto privzetih 40.
- `-s` / `--skip-download` – preskoči prenos HTML-ja in uporabi že shranjene datoteke v `podatki/html/` (uporabno, če želite samo ponovno izluščiti/shraniti podatke brez novega poizvedovanja po spletu).

Primer:
```bash
python main.py --skip-download
```

Ko je `podatki/albumi.csv` ustvarjen, odprite `analiza.ipynb` (npr. v VS Code ali Jupyterju) in poženite celice od zgoraj navzdol za analizo in grafe.

Pri projektni nalogi sem si bežno pomagal s Claudeom, tu je link do pogovora: https://claude.ai/share/cdc00b04-3791-42db-9f08-1be4dc9dc979
