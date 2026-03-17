"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.json import router as json_router

app = FastAPI(
    title="JSON Parser API",
    description="Backend service for JSON formatting, minifying, validation, and analysis",
    version="1.0.0",
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server default port
        "http://127.0.0.1:5173",
        "http://localhost:3000",  # Common alternative
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(json_router)


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "JSON Parser API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
