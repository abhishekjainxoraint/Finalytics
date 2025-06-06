from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import uuid


class MockDataService:
    def __init__(self):
        self.users = self._create_mock_users()
        self.analyses = self._create_mock_analyses()
        self.market_questions = self._create_mock_market_questions()
        self.files = self._create_mock_files()
    
    def _create_mock_users(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "user-1",
                "username": "john.doe",
                "email": "john.doe@bank.com",
                "full_name": "John Doe",
                "role": "analyst",
                "department": "FP&A",
                "is_active": True,
                "is_verified": True,
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-15T14:30:00Z",
                "last_login": "2024-01-20T09:15:00Z"
            },
            {
                "id": "user-2", 
                "username": "sarah.johnson",
                "email": "sarah.johnson@bank.com",
                "full_name": "Sarah Johnson",
                "role": "senior_analyst",
                "department": "Competitive Intelligence",
                "is_active": True,
                "is_verified": True,
                "created_at": "2023-12-15T08:00:00Z",
                "updated_at": "2024-01-18T16:45:00Z",
                "last_login": "2024-01-19T11:30:00Z"
            },
            {
                "id": "user-3",
                "username": "mike.chen",
                "email": "mike.chen@bank.com", 
                "full_name": "Mike Chen",
                "role": "manager",
                "department": "Strategic Planning",
                "is_active": True,
                "is_verified": True,
                "created_at": "2023-11-01T12:00:00Z",
                "updated_at": "2024-01-10T10:20:00Z",
                "last_login": "2024-01-20T08:45:00Z"
            }
        ]
    
    def _create_mock_analyses(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "analysis-1",
                "user_id": "user-1",
                "name": "Q4 2024 Banking Performance Analysis",
                "description": "Comprehensive analysis of Q4 2024 banking sector performance with competitive benchmarking",
                "period": "Q4 2024",
                "status": "completed",
                "progress": 100,
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-15T16:30:00Z",
                "completed_at": "2024-01-15T16:30:00Z",
                "competitors": [
                    {
                        "name": "Bank of America",
                        "ticker": "BAC",
                        "market_cap": "256.8B",
                        "status": "analyzed"
                    },
                    {
                        "name": "Wells Fargo", 
                        "ticker": "WFC",
                        "market_cap": "155.2B",
                        "status": "analyzed"
                    },
                    {
                        "name": "JPMorgan Chase",
                        "ticker": "JPM", 
                        "market_cap": "431.5B",
                        "status": "analyzed"
                    }
                ],
                "metrics": {
                    "revenue_growth": "8.5%",
                    "net_income_margin": "24.2%",
                    "roe": "15.3%",
                    "efficiency_ratio": "58.7%"
                },
                "files_count": 12,
                "questions_count": 8
            },
            {
                "id": "analysis-2",
                "user_id": "user-2", 
                "name": "Digital Banking Transformation Study",
                "description": "Market research on digital banking trends and competitive positioning",
                "period": "Q1 2024",
                "status": "in-progress",
                "progress": 65,
                "created_at": "2024-01-05T09:00:00Z",
                "updated_at": "2024-01-20T14:15:00Z",
                "completed_at": None,
                "competitors": [
                    {
                        "name": "Citibank",
                        "ticker": "C",
                        "market_cap": "98.4B", 
                        "status": "in-progress"
                    },
                    {
                        "name": "Goldman Sachs",
                        "ticker": "GS",
                        "market_cap": "112.7B",
                        "status": "analyzed"
                    }
                ],
                "metrics": {
                    "digital_adoption": "73%",
                    "mobile_users": "12.4M",
                    "api_transactions": "89%",
                    "cost_savings": "$2.1B"
                },
                "files_count": 8,
                "questions_count": 5
            },
            {
                "id": "analysis-3",
                "user_id": "user-3",
                "name": "Credit Risk Assessment 2024",
                "description": "Comprehensive credit risk analysis and peer comparison",
                "period": "FY 2024",
                "status": "draft",
                "progress": 25,
                "created_at": "2024-01-18T11:30:00Z",
                "updated_at": "2024-01-20T09:45:00Z", 
                "completed_at": None,
                "competitors": [
                    {
                        "name": "US Bank",
                        "ticker": "USB",
                        "market_cap": "62.1B",
                        "status": "pending"
                    }
                ],
                "metrics": {
                    "loan_loss_rate": "0.34%",
                    "npl_ratio": "0.52%",
                    "coverage_ratio": "165%",
                    "tier1_capital": "13.8%"
                },
                "files_count": 3,
                "questions_count": 2
            }
        ]
    
    def _create_mock_market_questions(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "question-1",
                "user_id": "user-1",
                "analysis_id": "analysis-1",
                "analysis_name": "Q4 2024 Banking Performance Analysis",
                "dashboard": "Financial Performance",
                "report": "Income Statement Analysis",
                "question": "What are the key revenue drivers for Bank of America compared to our institution?",
                "context": "Looking at Q4 2024 performance metrics",
                "priority": "high",
                "status": "answered",
                "created_at": "2024-01-02T11:00:00Z",
                "updated_at": "2024-01-08T15:30:00Z",
                "due_date": "2024-01-10T00:00:00Z",
                "tags": ["revenue", "competitive-analysis", "bofa"],
                "responses": [
                    {
                        "id": "response-1",
                        "analyst": "Sarah Johnson",
                        "analyst_id": "user-2",
                        "response": "Based on Q4 2024 reports, Bank of America's key revenue drivers include: 1) Net Interest Income ($14.2B, up 3% YoY) driven by rising rates, 2) Investment banking fees ($1.2B, up 18% YoY), 3) Trading revenue ($3.8B, up 12% YoY), and 4) Wealth management fees ($4.5B, up 8% YoY). Their digital banking platform contributed significantly with 42M digital users.",
                        "timestamp": "2024-01-08T15:30:00Z",
                        "attachments": []
                    }
                ]
            },
            {
                "id": "question-2",
                "user_id": "user-2",
                "analysis_id": "analysis-2", 
                "analysis_name": "Digital Banking Transformation Study",
                "dashboard": "Digital Transformation",
                "report": "Technology Investment Analysis",
                "question": "How do Citibank's mobile banking capabilities compare to industry leaders?",
                "context": "Focus on user experience and feature set",
                "priority": "medium",
                "status": "in-progress",
                "created_at": "2024-01-10T09:30:00Z",
                "updated_at": "2024-01-15T14:20:00Z",
                "due_date": "2024-01-25T00:00:00Z",
                "tags": ["mobile-banking", "citibank", "ux"],
                "responses": [
                    {
                        "id": "response-2",
                        "analyst": "Mike Chen",
                        "analyst_id": "user-3",
                        "response": "Analysis in progress. Initial findings show Citibank's mobile app scores 4.2/5 on app stores vs industry average of 4.0. Key features include biometric login, real-time notifications, and integrated investment tools. Will provide detailed comparison by Jan 25th.",
                        "timestamp": "2024-01-15T14:20:00Z",
                        "attachments": []
                    }
                ]
            },
            {
                "id": "question-3",
                "user_id": "user-1",
                "analysis_id": "analysis-1",
                "analysis_name": "Q4 2024 Banking Performance Analysis",
                "dashboard": "Risk Management", 
                "report": "Credit Risk Assessment",
                "question": "What is JPMorgan's approach to credit risk management in the current environment?",
                "context": "Particularly interested in provisions and loss rates",
                "priority": "high",
                "status": "pending",
                "created_at": "2024-01-12T16:45:00Z",
                "updated_at": "2024-01-12T16:45:00Z",
                "due_date": "2024-01-30T00:00:00Z",
                "tags": ["credit-risk", "jpmorgan", "provisions"],
                "responses": []
            },
            {
                "id": "question-4",
                "user_id": "user-3",
                "analysis_id": "analysis-3",
                "analysis_name": "Credit Risk Assessment 2024", 
                "dashboard": "Credit Analysis",
                "report": "Portfolio Quality",
                "question": "How does US Bank's loan portfolio composition compare to peer banks?",
                "context": "Focus on commercial vs retail mix",
                "priority": "low",
                "status": "draft",
                "created_at": "2024-01-19T10:15:00Z",
                "updated_at": "2024-01-19T10:15:00Z",
                "due_date": "2024-02-15T00:00:00Z",
                "tags": ["portfolio", "usbank", "composition"],
                "responses": []
            }
        ]
    
    def _create_mock_files(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "file-1",
                "user_id": "user-1",
                "analysis_id": "analysis-1",
                "filename": "bofa_q4_2024_earnings.pdf",
                "original_filename": "bofa_q4_2024_earnings.pdf", 
                "file_path": "/uploads/bofa_q4_2024_earnings.pdf",
                "file_size": 2456789,
                "file_type": "application/pdf",
                "upload_date": "2024-01-02T10:30:00Z",
                "status": "processed",
                "description": "Bank of America Q4 2024 earnings report",
                "metadata": {
                    "pages": 45,
                    "extracted_tables": 12,
                    "key_metrics_found": 28
                }
            },
            {
                "id": "file-2",
                "user_id": "user-1", 
                "analysis_id": "analysis-1",
                "filename": "wells_fargo_financial_data.xlsx",
                "original_filename": "wells_fargo_financial_data.xlsx",
                "file_path": "/uploads/wells_fargo_financial_data.xlsx",
                "file_size": 1234567,
                "file_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "upload_date": "2024-01-03T14:15:00Z",
                "status": "processed",
                "description": "Wells Fargo financial metrics and ratios",
                "metadata": {
                    "sheets": 8,
                    "rows": 1250,
                    "columns": 15
                }
            },
            {
                "id": "file-3",
                "user_id": "user-2",
                "analysis_id": "analysis-2",
                "filename": "digital_banking_trends_2024.pdf",
                "original_filename": "digital_banking_trends_2024.pdf",
                "file_path": "/uploads/digital_banking_trends_2024.pdf", 
                "file_size": 3456789,
                "file_size": 3456789,
                "file_type": "application/pdf",
                "upload_date": "2024-01-08T09:20:00Z",
                "status": "processing",
                "description": "Industry report on digital banking transformation",
                "metadata": {
                    "pages": 67,
                    "charts": 23,
                    "data_points": 156
                }
            }
        ]
    
    # User methods
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        return next((user for user in self.users if user["id"] == user_id), None)
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return next((user for user in self.users if user["email"] == email), None)
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        return next((user for user in self.users if user["username"] == username), None)
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        return self.users
    
    # Analysis methods
    def get_analysis_by_id(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        return next((analysis for analysis in self.analyses if analysis["id"] == analysis_id), None)
    
    def get_analyses_by_user(self, user_id: str, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        user_analyses = [analysis for analysis in self.analyses if analysis["user_id"] == user_id]
        return user_analyses[skip:skip + limit]
    
    def get_all_analyses(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        return self.analyses[skip:skip + limit]
    
    def create_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        analysis_data["id"] = f"analysis-{len(self.analyses) + 1}"
        analysis_data["created_at"] = datetime.now().isoformat() + "Z"
        analysis_data["updated_at"] = analysis_data["created_at"]
        self.analyses.append(analysis_data)
        return analysis_data
    
    def update_analysis(self, analysis_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        analysis = self.get_analysis_by_id(analysis_id)
        if analysis:
            analysis.update(update_data)
            analysis["updated_at"] = datetime.now().isoformat() + "Z"
            return analysis
        return None
    
    def delete_analysis(self, analysis_id: str) -> bool:
        original_length = len(self.analyses)
        self.analyses = [analysis for analysis in self.analyses if analysis["id"] != analysis_id]
        return len(self.analyses) < original_length
    
    # Market research methods
    def get_question_by_id(self, question_id: str) -> Optional[Dict[str, Any]]:
        return next((q for q in self.market_questions if q["id"] == question_id), None)
    
    def get_questions_by_analysis(self, analysis_id: str, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        questions = [q for q in self.market_questions if q["analysis_id"] == analysis_id]
        return questions[skip:skip + limit]
    
    def get_questions_by_user(self, user_id: str, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        questions = [q for q in self.market_questions if q["user_id"] == user_id]
        return questions[skip:skip + limit]
    
    def get_all_questions(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        return self.market_questions[skip:skip + limit]
    
    def create_question(self, question_data: Dict[str, Any]) -> Dict[str, Any]:
        question_data["id"] = f"question-{len(self.market_questions) + 1}"
        question_data["created_at"] = datetime.now().isoformat() + "Z"
        question_data["updated_at"] = question_data["created_at"]
        if "responses" not in question_data:
            question_data["responses"] = []
        self.market_questions.append(question_data)
        return question_data
    
    def update_question(self, question_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        question = self.get_question_by_id(question_id)
        if question:
            question.update(update_data)
            question["updated_at"] = datetime.now().isoformat() + "Z"
            return question
        return None
    
    def add_response_to_question(self, question_id: str, response_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        question = self.get_question_by_id(question_id)
        if question:
            response_data["id"] = f"response-{len(question['responses']) + 1}"
            response_data["timestamp"] = datetime.now().isoformat() + "Z"
            question["responses"].append(response_data)
            question["updated_at"] = response_data["timestamp"]
            if question["status"] == "pending":
                question["status"] = "in-progress"
            return question
        return None
    
    # File methods
    def get_file_by_id(self, file_id: str) -> Optional[Dict[str, Any]]:
        return next((file for file in self.files if file["id"] == file_id), None)
    
    def get_files_by_analysis(self, analysis_id: str) -> List[Dict[str, Any]]:
        return [file for file in self.files if file["analysis_id"] == analysis_id]
    
    def get_files_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        return [file for file in self.files if file["user_id"] == user_id]
    
    def create_file_record(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        file_data["id"] = f"file-{len(self.files) + 1}"
        file_data["upload_date"] = datetime.now().isoformat() + "Z"
        if "status" not in file_data:
            file_data["status"] = "uploaded"
        self.files.append(file_data)
        return file_data
    
    def update_file_status(self, file_id: str, status: str) -> Optional[Dict[str, Any]]:
        file_record = self.get_file_by_id(file_id)
        if file_record:
            file_record["status"] = status
            return file_record
        return None


# Global mock data service instance
mock_data_service = MockDataService() 