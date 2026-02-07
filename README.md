# GIAIC HACKATHON (5 - PHASES)
# Multi-Phase Todo Application - Phase II

<div align="center">

[![Next.js](https://img.shields.io/badge/Next.js-16+-black?logo=next.js&logoColor=white)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Phase](https://img.shields.io/badge/Phase-II-yellow.svg)](https://github.com/yourusername/hackathon-5-todoapp)

**🎯 Full-Stack Todo App | JWT Auth | Modern UI | Clean Architecture**

</div>

## 🌟 Overview

Welcome to the **Multi-Phase Todo Application**! This project represents the successful completion of **Phase II** - a full-stack web application with authentication, persistent storage, and a modern user interface.

Built with Next.js 16, FastAPI, and clean architecture principles, this application demonstrates a production-ready todo management system with security-first design.

## ✨ Features

### Core Functionality
- **📋 Task Management**: Create, read, update, and delete todos
- **✅ Task Completion**: Mark tasks as complete/incomplete
- **🎯 Priority Levels**: Low, Medium, High priority indicators
- **📝 Rich Details**: Add titles and descriptions to tasks
- **🔍 Real-time Updates**: Instant UI updates on all operations

### User Experience
- **🎨 Modern UI**: Beautiful, responsive design with Tailwind CSS
- **🌙 Dark Mode**: Full dark mode support with smooth transitions
- **💀 Skeleton Loaders**: Professional loading states
- **📭 Empty States**: Engaging empty state designs
- **⚠️ Confirmation Dialogs**: Safe delete operations with modals
- **🎭 Animations**: Smooth transitions with Framer Motion

### Security & Authentication
- **🔐 JWT Authentication**: Secure token-based auth
- **👤 User Isolation**: Each user sees only their own tasks
- **🛡️ Input Validation**: Comprehensive validation on frontend and backend
- **🔒 Password Hashing**: Bcrypt password encryption
- **🚫 CORS Protection**: Configured CORS policies

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- Next.js 16 (App Router, React Server Components)
- TypeScript
- Tailwind CSS
- Framer Motion
- Custom hooks for state management

**Backend:**
- FastAPI (Python 3.13+)
- SQLModel (ORM)
- SQLite (Development database)
- JWT authentication
- Pydantic validation

### Project Structure

```
hackathon-5-todoapp/
├── frontend/              # Next.js application
│   ├── app/              # App Router pages
│   │   ├── components/   # Reusable UI components
│   │   ├── todos/        # Todo management page
│   │   ├── login/        # Authentication pages
│   │   └── dashboard/    # User dashboard
│   └── src/
│       ├── hooks/        # Custom React hooks
│       └── lib/          # API client & utilities
│
├── backend/              # FastAPI application
│   └── app/
│       ├── models/       # SQLModel entities
│       ├── schemas/      # Pydantic schemas
│       ├── routers/      # API endpoints
│       ├── services/     # Business logic
│       ├── middleware/   # Auth middleware
│       └── utils/        # Helper functions
│
└── docs/                 # Documentation
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.13+
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hackathon-5-todoapp.git
   cd hackathon-5-todoapp
   ```

2. **Setup Backend**
   ```bash
   cd backend

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Copy environment file
   cp .env.example .env

   # Edit .env and set your SECRET_KEY
   # Generate with: python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Setup Frontend**
   ```bash
   cd frontend

   # Install dependencies
   npm install

   # Copy environment file
   cp .env.local.example .env.local

   # Edit .env.local and set NEXT_PUBLIC_API_URL
   ```

### Running the Application

1. **Start Backend** (Terminal 1)
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --port 8001 --host 0.0.0.0
   ```
   Backend will run at: `http://localhost:8001`

2. **Start Frontend** (Terminal 2)
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend will run at: `http://localhost:3000`

3. **Access the Application**
   - Open browser: `http://localhost:3000`
   - Register a new account
   - Start managing your todos!

## 📖 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8001/docs`
- **ReDoc**: `http://localhost:8001/redoc`

### Key Endpoints

```
POST   /api/auth/register    - Register new user
POST   /api/auth/login       - Login user
GET    /api/auth/me          - Get current user
POST   /api/auth/logout      - Logout user

GET    /api/todos            - Get all user's todos
POST   /api/todos            - Create new todo
GET    /api/todos/{id}       - Get specific todo
PATCH  /api/todos/{id}       - Update todo
DELETE /api/todos/{id}       - Delete todo
```

## 🔒 Environment Variables

### Backend (.env)

```bash
# Database (SQLite for development)
DATABASE_URL=sqlite:///./todo_test.db

# JWT Secret (REQUIRED - Generate a secure key!)
BETTER_AUTH_SECRET=your-secret-key-here-min-64-chars

# JWT Settings
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# Server
HOST=0.0.0.0
PORT=8001

# CORS
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.local)

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8001

# Auth Configuration (must match backend)
BETTER_AUTH_SECRET=your-secret-key-here-min-64-chars
BETTER_AUTH_URL=http://localhost:3000
```

## 🎯 Phase II Completion

Phase II successfully delivers:

- ✅ Full-stack web application (Next.js + FastAPI)
- ✅ JWT-based authentication system
- ✅ User registration and login
- ✅ Persistent SQLite database
- ✅ User-scoped data isolation
- ✅ Priority levels for tasks
- ✅ Modern, responsive UI with dark mode
- ✅ Professional UX (skeleton loaders, empty states, confirmations)
- ✅ RESTful API with OpenAPI documentation
- ✅ Input validation and error handling
- ✅ Security-first architecture

## 🔄 Future Phases

This foundation enables future phases:

- **Phase III**: AI-powered chatbot interface with natural language processing
- **Phase IV**: Local Kubernetes deployment with containerization
- **Phase V**: Advanced cloud deployment (AWS/Azure/GCP)

## 🛡️ Security Features

- **Password Hashing**: Bcrypt with configurable work factor
- **JWT Tokens**: Secure token-based authentication
- **User Isolation**: Database-level user data separation
- **Input Validation**: Pydantic schemas on backend, TypeScript on frontend
- **CORS Protection**: Configured allowed origins
- **SQL Injection Prevention**: SQLModel parameterized queries
- **Environment Variables**: Secrets stored in .env files (not committed)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Spec-Driven Development](https://spec-driven.com) methodology
- Clean Architecture principles
- Next.js 16 and FastAPI frameworks
- Tailwind CSS and Framer Motion for UI

---

<div align="center">

**Made with ❤️ during Hackathon-5**

[Back to Top](#multi-phase-todo-application---phase-ii)

</div>