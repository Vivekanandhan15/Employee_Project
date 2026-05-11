# 🎯 Postman Step-by-Step Visual Guide

## STEP 1️⃣: Register Your First User

```
┌─────────────────────────────────────────────────────────────┐
│ POSTMAN: Create New Request                                 │
├─────────────────────────────────────────────────────────────┤
│ 1. Click "+" to create new request                          │
│ 2. Method: SELECT "POST"                                    │
│ 3. URL: http://localhost:8000/users/register                │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ HEADERS TAB                                                 │
├─────────────────────────────────────────────────────────────┤
│ Key:          Value:                                        │
│ Content-Type  application/json                              │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ BODY TAB → Raw → JSON                                       │
├─────────────────────────────────────────────────────────────┤
│ {                                                           │
│   "first_name": "John",                                     │
│   "last_name": "Doe",                                       │
│   "email": "john@example.com",                              │
│   "password": "MySecurePassword123",                        │
│   "phone": "9876543210"                                     │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
         ↓
         CLICK "SEND" BUTTON
         ↓
┌─────────────────────────────────────────────────────────────┐
│ RESPONSE (Status: 201 Created) ✓                            │
├─────────────────────────────────────────────────────────────┤
│ {                                                           │
│   "user_id": "550e8400-e29b-41d4-a716-446655440000",       │
│   "first_name": "John",                                     │
│   "last_name": "Doe",                                       │
│   "email": "john@example.com",                              │
│   "is_active": true,                                        │
│   "phone": "9876543210"                                     │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
         ↓
  ✓ USER CREATED SUCCESSFULLY!
```

---

## STEP 2️⃣: Login to Get Token

```
┌─────────────────────────────────────────────────────────────┐
│ POSTMAN: Create New Request                                 │
├─────────────────────────────────────────────────────────────┤
│ 1. Click "+" to create new request                          │
│ 2. Method: SELECT "POST"                                    │
│ 3. URL: http://localhost:8000/auth/login                    │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ HEADERS TAB                                                 │
├─────────────────────────────────────────────────────────────┤
│ Key:          Value:                                        │
│ Content-Type  application/json                              │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ BODY TAB → Raw → JSON                                       │
├─────────────────────────────────────────────────────────────┤
│ {                                                           │
│   "email": "john@example.com",                              │
│   "password": "MySecurePassword123"                         │
│ }                                                           │
│                                                             │
│ ⚠️ USE SAME PASSWORD FROM STEP 1                            │
└─────────────────────────────────────────────────────────────┘
         ↓
         CLICK "SEND" BUTTON
         ↓
┌─────────────────────────────────────────────────────────────┐
│ RESPONSE (Status: 200 OK) ✓                                 │
├─────────────────────────────────────────────────────────────┤
│ {                                                           │
│   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.   │
│                   eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcx  │
│                   Ni00NDY2NTU0NDAwMDAiLCJlbWFpbCI6ImpvaG5A  │
│                   ZXhhbXBsZS5jb20iLCJleHAiOjE3MTUyNDk5MzN9  │
│                   .abc123...",                              │
│   "token_type": "bearer"                                    │
│ }                                                           │
│                                                             │
│ 🔑 COPY THIS TOKEN - YOU'LL NEED IT NEXT!                  │
└─────────────────────────────────────────────────────────────┘
         ↓
  ✓ LOGIN SUCCESSFUL!
  ✓ TOKEN RECEIVED!
```

---

## STEP 3️⃣: Use Token to Access Protected Endpoint

```
┌─────────────────────────────────────────────────────────────┐
│ POSTMAN: Create New Request                                 │
├─────────────────────────────────────────────────────────────┤
│ 1. Click "+" to create new request                          │
│ 2. Method: SELECT "GET"                                     │
│ 3. URL: http://localhost:8000/users                         │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ HEADERS TAB                                                 │
├─────────────────────────────────────────────────────────────┤
│ Key:              Value:                                    │
│ Content-Type      application/json                          │
│ Authorization     Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6Ijow  │
│                   VCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQ  │
│                   tYTcxNi00NDY2NTU0NDAwMDAiLCJlbWFpbCI6ImpvaG  │
│                   FAZXhhbXBsZS5jb20iLCJleHAiOjE3MTUyNDk5MzN  │
│                   9.abc123...                                │
│                                                             │
│ ⚠️ PASTE THE TOKEN FROM STEP 2!                             │
│    Format: "Bearer " + token_value                          │
└─────────────────────────────────────────────────────────────┘
         ↓
         CLICK "SEND" BUTTON
         ↓
┌─────────────────────────────────────────────────────────────┐
│ RESPONSE (Status: 200 OK) ✓                                 │
├─────────────────────────────────────────────────────────────┤
│ [                                                           │
│   {                                                         │
│     "user_id": "550e8400-e29b-41d4-a716-446655440000",     │
│     "first_name": "John",                                   │
│     "last_name": "Doe",                                     │
│     "email": "john@example.com",                            │
│     "is_active": true,                                      │
│     "phone": "9876543210"                                   │
│   }                                                         │
│ ]                                                           │
└─────────────────────────────────────────────────────────────┘
         ↓
  ✓ PROTECTED ENDPOINT ACCESSED!
  ✓ TOKEN VALIDATION SUCCESSFUL!
```

