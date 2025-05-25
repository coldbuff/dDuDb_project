from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    # 관계 정의
    favorites = relationship("Favorite", back_populates="user")
    rentals = relationship("Rental", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"
