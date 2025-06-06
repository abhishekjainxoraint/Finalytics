from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional, List
from datetime import datetime
import uuid
import math

from app.core.database import get_database
from app.core.config import settings
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.analysis import (
    AnalysisCreate,
    AnalysisUpdate,
    AnalysisResponse,
    AnalysisListResponse,
    AnalysisFilter,
    AnalysisStatus,
    DashboardData,
    BulkDeleteRequest
)

router = APIRouter()

# Mock data for development
MOCK_ANALYSES = [
    {
        "_id": "analysis-1",
        "name": "Q4 2024 Banking Performance Analysis",
        "description": "Comprehensive quarterly analysis of banking sector performance with competitive benchmarking",
        "period": "Q4 2024",
        "competitors": ["Bank of America", "Wells Fargo", "JPMorgan Chase"],
        "status": "completed",
        "user_id": "mock-user-id",
        "created_at": datetime(2024, 1, 15, 10, 0, 0),
        "updated_at": datetime(2024, 1, 20, 15, 30, 0),
        "competitor_data": [],
        "financial_data": {},
        "ai_insights": {},
        "file_ids": []
    },
    {
        "_id": "analysis-2", 
        "name": "Digital Banking Transformation Study",
        "description": "Analysis of digital banking trends and competitive positioning in the fintech space",
        "period": "Q1 2024",
        "competitors": ["Citibank", "Goldman Sachs", "Morgan Stanley"],
        "status": "in-progress",
        "user_id": "mock-user-id",
        "created_at": datetime(2024, 2, 1, 9, 0, 0),
        "updated_at": datetime(2024, 2, 10, 11, 15, 0),
        "competitor_data": [],
        "financial_data": {},
        "ai_insights": {},
        "file_ids": []
    },
    {
        "_id": "analysis-3",
        "name": "Risk Management Assessment",
        "description": "Credit risk and operational risk analysis across major banking institutions",
        "period": "Q3 2024",
        "competitors": ["US Bank", "PNC Bank", "Capital One"],
        "status": "draft",
        "user_id": "mock-user-id",
        "created_at": datetime(2024, 1, 5, 14, 30, 0),
        "updated_at": datetime(2024, 1, 6, 16, 45, 0),
        "competitor_data": [],
        "financial_data": {},
        "ai_insights": {},
        "file_ids": []
    },
    {
        "_id": "analysis-4",
        "name": "Market Share Analysis 2024",
        "description": "Regional market share analysis and growth opportunities identification",
        "period": "Full Year 2024",
        "competitors": ["Chase", "Bank of America", "Wells Fargo"],
        "status": "completed",
        "user_id": "mock-user-id",
        "created_at": datetime(2024, 1, 25, 8, 15, 0),
        "updated_at": datetime(2024, 1, 30, 17, 20, 0),
        "competitor_data": [],
        "financial_data": {},
        "ai_insights": {},
        "file_ids": []
    }
]


