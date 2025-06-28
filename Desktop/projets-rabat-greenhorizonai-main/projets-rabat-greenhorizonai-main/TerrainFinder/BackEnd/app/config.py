import os
from pathlib import Path

basedir = Path(__file__).parent.parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'terrain_finder_secret_key_2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              f"sqlite:///{os.path.join(basedir, 'database', 'terrains.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'