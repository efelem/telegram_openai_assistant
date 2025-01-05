# handlers.py
import time
import datetime
from telegram.ext import CallbackContext
from telegram import Update
from openai import OpenAI

from .config import assistant_id_bot1, assistant_id_bot2, client_api_key
from .utils import get_message_count, update_message_count, save_qa


client = OpenAI(api_key=client_api_key)


async def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message to the user."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello! Ask me anything."
    )


async def help_command(update: Update, context: CallbackContext) -> None:
    """Sends a help message to the user."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Just send me a question and I'll try to answer it.",
    )


def get_answer(message_str, assistant_id) -> None:
    """Get answer from assistant using the correct assistant_id."""
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=message_str
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,  # Use the assistant_id passed here
    )

    # Poll for the response (this could be improved with async calls)
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(run.status)
        if run.status == "completed":
            break
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.dict()["data"][0]["content"][0]["text"]["value"]
    return response

async def process_message_bot1(update: Update, context: CallbackContext):
    """Handles messages for bot1."""
    await process_message(update, context, bot_name='bot1', assistant_id=assistant_id_bot1)

async def process_message_bot2(update: Update, context: CallbackContext):
    """Handles messages for bot2."""
    await process_message(update, context, bot_name='bot2', assistant_id=assistant_id_bot2)


async def process_message(update: Update, context: CallbackContext, bot_name: str, assistant_id: str) -> None:
    """Processes a message from the user, gets an answer, and sends it back."""
    # Ensure update.message is not None
    if update.message is None:
        return  # Exit if the message is None

    chat_type = update.effective_chat.type  # Chat type: private, group, or supergroup
    message_text = update.message.text
    # Check if the message has entities and if there is a mention of the bot
    if update.message.entities:
        for entity in update.message.entities:
            if entity.type == 'mention' and '@' + context.bot.username in message_text[entity.offset:entity.offset + entity.length]:
                message_data = get_message_count()
                count = message_data["count"]
                date = message_data["date"]
                today = str(datetime.date.today())

                if date != today:
                    count = 0
                if count >= 100:
                    return
                answer = get_answer(update.message.text, assistant_id).strip()
                await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
                update_message_count(count + 1)
                save_qa(
                    update.effective_user.id,
                    update.effective_user.username,
                    update.message.text,
                    answer,
                    bot_name  # Pass the bot's name here
                )
    else:
        message_data = get_message_count()
        count = message_data["count"]
        date = message_data["date"]
        today = str(datetime.date.today())

        if date != today:
            count = 0
        if count >= 100:
            return

        answer = get_answer(update.message.text, assistant_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
        update_message_count(count + 1)
        save_qa(
            update.effective_user.id,
            update.effective_user.username,
            update.message.text,
            answer,
            bot_name  # Pass the bot's name here
        )
