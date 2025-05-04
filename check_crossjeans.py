import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 5 stron do monitorowania
URLS = {
    'Nowości': 'https://crossjeans.pl/lp-nowosci',
    'Jeansy damskie': 'https://crossjeans.pl/ona/jeansy-damskie',
    'Spodnie damskie': 'https://crossjeans.pl/ona/spodnie-damskie',
    'Odzież damska': 'https://crossjeans.pl/ona/odziez-damska',
    'Buty damskie': 'https://crossjeans.pl/ona/buty-damskie',
    'Akcesoria damskie': 'https://crossjeans.pl/ona/akcesoria-damskie',
    'Basic damski': 'https://crossjeans.pl/ona/basic-damski',
    'Komplety damskie': 'https://crossjeans.pl/ona/komplety-damskie',
    'Odzież męska': 'https://crossjeans.pl/on/odziez-meska',
    'Jeansy męskie': 'https://crossjeans.pl/on/jeansy-meskie',
    'Spodnie męskie': 'https://crossjeans.pl/on/spodnie-meskie',
    'Buty męskie': 'https://crossjeans.pl/on/buty-meskie',
    'Akcesoria męskie': 'https://crossjeans.pl/on/akcesoria-meskie',
    'Basic męski': 'https://crossjeans.pl/on/basic-meski',
}

HEADERS = {'User-Agent': 'Mozilla/5.0'}
DATA_FILE = 'last_seen.txt'       # produkty, które już widzieliśmy
OUTPUT_FILE = 'new_products.txt'  # nowości, które zapisujemy

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
