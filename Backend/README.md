# FP&A Intelligence Backend

A FastAPI-based backend for the Banking Analysis Platform providing competitive intelligence and financial analytics.

## Features

- 🚀 **FastAPI** with async/await support
- 🔐 **JWT Authentication** with refresh tokens
- 📊 **MongoDB** for data storage
- ⚡ **Redis** for caching and sessions
- 📁 **File Upload** support (PDF, Excel, CSV)
- 🎯 **Sorting & Filtering** for all data endpoints
- 📈 **Real-time Analytics** and dashboard data
- 🤖 **AI Integration** ready (OpenAI compatible)
- 🐳 **Docker** containerized
- 📝 **Comprehensive API Documentation**

## Quick Start

### Using Docker (Recommended)

1. **Clone and navigate to backend:**
   ```bash
   cd Backend
   ```

2. **Set up environment:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Start with Docker Compose:**
   ```bash
   cd ..
   docker-compose up backend mongodb redis
   ```

### Local Development

1. **Install Python 3.11+**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Start MongoDB and Redis:**
   ```bash
   # Using Docker
   docker run -d -p 27017:27017 --name mongodb mongo:6.0
   docker run -d -p 6379:6379 --name redis redis:7-alpine
   ```

5. **Run the application:**
   ```bash
   uvicorn main:app --reload --port 5000
   ```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/change-password` - Change password

### Users (Admin Only)
- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/{user_id}` - Get user details
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Analyses
- `POST /api/v1/analyses/` - Create analysis
- `GET /api/v1/analyses/` - List analyses (with sorting/filtering)
- `GET /api/v1/analyses/{analysis_id}` - Get analysis details
- `PUT /api/v1/analyses/{analysis_id}` - Update analysis
- `DELETE /api/v1/analyses/{analysis_id}` - Delete analysis
- `POST /api/v1/analyses/bulk-delete` - Bulk delete analyses
- `GET /api/v1/analyses/{analysis_id}/dashboard` - Get dashboard data
- `POST /api/v1/analyses/{analysis_id}/generate` - Generate AI insights

### Market Research
- `POST /api/v1/market-research/questions` - Create research question
- `GET /api/v1/market-research/questions` - List questions (with sorting)
- `GET /api/v1/market-research/questions/{question_id}` - Get question details
- `PUT /api/v1/market-research/questions/{question_id}` - Update question
- `DELETE /api/v1/market-research/questions/{question_id}` - Delete question
- `POST /api/v1/market-research/questions/{question_id}/responses` - Add response
- `POST /api/v1/market-research/questions/bulk-action` - Bulk actions
- `GET /api/v1/market-research/metrics` - Get research metrics

### Files
- `POST /api/v1/files/upload` - Upload file
- `GET /api/v1/files/` - List user files
- `GET /api/v1/files/{file_id}` - Download file
- `DELETE /api/v1/files/{file_id}` - Delete file
- `GET /api/v1/files/{file_id}/info` - Get file info

## Sorting & Filtering

All list endpoints support comprehensive sorting and filtering:

### Query Parameters

**Analyses (`/api/v1/analyses/`):**
- `sort_by`: `created_at`, `name`, `status`, `updated_at` (default: `created_at`)
- `sort_order`: `asc`, `desc` (default: `desc`)
- `status`: `draft`, `in-progress`, `completed`, `failed`
- `search`: Search in name, description, period
- `page`: Page number (default: 1)
- `size`: Items per page (default: 10, max: 100)

**Market Research Questions (`/api/v1/market-research/questions`):**
- `sort_by`: `created_at`, `status`, `analysis_id`, `user_id` (default: `created_at`)
- `sort_order`: `asc`, `desc` (default: `desc`)
- `analysis_id`: Filter by specific analysis
- `status`: `pending`, `answered`, `closed`
- `search`: Search in question, dashboard, report
- `page`: Page number (default: 1)
- `size`: Items per page (default: 10, max: 100)

### Example Requests

```bash
# Get analyses sorted by name (ascending)
GET /api/v1/analyses/?sort_by=name&sort_order=asc

# Get completed analyses with search
GET /api/v1/analyses/?status=completed&search=Q4%202024

# Get pending research questions for specific analysis
GET /api/v1/market-research/questions/?analysis_id=123&status=pending

# Get questions sorted by status
GET /api/v1/market-research/questions/?sort_by=status&sort_order=asc
```

## Environment Variables

Key configuration options:

```bash
# Application
ENVIRONMENT=development
PORT=5000

# Database
MONGODB_URI=mongodb://admin:password123@localhost:27017/fpa-analysis?authSource=admin
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External Services
OPENAI_API_KEY=your-openai-key

# File Upload
MAX_FILE_SIZE=52428800  # 50MB
UPLOAD_DIR=uploads
```

## Development

### Code Structure

```
Backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── app/
│   ├── core/              # Core functionality
│   │   ├── config.py      # Configuration management
│   │   ├── database.py    # MongoDB connection
│   │   ├── redis.py       # Redis connection
│   │   └── security.py    # Authentication & security
│   ├── models/            # Pydantic data models
│   │   ├── user.py        # User models
│   │   ├── analysis.py    # Analysis models
│   │   └── market_research.py  # Market research models
│   └── api/v1/           # API routes
│       ├── api.py         # Main router
│       └── endpoints/     # Individual endpoint modules
├── uploads/               # File upload directory
└── README.md             # This file
```

### Adding New Endpoints

1. Create model in `app/models/`
2. Create endpoint in `app/api/v1/endpoints/`
3. Add router to `app/api/v1/api.py`
4. Update database indexes if needed in `app/core/database.py`

### Database Collections

- **users** - User accounts and authentication
- **analyses** - Financial analysis documents
- **market_questions** - Market research questions and responses
- **files** - Uploaded file metadata

## Production Deployment

### Docker Compose

The backend is designed to work with the provided `docker-compose.yml`:

```bash
# Start all services
docker-compose up -d

# Backend only with dependencies
docker-compose up backend mongodb redis
```

### Environment Setup

1. Copy `env.example` to `.env`
2. Update production values:
   - `SECRET_KEY` - Use a secure random key
   - `MONGODB_URI` - Production MongoDB connection
   - `REDIS_URL` - Production Redis connection
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `ENVIRONMENT=production`

### Health Checks

- **Application**: `GET /health`
- **Database**: Automatic connection testing on startup
- **Redis**: Automatic connection testing on startup

## API Documentation

When running in development mode:
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

## Performance Features

- **Async/Await**: Full async support for high concurrency
- **Connection Pooling**: Optimized database connections
- **Redis Caching**: Automatic caching for frequently accessed data
- **Rate Limiting**: Configurable rate limits per endpoint
- **Database Indexes**: Optimized queries with proper indexing
- **Pagination**: All list endpoints support pagination
- **File Streaming**: Efficient file upload/download handling

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: BCrypt password hashing
- **Rate Limiting**: Protection against abuse
- **CORS Configuration**: Secure cross-origin requests
- **Input Validation**: Comprehensive request validation
- **File Type Validation**: Secure file upload restrictions
- **SQL Injection Protection**: MongoDB injection prevention

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 