# User Department Management API

A high-performance FastAPI application for managing users, departments, and their associations with Redis caching and background job processing.

## 🚀 Features

- **User Management**: Complete CRUD operations for users with secure password hashing
- **Department Management**: Full department lifecycle management
- **User-Department Associations**: Flexible many-to-many relationships
- **JWT Authentication**: Secure token-based authentication system
- **Redis Caching**: High-performance caching for frequently accessed data
- **Background Jobs**: Automated cache synchronization using APScheduler
- **Docker Deployment**: Containerized deployment with docker-compose
- **PostgreSQL Database**: Robust relational data storage
- **Comprehensive Error Handling**: Proper HTTP status codes and error responses

## 🛠 Technology Stack

- **Backend**: FastAPI (Python async web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis for high-performance data caching
- **Authentication**: JWT tokens with bcrypt password hashing
- **Background Jobs**: APScheduler for periodic tasks
- **Containerization**: Docker & Docker Compose
- **Documentation**: Auto-generated OpenAPI/Swagger UI

## 📁 Project Structure

```
├── main.py                 # FastAPI application entry point
├── core/                   # Core configurations
├── database/               # Database models and connections
│   ├── database.py        # SQLAlchemy setup
│   └── redis.py           # Redis client configuration
├── models/                # SQLAlchemy models
│   ├── user.py
│   ├── department.py
│   └── association.py
├── routers/               # API route handlers
│   ├── auth_router.py
│   ├── user_router.py
│   ├── department_router.py
│   ├── user_department_router.py
│   ├── address_router.py
│   ├── test_router.py
│   └── cache_router.py
├── schemas/               # Pydantic schemas for validation
├── services/              # Business logic layer
│   ├── user_service.py
│   ├── department_service.py
│   ├── user_department_service.py
│   ├── cache_service.py
│   └── background_sync_service.py
├── seeds/                 # Database seeders
├── utils/                 # Utility functions
├── middleware/            # Custom middleware
├── dependencies/          # Dependency injection
└── requirements.txt       # Python dependencies
```

## 🔧 Installation & Setup

### Prerequisites

- Python 3.12+
- PostgreSQL database
- Redis server
- Docker & Docker Compose (for containerized deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd user-department-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your configuration:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   SECRET_KEY=your-32-character-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Start Redis server**
   ```bash
   # Using Docker
   docker run -d -p 6379:6379 redis:7

   # Or using local Redis installation
   redis-server
   ```

6. **Run database migrations**
   ```bash
   python main.py  # This will create tables automatically
   ```

7. **Start the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

8. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

## 🐳 Docker Deployment

### Quick Start with Docker Compose

1. **Ensure Docker and Docker Compose are installed**

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and other settings
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

   This will start:
   - FastAPI application on port 8000
   - Redis cache on port 6379

4. **Access the application**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

### Docker Commands

```bash
# Build the application
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build --force-recreate
```

### Production Deployment

For production deployment, consider:

1. **Use external PostgreSQL database** (AWS RDS, Google Cloud SQL, etc.)
2. **Configure Redis cluster** for high availability
3. **Set up reverse proxy** (nginx) with SSL
4. **Configure environment variables** securely
5. **Set up monitoring** and logging

## 📊 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Users
- `GET /users` - List all users
- `GET /users/{user_id}` - Get user by ID
- `POST /users` - Create new user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Departments
- `GET /departments` - List all departments
- `GET /departments/{dept_id}` - Get department by ID
- `POST /departments` - Create new department
- `PUT /departments/{dept_id}` - Update department
- `DELETE /departments/{dept_id}` - Delete department

### User-Department Associations
- `POST /user-departments` - Assign users to departments
- `GET /user-departments/user/{user_id}` - Get user's departments
- `GET /user-departments/department/{dept_id}` - Get department's users
- `DELETE /user-departments/{user_id}/{dept_id}` - Remove user from department

### Cache Management (Admin)
- `POST /cache/invalidate-all` - Manually clear all cache

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register**: `POST /auth/register` with user details
2. **Login**: `POST /auth/login` with email/password
3. **Use Token**: Include `Authorization: Bearer <token>` header in requests
4. **Token Expiry**: 30 minutes by default

## ⚡ Redis Caching System

### Cache Strategy

- **Cache-First Reads**: API checks Redis before database queries
- **TTL Expiration**: 5-minute default cache expiration
- **Write-Through Invalidation**: Cache cleared immediately on data changes
- **Background Sync**: Periodic cache refresh every 5 minutes

### Cached Endpoints

- `GET /users` - All users list
- `GET /users/{id}` - Individual user details
- `GET /departments` - All departments list
- `GET /departments/{id}` - Individual department details
- `GET /user-departments/user/{id}` - User's departments
- `GET /user-departments/department/{id}` - Department's users

### Cache Invalidation

- **Automatic**: Triggered on create/update/delete operations
- **Manual**: Admin endpoint to clear all cache
- **Scheduled**: Background jobs refresh cache periodically

## 🔄 Background Jobs

The application uses APScheduler for automated tasks:

- **User Sync**: Refresh all users cache every 5 minutes
- **Department Sync**: Refresh all departments cache every 5 minutes
- **Cache Cleanup**: Remove expired entries every 10 minutes

Jobs run automatically when the application starts and stop gracefully on shutdown.

## 🧪 Testing

### Using Postman

Import the provided Postman collection and environment files:

1. Import `POSTMAN_TESTING_GUIDE.md` collection
2. Set up environment variables in Postman
3. Run authentication flow first, then test other endpoints

### Manual Testing

```bash
# Health check
curl http://localhost:8000/

# Register user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","first_name":"John","last_name":"Doe","phone":"1234567890"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## 📈 Performance Features

- **Async/Await**: Full async support for concurrent requests
- **Connection Pooling**: Efficient database and Redis connections
- **Caching**: Reduced database load for read operations
- **Background Processing**: Non-blocking cache synchronization
- **Optimized Queries**: Efficient SQLAlchemy queries with relationships

## 🔍 Monitoring & Debugging

### Logs

Application logs are available through:
```bash
# Docker logs
docker-compose logs -f api

# Direct application logs
uvicorn main:app --log-level info
```

### Health Checks

- `GET /` - Basic health check endpoint
- Check Redis connectivity in application logs
- Monitor background job execution

### Cache Monitoring

- Cache hit/miss ratios logged on requests
- Background sync operations logged
- Manual cache invalidation available for debugging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the Postman testing guide
- Check application logs for errors
- Ensure all environment variables are properly configured

## 🚀 Deployment Checklist

- [ ] Environment variables configured
- [ ] Database accessible and migrated
- [ ] Redis server running
- [ ] Docker images built (if using containers)
- [ ] SSL certificates configured (production)
- [ ] Monitoring and logging set up
- [ ] Background jobs verified
- [ ] Cache warming completed
- [ ] Load testing performed