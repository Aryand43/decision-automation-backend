import yaml
from typing import Dict, Any, List
from app.core.models import RiskEngineOutput
from pathlib import Path

class RiskEngine:
    """
    Symbolic + ML hybrid Risk Engine responsible for scoring, binning, and decision logic.
    Loads symbolic rules from a YAML file and applies them to compute a risk score.
    """
    def __init__(self):
        self.rules = self._load_rules()

    def _load_rules(self) -> List[Dict[str, Any]]:
        """Loads symbolic rules from the rules.yaml file."""
        rules_path = Path(__file__).parent.parent / "rules" / "rules.yaml"
        with open(rules_path, "r") as f:
            config = yaml.safe_load(f)
        return config.get("rules", [])

    async def compute_risk_score(self, data: Dict[str, Any]) -> RiskEngineOutput:
        """Computes a risk score (0-100), assigns a bin, and provides a decision and rationale."""
        score = 0
        rationale = []

        # Apply symbolic rules
        for rule in self.rules:
            condition_str = rule.get("condition")
            try:
                # Evaluate the condition dynamically. This is a simplified example;
                # in a real system, you'd use a more robust rule engine.
                if eval(condition_str, {"data": data, **data}):  # Provide 'data' and its contents to eval scope
                    score += rule.get("score_impact", 0)
                    rationale.append(rule.get("rationale", ""))
            except Exception as e:
                # Log error if rule evaluation fails
                print(f"Error evaluating rule '{rule.get("name")}'": {e})
                continue

        # Ensure score is within 0-100 range
        score = max(0, min(100, score))

        # Assign bins
        if score < 30:
            bin_category = "low"
            decision = "Approved"
        elif 30 <= score < 70:
            bin_category = "medium"
            decision = "Review Required"
        else:
            bin_category = "high"
            decision = "Rejected"

        if not rationale:
            rationale.append("No specific rules triggered. Base assessment.")

        return RiskEngineOutput(
            score=float(score),
            bin=bin_category,
            decision=decision,
            rationale=rationale
        )
