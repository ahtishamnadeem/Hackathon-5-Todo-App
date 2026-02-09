---
title: Todo App Backend API
emoji: 📝
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: apache-2.0
---

# Todo App Backend API 🚀

A secure, multi-user todo management API with AI-powered chatbot assistance.

## Features

- ✅ JWT-based authentication
- ✅ User-scoped todo management
- ✅ AI chatbot with OpenAI GPT-4 and Google Gemini
- ✅ RESTful API with FastAPI
- ✅ SQLite database with SQLModel ORM
- ✅ Dark mode support
- ✅ Comprehensive API documentation

## API Documentation

Once deployed, visit `/docs` to see the interactive API documentation.

## Environment Variables

The following environment variables are required (set as Secrets in Space settings):

- `OPENAI_API_KEY`: Your OpenAI API key
- `GOOGLE_API_KEY`: Your Google AI API key
- `BETTER_AUTH_SECRET`: Secret key for JWT authentication

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLModel
- **Authentication**: JWT with bcrypt
- **AI**: OpenAI GPT-4 & Google Gemini
- **Python**: 3.13+

## Endpoints

- `GET /` - Health check
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/todos` - Get user's todos
- `POST /api/todos` - Create new todo
- `PATCH /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo
- `POST /api/{user_id}/chat` - AI chatbot

## License

Apache 2.0
