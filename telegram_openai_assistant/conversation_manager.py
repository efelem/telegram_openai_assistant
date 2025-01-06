import time
import asyncio
from typing import Optional, Dict

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
        response = next_bot.assistant_handler.get_answer(message).strip()  # Use the bot's `get_answer`

        # Calculate the time taken to generate the answer
        elapsed_time = time.monotonic() - start_time

        # Ensure the delay is between 5-15 seconds
        delay = max(15, 25 - elapsed_time)  # Delay is 5 seconds minimum, subtract the elapsed time

        print(f"The bot {next_bot_name} tries to answer in group {self.group_id} with response {response}")
        await next_bot.application.bot.send_message(chat_id=self.group_id, text=f"{response}")

        # Wait for the remaining delay time
        await asyncio.sleep(delay)

        # Continue to the next turn (simulate continuous conversation)
        if self.is_active(self.group_id):  # Only continue if conversation is still active
            await self.handle_turn(response)

