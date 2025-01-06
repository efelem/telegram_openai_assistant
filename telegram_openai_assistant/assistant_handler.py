import time

class AssistantHandler:
    def __init__(self, client, assistant_id):
        self.client = client
        self.assistant_id = assistant_id
        self.thread_id = None
        self.message_history = []

    def get_answer(self, message_str):
        """Get answer from assistant."""
        # Create a thread if it doesn't exist
        if not self.thread_id:
            thread = self.client.beta.threads.create()
            self.thread_id = thread.id

        # Add the user message to the history
        self.message_history.append({"role": "user", "content": message_str})

        # Send the user message to the thread
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id, role="user", content=message_str
        )

        # Start a run for the assistant to process the thread
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
        )

        # Poll for the response
        while True:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id, run_id=run.id
            )
            if run.status == "completed":
                break
            time.sleep(1)

        # Retrieve the latest messages from the thread
        messages = self.client.beta.threads.messages.list(thread_id=self.thread_id)

        # Find the last assistant message
        # assistant_message = None
        # for message in reversed(messages.dict()["data"]):
        #     if message["role"] == "assistant":
        #         assistant_message = message["content"][0]["text"]["value"]
        #         break
        # import ipdb; ipdb.set_trace();
        assistant_message = messages.dict()['data'][0]["content"][0]["text"]["value"].strip()
        if not assistant_message:
            raise ValueError("No assistant response found in thread messages.")

        # Add the assistant's response to the history
        self.message_history.append({"role": "assistant", "content": assistant_message})

        # Manage message history to avoid exceeding token limits
        self.trim_message_history()

        return assistant_message


    def trim_message_history(self):
        """Trim history to maintain token limit."""
        max_messages = 20  # Adjust based on your token constraints
        if len(self.message_history) > max_messages:
            self.message_history = self.message_history[-max_messages:]