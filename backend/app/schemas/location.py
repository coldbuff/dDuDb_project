from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

class LocationType(str, Enum):
    TASHU = "tashu"
    DURUNUBI = "durunubi"
    CUSTOM = "custom"

class LocationBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    type: LocationType
    external_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class LocationInDB(LocationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Location(LocationInDB):
    pass

class LocationList(BaseModel):
    total: int
    items: List[Location]

    class Config:
        orm_mode = True
