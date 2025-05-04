import requests
from bs4 import BeautifulSoup

URL = 'https://crossjeans.pl/lp-nowosci'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
DATA_FILE = 'last_seen.txt'

def get_products():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.select('a.product-item-link')
    return [p.get('href') for p in products]

def load_last_seen():
    try:
        with open(DATA_FILE, 'r') as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

def save_last_seen(products):
    with open(DATA_FILE, 'w') as f:
        f.write('\n'.join(products))

def notify(new_products):
    print("NOWE PRODUKTY:")
    for link in new_products:
        print("https://www.crossjeans.com" + link)

def main():
    current_products = set(get_products())
    last_seen = load_last_seen()
    new = current_products - last_seen

    if new:
        notify(new)
        save_last_seen(current_products)
    else:
        print("Brak nowych produktów.")

if __name__ == '__main__':
    main()
