from fastapi import APIRouter
from app.core.models import HealthCheckResponse

router = APIRouter()

@router.get("/livez", response_model=HealthCheckResponse)
async def livez():
    """Health check endpoint for liveness probes."""
    return {"status": "ok", "message": "Service is live"}

@router.get("/readyz", response_model=HealthCheckResponse)
async def readyz():
    """Health check endpoint for readiness probes."""
    # Here you might check database connections, external services, etc.
    return {"status": "ok", "message": "Service is ready"}
