import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import urljoin, urlparse
import csv
import re

class MubawabScraperImproved:
    def __init__(self):
        self.base_url = "https://www.mubawab.ma"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def get_page(self, url, retries=3):
        """Récupère une page avec gestion des erreurs et retry"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                print(f"Erreur lors de la récupération de {url}: {e}")
                if attempt < retries - 1:
                    time.sleep(random.uniform(1, 3))
                else:
                    return None
    
    def extract_price_and_surface_from_text(self, text):
        """Extrait le prix et la surface depuis le texte de la page"""
        price_pattern = r'(\d{1,3}(?:\s?\d{3})*)\s*DH'
        surface_pattern = r'(\d+)\s*m²'
        
        price_match = re.search(price_pattern, text)
        surface_match = re.search(surface_pattern, text)
        
        price = price_match.group(1).replace(' ', '') + ' DH' if price_match else None
        surface = surface_match.group(1) + ' m²' if surface_match else None
        
        return price, surface
    
    def extract_terrain_data_from_markdown(self, content):
        """Extrait les données depuis le contenu markdown de la page"""
        terrains = []
        
        # Diviser le contenu en sections basées sur les prix
        sections = re.split(r'(\d{1,3}(?:\s?\d{3})*\s*DH)', content)
        
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                try:
                    terrain_data = {}
                    
                    # Prix
                    price_text = sections[i].strip()
                    terrain_data['prix'] = price_text
                    
                    # Contenu de la section
                    section_content = sections[i + 1]
                    
                    # Surface
                    surface_match = re.search(r'(\d+)\s*m²', section_content)
                    if surface_match:
                        terrain_data['surface'] = surface_match.group(1) + ' m²'
                    
                    # Description (première ligne significative)
                    lines = section_content.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if len(line) > 20 and not re.match(r'^\d+\s*m²', line):
                            terrain_data['description'] = line[:200] + '...' if len(line) > 200 else line
                            break
                    
                    # Localisation (recherche de noms de villes)
                    location_patterns = [
                        r'(Casablanca|Rabat|Marrakech|Fès|Tanger|Agadir|Meknès|Oujda|Kenitra|Tétouan|Safi|Mohammedia|Khouribga|Beni Mellal|El Jadida|Nador|Taza|Settat|Larache|Ksar el Kebir|Sale|Berrechid|Khemisset|Ouarzazate|Tiznit|Taroudant|Guelmim|Ouezzane|Fnideq|Sidi Kacem|Sidi Slimane|Youssoufia|Jerada|Taourirt|Midelt|Azrou|Ifrane|Errachidia|Zagora|Laayoune|Dakhla|Smara)',
                        r'(Béni Yakhlef|Settat|Oued Cherrat|Tit Mellil|Mediouna|Jnane Soualem|Nouaceur|Had Soualem|Benslimane|Témara|Skhirat|Harhoura|Ain Tekki|Mejjatia|Ouled Taleb)'
                    ]
                    
                    for pattern in location_patterns:
                        location_match = re.search(pattern, section_content, re.IGNORECASE)
                        if location_match:
                            terrain_data['localisation'] = location_match.group(1)
                            break
                    
                    # Type de terrain
                    if 'lotissement' in section_content.lower():
                        terrain_data['type'] = 'Lotissement'
                    elif 'villa' in section_content.lower():
                        terrain_data['type'] = 'Terrain pour villa'
                    elif 'commercial' in section_content.lower():
                        terrain_data['type'] = 'Terrain commercial'
                    else:
                        terrain_data['type'] = 'Terrain'
                    
                    # Statut (neuf, occasion, etc.)
                    if 'neuf' in section_content.lower() or 'nouveau' in section_content.lower():
                        terrain_data['statut'] = 'Neuf'
                    else:
                        terrain_data['statut'] = 'Occasion'
                    
                    if len(terrain_data) > 1:  # Au moins le prix + une autre info
                        terrains.append(terrain_data)
                        
                except Exception as e:
                    print(f"Erreur lors de l'extraction d'une section: {e}")
                    continue
        
        return terrains
    
    def scrape_terrains(self, max_pages=5):
        """Scrape les terrains depuis Mubawab"""
        all_terrains = []
        
        for page in range(1, max_pages + 1):
            print(f"Scraping page {page}...")
            
            # URL pour la page de terrains
            url = f"{self.base_url}/fr/sc/terrains-a-vendre?page={page}"
            
            response = self.get_page(url)
            if not response:
                print(f"Impossible de récupérer la page {page}")
                continue
            
            # Utiliser BeautifulSoup pour extraire le contenu textuel
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraire tout le texte de la page
            page_text = soup.get_text()
            
            # Extraire les données depuis le texte
            terrains = self.extract_terrain_data_from_markdown(page_text)
            
            if not terrains:
                print(f"Aucun terrain trouvé sur la page {page}")
                # Essayer de continuer quand même
                continue
            
            all_terrains.extend(terrains)
            print(f"Trouvé {len(terrains)} terrains sur la page {page}")
            
            # Pause entre les requêtes
            time.sleep(random.uniform(2, 5))
        
        return all_terrains
    
    def save_to_json(self, data, filename):
        """Sauvegarde les données en JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def save_to_csv(self, data, filename):
        """Sauvegarde les données en CSV"""
        if not data:
            return
        
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(fieldnames))
            writer.writeheader()
            writer.writerows(data)

def main():
    scraper = MubawabScraperImproved()
    
    print("Début du scraping amélioré des terrains sur Mubawab...")
    terrains = scraper.scrape_terrains(max_pages=3)
    
    if terrains:
        print(f"Total de {len(terrains)} terrains récupérés")
        
        # Sauvegarde en JSON
        scraper.save_to_json(terrains, 'terrains_mubawab_improved.json')
        print("Données sauvegardées dans terrains_mubawab_improved.json")
        
        # Sauvegarde en CSV
        scraper.save_to_csv(terrains, 'terrains_mubawab_improved.csv')
        print("Données sauvegardées dans terrains_mubawab_improved.csv")
        
        # Affichage d'un échantillon
        print("\nÉchantillon des données:")
        for i, terrain in enumerate(terrains[:3]):
            print(f"\nTerrain {i+1}:")
            for key, value in terrain.items():
                print(f"  {key}: {value}")
    else:
        print("Aucun terrain récupéré")

if __name__ == "__main__":
    main()

