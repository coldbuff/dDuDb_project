# 뚜따 서비스

카카오 지도 API, 타슈 API, 두루누비 API를 통합한 뚜따 서비스의 백엔드 구성입니다. FastAPI로 구현되었으며, 리액트 네이티브 모바일 앱의 백엔드로 사용됩니다.

## 기능

- **카카오 지도 API 통합**: 키워드 검색, 카테고리 검색, 주소-좌표 변환 등
- **타슈 API 통합**: 대여소 목록, 대여소 상세 정보, 자전거 이용 가능 여부 등
- **두루누비 API 통합**: 자전거 도로, 보행로, 자전거 시설물 정보 등
- **위치 정보 관리**: 위치 정보 저장, 조회, 업데이트, 삭제
- **즐겨찾기 기능**: 사용자별 위치 즐겨찾기 관리
- **사용자 인증**: 회원가입, 로그인, JWT 인증
- **자전거 대여 시스템**: 자전거 대여 및 반납, 이용 요금 계산
- **네비게이션 기능**: 자동차, 자전거, 보행자 경로 안내

## 프로젝트 구조

```
project_root/
├── backend/                # FastAPI 백엔드
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI 앱 진입점
│   │   ├── api/            # API 라우터
│   │   ├── core/           # 설정, 보안 등
│   │   ├── db/             # 데이터베이스 모델, 세션
│   │   ├── schemas/        # Pydantic 모델
│   │   └── services/       # 비즈니스 로직
│   ├── alembic/            # 데이터베이스 마이그레이션
│   ├── requirements.txt    # 의존성 목록
│   ├── .env                # 환경 변수
│   └── README.md
└── frontend/               # 리액트 네이티브 프론트엔드 (별도 개발)
```

## 설치 및 실행 방법

### 사전 요구사항

- Python 3.8 이상
- PostgreSQL 데이터베이스 (개발 환경에서는 SQLite 사용 가능)
- 카카오 API 키, 타슈 API 키, 두루누비 API 키

### 백엔드 설치

1. 저장소 클론

```bash
git clone <repository-url>
cd map_integration_project/backend
```

2. 가상 환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 의존성 설치

```bash
pip install -r requirements.txt
```

4. 환경 변수 설정

`.env` 파일을 수정하여 API 키와 데이터베이스 연결 정보를 설정합니다.

```
# API 키
KAKAO_API_KEY=your_kakao_api_key_here
TASHU_API_KEY=your_tashu_api_key_here
DURUNUBI_API_KEY=your_durunubi_api_key_here

# 데이터베이스 설정
DATABASE_URL=postgresql://username:password@localhost:5432/map_integration_db

# 보안 설정
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. 데이터베이스 마이그레이션

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

6. 서버 실행

```bash
uvicorn app.main:app --reload
```

서버가 실행되면 `http://localhost:8000`에서 API를 사용할 수 있습니다.
API 문서는 `http://localhost:8000/docs`에서 확인할 수 있습니다.

## API 엔드포인트

### 인증

- `POST /api/v1/auth/register`: 회원가입
- `POST /api/v1/auth/login`: 로그인 및 토큰 발급

### 지도

- `GET /api/v1/map/search/keyword`: 키워드로 장소 검색
- `GET /api/v1/map/search/category`: 카테고리로 장소 검색
- `GET /api/v1/map/address`: 좌표로 주소 검색
- `GET /api/v1/map/coordinates`: 주소로 좌표 검색

### 타슈

- `GET /api/v1/tashu/stations`: 타슈 대여소 목록 조회
- `GET /api/v1/tashu/stations/{station_id}`: 타슈 대여소 상세 정보 조회
- `GET /api/v1/tashu/stations/{station_id}/bikes`: 대여소별 자전거 이용 가능 여부 조회

### 두루누비

- `GET /api/v1/durunubi/bike/routes`: 자전거 도로 정보 조회
- `GET /api/v1/durunubi/bike/facilities`: 자전거 시설물 정보 조회
- `GET /api/v1/durunubi/walking/routes`: 보행로 정보 조회
- `GET /api/v1/durunubi/route/{route_id}`: 경로 상세 정보 조회

### 위치

- `GET /api/v1/locations`: 위치 정보 목록 조회
- `POST /api/v1/locations`: 새 위치 정보 생성
- `GET /api/v1/locations/{location_id}`: 위치 정보 상세 조회
- `PUT /api/v1/locations/{location_id}`: 위치 정보 업데이트
- `DELETE /api/v1/locations/{location_id}`: 위치 정보 삭제
- `GET /api/v1/locations/nearby`: 주변 위치 정보 조회

### 즐겨찾기

- `GET /api/v1/favorites`: 즐겨찾기 목록 조회
- `POST /api/v1/favorites`: 새 즐겨찾기 생성
- `GET /api/v1/favorites/{favorite_id}`: 즐겨찾기 상세 조회
- `PUT /api/v1/favorites/{favorite_id}`: 즐겨찾기 업데이트
- `DELETE /api/v1/favorites/{favorite_id}`: 즐겨찾기 삭제

### 네비게이션

- `POST /api/v1/navigation/directions/car`: 자동차 길찾기
- `POST /api/v1/navigation/directions/bike`: 자전거 길찾기
- `POST /api/v1/navigation/directions/pedestrian`: 보행자 길찾기

### 자전거 대여

- `GET /api/v1/rentals`: 대여 이력 조회
- `POST /api/v1/rentals`: 자전거 대여
- `GET /api/v1/rentals/active`: 현재 대여 중인 자전거 정보 조회
- `PUT /api/v1/rentals/{rental_id}/return`: 자전거 반납
- `PUT /api/v1/rentals/{rental_id}/cancel`: 대여 취소

## 개발 단계

1. **프로젝트 설계**
   - 요구사항 분석
   - API 설계
   - 데이터베이스 스키마 설계

2. **백엔드 개발**
   - FastAPI 프로젝트 구조 설정
   - 데이터베이스 모델 구현
   - API 서비스 구현
   - 인증 시스템 구현
   - 외부 API 통합

3. **AI 기반 추천 시스템 개발** (진행 중)
   - 사용자 선호도 분석
   - 최적 경로 추천 알고리즘
      - CCH(Customizable Contraction Hierarchies) 알고리즘 구현 완료
      - 경로 탐색 알고리즘 최적화 및 디버깅 완료
      - 샘플 데이터를 활용한 경로 탐색 테스트 완료
   - 날씨, 교통 상황 등 외부 요인 고려
   - 개인화된 자전거 코스 추천

4. **프론트엔드 개발** (리액트 네이티브)
   - 화면 설계
   - 컴포넌트 구현
   - 상태 관리
   - API 연동

5. **테스트 및 배포**
   - 단위 테스트
   - 통합 테스트
   - 배포 환경 설정

## 향후 계획

1. **AI 기반 경로 추천 시스템**
   - 사용자 이용 패턴 분석을 통한 맞춤형 경로 추천
   - 날씨, 시간대, 교통 상황을 고려한 최적 경로 제안
   - 사용자 피드백을 통한 추천 알고리즘 개선

2. **실시간 데이터 통합**
   - 실시간 교통 정보 연동
   - 날씨 API 통합
   - 대여소별 자전거 이용 가능 여부 실시간 업데이트

3. **커뮤니티 기능**
   - 사용자 경로 공유
   - 리뷰 및 평점 시스템
   - 그룹 라이딩 기능

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.
