# config.py
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file.
load_dotenv()

# Retrieve the variables from the environment and create lists
telegram_token_bots = [
    os.getenv("TELEGRAM_TOKEN_BOT1"),
    os.getenv("TELEGRAM_TOKEN_BOT2"),
    # Add more tokens as needed, e.g., os.getenv("TELEGRAM_TOKEN_BOT3")
]

assistant_id_bots = [
    os.getenv("ASSISTANT_ID_BOT1"),
    os.getenv("ASSISTANT_ID_BOT2"),
    # Add more assistant IDs as needed, e.g., os.getenv("ASSISTANT_ID_BOT3")
]

client_api_key = os.getenv("CLIENT_API_KEY")