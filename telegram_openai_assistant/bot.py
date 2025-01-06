import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram import Update
from openai import OpenAI

from .conversation_manager import ConversationManager
from .assistant_handler import AssistantHandler
from .config import telegram_token_bots, assistant_id_bots
from .handlers import BotHandlers

from .config import client_api_key

client = OpenAI(api_key=client_api_key)

class Bot:
    def __init__(self, bot_name: str, token: str, assistant_id: str, manager: ConversationManager):
        """Initialize the bot application with a token and assistant_id"""
        self.token = token
        self.bot_name = bot_name
        self.assistant_id = assistant_id
        self.manager = manager
        self.assistant_handler = AssistantHandler(client, assistant_id)
        self.handlers = BotHandlers(bot_name, assistant_id, token, manager)
        self.application = ApplicationBuilder().token(token).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Sets up the command and message handlers."""
        self.application.add_handler(CommandHandler("start", self.handlers.start))
        self.application.add_handler(CommandHandler("help", self.handlers.help_command))
        self.application.add_handler(CommandHandler("end", self.end_conversation))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.process_message))

    async def end_conversation(self, update: Update, context):
        """End the current conversation."""
        group_id = update.message.chat.id
        if self.manager.end_conversation(group_id):
            await context.bot.send_message(
                chat_id=group_id, text=f"Conversation ended by {self.bot_name}."
            )
        else:
            await context.bot.send_message(
                chat_id=group_id,
                text="No active conversation in this group to end.",
            )

    async def send_message(self, message: str):
        """Send a message to the specified chat_id"""
        await self.application.bot.send_message(chat_id=self.chat_id, text=message)

    async def start(self):
        """Start the bot."""
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

    async def stop(self):
        """Stop the bot."""
        await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()


async def start_bots(manager: ConversationManager):
    """Runs all bot applications concurrently."""
    names = ["Regen", "Degen"]
    bots = {
        name: Bot(name, token, assistant_id, manager)
        for name, token, assistant_id in zip(names, telegram_token_bots, assistant_id_bots)
    }
    manager.register_bots(bots)
    # Start all bots concurrently
    await asyncio.gather(*(bot.start() for bot in bots.values()))

    try:
        # Keep the event loop running until interrupted
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Bots shutting down...")
    finally:
        # Stop polling for all bots
        stop_tasks = [bot.application.updater.stop() for bot in bots]
        await asyncio.gather(*stop_tasks)

        # Stop all applications
        stop_tasks = [bot.application.stop() for bot in bots]
        await asyncio.gather(*stop_tasks)

        # Shutdown all applications
        shutdown_tasks = [bot.application.shutdown() for bot in bots]
        await asyncio.gather(*shutdown_tasks)


def main():
    """Main function to run the bots."""
    manager = ConversationManager()
    asyncio.run(start_bots(manager))


if __name__ == "__main__":
    main()
