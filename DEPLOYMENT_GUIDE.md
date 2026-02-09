# 🚀 Complete Deployment Guide - Todo App

## 📋 Overview
This guide will walk you through:
1. Testing your website locally
2. Deploying backend to Hugging Face Spaces
3. Connecting frontend to the deployed backend
4. Deploying frontend to Vercel

---

## Phase 1: Test Website Locally 🧪

### Step 1.1: Test Backend Locally

#### 1. Open a new terminal and navigate to backend directory
```bash
cd C:\Users\HP\Links\Desktop\Hackathon-5-TodoApp\backend
```

#### 2. Create/activate Python virtual environment (if not already done)
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Verify your .env file has all required variables
Your backend\.env should have:
```
DATABASE_URL=sqlite:///./todo_test.db
BETTER_AUTH_SECRET=your-secret-key-here-min-64-chars
HOST=0.0.0.0
PORT=8001
FRONTEND_URL=http://localhost:3000
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
GOOGLE_API_KEY=your-google-api-key-here
GOOGLE_MODEL=gemini-2.5-flash
```

#### 5. Start the backend server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

#### 6. Verify backend is running
- Open browser: http://localhost:8001
- You should see: `{"success": true, "data": {"message": "Todo API v2.0.0", ...}}`
- Check API docs: http://localhost:8001/docs

✅ **Backend is ready when you see the API documentation page!**

---

### Step 1.2: Test Frontend Locally

#### 1. Open a NEW terminal (keep backend running) and navigate to frontend
```bash
cd C:\Users\HP\Links\Desktop\Hackathon-5-TodoApp\frontend
```

#### 2. Install dependencies (if not already done)
```bash
npm install
```

#### 3. Verify your .env.local file
Your frontend\.env.local should have:
```
NEXT_PUBLIC_API_URL=http://localhost:8001
BETTER_AUTH_SECRET=55dbd04fbc20627e60ca799678b9c33087e099cdbc30c5d6468dbdaf95ce0522
BETTER_AUTH_URL=http://localhost:3000
```

#### 4. Start the frontend development server
```bash
npm run dev
```

#### 5. Test the application
- Open browser: http://localhost:3000
- You should see the homepage with dark theme by default
- Click "Get Started" or "Sign In"
- Try to register a new account
- Try to login
- Create some todos
- Test the AI chatbot (click the chat icon in bottom-right)

✅ **If everything works, you're ready for deployment!**

---

## Phase 2: Deploy Backend to Hugging Face 🤗

### Step 2.1: Prepare Backend for Hugging Face

#### 1. Create a new file: `backend/app.py` (Hugging Face entry point)
```bash
cd C:\Users\HP\Links\Desktop\Hackathon-5-TodoApp\backend
```

Create `app.py` with this content:
```python
"""
Hugging Face Spaces entry point for FastAPI application.
"""
import os
from app.main import app

# Hugging Face Spaces uses PORT environment variable
port = int(os.getenv("PORT", 7860))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
```

#### 2. Create `backend/requirements-hf.txt` (Hugging Face specific)
```txt
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlmodel==0.0.22
pyjwt==2.9.0
bcrypt==4.2.0
python-multipart==0.0.9
email-validator==2.1.0
openai==1.54.0
google-generativeai==0.8.3
python-dotenv==1.0.0
```

#### 3. Create `backend/.env.production` (for Hugging Face)
```bash
DATABASE_URL=sqlite:///./data/todos.db
BETTER_AUTH_SECRET=your-secret-key-here-min-64-chars
HOST=0.0.0.0
PORT=7860
FRONTEND_URL=https://your-app.vercel.app
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
GOOGLE_API_KEY=your-google-api-key-here
GOOGLE_MODEL=gemini-2.5-flash
```

---

### Step 2.2: Deploy to Hugging Face Spaces

#### 1. Go to Hugging Face Spaces
- Visit: https://huggingface.co/spaces
- Click "Create new Space"

#### 2. Configure your Space
- **Space name**: `todo-app-backend` (or your preferred name)
- **License**: Apache 2.0
- **Select SDK**: Docker
- **Space hardware**: CPU basic (free tier)
- **Visibility**: Public
- Click "Create Space"

