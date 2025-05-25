from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from app.services.kakao_map import KakaoMapService
from app.api.dependencies import get_kakao_map_service

router = APIRouter()

@router.get("/search/keyword")
async def search_by_keyword(
    query: str,
    x: Optional[str] = None,
    y: Optional[str] = None,
    radius: int = Query(1000, ge=0, le=20000),
    page: int = Query(1, ge=1),
    size: int = Query(15, ge=1, le=45),
    kakao_map_service: KakaoMapService = Depends(get_kakao_map_service)
):
    """
    키워드로 장소 검색
    """
    try:
        result = await kakao_map_service.search_keyword(
            query=query, x=x, y=y, radius=radius, page=page, size=size
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 중 오류 발생: {str(e)}")

@router.get("/search/category")
async def search_by_category(
    category_group_code: str,
    x: str,
    y: str,
    radius: int = Query(1000, ge=0, le=20000),
    page: int = Query(1, ge=1),
    size: int = Query(15, ge=1, le=45),
    kakao_map_service: KakaoMapService = Depends(get_kakao_map_service)
):
    """
    카테고리로 장소 검색
    """
    try:
        result = await kakao_map_service.search_category(
            category_group_code=category_group_code, x=x, y=y, 
            radius=radius, page=page, size=size
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 중 오류 발생: {str(e)}")

@router.get("/address")
async def get_address_from_coords(
    x: str,
    y: str,
    kakao_map_service: KakaoMapService = Depends(get_kakao_map_service)
):
    """
    좌표로 주소 검색 (좌표 -> 주소)
    """
    try:
        result = await kakao_map_service.get_address(x=x, y=y)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"주소 검색 중 오류 발생: {str(e)}")

@router.get("/coordinates")
async def get_coords_from_address(
    address: str,
    kakao_map_service: KakaoMapService = Depends(get_kakao_map_service)
):
    """
    주소로 좌표 검색 (주소 -> 좌표)
    """
    try:
        result = await kakao_map_service.get_coordinates(address=address)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"좌표 검색 중 오류 발생: {str(e)}")
