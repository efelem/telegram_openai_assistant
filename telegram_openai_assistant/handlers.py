from telegram.ext import CallbackContext
from telegram import Update


class BotHandlers:
    def __init__(self, bot_name: str, assistant_id: str, telegram_id: str, manager):
        self.assistant_id = assistant_id
        self.telegram_id = telegram_id
        self.bot_name = bot_name
        self.manager = manager

    async def start(self, update: Update, context: CallbackContext) -> None:
        """Sends a welcome message to the user."""
        print("I am doing smth")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Hello! Ask me anything."
        )

    async def help_command(self, update: Update, context: CallbackContext) -> None:
        """Sends a help message to the user."""
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Just send me a question and I'll try to answer it.",
        )

    async def process_message(self, update: Update, context: CallbackContext) -> None:
        """Handles incoming messages and delegates to ConversationManager."""
        if update.message is None:
            return  # No message to process

        chat_type = update.effective_chat.type
        group_id = update.effective_chat.id
        message_text = update.message.text

        # Ensure the bot is mentioned and the message is in a group
        if chat_type == "group" and update.message.entities:
            for entity in update.message.entities:
                if entity.type == 'mention' and '@' + context.bot.username in message_text[entity.offset:entity.offset + entity.length]:
                    if not self.manager.is_active(group_id):
                        # Start a new conversation with all participating bots
                        if self.manager.start_conversation(group_id, self.bot_name):
                            await context.bot.send_message(
                                chat_id=group_id,
                                text=f"Conversation started by {self.bot_name} on group {group_id}. Use /end to terminate."
                            )
                            # Trigger the first turn
                            await self.manager.handle_turn(update.message.text)
                    else:
                        # Ignore incoming messages while a conversation is ongoing
                        await context.bot.send_message(
                            chat_id=group_id,
                            text="A conversation is already active. Please wait until it ends."
                        )

    async def end_conversation(self, update: Update, context: CallbackContext) -> None:
        """Ends the active conversation."""
        group_id = update.effective_chat.id
        if self.manager.end_conversation(group_id):
            await context.bot.send_message(
                chat_id=group_id,
                text=f"Conversation ended by {self.bot_name}."
            )
        else:
            await context.bot.send_message(
                chat_id=group_id,
                text="No active conversation in this group to end."
            )