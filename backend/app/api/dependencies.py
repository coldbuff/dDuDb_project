from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Generator, Optional

from app.core.config import settings
from app.db.session import get_db
from app.services.kakao_map import KakaoMapService
from app.services.tashu import TashuService
from app.services.durunubi import DurunubiService
from app.services.navigation import NavigationService
from app.schemas.user import TokenPayload
from app.db.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_kakao_map_service() -> KakaoMapService:
    return KakaoMapService()

def get_tashu_service() -> TashuService:
    return TashuService()

def get_durunubi_service() -> DurunubiService:
    return DurunubiService()

def get_navigation_service() -> NavigationService:
    return NavigationService()

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    현재 인증된 사용자 가져오기
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증할 수 없습니다",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenPayload(sub=user_id)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == token_data.sub).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="비활성화된 사용자입니다")
    return user
