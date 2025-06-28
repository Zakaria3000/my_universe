#!/usr/bin/env python3
"""
Système complet de scraping de terrains et API FastAPI
Combine le scraping de Mubawab avec une API REST pour exposer les données
"""

import asyncio
import json
import os
import time
import schedule
from datetime import datetime
from typing import Optional
import subprocess
import sys

# Import des modules de scraping
from mubawab_scraper_improved import MubawabScraperImproved

class TerrainScrapingSystem:
    def __init__(self):
        self.scraper = MubawabScraperImproved()
        self.data_file = 'terrains_mubawab_improved.json'
        self.log_file = 'scraping_log.txt'
        self.api_process = None
        
    def log_message(self, message: str):
        """Enregistre un message dans le fichier de log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        print(log_entry.strip())
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def scrape_and_save_data(self, max_pages: int = 5):
        """Effectue le scraping et sauvegarde les données"""
        try:
            self.log_message("Début du scraping des terrains...")
            
            # Scraping des données
            terrains = self.scraper.scrape_terrains(max_pages=max_pages)
            
            if terrains:
                # Sauvegarde en JSON
                self.scraper.save_to_json(terrains, self.data_file)
                
                # Sauvegarde en CSV
                csv_file = self.data_file.replace('.json', '.csv')
                self.scraper.save_to_csv(terrains, csv_file)
                
                self.log_message(f"Scraping terminé: {len(terrains)} terrains récupérés")
                self.log_message(f"Données sauvegardées dans {self.data_file} et {csv_file}")
                
                return True
            else:
                self.log_message("Aucun terrain récupéré lors du scraping")
                return False
                
        except Exception as e:
            self.log_message(f"Erreur lors du scraping: {e}")
            return False
    
    def start_api_server(self):
        """Démarre le serveur API FastAPI"""
        try:
            if self.api_process and self.api_process.poll() is None:
                self.log_message("Le serveur API est déjà en cours d'exécution")
                return True
            
            self.log_message("Démarrage du serveur API...")
            
            # Lancer l'API en arrière-plan
            self.api_process = subprocess.Popen([
                sys.executable, 'terrain_api.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Attendre un peu pour que l'API se lance
            time.sleep(3)
            
            if self.api_process.poll() is None:
                self.log_message("Serveur API démarré avec succès sur http://localhost:8000")
                return True
            else:
                self.log_message("Erreur lors du démarrage du serveur API")
                return False
                
        except Exception as e:
            self.log_message(f"Erreur lors du démarrage de l'API: {e}")
            return False
    
    def stop_api_server(self):
        """Arrête le serveur API"""
        try:
            if self.api_process and self.api_process.poll() is None:
                self.api_process.terminate()
                self.api_process.wait(timeout=10)
                self.log_message("Serveur API arrêté")
            else:
                self.log_message("Aucun serveur API en cours d'exécution")
        except Exception as e:
            self.log_message(f"Erreur lors de l'arrêt de l'API: {e}")
    
    def refresh_api_data(self):
        """Actualise les données de l'API"""
        try:
            import requests
            response = requests.post('http://localhost:8000/terrains/refresh')
            if response.status_code == 200:
                self.log_message("Données de l'API actualisées")
                return True
            else:
                self.log_message(f"Erreur lors de l'actualisation: {response.status_code}")
                return False
        except Exception as e:
            self.log_message(f"Erreur lors de l'actualisation de l'API: {e}")
            return False
    
    def scheduled_scraping(self):
        """Tâche de scraping programmée"""
        self.log_message("Exécution du scraping programmé...")
        
        if self.scrape_and_save_data():
            # Actualiser les données de l'API si elle est en cours d'exécution
            if self.api_process and self.api_process.poll() is None:
                self.refresh_api_data()
    
    def run_full_system(self, enable_scheduling: bool = False):
        """Lance le système complet"""
        self.log_message("=== Démarrage du système de scraping de terrains ===")
        
        # Scraping initial
        self.log_message("Scraping initial...")
        self.scrape_and_save_data()
        
        # Démarrage de l'API
        self.start_api_server()
        
        if enable_scheduling:
            # Programmer le scraping automatique
            schedule.every(6).hours.do(self.scheduled_scraping)
            self.log_message("Scraping automatique programmé toutes les 6 heures")
            
            try:
                while True:
                    schedule.run_pending()
                    time.sleep(60)  # Vérifier toutes les minutes
            except KeyboardInterrupt:
                self.log_message("Arrêt du système demandé par l'utilisateur")
                self.stop_api_server()
        else:
            self.log_message("Système démarré. API disponible sur http://localhost:8000")
            self.log_message("Appuyez sur Ctrl+C pour arrêter")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.log_message("Arrêt du système demandé par l'utilisateur")
                self.stop_api_server()
    
    def get_system_status(self):
        """Retourne le statut du système"""
        status = {
            "data_file_exists": os.path.exists(self.data_file),
            "api_running": self.api_process and self.api_process.poll() is None,
            "last_scraping": None,
            "total_terrains": 0
        }
        
        # Vérifier les données
        if status["data_file_exists"]:
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    status["total_terrains"] = len(data)
                
                # Date de modification du fichier
                mod_time = os.path.getmtime(self.data_file)
                status["last_scraping"] = datetime.fromtimestamp(mod_time).isoformat()
            except Exception as e:
                self.log_message(f"Erreur lors de la lecture des données: {e}")
        
        return status

def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Système de scraping de terrains")
    parser.add_argument('--scrape-only', action='store_true', 
                       help='Effectuer seulement le scraping sans lancer l\'API')
    parser.add_argument('--api-only', action='store_true', 
                       help='Lancer seulement l\'API sans scraping')
    parser.add_argument('--schedule', action='store_true', 
                       help='Activer le scraping automatique programmé')
    parser.add_argument('--pages', type=int, default=5, 
                       help='Nombre de pages à scraper (défaut: 5)')
    parser.add_argument('--status', action='store_true', 
                       help='Afficher le statut du système')
    
    args = parser.parse_args()
    
    system = TerrainScrapingSystem()
    
    if args.status:
        status = system.get_system_status()
        print("=== Statut du système ===")
        print(f"Fichier de données: {'✓' if status['data_file_exists'] else '✗'}")
        print(f"API en cours: {'✓' if status['api_running'] else '✗'}")
        print(f"Total terrains: {status['total_terrains']}")
        print(f"Dernier scraping: {status['last_scraping'] or 'Jamais'}")
        return
    
    if args.scrape_only:
        system.scrape_and_save_data(max_pages=args.pages)
    elif args.api_only:
        system.start_api_server()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            system.stop_api_server()
    else:
        system.run_full_system(enable_scheduling=args.schedule)

if __name__ == "__main__":
    main()

