import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure to use Google AI API instead of Vertex AI
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

# Optional: Google Cloud logging (only if credentials are set up)
try:
    import google.cloud.logging
    cloud_logging_client = google.cloud.logging.Client()
    print("✓ Google Cloud logging initialized")
except Exception as e:
    cloud_logging_client = None
    print(f"⚠ Google Cloud logging not available (optional)")

model_name = os.getenv("MODEL", "gemini-2.0-flash-exp")
google_api_key = os.getenv("GOOGLE_API_KEY")


