from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
import models
import schemas


def get_terrain(db: Session, terrain_id: int) :
    return db.query (models.Terrain).filter (models.Terrain.id == terrain_id).first ( )


def get_terrains(
        db: Session,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_area: Optional[int] = None,
        max_area: Optional[int] = None,
        city: Optional[str] = None,
        distance_to_city: Optional[int] = None,
        has_water: Optional[bool] = None,
        has_electricity: Optional[bool] = None,
        zone_type: Optional[str] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius: Optional[float] = None,
        skip: int = 0,
        limit: int = 100
) :
    query = db.query (models.Terrain).filter (models.Terrain.is_active == True)

    if min_price is not None :
        query = query.filter (models.Terrain.price >= min_price)
    if max_price is not None :
        query = query.filter (models.Terrain.price <= max_price)
    if min_area is not None :
        query = query.filter (models.Terrain.area >= min_area)
    if max_area is not None :
        query = query.filter (models.Terrain.area <= max_area)
    if city is not None :
        query = query.filter (models.Terrain.city.ilike (f"%{city}%"))
    if has_water is not None :
        query = query.filter (models.Terrain.has_water == has_water)
    if has_electricity is not None :
        query = query.filter (models.Terrain.has_electricity == has_electricity)
    if zone_type is not None :
        query = query.filter (models.Terrain.zone_type == zone_type)

    # Recherche géospatiale si latitude, longitude et rayon sont fournis
    if lat is not None and lng is not None and radius is not None :
        # Utilise PostGIS pour calculer la distance et filtrer
        point = func.ST_SetSRID (func.ST_MakePoint (lng, lat), 4326)
        distance = func.ST_DistanceSphere (models.Terrain.geom, point)
        query = query.filter (distance <= radius)
        query = query.order_by (distance)

    return query.offset (skip).limit (limit).all ( )


def create_terrain(db: Session, terrain: schemas.TerrainCreate) :
    db_terrain = models.Terrain (
        title=terrain.title,
        description=terrain.description,
        price=terrain.price,
        area=terrain.area,
        address=terrain.address,
        city=terrain.city,
        postal_code=terrain.postal_code,
        zone_type=terrain.zone_type,
        has_water=terrain.has_water,
        has_electricity=terrain.has_electricity,
        has_gas=terrain.has_gas,
        latitude=terrain.latitude,
        longitude=terrain.longitude,
        # Créer le point géographique pour PostGIS
        geom=func.ST_SetSRID (func.ST_MakePoint (terrain.longitude, terrain.latitude), 4326)
    )
    db.add (db_terrain)
    db.commit ( )
    db.refresh (db_terrain)
    return db_terrain