# bot.py
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from .config import telegram_token_bot1, telegram_token_bot2
from .handlers import start, help_command, process_message_bot1, process_message_bot2

# Initialize the two applications
application_bot1 = ApplicationBuilder().token(telegram_token_bot1).build()
application_bot2 = ApplicationBuilder().token(telegram_token_bot2).build()

def setup_handlers_bot1(app):
    """Sets up the command and message handlers for bot1."""
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message_bot1))

def setup_handlers_bot2(app):
    """Sets up the command and message handlers for bot2."""
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message_bot2))

async def start_bots():
    """Manages the startup and shutdown of both bots."""
    setup_handlers_bot1(application_bot1)
    setup_handlers_bot2(application_bot2)

    # Initialize both applications
    await application_bot1.initialize()
    await application_bot2.initialize()

    # Start both applications
    await application_bot1.start()
    await application_bot2.start()

    # Start polling for both bots
    await application_bot1.updater.start_polling()
    await application_bot2.updater.start_polling()

    try:
        # Keep the event loop running until interrupted
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Bots shutting down...")
    finally:
        # Stop polling for both bots
        await application_bot1.updater.stop()
        await application_bot2.updater.stop()

        # Stop both applications
        await application_bot1.stop()
        await application_bot2.stop()

        # Shutdown both applications
        await application_bot1.shutdown()
        await application_bot2.shutdown()

def main():
    """Main function to run the bots."""
    asyncio.run(start_bots())

if __name__ == "__main__":
    main()
