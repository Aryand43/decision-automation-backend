import pytest
from httpx import AsyncClient
from app.main import app
from app.core.models import DocumentAnalysisRequest, RiskScoreRequest

@pytest.mark.asyncio
async def test_health_livez():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health/livez")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Service is live"}

@pytest.mark.asyncio
async def test_health_readyz():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health/readyz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Service is ready"}

@pytest.mark.asyncio
async def test_analyze_document():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        request_data = {
            "document": {
                "document_id": "doc123",
                "content": {
                    "text": "This is a sample document content.",
                    "images": ["base64_image_data"]
                },
                "metadata": {
                    "source": "etl_pipeline"
                }
            }
        }
        response = await ac.post("/document/analyze-document", json=request_data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["document_id"] == "doc123"
    assert "cv_output" in response_json
    assert "rag_output" in response_json
    assert "anomaly_output" in response_json
    assert "forecast_output" in response_json
    assert "risk_engine_output" in response_json
    assert response_json["risk_engine_output"]["score"] >= 0

@pytest.mark.asyncio
async def test_risk_score():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        request_data = {
            "document_id": "doc456",
            "data": {
                "amount": 5000,
                "location": "remote",
                "customer_age_days": 60
            }
        }
        response = await ac.post("/risk/risk-score", json=request_data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["document_id"] == "doc456"
    assert "risk_score" in response_json
    assert response_json["risk_score"]["score"] >= 0



