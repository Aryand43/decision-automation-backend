import pandas as pd
import json
import httpx
import asyncio
import os

async def run_test_with_bank_xlsx():
    print("Step 1: Reading bank.xlsx file...")
    file_path = "test/bank.xlsx"
    
    # Ensure the file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}. Please ensure bank.xlsx is in the 'test' directory.")
        return

    try:
        df = pd.read_excel(file_path)
        print("bank.xlsx read successfully.")
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Convert any datetime columns to ISO format strings for JSON serialization
    # Handle NaT values by converting them to None, then applying isoformat to valid datetimes
    for col in df.select_dtypes(include=['datetime', 'datetimetz']).columns:
        df[col] = df[col].apply(lambda x: x.isoformat() if pd.notna(x) else None)

    print("Step 2: Preparing document payload...")
    excel_data_list = df.to_dict(orient='records')

    document_content = {
        "excel_data": excel_data_list
    }

    request_payload = {
        "document": {
            "document_id": "bank_statement_test_001",
            "content": document_content,
            "metadata": {"filename": "bank.xlsx", "source": "test"}
        }
    }
    print("Payload prepared.")

    print("\nStep 3: Sending request to FastAPI endpoint...")
    fastapi_url = "http://localhost:8000/document/analyze-document" # Corrected URL
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(fastapi_url, json=request_payload, timeout=60.0)
            response.raise_for_status()
            
            print("\n--- API Response Start ---")
            api_response = response.json()
            print(json.dumps(api_response, indent=2))
            print("--- API Response End ---\n")
            
            print("Test completed. Please share the API response above for verification.")
            return api_response

        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            print("Please ensure your FastAPI server is running on http://127.0.0.1:8000")
        except httpx.HTTPStatusError as exc:
            print(f"Error response {exc.response.status_code} from {exc.request.url!r}:")
            print(exc.response.text)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(run_test_with_bank_xlsx())
