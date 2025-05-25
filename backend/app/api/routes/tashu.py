from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from app.services.tashu import TashuService
from app.api.dependencies import get_tashu_service

router = APIRouter()

@router.get("/stations")
async def get_tashu_stations(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: Optional[int] = Query(None, ge=0, le=20000),
    tashu_service: TashuService = Depends(get_tashu_service)
):
    """
    타슈 대여소 목록 조회
    """
    try:
        stations = await tashu_service.get_stations(
            latitude=latitude, longitude=longitude, radius=radius
        )
        
        # 위치 정보 형식으로 변환
        locations = [tashu_service.parse_station_to_location(station) for station in stations]
        return {"total": len(locations), "items": locations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"타슈 대여소 조회 중 오류 발생: {str(e)}")

@router.get("/stations/{station_id}")
async def get_tashu_station_detail(
    station_id: str,
    tashu_service: TashuService = Depends(get_tashu_service)
):
    """
    타슈 대여소 상세 정보 조회
    """
    try:
        station = await tashu_service.get_station_detail(station_id=station_id)
        if not station:
            raise HTTPException(status_code=404, detail=f"ID가 {station_id}인 대여소를 찾을 수 없습니다")
        
        # 위치 정보 형식으로 변환
        location = tashu_service.parse_station_to_location(station)
        return location
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"타슈 대여소 상세 정보 조회 중 오류 발생: {str(e)}")

@router.get("/stations/{station_id}/bikes")
async def get_tashu_available_bikes(
    station_id: str,
    tashu_service: TashuService = Depends(get_tashu_service)
):
    """
    타슈 대여소별 사용 가능한 자전거 수 조회
    """
    try:
        bikes_info = await tashu_service.get_available_bikes(station_id=station_id)
        if not bikes_info:
            raise HTTPException(status_code=404, detail=f"ID가 {station_id}인 대여소의 자전거 정보를 찾을 수 없습니다")
        
        return bikes_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"타슈 대여소 자전거 정보 조회 중 오류 발생: {str(e)}")
