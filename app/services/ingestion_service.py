from app.core.models import DocumentAnalysisRequest, DocumentAnalysisResponse, CvOutput, RagOutput, AnomalyOutput, ForecastOutput, RiskEngineOutput
from app.services.cv_service import CvService
from app.services.rag_service import RagService
from app.services.anomaly_service import AnomalyService
from app.services.forecast_service import ForecastService
from app.services.risk_engine import RiskEngine

class IngestionService:
    """Handles document ingestion, routes to appropriate services, and aggregates results."""

    def __init__(self):
        self.cv_service = CvService()
        self.rag_service = RagService()
        self.anomaly_service = AnomalyService()
        self.forecast_service = ForecastService()
        self.risk_engine = RiskEngine()

    async def process_document(self, request: DocumentAnalysisRequest) -> DocumentAnalysisResponse:
        """Processes the document by calling various services and aggregating their outputs."""
        document_id = request.document.document_id

        # Call individual services
        cv_output = await self.cv_service.analyze_document(request.document.content)
        rag_output = await self.rag_service.process_document(request.document.content)
        anomaly_output = await self.anomaly_service.detect_anomaly(request.document.content)
        forecast_output = await self.forecast_service.get_forecast(request.document.content)
        risk_engine_output = await self.risk_engine.compute_risk_score(request.document.content)

        return DocumentAnalysisResponse(
            document_id=document_id,
            cv_output=cv_output,
            rag_output=rag_output,
            anomaly_output=anomaly_output,
            forecast_output=forecast_output,
            risk_engine_output=risk_engine_output
        )
