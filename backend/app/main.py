"""FastAPI main application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import Base, engine
from app.api import sequences, mutations, experiments, literature, reports

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="MLDP Lipid Droplet Localization Research Assistant API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "MLDP Research Assistant"}
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return JSONResponse(
        status_code=200,
        content={
            "title": settings.api_title,
            "version": settings.api_version,
            "documentation": "/docs",
            "redoc": "/redoc"
        }
    )


# Include routers
app.include_router(sequences.router)
app.include_router(mutations.router)
app.include_router(experiments.router)
app.include_router(literature.router)
app.include_router(reports.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.server_reload
    )
