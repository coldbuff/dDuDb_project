from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.favorite import Favorite as FavoriteModel
from app.db.models.location import Location as LocationModel
from app.schemas.favorite import Favorite, FavoriteCreate, FavoriteUpdate, FavoriteWithLocation
from app.api.dependencies import get_current_user
from app.db.models.user import User

router = APIRouter()

@router.get("", response_model=List[FavoriteWithLocation])
def get_user_favorites(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    현재 사용자의 즐겨찾기 목록 조회
    """
    favorites = (
        db.query(FavoriteModel)
        .filter(FavoriteModel.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # 위치 정보와 함께 반환
    result = []
    for fav in favorites:
        location = db.query(LocationModel).filter(LocationModel.id == fav.location_id).first()
        if location:
            result.append({
                "id": fav.id,
                "user_id": fav.user_id,
                "location_id": fav.location_id,
                "memo": fav.memo,
                "created_at": fav.created_at,
                "location": location
            })
    
    return result

@router.post("", response_model=Favorite)
def create_favorite(
    favorite: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    새 즐겨찾기 생성
    """
    # 위치 존재 여부 확인
    location = db.query(LocationModel).filter(LocationModel.id == favorite.location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail=f"ID가 {favorite.location_id}인 위치를 찾을 수 없습니다")
    
    # 이미 즐겨찾기에 추가되어 있는지 확인
    existing_favorite = (
        db.query(FavoriteModel)
        .filter(
            FavoriteModel.user_id == current_user.id,
            FavoriteModel.location_id == favorite.location_id
        )
        .first()
    )
    
    if existing_favorite:
        raise HTTPException(status_code=400, detail="이미 즐겨찾기에 추가된 위치입니다")
    
    # 새 즐겨찾기 생성
    db_favorite = FavoriteModel(
        user_id=current_user.id,
        location_id=favorite.location_id,
        memo=favorite.memo
    )
    
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    
    return db_favorite

@router.get("/{favorite_id}", response_model=FavoriteWithLocation)
def get_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    즐겨찾기 상세 조회
    """
    favorite = (
        db.query(FavoriteModel)
        .filter(
            FavoriteModel.id == favorite_id,
            FavoriteModel.user_id == current_user.id
        )
        .first()
    )
    
    if not favorite:
        raise HTTPException(status_code=404, detail=f"ID가 {favorite_id}인 즐겨찾기를 찾을 수 없습니다")
    
    # 위치 정보 가져오기
    location = db.query(LocationModel).filter(LocationModel.id == favorite.location_id).first()
    
    return {
        "id": favorite.id,
        "user_id": favorite.user_id,
        "location_id": favorite.location_id,
        "memo": favorite.memo,
        "created_at": favorite.created_at,
        "location": location
    }

@router.put("/{favorite_id}", response_model=Favorite)
def update_favorite(
    favorite_id: int,
    favorite_update: FavoriteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    즐겨찾기 업데이트
    """
    favorite = (
        db.query(FavoriteModel)
        .filter(
            FavoriteModel.id == favorite_id,
            FavoriteModel.user_id == current_user.id
        )
        .first()
    )
    
    if not favorite:
        raise HTTPException(status_code=404, detail=f"ID가 {favorite_id}인 즐겨찾기를 찾을 수 없습니다")
    
    # 업데이트할 필드 설정
    update_data = favorite_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(favorite, key, value)
    
    db.commit()
    db.refresh(favorite)
    
    return favorite

@router.delete("/{favorite_id}")
def delete_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    즐겨찾기 삭제
    """
    favorite = (
        db.query(FavoriteModel)
        .filter(
            FavoriteModel.id == favorite_id,
            FavoriteModel.user_id == current_user.id
        )
        .first()
    )
    
    if not favorite:
        raise HTTPException(status_code=404, detail=f"ID가 {favorite_id}인 즐겨찾기를 찾을 수 없습니다")
    
    db.delete(favorite)
    db.commit()
    
    return {"detail": "즐겨찾기가 삭제되었습니다"}
