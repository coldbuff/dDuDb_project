from dataclasses import dataclass

from daejeonBike import DaejeonBikeAPI
from cch import CustomizableContractionHierarchies, Graph, Vertex, Arc

# CCH 알고리즘과 대전광역시 자전거 도로 API를 결합한 예제
def daejeon_bike_cch_example():
    # 대전광역시 자전거 도로 API 인스턴스 생성
    daejeon_bike_api = DaejeonBikeAPI()
    
    # 대전광역시 자전거 도로 데이터 가져오기
    print("대전광역시 자전거 도로 데이터 요청 중...")
    bike_routes = daejeon_bike_api.get_bike_routes(page_no=1, num_of_rows=30)
    print("API 요청 완료")
    
    # API 응답 디버깅
    if bike_routes:
        header = bike_routes.get('GetBycpListService', {}).get('header', {})
        result_code = header.get('resultCode', '')
        result_msg = header.get('resultMsg', '')
        print(f"API 응답 코드: {result_code}, 메시지: {result_msg}")
    else:
        print("API 응답을 받지 못했습니다.")
        
    # 자전거 도로 데이터로 그래프 생성
    graph = daejeon_bike_api.create_graph_from_api_data(bike_routes)
    
    # 그래프에 정점이 있는지 확인
    if len(graph.vertices) > 1:
        # 최단 경로 계산을 위한 시작점과 도착점 선택
        start_id = 0  # 첫 번째 정점
        end_id = 1    # 두 번째 정점
        
        # 1. 메트릭 독립적 전처리 단계 실행
        print("\n1. 메트릭 독립적 전처리 단계 실행...")
        cch = CustomizableContractionHierarchies(graph)
        cch.metric_independent_preprocessing(len(graph.vertices))
        
        # 2. 커스터마이징 단계 - 실제 간선 비용 적용
        print("\n2. 커스터마이징 단계 - 실제 간선 비용 적용...")
        cch.customize()
        
        # 간선 비용 출력
        print("\n업데이트된 간선 비용:")
        for (source_id, target_id), arc in graph.arcs.items():
            if source_id < 5 and target_id < 5:  # 처음 5개 정점 간의 간선만 출력
                print(f"{source_id} -> {target_id}: {arc.cost}")
        
        # 경로 추출 테스트
        print(f"\n{start_id}->{end_id} 경로 풀기 결과:")
        path = []
        
        # 직접 간선이 있는지 확인
        start_arc = graph.arcs.get((start_id, end_id))
        if start_arc:
            cch.unpack_path(start_arc, path)
            
            # 결과 출력
            if path:
                total_cost = 0
                for arc in path:
                    print(f"{arc.source.id} -> {arc.target.id} (비용: {arc.cost})")
                    total_cost += arc.cost
                print(f"\n총 비용: {total_cost}")
            else:
                print("  경로를 찾을 수 없습니다.")
        else:
            print("  직접 간선이 없습니다. 다른 경로를 탐색합니다.")
            
            # CCH 알고리즘을 사용하여 경로 찾기
            # 여기에 추가 경로 찾기 로직 구현
        
        # 3. 다른 메트릭 적용 예시 (전기자전거 경로)
        print("\n3. 다른 메트릭 적용 예시 (전기자전거 경로)...")
        
        # 전기자전거 메트릭으로 동일한 경로 풀기
        print(f"\n전기자전거 메트릭으로 {start_id}->{end_id} 경로 풀기 결과:")
        if start_arc:
            path = []
            cch.unpack_path(start_arc, path)
            
            if path:
                total_cost = 0
                for arc in path:
                    print(f"{arc.source.id} -> {arc.target.id} (비용: {arc.cost})")
                    total_cost += arc.cost
                print(f"\n총 비용: {total_cost}")
            else:
                print("  경로를 찾을 수 없습니다.")
    
    else:
        print("  경로 계산을 위한 충분한 정점이 없습니다.")
        return graph  # 그래프 반환
    
    print("\n대전광역시 자전거 도로 데이터를 이용한 CCH 알고리즘 예제 완료")
    return graph  # 생성된 그래프 반환


# 메인 함수
if __name__ == "__main__":
    # 대전광역시 자전거도로조회서비스 API와 CCH 알고리즘을 결합한 예제 실행
    print("대전광역시 자전거 도로 API와 CCH 알고리즘 예제 실행\n")
    daejeon_bike_cch_example()
    
    # 기본 예제도 실행 가능
    # print("\n기본 CCH 알고리즘 예제 실행\n")
    # simple_cch_example()

