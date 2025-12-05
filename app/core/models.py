from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# Health Check Models
class HealthCheckResponse(BaseModel):
    status: str
    message: str

# Document Analysis Models
class DocumentInput(BaseModel):
    document_id: str
    content: Dict[str, Any]  # Parsed content from ETL
    metadata: Dict[str, Any] = {}

class DocumentAnalysisRequest(BaseModel):
    document: DocumentInput

class CvOutput(BaseModel):
    text_detections: List[Dict[str, Any]] = []
    object_detections: List[Dict[str, Any]] = []

class RagOutput(BaseModel):
    summary: str
    relevant_chunks: List[str]

class AnomalyOutput(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    reason: Optional[str] = None

class ForecastOutput(BaseModel):
    predicted_value: float
    confidence_interval: List[float]

class RiskEngineOutput(BaseModel):
    score: float = Field(..., ge=0, le=100)
    bin: str
    decision: str
    rationale: List[str]

class DocumentAnalysisResponse(BaseModel):
    document_id: str
    cv_output: CvOutput
    rag_output: RagOutput
    anomaly_output: AnomalyOutput
    forecast_output: ForecastOutput
    risk_engine_output: RiskEngineOutput

# Risk Scoring Models
class RiskScoreRequest(BaseModel):
    document_id: str
    data: Dict[str, Any]  # Data required for risk calculation

class RiskScoreResponse(BaseModel):
    document_id: str
    risk_score: RiskEngineOutput
