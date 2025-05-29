import httpx
from typing import Dict, Any, List, Optional
from app.core.config import settings

class KakaoMapService:
    """카카오 지도 API 서비스"""
    
    BASE_URL = "https://dapi.kakao.com/v2/local"
    
    def __init__(self):
        self.api_key = settings.KAKAO_API_KEY
        self.headers = {
            "Authorization": f"KakaoAK {self.api_key}"
        }
    
    async def search_keyword(self, query: str, x: Optional[str] = None, y: Optional[str] = None, 
                            radius: int = 1000, page: int = 1, size: int = 15) -> Dict[str, Any]:
        """
        키워드로 장소 검색
        
        Args:
            query: 검색할 키워드
            x: 중심 경도 좌표
            y: 중심 위도 좌표
            radius: 반경 (미터 단위)
            page: 페이지 번호
            size: 한 페이지에 보여질 문서 수
            
        Returns:
            검색 결과
        """
        url = f"{self.BASE_URL}/search/keyword.json"
        params = {
            "query": query,
            "page": page,
            "size": size
        }
        
        # 좌표 기반 검색인 경우
        if x and y:
            params.update({
                "x": x,
                "y": y,
                "radius": radius
            })
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
    
    async def search_category(self, category_group_code: str, x: str, y: str, 
                             radius: int = 1000, page: int = 1, size: int = 15) -> Dict[str, Any]:
        """
        카테고리로 장소 검색
        
        Args:
            category_group_code: 카테고리 코드
            x: 중심 경도 좌표
            y: 중심 위도 좌표
            radius: 반경 (미터 단위)
            page: 페이지 번호
            size: 한 페이지에 보여질 문서 수
            
        Returns:
            검색 결과
        """
        url = f"{self.BASE_URL}/search/category.json"
        params = {
            "category_group_code": category_group_code,
            "x": x,
            "y": y,
            "radius": radius,
            "page": page,
            "size": size
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
    
    async def get_address(self, x: str, y: str) -> Dict[str, Any]:
        """
        좌표로 주소 검색 (좌표 -> 주소)
        
        Args:
            x: 경도 좌표
            y: 위도 좌표
            
        Returns:
            주소 정보
        """
        url = f"{self.BASE_URL}/geo/coord2address.json"
        params = {
            "x": x,
            "y": y
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
    
    async def get_coordinates(self, address: str) -> Dict[str, Any]:
        """
        주소로 좌표 검색 (주소 -> 좌표)
        
        Args:
            address: 주소
            
        Returns:
            좌표 정보
        """
        url = f"{self.BASE_URL}/search/address.json"
        params = {
            "query": address
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
