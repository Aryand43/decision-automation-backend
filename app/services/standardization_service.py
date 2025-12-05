from typing import Dict, Any, List
from datetime import date
import pandas as pd
from app.schema.bank_statement_schema import BankStatementInput, Transaction
from app.schema.credit_bureau_schema import CreditBureauInput
from app.schema.kyb_kyc_schema import KybKycInput

class StandardizationService:
    @staticmethod
    def standardize_bank_statement(raw_data: Dict[str, Any]) -> BankStatementInput:
        if "excel_data" in raw_data and isinstance(raw_data["excel_data"], list):
            excel_records = raw_data["excel_data"]
            transactions: List[Transaction] = []
            
            for record in excel_records:
                try:
                    transactions.append(
                        Transaction(
                            date=pd.to_datetime(record.get('Date')).date(),
                            description=record.get('Description', 'N/A'),
                            amount=float(record.get('Amount', 0.0)),
                            type=record.get('Type', 'unknown'),
                            balance=float(record.get('Balance')) if record.get('Balance') is not None else None
                        )
                    )
                except Exception as e:
                    print(f"Error parsing transaction record: {record} - {e}")
                    continue
            
            return BankStatementInput(
                account_holder_name="Default Account Holder",
                account_number="XXXX-XXXX-XXXX-1234",
                bank_name="Generic Bank",
                start_date=transactions[0].date if transactions else date.min,
                end_date=transactions[-1].date if transactions else date.max,
                transactions=transactions,
                currency="USD"
            )
        else:
            return BankStatementInput(**raw_data)

    @staticmethod
    def standardize_credit_bureau(raw_data: Dict[str, Any]) -> CreditBureauInput:
        return CreditBureauInput(**raw_data)

    @staticmethod
    def standardize_kyb_kyc(raw_data: Dict[str, Any]) -> KybKycInput:
        return KybKycInput(**raw_data)
