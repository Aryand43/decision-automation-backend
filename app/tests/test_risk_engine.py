import pytest
from app.services.risk_engine import RiskEngine
from app.core.models import RiskEngineOutput

@pytest.fixture
def risk_engine_instance():
    return RiskEngine()

@pytest.mark.asyncio
async def test_risk_engine_low_risk(risk_engine_instance):
    data = {"amount": 500, "location": "local", "customer_age_days": 100}
    result = await risk_engine_instance.compute_risk_score(data)

    assert isinstance(result, RiskEngineOutput)
    assert result.score < 30
    assert result.bin == "low"
    assert result.decision == "Approved"
    assert "No specific rules triggered" in result.rationale or not result.rationale

@pytest.mark.asyncio
async def test_risk_engine_medium_risk(risk_engine_instance):
    data = {"amount": 5000, "location": "remote", "customer_age_days": 50}
    result = await risk_engine_instance.compute_risk_score(data)

    assert isinstance(result, RiskEngineOutput)
    assert 30 <= result.score < 70
    assert result.bin == "medium"
    assert result.decision == "Review Required"
    assert len(result.rationale) > 0

@pytest.mark.asyncio
async def test_risk_engine_high_risk(risk_engine_instance):
    data = {"amount": 15000, "location": "remote", "customer_age_days": 10}
    result = await risk_engine_instance.compute_risk_score(data)

    assert isinstance(result, RiskEngineOutput)
    assert result.score >= 70
    assert result.bin == "high"
    assert result.decision == "Rejected"
    assert len(result.rationale) > 0

@pytest.mark.asyncio
async def test_risk_engine_score_bounds(risk_engine_instance):
    # Test score does not exceed 100
    data = {"amount": 1000000, "location": "remote", "customer_age_days": 1}
    result = await risk_engine_instance.compute_risk_score(data)
    assert result.score <= 100

    # Test score does not go below 0 (though our rules only add positive scores)
    data = {"amount": -100, "location": "local", "customer_age_days": 1000}
    result = await risk_engine_instance.compute_risk_score(data)
    assert result.score >= 0
