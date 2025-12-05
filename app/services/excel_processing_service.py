import pandas as pd
from typing import Dict, Any, Union
from io import BytesIO

class ExcelProcessingService:
    @staticmethod
    def process_excel_file(file_content: bytes, document_type: str = "auto") -> Dict[str, Any]:
        df = pd.read_excel(BytesIO(file_content))

        if not df.empty:
            if all(col in df.columns for col in ['Date', 'Description', 'Amount', 'Type']):
                transactions = []
                for index, row in df.iterrows():
                    transactions.append({
                        "date": row['Date'].strftime('%Y-%m-%d'),
                        "description": row['Description'],
                        "amount": float(row['Amount']),
                        "type": row['Type'],
                        "balance": float(row['Balance']) if 'Balance' in row and pd.notna(row['Balance']) else None
                    })
                return {
                    "account_holder_name": "Dummy Account Holder",
                    "account_number": "123456789",
                    "bank_name": "Dummy Bank",
                    "start_date": df['Date'].min().strftime('%Y-%m-%d'),
                    "end_date": df['Date'].max().strftime('%Y-%m-%d'),
                    "transactions": transactions,
                    "currency": "USD"
                }
            else:
                return {"excel_data": df.to_dict(orient='records')}
        else:
            return {"excel_data": []}
