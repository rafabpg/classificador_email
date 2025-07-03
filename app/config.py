import os
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = os.getenv("API_URL")
MODEL_ID = os.getenv("MODEL_ID")