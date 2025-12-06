import pandas as pd
import json

# 1. Read the bank.xlsx file
file_path = "test/bank.xlsx"
df = pd.read_excel(file_path)

# 2. Convert DataFrame to the expected dictionary format for IngestionService
# The IngestionService expects a dictionary with an 'excel_data' key, which is a list of dictionaries (rows).
excel_data_list = df.to_dict(orient='records')

# Create the document content dictionary
document_content = {
    "excel_data": excel_data_list
}

# Create the DocumentAnalysisRequest structure
# This mimics the structure expected by your FastAPI endpoint
request_payload = {
    "document": {
        "document_id": "bank_statement_test_001",
        "content": document_content,
        "metadata": {"filename": "bank.xlsx", "source": "test"}
    }
}

# For demonstration, print the first few records and the overall structure
print("\nFirst 5 records of excel_data:")
print(json.dumps(excel_data_list[:5], indent=2))

print("\nFull request payload structure:")
print(json.dumps(request_payload, indent=2))

# In a real scenario, you would send this `request_payload` to your FastAPI endpoint.
# Example using httpx (if you were to run this in a separate script):
# import httpx
# async def send_request():
#     async with httpx.AsyncClient() as client:
#         response = await client.post("http://localhost:8000/analyze-document", json=request_payload)
#         print(response.json())
# asyncio.run(send_request())

