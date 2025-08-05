# 🚀 Setup Guide

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Environment File
Create a `.env` file in the root directory:
```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
GUILD_ID=your_guild_id_here
FLASK_SECRET_KEY=your-secret-key-here
```

### 3. Run the Bot
```bash
python run.py
```

## 📋 Detailed Setup

### Discord Bot Setup

1. **Create Application**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name

2. **Create Bot**
   - Go to the "Bot" section in the left sidebar
   - Click "Add Bot"
   - Copy the bot token and add it to your `.env` file

3. **Configure Permissions**
   - Under "Privileged Gateway Intents", enable:
     - ✅ Message Content Intent

4. **Generate Invite URL**
   - Go to "OAuth2" → "URL Generator"
   - Select scopes: `bot` and `applications.commands`
   - Select bot permissions:
     - ✅ Send Messages
     - ✅ Use Slash Commands
     - ✅ Read Message History
   - Copy the generated URL and invite the bot to your server

### OpenRouter API Setup

1. **Sign Up**
   - Visit [OpenRouter](https://openrouter.ai/)
   - Create an account

2. **Get API Key**
   - Navigate to your dashboard
   - Copy your API key

3. **Add Models**
   - Use the web interface to add models with their official names

### Adding Your First Model

1. **Start the Bot**
   ```bash
   python run.py
   ```

2. **Access Web Interface**
   - Open http://localhost:5000 in your browser

3. **Add Model**
   - Click "Add New Model"
   - Fill in the details:
     - **Model Name**: `GPT-4` (friendly name)
     - **Official Name**: `openai/gpt-4` (OpenRouter identifier)
     - **API Key**: Your OpenRouter API key
   - Click "Add Model"

### Testing the Bot

1. **Basic Test**
   ```discord
   /ping
   ```
   Should respond with "Pong! 🏓"

2. **Set Your Model**
   ```discord
   /change GPT-4
   ```
   Use autocomplete to select your preferred model

3. **Check Available Models**
   ```discord
   /models
   ```
   Shows all available models and your current selection

4. **Test AI Chat**
   ```discord
   /ask Hello, how are you?
   ```
   Should get a response from your selected AI model

## 🔧 Common Issues

### Bot Not Responding
- ✅ Check if the bot token is correct
- ✅ Ensure the bot is online in your server
- ✅ Verify the bot has proper permissions

### AI Not Working
- ✅ Check if the model is active in the web interface
- ✅ Verify the OpenRouter API key is correct
- ✅ Ensure you've set a model with `/change`

### Web Interface Not Loading
- ✅ Check if port 5000 is available
- ✅ Ensure the bot is running
- ✅ Check console for error messages

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DISCORD_BOT_TOKEN` | Your Discord bot token | ✅ |
| `GUILD_ID` | Your Discord server ID | ✅ |
| `FLASK_SECRET_KEY` | Secret key for Flask sessions | ✅ |

## 🎯 Next Steps

After setup, you can:
- 🌐 Access the web interface to manage models
- 💬 Start chatting with AI using `/ask`
- 🔄 Switch between different AI models
- 📊 Monitor usage and performance

## 🆘 Need Help?

- 📖 Check the [README.md](README.md) for detailed information
- 🔧 See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- 🚀 Review [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment 