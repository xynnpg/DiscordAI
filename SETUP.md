# Setup Guide

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create Environment File**
   Create a `.env` file in the root directory with:
   ```
   DISCORD_BOT_TOKEN=MTM5ODY2ODEzMzM4MzkyOTg4Ng.GIbhD8.3cGw4I6ps4SecKK8tckVvOf3h7wgAI4y48WW5Q
   GUILD_ID=1398670692077142037
   FLASK_SECRET_KEY=your-secret-key-here
   ```

3. **Run the Bot**
   ```bash
   python run.py
   ```

## Detailed Setup

### Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot"
5. Copy the bot token and add it to your `.env` file
6. Under "Privileged Gateway Intents", enable:
   - Message Content Intent
7. Go to "OAuth2" → "URL Generator"
8. Select scopes: `bot` and `applications.commands`
9. Select bot permissions:
   - Send Messages
   - Use Slash Commands
   - Read Message History
10. Copy the generated URL and invite the bot to your server

### OpenRouter API Setup

1. Sign up at [OpenRouter](https://openrouter.ai/)
2. Get your API key from the dashboard
3. Use the web interface (http://localhost:5000) to add models

### Adding Your First Model

1. Start the bot: `python run.py`
2. Open http://localhost:5000 in your browser
3. Click "Add New Model"
4. Fill in the details:
   - **Model Name**: `GPT-4` (friendly name)
   - **Official Name**: `openai/gpt-4` (OpenRouter identifier)
   - **API Key**: Your OpenRouter API key
5. Click "Add Model"

### Testing the Bot

1. In Discord, use `/ping` to test if the bot is working
2. Use `/change <model_name>` to set your preferred model (autocomplete will show available models)
3. Use `/models` to see available models and your current selection
4. Use `/ask Hello, how are you?` to test the AI

## Common Issues

### Bot Not Responding
- Check if the bot token is correct
- Ensure the bot is online in your server
- Verify the bot has proper permissions

### AI Not Working
- Check if the model is active in the web interface
- Verify the OpenRouter API key is correct
- Ensure you've set a model with `/change`

### Web Interface Not Loading
- Check if port 5000 is available
- Ensure the bot is running
- Check console for error messages 