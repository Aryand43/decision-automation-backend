from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.ingestion_service import IngestionService
from app.core.models import DocumentAnalysisRequest, DocumentAnalysisResponse, RiskScoreRequest, RiskScoreResponse

router = APIRouter()

@router.post("/analyze-document", response_model=DocumentAnalysisResponse)
async def analyze_document(request: DocumentAnalysisRequest, ingestion_service: IngestionService = Depends()):
    """Accepts parsed document input and routes it for analysis."""
    try:
        response = await ingestion_service.process_document(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
