#!/usr/bin/env python3
"""
PS4 Game Cover Scraper
Fetches game cover art from PlayStation Store and other sources
"""

import requests
import json
import os
from urllib.parse import quote
import time

class PS4CoverScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def search_playstation_store(self, game_name, country='US', limit=100):
        """
        Search PlayStation Store for games
        """
        try:
            # PlayStation Store search API
            url = f"https://store.playstation.com/store/api/chihiro/00_09_000/tumbler/{country}/en/999/{quote(game_name)}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            if 'links' in data:
                for item in data['links'][:limit]:
                    if item.get('name'):
                        results.append({
                            'id': item.get('id'),
                            'name': item.get('name'),
                            'platform': item.get('playable_platform', []),
                            'image_url': item.get('images', [{}])[0].get('url') if item.get('images') else None
                        })
            
            return results
        except Exception as e:
            print(f"PlayStation Store search error: {e}")
            return []
    
    def get_cover_from_psn_api(self, game_id):
        """
        Get cover art using PlayStation API
        """
        try:
            # Try to get game details
            url = f"https://store.playstation.com/store/api/chihiro/00_09_000/container/US/en/999/{game_id}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract images
            images = {}
            if 'images' in data:
                for img in data['images']:
                    img_type = img.get('type')
                    img_url = img.get('url')
                    if img_type and img_url:
                        images[img_type] = img_url
            
            return images
        except Exception as e:
            print(f"PSN API error: {e}")
            return {}
    
    def search_igdb(self, game_name, api_key=None):
        """
        Search IGDB for game covers (requires API key)
        Get free API key at: https://api-docs.igdb.com/
        """
        if not api_key:
            print("IGDB requires API key. Get one at: https://api-docs.igdb.com/")
            return []
        
        try:
            headers = {
                'Client-ID': api_key.split(':')[0],
                'Authorization': f'Bearer {api_key.split(":")[1]}',
            }
            
            url = "https://api.igdb.com/v4/games"
            data = f'search "{game_name}"; fields name,cover.url,platforms; where platforms = (48); limit 10;'
            
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            
            games = response.json()
            results = []
            
            for game in games:
                if 'cover' in game:
                    cover_url = game['cover']['url'].replace('t_thumb', 't_cover_big')
                    if not cover_url.startswith('http'):
                        cover_url = 'https:' + cover_url
                    
                    results.append({
                        'name': game['name'],
                        'cover_url': cover_url
                    })
            
            return results
        except Exception as e:
            print(f"IGDB error: {e}")
            return []
    
    def download_cover(self, image_url, output_path):
        """
        Download cover image to file
        """
        try:
            response = self.session.get(image_url, timeout=30)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Downloaded: {output_path}")
            return True
        except Exception as e:
            print(f"✗ Download failed: {e}")
            return False
    
    def scrape_game_covers(self, game_name, output_dir='covers', download=True):
        """
        Main function to search and download game covers
        """
        print(f"\n🎮 Searching for: {game_name}")
        print("=" * 50)
        
        # Create output directory
        if download and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Search PlayStation Store
        print("\n📡 Searching PlayStation Store...")
        ps_results = self.search_playstation_store(game_name, limit=100)
        
        if ps_results:
            print(f"Found {len(ps_results)} results:")
            for i, game in enumerate(ps_results, 1):
                print(f"\n{i}. {game['name']}")
                print(f"   Platform: {game['platform']}")
                if game['image_url']:
                    print(f"   Image: {game['image_url']}")
                    
                    if download:
                        # Clean filename
                        safe_name = "".join(c for c in game['name'] if c.isalnum() or c in (' ', '-', '_')).strip()
                        filename = f"{safe_name}.jpg"
                        filepath = os.path.join(output_dir, filename)
                        
                        self.download_cover(game['image_url'], filepath)
                        time.sleep(0.5)  # Be nice to servers
        else:
            print("No results found in PlayStation Store")
        
        return ps_results


def main():
    """
    Example usage
    """
    scraper = PS4CoverScraper()
    
    # Example searches
    games = [
        "God of War",
        "The Last of Us",
        "Spider-Man"
    ]
    
    print("PS4 Cover Scraper")
    print("=" * 50)
    
    # Interactive mode
    while True:
        print("\nOptions:")
        print("1. Search for a game")
        print("2. Search multiple games")
        print("3. Exit")
        
        choice = input("\nChoice (1-3): ").strip()
        
        if choice == '1':
            game_name = input("Enter game name: ").strip()
            if game_name:
                scraper.scrape_game_covers(game_name)
        
        elif choice == '2':
            print("\nEnter game names (one per line, empty line to finish):")
            games = []
            while True:
                game = input().strip()
                if not game:
                    break
                games.append(game)
            
            for game in games:
                scraper.scrape_game_covers(game)
                time.sleep(1)  # Rate limiting
        
        elif choice == '3':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
