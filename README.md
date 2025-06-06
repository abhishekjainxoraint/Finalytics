# FP&A Analysis Application

A comprehensive AI-powered Financial Planning & Analysis platform designed for banking analysts to compare internal financial performance with competitors using both internal documents and publicly available financial reports.

## 🏗️ Architecture Overview

This application consists of two main components:

### Frontend (React + TypeScript + Vite)
- **Location**: `./Frontend/`
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Library**: shadcn/ui with Tailwind CSS
- **State Management**: React Query for server state
- **Routing**: React Router DOM

### Backend (Node.js + TypeScript + Express)
- **Location**: `./Backend/`
- **Runtime**: Node.js with TypeScript
- **Framework**: Express.js
- **Database**: MongoDB with Mongoose
- **Cache**: Redis
- **Real-time**: Socket.IO
- **Background Jobs**: Bull Queue
- **Authentication**: JWT

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18 or higher)
- **MongoDB** (v5.0 or higher)
- **Redis** (v6.0 or higher)
- **npm** or **yarn**

### 1. Clone the Repository

```bash
git clone <repository-url>
cd bank-analysis-forge-main
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd Backend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env
# Edit .env file with your configuration

# Start the backend server
npm run dev
```

The backend will start on `http://localhost:5000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd Frontend

# Install dependencies
npm install

# Start the frontend development server
npm run dev
```

The frontend will start on `http://localhost:3000`

## 📋 Features

### 🏠 Dashboard & Navigation
- **Role-based UI**: Different interfaces for Analyst, Reviewer, and Admin roles
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dark/Light Theme**: User preference-based theming

### 📊 Analysis Management
- **Create Analysis**: Define analysis parameters, upload documents, add competitors
- **Progress Tracking**: Real-time progress updates with AI agent status
- **Analysis History**: View, filter, and manage all created analyses

### 📈 Financial Dashboards
- **Income Statement Analysis**: Revenue growth, expense ratios, profitability metrics
- **Balance Sheet Analysis**: Asset composition, liability structure, capital ratios
- **Cash Flow Analysis**: Operating cash flow trends and analysis
- **KPIs & Ratios**: Non-performing loans, customer metrics, liquidity ratios
- **MD&A Analysis**: Strategic priorities, risk factors, outlook analysis

### 🔧 Correction Workflow
- **AI Output Correction**: Users can correct AI-generated insights
- **Document Reference**: Link corrections to specific document pages
- **Review Process**: Track correction status and reviewer feedback

### 🔍 Market Research Q&A
- **External Research**: Submit questions to market research analysts
- **Response Tracking**: View responses and attachments
- **AI Summarization**: Automated summaries of research responses

### 💬 AI Chatbot
- **Contextual Queries**: Ask questions about your financial documents
- **Source Citations**: Responses include document references and page numbers
- **Analysis Context**: Chatbot understands the current analysis context

### 📁 Document Management
- **File Upload**: Support for PDF, Word, Excel documents
- **GridFS Storage**: Efficient storage of large financial documents
- **Text Extraction**: Automatic text extraction for AI processing

## 🔐 User Roles & Permissions

### 👨‍💼 FP&A Analyst
- Create and manage financial analyses
- Upload internal and competitor documents
- Generate AI-powered insights
- Submit corrections and market research questions
- Full access to all analysis features

### 👨‍💻 Reviewer
- Read-only access to analyses
- Add comments and feedback
- Review correction submissions
- Cannot create or modify analyses

### 👨‍💼 Admin
- Full system access
- User management capabilities
- System configuration
- Access to all analyses across users

## 🛠️ Technology Stack

### Frontend Technologies
- **React 18** - Modern React with hooks and concurrent features
- **TypeScript** - Type safety and better developer experience
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - High-quality React components
- **React Query** - Server state management
- **React Router** - Client-side routing
- **Recharts** - Chart and visualization library

### Backend Technologies
- **Node.js** - JavaScript runtime
- **Express.js** - Web application framework
- **TypeScript** - Type safety for backend code
- **MongoDB** - NoSQL database
- **Mongoose** - MongoDB object modeling
- **Redis** - In-memory data structure store
- **Socket.IO** - Real-time bidirectional communication
- **Bull** - Background job processing
- **JWT** - JSON Web Token authentication
- **Multer** - File upload handling
- **GridFS** - File storage in MongoDB

## 📡 API Documentation

### Authentication Endpoints
```
POST /api/auth/register    - Register new user
POST /api/auth/login       - User login
GET  /api/auth/profile     - Get user profile
PUT  /api/auth/profile     - Update profile
PUT  /api/auth/change-password - Change password
```

### Analysis Endpoints
```
GET    /api/analysis           - Get all analyses
POST   /api/analysis           - Create new analysis
GET    /api/analysis/:id       - Get analysis by ID
PUT    /api/analysis/:id       - Update analysis
DELETE /api/analysis/:id       - Delete analysis
POST   /api/analysis/:id/generate - Start analysis generation
```

### Document Endpoints
```
POST   /api/documents/upload   - Upload documents
GET    /api/documents          - Get documents list
GET    /api/documents/:id      - Get document details
DELETE /api/documents/:id      - Delete document
```

For complete API documentation, see `Backend/README.md`

## 🔄 Real-time Features

The application uses Socket.IO for real-time updates:

- **Analysis Progress**: Live updates during AI processing
- **Collaboration**: Real-time notifications for team members
- **Status Updates**: Instant feedback on system operations

## 🚀 Deployment

### Development
```bash
# Backend
cd Backend && npm run dev

# Frontend (new terminal)
cd Frontend && npm run dev
```

### Production Build
```bash
# Backend
cd Backend
npm run build
npm start

# Frontend
cd Frontend
npm run build
npm run preview
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
# Database
MONGODB_URI=mongodb://localhost:27017/fpa-analysis
REDIS_URL=redis://localhost:6379

# Server
PORT=5000
NODE_ENV=development

# Authentication
JWT_SECRET=your-secret-key
JWT_EXPIRES_IN=7d

# AI Services
OPENAI_API_KEY=your-openai-key

# CORS
FRONTEND_URL=http://localhost:3000
```

#### Frontend
```env
VITE_API_URL=http://localhost:5000/api
VITE_SOCKET_URL=http://localhost:5000
```

## 🧪 Testing

### Backend Tests
```bash
cd Backend
npm test
```

### Frontend Tests
```bash
cd Frontend
npm test
```

## 📝 Development Guidelines

### Code Style
- **TypeScript** for type safety
- **ESLint** for code linting
- **Prettier** for code formatting
- **Conventional Commits** for commit messages

### Project Structure
- **Modular Architecture**: Clear separation of concerns
- **Path Aliases**: Clean import statements using @/ prefix
- **Component Organization**: Logical grouping of UI components
- **Service Layer**: Business logic separated from UI components

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Check the documentation in `Frontend/README.md` and `Backend/README.md`
- Review the API documentation
- Contact the development team

## 🔮 Future Enhancements

- **Advanced AI Models**: Integration with specialized financial AI models
- **Data Visualization**: Enhanced charting and visualization capabilities
- **Mobile App**: Native mobile application for on-the-go analysis
- **Integration APIs**: Connect with external financial data providers
- **Advanced Analytics**: Machine learning-powered predictive analytics

---

**Built with ❤️ for Financial Analysts**
