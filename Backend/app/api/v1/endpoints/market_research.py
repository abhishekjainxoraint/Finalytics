from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional, List
from datetime import datetime
import uuid
import math

from app.core.database import get_database
from app.core.config import settings
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.market_research import (
    MarketQuestionCreate,
    MarketQuestionUpdate,
    MarketQuestionResponse,
    MarketQuestionListResponse,
    MarketQuestionFilter,
    QuestionStatus,
    AddResponseRequest,
    BulkQuestionAction,
    ResearchMetrics
)

router = APIRouter()

# Mock data for development
MOCK_QUESTIONS = [
    {
        "_id": "question-1",
        "analysis_id": "analysis-1",
        "dashboard": "Financial Performance",
        "report": "Income Statement",
        "question": "What are the key revenue drivers for our competitors in Q4 2024?",
        "status": "answered",
        "user_id": "mock-user-id",
        "created_at": datetime(2024, 1, 16, 11, 0, 0),
        "updated_at": datetime(2024, 1, 18, 14, 30, 0),
        "responses": [
            {
                "analyst": "Sarah Johnson",
                "response": "Based on Q4 reports, key revenue drivers include digital banking fees (15% growth), loan origination volumes (8% increase), and wealth management services (12% growth). Investment banking revenues declined 5% due to market volatility.",
                "timestamp": datetime(2024, 1, 18, 14, 30, 0),
                "attachments": [],
                "confidence_score": 0.85
            }
        ],
        "ai_summary": "Revenue growth driven primarily by digital services and traditional lending",
        "priority": 1,
        "tags": ["revenue", "Q4", "competitors"]
    },
    {
        "_id": "question-2", 
        "analysis_id": "analysis-2",
        "dashboard": "Risk Management",
        "report": "Credit Risk Assessment",
        "question": "How do competitor credit loss provisions compare to industry benchmarks?",
        "status": "pending",
        "user_id": "mock-user-id",
        "created_at": datetime(2024, 2, 2, 10, 15, 0),
        "updated_at": datetime(2024, 2, 2, 10, 15, 0),
        "responses": [],
        "ai_summary": None,
        "priority": 2,
        "tags": ["credit-risk", "provisions", "benchmarks"]
    },
    {
        "_id": "question-3",
        "analysis_id": "analysis-1", 
        "dashboard": "Market Trends",
        "report": "Competitive Analysis",
        "question": "What digital banking initiatives are our competitors prioritizing?",
        "status": "answered",
        "user_id": "mock-user-id",
        "created_at": datetime(2024, 1, 20, 9, 30, 0),
        "updated_at": datetime(2024, 1, 25, 16, 45, 0),
        "responses": [
            {
                "analyst": "Mike Analytics",
                "response": "Major competitors are focusing on AI-powered customer service, mobile-first account opening, and cryptocurrency trading platforms. JPMorgan leads in AI adoption while Bank of America excels in mobile UX.",
                "timestamp": datetime(2024, 1, 25, 16, 45, 0),
                "attachments": [],
                "confidence_score": 0.78
            }
        ],
        "ai_summary": "Digital transformation focused on AI, mobile experience, and emerging assets",
        "priority": 1,
        "tags": ["digital", "AI", "mobile", "crypto"]
    },
    {
        "_id": "question-4",
        "analysis_id": "analysis-3",
        "dashboard": "Operational Metrics",
        "report": "Efficiency Analysis", 
        "question": "How do operational efficiency ratios compare across major banks?",
        "status": "pending",
        "user_id": "mock-user-id",
        "created_at": datetime(2024, 1, 8, 15, 20, 0),
        "updated_at": datetime(2024, 1, 8, 15, 20, 0),
        "responses": [],
        "ai_summary": None,
        "priority": 0,
        "tags": ["efficiency", "operations", "ratios"]
    },
    {
        "_id": "question-5",
        "analysis_id": "analysis-4",
        "dashboard": "Market Share",
        "report": "Regional Analysis",
        "question": "Which regions show the highest growth potential for banking services?",
        "status": "answered",
        "user_id": "mock-user-id",
        "created_at": datetime(2024, 1, 26, 13, 10, 0),
        "updated_at": datetime(2024, 1, 29, 11, 25, 0),
        "responses": [
            {
                "analyst": "Emma Insights",
                "response": "Southeast and Southwest regions show strongest growth potential with 15% and 12% projected growth respectively. Urban millennial demographics driving digital banking adoption.",
                "timestamp": datetime(2024, 1, 29, 11, 25, 0),
                "attachments": [],
                "confidence_score": 0.92
            }
        ],
        "ai_summary": "Southeast and Southwest regions present highest growth opportunities",
        "priority": 1,
        "tags": ["regions", "growth", "millennials"]
    }
]

