# OpenAI Assistant Telegram Bot

This repository provides a general framework for integrating an OpenAI Assistant with a Telegram bot. It allows users to interact with the OpenAI-powered conversational agent through the Telegram platform.

## Features

- Real-time response to user queries.
- Daily message count tracking.
- Storage of question and answer pairs for future retrieval and analysis.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have a `Python` environment running version 3.7+.
- You have a Telegram account and have created a bot with `@BotFather` to obtain a token.
- You have an `OpenAI` account to obtain your API keys.

You also need 

- An open ai assistant id : https://platform.openai.com/assistants
- An open ai API key : https://platform.openai.com/api-keys
- A telegram token : use botfather directly from telegram to create your bot and get the telegram token

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/efelem/telegram_openai_assistant
cd telegram_openai_assistant
```

Install the packages:

```bash
# If you want to create a venv
mkdir venv
python3 -m venv venv
source venv/bin/activate
# To install packages
pip install -e .
```

## Configuration

Create a `.env` file in the root directory and fill in your OpenAI and Telegram credentials. For consistency, both TELEGRAM_TOKEN_BOT and ASSISTANT_ID_BOT support comma-separated lists for multiple bot configurations.

Example .env file:

```env
TELEGRAM_TOKEN_BOT=bot1_token,bot2_token
ASSISTANT_ID_BOT=assistant1_id,assistant2_id
CLIENT_API_KEY=your-openai-api-key
```

If you have only one bot, simply provide a single value (e.g., bot1_token or assistant1_id).
Tokens and IDs will be processed as lists automatically.

## Usage

To start the bots, run the following command in your terminal:

```bash
chatbot
```

The bots should now be running and can be interacted with through your Telegram bot interface.

## Launching the Telegram Bot Client on DeepSquare

> This is not working, until the testnet is up and running again, happening soon.

You can easily launch the Telegram bot client using the `job.telegram_openai_assistant.yaml` workflow file in our repository. Follow these simple steps to get started:

### Launching through the DeepSquare Platform

1. **Log in to the DeepSquare Platform:** Ensure you are logged into [app.deepsquare.run](https://app.deepsquare.run).
2. **Navigate to Workflows:** Go to the 'Workflows' section in the platform.
3. **Create a new Workflow:** Click on the 'New Workflow' and copy paste the content of the `job.telegram_openai_assistant.yaml` file
4. **Start the Workflow:** Once created, you can start the workflow by clicking on the 'Run Workflow' button.
5. **Monitor and Access:** Monitor the progress of your job under the 'Jobs' section. Upon completion, access the Telegram bot as per the instructions provided in the job logs.

### Launching through the DeepSquare Command Line Tool

1. **Install DeepSquare CLI:** If you haven’t already, install the DeepSquare CLI tool. Instructions can be found [here](https://docs.deepsquare.run/cli/installation).
2. **Clone the Repository:** Clone the repository containing the `job.telegram_openai_assistant.yaml` file.
3. **Navigate to the Repository Directory:** Open a terminal and navigate to the directory where you cloned the repository.
4. **Run the Workflow File:** Execute the following command:

    ```bash
    deepsquare run job.telegram_openai_assistant.yaml
    ```

5. **Monitor the Job:** Use the following command to monitor the status of your job:

    ```bash
    deepsquare status
    ```

6. **Access the Telegram Bot:** Once the job is complete, follow the instructions provided in the job logs to access and interact with the Telegram bot.

By following these steps, you can effortlessly launch and interact with the Telegram bot client on DeepSquare.




## Contributions

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (\`git checkout -b feature/AmazingFeature\`)
3. Commit your Changes (\`git commit -m 'Add some AmazingFeature'\`)
4. Push to the Branch (\`git push origin feature/AmazingFeature\`)
5. Open a Pull Request

## License

Distributed under the MIT License. See \`LICENSE\` for more information.

## Contact

Project Link: [https://github.com/efelem/telegram_openai_assistant](https://github.com/efelem/telegram_openai_assistant)

