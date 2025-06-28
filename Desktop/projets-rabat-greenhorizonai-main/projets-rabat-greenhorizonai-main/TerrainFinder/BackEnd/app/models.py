from datetime import datetime, timedelta
from app import db

class Terrain(db.Model):
    __tablename__ = 'terrains'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    superficie_m2 = db.Column(db.Integer, nullable=False)
    prix_m2 = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    ville = db.Column(db.String(100))
    region = db.Column(db.String(100))
    statut_foncier = db.Column(db.String(50))
    proximite_infrastructures = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'superficie_m2': self.superficie_m2,
            'prix_m2': self.prix_m2,
            'prix_total': self.superficie_m2 * self.prix_m2,
            'type': self.type,
            'description': self.description,
            'ville': self.ville,
            'region': self.region,
            'statut_foncier': self.statut_foncier,
            'proximite_infrastructures': self.proximite_infrastructures,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None
        }

class PremiumUser(db.Model):
    __tablename__ = 'premium_users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    plan = db.Column(db.String(50), nullable=False)  # 'premium' ou 'enterprise'
    token = db.Column(db.String(100), unique=True, nullable=False)
    date_souscription = db.Column(db.DateTime, default=datetime.utcnow)
    date_expiration = db.Column(db.DateTime, nullable=False)
    actif = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'plan': self.plan,
            'date_souscription': self.date_souscription.isoformat(),
            'date_expiration': self.date_expiration.isoformat(),
            'actif': self.actif
        }