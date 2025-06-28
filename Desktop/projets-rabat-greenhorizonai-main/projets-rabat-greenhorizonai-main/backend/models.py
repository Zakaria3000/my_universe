from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text, Date
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from database import Base


class Terrain (Base) :
    __tablename__ = "terrains"

    id = Column (Integer, primary_key=True, index=True)
    title = Column (String, index=True)
    description = Column (Text)
    price = Column (Float, index=True)
    area = Column (Float, index=True)  # en m²

    # Localisation
    address = Column (String)
    city = Column (String, index=True)
    postal_code = Column (String, index=True)
    region = Column (String, index=True)
    country = Column (String, default="France")
    latitude = Column (Float)
    longitude = Column (Float)
    geom = Column (Geometry ('POINT'))

    # Caractéristiques
    zone_type = Column (String, index=True)  # résidentiel, commercial, agricole, etc.
    has_water = Column (Boolean, default=False)
    has_electricity = Column (Boolean, default=False)
    has_gas = Column (Boolean, default=False)
    slope_percentage = Column (Float)
    soil_type = Column (String)

    # Restrictions et réglementations
    building_permit_status = Column (String)
    max_building_height = Column (Float)
    max_building_area = Column (Float)

    # Métadonnées
    created_at = Column (Date)
    updated_at = Column (Date)
    is_active = Column (Boolean, default=True)
    thumbnail_url = Column (String)

    # Relations
    images = relationship ("TerrainImage", back_populates="terrain")
    documents = relationship ("TerrainDocument", back_populates="terrain")
    nearest_pois = relationship ("TerrainPOI", back_populates="terrain")


class TerrainImage (Base) :
    __tablename__ = "terrain_images"

    id = Column (Integer, primary_key=True, index=True)
    terrain_id = Column (Integer, ForeignKey ("terrains.id"))
    url = Column (String)
    caption = Column (String)
    is_main = Column (Boolean, default=False)

    terrain = relationship ("Terrain", back_populates="images")


class TerrainDocument (Base) :
    __tablename__ = "terrain_documents"

    id = Column (Integer, primary_key=True, index=True)
    terrain_id = Column (Integer, ForeignKey ("terrains.id"))
    name = Column (String)
    url = Column (String)
    type = Column (String)  # cadastre, plan local d'urbanisme, etc.

    terrain = relationship ("Terrain", back_populates="documents")


class POI (Base) :
    __tablename__ = "pois"

    id = Column (Integer, primary_key=True, index=True)
    name = Column (String, index=True)
    type = Column (String, index=True)  # école, hôpital, commerce, etc.
    latitude = Column (Float)
    longitude = Column (Float)
    geom = Column (Geometry ('POINT'))

    terrain_pois = relationship ("TerrainPOI", back_populates="poi")


class TerrainPOI (Base) :
    __tablename__ = "terrain_pois"

    terrain_id = Column (Integer, ForeignKey ("terrains.id"), primary_key=True)
    poi_id = Column (Integer, ForeignKey ("pois.id"), primary_key=True)
    distance = Column (Float)  # en mètres

    terrain = relationship ("Terrain", back_populates="nearest_pois")
    poi = relationship ("POI", back_populates="terrain_pois")