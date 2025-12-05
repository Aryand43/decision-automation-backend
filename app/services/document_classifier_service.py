from typing import Dict, Any

class DocumentClassifierService:
    @staticmethod
    def classify_document(document_content: Dict[str, Any]) -> str:
        content_str = str(document_content).lower()

        if "bank statement" in content_str or "transaction" in content_str and "balance" in content_str:
            return "bank_statement"
        elif "credit score" in content_str or "credit account" in content_str or "debt" in content_str:
            return "credit_bureau"
        elif "company name" in content_str or "registration number" in content_str or "kyc" in content_str or "kyb" in content_str:
            return "kyb_kyc"
        else:
            return "unknown"
