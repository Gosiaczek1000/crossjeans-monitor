def read_links(file_path):
    try:
        with open(file_path, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        print(f"Plik {file_path} nie istnieje.")
        return set()

def main():
    yesterday = "2025-05-06.txt"
    today = "2025-05-07.txt"

    old_links = read_links(yesterday)
    new_links = read_links(today)

    added_today = new_links - old_links

    if added_today:
        print("Nowe linki dodane dzisiaj:")
        for link in sorted(added_today):
            print(link)
    else:
        print("Brak nowych linków.")

if __name__ == "__main__":
    main()
