from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class AnalysisStatus(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    FAILED = "failed"


class CompetitorData(BaseModel):
    name: str
    ticker: Optional[str] = None
    data: Dict[str, Any] = {}


class AnalysisBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    period: str = Field(..., min_length=1, max_length=50)
    competitors: List[str] = Field(default_factory=list)
    status: AnalysisStatus = AnalysisStatus.DRAFT


class AnalysisCreate(AnalysisBase):
    pass


class AnalysisUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    period: Optional[str] = Field(None, min_length=1, max_length=50)
    competitors: Optional[List[str]] = None
    status: Optional[AnalysisStatus] = None


class AnalysisInDB(AnalysisBase):
    id: str = Field(alias="_id")
    user_id: str
    created_at: datetime
    updated_at: datetime
    competitor_data: List[CompetitorData] = Field(default_factory=list)
    financial_data: Dict[str, Any] = Field(default_factory=dict)
    ai_insights: Dict[str, Any] = Field(default_factory=dict)
    file_ids: List[str] = Field(default_factory=list)


class Analysis(AnalysisBase):
    id: str = Field(alias="_id")
    user_id: str
    created_at: datetime
    updated_at: datetime
    competitor_data: List[CompetitorData] = Field(default_factory=list)
    financial_data: Dict[str, Any] = Field(default_factory=dict)
    ai_insights: Dict[str, Any] = Field(default_factory=dict)
    file_ids: List[str] = Field(default_factory=list)
    
    class Config:
        populate_by_name = True


class AnalysisResponse(BaseModel):
    id: str
    name: str
    description: str
    period: str
    competitors: List[str]
    status: AnalysisStatus
    user_id: str
    created_at: datetime
    updated_at: datetime
    competitor_data: List[CompetitorData] = Field(default_factory=list)
    financial_data: Dict[str, Any] = Field(default_factory=dict)
    ai_insights: Dict[str, Any] = Field(default_factory=dict)


class AnalysisListResponse(BaseModel):
    analyses: List[AnalysisResponse]
    total: int
    page: int
    size: int
    pages: int


class DashboardData(BaseModel):
    income_statement: Dict[str, Any] = Field(default_factory=dict)
    balance_sheet: Dict[str, Any] = Field(default_factory=dict)
    cash_flow: Dict[str, Any] = Field(default_factory=dict)
    kpis: Dict[str, Any] = Field(default_factory=dict)
    mda: Dict[str, Any] = Field(default_factory=dict)


class AnalysisFilter(BaseModel):
    status: Optional[AnalysisStatus] = None
    period: Optional[str] = None
    search: Optional[str] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"


class BulkDeleteRequest(BaseModel):
    analysis_ids: List[str] = Field(..., min_items=1) 