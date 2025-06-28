from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class TerrainBase (BaseModel) :
    title: str
    description: Optional[str] = None
    price: float
    area: float
    address: Optional[str] = None
    city: str
    postal_code: str
    zone_type: str
    has_water: bool = False
    has_electricity: bool = False
    has_gas: bool = False
    latitude: float
    longitude: float


class TerrainCreate (TerrainBase) :
    pass


class TerrainImage (BaseModel) :
    id: int
    url: str
    caption: Optional[str] = None
    is_main: bool

    class Config :
        orm_mode = True


class POIBase (BaseModel) :
    name: str
    type: str
    latitude: float
    longitude: float


class POI (POIBase) :
    id: int

    class Config :
        orm_mode = True


class TerrainPOI (BaseModel) :
    poi: POI
    distance: float

    class Config :
        orm_mode = True


class TerrainDocument (BaseModel) :
    id: int
    name: str
    url: str
    type: str

    class Config :
        orm_mode = True


class Terrain (TerrainBase) :
    id: int
    region: Optional[str] = None
    country: str = "France"
    slope_percentage: Optional[float] = None
    soil_type: Optional[str] = None
    thumbnail_url: Optional[str] = None

    class Config :
        orm_mode = True


class TerrainDetail (Terrain) :
    building_permit_status: Optional[str] = None
    max_building_height: Optional[float] = None
    max_building_area: Optional[float] = None
    created_at: Optional[date] = None
    updated_at: Optional[date] = None
    images: List[TerrainImage] = []
    documents: List[TerrainDocument] = []
    nearest_pois: List[TerrainPOI] = []

    class Config :
        orm_mode = True