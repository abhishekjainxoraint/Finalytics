from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional, List
from datetime import datetime
import math

from app.core.database import get_database
from app.core.security import get_current_admin_user, get_password_hash
from app.models.user import (
    User,
    UserResponse,
    UserUpdate,
    UserRole
)

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    role: Optional[UserRole] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_current_admin_user)
):
    """Get all users (admin only)"""
    db = get_database()
    
    # Build query
    query = {}
    
    if search:
        query["$or"] = [
            {"username": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
            {"full_name": {"$regex": search, "$options": "i"}}
        ]
    
    if role:
        query["role"] = role
    
    if is_active is not None:
        query["is_active"] = is_active
    
    # Calculate pagination
    skip = (page - 1) * size
    
    # Get users
    cursor = db.users.find(query, {"hashed_password": 0}).skip(skip).limit(size)
    users = await cursor.to_list(length=size)
    
    # Convert to response models
    return [UserResponse(**user) for user in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_admin_user)
):
    """Get a specific user (admin only)"""
    db = get_database()
    
    user = await db.users.find_one({"_id": user_id}, {"hashed_password": 0})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(**user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_admin_user)
):
    """Update a user (admin only)"""
    db = get_database()
    
    # Check if user exists
    existing_user = await db.users.find_one({"_id": user_id})
    
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Build update data
    update_data = {"updated_at": datetime.utcnow()}
    
    if user_data.username is not None:
        # Check if username is already taken
        username_exists = await db.users.find_one({
            "username": user_data.username,
            "_id": {"$ne": user_id}
        })
        if username_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        update_data["username"] = user_data.username
    
    if user_data.email is not None:
        # Check if email is already taken
        email_exists = await db.users.find_one({
            "email": user_data.email,
            "_id": {"$ne": user_id}
        })
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        update_data["email"] = user_data.email
    
    if user_data.full_name is not None:
        update_data["full_name"] = user_data.full_name
    if user_data.role is not None:
        update_data["role"] = user_data.role
    if user_data.is_active is not None:
        update_data["is_active"] = user_data.is_active
    
    # Update user
    await db.users.update_one(
        {"_id": user_id},
        {"$set": update_data}
    )
    
    # Get updated user
    updated_user = await db.users.find_one({"_id": user_id}, {"hashed_password": 0})
    
    return UserResponse(**updated_user)


@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a user (admin only)"""
    db = get_database()
    
    # Check if user exists
    user = await db.users.find_one({"_id": user_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent self-deletion
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Delete user
    await db.users.delete_one({"_id": user_id})
    
    # Delete user's analyses and questions
    await db.analyses.delete_many({"user_id": user_id})
    await db.market_questions.delete_many({"user_id": user_id})
    
    return {"message": "User deleted successfully"} 