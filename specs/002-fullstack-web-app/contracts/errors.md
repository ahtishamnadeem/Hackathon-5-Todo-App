# Error Response Specifications

**Feature**: Todo Full-Stack Web Application (Phase II)
**Date**: 2026-01-08
**Requirement**: FR-028 (HTTP status codes), FR-029 (standardized error format), FR-031 (meaningful error messages)

## Overview

All API errors follow a standardized JSON format with consistent HTTP status codes. This enables frontend error handling without case-by-case parsing and provides clear debugging information.

## Standard Error Response Format

### Schema

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}  // Optional field-specific details
  }
}
```

### Fields

| Field          | Type    | Description                                                      |
|----------------|---------|------------------------------------------------------------------|
| success        | boolean | Always `false` for error responses                               |
| data           | null    | Always `null` for error responses (consistency)                  |
| error          | object  | Error details object                                             |
| error.code     | string  | Machine-readable error code (uppercase snake_case)               |
| error.message  | string  | Human-readable error message for display                         |
| error.details  | object  | Optional additional context (field names, validation details)    |

---

## HTTP Status Code Mapping (FR-028)

| Status Code | Meaning                     | When to Use                                               |
|-------------|-----------------------------|-----------------------------------------------------------|
| 200 OK      | Success                     | Successful GET, PATCH, DELETE operations                  |
| 201 Created | Resource created            | Successful POST (new user, new todo)                      |
| 400 Bad Request | Client error             | Validation errors, malformed requests, business rule violations |
| 401 Unauthorized | Authentication required | Missing, invalid, or expired JWT token                     |
| 404 Not Found | Resource not found        | Todo doesn't exist OR user doesn't own resource (security)|
| 500 Internal Server Error | Server error   | Unexpected errors, database failures, uncaught exceptions |

**Security Note**: Return 404 (not 403) when user attempts to access another user's resource. This prevents resource enumeration attacks.

---

## Error Categories

### 1. Authentication Errors (401 Unauthorized)

#### Missing Token
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "MISSING_TOKEN",
    "message": "Authorization header required",
    "details": {}
  }
}
```

**Trigger**: Request to protected endpoint without Authorization header
**HTTP Status**: 401 Unauthorized

#### Invalid Token
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_TOKEN",
    "message": "Token signature verification failed",
    "details": {}
  }
}
```

**Trigger**: JWT signature doesn't match or token is malformed
**HTTP Status**: 401 Unauthorized

#### Expired Token
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "Token has expired, please login again",
    "details": {
      "expired_at": "2026-01-01T10:00:00Z"
    }
  }
}
```

**Trigger**: JWT exp claim is in the past
**HTTP Status**: 401 Unauthorized

#### Invalid Credentials
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password",
    "details": {}
  }
}
```

**Trigger**: Login attempt with wrong email or password
**HTTP Status**: 400 Bad Request (not 401, as this is request validation)

---

### 2. Validation Errors (400 Bad Request)

#### Empty Title
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title cannot be empty",
    "details": {
      "field": "title",
      "constraint": "min_length",
      "min_length": 1
    }
  }
}
```

**Trigger**: Todo creation/update with empty or whitespace-only title (FR-013)
**HTTP Status**: 400 Bad Request

#### Title Too Long
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title exceeds maximum length of 500 characters",
    "details": {
      "field": "title",
      "constraint": "max_length",
      "max_length": 500,
      "provided_length": 650
    }
  }
}
```

**Trigger**: Title exceeds 500 characters
**HTTP Status**: 400 Bad Request

#### Description Too Long
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Description exceeds maximum length of 10000 characters",
    "details": {
      "field": "description",
      "constraint": "max_length",
      "max_length": 10000,
      "provided_length": 15000
    }
  }
}
```

**Trigger**: Description exceeds 10,000 characters
**HTTP Status**: 400 Bad Request

#### Invalid Email Format
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "constraint": "email_format",
      "provided": "not-an-email"
    }
  }
}
```

**Trigger**: Registration with malformed email (FR-002)
**HTTP Status**: 400 Bad Request

#### Weak Password
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Password must be at least 8 characters with one letter and one number",
    "details": {
      "field": "password",
      "constraint": "password_complexity",
      "min_length": 8,
      "requirements": ["letter", "number"]
    }
  }
}
```

