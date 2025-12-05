from fastapi import APIRouter, Depends, HTTPException
from app.services.risk_engine import RiskEngine
from app.core.models import RiskScoreRequest, RiskScoreResponse

router = APIRouter()

@router.post("/risk-score", response_model=RiskScoreResponse)
async def get_risk_score(request: RiskScoreRequest, risk_engine: RiskEngine = Depends()):
    """Calculates a risk score based on the provided document data."""
    try:
        response = await risk_engine.compute_risk_score(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
