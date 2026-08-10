# Analiza najbolje ocenjenih albumov (AlbumOfTheYear)

Projektna naloga pri predmetu Uvod v programiranje. Skripta zajame podatke o 500 najbolje ocenjenih albumih s spletne strani [AlbumOfTheYear](https://www.albumoftheyear.org/) ter izvede osnovno statistično analizo.

## Struktura projekta

- `zajem.py` – Prenaša HTML strani s spleta in jih lokalno shranjuje v `podatki/html/`.
- `izluscenje.py` – Parsira podatke (izvajalec, naslov, leto, žanri, ocena, št. recenzij) iz lokalnih HTML datotek.
- `naredi_csv.py` – Zapisuje izluščene podatke v `podatki/albumi.csv`.
- `main.py` – Glavna skripta, ki povezuje celoten cevovod (pipeline).
- `analiza.ipynb` – Jupyter zvezek z analizo in vizualizacijo podatkov.
- `podatki/` – Mapa z shranjenimi HTML datotekami in končno CSV datoteko.

## Navodila za zagon

1. **Aktivacija virtualnega okolja (če uporabljate venv):**
   ```powershell
   .\venv\Scripts\Activate.ps1