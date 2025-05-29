from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.session import Base

class RentalStatus(enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    station_id = Column(String, nullable=False)  # 대여소 ID
    bike_id = Column(String, nullable=False)  # 자전거 ID
    rental_time = Column(DateTime(timezone=True), server_default=func.now())
    return_time = Column(DateTime(timezone=True), nullable=True)
    return_station_id = Column(String, nullable=True)  # 반납 대여소 ID
    status = Column(Enum(RentalStatus), default=RentalStatus.ACTIVE, nullable=False)
    cost = Column(Float, nullable=True)  # 이용 요금
    
    # 관계 정의
    user = relationship("User", back_populates="rentals")
    
    def __repr__(self):
        return f"<Rental {self.id} - {self.status.value}>"
