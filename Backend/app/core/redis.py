import redis.asyncio as redis
from loguru import logger
from typing import Optional, Any
import json
import pickle
from datetime import timedelta

from app.core.config import settings


class RedisManager:
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Connect to Redis"""
        if settings.DISABLE_REDIS:
            logger.warning("🔄 Redis disabled in development mode")
            return
            
        try:
            logger.info("🔄 Connecting to Redis...")
            
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
                password=settings.REDIS_PASSWORD
            )
            
            # Test connection
            await self.redis_client.ping()
            logger.info("✅ Connected to Redis successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to Redis: {e}")
            if settings.ENVIRONMENT == "development":
                logger.warning("🔄 Running in development mode without Redis")
                settings.DISABLE_REDIS = True
                return
            raise
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if settings.DISABLE_REDIS or not self.redis_client:
            return
            
        try:
            if self.redis_client:
                await self.redis_client.close()
                logger.info("✅ Redis connection closed")
        except Exception as e:
            logger.error(f"❌ Error closing Redis connection: {e}")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value by key"""
        if settings.DISABLE_REDIS:
            return None
            
        try:
            if not self.redis_client:
                return None
            
            value = await self.redis_client.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None
        except Exception as e:
            logger.error(f"❌ Redis GET error for key {key}: {e}")
            return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        expire: Optional[int] = None
    ) -> bool:
        """Set key-value pair with optional expiration"""
        if settings.DISABLE_REDIS:
            return True  # Return True to avoid breaking the app
            
        try:
            if not self.redis_client:
                return False
            
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            if expire:
                await self.redis_client.setex(key, expire, value)
            else:
                await self.redis_client.set(key, value)
            
            return True
        except Exception as e:
            logger.error(f"❌ Redis SET error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key"""
        if settings.DISABLE_REDIS:
            return True
            
        try:
            if not self.redis_client:
                return False
            
            result = await self.redis_client.delete(key)
            return bool(result)
        except Exception as e:
            logger.error(f"❌ Redis DELETE error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if settings.DISABLE_REDIS:
            return False
            
        try:
            if not self.redis_client:
                return False
            
            result = await self.redis_client.exists(key)
            return bool(result)
        except Exception as e:
            logger.error(f"❌ Redis EXISTS error for key {key}: {e}")
            return False
    
    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment counter"""
        if settings.DISABLE_REDIS:
            return amount
            
        try:
            if not self.redis_client:
                return None
            
            result = await self.redis_client.incrby(key, amount)
            return result
        except Exception as e:
            logger.error(f"❌ Redis INCREMENT error for key {key}: {e}")
            return None
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration for key"""
        if settings.DISABLE_REDIS:
            return True
            
        try:
            if not self.redis_client:
                return False
            
            result = await self.redis_client.expire(key, seconds)
            return bool(result)
        except Exception as e:
            logger.error(f"❌ Redis EXPIRE error for key {key}: {e}")
            return False
    
    async def flush_all(self) -> bool:
        """Clear all data (use with caution!)"""
        if settings.DISABLE_REDIS:
            return True
            
        try:
            if not self.redis_client:
                return False
            
            await self.redis_client.flushall()
            return True
        except Exception as e:
            logger.error(f"❌ Redis FLUSHALL error: {e}")
            return False


# Global Redis manager instance
redis_manager = RedisManager()


async def connect_to_redis():
    """Connect to Redis"""
    await redis_manager.connect()


async def close_redis_connection():
    """Close Redis connection"""
    await redis_manager.disconnect()


def get_redis_client():
    """Get Redis client instance"""
    return redis_manager


# Convenience functions
async def cache_get(key: str) -> Optional[Any]:
    """Get cached value"""
    return await redis_manager.get(key)


async def cache_set(key: str, value: Any, expire: int = settings.CACHE_TTL) -> bool:
    """Set cached value"""
    return await redis_manager.set(key, value, expire)


async def cache_delete(key: str) -> bool:
    """Delete cached value"""
    return await redis_manager.delete(key)


async def cache_key_exists(key: str) -> bool:
    """Check if cache key exists"""
    return await redis_manager.exists(key) 