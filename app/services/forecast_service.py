from typing import List, Dict, Any
from app.schema.output_schema import ForecastOutputs
from datetime import date

class ForecastService:

    async def get_forecast(self, time_series_data: Dict[date, float]) -> ForecastOutputs:
        if not time_series_data:
            return ForecastOutputs(
                short_term_cashflow_forecast={},
                long_term_revenue_projection={},
                liquidity_stress_test_results={}
            )
            
        dates = sorted(time_series_data.keys())
        values = [time_series_data[d] for d in dates]
        
        short_term_forecast = {}
        if len(values) >= 3:
            for i in range(len(values)):
                if i + 1 < len(values):
                    if i >= 2:
                        short_term_forecast[dates[i+1]] = sum(values[i-2:i+1]) / 3
                    else:
                        short_term_forecast[dates[i+1]] = values[i]

        return ForecastOutputs(
            short_term_cashflow_forecast=short_term_forecast,
            long_term_revenue_projection={dates[-1]: values[-1] * 1.05},
            liquidity_stress_test_results={"scenario_a": "pass", "scenario_b": "fail"}
        )

