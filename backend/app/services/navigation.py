import httpx
from typing import Dict, Any, List, Optional
from app.core.config import settings

class NavigationService:
    """네비게이션 서비스 - 경로 탐색 및 안내"""
    
    # 카카오 모빌리티 API 기반 (실제 엔드포인트는 API 문서 참조)
    BASE_URL = "https://apis-navi.kakaomobility.com/v1"
    
    def __init__(self):
        self.api_key = settings.KAKAO_API_KEY
        self.headers = {
            "Authorization": f"KakaoAK {self.api_key}"
        }
    
    async def get_directions(self, 
                           origin_x: float, 
                           origin_y: float, 
                           destination_x: float, 
                           destination_y: float,
                           waypoints: Optional[List[Dict[str, float]]] = None,
                           priority: str = "RECOMMEND",  # RECOMMEND, DISTANCE, TIME
                           car_fuel: str = "GASOLINE",
                           car_hipass: bool = False,
                           alternatives: bool = False,
                           road_details: bool = True) -> Dict[str, Any]:
        """
        자동차 길찾기 API
        
        Args:
            origin_x: 출발지 경도
            origin_y: 출발지 위도
            destination_x: 목적지 경도
            destination_y: 목적지 위도
            waypoints: 경유지 목록 [{"x": 경도, "y": 위도}, ...]
            priority: 길안내 우선순위 (RECOMMEND: 추천, DISTANCE: 최단거리, TIME: 최소시간)
            car_fuel: 자동차 연료 (GASOLINE, DIESEL, LPG, ELECTRIC)
            car_hipass: 하이패스 사용 여부
            alternatives: 대안 경로 요청 여부
            road_details: 도로 상세 정보 포함 여부
            
        Returns:
            경로 정보
        """
        url = f"{self.BASE_URL}/directions"
        
        # 요청 본문 구성
        payload = {
            "origin": {
                "x": origin_x,
                "y": origin_y
            },
            "destination": {
                "x": destination_x,
                "y": destination_y
            },
            "priority": priority,
            "car_fuel": car_fuel,
            "car_hipass": car_hipass,
            "alternatives": alternatives,
            "road_details": road_details
        }
        
        # 경유지가 있는 경우
        if waypoints:
            payload["waypoints"] = waypoints
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"길찾기 API 오류: {e}")
                return {"error": str(e)}
            except Exception as e:
                print(f"길찾기 API 호출 중 오류 발생: {e}")
                return {"error": str(e)}
    
    async def get_bike_directions(self,
                                origin_x: float,
                                origin_y: float,
                                destination_x: float,
                                destination_y: float,
                                waypoints: Optional[List[Dict[str, float]]] = None,
                                priority: str = "RECOMMEND") -> Dict[str, Any]:
        """
        자전거 길찾기 API
        
        Args:
            origin_x: 출발지 경도
            origin_y: 출발지 위도
            destination_x: 목적지 경도
            destination_y: 목적지 위도
            waypoints: 경유지 목록 [{"x": 경도, "y": 위도}, ...]
            priority: 길안내 우선순위 (RECOMMEND: 추천, SAFETY: 안전우선, DISTANCE: 최단거리)
            
        Returns:
            자전거 경로 정보
        """
        # 실제 API가 없으므로 두루누비 데이터와 카카오 API를 조합하여 구현
        # 여기서는 예시로 구현
        
        # 자전거 도로 정보 가져오기
        bike_routes = await self._get_bike_routes_near_path(
            origin_x, origin_y, destination_x, destination_y
        )
        
        # 기본 경로 정보 가져오기
        base_directions = await self.get_directions(
            origin_x, origin_y, destination_x, destination_y,
            waypoints=waypoints, priority="DISTANCE"
        )
        
        # 자전거 경로 최적화 (실제로는 더 복잡한 알고리즘 필요)
        optimized_route = self._optimize_bike_route(base_directions, bike_routes, priority)
        
        return optimized_route
    
    async def _get_bike_routes_near_path(self, 
                                       origin_x: float, 
                                       origin_y: float, 
                                       destination_x: float, 
                                       destination_y: float) -> List[Dict[str, Any]]:
        """
        경로 주변의 자전거 도로 정보 조회
        """
        # 실제 구현에서는 두루누비 API 또는 자체 DB에서 자전거 도로 정보 조회
        # 여기서는 더미 데이터 반환
        return [
            {
                "route_id": "bike_route_1",
                "name": "한강 자전거 도로",
                "safety_level": 5,  # 1-5, 5가 가장 안전
                "path": [
                    {"x": origin_x + 0.001, "y": origin_y + 0.001},
                    {"x": origin_x + 0.002, "y": origin_y + 0.002},
                    # ... 더 많은 좌표
                ]
            },
            {
                "route_id": "bike_route_2",
                "name": "도심 자전거 도로",
                "safety_level": 3,
                "path": [
                    {"x": destination_x - 0.001, "y": destination_y - 0.001},
                    {"x": destination_x - 0.002, "y": destination_y - 0.002},
                    # ... 더 많은 좌표
                ]
            }
        ]
    
    def _optimize_bike_route(self, 
                           base_directions: Dict[str, Any], 
                           bike_routes: List[Dict[str, Any]], 
                           priority: str) -> Dict[str, Any]:
        """
        자전거 경로 최적화
        
        Args:
            base_directions: 기본 경로 정보
            bike_routes: 자전거 도로 정보
            priority: 우선순위 (RECOMMEND, SAFETY, DISTANCE)
            
        Returns:
            최적화된 자전거 경로
        """
        # 실제 구현에서는 복잡한 경로 최적화 알고리즘 적용
        # 여기서는 간단한 예시만 구현
        
        # 에러 처리
        if "error" in base_directions:
            return base_directions
        
        # 기본 응답 구조 복사
        optimized = base_directions.copy()
        
        # 자전거 경로 정보 추가
        if "routes" in optimized and optimized["routes"]:
            for route in optimized["routes"]:
                route["bike_friendly"] = True
                route["bike_safety_score"] = 4.5  # 1-5 척도
                
                # 우선순위에 따라 추가 정보 설정
                if priority == "SAFETY":
                    route["bike_safety_tips"] = [
                        "이 경로는 자전거 전용도로를 포함합니다.",
                        "교차로에서 주의하세요.",
                        "헬멧 착용을 권장합니다."
                    ]
                elif priority == "DISTANCE":
                    route["bike_shortcuts"] = [
                        {"description": "공원 통과 경로", "distance_saved": 300}  # 미터 단위
                    ]
        
        # 자전거 경로 전용 정보 추가
        optimized["bike_specific"] = {
            "recommended_routes": [route["route_id"] for route in bike_routes],
            "difficulty_level": "MEDIUM",  # EASY, MEDIUM, HARD
            "estimated_calories": 250,  # kcal
            "terrain_type": "MIXED"  # FLAT, HILLY, MIXED
        }
        
        return optimized
    
    async def get_pedestrian_directions(self,
                                      origin_x: float,
                                      origin_y: float,
                                      destination_x: float,
                                      destination_y: float,
                                      waypoints: Optional[List[Dict[str, float]]] = None) -> Dict[str, Any]:
        """
        보행자 길찾기 API
        
        Args:
            origin_x: 출발지 경도
            origin_y: 출발지 위도
            destination_x: 목적지 경도
            destination_y: 목적지 위도
            waypoints: 경유지 목록 [{"x": 경도, "y": 위도}, ...]
            
        Returns:
            보행자 경로 정보
        """
        url = f"{self.BASE_URL}/directions/pedestrian"
        
        # 요청 본문 구성
        payload = {
            "origin": {
                "x": origin_x,
                "y": origin_y
            },
            "destination": {
                "x": destination_x,
                "y": destination_y
            }
        }
        
        # 경유지가 있는 경우
        if waypoints:
            payload["waypoints"] = waypoints
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"보행자 길찾기 API 오류: {e}")
                return {"error": str(e)}
            except Exception as e:
                print(f"보행자 길찾기 API 호출 중 오류 발생: {e}")
                return {"error": str(e)}
