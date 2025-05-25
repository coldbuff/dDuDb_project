from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from app.db.session import get_db
from app.db.models.rental import Rental as RentalModel, RentalStatus
from app.schemas.rental import Rental, RentalCreate, RentalUpdate, RentalList
from app.api.dependencies import get_current_user, get_tashu_service
from app.db.models.user import User
from app.services.tashu import TashuService

router = APIRouter()

@router.get("", response_model=RentalList)
async def get_user_rentals(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    현재 사용자의 대여 이력 조회
    """
    query = db.query(RentalModel).filter(RentalModel.user_id == current_user.id)
    
    # 상태로 필터링
    if status:
        try:
            status_enum = RentalStatus[status.upper()]
            query = query.filter(RentalModel.status == status_enum)
        except KeyError:
            raise HTTPException(status_code=400, detail=f"유효하지 않은 대여 상태: {status}")
    
    # 전체 개수 계산
    total = query.count()
    
    # 페이지네이션 적용 및 최신순 정렬
    rentals = query.order_by(RentalModel.rental_time.desc()).offset(skip).limit(limit).all()
    
    return {"total": total, "items": rentals}

@router.post("", response_model=Rental)
async def create_rental(
    station_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tashu_service: TashuService = Depends(get_tashu_service)
):
    """
    새 자전거 대여
    """
    # 대여소 정보 확인
    station = await tashu_service.get_station_detail(station_id)
    if not station:
        raise HTTPException(status_code=404, detail=f"ID가 {station_id}인 대여소를 찾을 수 없습니다")
    
    # 사용 가능한 자전거 확인
    bikes_info = await tashu_service.get_available_bikes(station_id)
    if not bikes_info or bikes_info.get("available_bikes", 0) <= 0:
        raise HTTPException(status_code=400, detail="현재 대여 가능한 자전거가 없습니다")
    
    # 이미 활성화된 대여가 있는지 확인
    active_rental = db.query(RentalModel).filter(
        RentalModel.user_id == current_user.id,
        RentalModel.status == RentalStatus.ACTIVE
    ).first()
    
    if active_rental:
        raise HTTPException(
            status_code=400, 
            detail="이미 대여 중인 자전거가 있습니다. 먼저 반납해주세요."
        )
    
    # 자전거 ID 생성 (실제로는 API에서 받아와야 함)
    bike_id = f"BIKE_{random.randint(1000, 9999)}"
    
    # 새 대여 생성
    db_rental = RentalModel(
        user_id=current_user.id,
        station_id=station_id,
        bike_id=bike_id,
        status=RentalStatus.ACTIVE
    )
    
    db.add(db_rental)
    db.commit()
    db.refresh(db_rental)
    
    return db_rental

@router.get("/active", response_model=Rental)
async def get_active_rental(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    현재 활성화된 대여 정보 조회
    """
    active_rental = db.query(RentalModel).filter(
        RentalModel.user_id == current_user.id,
        RentalModel.status == RentalStatus.ACTIVE
    ).first()
    
    if not active_rental:
        raise HTTPException(status_code=404, detail="현재 대여 중인 자전거가 없습니다")
    
    return active_rental

@router.put("/{rental_id}/return", response_model=Rental)
async def return_bike(
    rental_id: int = Path(..., title="대여 ID"),
    return_station_id: str = Query(..., title="반납 대여소 ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tashu_service: TashuService = Depends(get_tashu_service)
):
    """
    자전거 반납
    """
    # 대여 정보 확인
    rental = db.query(RentalModel).filter(
        RentalModel.id == rental_id,
        RentalModel.user_id == current_user.id,
        RentalModel.status == RentalStatus.ACTIVE
    ).first()
    
    if not rental:
        raise HTTPException(status_code=404, detail=f"ID가 {rental_id}인 활성 대여를 찾을 수 없습니다")
    
    # 반납 대여소 확인
    return_station = await tashu_service.get_station_detail(return_station_id)
    if not return_station:
        raise HTTPException(status_code=404, detail=f"ID가 {return_station_id}인 대여소를 찾을 수 없습니다")
    
    # 이용 시간 계산
    rental_time = rental.rental_time
    return_time = datetime.now()
    duration_minutes = (return_time - rental_time).total_seconds() / 60
    
    # 요금 계산 (예: 기본 30분 1,000원, 추가 10분당 500원)
    base_fee = 1000  # 기본 요금
    additional_fee = max(0, int((duration_minutes - 30) / 10)) * 500  # 추가 요금
    total_fee = base_fee + additional_fee
    
    # 대여 정보 업데이트
    rental.return_station_id = return_station_id
    rental.return_time = return_time
    rental.status = RentalStatus.COMPLETED
    rental.cost = total_fee
    
    db.commit()
    db.refresh(rental)
    
    return rental

@router.put("/{rental_id}/cancel", response_model=Rental)
async def cancel_rental(
    rental_id: int = Path(..., title="대여 ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    자전거 대여 취소
    """
    # 대여 정보 확인
    rental = db.query(RentalModel).filter(
        RentalModel.id == rental_id,
        RentalModel.user_id == current_user.id,
        RentalModel.status == RentalStatus.ACTIVE
    ).first()
    
    if not rental:
        raise HTTPException(status_code=404, detail=f"ID가 {rental_id}인 활성 대여를 찾을 수 없습니다")
    
    # 대여 후 1분 이내인지 확인 (취소 정책)
    rental_time = rental.rental_time
    current_time = datetime.now()
    if (current_time - rental_time).total_seconds() > 60:
        raise HTTPException(status_code=400, detail="대여 후 1분이 지나 취소할 수 없습니다")
    
    # 대여 정보 업데이트
    rental.status = RentalStatus.CANCELLED
    rental.return_time = current_time
    rental.cost = 0  # 취소 시 요금 없음
    
    db.commit()
    db.refresh(rental)
    
    return rental
