from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
import os
from pydantic import BaseModel
import re
from datetime import datetime

# Modèles Pydantic
class Terrain(BaseModel):
    prix: Optional[str] = None
    surface: Optional[str] = None
    description: Optional[str] = None
    localisation: Optional[str] = None
    type: Optional[str] = None
    statut: Optional[str] = None

class TerrainResponse(BaseModel):
    total: int
    terrains: List[Terrain]

class StatsResponse(BaseModel):
    total_terrains: int
    localisations: dict
    types: dict
    prix_moyen: Optional[float] = None
    surface_moyenne: Optional[float] = None

# Initialisation de l'API
app = FastAPI(
    title="API Terrains Maroc",
    description="API pour récupérer les données de terrains à vendre au Maroc",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales pour stocker les données
terrains_data = []

def load_terrain_data():
    """Charge les données de terrains depuis le fichier JSON"""
    global terrains_data
    
    json_files = [
        'terrains_mubawab_improved.json',
        'terrains_mubawab.json'
    ]
    
    for json_file in json_files:
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    terrains_data = json.load(f)
                print(f"Données chargées depuis {json_file}: {len(terrains_data)} terrains")
                return
            except Exception as e:
                print(f"Erreur lors du chargement de {json_file}: {e}")
    
    print("Aucun fichier de données trouvé")

def extract_numeric_value(value_str: str) -> Optional[float]:
    """Extrait la valeur numérique d'une chaîne"""
    if not value_str:
        return None
    
    # Supprimer les espaces et extraire les chiffres
    numbers = re.findall(r'\d+', value_str.replace(' ', ''))
    if numbers:
        return float(''.join(numbers))
    return None

def filter_terrains(
    terrains: List[dict],
    localisation: Optional[str] = None,
    prix_min: Optional[float] = None,
    prix_max: Optional[float] = None,
    surface_min: Optional[float] = None,
    surface_max: Optional[float] = None,
    type_terrain: Optional[str] = None,
    statut: Optional[str] = None
) -> List[dict]:
    """Filtre les terrains selon les critères donnés"""
    
    filtered = []
    
    for terrain in terrains:
        # Filtre par localisation
        if localisation and terrain.get('localisation'):
            if localisation.lower() not in terrain['localisation'].lower():
                continue
        
        # Filtre par prix
        if prix_min or prix_max:
            prix_numeric = extract_numeric_value(terrain.get('prix', ''))
            if prix_numeric:
                if prix_min and prix_numeric < prix_min:
                    continue
                if prix_max and prix_numeric > prix_max:
                    continue
        
        # Filtre par surface
        if surface_min or surface_max:
            surface_numeric = extract_numeric_value(terrain.get('surface', ''))
            if surface_numeric:
                if surface_min and surface_numeric < surface_min:
                    continue
                if surface_max and surface_numeric > surface_max:
                    continue
        
        # Filtre par type
        if type_terrain and terrain.get('type'):
            if type_terrain.lower() not in terrain['type'].lower():
                continue
        
        # Filtre par statut
        if statut and terrain.get('statut'):
            if statut.lower() not in terrain['statut'].lower():
                continue
        
        filtered.append(terrain)
    
    return filtered

# Charger les données au démarrage
load_terrain_data()

@app.get("/", summary="Page d'accueil")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "API Terrains Maroc",
        "version": "1.0.0",
        "description": "API pour récupérer les données de terrains à vendre au Maroc",
        "endpoints": {
            "/terrains": "Récupérer tous les terrains",
            "/terrains/search": "Rechercher des terrains avec filtres",
            "/terrains/stats": "Statistiques sur les terrains",
            "/terrains/localisations": "Liste des localisations disponibles",
            "/docs": "Documentation interactive"
        },
        "total_terrains": len(terrains_data)
    }

@app.get("/terrains", response_model=TerrainResponse, summary="Récupérer tous les terrains")
async def get_all_terrains(
    limit: int = Query(50, ge=1, le=1000, description="Nombre maximum de terrains à retourner"),
    offset: int = Query(0, ge=0, description="Nombre de terrains à ignorer")
):
    """Récupère tous les terrains avec pagination"""
    
    if not terrains_data:
        raise HTTPException(status_code=404, detail="Aucune donnée de terrain disponible")
    
    total = len(terrains_data)
    terrains_slice = terrains_data[offset:offset + limit]
    
    return TerrainResponse(
        total=total,
        terrains=[Terrain(**terrain) for terrain in terrains_slice]
    )

