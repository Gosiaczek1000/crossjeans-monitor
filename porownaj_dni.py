import os
from datetime import datetime, timedelta

dzis = datetime.today().strftime("%Y-%m-%d")
wczoraj = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

plik_dzis = f"produkty_{dzis}.txt"
plik_wczoraj = f"produkty_{wczoraj}.txt"
plik_nowe = "nowe_produkty.txt"

def wczytaj_linki(nazwa_pliku):
    if not os.path.exists(nazwa_pliku):
        return set()
    with open(nazwa_pliku, "r") as f:
        return set(line.strip() for line in f if line.strip())

linki_dzis = wczytaj_linki(plik_dzis)
linki_wczoraj = wczytaj_linki(plik_wczoraj)

nowe_linki = sorted(linki_dzis - linki_wczoraj)

if nowe_linki:
    with open(plik_nowe, "w") as f:
        f.write("\n".join(nowe_linki))
    print(f"Znaleziono {len(nowe_linki)} nowych linków:")
    for link in nowe_linki:
        print(link)
else:
    print("Brak nowych linków.")
