# Quick Start Guide

**Feature**: Todo Full-Stack Web Application (Phase II)
**Date**: 2026-01-08
**Target Audience**: Developers setting up local development environment

## Overview

This guide walks through setting up and running the Phase II full-stack todo application locally. The system consists of two separate services: a Python FastAPI backend and a Next.js frontend.

---

## Prerequisites

### Required Software

- **Python**: 3.13+ ([download](https://www.python.org/downloads/))
- **Node.js**: 20+ with npm ([download](https://nodejs.org/))
- **Git**: For version control ([download](https://git-scm.com/))
- **PostgreSQL Client** (optional): For direct database inspection

### Required Accounts/Services

- **Neon Database**: Free serverless PostgreSQL account ([sign up](https://neon.tech/))
- **Modern Web Browser**: Chrome, Firefox, Safari, or Edge

---

## Step 1: Clone Repository

```bash
git clone <repository-url>
cd Hackathon-5-TodoApp
git checkout 002-fullstack-web-app  # Switch to Phase II branch
```

---

## Step 2: Backend Setup

### 2.1 Navigate to Backend Directory

```bash
cd backend
```

### 2.2 Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2.3 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected dependencies** (requirements.txt):
```
fastapi==0.115.0
sqlmodel==0.0.22
pyjwt==2.9.0
bcrypt==4.2.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
uvicorn[standard]==0.30.0
alembic==1.13.0
pytest==8.3.0
httpx==0.27.0
```

### 2.4 Configure Environment Variables

Create `.env` file in `backend/` directory:

```bash
# Copy example file
cp .env.example .env

# Edit .env with your values
```

**backend/.env**:
```bash
# Database Configuration (from Neon dashboard)
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/todoapp

# JWT Configuration (MUST match frontend)
BETTER_AUTH_SECRET=your-super-secret-256-bit-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# Password Hashing
BCRYPT_WORK_FACTOR=12

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Configuration (frontend URL)
FRONTEND_URL=http://localhost:3000
```

**CRITICAL**: Generate a secure `BETTER_AUTH_SECRET`:
```bash
# Generate random 32-byte key (256-bit)
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2.5 Initialize Database

```bash
# Run migrations to create tables
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001_create_users_and_todos_tables
```

### 2.6 Start Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 2.7 Verify Backend

Open browser to [http://localhost:8000/docs](http://localhost:8000/docs)

You should see the **FastAPI automatic API documentation** (Swagger UI).

---

## Step 3: Frontend Setup

Open a **new terminal window** (keep backend running).

### 3.1 Navigate to Frontend Directory

```bash
cd frontend
```

### 3.2 Install Dependencies

```bash
npm install
```

**Expected dependencies** (package.json):
```json
{
  "dependencies": {
    "next": "^16.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "better-auth": "^latest",
    "typescript": "^5.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^19.0.0",
    "vitest": "^2.0.0",
    "playwright": "^1.40.0"
  }
}
```

### 3.3 Configure Environment Variables

Create `.env.local` file in `frontend/` directory:

```bash
# Copy example file
cp .env.local.example .env.local

# Edit .env.local with your values
```

**frontend/.env.local**:
```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# JWT Secret (MUST match backend .env)
BETTER_AUTH_SECRET=your-super-secret-256-bit-key-change-this-in-production

# Better Auth Configuration
BETTER_AUTH_URL=http://localhost:3000/api/auth
```

**CRITICAL**: `BETTER_AUTH_SECRET` MUST be identical to backend `.env`

### 3.4 Start Frontend Development Server

```bash
npm run dev
```

Expected output:
```
▲ Next.js 16.0.0
- Local:        http://localhost:3000
- Network:      http://192.168.1.x:3000

✓ Ready in 2.5s
```

### 3.5 Verify Frontend

Open browser to [http://localhost:3000](http://localhost:3000)

You should see the **todo application landing page**.

---

## Step 4: Test End-to-End Flow

### 4.1 Register New User

1. Navigate to [http://localhost:3000/register](http://localhost:3000/register)
2. Enter email: `test@example.com`
3. Enter password: `TestPass123`
4. Click **Register**
5. You should be automatically logged in and redirected to dashboard

### 4.2 Create Todo

1. On dashboard, enter todo title: `Buy groceries`
2. (Optional) Enter description: `Milk, eggs, bread`
3. Click **Add Todo**
4. Todo should appear in the list immediately

### 4.3 Update Todo

1. Click on todo title to edit
2. Change title to: `Buy groceries and fruit`
3. Click **Save**
4. Todo should update in the list

### 4.4 Mark Complete

1. Click checkbox next to todo
2. Todo should show strikethrough or visual indicator of completion

### 4.5 Delete Todo

1. Click delete button (trash icon) next to todo
2. Confirm deletion
3. Todo should disappear from list

### 4.6 Test User Isolation

1. Open **incognito/private browser window**
2. Navigate to [http://localhost:3000/register](http://localhost:3000/register)
3. Register different user: `alice@example.com` / `AlicePass123`
4. Create todos as Alice
5. Switch back to original browser window
6. Verify you **CANNOT see Alice's todos** (only your own)

**Expected Result**: Zero data leakage between users ✅ (SC-003)

---

## Step 5: Run Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
pytest tests/test_todos.py
pytest tests/test_isolation.py
```

Expected output:
```
======================== test session starts =========================
collected 25 items

tests/test_auth.py ........                                    [ 32%]
tests/test_todos.py ............                               [ 80%]
tests/test_isolation.py .....                                  [100%]

========================= 25 passed in 2.34s =========================
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm run test

# Run E2E tests
npm run test:e2e
```

---

## Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**:
```bash
# Make sure you're in backend directory
cd backend

# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Database connection error

**Error**: `could not connect to server: Connection refused`

**Solution**:
1. Verify `DATABASE_URL` in backend/.env is correct
2. Check Neon dashboard to ensure database is not paused
3. Test connection:
```bash
python -c "from app.database import engine; engine.connect(); print('Connected!')"
```

### Frontend can't reach backend

**Error**: `Failed to fetch` or `Network error` in browser console

**Solution**:
1. Verify backend is running on port 8000 (`http://localhost:8000/docs`)
2. Check `NEXT_PUBLIC_API_URL` in frontend/.env.local is correct
3. Verify CORS settings in backend allow frontend origin

### JWT token validation fails

**Error**: `Token signature verification failed` or 401 Unauthorized

**Solution**:
1. **CRITICAL**: Ensure `BETTER_AUTH_SECRET` is IDENTICAL in both:
   - `backend/.env`
   - `frontend/.env.local`
2. Regenerate secret if needed:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
3. Update both files with the same secret
4. Restart both backend and frontend servers

### Alembic migration fails

**Error**: `Target database is not up to date`

**Solution**:
```bash
# Check current migration status
alembic current

# Reset and re-run migrations
alembic downgrade base
alembic upgrade head
```

### Port already in use

**Error**: `Address already in use` (port 8000 or 3000)

**Solution**:
```bash
# Find and kill process using port
# On macOS/Linux:
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9

# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## Development Workflow

### Making Database Schema Changes

1. Edit SQLModel models in `backend/app/models/`
2. Generate migration:
```bash
cd backend
alembic revision --autogenerate -m "description of change"
```
3. Review generated migration in `alembic/versions/`
4. Apply migration:
```bash
alembic upgrade head
```

### Adding New API Endpoint

1. Define Pydantic schemas in `backend/app/schemas/`
2. Implement business logic in `backend/app/services/`
3. Create router endpoint in `backend/app/routers/`
4. Add tests in `backend/tests/`
5. Verify in Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### Adding New Frontend Component

1. Create component in `frontend/src/components/`
2. Add TypeScript types in `frontend/src/lib/types.ts`
3. Use component in pages under `frontend/src/app/`
4. Add unit tests in `frontend/tests/unit/`

---

## Useful Commands

### Backend

```bash
# Start dev server with auto-reload
uvicorn app.main:app --reload

# Run tests with verbose output
pytest -v

# Check code formatting
black app/ tests/
flake8 app/ tests/

# Generate OpenAPI JSON
python -c "from app.main import app; import json; print(json.dumps(app.openapi(), indent=2))" > openapi.json
```

### Frontend

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Type checking
npm run type-check

# Linting
npm run lint
```

### Database

```bash
# Connect to Neon database (psql)
psql "postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/todoapp"

# View tables
\dt

# View table schema
\d users
\d todos

# Query todos
SELECT * FROM todos ORDER BY created_at DESC LIMIT 10;
```

---

## Environment Variables Reference

### Backend (.env)

| Variable              | Required | Description                                    | Example                              |
|-----------------------|----------|------------------------------------------------|--------------------------------------|
| DATABASE_URL          | Yes      | PostgreSQL connection string                   | postgresql://user:pass@host/db       |
| BETTER_AUTH_SECRET    | Yes      | JWT signing secret (must match frontend)       | 64-char hex string                   |
| JWT_ALGORITHM         | Yes      | JWT algorithm (use HS256)                      | HS256                                |
| JWT_EXPIRATION_DAYS   | Yes      | Token validity period                          | 7                                    |
| BCRYPT_WORK_FACTOR    | Yes      | Password hashing cost (10-14 recommended)      | 12                                   |
| HOST                  | No       | Server bind address                            | 0.0.0.0                              |
| PORT                  | No       | Server port                                    | 8000                                 |
| FRONTEND_URL          | Yes      | Frontend origin for CORS                       | http://localhost:3000                |

### Frontend (.env.local)

| Variable              | Required | Description                                    | Example                              |
|-----------------------|----------|------------------------------------------------|--------------------------------------|
| NEXT_PUBLIC_API_URL   | Yes      | Backend API base URL                           | http://localhost:8000                |
| BETTER_AUTH_SECRET    | Yes      | JWT signing secret (must match backend)        | 64-char hex string                   |
| BETTER_AUTH_URL       | Yes      | Better Auth endpoint                           | http://localhost:3000/api/auth       |

---

## Success Criteria Verification

After completing this quickstart, verify these requirements are met:

- ✅ **SC-001**: Registration and login complete within 1 minute
- ✅ **SC-002**: Todo creation appears in list within 2 seconds
- ✅ **SC-003**: Multi-user isolation (incognito test shows no data leakage)
- ✅ **SC-004**: API responses within 500ms (check Network tab)
- ✅ **SC-005**: All CRUD operations work without errors
- ✅ **SC-006**: Invalid login attempts are rejected
- ✅ **SC-007**: Session persists across browser restart
- ✅ **SC-008**: Multiple users can operate simultaneously
- ✅ **SC-009**: Graceful error handling (test by stopping backend)
- ✅ **SC-010**: Weak passwords are rejected during registration

---

## Next Steps

Now that your local environment is running:

1. Review API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
2. Review [data-model.md](data-model.md) for database schema details
3. Review [contracts/auth.md](contracts/auth.md) for authentication flow
4. Review [contracts/errors.md](contracts/errors.md) for error handling
5. Proceed to `/sp.tasks` to generate implementation task breakdown

---

## Support

If you encounter issues not covered in Troubleshooting:

1. Check backend logs in terminal where uvicorn is running
2. Check browser console (F12) for frontend errors
3. Verify both .env files have correct configuration
4. Ensure all services (backend, frontend, database) are running
5. Review [plan.md](plan.md) for architecture details

---

## Summary

**Setup Time**: ~15 minutes
**Services Running**: 3 (Backend API, Frontend UI, Neon Database)
**Ports Used**: 8000 (backend), 3000 (frontend)
**Database**: Neon Serverless PostgreSQL (remote)
**Environment Files**: backend/.env, frontend/.env.local

**Quick Verification**:
```bash
# Backend health check
curl http://localhost:8000/docs

# Frontend running
curl http://localhost:3000

# Database connected
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM users;"
```

All systems operational ✅ - Ready for implementation!
