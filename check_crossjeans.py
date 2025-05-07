import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Lista podstron z pełnymi limitami i paginacją
URLS = {
    'Jeansy damskie': 'https://crossjeans.pl/ona/jeansy-damskie?limit=0',
    'Spodnie damskie': 'https://crossjeans.pl/ona/spodnie-damskie?limit=0',
    'Odzież damska': 'https://crossjeans.pl/ona/odziez-damska?limit=0',
    'Buty damskie': 'https://crossjeans.pl/ona/buty-damskie?limit=0',
    'Akcesoria damskie': 'https://crossjeans.pl/ona/akcesoria-damskie?limit=0',
    'Basic damski': 'https://crossjeans.pl/ona/basic-damski?limit=0',
    'Komplety damskie': 'https://crossjeans.pl/ona/komplety-damskie?limit=0',
    'Jeansy męskie': 'https://crossjeans.pl/on/jeansy-meskie?limit=0',
    'Spodnie męskie': 'https://crossjeans.pl/on/spodnie-meskie?limit=0',
    'Buty męskie': 'https://crossjeans.pl/on/buty-meskie?limit=0',
    'Akcesoria męskie': 'https://crossjeans.pl/on/akcesoria-meskie?limit=0',
    'Basic męski': 'https://crossjeans.pl/on/basic-meski?limit=0',
    'Nowości damskie': 'https://crossjeans.pl/lp-nowosci-damskie?limit=0',
    'Nowości męskie': 'https://crossjeans.pl/lp-nowosci-meskie?limit=0',
    'Odzież męska str. 1': 'https://crossjeans.pl/on/odziez-meska?limit=100',
    'Odzież męska str. 2': 'https://crossjeans.pl/on/odziez-meska?limit=100&page=2',
    'Odzież męska str. 3': 'https://crossjeans.pl/on/odziez-meska?limit=100&page=3',
    'Odzież męska str. 4': 'https://crossjeans.pl/on/odziez-meska?limit=100&page=4',
    'Odzież męska str. 5': 'https://crossjeans.pl/on/odziez-meska?limit=100&page=5',
}

HEADERS = {'User-Agent': 'Mozilla/5.0'}
from datetime import datetime

# Format nazw plików wg daty
dzis = datetime.today().strftime("%Y-%m-%d")
DATA_FILE = f"produkty_{dzis}.txt"         # Zawiera wszystkie linki z danego dnia

def get_products(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    product_links = [
        link['href'] for link in links
        if ('/ona/' in link['href'] or '/on/' in link['href']) and '/produkty/' not in link['href']
    ]
    return list(set(product_links))

def load_last_seen():
    try:
        with open(DATA_FILE, 'r') as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

def save_last_seen(products):
    with open(DATA_FILE, 'w') as f:
        f.write('\n'.join(products))

def log_new_products(new_links):
    with open(OUTPUT_FILE, 'a') as f:
        f.write(f"\n=== {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")
        for link in new_links:
            full_link = link if link.startswith('http') else "https://crossjeans.pl" + link
            f.write(full_link + '\n')

def notify(new_links):
    print("NOWE PRODUKTY ZNALEZIONE:")
    for link in new_links:
        full_link = link if link.startswith('http') else "https://crossjeans.pl" + link
        print(full_link)

def main():
    current_products = set()
    for name, url in URLS.items():
        print(f"Sprawdzam: {name}")
        current_products.update(get_products(url))

    last_seen = load_last_seen()
    new = current_products - last_seen

    if new:
        notify(new)
        log_new_products(new)
        save_last_seen(current_products)
    else:
        print("Brak nowych produktów.")

if __name__ == '__main__':
    main()
