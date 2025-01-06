# config.py
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file.
load_dotenv()

# Retrieve TELEGRAM_TOKEN as a comma-separated string and split it into a list
telegram_token_bots = os.getenv("TELEGRAM_TOKEN_BOT", "").split(",")

# Retrieve ASSISTANT_ID as a comma-separated string and split it into a list
assistant_id_bots = os.getenv("ASSISTANT_ID_BOT", "").split(",")

client_api_key = os.getenv("CLIENT_API_KEY")

# Optional: Clean up whitespace from each item in the lists
telegram_token_bots = [token.strip() for token in telegram_token_bots if token.strip()]
assistant_id_bots = [aid.strip() for aid in assistant_id_bots if aid.strip()]

# Debugging print to verify the lists (remove in production)
print("Telegram Tokens:", telegram_token_bots)
print("Assistant IDs:", assistant_id_bots)
print("Client API Key:", client_api_key)
