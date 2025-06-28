import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

# Chemin pour sauvegarder le modèle
MODEL_PATH = 'models/value_prediction_model.pkl'

def prepare_data():
    """
    Prépare les données pour l'entraînement du modèle de prédiction de valeur
    """
    # Simulation de données (à remplacer par de vraies données)
    data = {
        'price': np.random.uniform(50000, 1000000, size=2000),
        'area': np.random.uniform(500, 10000, size=2000),
        'city': np.random.choice(['Paris', 'Lyon', 'Marseille', 'Bordeaux', 'Toulouse', 'Nantes'], size=2000),
        'zone_type': np.random.choice(['residential', 'commercial', 'agricultural', 'industrial', 'mixed'], size=2000),
        'distance_to_city_center': np.random.uniform(1, 30, size=2000),
        'has_water': np.random.choice([0, 1], size=2000),
        'has_electricity': np.random.choice([0, 1], size=2000),
        'soil_quality': np.random.choice(['low', 'medium', 'high'], size=2000),
        'urban_density': np.random.uniform(0, 1, size=2000),
        'economic_growth_rate': np.random.uniform(0.01, 0.05, size=2000),
        # Simulation de la variation annuelle de prix pour créer des données d'historique
        'price_evolution_1y': np.random.uniform(0.01, 0.08, size=2000),  # 1 à 8% par an
    }
    
    df = pd.DataFrame(data)
    
    # Créer une colonne cible: prix dans 5 ans
    compound_growth = np.power(1 + df['price_evolution_1y'], 5)
    df['future_price_5y'] = df['price'] * compound_growth
    
    return df

def train_model(df):
    """
    Entraîne un modèle de prédiction de valeur de terrain
    """
    # Définir les features et la cible
    X = df.drop(['future_price_5y', 'price_evolution_1y'], axis=1)
    y = df['future_price_5y']
    
    # Diviser en train et test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Définir les transformations pour les colonnes
    numeric_features = ['price', 'area', 'distance_to_city_center', 'urban_density', 'economic_growth_rate']
    categorical_features = ['city', 'zone_type', 'soil_quality']
    binary_features = ['has_water', 'has_electricity']
    
    # Créer le préprocesseur
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ],
        remainder='passthrough'
    )
    
    # Créer le pipeline avec le préprocesseur et le modèle
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    # Entraîner le modèle
    pipeline.fit(X_train, y_train)
    
    # Évaluer le modèle
    y_pred = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"Évaluation du modèle:")
    print(f"MAE: {mae:.2f} €")
    print(f"RMSE: {rmse:.2f} €")
    print(f"R²: {r2:.4f}")
    
    # Créer le répertoire pour sauvegarder le modèle si nécessaire
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Sauvegarder le modèle
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Modèle sauvegardé à {MODEL_PATH}")
    
    return pipeline

def predict_future_value(model, terrain_data, years_ahead=5):
    """
    Prédit la valeur future d'un terrain
    
    Args:
        model: Le modèle entraîné
        terrain_data: Dictionnaire avec les caractéristiques du terrain
        years_ahead: Nombre d'années dans le futur (par défaut 5)
    
    Returns:
        Valeur prédite et score de confiance
    """
    # Conversion en DataFrame
    terrain_df = pd.DataFrame([terrain_data])
    
    # Prédiction directe pour 5 ans
    if years_ahead == 5:
        predicted_value = model.predict(terrain_df)[0]
        confidence_score = 0.85  # Score de confiance simulé
    else:
        # Pour d'autres horizons, on ajuste en fonction de la croissance annuelle moyenne
        # (Ceci est une approximation simplifiée)
        predicted_5y = model.predict(terrain_df)[0]
        annual_growth_rate = np.power(predicted_5y / terrain_data['price'], 1/5) - 1
        predicted_value = terrain_data['price'] * np.power(1 + annual_growth_rate, years_ahead)
        
        # Le score de confiance diminue pour les prédictions plus lointaines
        confidence_score = 0.85 * np.exp(-0.05 * (years_ahead - 5))
    
    return predicted_value, min(confidence_score, 0.95)

if _name_ == "_main_":
    print("Préparation des données...")
    df = prepare_data()
    
    print("Entraînement du modèle...")
    model = train_model(df)
    
    # Test du modèle sur un exemple
    test_terrain = {
        'price': 250000,
        'area': 1500,
        'city': 'Paris',
        'zone_type': 'residential',
        'distance_to_city_center': 15,
        'has_water': 1,
        'has_electricity': 1,
        'soil_quality': 'medium',
        'urban_density': 0.6,
        'economic_growth_rate': 0.03
    }
    
    predicted_value, confidence = predict_future_value(model, test_terrain, 5)
    print(f"\nTest de prédiction pour un terrain de 1500m² à Paris:")
    print(f"Prix actuel: 250 000 €")
    print(f"Prix prédit dans 5 ans: {predicted_value:.2f} €")
    print(f"Score de confiance: {confidence:.2%}")