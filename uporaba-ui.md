# Dokumentacija uporabe umetne inteligence (UI)

## 1. Nastavitev okolja in repozitorija
- **Orodje:** Gemini
- **Namen:** Pomoč pri nastavitvi virtualnega okolja v VS Code, konfiguraciji `.gitignore` ter odpravljanju napake z Windows Long Paths pri namestitvi knjižnic za Jupyter.
## 2. Zajem podatkov (Scraping)
- **Orodje:** Gemini
- **Namen:** Pomoč pri analizi HTML strukture spletne strani `albumoftheyear.org` (selektorji `.albumListRow`, `.albumListTitle`) ter pisanju Python skripte (`zajem.py`) z uporabo `requests`, `BeautifulSoup` in `pandas`.

## Uporaba orodij umetne inteligence (AI)

Pri razvoju projektne naloge so bila orodja umetne inteligence (UI) uporabljena kot pomočnik pri strukturi cevovoda in odpravljanju napak:

- **Strukturiranje cevovoda (Pipeline):** UI je pomagal pri razdelitvi projekta na modularne skripte (`zajem.py`, `izluscenje.py`, `naredi_csv.py` in `main.py`) ter pri implementaciji ukaznih argumentov (`argparse` za `--skip-download`).
- **Parsanje HTML kode:** Pomoč pri ugotavljanju točnih CSS selektorjev v HTML strukturi spletne strani *AlbumOfTheYear* (npr. `div.scoreValue` za izluščenje ocen).
- **Odpravljanje napak (Debugging):** Pomoč pri reševanju napak v okolju in Git orodjih (npr. reševanje težav z `moj-projekt/` podmoduli ter uskladitev tipov podatkov med Pandas DataFrame in seznami slovarjev).
- **Vizualizacija podatkov:** Pomoč pri sestavi kodo za izris histogramov porazdelitve ocen in prikazov po desetletjih v `analiza.ipynb`.