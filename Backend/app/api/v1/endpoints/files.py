from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import Optional, List
from datetime import datetime
import uuid
import os
import aiofiles

from app.core.config import settings
from app.core.database import get_database
from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.post("/upload", response_model=dict)
async def upload_file(
    file: UploadFile = File(...),
    analysis_id: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user)
):
    """Upload a file"""
    
    # Validate file type
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed"
        )
    
    # Validate file size
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size too large. Maximum size is {settings.MAX_FILE_SIZE} bytes"
        )
    
    # Reset file pointer
    await file.seek(0)
    
    # Verify analysis exists if provided
    if analysis_id:
        db = get_database()
        analysis = await db.analyses.find_one({
            "_id": analysis_id,
            "user_id": current_user.id
        })
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{file_id}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(content)
    
    # Save file metadata to database
    db = get_database()
    file_doc = {
        "_id": file_id,
        "filename": file.filename,
        "unique_filename": unique_filename,
        "content_type": file.content_type,
        "size": file_size,
        "user_id": current_user.id,
        "analysis_id": analysis_id,
        "upload_date": datetime.utcnow(),
        "file_path": file_path
    }
    
    await db.files.insert_one(file_doc)
    
    # Update analysis with file ID if provided
    if analysis_id:
        await db.analyses.update_one(
            {"_id": analysis_id},
            {"$push": {"file_ids": file_id}}
        )
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "size": file_size,
        "content_type": file.content_type,
        "message": "File uploaded successfully"
    }


@router.get("/", response_model=List[dict])
async def get_files(
    analysis_id: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Get user's files"""
    db = get_database()
    
    # Build query
    query = {"user_id": current_user.id}
    
    if analysis_id:
        query["analysis_id"] = analysis_id
    
    # Get files
    cursor = db.files.find(query, {"file_path": 0})  # Exclude file_path for security
    files = await cursor.to_list(length=None)
    
    return files


@router.get("/{file_id}", response_class=FileResponse)
async def download_file(
    file_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Download a file"""
    db = get_database()
    
    # Get file metadata
    file_doc = await db.files.find_one({
        "_id": file_id,
        "user_id": current_user.id
    })
    
    if not file_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check if file exists on disk
    if not os.path.exists(file_doc["file_path"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on disk"
        )
    
    return FileResponse(
        path=file_doc["file_path"],
        filename=file_doc["filename"],
        media_type=file_doc["content_type"]
    )


@router.delete("/{file_id}", response_model=dict)
async def delete_file(
    file_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a file"""
    db = get_database()
    
    # Get file metadata
    file_doc = await db.files.find_one({
        "_id": file_id,
        "user_id": current_user.id
    })
    
    if not file_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Delete file from disk
    try:
        if os.path.exists(file_doc["file_path"]):
            os.remove(file_doc["file_path"])
    except Exception as e:
        # Log error but continue with database deletion
        pass
    
    # Remove file from analysis if associated
    if file_doc.get("analysis_id"):
        await db.analyses.update_one(
            {"_id": file_doc["analysis_id"]},
            {"$pull": {"file_ids": file_id}}
        )
    
    # Delete file metadata
    await db.files.delete_one({"_id": file_id})
    
    return {"message": "File deleted successfully"}


@router.get("/{file_id}/info", response_model=dict)
async def get_file_info(
    file_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get file information"""
    db = get_database()
    
    # Get file metadata
    file_doc = await db.files.find_one(
        {"_id": file_id, "user_id": current_user.id},
        {"file_path": 0}  # Exclude file_path for security
    )
    
    if not file_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    return file_doc 