def get_mock_user():
    """Get mock user for development"""
    return User(
        _id="mock-user-id",
        username="devuser",
        email="dev@example.com",
        full_name="Development User",
        role="admin",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


async def get_user_dependency():
    """Get user dependency based on database availability"""
    if settings.DISABLE_DATABASE:
        return get_mock_user()
    else:
        # For database mode, we need to handle the authentication properly
        # This is a simplified version - in production you'd want proper auth
        return get_mock_user()


def sort_mock_analyses(analyses: List[dict], sort_by: str, sort_order: str) -> List[dict]:
    """Sort mock analyses data"""
    reverse = sort_order == "desc"
    
    if sort_by == "created_at":
        return sorted(analyses, key=lambda x: x["created_at"], reverse=reverse)
    elif sort_by == "name":
        return sorted(analyses, key=lambda x: x["name"].lower(), reverse=reverse)
    elif sort_by == "status":
        status_order = {"completed": 0, "in-progress": 1, "draft": 2}
        return sorted(analyses, key=lambda x: status_order.get(x["status"], 3), reverse=reverse)
    elif sort_by == "updated_at":
        return sorted(analyses, key=lambda x: x["updated_at"], reverse=reverse)
    else:
        return analyses


def filter_mock_analyses(analyses: List[dict], status: Optional[str], search: Optional[str]) -> List[dict]:
    """Filter mock analyses data"""
    filtered = analyses.copy()
    
    if status:
        filtered = [a for a in filtered if a["status"] == status]
    
    if search:
        search_lower = search.lower()
        filtered = [a for a in filtered if 
                   search_lower in a["name"].lower() or 
                   search_lower in a["description"].lower() or 
                   search_lower in a["period"].lower()]
    
    return filtered


@router.post("/", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    analysis_data: AnalysisCreate,
    current_user: User = Depends(get_user_dependency)
):
    """Create a new financial analysis"""
    if settings.DISABLE_DATABASE:
        # Mock creation
        new_analysis = {
            "_id": f"analysis-{len(MOCK_ANALYSES) + 1}",
            "name": analysis_data.name,
            "description": analysis_data.description,
            "period": analysis_data.period,
            "competitors": analysis_data.competitors,
            "status": analysis_data.status,
            "user_id": "mock-user-id",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "competitor_data": [],
            "financial_data": {},
            "ai_insights": {},
            "file_ids": []
        }
        MOCK_ANALYSES.append(new_analysis)
        
        # Convert _id to id for response
        response_data = new_analysis.copy()
        response_data["id"] = response_data.pop("_id")
        return AnalysisResponse(**response_data)
    
    # Database implementation
    db = get_database()
    analysis_doc = {
        "_id": str(uuid.uuid4()),
        "name": analysis_data.name,
        "description": analysis_data.description,
        "period": analysis_data.period,
        "competitors": analysis_data.competitors,
        "status": analysis_data.status,
        "user_id": current_user.id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "competitor_data": [],
        "financial_data": {},
        "ai_insights": {},
        "file_ids": []
    }
    await db.analyses.insert_one(analysis_doc)
    return AnalysisResponse(**analysis_doc)


@router.get("/", response_model=AnalysisListResponse)
async def get_analyses(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[AnalysisStatus] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = Query("created_at", regex="^(created_at|name|status|updated_at)$"),
    sort_order: Optional[str] = Query("desc", regex="^(asc|desc)$"),
    current_user: User = Depends(get_user_dependency)
):
    """Get user's analyses with filtering and sorting"""
    if settings.DISABLE_DATABASE:
        # Use mock data
        analyses = MOCK_ANALYSES.copy()
        
        # Filter
        analyses = filter_mock_analyses(analyses, status, search)
        
        # Sort
        analyses = sort_mock_analyses(analyses, sort_by, sort_order)
        
        # Paginate
        total = len(analyses)
        skip = (page - 1) * size
        paginated_analyses = analyses[skip:skip + size]
        pages = math.ceil(total / size)
        
        # Convert to response models - fix field mapping
        analysis_responses = []
        for analysis in paginated_analyses:
            response_data = analysis.copy()
            response_data["id"] = response_data.pop("_id")  # Convert _id to id
            analysis_responses.append(AnalysisResponse(**response_data))
        
        return AnalysisListResponse(
            analyses=analysis_responses,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
    
    # Database implementation
    db = get_database()
    query = {"user_id": current_user.id}
    
    if status:
        query["status"] = status
    
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"period": {"$regex": search, "$options": "i"}}
        ]
    
    sort_direction = 1 if sort_order == "asc" else -1
    sort_spec = [(sort_by, sort_direction)]
    
    total = await db.analyses.count_documents(query)
    skip = (page - 1) * size
    pages = math.ceil(total / size)
    
    cursor = db.analyses.find(query).sort(sort_spec).skip(skip).limit(size)
    analyses = await cursor.to_list(length=size)
    
    analysis_responses = [AnalysisResponse(**analysis) for analysis in analyses]
    
    return AnalysisListResponse(
        analyses=analysis_responses,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    current_user: User = Depends(get_user_dependency)
):
    """Get a specific analysis"""
    if settings.DISABLE_DATABASE:
        # Find in mock data
        analysis = next((a for a in MOCK_ANALYSES if a["_id"] == analysis_id), None)
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )
        
        # Convert _id to id for response
        response_data = analysis.copy()
        response_data["id"] = response_data.pop("_id")
        return AnalysisResponse(**response_data)
    
    # Database implementation
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
    
    return AnalysisResponse(**analysis)


@router.put("/{analysis_id}", response_model=AnalysisResponse)
async def update_analysis(
    analysis_id: str,
    analysis_data: AnalysisUpdate,
    current_user: User = Depends(get_user_dependency)
):
    """Update an analysis"""
    if settings.DISABLE_DATABASE:
        # Find and update in mock data
        analysis = next((a for a in MOCK_ANALYSES if a["_id"] == analysis_id), None)
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )
        
        # Update fields
        if analysis_data.name is not None:
            analysis["name"] = analysis_data.name
        if analysis_data.description is not None:
            analysis["description"] = analysis_data.description
        if analysis_data.period is not None:
            analysis["period"] = analysis_data.period
        if analysis_data.competitors is not None:
            analysis["competitors"] = analysis_data.competitors
        if analysis_data.status is not None:
            analysis["status"] = analysis_data.status
        
        analysis["updated_at"] = datetime.utcnow()
        
        # Convert _id to id for response
        response_data = analysis.copy()
        response_data["id"] = response_data.pop("_id")
        return AnalysisResponse(**response_data)
    
    # Database implementation continues...
    db = get_database()
    existing_analysis = await db.analyses.find_one({
        "_id": analysis_id,
        "user_id": current_user.id
    })
    
    if not existing_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    update_data = {"updated_at": datetime.utcnow()}
    
    if analysis_data.name is not None:
        update_data["name"] = analysis_data.name
    if analysis_data.description is not None:
        update_data["description"] = analysis_data.description
    if analysis_data.period is not None:
        update_data["period"] = analysis_data.period
    if analysis_data.competitors is not None:
        update_data["competitors"] = analysis_data.competitors
    if analysis_data.status is not None:
        update_data["status"] = analysis_data.status
    
    await db.analyses.update_one(
        {"_id": analysis_id},
        {"$set": update_data}
    )
    
    updated_analysis = await db.analyses.find_one({"_id": analysis_id})
    return AnalysisResponse(**updated_analysis)


