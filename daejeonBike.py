import heapq
import requests
import json
from dataclasses import dataclass
from typing import List, Set, Dict, Optional, Tuple, Any
import warnings
import subprocess
from cch import Graph, Vertex, Arc


class DaejeonBikeAPI:
    """
    대전광역시 자전거 도로 정보 API 클래스
    데이터포맷: JSON, API형태: REST
    대전광역시 자전거 도로 정보 서비스 API 사용
    자전거 도로 정보 제공
    """
    def __init__(self):
        # API 키 설정
        self.api_key = "JuyFVsOLXJrw0gcT9TQdLPhCjdDgUCxJXFLRBs8H3nrA8uUVv574SW2++PESxGhK25E4ekOXCeYZ+hZ7OqVcXA=="
        
        # URL에 사용하기 위해 인코딩된 API 키
        self.encoded_api_key = "JuyFVsOLXJrw0gcT9TQdLPhCjdDgUCxJXFLRBs8H3nrA8uUVv574SW2%2B%2BPESxGhK25E4ekOXCeYZ%2BhZ7OqVcXA%3D%3D"
        
        # API 기본 URL
        self.base_url = "https://apis.data.go.kr/6300000/"
        
        # API 엔드포인트
        self.bike_path_list_endpoint = "GetBycpListService"
    
    def get_bike_routes(self, page_no=1, num_of_rows=10):
        """
        대전광역시 자전거 도로 정보를 가져옵니다.
        GetBycpListService 엔드포인트를 사용하여 자전거 도로 정보를 가져옵니다.
        
        Args:
            page_no (int): 페이지 번호
            num_of_rows (int): 한 페이지 결과 수
            
        Returns:
            dict: API 응답 결과
        """
        try:
            print(f"\n대전광역시 자전거 도로 정보 요청 중...")
            
            # API URL 생성
            url = f"{self.base_url}{self.bike_path_list_endpoint}"
            params = {
                'serviceKey': self.encoded_api_key,
                'pageNo': page_no,
                'numOfRows': num_of_rows,
                'type': 'json'  # JSON 형식으로 응답 요청
            }
            
            # 요청 URL 출력
            request_url = f"{url}?serviceKey={self.encoded_api_key}&pageNo={page_no}&numOfRows={num_of_rows}&type=json"
            print(f"API 요청 URL: {request_url}")
            
            # SSL 경고 무시
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                
                # 1. requests를 사용한 요청
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0',
                        'Accept': 'application/json'
                    }
                    response = requests.get(request_url, headers=headers, verify=False)
                    
                    if response.status_code == 200:
                        try:
                            # JSON 응답 파싱
                            result = response.json()
                            
                            # 자전거 도로 정보 출력
                            if 'response' in result and 'body' in result['response'] and 'items' in result['response']['body']:
                                items = result['response']['body']['items']
                                if 'item' in items:
                                    bike_items = items['item']
                                    if not isinstance(bike_items, list):
                                        bike_items = [bike_items]
                                    
                                    print(f"자전거 도로 정보 {len(bike_items)}개 발견")
                                    
                                    # 처음 5개만 출력
                                    for i, item in enumerate(bike_items[:5]):
                                        print(f"\n자전거도로 {i+1}: {item.get('BYCP_NM', 'N/A')}")
                                        print(f"  - 위치: 위도 {item.get('BYCP_LT', 'N/A')}, 경도 {item.get('BYCP_LN', 'N/A')}")
                                        print(f"  - 길이: {item.get('BYCP_LEN', 'N/A')}km, 너비: {item.get('BYCP_WID', 'N/A')}m")
                                else:
                                    print("자전거 도로 정보가 없습니다.")
                            else:
                                print("자전거 도로 정보가 없습니다.")
                                
                            # API 응답을 대전광역시 자전거 도로 API 형식에 맞게 변환
                            response_data = {
                                'GetBycpListService': {
                                    'header': result.get('response', {}).get('header', {}),
                                    'item': bike_items if 'response' in result and 'body' in result['response'] and 
                                            'items' in result['response']['body'] and 'item' in result['response']['body']['items'] else []
                                }
                            }
                            
                            return response_data
                            
                        except json.JSONDecodeError:
                            print("JSON 파싱 오류")
                    else:
                        print(f"API 요청 오류: 상태 코드 {response.status_code}")
                        
                except Exception as e:
                    print(f"requests 요청 오류: {e}")
                
                # 2. curl을 사용한 백업 요청
                try:
                    curl_command = [
                        'curl',
                        '-s',  # 조용한 모드
                        '-k',  # SSL 인증서 검증 무시
                        request_url
                    ]
                    
                    result = subprocess.run(curl_command, capture_output=True, text=True)
                    
                    if result.returncode == 0 and result.stdout:
                        try:
                            # JSON 응답 파싱
                            data = json.loads(result.stdout)
                            
                            # API 응답을 대전광역시 자전거 도로 API 형식에 맞게 변환
                            response_data = {
                                'GetBycpListService': {
                                    'header': data.get('response', {}).get('header', {}),
                                    'item': data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
                                }
                            }
                            
                            return response_data
                        except json.JSONDecodeError:
                            print("JSON 파싱 오류")
                    else:
                        print(f"curl 요청 실패: {result.stderr}")
                except Exception as e:
                    print(f"curl 요청 오류: {e}")
            
            print("\n모든 API 요청 방법이 실패했습니다.")
            print("API 서비스가 일시적으로 중단되었거나 접근할 수 없습니다.")
            return None
            
        except Exception as e:
            print(f"API 요청 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return None
            
    def create_graph_from_api_data(self, bike_routes_data):
        """
        대전광역시 자전거도로조회서비스 API 데이터로부터 그래프를 생성합니다.
        
        Args:
            bike_routes_data (dict): API 응답 데이터
            
        Returns:
            Graph: 생성된 그래프 객체
        """
        import math
        graph = Graph()
        
        # API 데이터가 없는 경우 빈 그래프 반환
        if not bike_routes_data:
            print("유효한 API 데이터가 없습니다.")
            return graph
            
        # API 데이터 형식 확인
        if 'GetBycpListService' not in bike_routes_data:
            print("올바른 API 데이터 형식이 아닙니다.")
            return graph
        
        try:
            # 자전거 도로 정보 추출
            items = bike_routes_data.get('GetBycpListService', {}).get('item', [])
            
            # 리스트가 아닌 경우 리스트로 변환
            if isinstance(items, dict):
                items = [items]
            
            if not items:
                print("자전거 도로 정보가 없습니다.")
                return graph
                
            print(f"자전거 도로 정보 {len(items)}개 발견")
            
            # 정점 생성
            vertices = {}
            vertex_id = 0
            
            # 각 자전거 도로를 정점으로 처리
            for item in items:
                # 위도/경도 정보 추출
                lat = item.get('BYCP_LT')
                lon = item.get('BYCP_LN')
                name = item.get('BYCP_NM', '이름 없음')
                
                if not lat or not lon:
                    print(f"[경고] 자전거 도로 '{name}'의 위치 정보가 없습니다.")
                    continue
                
                try:
                    lat = float(lat)
                    lon = float(lon)
                    
                    # 정점 생성
                    vertex = Vertex(vertex_id, lat, lon)
                    graph.add_vertex(vertex)
                    vertices[vertex_id] = vertex
                    vertex_id += 1
                except ValueError:
                    print(f"[경고] 자전거 도로 '{name}'의 위치 정보가 유효하지 않습니다.")
            
            # 정점이 없는 경우 빈 그래프 반환
            if len(vertices) < 2:
                print("그래프 생성을 위한 충분한 정점이 없습니다.")
                return graph
            
            # 각 자전거 도로의 시작과 끝점을 연결하는 간선 생성
            vertex_ids = list(vertices.keys())
            for i in range(len(vertex_ids) - 1):
                v1_id = vertex_ids[i]
                v2_id = vertex_ids[i + 1]
                v1 = vertices[v1_id]
                v2 = vertices[v2_id]
                
                # 두 정점 간의 거리 계산
                distance = self._calculate_distance(v1.lat, v1.lon, v2.lat, v2.lon)
                
                # 간선 추가
                arc1 = Arc(v1, v2, distance)
                arc2 = Arc(v2, v1, distance)
                graph.add_arc(arc1)
                graph.add_arc(arc2)
                
                print(f"  간선 추가: {v1_id} -> {v2_id} (거리: {distance:.2f}km)")
            
            # 추가로 가까운 정점들을 연결하여 네트워크 구성
            for i in range(len(vertex_ids)):
                for j in range(i+1, len(vertex_ids)):
                    if j != i+1:  # 이미 연결된 정점은 제외
                        v1_id = vertex_ids[i]
                        v2_id = vertex_ids[j]
                        v1 = vertices[v1_id]
                        v2 = vertices[v2_id]
                        
                        # 두 정점 간의 거리 계산
                        distance = self._calculate_distance(v1.lat, v1.lon, v2.lat, v2.lon)
                        
                        # 일정 거리 이내의 정점만 연결 (2km 이내)
                        if distance < 2.0:
                            # 간선 추가
                            arc1 = Arc(v1, v2, distance)
                            arc2 = Arc(v2, v1, distance)
                            graph.add_arc(arc1)
                            graph.add_arc(arc2)
                            
                            print(f"  추가 간선: {v1_id} -> {v2_id} (거리: {distance:.2f}km)")
            
            print(f"그래프 생성 완료: {len(graph.vertices)}개의 정점, {len(graph.arcs)}개의 간선")
            return graph
            
        except Exception as e:
            print(f"그래프 생성 오류: {e}")
            import traceback
            traceback.print_exc()
            return graph
    
    # GPX 관련 메서드는 삭제하고 JSON을 사용하도록 변경
    
    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        두 지점 간의 거리를 계산합니다 (Haversine 공식 사용).
        
        Args:
            lat1, lon1: 첫 번째 지점의 위도/경도
            lat2, lon2: 두 번째 지점의 위도/경도
            
        Returns:
            float: 두 지점 간의 거리 (km)
        """
        from math import radians, sin, cos, sqrt, atan2
        
        # 지구 반경 (km)
        R = 6371.0
        
        # 위도/경도를 라디안으로 변환
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine 공식
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        
        return distance  # 거리(km)