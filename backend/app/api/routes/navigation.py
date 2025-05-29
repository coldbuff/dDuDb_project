from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from app.services.navigation import NavigationService
from app.api.dependencies import get_current_user
from app.db.models.user import User

router = APIRouter()

# 네비게이션 서비스 의존성 주입 함수
def get_navigation_service():
    return NavigationService()

@router.post("/directions/car")
async def get_car_directions(
    origin_x: float,
    origin_y: float,
    destination_x: float,
    destination_y: float,
    waypoints: Optional[List[Dict[str, float]]] = None,
    priority: str = Query("RECOMMEND", enum=["RECOMMEND", "DISTANCE", "TIME"]),
    car_fuel: str = Query("GASOLINE", enum=["GASOLINE", "DIESEL", "LPG", "ELECTRIC"]),
    car_hipass: bool = False,
    alternatives: bool = False,
    road_details: bool = True,
    navigation_service: NavigationService = Depends(get_navigation_service)
):
    """
    자동차 길찾기 API
    """
    try:
        result = await navigation_service.get_directions(
            origin_x=origin_x,
            origin_y=origin_y,
            destination_x=destination_x,
            destination_y=destination_y,
            waypoints=waypoints,
            priority=priority,
            car_fuel=car_fuel,
            car_hipass=car_hipass,
            alternatives=alternatives,
            road_details=road_details
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"길찾기 중 오류 발생: {str(e)}")

@router.post("/directions/bike")
async def get_bike_directions(
    origin_x: float,
    origin_y: float,
    destination_x: float,
    destination_y: float,
    waypoints: Optional[List[Dict[str, float]]] = None,
    priority: str = Query("RECOMMEND", enum=["RECOMMEND", "SAFETY", "DISTANCE"]),
    navigation_service: NavigationService = Depends(get_navigation_service)
):
    """
    자전거 길찾기 API
    """
    try:
        result = await navigation_service.get_bike_directions(
            origin_x=origin_x,
            origin_y=origin_y,
            destination_x=destination_x,
            destination_y=destination_y,
            waypoints=waypoints,
            priority=priority
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"자전거 길찾기 중 오류 발생: {str(e)}")

@router.post("/directions/pedestrian")
async def get_pedestrian_directions(
    origin_x: float,
    origin_y: float,
    destination_x: float,
    destination_y: float,
    waypoints: Optional[List[Dict[str, float]]] = None,
    navigation_service: NavigationService = Depends(get_navigation_service)
):
    """
    보행자 길찾기 API
    """
    try:
        result = await navigation_service.get_pedestrian_directions(
            origin_x=origin_x,
            origin_y=origin_y,
            destination_x=destination_x,
            destination_y=destination_y,
            waypoints=waypoints
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"보행자 길찾기 중 오류 발생: {str(e)}")

@router.get("/tashu/nearby-routes")
async def get_nearby_tashu_routes(
    latitude: float,
    longitude: float,
    radius: float = Query(1000, ge=100, le=5000),  # 미터 단위, 최소 100m, 최대 5km
    navigation_service: NavigationService = Depends(get_navigation_service),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    현재 위치 주변의 타슈 대여소를 경유하는 추천 경로
    """
    # 이 기능은 실제 구현에서 타슈 서비스와 네비게이션 서비스를 조합하여 구현
    # 여기서는 더미 데이터 반환
    return {
        "routes": [
            {
                "name": "한강변 자전거 코스",
                "distance": 5.2,  # km
                "estimated_time": 25,  # 분
                "difficulty": "EASY",
                "stations": [
                    {
                        "id": "station_1",
                        "name": "대전역 앞 대여소",
                        "available_bikes": 8,
                        "coordinates": {"latitude": latitude + 0.01, "longitude": longitude + 0.01}
                    },
                    {
                        "id": "station_2",
                        "name": "엑스포 다리 대여소",
                        "available_bikes": 5,
                        "coordinates": {"latitude": latitude + 0.02, "longitude": longitude + 0.02}
                    }
                ],
                "path": [
                    {"latitude": latitude, "longitude": longitude},
                    {"latitude": latitude + 0.01, "longitude": longitude + 0.01},
                    {"latitude": latitude + 0.02, "longitude": longitude + 0.02},
                    {"latitude": latitude + 0.03, "longitude": longitude + 0.03}
                ]
            },
            {
                "name": "도심 관광 코스",
                "distance": 3.8,  # km
                "estimated_time": 18,  # 분
                "difficulty": "MEDIUM",
                "stations": [
                    {
                        "id": "station_3",
                        "name": "시청 앞 대여소",
                        "available_bikes": 12,
                        "coordinates": {"latitude": latitude - 0.01, "longitude": longitude - 0.01}
                    },
                    {
                        "id": "station_4",
                        "name": "대전시립미술관 대여소",
                        "available_bikes": 3,
                        "coordinates": {"latitude": latitude - 0.02, "longitude": longitude - 0.02}
                    }
                ],
                "path": [
                    {"latitude": latitude, "longitude": longitude},
                    {"latitude": latitude - 0.01, "longitude": longitude - 0.01},
                    {"latitude": latitude - 0.02, "longitude": longitude - 0.02},
                    {"latitude": latitude - 0.03, "longitude": longitude - 0.03}
                ]
            }
        ],
        "total": 2
    }