# Mock analysis names mapping
MOCK_ANALYSIS_NAMES = {
    "analysis-1": "Q4 2024 Banking Performance Analysis",
    "analysis-2": "Digital Banking Transformation Study", 
    "analysis-3": "Risk Management Assessment",
    "analysis-4": "Market Share Analysis 2024"
}


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


def sort_mock_questions(questions: List[dict], sort_by: str, sort_order: str) -> List[dict]:
    """Sort mock questions data"""
    reverse = sort_order == "desc"
    
    if sort_by == "created_at":
        return sorted(questions, key=lambda x: x["created_at"], reverse=reverse)
    elif sort_by == "status":
        status_order = {"pending": 0, "answered": 1, "closed": 2}
        return sorted(questions, key=lambda x: status_order.get(x["status"], 3), reverse=reverse)
    elif sort_by == "analysis_id":
        return sorted(questions, key=lambda x: x["analysis_id"], reverse=reverse)
    elif sort_by == "user_id":
        return sorted(questions, key=lambda x: x["user_id"], reverse=reverse)
    else:
        return questions


def filter_mock_questions(questions: List[dict], analysis_id: Optional[str], status: Optional[str], search: Optional[str]) -> List[dict]:
    """Filter mock questions data"""
    filtered = questions.copy()
    
    if analysis_id:
        filtered = [q for q in filtered if q["analysis_id"] == analysis_id]
    
    if status:
        filtered = [q for q in filtered if q["status"] == status]
    
    if search:
        search_lower = search.lower()
        filtered = [q for q in filtered if 
                   search_lower in q["question"].lower() or 
                   search_lower in q["dashboard"].lower() or 
                   search_lower in q["report"].lower()]
    
    return filtered


@router.post("/questions", response_model=MarketQuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    question_data: MarketQuestionCreate,
    current_user: User = Depends(get_user_dependency)
):
    """Create a new market research question"""
    if settings.DISABLE_DATABASE:
        # Mock creation
        new_question = {
            "_id": f"question-{len(MOCK_QUESTIONS) + 1}",
            "analysis_id": question_data.analysis_id,
            "dashboard": question_data.dashboard,
            "report": question_data.report,
            "question": question_data.question,
            "status": question_data.status,
            "user_id": "mock-user-id",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "responses": [],
            "ai_summary": None,
            "priority": 0,
            "tags": []
        }
        MOCK_QUESTIONS.append(new_question)
        
        # Add analysis name for response and fix field mapping
        new_question["analysis_name"] = MOCK_ANALYSIS_NAMES.get(question_data.analysis_id, "Unknown Analysis")
        new_question["user_name"] = "Development User"
        
        # Convert _id to id for response
        response_data = new_question.copy()
        response_data["id"] = response_data.pop("_id")
        
        return MarketQuestionResponse(**response_data)
    
    # Database implementation
    db = get_database()
    
    # Verify the analysis exists and belongs to the user
    analysis = await db.analyses.find_one({
        "_id": question_data.analysis_id,
        "user_id": current_user.id
    })
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Create question document
    question_doc = {
        "_id": str(uuid.uuid4()),
        "analysis_id": question_data.analysis_id,
        "dashboard": question_data.dashboard,
        "report": question_data.report,
        "question": question_data.question,
        "status": question_data.status,
        "user_id": current_user.id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "responses": [],
        "ai_summary": None,
        "priority": 0,
        "tags": []
    }
    
    # Insert question
    await db.market_questions.insert_one(question_doc)
    
    # Add analysis name for response
    question_doc["analysis_name"] = analysis["name"]
    question_doc["user_name"] = current_user.full_name
    
    return MarketQuestionResponse(**question_doc)


