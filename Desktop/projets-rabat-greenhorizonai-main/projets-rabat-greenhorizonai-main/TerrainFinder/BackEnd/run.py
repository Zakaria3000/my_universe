from app import create_app
from app.models import db, Terrain, PremiumUser
import os

app = create_app()

def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        # Create all database tables
        db.create_all()

        # Add sample terrains if database is empty
        if Terrain.query.count() == 0:

            terrains_exemple = [
                Terrain(
                    nom="Villa Moderne Casablanca Anfa",
                    latitude=33.5731,
                    longitude=-7.5898,
                    superficie_m2=500,
                    prix_m2=8000,
                    type="Résidentiel",
                    description="Terrain exceptionnel dans le quartier prestigieux d'Anfa, idéal pour villa de luxe avec vue mer.",
                    ville="Casablanca",
                    region="Casablanca-Settat",
                    statut_foncier="Titré",
                    proximite_infrastructures="École internationale, Hôpital privé, Centre commercial, Transport public"
                ),
                Terrain(
                    nom="Centre Commercial Rabat Agdal",
                    latitude=34.020882,
                    longitude=-6.84165,
                    superficie_m2=1200,
                    prix_m2=10000,
                    type="Commercial",
                    description="Emplacement stratégique au cœur d'Agdal, parfait pour projet commercial d'envergure.",
                    ville="Rabat",
                    region="Rabat-Salé-Kénitra",
                    statut_foncier="Titré",
                    proximite_infrastructures="Université, Centre commercial, Banques, Restaurants, Métro"
                ),
                Terrain(
                    nom="Exploitation Agricole Fès",
                    latitude=34.0000,
                    longitude=-5.0000,
                    superficie_m2=10000,
                    prix_m2=500,
                    type="Agricole",
                    description="Vaste terrain agricole avec système d'irrigation moderne et accès direct à l'eau.",
                    ville="Fès",
                    region="Fès-Meknès",
                    statut_foncier="Titré",
                    proximite_infrastructures="Source d'eau, Route nationale, Coopérative agricole"
                ),
                Terrain(
                    nom="Résidence Marrakech Gueliz",
                    latitude=31.6295,
                    longitude=-7.9811,
                    superficie_m2=750,
                    prix_m2=7000,
                    type="Résidentiel",
                    description="Terrain ensoleillé dans le quartier moderne de Gueliz, vue panoramique sur l'Atlas.",
                    ville="Marrakech",
                    region="Marrakech-Safi",
                    statut_foncier="Titré",
                    proximite_infrastructures="Golf, Hôtels de luxe, Restaurants, Aéroport"
                ),
                Terrain(
                    nom="Zone Industrielle Tanger Med",
                    latitude=35.7595,
                    longitude=-5.7975,
                    superficie_m2=2000,
                    prix_m2=6000,
                    type="Industriel",
                    description="Terrain industriel stratégique proche du port de Tanger Med, idéal pour export.",
                    ville="Tanger",
                    region="Tanger-Tétouan-Al Hoceima",
                    statut_foncier="Titré",
                    proximite_infrastructures="Port Tanger Med, Autoroute, Zone franche, Douane"
                ),
                Terrain(
                    nom="Resort Agadir Baie",
                    latitude=30.4278,
                    longitude=-9.5981,
                    superficie_m2=600,
                    prix_m2=9000,
                    type="Résidentiel",
                    description="Terrain premium face à l'océan, parfait pour résidence de vacances ou investissement touristique.",
                    ville="Agadir",
                    region="Souss-Massa",
                    statut_foncier="Titré",
                    proximite_infrastructures="Plage, Aéroport international, Hôtels, Marina"
                ),
                Terrain(
                    nom="Business Center Oujda",
                    latitude=34.6814,
                    longitude=-1.9086,
                    superficie_m2=800,
                    prix_m2=5500,
                    type="Commercial",
                    description="Terrain commercial stratégique au centre d'Oujda, parfait pour centre d'affaires moderne.",
                    ville="Oujda",
                    region="Oriental",
                    statut_foncier="Titré",
                    proximite_infrastructures="Gare, Université, Administrations, Centre-ville"
                ),
                Terrain(
                    nom="Agro-Business Béni Mellal",
                    latitude=32.3373,
                    longitude=-6.3498,
                    superficie_m2=15000,
                    prix_m2=400,
                    type="Agricole",
                    description="Grande exploitation moderne avec technologie d'irrigation avancée et certification bio.",
                    ville="Béni Mellal",
                    region="Béni Mellal-Khénifra",
                    statut_foncier="Titré",
                    proximite_infrastructures="Barrage, Coopérative agricole, Route nationale"
                )
            ]

            for terrain in terrains_exemple:
                db.session.add(terrain)

            db.session.commit()
            print("Database initialized successfully!")

if __name__ == '__main__':
    # Create database directory if it doesn't exist
    if not os.path.exists('database'):
        os.makedirs('database')

    init_database()
    app.run(host='0.0.0.0', port=5000, debug=True)