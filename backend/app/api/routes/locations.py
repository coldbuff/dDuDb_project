from fastapi import APIRouter, Depends, HTTPException, Query, Body
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.location import Location as LocationModel, LocationType
from app.schemas.location import Location, LocationCreate, LocationUpdate, LocationList
from app.api.dependencies import get_current_user
from app.db.models.user import User

router = APIRouter()

@router.get("", response_model=LocationList)
def get_locations(
    skip: int = 0,
    limit: int = 100,
    location_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    위치 정보 목록 조회
    """
    query = db.query(LocationModel)
    
    # 위치 유형으로 필터링
    if location_type:
        try:
            type_enum = LocationType[location_type.upper()]
            query = query.filter(LocationModel.type == type_enum)
        except KeyError:
            raise HTTPException(status_code=400, detail=f"유효하지 않은 위치 유형: {location_type}")
    
    # 전체 개수 계산
    total = query.count()
    
    # 페이지네이션 적용
    locations = query.offset(skip).limit(limit).all()
    
    return {"total": total, "items": locations}

@router.post("", response_model=Location)
def create_location(
    location: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    새 위치 정보 생성
    """
    # 위치 유형 확인
    try:
        location_type = LocationType[location.type.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"유효하지 않은 위치 유형: {location.type}")
    
    # 새 위치 정보 생성
    db_location = LocationModel(
        name=location.name,
        latitude=location.latitude,
        longitude=location.longitude,
        address=location.address,
        type=location_type,
        external_id=location.external_id,
        details=location.details
    )
    
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    
    return db_location

@router.get("/{location_id}", response_model=Location)
def get_location(
    location_id: int,
    db: Session = Depends(get_db)
):
    """
    위치 정보 상세 조회
    """
    location = db.query(LocationModel).filter(LocationModel.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail=f"ID가 {location_id}인 위치를 찾을 수 없습니다")
    
    return location

@router.put("/{location_id}", response_model=Location)
def update_location(
    location_id: int,
    location_update: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    위치 정보 업데이트
    """
    db_location = db.query(LocationModel).filter(LocationModel.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail=f"ID가 {location_id}인 위치를 찾을 수 없습니다")
    
    # 업데이트할 필드 설정
    update_data = location_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_location, key, value)
    
    db.commit()
    db.refresh(db_location)
    
    return db_location

@router.delete("/{location_id}")
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    위치 정보 삭제
    """
    db_location = db.query(LocationModel).filter(LocationModel.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail=f"ID가 {location_id}인 위치를 찾을 수 없습니다")
    
    db.delete(db_location)
    db.commit()
    
    return {"detail": "위치 정보가 삭제되었습니다"}

@router.get("/nearby", response_model=LocationList)
def get_nearby_locations(
    latitude: float,
    longitude: float,
    radius: float = Query(1000, ge=0),  # 미터 단위
    location_type: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    주변 위치 정보 조회 (거리 기반)
    
    참고: 실제 구현에서는 PostgreSQL의 PostGIS 확장을 사용하거나
    Haversine 공식을 사용하여 거리 계산을 구현해야 합니다.
    여기서는 간단한 예시만 제공합니다.
    """
    # 여기에 거리 기반 쿼리 구현
    # 예시: PostgreSQL + PostGIS를 사용한 쿼리
    # query = db.query(LocationModel).filter(
    #     func.ST_DWithin(
    #         func.ST_SetSRID(func.ST_MakePoint(LocationModel.longitude, LocationModel.latitude), 4326),
    #         func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326),
    #         radius / 111320  # 미터를 대략적인 도(degree)로 변환
    #     )
    # )
    
    # 간단한 구현을 위해 모든 위치를 가져와서 Python에서 필터링
    # 실제 프로덕션에서는 데이터베이스 수준에서 필터링하는 것이 좋습니다
    locations = db.query(LocationModel).all()
    
    # 위치 유형으로 필터링
    if location_type:
        try:
            type_enum = LocationType[location_type.upper()]
            locations = [loc for loc in locations if loc.type == type_enum]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"유효하지 않은 위치 유형: {location_type}")
    
    # 거리 계산 및 필터링 (간단한 구현)
    # 실제로는 Haversine 공식을 사용하여 정확한 거리 계산 필요
    nearby_locations = []
    for loc in locations:
        # 간단한 거리 계산 (실제 구현에서는 Haversine 공식 사용)
        distance = ((loc.latitude - latitude) ** 2 + (loc.longitude - longitude) ** 2) ** 0.5 * 111320  # 대략적인 미터 변환
        if distance <= radius:
            nearby_locations.append(loc)
    
    # 거리순으로 정렬
    nearby_locations.sort(key=lambda loc: ((loc.latitude - latitude) ** 2 + (loc.longitude - longitude) ** 2))
    
    # 개수 제한
    nearby_locations = nearby_locations[:limit]
    
    return {"total": len(nearby_locations), "items": nearby_locations}
