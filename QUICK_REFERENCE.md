# Quick Reference: Authentication Flow Diagram

## 🔐 Password Hashing Flow
```
┌─────────────────────────────────────────────────────────────┐
│ USER REGISTERS / CREATES ACCOUNT                            │
└─────────────────────────────────────────────────────────────┘
                         ↓
              Plain Text Password
                  "mypassword"
                         ↓
              hash_password() [bcrypt]
                         ↓
         Hashed: $2b$12$N9qo8uLO...
                         ↓
          Stored in Database
          (Original password LOST)
```

## 🔑 Login & Token Generation Flow
```
┌──────────────────────────────────────────────┐
│ USER ENTERS EMAIL & PASSWORD                 │
└──────────────────────────────────────────────┘
         ↓
    POST /auth/login
    {email, password}
         ↓
┌──────────────────────────────────────────────┐
│ SERVER VERIFICATION                          │
├──────────────────────────────────────────────┤
│ 1. Find user by email in DB                  │
│ 2. Get stored hash from DB                   │
│ 3. Hash user's plain password                │
│ 4. Compare hashes                            │
└──────────────────────────────────────────────┘
         ↓
    Match? ──YES→ Create JWT Token ──→ Send to User
              ─NO→ Return 401 Error
```

## 🛡️ Protected Endpoint Access Flow
```
┌──────────────────────────────────────────────┐
│ USER REQUESTS PROTECTED ENDPOINT             │
│ GET /users                                   │
│ Header: Authorization: Bearer <token>        │
└──────────────────────────────────────────────┘
         ↓
┌──────────────────────────────────────────────┐
│ MIDDLEWARE VALIDATION                        │
├──────────────────────────────────────────────┤
│ ✓ Header exists?                             │
│ ✓ Format is "Bearer <token>"?                │
│ ✓ Token signature valid?                     │
│ ✓ Token not expired?                         │
└──────────────────────────────────────────────┘
         ↓
    All valid? ──YES→ Pass to endpoint ──→ Return data
               ──NO→ Return 401 Error
```

## 📋 Complete User Journey
```
START
  │
  ├─→ [1] POST /users/register (NO TOKEN NEEDED)
  │   Input: email, password, name, phone
  │   Process: Hash password → Store user
  │   Response: User created ✓
  │
  ├─→ [2] POST /auth/login
  │   Input: email, password
  │   Process: Verify password → Generate JWT
  │   Response: access_token ✓
  │
  ├─→ [3] GET /users (REQUIRES TOKEN)
  │   Header: Authorization: Bearer <token>
  │   Process: Validate token → Fetch data
  │   Response: List of users ✓
  │
  ├─→ [4] POST /users (REQUIRES TOKEN)
  │   Header: Authorization: Bearer <token>
  │   Input: email, password, name, phone
  │   Process: Hash password → Store user
  │   Response: User created ✓
  │
  └─→ [5] Any protected endpoint (REQUIRES TOKEN)
      All endpoints need: Authorization: Bearer <token>
```

## 📊 Token Expiration Timeline
```
Time: 0 min         ← Token Generated (POST /auth/login)
      │
      ├─→ 15 min    ✓ Token still valid
      │
      ├─→ 29 min    ✓ Token still valid
      │
      ├─→ 30 min    ✗ Token EXPIRED (401 error)
      │
      └─→ Login again to get new token
```

## 🚀 Postman Request Templates

### REGISTER USER
```
POST http://localhost:8000/users/register
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "password123",
  "phone": "1234567890"
}
```

### LOGIN
```
POST http://localhost:8000/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}

Response → Copy access_token
```

### USE TOKEN (Example: Get Users)
```
GET http://localhost:8000/users
Content-Type: application/json
Authorization: Bearer {{TOKEN_FROM_LOGIN}}
```

### CREATE ANOTHER USER (Authenticated)
```
POST http://localhost:8000/users
Content-Type: application/json
Authorization: Bearer {{TOKEN_FROM_LOGIN}}

{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@example.com",
  "password": "password456",
  "phone": "9876543210"
}
```

## ✅ Status Codes Guide

| Code | Meaning | When |
|------|---------|------|
| 201 | Created ✓ | User registered/created successfully |
| 200 | OK ✓ | Request successful, data returned |
| 400 | Bad Request ✗ | Invalid input (e.g., email exists) |
| 401 | Unauthorized ✗ | Token missing/invalid/expired |
| 404 | Not Found ✗ | User/resource not found |
| 500 | Server Error ✗ | Internal error |

## 🔐 Security Facts

- **Bcrypt Hash**: One-way encryption, cannot be reversed
- **Token Expiry**: 30 minutes (configurable in .env)
- **Password Storage**: Never stored as plain text
- **Password Transmission**: Only over HTTPS in production
- **Token Signature**: Verified with SECRET_KEY on every request
- **Salt**: Automatic with bcrypt, prevents rainbow tables

