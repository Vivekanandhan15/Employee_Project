# Complete Authentication Flow & Postman Testing Guide

## 🔐 How Authentication Works

### 1. **Password Security Flow**
```
User Input: "mypassword123"
          ↓
     hash_password() [bcrypt with salt]
          ↓
Stored in DB: "$2b$12$N9qo8uLOickgx2ZMRZoMyeIjZAgcg7b3XeKeUxWdeS86U7tS8qWFm"
```

**Key Points:**
- Password is hashed using bcrypt with automatic salt generation
- Same password produces different hash each time (due to salt)
- Hash is one-way: cannot be reversed to get original password
- Only the hash is stored in the database, never plain text

### 2. **User Registration & Login Flow**

#### Step 1: Register New User
```
POST /users/register
Body: {
  "first_name": "John",
  "last_name": "Doe", 
  "email": "john@example.com",
  "password": "mypassword123",  ← Plain text
  "phone": "1234567890"
}
     ↓
UserService.create_user()
     ↓
hash_password("mypassword123")  ← Bcrypt hashing
     ↓
Store in Database:
- user_id: "550e8400-e29b-41d4-a716-446655440000"
- email: "john@example.com"
- password: "$2b$12$..." ← Hashed (never original)
```

#### Step 2: Login
```
POST /auth/login
Body: {
  "email": "john@example.com",
  "password": "mypassword123"  ← Plain text user enters
}
     ↓
1. Find user by email in database
2. Get stored hash from database
3. verify_password(plain_password, stored_hash)
   - Hash the plain password again
   - Compare with stored hash
4. If match → Create JWT token
   If no match → Return 401 Unauthorized
     ↓
Response: {
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Step 3: Access Protected Endpoints
```
GET /users (or any protected endpoint)
Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
     ↓
JWTMiddleware checks:
1. Is Authorization header present?
2. Is token format "Bearer <token>"?
3. Verify token signature with SECRET_KEY
4. Check token expiration
5. Extract user info (user_id, email, etc.)
     ↓
If valid → Pass to endpoint
If invalid → Return 401 Unauthorized
```

---

## 📮 Postman Testing Guide

### **Prerequisites**
- Postman installed
- API running: `uvicorn main:app --reload`
- Base URL: `http://localhost:8000`

---

### **Test 1: Register New User** ✅

**Step 1:** Create new request
- Method: **POST**
- URL: `http://localhost:8000/users/register`

**Step 2:** Set Headers
```
Content-Type: application/json
```

**Step 3:** Set Body (raw JSON)
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "secure_password_123",
  "phone": "9876543210"
}
```

**Step 4:** Click Send

**Expected Response (201):**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "is_active": true,
  "phone": "9876543210"
}
```

**Notice:** Password is NOT returned (security best practice!)

---

### **Test 2: Try Wrong Password** ❌

**Step 1:** Create new request
- Method: **POST**
- URL: `http://localhost:8000/auth/login`

**Step 2:** Set Headers
```
Content-Type: application/json
```

**Step 3:** Set Body (Wrong Password)
```json
{
  "email": "john@example.com",
  "password": "wrong_password"
}
```

**Step 4:** Click Send

**Expected Response (401):**
```json
{
  "detail": "Invalid email or password"
}
```

---

### **Test 3: Login Successfully** ✅

**Step 1:** Create new request
- Method: **POST**
- URL: `http://localhost:8000/auth/login`

**Step 2:** Set Headers
```
Content-Type: application/json
```

**Step 3:** Set Body (Correct Password)
```json
{
  "email": "john@example.com",
  "password": "secure_password_123"
}
```

**Step 4:** Click Send

**Expected Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJleHAiOjE3MTUyNDk5MzN9.abc123...",
  "token_type": "bearer"
}
```

**⚠️ Important:** Save the `access_token` value for the next steps!

---

### **Test 4: Access Protected Endpoint (Without Token)** ❌

**Step 1:** Create new request
- Method: **GET**
- URL: `http://localhost:8000/users`

**Step 2:** Set Headers
```
Content-Type: application/json
```
(NO Authorization header)

**Step 3:** Click Send

**Expected Response (401):**
```json
{
  "detail": "Authorization header missing"
}
```

---

### **Test 5: Access Protected Endpoint (With Token)** ✅

**Step 1:** Create new request
- Method: **GET**
- URL: `http://localhost:8000/users`

**Step 2:** Set Headers
```
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJleHAiOjE3MTUyNDk5MzN9.abc123...
```

**⚠️ Replace with your token from Test 3!**

