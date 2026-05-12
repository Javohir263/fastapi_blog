from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db


router = APIRouter(
    tags=["Authentication"]
)


# ─────────────────────────────
# LOGIN
# ─────────────────────────────
@router.post(
    "/login",
    response_model=schemas.Token
)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # USERNI TOPISH
    user = db.query(models.User).filter(
        models.User.username == user_credentials.username
    ).first()

    # USER YO'Q BO'LSA
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Noto'g'ri username yoki parol"
        )

    # PAROLNI TEKSHIRISH
    if not utils.verify(
        user_credentials.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Noto'g'ri username yoki parol"
        )

    # ACCESS TOKEN YARATISH
    access_token = oauth2.create_access_token(
        data={"user_id": user.id}
    )

    # REFRESH TOKEN YARATISH
    refresh_token = oauth2.create_refresh_token(
        data={"user_id": user.id}
    )

    # TOKENLARNI QAYTARISH
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# ─────────────────────────────
# REFRESH TOKEN
# ─────────────────────────────
@router.post(
    "/refresh",
    response_model=schemas.AccessTokenResponse
)
def refresh_token(
    token_data: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    # REFRESH TOKENNI TEKSHIRISH
    token = oauth2.verify_refresh_token(
        token_data.refresh_token
    )

    # USERNI DB DAN TOPISH
    user = db.query(models.User).filter(
        models.User.id == token.id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User topilmadi"
        )

    # YANGI ACCESS TOKEN YARATISH
    new_access_token = oauth2.create_access_token(
        data={"user_id": user.id}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


# ─────────────────────────────
# LOGOUT
# ─────────────────────────────
@router.post("/logout")
def logout():
    return {
        "message": "JWT stateless. Logout client tarafda qilinadi: access_token va refresh_token localStorage/cookie/session dan o'chiriladi."
    }