#### 3. Create Dockerfile for Hugging Face
In your backend directory, create `Dockerfile.hf`:
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements-hf.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for SQLite
RUN mkdir -p /app/data

# Expose Hugging Face default port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the application
CMD ["python", "app.py"]
```

#### 4. Upload files to Hugging Face Space

**Option A: Using Git (Recommended)**
```bash
cd C:\Users\HP\Links\Desktop\Hackathon-5-TodoApp\backend

# Initialize git if not already done
git init

# Add Hugging Face remote (replace USERNAME and SPACE_NAME)
git remote add hf https://huggingface.co/spaces/USERNAME/SPACE_NAME

# Create .gitignore for backend
echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
echo "venv/" >> .gitignore
echo ".env" >> .gitignore
echo "todo_test.db" >> .gitignore
echo "data/" >> .gitignore

# Add files
git add .
git commit -m "Initial backend deployment"

# Push to Hugging Face
git push hf main
```

**Option B: Using Web Interface**
1. Click "Files" tab in your Space
2. Click "Add file" → "Upload files"
3. Upload these files from backend directory:
   - `app/` (entire folder)
   - `requirements-hf.txt` (rename to `requirements.txt`)
   - `Dockerfile.hf` (rename to `Dockerfile`)
   - `app.py`
   - `.env.production` (rename to `.env`)

#### 5. Configure Environment Variables (Secrets)
1. Go to your Space settings
2. Click "Variables and secrets"
3. Add these secrets (use your actual API keys):
   - `OPENAI_API_KEY`: your-openai-api-key-here
   - `GOOGLE_API_KEY`: your-google-api-key-here
   - `BETTER_AUTH_SECRET`: your-secret-key-here-min-64-chars

#### 6. Wait for deployment
- Hugging Face will automatically build and deploy your Space
- This takes 5-10 minutes
- Watch the "Logs" tab for progress

#### 7. Get your backend URL
Once deployed, your backend URL will be:
```
https://USERNAME-SPACE_NAME.hf.space
```
Example: `https://johndoe-todo-app-backend.hf.space`

#### 8. Test your deployed backend
- Visit: `https://YOUR-SPACE-URL.hf.space`
- You should see the API response
- Visit: `https://YOUR-SPACE-URL.hf.space/docs`
- You should see the API documentation

✅ **Copy this URL - you'll need it for the frontend!**

---

## Phase 3: Connect Frontend to Deployed Backend 🔗

### Step 3.1: Update Frontend Environment Variables

#### 1. Update frontend/.env.local for local testing with deployed backend
```bash
cd C:\Users\HP\Links\Desktop\Hackathon-5-TodoApp\frontend
```

Edit `.env.local`:
```
# Replace with your Hugging Face backend URL
NEXT_PUBLIC_API_URL=https://YOUR-SPACE-URL.hf.space

BETTER_AUTH_SECRET=55dbd04fbc20627e60ca799678b9c33087e099cdbc30c5d6468dbdaf95ce0522
BETTER_AUTH_URL=http://localhost:3000
```

#### 2. Test locally with deployed backend
```bash
npm run dev
```

- Open: http://localhost:3000
- Try to register and login
- If it works, you're ready for Vercel deployment!

---

## Phase 4: Deploy Frontend to Vercel 🌐

### Step 4.1: Prepare Frontend for Vercel

#### 1. Create `.env.production` in frontend directory
```
NEXT_PUBLIC_API_URL=https://YOUR-SPACE-URL.hf.space
BETTER_AUTH_SECRET=55dbd04fbc20627e60ca799678b9c33087e099cdbc30c5d6468dbdaf95ce0522
BETTER_AUTH_URL=https://your-app.vercel.app
```

#### 2. Create `vercel.json` in frontend directory
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["iad1"]
}
```

#### 3. Update backend CORS to allow Vercel domain
You'll need to update this after getting your Vercel URL.

---

### Step 4.2: Deploy to Vercel

#### 1. Install Vercel CLI (if not installed)
```bash
npm install -g vercel
```

#### 2. Login to Vercel
```bash
vercel login
```

#### 3. Deploy from frontend directory
```bash
cd C:\Users\HP\Links\Desktop\Hackathon-5-TodoApp\frontend
vercel
```

Follow the prompts:
- **Set up and deploy?** Yes
- **Which scope?** Your account
- **Link to existing project?** No
- **Project name?** todo-app (or your preferred name)
- **Directory?** ./
- **Override settings?** No

#### 4. Set environment variables in Vercel
```bash
# Set production environment variables
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://YOUR-SPACE-URL.hf.space

