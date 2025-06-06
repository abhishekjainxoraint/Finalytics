from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class QuestionStatus(str, Enum):
    PENDING = "pending"
    ANSWERED = "answered"
    CLOSED = "closed"


class ResearchResponse(BaseModel):
    analyst: str
    response: str
    timestamp: datetime
    attachments: List[str] = Field(default_factory=list)
    confidence_score: Optional[float] = None


class MarketQuestionBase(BaseModel):
    analysis_id: str
    dashboard: str = Field(..., min_length=1, max_length=100)
    report: str = Field(..., min_length=1, max_length=100)
    question: str = Field(..., min_length=10, max_length=2000)
    status: QuestionStatus = QuestionStatus.PENDING


class MarketQuestionCreate(MarketQuestionBase):
    pass


class MarketQuestionUpdate(BaseModel):
    dashboard: Optional[str] = Field(None, min_length=1, max_length=100)
    report: Optional[str] = Field(None, min_length=1, max_length=100)
    question: Optional[str] = Field(None, min_length=10, max_length=2000)
    status: Optional[QuestionStatus] = None


class MarketQuestionInDB(MarketQuestionBase):
    id: str = Field(alias="_id")
    user_id: str
    created_at: datetime
    updated_at: datetime
    responses: List[ResearchResponse] = Field(default_factory=list)
    ai_summary: Optional[str] = None
    priority: int = 0
    tags: List[str] = Field(default_factory=list)


class MarketQuestion(MarketQuestionBase):
    id: str = Field(alias="_id")
    user_id: str
    created_at: datetime
    updated_at: datetime
    responses: List[ResearchResponse] = Field(default_factory=list)
    ai_summary: Optional[str] = None
    priority: int = 0
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        populate_by_name = True


class MarketQuestionResponse(BaseModel):
    id: str
    analysis_id: str
    analysis_name: Optional[str] = None
    dashboard: str
    report: str
    question: str
    status: QuestionStatus
    user_id: str
    user_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    responses: List[ResearchResponse] = Field(default_factory=list)
    ai_summary: Optional[str] = None
    priority: int = 0
    tags: List[str] = Field(default_factory=list)


class MarketQuestionListResponse(BaseModel):
    questions: List[MarketQuestionResponse]
    total: int
    page: int
    size: int
    pages: int


class AddResponseRequest(BaseModel):
    analyst: str = Field(..., min_length=1, max_length=100)
    response: str = Field(..., min_length=10, max_length=5000)
    attachments: List[str] = Field(default_factory=list)
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class MarketQuestionFilter(BaseModel):
    analysis_id: Optional[str] = None
    status: Optional[QuestionStatus] = None
    dashboard: Optional[str] = None
    search: Optional[str] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"


class AIAnalysisRequest(BaseModel):
    question_id: str
    force_refresh: bool = False


class BulkQuestionAction(BaseModel):
    question_ids: List[str] = Field(..., min_items=1)
    action: str = Field(..., pattern="^(close|reopen|delete)$")


class ResearchMetrics(BaseModel):
    total_questions: int
    pending_questions: int
    answered_questions: int
    closed_questions: int
    avg_response_time_hours: float
    top_analysts: List[Dict[str, Any]] = Field(default_factory=list)
    popular_topics: List[Dict[str, Any]] = Field(default_factory=list) 