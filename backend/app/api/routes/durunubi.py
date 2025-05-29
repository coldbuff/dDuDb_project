from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from app.services.durunubi import DurunubiService
from app.api.dependencies import get_durunubi_service

router = APIRouter()

@router.get("/bike/routes")
async def get_bike_routes(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: Optional[int] = Query(None, ge=0, le=20000),
    durunubi_service: DurunubiService = Depends(get_durunubi_service)
):
    """
    자전거 도로 정보 조회
    """
    try:
        routes = await durunubi_service.get_bike_routes(
            latitude=latitude, longitude=longitude, radius=radius
        )
        return {"total": len(routes), "items": routes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"자전거 도로 정보 조회 중 오류 발생: {str(e)}")

@router.get("/bike/facilities")
async def get_bike_facilities(
    latitude: float,
    longitude: float,
    radius: int = Query(5000, ge=0, le=20000),
    durunubi_service: DurunubiService = Depends(get_durunubi_service)
):
    """
    자전거 시설물(주차장, 수리센터 등) 정보 조회
    """
    try:
        facilities = await durunubi_service.get_bike_facilities(
            latitude=latitude, longitude=longitude, radius=radius
        )
        
        # 위치 정보 형식으로 변환
        locations = [durunubi_service.parse_facility_to_location(facility) for facility in facilities]
        return {"total": len(locations), "items": locations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"자전거 시설물 정보 조회 중 오류 발생: {str(e)}")

@router.get("/walking/routes")
async def get_walking_routes(
    latitude: float,
    longitude: float,
    radius: int = Query(5000, ge=0, le=20000),
    durunubi_service: DurunubiService = Depends(get_durunubi_service)
):
    """
    보행로 정보 조회
    """
    try:
        routes = await durunubi_service.get_walking_routes(
            latitude=latitude, longitude=longitude, radius=radius
        )
        return {"total": len(routes), "items": routes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"보행로 정보 조회 중 오류 발생: {str(e)}")

@router.get("/route/{route_id}")
async def get_route_detail(
    route_id: str,
    durunubi_service: DurunubiService = Depends(get_durunubi_service)
):
    """
    경로 상세 정보 조회
    """
    try:
        route = await durunubi_service.get_route_detail(route_id=route_id)
        if not route:
            raise HTTPException(status_code=404, detail=f"ID가 {route_id}인 경로를 찾을 수 없습니다")
        
        return route
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"경로 상세 정보 조회 중 오류 발생: {str(e)}")
