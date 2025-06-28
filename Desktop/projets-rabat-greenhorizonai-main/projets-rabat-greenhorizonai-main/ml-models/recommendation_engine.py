import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os

class RecommendationEngine:
    """
    Moteur de recommandation pour les terrains basé sur le filtrage collaboratif et le contenu
    """
    def _init_(self):
        self.terrain_features = None
        self.scaler = StandardScaler()
    
    def fit(self, terrains_df):
        """
        Prépare le moteur de recommandation avec les données des terrains
        
        Args:
            terrains_df: DataFrame contenant les données de tous les terrains
        """
        # Sélectionner les caractéristiques pertinentes pour la comparaison
        features = [
            'price', 'area', 'latitude', 'longitude', 
            'has_water', 'has_electricity', 'has_gas'
        ]
        
        # Créer des caractéristiques pour zone_type (one-hot encoding)
        zone_dummies = pd.get_dummies(terrains_df['zone_type'], prefix='zone')
        
        # Combiner les caractéristiques numériques et catégorielles
        self.terrain_features = pd.concat([terrains_df[features], zone_dummies], axis=1)
        
        # Normaliser les caractéristiques pour la similarité
        self.terrain_features_scaled = self.scaler.fit_transform(self.terrain_features)
        
        # Stocker les IDs des terrains pour référence
        self.terrain_ids = terrains_df['id'].values
        
        return self
    
    def get_similar_terrains(self, terrain_id, n=5):
        """
        Trouve des terrains similaires à un terrain spécifié
        
        Args:
            terrain_id: ID du terrain de référence
            n: Nombre de recommandations à retourner
            
        Returns:
            Liste des IDs des terrains similaires
        """
        # Trouver l'index du terrain dans notre dataset
        terrain_idx = np.where(self.terrain_ids == terrain_id)[0][0]
        
        # Calculer la similarité avec tous les autres terrains
        terrain_vector = self.terrain_features_scaled[terrain_idx].reshape(1, -1)
        similarities = cosine_similarity(terrain_vector, self.terrain_features_scaled)[0]
        
        # Trier par similarité et prendre les n plus similaires (en excluant le terrain lui-même)
        similar_indices = similarities.argsort()[::-1][1:n+1]
        
        # Retourner les IDs des terrains similaires
        return [self.terrain_ids[idx] for idx in similar_indices]
    
    def recommend_for_user(self, user_preferences, n=5):
        """
        Recommande des terrains basés sur les préférences utilisateur
        
        Args:
            user_preferences: Dictionnaire des préférences utilisateur
            n: Nombre de recommandations à retourner
            
        Returns:
            Liste des IDs des terrains recommandés
        """
        # Créer un vecteur de préférences utilisateur
        user_vector = np.zeros(self.terrain_features.shape[1])
        
        # Remplir le vecteur avec les préférences de l'utilisateur
        for i, feature in enumerate(self.terrain_features.columns):
            if feature == 'price' and 'max_price' in user_preferences:
                # Pour le prix, nous voulons des terrains moins chers
                user_vector[i] = user_preferences.get('max_price', 0) * 0.8
            elif feature == 'area' and 'min_area' in user_preferences:
                # Pour la surface, nous voulons des terrains plus grands
                user_vector[i] = user_preferences.get('min_area', 0) * 1.2
            elif feature.startswith('zone_') and 'preferred_zone' in user_preferences:
                # Pour la zone, nous mettons 1 pour la zone préférée
                zone_prefix = 'zone_' + user_preferences['preferred_zone']
                if feature == zone_prefix:
                    user_vector[i] = 1
            elif feature in user_preferences:
                user_vector[i] = user_preferences[feature]
        
        # Normaliser le vecteur de préférences
        user_vector_scaled = self.scaler.transform(user_vector.reshape(1, -1))
        
        # Calculer la similarité avec tous les terrains
        similarities = cosine_similarity(user_vector_scaled, self.terrain_features_scaled)[0]
        
        # Trier par similarité et prendre les n plus similaires
        similar_indices = similarities.argsort()[::-1][:n]
        
        # Retourner les IDs des terrains recommandés
        return [self.terrain_ids[idx] for idx in similar_indices]
    
    def save(self, filepath):
        """Sauvegarde le moteur de recommandation"""
        joblib.dump(self, filepath)
    
    @classmethod
    def load(cls, filepath):
        """Charge un moteur de recommandation sauvegardé"""
        return joblib.load(filepath)

def generate_sample_data(n=1000):
    """Génère des données d'exemple pour tester le moteur de recommandation"""
    np.random.seed(42)
    
    data = {
        'id': range(1, n+1),
        'price': np.random.uniform(50000, 1000000, size=n),
        'area': np.random.uniform(500, 10000, size=n),
        'latitude': np.random.uniform(43.0, 49.0, size=n),  # France
        'longitude': np.random.uniform(-1.0, 7.0, size=n),  # France
        'zone_type': np.random.choice(['residential', 'commercial', 'agricultural', 'industrial'], size=n),
        'has_water': np.random.choice([0, 1], size=n),
        'has_electricity': np.random.choice([0, 1], size=n),
        'has_gas': np.random.choice([0, 1], size=n),
    }
    
    return pd.DataFrame(data)

if _name_ == "_main_":
    # Générer des données d'exemple
    print("Génération de données d'exemple...")
    terrains_df = generate_sample_data(1000)
    
    # Créer et entraîner le moteur de recommandation
    print("Entraînement du moteur de recommandation...")
    engine = RecommendationEngine().fit(terrains_df)
    
    # Test des recommandations similaires
    test_terrain_id = 42
    similar_terrains = engine.get_similar_terrains(test_terrain_id, n=5)
    print(f"\nTerrains similaires au terrain #{test_terrain_id}:")
    print(similar_terrains)
    
    # Test des recommandations basées sur les préférences utilisateur
    user_preferences = {
        'max_price': 300000,
        'min_area': 2000,
        'preferred_zone': 'residential',
        'has_water': 1,
        'has_electricity': 1
    }
    
    recommended_terrains = engine.recommend_for_user(user_preferences, n=5)
    print(f"\nTerrains recommandés basés sur les préférences utilisateur:")
    print(recommended_terrains)
    
    # Sauvegarder le moteur de recommandation
    os.makedirs('models', exist_ok=True)
    engine.save('models/recommendation_engine.pkl')
    print("\nMoteur de recommandation sauvegardé dans models/recommendation_engine.pkl")