from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# =========================================
# CREATE USER
# =========================================
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponse
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    # HASH PASSWORD
    hashed_password = utils.hash(user.password)

    user.password = hashed_password

    # CREATE USER
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================================
# GET CURRENT USER
# =========================================
@router.get(
    "/me",
    response_model=schemas.UserResponse
)
def get_current_user_info(
    current_user: models.User = Depends(
        oauth2.get_current_user
    )
):
    return current_user


# =========================================
# CHANGE PASSWORD
# =========================================
@router.put("/me/password")
def change_password(
    passwords: schemas.PasswordChange,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        oauth2.get_current_user
    )
):
    # CHECK OLD PASSWORD
    if not utils.verify(
        passwords.old_password,
        current_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect"
        )

    # HASH NEW PASSWORD
    hashed_password = utils.hash(
        passwords.new_password
    )

    # UPDATE PASSWORD
    current_user.password = hashed_password

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Password changed successfully"
    }
    