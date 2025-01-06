import asyncio
import time
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram import Update
from typing import Optional, Dict
from .config import telegram_token_bots, assistant_id_bots
from .handlers import BotHandlers

class ConversationManager:
    """Manages global state and orchestrates bot-to-bot conversations."""
    def __init__(self):
        self.all_bots: Dict[str, 'Bot'] = {}  # Dictionary to hold all bots by name
        self.active_conversation: Optional[Dict[str, str]] = None
        self.bot_order: list[str] = []  # List of bot names in fixed order
        self.current_bot_index: int = 0  # Tracks the current bot in the rotation
        self.group_id: Optional[int] = None  # Active group's ID

    def register_bots(self, bots: Dict[str, 'Bot']):
        """Register all bots after their creation."""
        self.all_bots = bots
        self.bot_order = list(bots.keys())

    def start_conversation(self, group_id: int, initiating_bot: str) -> Optional[str]:
        """
        Start a conversation if no active conversation exists.
        
        Returns:
            The name of the bot that should respond first, or None if the conversation can't start.
        """
        if self.active_conversation is None:
            self.active_conversation = {"group_id": group_id, "initiating_bot": initiating_bot}
            self.group_id = group_id

            # Find the position of the initiating bot and set the index to the next bot
            initiating_index = self.bot_order.index(initiating_bot)
            self.current_bot_index = (initiating_index + 1) % len(self.bot_order)
            return self.bot_order[self.current_bot_index]  # Return the next bot in rotation
        return None

    def is_active(self, group_id: int) -> bool:
        """Check if the current group has an active conversation."""
        return self.active_conversation and self.group_id == group_id

    def end_conversation(self, group_id: int) -> bool:
        """End the active conversation if it matches the group."""
        if self.active_conversation and self.group_id == group_id:
            self.active_conversation = None
            self.group_id = None
            self.current_bot_index = 0  # Reset the rotation index
            return True
        return False

    def get_next_bot(self) -> Optional[str]:
        """Get the next bot to respond in the conversation."""
        if not self.bot_order:
            return None  # No bots registered

        # Move to the next bot in the rotation
        self.current_bot_index = (self.current_bot_index + 1) % len(self.bot_order)
        return self.bot_order[self.current_bot_index]

    async def handle_turn(self, message: str) -> None:
        """Orchestrates the next bot's response with a delay."""
        if not self.group_id or not self.bot_order:
            return  # No active conversation or no bots available

        next_bot_name = self.get_next_bot()
        if not next_bot_name:
            return  # No bot available to respond

        next_bot = self.all_bots[next_bot_name]  # Get the bot instance

        # Record the start time to measure response time
        start_time = time.monotonic()

        # Generate the response using the bot's logic
        response = next_bot.handlers.get_answer(message).strip()  # Use the bot's `get_answer`

        # Calculate the time taken to generate the answer
        elapsed_time = time.monotonic() - start_time

        # Ensure the delay is between 5-15 seconds
        delay = max(5, 15 - elapsed_time)  # Delay is 5 seconds minimum, subtract the elapsed time

        print(f"The bot {next_bot_name} tries to answer in group {self.group_id} with response {response}")
        await next_bot.application.bot.send_message(chat_id=self.group_id, text=f"{response}")

        # Wait for the remaining delay time
        await asyncio.sleep(delay)

        # Continue to the next turn (simulate continuous conversation)
        if self.is_active(self.group_id):  # Only continue if conversation is still active
            await self.handle_turn(response)


class Bot:
    def __init__(self, bot_name: str, token: str, assistant_id: str, manager: ConversationManager):
        """Initialize the bot application with a token and assistant_id"""
        self.token = token
        self.bot_name = bot_name
        self.assistant_id = assistant_id
        self.manager = manager
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
