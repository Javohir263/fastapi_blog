from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# =========================================================
# CATEGORY SCHEMAS
# =========================================================

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# =========================================================
# USER SCHEMAS
# =========================================================

class UserBase(BaseModel):
    username: str = Field(..., max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# =========================================================
# PASSWORD CHANGE
# =========================================================

class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)


# =========================================================
# OWNER INFO
# =========================================================

class OwnerInfo(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


# =========================================================
# POST SCHEMAS
# =========================================================

class PostBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    published: bool = True
    rating: Optional[int] = None
    category_id: Optional[int] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    published: Optional[bool] = None
    rating: Optional[int] = None
    category_id: Optional[int] = None


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    rating: Optional[int] = None
    category_id: Optional[int] = None
    owner_id: int
    created_at: datetime

    owner: Optional[OwnerInfo] = None
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True


# =========================================================
# ONLY MY POSTS
# =========================================================

class MyPostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    rating: Optional[int] = None
    category_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# =========================================================
# AUTH SCHEMAS
# =========================================================

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None