import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Lista podstron do monitorowania
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
    'Odzież męska': 'https://crossjeans.pl/on/odziez-meska?limit=0',
    'Buty męskie': 'https://crossjeans.pl/on/buty-meskie?limit=0',
    'Akcesoria męskie': 'https://crossjeans.pl/on/akcesoria-meskie?limit=0',
    'Basic męski': 'https://crossjeans.pl/on/basic-meski?limit=0',
    'Nowości damskie': 'https://crossjeans.pl/lp-nowosci-damskie?limit=0',
    'Nowości męskie': 'https://crossjeans.pl/lp-nowosci-meskie?limit=0',
}


HEADERS = {'User-Agent': 'Mozilla/5.0'}
DATA_FILE = 'last_seen.txt'        # plik zapamiętujący wcześniej widziane linki
OUTPUT_FILE = 'new_products.txt'   # plik ze znalezionymi nowościami

def get_products(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select('a.product-item')
    return [link.get('href') for link in links if link.get('href')]

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
            f.write("https://crossjeans.pl" + link + '\n')

def notify(new_links):
    print("NOWE PRODUKTY ZNALEZIONE:")
    for link in new_links:
        print("https://crossjeans.pl" + link)

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
