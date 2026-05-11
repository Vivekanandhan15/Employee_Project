# Authentication Implementation Guide

## Overview
This API implements a complete JWT-based authentication system with middleware-based authorization for all endpoints.

## Features Implemented

### 1. **Secure Login & Token Generation**
- User login endpoint: `POST /auth/login`
- Generates JWT access tokens with configurable expiration
- Passwords are hashed using bcrypt
- Tokens include user ID and email claims

### 2. **JWT Middleware (Global Authentication)**
- Automatically validates JWT tokens for all protected endpoints
- Located in `middleware/auth_middleware.py`
- Excluded paths (no auth required):
  - `/auth/login` - Login endpoint
  - `/docs` - Swagger documentation
  - `/openapi.json` - OpenAPI schema
  - `/redoc` - ReDoc documentation

### 3. **Endpoint-Level Authentication**
- All routers include `get_current_user` dependency
- Extracts user info from valid JWT tokens
- Returns user context to endpoints (user_id, email, etc.)

### 4. **Secure Configuration**
- Environment variables for sensitive data:
  - `SECRET_KEY`: Secret signing key (use `openssl rand -hex 32` to generate)
  - `ALGORITHM`: JWT algorithm (default: HS256)
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30 minutes)

## Configuration

### Environment Variables (.env)
```
DATABASE_URL=your_database_connection_string
SECRET_KEY=your_random_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Generate Secure SECRET_KEY
```bash
openssl rand -hex 32
```

## API Endpoints

### Authentication
- **POST** `/auth/login`
  - Request: `{"email": "user@example.com", "password": "password"}`
  - Response: `{"access_token": "jwt_token", "token_type": "bearer"}`

### Protected Endpoints (Require JWT Token)
All endpoints below require `Authorization: Bearer <token>` header:

**Users**
- POST `/users` - Create user
- GET `/users` - List all users
- GET `/users/{user_id}` - Get specific user
- PUT `/users/{user_id}` - Update user
- DELETE `/users/{user_id}` - Delete user

**Departments**
- POST `/departments` - Create department
- GET `/departments` - List all departments
- GET `/departments/{dept_id}` - Get specific department
- PUT `/departments/{dept_id}` - Update department
- DELETE `/departments/{dept_id}` - Delete department

**Addresses**
- POST `/addresses/users/{user_id}` - Create address
- GET `/addresses/users/{user_id}` - Get user addresses
- PUT `/addresses/{address_id}` - Update address
- DELETE `/addresses/{address_id}` - Delete address

**User Departments**
- POST `/user-departments` - Assign user to department
- GET `/user-departments/user/{user_id}` - Get user departments
- GET `/user-departments/department/{dept_id}` - Get department users
- DELETE `/user-departments/{user_id}/{dept_id}` - Remove user from department

## Usage Example

### Step 1: Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Step 2: Access Protected Endpoint
```bash
curl -X GET "http://localhost:8000/users" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## File Structure

```
core/
  config.py                 # Settings with JWT configuration
utils/
  jwt_handler.py           # JWT token creation
  security.py              # Password hashing & verification
dependencies/
  auth_dependency.py       # JWT verification dependency
middleware/
  auth_middleware.py       # Global JWT middleware
routers/
  auth_router.py          # Login endpoint
  user_router.py          # Protected user endpoints
  department_router.py    # Protected department endpoints
  address_router.py       # Protected address endpoints
  user_department_router.py # Protected assignment endpoints
```

## Security Best Practices

1. **Secret Key Management**
   - Never commit `.env` with real SECRET_KEY to version control
   - Use strong random keys (minimum 32 bytes)
   - Rotate keys periodically

2. **Token Expiration**
   - Set appropriate expiration time (default: 30 minutes)
   - Implement refresh token mechanism for extended sessions

3. **Password Security**
   - Passwords are hashed with bcrypt (salted)
   - Never store plain text passwords

4. **HTTPS**
   - Always use HTTPS in production
   - Tokens should only be transmitted over secure channels

5. **Token Storage**
   - Store tokens in secure, httpOnly cookies or secure storage
   - Avoid localStorage for sensitive tokens

## Troubleshooting

### Invalid Secret Key Error
```
Error: Invalid or expired token
```
Ensure `SECRET_KEY` in `.env` matches the key used to create the token.

### Token Expired
```
Error: Invalid or expired token: Token is expired
```
Tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES`. User needs to login again.

### Missing Authorization Header
```
Error: Authorization header missing
```
Include `Authorization: Bearer <token>` in request headers.

## Bug Fixes Applied

1. Fixed typo: `SCRET_KEY` → `SECRET_KEY`
2. Fixed typo: `hase_password()` → `hash_password()`
3. Fixed bug: `verify_password()` now correctly verifies passwords
4. Fixed typo: Config class formatting and naming conventions
