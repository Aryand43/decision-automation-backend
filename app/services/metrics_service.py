from typing import List, Dict, Any
from datetime import date
from app.schema.output_schema import CashflowMetrics, LiquidityMetrics, FinancialDisciplineMetrics, DebtServicingMetrics, RiskIndicators
from app.schema.bank_statement_schema import BankStatementInput, Transaction

class MetricsService:
    @staticmethod
    def calculate_cashflow_metrics(bank_statement: BankStatementInput) -> CashflowMetrics:
        total_inflow = sum(t.amount for t in bank_statement.transactions if t.type == 'credit')
        total_outflow = sum(t.amount for t in bank_statement.transactions if t.type == 'debit')
        net_cashflow = total_inflow - total_outflow
        return CashflowMetrics(
            total_inflow=total_inflow,
            total_outflow=total_outflow,
            net_cashflow=net_cashflow,
            average_monthly_cashflow=net_cashflow,
            cashflow_volatility=0.0
        )

    @staticmethod
    def calculate_liquidity_metrics(bank_statement: BankStatementInput) -> LiquidityMetrics:
        current_assets = sum(t.balance for t in bank_statement.transactions if t.balance is not None and t.type == 'credit')
        current_liabilities = sum(t.balance for t in bank_statement.transactions if t.balance is not None and t.type == 'debit')
        
        if current_liabilities == 0:
            current_ratio = 0.0
            quick_ratio = 0.0
        else:
            current_ratio = current_assets / current_liabilities
            quick_ratio = current_assets / current_liabilities

        return LiquidityMetrics(
            current_ratio=current_ratio,
            quick_ratio=quick_ratio,
            cash_conversion_cycle=None,
            days_cash_on_hand=current_assets
        )

    @staticmethod
    def calculate_financial_discipline_metrics(bank_statement: BankStatementInput) -> FinancialDisciplineMetrics:
        overdraft_frequency = 0
        late_payment_count = 0
        bounced_cheque_count = 0
        
        total_inflow = sum(t.amount for t in bank_statement.transactions if t.type == 'credit')
        savings = 0.0
        savings_rate = savings / total_inflow if total_inflow > 0 else 0.0

        return FinancialDisciplineMetrics(
            overdraft_frequency=overdraft_frequency,
            late_payment_count=late_payment_count,
            bounced_cheque_count=bounced_cheque_count,
            savings_rate=savings_rate
        )
    
    @staticmethod
    def calculate_debt_servicing_metrics(bank_statement: BankStatementInput, total_debt: float = 0.0) -> DebtServicingMetrics:
        total_outflow = sum(t.amount for t in bank_statement.transactions if t.type == 'debit')
        annual_debt_payments = total_outflow * 0.1
        ebitda = sum(t.amount for t in bank_statement.transactions if t.type == 'credit') * 0.5
        
        if annual_debt_payments > 0:
            dscr = ebitda / annual_debt_payments
        else:
            dscr = 0.0
            
        debt_to_income_ratio = total_debt / sum(t.amount for t in bank_statement.transactions if t.type == 'credit') if sum(t.amount for t in bank_statement.transactions if t.type == 'credit') > 0 else 0.0
        loan_payment_to_income_ratio = annual_debt_payments / sum(t.amount for t in bank_statement.transactions if t.type == 'credit') if sum(t.amount for t in bank_statement.transactions if t.type == 'credit') > 0 else 0.0

        return DebtServicingMetrics(
            dscr=dscr,
            debt_to_income_ratio=debt_to_income_ratio,
            loan_payment_to_income_ratio=loan_payment_to_income_ratio
        )

    @staticmethod
    def identify_risk_indicators(bank_statement: BankStatementInput, credit_score_change: float = 0.0, negative_news_mentions: int = 0, bankruptcy_flags: bool = False) -> RiskIndicators:
        high_risk_transactions = []

        average_debit = sum(t.amount for t in bank_statement.transactions if t.type == 'debit') / len([t for t in bank_statement.transactions if t.type == 'debit']) if any(t.type == 'debit' for t in bank_statement.transactions) else 0
        for t in bank_statement.transactions:
            if t.type == 'debit' and t.amount > average_debit * 2:
                high_risk_transactions.append(t.dict())

        return RiskIndicators(
            high_risk_transactions=high_risk_transactions,
            credit_score_change=credit_score_change,
            negative_news_mentions=negative_news_mentions,
            bankruptcy_flags=bankruptcy_flags
        )