---

## STEP 4️⃣: Test What Happens Without Token

```
┌─────────────────────────────────────────────────────────────┐
│ POSTMAN: Create New Request                                 │
├─────────────────────────────────────────────────────────────┤
│ 1. Click "+" to create new request                          │
│ 2. Method: SELECT "GET"                                     │
│ 3. URL: http://localhost:8000/users                         │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ HEADERS TAB                                                 │
├─────────────────────────────────────────────────────────────┤
│ Key:          Value:                                        │
│ Content-Type  application/json                              │
│                                                             │
│ ❌ DO NOT ADD Authorization HEADER                          │
└─────────────────────────────────────────────────────────────┘
         ↓
         CLICK "SEND" BUTTON
         ↓
┌─────────────────────────────────────────────────────────────┐
│ RESPONSE (Status: 401 Unauthorized) ❌                      │
├─────────────────────────────────────────────────────────────┤
│ {                                                           │
│   "detail": "Authorization header missing"                  │
│ }                                                           │
│                                                             │
│ ✓ THIS IS EXPECTED - SECURITY WORKING!                      │
└─────────────────────────────────────────────────────────────┘
         ↓
  ✓ SECURITY VERIFIED!
  ✓ ENDPOINTS PROTECTED!
```

---

## STEP 5️⃣: Create Another User (Authenticated)

```
┌─────────────────────────────────────────────────────────────┐
│ POSTMAN: Create New Request                                 │
├─────────────────────────────────────────────────────────────┤
│ 1. Click "+" to create new request                          │
│ 2. Method: SELECT "POST"                                    │
│ 3. URL: http://localhost:8000/users                         │
│          (NO /register - requires auth)                     │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ HEADERS TAB                                                 │
├─────────────────────────────────────────────────────────────┤
│ Key:              Value:                                    │
│ Content-Type      application/json                          │
│ Authorization     Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6Ijow  │
│                   VCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQ  │
│                   ... (your token from Step 2)              │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ BODY TAB → Raw → JSON                                       │
├─────────────────────────────────────────────────────────────┤
│ {                                                           │
│   "first_name": "Jane",                                     │
│   "last_name": "Smith",                                     │
│   "email": "jane@example.com",                              │
│   "password": "AnotherPassword456",                         │
│   "phone": "5555555555"                                     │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
         ↓
         CLICK "SEND" BUTTON
         ↓
┌─────────────────────────────────────────────────────────────┐
│ RESPONSE (Status: 201 Created) ✓                            │
├─────────────────────────────────────────────────────────────┤
│ {                                                           │
│   "user_id": "660e8400-e29b-41d4-a716-446655440000",       │
│   "first_name": "Jane",                                     │
│   "last_name": "Smith",                                     │
│   "email": "jane@example.com",                              │
│   "is_active": true,                                        │
│   "phone": "5555555555"                                     │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
         ↓
  ✓ AUTHENTICATED USER CAN CREATE USERS!
```

---

## 🧪 Complete Test Scenarios

### Scenario A: Successful Authentication & Access
```
✓ Step 1: Register user at /users/register (no token needed)
✓ Step 2: Login at /auth/login (get token)
✓ Step 3: GET /users with token (success 200)
✓ Step 4: POST /users with token (create user, success 201)
```

### Scenario B: Security Verification
```
✓ Try GET /users without token → 401 (access denied)
✓ Try GET /users with fake token → 401 (invalid)
✓ Try GET /users with expired token → 401 (expired)
```

### Scenario C: Wrong Credentials
```
✓ Try login with wrong password → 401 (invalid)
✓ Try login with non-existent email → 401 (invalid)
✓ Try register with existing email → 400 (email exists)
```

---

## 🎯 Summary: What's Happening Behind Scenes

| Step | Action | Password | Token | Auth |
|------|--------|----------|-------|------|
| 1 | Register user | Hashed & stored | None | ❌ |
| 2 | Login | Verified against hash | Generated | ❌ |
| 3 | GET users | N/A | Validated | ✅ |
| 4 | Create user | Hashed & stored | Validated | ✅ |
| 5 | No token | N/A | Missing | ❌ DENIED |

---

## 📝 Quick Copy-Paste Templates

### Template 1: Register
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "phone": "1234567890"
}
```

### Template 2: Login
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

### Template 3: Create User (Authenticated)
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@example.com",
  "password": "AnotherPass456",
  "phone": "9876543210"
}
```

---

## 🚦 Status Code Reference

```
201 Created      → User successfully created ✓
200 OK           → Request successful ✓
400 Bad Request  → Invalid data (email exists, etc) ✗
401 Unauthorized → Missing/invalid/expired token ✗
404 Not Found    → User not found ✗
500 Server Error → Internal error ✗
```

