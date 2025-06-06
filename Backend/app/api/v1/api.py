from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, analyses, market_research, files


api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(analyses.router, prefix="/analyses", tags=["analyses"])
api_router.include_router(market_research.router, prefix="/market-research", tags=["market-research"])
api_router.include_router(files.router, prefix="/files", tags=["files"]) 