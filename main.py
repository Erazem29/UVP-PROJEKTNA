import argparse
from zajem import prenesi_strani
from izluscenje import izlusci_podatke_iz_html
from naredi_csv import shrani_v_csv

def glavna_funkcija():
    # Nastavimo branje argumentov iz terminala
    parser = argparse.ArgumentParser(
        description="Celoten cevovod za zajem, obdelavo in shranjevanje podatkov o albumih."
    )
    parser.add_argument(
        "-s", "--skip-download", 
        action="store_true", 
        help="Preskoči prenos HTML datotek s spleta (uporabi že shranjene datoteke)."
    )
    parser.add_argument(
        "-p", "--pages", 
        type=int, 
        default=20, 
        help="Število strani za zajem (privzeto: 20 strani)."
    )

    args = parser.parse_args()

    print("=== ZAČETEK PROCESA ===")

    # 1. Korak: Prenos HTML-jev (če ni vklopljeno preskakovanje)
    if args.skip_download:
        print("\n[1/3] Preskakujem prenos HTML datotek (--skip-download vklopljen).")
    else:
        print(f"\n[1/3] Začenjam prenos {args.pages} HTML strani...")
        prenesi_strani(st_strani=args.pages)

    # 2. Korak: Parsanje podatkov iz lokanih HTML-jev
    print("\n[2/3] Začenjam izluščenje podatkov iz HTML datotek...")
    albumi = izlusci_podatke_iz_html()

    # 3. Korak: Zapis v CSV
    print("\n[3/3] Začenjam shranjevanje v CSV datoteko...")
    shrani_v_csv(albumi)

    print("\n=== PROCES USPEŠNO ZAKLJUČEN ===")

if __name__ == "__main__":
    glavna_funkcija()