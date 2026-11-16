import os

APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
APPROVAL_REQUIRED_FOR_WRITES = os.getenv("APPROVAL_REQUIRED_FOR_WRITES", "true").lower() == "true"
