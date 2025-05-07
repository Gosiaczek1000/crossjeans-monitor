import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

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

DATA_DIR = "data"
TODAY_FILE = os.path.join(DATA_DIR, "today.txt")
YESTERDAY_FILE = os.path.join(DATA_DIR, "yesterday.txt")
NEW_FILE = os.path.join(DATA_DIR, "new_products.txt")

def get_products(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.select(".product-item a")
    return set(link["href"] for link in links if link.has_attr("href"))

def save_list(path, data):
    with open(path, "w") as f:
        for item in sorted(data):
            f.write(f"https://crossjeans.pl{item}\n")

def load_list(path):
    try:
        with open(path) as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    all_links = set()

    for name, url in URLS.items():
        print(f"Sprawdzam: {name}")
        all_links.update(get_products(url))

    save_list(TODAY_FILE, all_links)

    old_links = load_list(YESTERDAY_FILE)
    new_links = all_links - old_links

    if new_links:
        print("NOWE PRODUKTY ZNALEZIONE:")
        save_list(NEW_FILE, new_links)
        for link in new_links:
            print(link)

    # dzisiejsze zapisujemy jako wczorajsze (do porównań jutro)
    save_list(YESTERDAY_FILE, all_links)

if __name__ == "__main__":
    main()
