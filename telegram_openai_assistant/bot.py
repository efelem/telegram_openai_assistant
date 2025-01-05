import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from .config import telegram_token_bots, assistant_id_bots
from .handlers import BotHandlers

class Bot:
    def __init__(self, token: str, assistant_id: str):
        """Initialize the bot application with a token and assistant_id"""
        self.application = ApplicationBuilder().token(token).build()
        self.assistant_id = assistant_id
        self.handlers = BotHandlers(self.assistant_id, token)
        self.setup_handlers()

    def setup_handlers(self):
        """Sets up the command and message handlers."""
        self.application.add_handler(CommandHandler("start", self.handlers.start))
        self.application.add_handler(CommandHandler("help", self.handlers.help_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.process_message))

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


async def start_bots():
    """Runs all bot applications concurrently."""
    bots = [
        Bot(token, assistant_id)
        for token, assistant_id in zip(telegram_token_bots, assistant_id_bots)
    ]
    
    # Start all bots concurrently
    start_tasks = [bot.start() for bot in bots]
    await asyncio.gather(*start_tasks)

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
    asyncio.run(start_bots())


if __name__ == "__main__":
    main()
