from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import datetime
import uuid

from app.core.config import settings
from app.core.database import get_database
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_tokens,
    verify_token,
    get_current_active_user
)
from app.models.user import (
    UserCreate, 
    UserResponse, 
    LoginRequest, 
    LoginResponse,
    RefreshTokenRequest,
    PasswordChangeRequest,
    User
)

router = APIRouter()
security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)

# Mock user for development
MOCK_USER = {
    "_id": "mock-user-id",
    "username": "devuser",
    "email": "dev@example.com",
    "full_name": "Development User",
    "role": "admin",
    "is_active": True,
    "hashed_password": get_password_hash("password123"),
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow(),
    "last_login": None
}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(user_data: UserCreate, request=None):
    """Register a new user"""
    if settings.DISABLE_DATABASE:
        # Mock registration - just return success
        return UserResponse(
            id="mock-user-id",
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            role=user_data.role,
            is_active=user_data.is_active,
            created_at=datetime.utcnow(),
            last_login=None
        )
    
    # Database implementation
    db = get_database()
    
    # Check if user already exists
    existing_user = await db.users.find_one({
        "$or": [
            {"email": user_data.email},
            {"username": user_data.username}
        ]
    })
    
    if existing_user:
        if existing_user["email"] == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Create user document
    user_doc = {
        "_id": str(uuid.uuid4()),
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "role": user_data.role,
        "is_active": user_data.is_active,
        "hashed_password": get_password_hash(user_data.password),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "last_login": None
    }
    
    # Insert user
    await db.users.insert_one(user_doc)
    
    # Return user response
    return UserResponse(
        id=user_doc["_id"],
        username=user_doc["username"],
        email=user_doc["email"],
        full_name=user_doc["full_name"],
        role=user_doc["role"],
        is_active=user_doc["is_active"],
        created_at=user_doc["created_at"],
        last_login=user_doc["last_login"]
    )


@router.post("/login", response_model=LoginResponse)
@limiter.limit("10/minute")
async def login(login_data: LoginRequest, request=None):
    """Login user and return tokens"""
    if settings.DISABLE_DATABASE:
        # Mock login - accept any email/password combination for development
        # Create tokens for mock user
        tokens = create_tokens(MOCK_USER["_id"], MOCK_USER["email"])
        
        return LoginResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            token_type=tokens["token_type"],
            user=UserResponse(
                id=MOCK_USER["_id"],
                username=MOCK_USER["username"],
                email=MOCK_USER["email"],
                full_name=MOCK_USER["full_name"],
                role=MOCK_USER["role"],
                is_active=MOCK_USER["is_active"],
                created_at=MOCK_USER["created_at"],
                last_login=datetime.utcnow()
            )
        )
    
    # Database implementation
    db = get_database()
    
    # Find user by email
    user_doc = await db.users.find_one({"email": login_data.email})
    
    if not user_doc or not verify_password(login_data.password, user_doc["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user_doc["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Update last login
    await db.users.update_one(
        {"_id": user_doc["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    
    # Create tokens
    tokens = create_tokens(user_doc["_id"], user_doc["email"])
    
    # Return response
    return LoginResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type=tokens["token_type"],
        user=UserResponse(
            id=user_doc["_id"],
            username=user_doc["username"],
            email=user_doc["email"],
            full_name=user_doc["full_name"],
            role=user_doc["role"],
            is_active=user_doc["is_active"],
            created_at=user_doc["created_at"],
            last_login=datetime.utcnow()
        )
    )


@router.post("/refresh", response_model=dict)
@limiter.limit("20/minute")
async def refresh_token(refresh_data: RefreshTokenRequest, request=None):
    """Refresh access token using refresh token"""
    
    # Verify refresh token
    payload = verify_token(refresh_data.refresh_token, "refresh")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Get user info
    user_id = payload.get("sub")
    email = payload.get("email")
    
    if not user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    if settings.DISABLE_DATABASE:
        # For development, just create new tokens
        tokens = create_tokens(user_id, email)
        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": tokens["token_type"]
        }
    
    # Verify user exists and is active
    db = get_database()
    user_doc = await db.users.find_one({"_id": user_id, "is_active": True})
    
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new tokens
    tokens = create_tokens(user_id, email)
    
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": tokens["token_type"]
    }


@router.post("/change-password", response_model=dict)
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Change user password"""
    db = get_database()
    
    # Get user document
    user_doc = await db.users.find_one({"_id": current_user.id})
    
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify current password
    if not verify_password(password_data.current_password, user_doc["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Update password
    hashed_new_password = get_password_hash(password_data.new_password)
    await db.users.update_one(
        {"_id": current_user.id},
        {
            "$set": {
                "hashed_password": hashed_new_password,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"message": "Password changed successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )


# Development endpoint - no authentication required
if settings.ENVIRONMENT == "development":
    @router.post("/dev-login", response_model=LoginResponse)
    async def dev_login():
        """Development login - no credentials required"""
        tokens = create_tokens(MOCK_USER["_id"], MOCK_USER["email"])
        
        return LoginResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            token_type=tokens["token_type"],
            user=UserResponse(
                id=MOCK_USER["_id"],
                username=MOCK_USER["username"],
                email=MOCK_USER["email"],
                full_name=MOCK_USER["full_name"],
                role=MOCK_USER["role"],
                is_active=MOCK_USER["is_active"],
                created_at=MOCK_USER["created_at"],
                last_login=datetime.utcnow()
            )
        ) 