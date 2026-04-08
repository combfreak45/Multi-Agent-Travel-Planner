import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

load_dotenv()
cloud_logging_client = google.cloud.logging.Client()

model_name = os.getenv("MODEL")
