"""
FastAPI application — demo app for CI/CD pipeline project.
"""
import os
import time
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .api import router
from .models import HealthResponse, StatusResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP_VERSION = os.getenv("VERSION", "0.0.0")
START_TIME = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting myapp v{APP_VERSION}")
    yield
    logger.info("Shutting down myapp")


app = FastAPI(
    title="MyApp API",
    version=APP_VERSION,
    description="Demo application for DevOps CI/CD pipeline",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Kubernetes liveness probe endpoint."""
    return HealthResponse(status="healthy", version=APP_VERSION)


@app.get("/ready", tags=["Health"])
async def readiness_check():
    """Kubernetes readiness probe endpoint."""
    # Check DB and Redis connectivity here in real app
    return JSONResponse({"status": "ready"})


@app.get("/api/v1/status", response_model=StatusResponse, tags=["Status"])
async def status():
    uptime = round(time.time() - START_TIME, 2)
    return StatusResponse(
        status="running",
        version=APP_VERSION,
        uptime_seconds=uptime,
        environment=os.getenv("ENVIRONMENT", "unknown"),
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)
