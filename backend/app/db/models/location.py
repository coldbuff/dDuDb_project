from sqlalchemy import Column, Integer, String, Float, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.session import Base

class LocationType(enum.Enum):
    TASHU = "tashu"
    DURUNUBI = "durunubi"
    CUSTOM = "custom"

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=True)
    type = Column(Enum(LocationType), nullable=False)
    external_id = Column(String, nullable=True)  # 외부 API의 ID
    details = Column(String, nullable=True)  # 추가 정보 (JSON 형태로 저장)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 관계 정의
    favorites = relationship("Favorite", back_populates="location")
    
    def __repr__(self):
        return f"<Location {self.name} ({self.type.value})>"
