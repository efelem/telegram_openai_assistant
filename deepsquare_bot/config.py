# config.py
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file.
load_dotenv()

# Retrieve the variables from the environment.
assistant_id = os.getenv("ASSISTANT_ID")
client_api_key = os.getenv("CLIENT_API_KEY")
telegram_token = os.getenv("TELEGRAM_TOKEN")