vercel env add BETTER_AUTH_SECRET production
# Enter: 55dbd04fbc20627e60ca799678b9c33087e099cdbc30c5d6468dbdaf95ce0522
```

#### 5. Deploy to production
```bash
vercel --prod
```

#### 6. Get your Vercel URL
After deployment completes, you'll get a URL like:
```
https://todo-app-xyz123.vercel.app
```

✅ **Copy this URL!**

---

### Step 4.3: Update Backend CORS for Vercel

#### 1. Update backend/app/main.py
Add your Vercel URL to the allowed_origins list:

```python
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:30000",
    "http://127.0.0.1:50129",
    "http://127.0.0.1:64865",
    "https://your-app-xyz123.vercel.app",  # Add your Vercel URL
]
```

#### 2. Redeploy backend to Hugging Face
```bash
cd C:\Users\HP\Links\Desktop\Hackathon-5-TodoApp\backend
git add app/main.py
git commit -m "Add Vercel URL to CORS"
git push hf main
```

#### 3. Wait for Hugging Face to rebuild (2-3 minutes)

---

## Phase 5: Final Testing 🎉

### Test your deployed application:

1. **Visit your Vercel URL**: https://your-app.vercel.app
2. **Test Registration**: Create a new account
3. **Test Login**: Sign in with your account
4. **Test Todos**: Create, complete, and delete todos
5. **Test AI Chatbot**: Click the chat icon and ask questions
6. **Test Dark Mode**: Should be dark by default, toggle to light
7. **Test Mobile**: Open on your phone to test responsive design

---

## 🔧 Troubleshooting

### Backend Issues:

**Problem**: Backend not starting on Hugging Face
- Check logs in Hugging Face Space
- Verify all environment variables are set
- Check Dockerfile syntax

**Problem**: CORS errors
- Verify Vercel URL is in allowed_origins
- Check backend logs for CORS errors
- Ensure backend is redeployed after CORS changes

### Frontend Issues:

**Problem**: "Failed to fetch" errors
- Verify NEXT_PUBLIC_API_URL is correct
- Check if backend is running
- Test backend URL directly in browser

**Problem**: Build fails on Vercel
- Check build logs in Vercel dashboard
- Verify all dependencies are in package.json
- Check for TypeScript errors

### Database Issues:

**Problem**: Data not persisting on Hugging Face
- Hugging Face Spaces may reset on rebuild
- Consider upgrading to persistent storage
- Or use external database (PostgreSQL on Railway/Supabase)

---

## 📝 Important URLs to Save

After deployment, save these URLs:

1. **Backend (Hugging Face)**: https://YOUR-SPACE-URL.hf.space
2. **Frontend (Vercel)**: https://your-app.vercel.app
3. **Backend API Docs**: https://YOUR-SPACE-URL.hf.space/docs
4. **Hugging Face Space**: https://huggingface.co/spaces/USERNAME/SPACE_NAME
5. **Vercel Dashboard**: https://vercel.com/dashboard

---

## 🎯 Next Steps (Optional)

1. **Custom Domain**: Add custom domain in Vercel settings
2. **Analytics**: Add Vercel Analytics
3. **Monitoring**: Set up error tracking (Sentry)
4. **Database**: Migrate to PostgreSQL for production
5. **CI/CD**: Set up automatic deployments from GitHub

---

## ✅ Deployment Checklist

- [ ] Backend tested locally
- [ ] Frontend tested locally
- [ ] Backend deployed to Hugging Face
- [ ] Backend URL obtained
- [ ] Frontend environment variables updated
- [ ] Frontend tested with deployed backend
- [ ] Frontend deployed to Vercel
- [ ] Vercel URL obtained
- [ ] Backend CORS updated with Vercel URL
- [ ] Backend redeployed
- [ ] Full application tested in production
- [ ] Mobile responsiveness verified
- [ ] Dark mode working
- [ ] AI chatbot working

---

**🎉 Congratulations! Your Todo App is now live!**
