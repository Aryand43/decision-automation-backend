import os

class Settings:
    PROJECT_NAME: str = "Document Intelligence Backend"
    PROJECT_VERSION: str = "0.1.0"
    # Example of how to load from environment variables
    # DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

settings = Settings()
