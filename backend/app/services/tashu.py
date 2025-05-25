import httpx
from typing import Dict, Any, List, Optional
from app.core.config import settings
import json

class TashuService:
    """타슈(대전시 공공자전거) API 서비스"""
    
    # 타슈 API 엔드포인트는 실제 API에 맞게 수정해야 합니다
    BASE_URL = "https://api.tashu.or.kr/api/v1"  # 예시 URL
    
    def __init__(self):
        self.api_key = settings.TASHU_API_KEY
    
    async def get_stations(self, latitude: Optional[float] = None, 
                          longitude: Optional[float] = None, 
                          radius: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        타슈 대여소 목록 조회
        
        Args:
            latitude: 위도 (선택)
            longitude: 경도 (선택)
            radius: 반경 (미터 단위, 선택)
            
        Returns:
            대여소 목록
        """
        url = f"{self.BASE_URL}/station/list"
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
                print(f"타슈 API 오류: {e}")
                return []
            except Exception as e:
                # 기타 오류 처리
                print(f"타슈 API 호출 중 오류 발생: {e}")
                return []
    
    async def get_station_detail(self, station_id: str) -> Dict[str, Any]:
        """
        타슈 대여소 상세 정보 조회
        
        Args:
            station_id: 대여소 ID
            
        Returns:
            대여소 상세 정보
        """
        url = f"{self.BASE_URL}/station/{station_id}"
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
                print(f"타슈 API 오류: {e}")
                return {}
            except Exception as e:
                # 기타 오류 처리
                print(f"타슈 API 호출 중 오류 발생: {e}")
                return {}
    
    async def get_available_bikes(self, station_id: str) -> Dict[str, Any]:
        """
        대여소별 사용 가능한 자전거 수 조회
        
        Args:
            station_id: 대여소 ID
            
        Returns:
            사용 가능한 자전거 정보
        """
        url = f"{self.BASE_URL}/station/{station_id}/bikes"
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
                print(f"타슈 API 오류: {e}")
                return {}
            except Exception as e:
                # 기타 오류 처리
                print(f"타슈 API 호출 중 오류 발생: {e}")
                return {}
    
    def parse_station_to_location(self, station: Dict[str, Any]) -> Dict[str, Any]:
        """
        타슈 대여소 정보를 위치 정보로 변환
        
        Args:
            station: 타슈 대여소 정보
            
        Returns:
            위치 정보
        """
        return {
            "name": station.get("name", ""),
            "latitude": float(station.get("latitude", 0)),
            "longitude": float(station.get("longitude", 0)),
            "address": station.get("address", ""),
            "type": "tashu",
            "external_id": str(station.get("id", "")),
            "details": {
                "total_bikes": station.get("total_bikes", 0),
                "available_bikes": station.get("available_bikes", 0),
                "is_active": station.get("is_active", True)
            }
        }
