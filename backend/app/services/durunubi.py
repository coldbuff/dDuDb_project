import httpx
from typing import Dict, Any, List, Optional
from app.core.config import settings

class DurunubiService:
    """두루누비(자전거 도로 및 보행로) API 서비스"""
    
    # 두루누비 API 엔드포인트는 실제 API에 맞게 수정해야 합니다
    BASE_URL = "https://api.durunubi.kr/api/v1"  # 예시 URL
    
    def __init__(self):
        self.api_key = settings.DURUNUBI_API_KEY
    
    async def get_bike_routes(self, latitude: Optional[float] = None, 
                             longitude: Optional[float] = None, 
                             radius: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        자전거 도로 정보 조회
        
        Args:
            latitude: 위도 (선택)
            longitude: 경도 (선택)
            radius: 반경 (미터 단위, 선택)
            
        Returns:
            자전거 도로 목록
        """
        url = f"{self.BASE_URL}/bike/routes"
        params = {
            "apiKey": self.api_key
        }
        
        # 위치 기반 검색인 경우
        if latitude and longitude and radius:
            params.update({
                "lat": latitude,
                "lng": longitude,
                "radius": radius
            })
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()["data"]
            except httpx.HTTPStatusError as e:
                # API 오류 처리
                print(f"두루누비 API 오류: {e}")
                return []
            except Exception as e:
                # 기타 오류 처리
                print(f"두루누비 API 호출 중 오류 발생: {e}")
                return []
    
    async def get_bike_facilities(self, latitude: float, longitude: float, 
                                radius: int = 5000) -> List[Dict[str, Any]]:
        """
        자전거 시설물(주차장, 수리센터 등) 정보 조회
        
        Args:
            latitude: 위도
            longitude: 경도
            radius: 반경 (미터 단위)
            
        Returns:
            자전거 시설물 목록
        """
        url = f"{self.BASE_URL}/bike/facilities"
        params = {
            "apiKey": self.api_key,
            "lat": latitude,
            "lng": longitude,
            "radius": radius
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()["data"]
            except httpx.HTTPStatusError as e:
                # API 오류 처리
                print(f"두루누비 API 오류: {e}")
                return []
            except Exception as e:
                # 기타 오류 처리
                print(f"두루누비 API 호출 중 오류 발생: {e}")
                return []
    
    async def get_walking_routes(self, latitude: float, longitude: float, 
                               radius: int = 5000) -> List[Dict[str, Any]]:
        """
        보행로 정보 조회
        
        Args:
            latitude: 위도
            longitude: 경도
            radius: 반경 (미터 단위)
            
        Returns:
            보행로 목록
        """
        url = f"{self.BASE_URL}/walking/routes"
        params = {
            "apiKey": self.api_key,
            "lat": latitude,
            "lng": longitude,
            "radius": radius
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()["data"]
            except httpx.HTTPStatusError as e:
                # API 오류 처리
                print(f"두루누비 API 오류: {e}")
                return []
            except Exception as e:
                # 기타 오류 처리
                print(f"두루누비 API 호출 중 오류 발생: {e}")
                return []
    
    async def get_route_detail(self, route_id: str) -> Dict[str, Any]:
        """
        경로 상세 정보 조회
        
        Args:
            route_id: 경로 ID
            
        Returns:
            경로 상세 정보
        """
        url = f"{self.BASE_URL}/route/{route_id}"
        params = {
            "apiKey": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()["data"]
            except httpx.HTTPStatusError as e:
                # API 오류 처리
                print(f"두루누비 API 오류: {e}")
                return {}
            except Exception as e:
                # 기타 오류 처리
                print(f"두루누비 API 호출 중 오류 발생: {e}")
                return {}
    
    def parse_facility_to_location(self, facility: Dict[str, Any]) -> Dict[str, Any]:
        """
        두루누비 시설물 정보를 위치 정보로 변환
        
        Args:
            facility: 두루누비 시설물 정보
            
        Returns:
            위치 정보
        """
        return {
            "name": facility.get("name", ""),
            "latitude": float(facility.get("latitude", 0)),
            "longitude": float(facility.get("longitude", 0)),
            "address": facility.get("address", ""),
            "type": "durunubi",
            "external_id": str(facility.get("id", "")),
            "details": {
                "facility_type": facility.get("type", ""),
                "description": facility.get("description", ""),
                "is_active": facility.get("is_active", True)
            }
        }
