from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


# ─────────────────────────────
# CREATE CATEGORY
# ─────────────────────────────
@router.post(
    "/",
    response_model=schemas.CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    # Duplicate category name tekshirish
    existing_category = db.query(models.Category).filter(
        models.Category.name == category.name
    ).first()

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bunday category allaqachon mavjud"
        )

    new_category = models.Category(**category.model_dump())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


# ─────────────────────────────
# GET ALL CATEGORIES
# ─────────────────────────────
@router.get(
    "/",
    response_model=List[schemas.CategoryResponse]
)
def get_categories(
    db: Session = Depends(get_db)
):
    categories = db.query(models.Category).all()
    return categories


# ─────────────────────────────
# GET SINGLE CATEGORY
# ─────────────────────────────
@router.get(
    "/{category_id}",
    response_model=schemas.CategoryResponse
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category topilmadi"
        )

    return category


# ─────────────────────────────
# UPDATE CATEGORY
# ─────────────────────────────
@router.put(
    "/{category_id}",
    response_model=schemas.CategoryResponse
)
def update_category(
    category_id: int,
    updated_category: schemas.CategoryUpdate,
    db: Session = Depends(get_db)
):
    category_query = db.query(models.Category).filter(
        models.Category.id == category_id
    )

    category = category_query.first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category topilmadi"
        )

    # Duplicate name tekshirish
    duplicate_category = db.query(models.Category).filter(
        models.Category.name == updated_category.name,
        models.Category.id != category_id
    ).first()

    if duplicate_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bunday category nomi mavjud"
        )

    category_query.update(
        updated_category.model_dump(),
        synchronize_session=False
    )

    db.commit()

    return category_query.first()


# ─────────────────────────────
# DELETE CATEGORY
# ─────────────────────────────
@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category_query = db.query(models.Category).filter(
        models.Category.id == category_id
    )

    category = category_query.first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category topilmadi"
        )

    category_query.delete(synchronize_session=False)
    db.commit()

    return None