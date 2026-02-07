# API Documentation

**Feature**: Todo Full-Stack Web Application (Phase II)
**Last Updated**: 2026-01-08

## Overview

This document provides comprehensive API documentation for the Todo application backend. The API follows RESTful principles with standard HTTP methods and status codes.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: TBD

## Authentication

All endpoints except `/api/auth/register`, `/api/auth/login` require JWT authentication.

**Authentication Header**:
```
Authorization: Bearer <jwt_token>
```

JWT tokens are issued upon successful registration or login and stored in httpOnly cookies on the frontend.

## API Endpoints

### Authentication Endpoints

See [authentication.md](authentication.md) for detailed authentication flow documentation.

#### POST /api/auth/register
Register a new user account.

#### POST /api/auth/login
Authenticate user and issue JWT token.

#### POST /api/auth/logout
Terminate user session and clear token.

### Todo Endpoints

#### GET /api/todos
Retrieve all todos for authenticated user.

#### POST /api/todos
Create a new todo.

#### GET /api/todos/{id}
Retrieve a specific todo by ID.

#### PATCH /api/todos/{id}
Update a todo's title, description, or completion status.

#### DELETE /api/todos/{id}
Permanently delete a todo.

## Error Handling

See [error-handling.md](error-handling.md) for complete error response format and error codes.

## Interactive Documentation

The FastAPI backend provides automatically generated interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- View all available endpoints
- See request/response schemas
- Test API calls directly from the browser
- View authentication requirements

## OpenAPI Specification

The complete OpenAPI 3.0 specification is available at:
- **JSON Format**: http://localhost:8000/openapi.json

You can also find the static specification in `specs/002-fullstack-web-app/contracts/openapi.yaml`.

## Rate Limiting

*To be implemented in production deployment*

## Versioning

Current API version: **v1** (implicit, no version prefix)

Future versions will use path prefixes: `/api/v2/...`

---

For detailed endpoint specifications, request/response schemas, and examples, please visit the interactive documentation at http://localhost:8000/docs when the backend server is running.
