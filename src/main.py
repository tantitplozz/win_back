"""
Main API module for the Advanced AI Backend.
"""
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from typing import Dict, Any, List, Optional

from src.config.settings import settings
from src.api.routes import router as api_router
from src.utils.logger import setup_logger

# Setup logger
logger = setup_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Advanced AI Backend with unrestricted capabilities",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Simple rate limiting based on client IP
    client_ip = request.client.host
    current_time = time.time()
    
    # Check if client has exceeded rate limit
    # In a real implementation, use Redis or another distributed cache
    # This is a simplified example
    if hasattr(app.state, "rate_limit"):
        if client_ip in app.state.rate_limit:
            requests = [t for t in app.state.rate_limit[client_ip] if current_time - t < 60]
            if len(requests) >= settings.RATE_LIMIT_REQUESTS:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Rate limit exceeded"}
                )
            app.state.rate_limit[client_ip] = requests + [current_time]
        else:
            app.state.rate_limit[client_ip] = [current_time]
    else:
        app.state.rate_limit = {client_ip: [current_time]}
    
    response = await call_next(request)
    return response

# Include API routes
app.include_router(api_router, prefix=settings.API_PREFIX)

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Unrestricted mode: {settings.ENABLE_UNRESTRICTED_MODE}")
    
    # Initialize services
    # This would typically include database connections, AI model loading, etc.
    logger.info("Initializing services...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}")
    
    # Cleanup resources
    # This would typically include closing database connections, etc.
    logger.info("Cleaning up resources...")

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": "1.0.0",
        "timestamp": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