@router.delete("/{analysis_id}", response_model=dict)
async def delete_analysis(
    analysis_id: str,
    current_user: User = Depends(get_user_dependency)
):
    """Delete an analysis"""
    if settings.DISABLE_DATABASE:
        # Find and remove from mock data
        analysis = next((a for a in MOCK_ANALYSES if a["_id"] == analysis_id), None)
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )
        
        MOCK_ANALYSES.remove(analysis)
        return {"message": "Analysis deleted successfully"}
    
    # Database implementation
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
    
    await db.analyses.delete_one({"_id": analysis_id})
    await db.market_questions.delete_many({"analysis_id": analysis_id})
    
    return {"message": "Analysis deleted successfully"}


@router.post("/bulk-delete", response_model=dict)
async def bulk_delete_analyses(
    request: BulkDeleteRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Delete multiple analyses"""
    db = get_database()
    
    # Verify all analyses belong to the user
    analyses = await db.analyses.find({
        "_id": {"$in": request.analysis_ids},
        "user_id": current_user.id
    }).to_list(length=None)
    
    found_ids = [analysis["_id"] for analysis in analyses]
    
    if len(found_ids) != len(request.analysis_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some analyses not found or don't belong to user"
        )
    
    # Delete analyses
    delete_result = await db.analyses.delete_many({
        "_id": {"$in": request.analysis_ids}
    })
    
    # Delete related market research questions
    await db.market_questions.delete_many({
        "analysis_id": {"$in": request.analysis_ids}
    })
    
    return {
        "message": f"Successfully deleted {delete_result.deleted_count} analyses"
    }


@router.get("/{analysis_id}/dashboard", response_model=DashboardData)
async def get_dashboard_data(
    analysis_id: str,
    current_user: User = Depends(get_user_dependency)
):
    """Get dashboard data for an analysis"""
    if settings.DISABLE_DATABASE:
        # Find analysis in mock data
        analysis = next((a for a in MOCK_ANALYSES if a["_id"] == analysis_id), None)
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )
    
    # Return mock dashboard data
    dashboard_data = {
        "income_statement": {
            "revenue_growth": [
                {"quarter": "Q1 2023", "our_bank": 4.2, "bank_of_america": 4.8, "wells_fargo": 4.1},
                {"quarter": "Q2 2023", "our_bank": 4.5, "bank_of_america": 4.9, "wells_fargo": 4.3},
                {"quarter": "Q3 2023", "our_bank": 4.8, "bank_of_america": 5.1, "wells_fargo": 4.5},
                {"quarter": "Q4 2023", "our_bank": 5.1, "bank_of_america": 5.3, "wells_fargo": 4.7}
            ],
            "net_interest_margin": 5.6,
            "efficiency_ratio": 62
        },
        "balance_sheet": {
            "asset_growth": 8.2,
            "capital_ratio": 14.8,
            "loan_to_deposit": 78,
            "deposit_growth": 5.4
        },
        "cash_flow": {
            "operating_cash_flow": 1250.5,
            "investment_cash_flow": -320.8,
            "financing_cash_flow": -180.2
        },
        "kpis": {
            "npl_ratio": 0.7,
            "customer_acquisition_cost": 225,
            "lcr": 132,
            "customer_growth": 7.8
        },
        "mda": {
            "strategic_priorities": ["Digital transformation", "Market expansion", "Risk management"],
            "risk_factors": ["Credit risk", "Interest rate risk", "Regulatory compliance"],
            "outlook": "Positive growth expected in Q1 2025"
        }
    }
    
    return DashboardData(**dashboard_data)


@router.post("/{analysis_id}/generate", response_model=dict)
async def generate_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Generate AI-powered analysis insights"""
    db = get_database()
    
    # Check if analysis exists and belongs to user
    analysis = await db.analyses.find_one({
        "_id": analysis_id,
        "user_id": current_user.id
    })
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Update status to in-progress
    await db.analyses.update_one(
        {"_id": analysis_id},
        {
            "$set": {
                "status": AnalysisStatus.IN_PROGRESS,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # In a real implementation, this would trigger background processing
    # For now, we'll just simulate completion
    await db.analyses.update_one(
        {"_id": analysis_id},
        {
            "$set": {
                "status": AnalysisStatus.COMPLETED,
                "updated_at": datetime.utcnow(),
                "ai_insights": {
                    "summary": "Analysis completed successfully",
                    "key_findings": ["Strong revenue growth", "Improving efficiency ratios"],
                    "recommendations": ["Focus on digital channels", "Optimize cost structure"]
                }
            }
        }
    )
    
    return {"message": "Analysis generation completed", "status": "completed"} 