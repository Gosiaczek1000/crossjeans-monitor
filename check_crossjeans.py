import requests
from bs4 import BeautifulSoup

URLS = {
    'Nowości': 'https://crossjeans.pl/lp-nowosci',
    'Jeansy damskie': 'https://crossjeans.pl/ona/jeansy-damskie',
    'Spodnie damskie': 'https://crossjeans.pl/ona/spodnie-damskie',
    'Odzież damska': 'https://crossjeans.pl/ona/odziez-damska',
    'Odzież męska': 'https://crossjeans.pl/on/odziez-meska',
}

HEADERS = {'User-Agent': 'Mozilla/5.0'}
DATA_FILE = 'last_seen.txt'

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

def notify(new_links):
    print("NOWE PRODUKTY ZNALEZIONE:")
    for link in new_links:
        print("https://crossjeans.pl" + link)

def main():
    current_products = set()
    for name, url in URLS.items():
        print(f"Sprawdzam: {name} ({url})")
        products = get_products(url)
        current_products.update(products)

    last_seen = load_last_seen()
    new = current_products - last_seen

    if new:
        notify(new)
        save_last_seen(current_products)
    else:
        print("Brak nowych produktów.")

if __name__ == '__main__':
    main()
