# 🎮 PS4 Cover Scraper

A Python tool to search and download PS4 game cover art from the PlayStation Store. Search for a single game or bulk download covers for an entire library — all saved locally and ready to use.

---

## ✨ Features

- 🔍 Search the PlayStation Store by game name
- 📦 Batch download covers for multiple games at once
- 💾 Saves covers as `.jpg` files with clean, sanitized filenames
- 🌍 Region support — search any PSN regional store (US, GB, JP, etc.)
- 🎯 Optional [IGDB](https://api-docs.igdb.com/) integration for higher-quality cover art

---

## 📋 Requirements

- Python 3.6+
- `requests`

---

## 🚀 Installation

**1. Clone the repository or download code and extract on your pc**

```bash
git clone https://github.com/CyberMask367/PS4-Cover-Scraper.git
cd ps4-cover-scraper
```

**2. Install dependencies**

```bash
pip install requests
```

---

## 🖥️ Usage

```bash
python ps4_cover_scraper.py
```

You'll be greeted with an interactive menu:

```
PS4 Cover Scraper
==================================================

Options:
1. Search for a game
2. Search multiple games
3. Exit
```

### Option 1 — Single search

Enter any game name and the scraper will find and download all matching covers from the PlayStation Store (up to 100 results).

```
Choice (1-3): 1
Enter game name: God of War

🎮 Searching for: God of War
==================================================
📡 Searching PlayStation Store...
Found 4 results:

1. God of War
   Platform: ['PS4']
   Image: https://...
   ✓ Downloaded: covers/God of War.jpg
```

### Option 2 — Batch search

Enter multiple game names, one per line. Leave a blank line when finished and the scraper will process each one in sequence.

```
Choice (1-3): 2

Enter game names (one per line, empty line to finish):
God of War
The Last of Us
Spider-Man

🎮 Searching for: God of War
...
🎮 Searching for: The Last of Us
...
```

---

## 📁 Output

All covers are saved to a `covers/` folder in the current directory:

```
covers/
  God of War.jpg
  The Last of Us Part I.jpg
  Marvels Spider-Man.jpg
```

Filenames are automatically sanitized — only letters, numbers, spaces, hyphens, and underscores are kept.

---

## 🔧 IGDB Integration (Optional)

For higher-quality cover art, the scraper supports the [IGDB API](https://api-docs.igdb.com/). This is not connected to the interactive menu but can be used directly in your own scripts:

```python
from ps4_cover_scraper import PS4CoverScraper

scraper = PS4CoverScraper()
results = scraper.search_igdb("God of War", api_key="YOUR_CLIENT_ID:YOUR_ACCESS_TOKEN")

for game in results:
    print(game['name'], game['cover_url'])
```

Get a free API key at: https://api-docs.igdb.com/

---

## 🛠️ API Reference

| Method | Description |
|---|---|
| `search_playstation_store(game_name, country, limit)` | Searches PSN and returns matching games with image URLs. Default country: `US`, limit: `100`. |
| `get_cover_from_psn_api(game_id)` | Fetches all available image types for a specific PSN game ID. |
| `search_igdb(game_name, api_key)` | Searches IGDB for PS4 game covers. Requires a Twitch/IGDB API key. |
| `download_cover(image_url, output_path)` | Downloads a single image from a URL to disk. |
| `scrape_game_covers(game_name, output_dir, download)` | Main method — searches PSN and optionally downloads all matching covers. |

---

## ‼️ Issues (hoping to fix soon)

- Searches pulls from all platfroms so PS3, PSP, PSVita games might show up in the results
- Searche results might also include image of dlcs or addons
- The scraper always display upto 20 listings even tho i set the limit to 100, maybe its a limit with the api
---

## ⚠️ Disclaimer

This tool uses an unofficial, legacy PlayStation Store API endpoint (`chihiro`). It is not affiliated with or endorsed by Sony Interactive Entertainment. The endpoint may change or become unavailable at any time. Use responsibly and respect PlayStation's servers.

AI was used in development of this script.

---

## 🤝 Contributing

Pull requests are welcome! If you find a bug or want to add a feature, feel free to open an issue or submit a PR.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request
