from typing import Dict, Any
from app.core.models import AnomalyOutput

class AnomalyService:

    async def detect_anomaly(self, data: Dict[str, Any]) -> AnomalyOutput:
        return AnomalyOutput(
            is_anomaly=False,
            anomaly_score=0.1,
            reason="No anomaly detected (stub)"
        )

