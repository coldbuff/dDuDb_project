from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.routes import map, tashu, durunubi, locations, favorites, auth, navigation, rental
from app.core.config import settings

# FastAPI 애플리케이션 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 환경에서는 특정 도메인만 허용하도록 수정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["인증"])
app.include_router(map.router, prefix=f"{settings.API_V1_STR}/map", tags=["지도"])
app.include_router(tashu.router, prefix=f"{settings.API_V1_STR}/tashu", tags=["타슈"])
app.include_router(durunubi.router, prefix=f"{settings.API_V1_STR}/durunubi", tags=["두루누비"])
app.include_router(locations.router, prefix=f"{settings.API_V1_STR}/locations", tags=["위치"])
app.include_router(favorites.router, prefix=f"{settings.API_V1_STR}/favorites", tags=["즐겨찾기"])
app.include_router(navigation.router, prefix=f"{settings.API_V1_STR}/navigation", tags=["네비게이션"])
app.include_router(rental.router, prefix=f"{settings.API_V1_STR}/rentals", tags=["대여"])

# 루트 경로
@app.get("/")
def root():
    return {
        "message": "지도 통합 API 서비스에 오신 것을 환영합니다!",
        "docs_url": "/docs",
        "version": "1.0.0"
    }

# OpenAPI 스키마 커스터마이징
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="카카오 지도 API, 타슈 API, 두루누비 API를 통합한 지도 서비스 API",
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