**Trigger**: Registration with password <8 chars or missing letter/number (FR-003)
**HTTP Status**: 400 Bad Request

#### Duplicate Email
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "DUPLICATE_EMAIL",
    "message": "An account with this email already exists",
    "details": {
      "field": "email"
    }
  }
}
```

**Trigger**: Registration attempt with email that's already registered
**HTTP Status**: 400 Bad Request

#### Missing Required Field
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required",
    "details": {
      "field": "title",
      "constraint": "required"
    }
  }
}
```

**Trigger**: Todo creation without title field
**HTTP Status**: 400 Bad Request

#### Invalid JSON
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_JSON",
    "message": "Request body is not valid JSON",
    "details": {
      "parse_error": "Expecting property name enclosed in double quotes"
    }
  }
}
```

**Trigger**: Malformed JSON in request body
**HTTP Status**: 400 Bad Request

---

### 3. Resource Errors (404 Not Found)

#### Todo Not Found
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "NOT_FOUND",
    "message": "Todo not found",
    "details": {
      "resource": "todo",
      "id": 123
    }
  }
}
```

**Trigger**:
- Todo ID doesn't exist in database
- OR todo exists but belongs to different user (security - don't reveal existence)

**HTTP Status**: 404 Not Found

**Security Note**: Return same 404 response whether todo doesn't exist or user doesn't own it. Never return 403 Forbidden as it reveals the resource exists.

#### User Not Found
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found",
    "details": {
      "resource": "user"
    }
  }
}
```

**Trigger**: JWT contains user_id that doesn't exist in database (edge case: user deleted)
**HTTP Status**: 404 Not Found

---

### 4. Server Errors (500 Internal Server Error)

#### Database Connection Failure
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "DATABASE_ERROR",
    "message": "Unable to connect to database, please try again later",
    "details": {}
  }
}
```

**Trigger**: Neon database is temporarily unavailable (SC-009)
**HTTP Status**: 500 Internal Server Error

**Frontend Handling**: Display error message and provide retry button

