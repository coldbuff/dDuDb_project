from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
from app.core.config import settings

# 데이터베이스 초기화 함수
def init_db() -> None:
    # 모든 테이블 생성
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
