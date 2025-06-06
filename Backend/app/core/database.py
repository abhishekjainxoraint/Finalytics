from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from loguru import logger
from typing import Optional

from app.core.config import settings


class Database:
    client: Optional[AsyncIOMotorClient] = None
    database = None


db = Database()


async def connect_to_mongo():
    """Create database connection"""
    if settings.DISABLE_DATABASE:
        logger.warning("🔄 Database disabled in development mode - using mock data")
        return
        
    try:
        logger.info("🔄 Connecting to MongoDB...")
        db.client = AsyncIOMotorClient(settings.MONGODB_URI)
        
        # Test the connection
        await db.client.admin.command('ping')
        
        db.database = db.client[settings.DATABASE_NAME]
        logger.info(f"✅ Connected to MongoDB: {settings.DATABASE_NAME}")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        if settings.ENVIRONMENT == "development":
            logger.warning("🔄 Running in development mode without database - using mock data")
            settings.DISABLE_DATABASE = True
            return
        raise


async def close_mongo_connection():
    """Close database connection"""
    if settings.DISABLE_DATABASE or not db.client:
        return
        
    try:
        if db.client:
            db.client.close()
            logger.info("✅ MongoDB connection closed")
    except Exception as e:
        logger.error(f"❌ Error closing MongoDB connection: {e}")


async def create_indexes():
    """Create database indexes for optimal performance"""
    if settings.DISABLE_DATABASE or not db.database:
        return
        
    try:
        # Users collection indexes
        await db.database.users.create_index("email", unique=True)
        await db.database.users.create_index("username", unique=True)
        await db.database.users.create_index("created_at")
        
        # Analyses collection indexes
        await db.database.analyses.create_index("user_id")
        await db.database.analyses.create_index("created_at")
        await db.database.analyses.create_index("status")
        await db.database.analyses.create_index([("name", "text"), ("description", "text")])
        
        # Market research questions indexes
        await db.database.market_questions.create_index("user_id")
        await db.database.market_questions.create_index("analysis_id")
        await db.database.market_questions.create_index("status")
        await db.database.market_questions.create_index("created_at")
        
        # Files collection indexes
        await db.database.files.create_index("user_id")
        await db.database.files.create_index("analysis_id")
        await db.database.files.create_index("filename")
        await db.database.files.create_index("upload_date")
        
        logger.info("✅ Database indexes created successfully")
        
    except Exception as e:
        logger.error(f"❌ Error creating indexes: {e}")


def get_database():
    """Get database instance"""
    if settings.DISABLE_DATABASE:
        # Import here to avoid circular imports
        from app.core.mock_data import mock_data_service
        return mock_data_service
    return db.database


async def get_collection(collection_name: str):
    """Get a specific collection"""
    if settings.DISABLE_DATABASE or not db.database:
        return None
    return db.database[collection_name]


# Using mock_data_service for mocked data when database is disabled 