#### Unexpected Server Error
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred, please try again",
    "details": {}
  }
}
```

**Trigger**: Uncaught exception in backend code
**HTTP Status**: 500 Internal Server Error

**Backend Behavior**: Log full stack trace for debugging, but don't expose internal details to client

---

## Error Code Reference

| Error Code            | HTTP Status | Category       | Description                                           |
|-----------------------|-------------|----------------|-------------------------------------------------------|
| MISSING_TOKEN         | 401         | Authentication | Authorization header not provided                     |
| INVALID_TOKEN         | 401         | Authentication | JWT signature invalid or token malformed              |
| TOKEN_EXPIRED         | 401         | Authentication | JWT exp claim is in the past                          |
| INVALID_CREDENTIALS   | 400         | Authentication | Wrong email or password during login                  |
| VALIDATION_ERROR      | 400         | Validation     | Field validation failed (empty, too long, wrong format)|
| DUPLICATE_EMAIL       | 400         | Validation     | Email already registered                              |
| INVALID_JSON          | 400         | Validation     | Request body is not valid JSON                        |
| NOT_FOUND             | 404         | Resource       | Resource doesn't exist or user doesn't own it         |
| DATABASE_ERROR        | 500         | Server         | Database connection or query failure                  |
| INTERNAL_ERROR        | 500         | Server         | Unexpected server error                               |

---

## Frontend Error Handling Examples

### Displaying Validation Errors

```typescript
// Example: Display inline form validation error
async function createTodo(title: string, description: string) {
  try {
    const response = await fetch('/api/todos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description }),
      credentials: 'include'  // Include JWT cookie
    });

    const data = await response.json();

    if (!data.success) {
      // Display error message to user
      if (data.error.code === 'VALIDATION_ERROR') {
        // Show inline error on form field
        setFieldError(data.error.details.field, data.error.message);
      } else {
        // Show toast notification
        showToast(data.error.message, 'error');
      }
      return null;
    }

    return data.data;
  } catch (err) {
    // Network error or JSON parse failure
    showToast('Network error, please check your connection', 'error');
    return null;
  }
}
```

### Handling Authentication Errors

```typescript
// Example: Redirect to login on auth failure
async function makeAuthenticatedRequest(url: string, options: RequestInit) {
  const response = await fetch(url, {
    ...options,
    credentials: 'include'  // Include JWT cookie
  });

  const data = await response.json();

  if (response.status === 401) {
    // Token missing, invalid, or expired - redirect to login
    if (data.error.code === 'TOKEN_EXPIRED') {
      showToast('Session expired, please login again', 'info');
    }
    router.push('/login');
    return null;
  }

  if (!data.success) {
    showToast(data.error.message, 'error');
    return null;
  }

  return data.data;
}
```

### Handling Server Errors

```typescript
// Example: Retry on database failure
async function getTodos() {
  try {
    const response = await fetch('/api/todos', {
      credentials: 'include'
    });

    const data = await response.json();

    if (response.status === 500) {
      // Server error - show retry button
      if (data.error.code === 'DATABASE_ERROR') {
        showToast(
          'Database temporarily unavailable. Please retry.',
          'error',
          { action: 'Retry', onClick: getTodos }
        );
      } else {
        showToast('Unexpected error occurred', 'error');
      }
      return null;
    }

    return data.data;
  } catch (err) {
    showToast('Network error', 'error');
    return null;
  }
}
```

---

## Backend Error Handling Implementation

### Exception Handler (FastAPI)

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Format HTTPException as standardized error response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": exc.detail.get("code", "ERROR"),
                "message": exc.detail.get("message", str(exc.detail)),
                "details": exc.detail.get("details", {})
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    # Log full stack trace for debugging
    logger.error(f"Unexpected error: {exc}", exc_info=True)

    # Return generic error (don't expose internals)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred, please try again",
                "details": {}
            }
        }
    )
```

### Raising Custom Errors

```python
from fastapi import HTTPException

# Validation error
raise HTTPException(
    status_code=400,
    detail={
        "code": "VALIDATION_ERROR",
        "message": "Title cannot be empty",
        "details": {"field": "title", "constraint": "min_length"}
    }
)

# Authentication error
raise HTTPException(
    status_code=401,
    detail={
        "code": "INVALID_TOKEN",
        "message": "Token signature verification failed",
        "details": {}
    }
)

# Not found (security-conscious)
raise HTTPException(
    status_code=404,
    detail={
        "code": "NOT_FOUND",
        "message": "Todo not found",
        "details": {"resource": "todo", "id": todo_id}
    }
)
```

---

## Testing Error Responses

### Test Validation Error
```bash
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <valid-token>" \
  -d '{"title":""}' \
  -w "\nHTTP Status: %{http_code}\n"
```

Expected: 400 Bad Request with VALIDATION_ERROR

### Test Authentication Error
```bash
curl -X GET http://localhost:8000/api/todos \
  -w "\nHTTP Status: %{http_code}\n"
```

Expected: 401 Unauthorized with MISSING_TOKEN

### Test Not Found
```bash
curl -X GET http://localhost:8000/api/todos/99999 \
  -H "Authorization: Bearer <valid-token>" \
  -w "\nHTTP Status: %{http_code}\n"
```

Expected: 404 Not Found with NOT_FOUND

---

## Summary

**Standardized Format**: All errors use consistent JSON structure (FR-029)
**HTTP Status Codes**: Proper mapping for each error type (FR-028)
**Meaningful Messages**: Human-readable messages for end users (FR-031)
**Error Codes**: Machine-readable codes for programmatic handling
**Security**: Return 404 (not 403) for unauthorized resource access
**Details**: Optional field-specific information for debugging

**Error Types**:
- **401 Unauthorized**: Authentication failures (4 error codes)
- **400 Bad Request**: Validation and business logic errors (7 error codes)
- **404 Not Found**: Resource not found or unauthorized access (1 error code)
- **500 Internal Server Error**: Database failures and unexpected errors (2 error codes)

**Total Error Codes Defined**: 14
