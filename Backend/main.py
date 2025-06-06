import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import uvicorn
from loguru import logger
import os

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.redis import connect_to_redis, close_redis_connection
from app.api.v1.api import api_router
from app.core.security import get_current_user


# Rate limiter
limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting FP&A Analysis Backend")
    await connect_to_mongo()
    await connect_to_redis()
    logger.info("✅ Backend startup complete")
    
    yield
    
    # Shutdown
    logger.info("🔄 Shutting down backend")
    await close_mongo_connection()
    await close_redis_connection()
    logger.info("✅ Backend shutdown complete")


app = FastAPI(
    title="FP&A Intelligence API",
    description="Banking Analysis Platform - Competitive Intelligence & Financial Analytics",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    lifespan=lifespan
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=settings.ALLOWED_HOSTS
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Static files
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "FP&A Intelligence API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs" if settings.ENVIRONMENT == "development" else "Documentation disabled in production",
        "environment": settings.ENVIRONMENT,
        "database_enabled": not settings.DISABLE_DATABASE,
        "redis_enabled": not settings.DISABLE_REDIS
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "timestamp": "2024-01-01T00:00:00Z",
        "database": "connected" if not settings.DISABLE_DATABASE else "disabled",
        "redis": "connected" if not settings.DISABLE_REDIS else "disabled"
    }

# Development demo endpoints (no auth required)
if settings.ENVIRONMENT == "development":
    @app.get("/demo/analyses")
    async def demo_analyses():
        """Demo analyses endpoint without authentication"""
        return {
            "analyses": [
                {
                    "id": "demo-1",
                    "name": "Q4 2024 Banking Analysis",
                    "description": "Comprehensive analysis of Q4 2024 banking performance",
                    "period": "Q4 2024",
                    "status": "completed",
                    "created_at": "2024-01-01T10:00:00Z",
                    "updated_at": "2024-01-01T15:00:00Z",
                    "competitors": ["Bank of America", "Wells Fargo", "JPMorgan Chase"]
                },
                {
                    "id": "demo-2", 
                    "name": "Market Research Analysis",
                    "description": "Market trends and competitive intelligence",
                    "period": "Q1 2024",
                    "status": "in-progress",
                    "created_at": "2024-01-15T09:00:00Z",
                    "updated_at": "2024-01-20T14:30:00Z",
                    "competitors": ["Citibank", "Goldman Sachs"]
                }
            ],
            "total": 2,
            "page": 1,
            "size": 10,
            "pages": 1
        }

    @app.get("/demo/market-research")
    async def demo_market_research():
        """Demo market research endpoint without authentication"""
        return {
            "questions": [
                {
                    "id": "demo-q1",
                    "analysis_id": "demo-1",
                    "analysis_name": "Q4 2024 Banking Analysis",
                    "dashboard": "Financial Performance",
                    "report": "Income Statement",
                    "question": "What are the key revenue drivers for our competitors?",
                    "status": "answered",
                    "created_at": "2024-01-01T11:00:00Z",
                    "responses": [
                        {
                            "analyst": "Sarah Johnson",
                            "response": "Based on the Q4 reports, key revenue drivers include digital banking fees, loan origination, and investment services.",
                            "timestamp": "2024-01-01T14:00:00Z"
                        }
                    ]
                },
                {
                    "id": "demo-q2",
                    "analysis_id": "demo-2",
                    "analysis_name": "Market Research Analysis", 
                    "dashboard": "Market Trends",
                    "report": "Competitive Analysis",
                    "question": "How do our interest rates compare to market leaders?",
                    "status": "pending",
                    "created_at": "2024-01-15T10:00:00Z",
                    "responses": []
                }
            ],
            "total": 2,
            "page": 1,
            "size": 10,
            "pages": 1
        }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level="info"
    ) 