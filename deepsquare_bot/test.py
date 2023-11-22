import openai as client
import ipdb
import time
import sys

# Replace 'your-assistant-id' with the Assistant ID from OpenAI's platform
assistant_id = ""
# Replace 'your-api-key' with your actual API key
client.api_key = ""
thread = client.beta.threads.create()

message_str = " ".join(sys.argv[1:])

message = client.beta.threads.messages.create(
    thread_id=thread.id, role="user", content=message_str
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id,
)

while True:
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    print(run.status)
    if run.status == "completed":
        break
    time.sleep(1)


messages = client.beta.threads.messages.list(thread_id=thread.id)

print(messages.dict()["data"][0]["content"][0]["text"]["value"])
