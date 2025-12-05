from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import date

class CashflowMetrics(BaseModel):
    total_inflow: float
    total_outflow: float
    net_cashflow: float
    average_monthly_cashflow: float
    cashflow_volatility: float

class LiquidityMetrics(BaseModel):
    current_ratio: float
    quick_ratio: float
    cash_conversion_cycle: Optional[float] = None
    days_cash_on_hand: float

class FinancialDisciplineMetrics(BaseModel):
    overdraft_frequency: int
    late_payment_count: int
    bounced_cheque_count: int
    savings_rate: float

class DebtServicingMetrics(BaseModel):
    dscr: float
    debt_to_income_ratio: float
    loan_payment_to_income_ratio: float

class RiskIndicators(BaseModel):
    high_risk_transactions: List[Dict[str, Any]]
    credit_score_change: float
    negative_news_mentions: int
    bankruptcy_flags: bool

class LlmSummaryOutput(BaseModel):
    summary_text: str
    key_insights: List[str]
    red_flags_identified: List[str]

class ForecastOutputs(BaseModel):
    short_term_cashflow_forecast: Dict[date, float]
    long_term_revenue_projection: Dict[date, float]
    liquidity_stress_test_results: Dict[str, Any]

class UnifiedDocumentResponse(BaseModel):
    document_type: str
    extracted_data: Dict[str, Any]
    cashflow_metrics: Optional[CashflowMetrics] = None
    liquidity_metrics: Optional[LiquidityMetrics] = None
    financial_discipline_metrics: Optional[FinancialDisciplineMetrics] = None
    debt_servicing_metrics: Optional[DebtServicingMetrics] = None
    risk_indicators: Optional[RiskIndicators] = None
    llm_summary: Optional[LlmSummaryOutput] = None
    forecasts: Optional[ForecastOutputs] = None
    risk_score: Optional[float] = None
    risk_factors: Optional[List[str]] = None

class RiskEngineOutput(BaseModel):
    score: float = Field(..., ge=0, le=100)
    bin: str
    decision: str
    rationale: List[str]

class RiskScoreRequest(BaseModel):
    cashflow_metrics: CashflowMetrics
    liquidity_metrics: LiquidityMetrics
    financial_discipline_metrics: FinancialDisciplineMetrics
    debt_servicing_metrics: DebtServicingMetrics
    risk_indicators: RiskIndicators

class RiskScoreResponse(BaseModel):
    document_id: Optional[str] = None
    risk_engine_output: RiskEngineOutput
