from typing import Dict, Any
from app.core.models import AnomalyOutput

class AnomalyService:
    """Placeholder for anomaly detection logic."""

    async def detect_anomaly(self, data: Dict[str, Any]) -> AnomalyOutput:
        """Stubs anomaly detection, always returning no anomaly for now."""
        # Minimal implementation / stub
        return AnomalyOutput(
            is_anomaly=False,
            anomaly_score=0.1,
            reason="No anomaly detected (stub)"
        )
