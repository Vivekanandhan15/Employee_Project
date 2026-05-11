from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError

from core.config import settings

EXCLUDED_PATHS = {
    "/",
    "/auth/login",
    "/users/register",  
    "/docs",
    "/openapi.json",
    "/redoc",
    "/redis-test"
}


class JWTMiddleware(BaseHTTPMiddleware):
    """Middleware to validate JWT tokens for all protected endpoints."""

    async def dispatch(self, request: Request, call_next):
        # Allow excluded paths without authentication
        if request.url.path in EXCLUDED_PATHS:
            response = await call_next(request)
            return response

        # Check for Authorization header
        auth_header = request.headers.get("authorization")
        
        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header missing"}
            )

        # Extract token from "Bearer <token>" format
        try:
            scheme, token = auth_header.split(" ")
            if scheme.lower() != "bearer":
                raise ValueError("Invalid authorization scheme")
        except ValueError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authorization header format"}
            )

        # Verify JWT token
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            # Attach user info to request state for access in endpoints
            request.state.user = payload
        except JWTError as e:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": f"Invalid or expired token: {str(e)}"}
            )

        response = await call_next(request)
        return response
