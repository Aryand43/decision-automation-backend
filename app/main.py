from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="Document Intelligence Backend",
    description="Glue layer for document processing and risk assessment",
    version="0.1.0",
)

app.include_router(api_router)
