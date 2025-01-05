# config.py
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file.
load_dotenv()

# Retrieve the variables from the environment.
assistant_id_bot1 = os.getenv("ASSISTANT_ID_BOT1")
assistant_id_bot2 = os.getenv("ASSISTANT_ID_BOT2")
client_api_key = os.getenv("CLIENT_API_KEY")
telegram_token_bot1 = os.getenv("TELEGRAM_TOKEN_BOT1")
telegram_token_bot2 = os.getenv("TELEGRAM_TOKEN_BOT2")