@router.get("/questions", response_model=MarketQuestionListResponse)
async def get_questions(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    analysis_id: Optional[str] = None,
    status: Optional[QuestionStatus] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = Query("created_at", regex="^(created_at|status|analysis_id|user_id)$"),
    sort_order: Optional[str] = Query("desc", regex="^(asc|desc)$"),
    current_user: User = Depends(get_user_dependency)
):
    """Get market research questions with filtering and sorting"""
    if settings.DISABLE_DATABASE:
        # Use mock data
        questions = MOCK_QUESTIONS.copy()
        
        # Filter
        questions = filter_mock_questions(questions, analysis_id, status, search)
        
        # Sort
        questions = sort_mock_questions(questions, sort_by, sort_order)
        
        # Paginate
        total = len(questions)
        skip = (page - 1) * size
        paginated_questions = questions[skip:skip + size]
        pages = math.ceil(total / size)
        
        # Enrich with analysis and user names and fix field mapping
        question_responses = []
        for question in paginated_questions:
            response_data = question.copy()
            response_data["analysis_name"] = MOCK_ANALYSIS_NAMES.get(question["analysis_id"], "Unknown Analysis")
            response_data["user_name"] = "Development User"
            
            # Convert _id to id for response
            response_data["id"] = response_data.pop("_id")
            
            question_responses.append(MarketQuestionResponse(**response_data))
        
        return MarketQuestionListResponse(
            questions=question_responses,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
    
    # Database implementation
    db = get_database()
    
    # Build query
    query = {"user_id": current_user.id}
    
    if analysis_id:
        query["analysis_id"] = analysis_id
    
    if status:
        query["status"] = status
    
    if search:
        query["$or"] = [
            {"question": {"$regex": search, "$options": "i"}},
            {"dashboard": {"$regex": search, "$options": "i"}},
            {"report": {"$regex": search, "$options": "i"}}
        ]
    
    # Build sort
    sort_direction = 1 if sort_order == "asc" else -1
    sort_spec = [(sort_by, sort_direction)]
    
    # Get total count
    total = await db.market_questions.count_documents(query)
    
    # Calculate pagination
    skip = (page - 1) * size
    pages = math.ceil(total / size)
    
    # Get questions
    cursor = db.market_questions.find(query).sort(sort_spec).skip(skip).limit(size)
    questions = await cursor.to_list(length=size)
    
    # Enrich questions with analysis and user names
    for question in questions:
        # Get analysis name
        analysis = await db.analyses.find_one({"_id": question["analysis_id"]})
        question["analysis_name"] = analysis["name"] if analysis else "Unknown"
        question["user_name"] = current_user.full_name
    
    # Convert to response models
    question_responses = [MarketQuestionResponse(**question) for question in questions]
    
    return MarketQuestionListResponse(
        questions=question_responses,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/questions/{question_id}", response_model=MarketQuestionResponse)
async def get_question(
    question_id: str,
    current_user: User = Depends(get_user_dependency)
):
    """Get a specific market research question"""
    if settings.DISABLE_DATABASE:
        # Find in mock data
        question = next((q for q in MOCK_QUESTIONS if q["_id"] == question_id), None)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        
        # Add analysis name and fix field mapping
        response_data = question.copy()
        response_data["analysis_name"] = MOCK_ANALYSIS_NAMES.get(question["analysis_id"], "Unknown Analysis")
        response_data["user_name"] = "Development User"
        
        # Convert _id to id for response
        response_data["id"] = response_data.pop("_id")
        
        return MarketQuestionResponse(**response_data)
    
    # Database implementation
    db = get_database()
    
    question = await db.market_questions.find_one({
        "_id": question_id,
        "user_id": current_user.id
    })
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Add analysis name
    analysis = await db.analyses.find_one({"_id": question["analysis_id"]})
    question["analysis_name"] = analysis["name"] if analysis else "Unknown"
    question["user_name"] = current_user.full_name
    
    return MarketQuestionResponse(**question)


@router.put("/questions/{question_id}", response_model=MarketQuestionResponse)
async def update_question(
    question_id: str,
    question_data: MarketQuestionUpdate,
    current_user: User = Depends(get_user_dependency)
):
    """Update a market research question"""
    db = get_database()
    
    # Check if question exists and belongs to user
    existing_question = await db.market_questions.find_one({
        "_id": question_id,
        "user_id": current_user.id
    })
    
    if not existing_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Build update data
    update_data = {"updated_at": datetime.utcnow()}
    
    if question_data.dashboard is not None:
        update_data["dashboard"] = question_data.dashboard
    if question_data.report is not None:
        update_data["report"] = question_data.report
    if question_data.question is not None:
        update_data["question"] = question_data.question
    if question_data.status is not None:
        update_data["status"] = question_data.status
    
    # Update question
    await db.market_questions.update_one(
        {"_id": question_id},
        {"$set": update_data}
    )
    
    # Get updated question
    updated_question = await db.market_questions.find_one({"_id": question_id})
    
    # Add analysis name
    analysis = await db.analyses.find_one({"_id": updated_question["analysis_id"]})
    updated_question["analysis_name"] = analysis["name"] if analysis else "Unknown"
    updated_question["user_name"] = current_user.full_name
    
    return MarketQuestionResponse(**updated_question)


@router.delete("/questions/{question_id}", response_model=dict)
async def delete_question(
    question_id: str,
    current_user: User = Depends(get_user_dependency)
):
    """Delete a market research question"""
    db = get_database()
    
    # Check if question exists and belongs to user
    question = await db.market_questions.find_one({
        "_id": question_id,
        "user_id": current_user.id
    })
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Delete question
    await db.market_questions.delete_one({"_id": question_id})
    
    return {"message": "Question deleted successfully"}


@router.post("/questions/{question_id}/responses", response_model=MarketQuestionResponse)
async def add_response(
    question_id: str,
    response_data: AddResponseRequest,
    current_user: User = Depends(get_user_dependency)
):
    """Add a response to a market research question"""
    db = get_database()
    
    # Check if question exists and belongs to user
    question = await db.market_questions.find_one({
        "_id": question_id,
        "user_id": current_user.id
    })
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Create response object
    response_obj = {
        "analyst": response_data.analyst,
        "response": response_data.response,
        "timestamp": datetime.utcnow(),
        "attachments": response_data.attachments,
        "confidence_score": response_data.confidence_score
    }
    
    # Update question with new response and status
    await db.market_questions.update_one(
        {"_id": question_id},
        {
            "$push": {"responses": response_obj},
            "$set": {
                "status": QuestionStatus.ANSWERED,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Get updated question
    updated_question = await db.market_questions.find_one({"_id": question_id})
    
    # Add analysis name
    analysis = await db.analyses.find_one({"_id": updated_question["analysis_id"]})
    updated_question["analysis_name"] = analysis["name"] if analysis else "Unknown"
    updated_question["user_name"] = current_user.full_name
    
    return MarketQuestionResponse(**updated_question)


@router.post("/questions/bulk-action", response_model=dict)
async def bulk_question_action(
    action_data: BulkQuestionAction,
    current_user: User = Depends(get_user_dependency)
):
    """Perform bulk actions on questions"""
    db = get_database()
    
    # Verify all questions belong to the user
    questions = await db.market_questions.find({
        "_id": {"$in": action_data.question_ids},
        "user_id": current_user.id
    }).to_list(length=None)
    
    found_ids = [question["_id"] for question in questions]
    
    if len(found_ids) != len(action_data.question_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some questions not found or don't belong to user"
        )
    
    # Perform action
    if action_data.action == "delete":
        delete_result = await db.market_questions.delete_many({
            "_id": {"$in": action_data.question_ids}
        })
        return {"message": f"Successfully deleted {delete_result.deleted_count} questions"}
    
    elif action_data.action == "close":
        update_result = await db.market_questions.update_many(
            {"_id": {"$in": action_data.question_ids}},
            {
                "$set": {
                    "status": QuestionStatus.CLOSED,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return {"message": f"Successfully closed {update_result.modified_count} questions"}
    
    elif action_data.action == "reopen":
        update_result = await db.market_questions.update_many(
            {"_id": {"$in": action_data.question_ids}},
            {
                "$set": {
                    "status": QuestionStatus.PENDING,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return {"message": f"Successfully reopened {update_result.modified_count} questions"}
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid action"
        )


@router.get("/metrics", response_model=ResearchMetrics)
async def get_research_metrics(
    current_user: User = Depends(get_user_dependency)
):
    """Get market research metrics for the user"""
    if settings.DISABLE_DATABASE:
        # Calculate metrics from mock data
        total_questions = len(MOCK_QUESTIONS)
        pending_questions = len([q for q in MOCK_QUESTIONS if q["status"] == "pending"])
        answered_questions = len([q for q in MOCK_QUESTIONS if q["status"] == "answered"])
        closed_questions = len([q for q in MOCK_QUESTIONS if q["status"] == "closed"])
        
        # Mock data for other metrics
        avg_response_time_hours = 18.5
        top_analysts = [
            {"name": "Sarah Johnson", "responses": 8, "avg_score": 0.85},
            {"name": "Mike Analytics", "responses": 6, "avg_score": 0.78},
            {"name": "Emma Insights", "responses": 4, "avg_score": 0.92}
        ]
        popular_topics = [
            {"topic": "Digital Banking", "count": 15},
            {"topic": "Risk Management", "count": 12},
            {"topic": "Market Growth", "count": 8}
        ]
        
        return ResearchMetrics(
            total_questions=total_questions,
            pending_questions=pending_questions,
            answered_questions=answered_questions,
            closed_questions=closed_questions,
            avg_response_time_hours=avg_response_time_hours,
            top_analysts=top_analysts,
            popular_topics=popular_topics
        )
    
    # Database implementation
    db = get_database()
    
    # Get question counts by status
    pipeline = [
        {"$match": {"user_id": current_user.id}},
        {"$group": {
            "_id": "$status",
            "count": {"$sum": 1}
        }}
    ]
    
    status_counts = {}
    async for result in db.market_questions.aggregate(pipeline):
        status_counts[result["_id"]] = result["count"]
    
    total_questions = sum(status_counts.values())
    pending_questions = status_counts.get("pending", 0)
    answered_questions = status_counts.get("answered", 0)
    closed_questions = status_counts.get("closed", 0)
    
    # Calculate average response time (mock data for now)
    avg_response_time_hours = 24.5
    
    # Get top analysts (mock data)
    top_analysts = [
        {"name": "Sarah Research", "responses": 15, "avg_score": 0.85},
        {"name": "Mike Analytics", "responses": 12, "avg_score": 0.82},
        {"name": "Emma Insights", "responses": 8, "avg_score": 0.88}
    ]
    
    # Get popular topics (mock data)
    popular_topics = [
        {"topic": "Revenue Growth", "count": 25},
        {"topic": "Risk Assessment", "count": 18},
        {"topic": "Market Share", "count": 15}
    ]
    
    return ResearchMetrics(
        total_questions=total_questions,
        pending_questions=pending_questions,
        answered_questions=answered_questions,
        closed_questions=closed_questions,
        avg_response_time_hours=avg_response_time_hours,
        top_analysts=top_analysts,
        popular_topics=popular_topics
    ) 