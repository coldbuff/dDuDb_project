from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.location import Location

class FavoriteBase(BaseModel):
    location_id: int
    memo: Optional[str] = None

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteUpdate(BaseModel):
    memo: Optional[str] = None

class FavoriteInDB(FavoriteBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Favorite(FavoriteInDB):
    location: Optional[Location] = None

class FavoriteWithLocation(FavoriteInDB):
    location: Location