**Step 3:** Click Send

**Expected Response (200):**
```json
[
  {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "is_active": true,
    "phone": "9876543210"
  }
]
```

---

### **Test 6: Expired Token** ❌

**Step 1:** Wait 30+ minutes (or manually edit token)

**Step 2:** Try to access protected endpoint with old token
- Method: **GET**
- URL: `http://localhost:8000/users`
- Header: `Authorization: Bearer <old_token>`

**Expected Response (401):**
```json
{
  "detail": "Invalid or expired token: Token is expired"
}
```

**Solution:** Login again to get a new token

---

### **Test 7: Create User as Authenticated User** ✅

**Step 1:** Create new request
- Method: **POST**
- URL: `http://localhost:8000/users`

**Step 2:** Set Headers
```
Content-Type: application/json
Authorization: Bearer <your_token_from_test_3>
```

**Step 3:** Set Body
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@example.com",
  "password": "another_secure_pwd_456",
  "phone": "5555555555"
}
```

**Step 4:** Click Send

**Expected Response (201):**
```json
{
  "user_id": "660e8400-e29b-41d4-a716-446655440000",
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@example.com",
  "is_active": true,
  "phone": "5555555555"
}
```

---

## 🔑 How to Use Postman Variables to Simplify Testing

Instead of copying tokens manually, use Postman variables:

### **Step 1:** Set Base URL Variable
1. Click **Environment** tab (top left)
2. Click **Create** or **Edit** your environment
3. Add variable:
   - Key: `baseUrl`
   - Value: `http://localhost:8000`

### **Step 2:** Set Token Variable After Login
1. In Login response, select the token value
2. Right-click → **Set as variable** → Create new variable `token`

### **Step 3:** Use Variables in Requests
- URL: `{{baseUrl}}/users`
- Authorization Header: `Bearer {{token}}`

---

## 📊 Testing Checklist

- [ ] **Register**: POST /users/register (no auth)
- [ ] **Login with correct password**: POST /auth/login
- [ ] **Login with wrong password**: GET 401
- [ ] **GET /users without token**: GET 401
- [ ] **GET /users with token**: GET 200 (list users)
- [ ] **POST /users without token**: GET 401
- [ ] **POST /users with token**: POST 201 (create user)
- [ ] **GET /users/{id} with token**: GET 200
- [ ] **PUT /users/{id} with token**: PUT 200
- [ ] **DELETE /users/{id} with token**: DELETE 200
- [ ] **Test expired token**: Login, wait, then 401

---

## 🔍 Database Verification

To verify password is actually hashed in the database:

```bash
# Connect to your database (PostgreSQL example)
psql -U neondb_owner -h ep-cool-queen-ape3s0ny-pooler.c-7.us-east-1.aws.neon.tech -d neondb

# Query users table
SELECT user_id, email, password FROM users LIMIT 5;
```

**You should see:**
```
                 user_id                  |       email        |                           password
------------------------------------------|--------------------|---------------------------------------------------------
550e8400-e29b-41d4-a716-446655440000     | john@example.com   | $2b$12$N9qo8uLOickgx2ZMRZoMyeIjZAgcg7b3XeKeUxWdeS86...
660e8400-e29b-41d4-a716-446655440000     | jane@example.com   | $2b$12$anotherHashedPasswordHere7b3XeKeUxWdeS86U7tS8q...
```

**Notice:** All passwords start with `$2b$12$` (bcrypt format) - they are hashed, not plain text!

---

## 🛡️ Security Verification

### ✅ What's Secure
- Passwords are hashed with bcrypt + salt
- Tokens expire after 30 minutes
- Tokens are signed with SECRET_KEY
- Middleware validates every protected request
- Password never returned in API responses

### ✅ How It Protects You
1. **If database is stolen**: Hashes cannot be reversed to get passwords
2. **If token is intercepted**: It expires in 30 minutes
3. **If someone tries to modify token**: Signature check fails (401)
4. **Brute force attacks**: Bcrypt is intentionally slow
5. **No plaintext passwords**: Ever stored or transmitted

---

## 🐛 Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `Authorization header missing` | No token sent | Add `Authorization: Bearer <token>` header |
| `Invalid or expired token` | Token expired | Login again to get new token |
| `Email already exists` | User already registered | Use different email |
| `Invalid email or password` | Wrong credentials | Check email/password spelling |
| `Token is not valid` | Token tampered | Get fresh token from login |
| `CORS error` | Frontend/Postman on different domain | Add CORS middleware if needed |

