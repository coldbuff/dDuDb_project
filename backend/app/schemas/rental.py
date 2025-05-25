from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RentalStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class RentalBase(BaseModel):
    user_id: int
    station_id: str
    bike_id: str

class RentalCreate(RentalBase):
    pass

class RentalUpdate(BaseModel):
    return_station_id: Optional[str] = None
    status: Optional[RentalStatus] = None

class RentalInDB(RentalBase):
    id: int
    rental_time: datetime
    return_time: Optional[datetime] = None
    return_station_id: Optional[str] = None
    status: RentalStatus
    cost: Optional[float] = None

    class Config:
        orm_mode = True

class Rental(RentalInDB):
    pass

class RentalList(BaseModel):
    total: int
    items: List[Rental]

    class Config:
        orm_mode = True
