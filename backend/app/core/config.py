from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "지도 통합 API 서비스"
    API_V1_STR: str = "/api/v1"
    
    # API 키
    KAKAO_API_KEY: str = os.getenv("KAKAO_API_KEY", "")
    TASHU_API_KEY: Optional[str] = os.getenv("TASHU_API_KEY", "")
    DURUNUBI_API_KEY: Optional[str] = os.getenv("DURUNUBI_API_KEY", "")
    
    # 데이터베이스 설정
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # 보안 설정
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    class Config:
        case_sensitive = True

settings = Settings()
