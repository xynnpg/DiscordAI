# Discord AI Chat Bot

A powerful Discord bot that integrates with OpenRouter APIs to provide AI chat capabilities. Features a web interface for managing multiple AI models and user-specific model preferences.

## Features

- 🤖 **AI Chat**: Ask questions using `/ask` command
- 🔄 **Model Switching**: Change AI models with `/change` command
- 👤 **User Preferences**: Each user can have their own preferred model
- 🌐 **Web Interface**: Beautiful Flask web interface for managing models
- 📊 **Multiple Models**: Support for multiple OpenRouter AI models
- ⚡ **Real-time**: Instant responses with proper error handling

## Discord Commands

- `/ping` - Check if the bot is working
- `/ask <content>` - Ask the AI a question
- `/change <model>` - Change your preferred AI model (with autocomplete)
- `/models` - Show available models and your current selection

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory with your Discord bot token and guild ID:

```
DISCORD_BOT_TOKEN=your_discord_bot_token_here
GUILD_ID=your_guild_id_here
FLASK_SECRET_KEY=your_secret_key_here
```

### 3. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and create a bot
4. Copy the bot token and add it to your `.env` file
5. Enable the following bot permissions:
   - Send Messages
   - Use Slash Commands
   - Read Message History
6. Invite the bot to your server using the OAuth2 URL

### 4. OpenRouter API Setup

1. Sign up at [OpenRouter](https://openrouter.ai/)
2. Get your API key
3. Use the web interface to add models with their official names

### 5. Running the Bot

```bash
python discord_bot.py
```

The bot will start and:
- Initialize the database
- Start the Flask web interface on `http://localhost:5000`
- Connect to Discord and sync slash commands

## Web Interface

Access the web interface at `http://localhost:5000` to:

- **Add Models**: Configure new AI models with their OpenRouter identifiers
- **Edit Models**: Modify existing model configurations
- **Toggle Models**: Enable/disable models for use
- **Delete Models**: Remove unused models

### Adding a Model

1. Go to the web interface
2. Click "Add New Model"
3. Fill in:
   - **Model Name**: Friendly name (e.g., "GPT-4", "Claude-3")
   - **Official Name**: OpenRouter model identifier (e.g., "openai/gpt-4")
   - **API Key**: Your OpenRouter API key

## Usage

### For Users

1. **First Time**: Use `/change <model_name>` to set your preferred model (autocomplete available)
2. **Ask Questions**: Use `/ask <your question>` to chat with the AI
3. **Switch Models**: Use `/change <model_name>` to select a different AI model
4. **Check Models**: Use `/models` to see available models and your current selection

### For Administrators

1. **Add Models**: Use the web interface to add new AI models
2. **Monitor Usage**: Check the bot logs for any issues
3. **Manage Models**: Enable/disable models as needed

## File Structure

```
DiscordAIChatBot/
├── discord_bot.py      # Main Discord bot
├── flask_web.py        # Flask web interface
├── openrouter_client.py # OpenRouter API client
├── database.py         # Database models
├── config.py           # Configuration
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── templates/         # Flask HTML templates
    ├── base.html
    ├── index.html
    ├── add_model.html
    └── edit_model.html
```

## Troubleshooting

### Bot Not Responding
- Check if the bot token is correct
- Ensure the bot has proper permissions
- Verify the bot is online in Discord

### AI Not Responding
- Check if the model is active in the web interface
- Verify the OpenRouter API key is correct
- Ensure the official model name is valid

### Web Interface Not Loading
- Check if Flask is running on port 5000
- Ensure no other application is using the port
- Check the console for any error messages

## Security Notes

- Keep your Discord bot token and API keys secure
- Never share your `.env` file
- Use strong, unique API keys for each model
- Regularly rotate your API keys

## Contributing

Feel free to submit issues and enhancement requests!

## 🚀 Deployment

This bot is ready for deployment on Railway! See the deployment guides:

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Pre-deployment checklist

### Quick Deploy

1. Push your code to GitHub
2. Connect to Railway
3. Add environment variables
4. Deploy!

## License

This project is open source and available under the MIT License. 