@app.get("/terrains/search", response_model=TerrainResponse, summary="Rechercher des terrains")
async def search_terrains(
    localisation: Optional[str] = Query(None, description="Filtrer par localisation"),
    prix_min: Optional[float] = Query(None, description="Prix minimum en DH"),
    prix_max: Optional[float] = Query(None, description="Prix maximum en DH"),
    surface_min: Optional[float] = Query(None, description="Surface minimum en m²"),
    surface_max: Optional[float] = Query(None, description="Surface maximum en m²"),
    type_terrain: Optional[str] = Query(None, description="Type de terrain"),
    statut: Optional[str] = Query(None, description="Statut du terrain"),
    limit: int = Query(50, ge=1, le=1000, description="Nombre maximum de terrains à retourner"),
    offset: int = Query(0, ge=0, description="Nombre de terrains à ignorer")
):
    """Recherche des terrains selon différents critères"""
    
    if not terrains_data:
        raise HTTPException(status_code=404, detail="Aucune donnée de terrain disponible")
    
    # Appliquer les filtres
    filtered_terrains = filter_terrains(
        terrains_data,
        localisation=localisation,
        prix_min=prix_min,
        prix_max=prix_max,
        surface_min=surface_min,
        surface_max=surface_max,
        type_terrain=type_terrain,
        statut=statut
    )
    
    total = len(filtered_terrains)
    terrains_slice = filtered_terrains[offset:offset + limit]
    
    return TerrainResponse(
        total=total,
        terrains=[Terrain(**terrain) for terrain in terrains_slice]
    )

@app.get("/terrains/stats", response_model=StatsResponse, summary="Statistiques des terrains")
async def get_terrain_stats():
    """Récupère les statistiques sur les terrains"""
    
    if not terrains_data:
        raise HTTPException(status_code=404, detail="Aucune donnée de terrain disponible")
    
    # Compter les localisations
    localisations = {}
    types = {}
    prix_values = []
    surface_values = []
    
    for terrain in terrains_data:
        # Localisations
        if terrain.get('localisation'):
            loc = terrain['localisation']
            localisations[loc] = localisations.get(loc, 0) + 1
        
        # Types
        if terrain.get('type'):
            type_t = terrain['type']
            types[type_t] = types.get(type_t, 0) + 1
        
        # Prix pour calcul de moyenne
        prix_numeric = extract_numeric_value(terrain.get('prix', ''))
        if prix_numeric:
            prix_values.append(prix_numeric)
        
        # Surface pour calcul de moyenne
        surface_numeric = extract_numeric_value(terrain.get('surface', ''))
        if surface_numeric:
            surface_values.append(surface_numeric)
    
    # Calcul des moyennes
    prix_moyen = sum(prix_values) / len(prix_values) if prix_values else None
    surface_moyenne = sum(surface_values) / len(surface_values) if surface_values else None
    
    return StatsResponse(
        total_terrains=len(terrains_data),
        localisations=localisations,
        types=types,
        prix_moyen=prix_moyen,
        surface_moyenne=surface_moyenne
    )

@app.get("/terrains/localisations", summary="Liste des localisations")
async def get_localisations():
    """Récupère la liste de toutes les localisations disponibles"""
    
    if not terrains_data:
        raise HTTPException(status_code=404, detail="Aucune donnée de terrain disponible")
    
    localisations = set()
    for terrain in terrains_data:
        if terrain.get('localisation'):
            localisations.add(terrain['localisation'])
    
    return {
        "localisations": sorted(list(localisations)),
        "total": len(localisations)
    }

@app.post("/terrains/refresh", summary="Actualiser les données")
async def refresh_data():
    """Recharge les données de terrains depuis les fichiers"""
    
    load_terrain_data()
    
    return {
        "message": "Données actualisées",
        "total_terrains": len(terrains_data),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

