
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, posts, users


app = FastAPI(
    title="Blog API",
    description="FastAPI + PostgreSQL + JWT + Alembic + CORS",
    version="5.0.0",
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None if settings.is_production else "/redoc",
    openapi_url=None if settings.is_production else "/openapi.json",
)


# =========================================================
# CORS SETTINGS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)


# =========================================================
# ROOT
# =========================================================

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Blog API v5.0 — JWT + Alembic + CORS",
        "version": "5.0.0",
        "environment": settings.environment,
        "docs": None if settings.is_production else "/docs",
        "redoc": None if settings.is_production else "/redoc",
        "status": "running",
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "database": "PostgreSQL",
        "migrations": "Alembic",
        "cors": "enabled",
        "allowed_origins": settings.origins_list,
        "environment": settings.environment,
    }