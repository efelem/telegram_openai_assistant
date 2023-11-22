# DeepSquare Bot

DeepSquare Bot is a conversational AI agent powered by OpenAI, designed to interact with users through Telegram. It leverages the OpenAI API to process and respond to messages.

## Features

- Responds to user queries in real-time.
- Keeps track of the daily message count.
- Stores question and answer pairs for future reference.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have a `Python` environment running version 3.7+.
- You have a Telegram account and have created a bot with `@BotFather` to obtain a token.
- You have an `OpenAI` account to obtain your API keys.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/deepsquare_bot.git
cd deepsquare_bot
```

Install the packages:

```bash
pip install -e .
```

## Configuration

Create a `.env` file in the root directory and fill in your OpenAI and Telegram credentials:

```env
ASSISTANT_ID=your-assistant-id
CLIENT_API_KEY=your-openai-api-key
TELEGRAM_TOKEN=your-telegram-bot-token
```

## Usage

To start the bot, run the following command in your terminal:

```bash
deepsquare-bot
```

The bot should now be running and can be interacted with through your Telegram bot interface.

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

Project Link: [https://github.com/your-username/deepsquare_bot](https://github.com/your-username/deepsquare_bot)

