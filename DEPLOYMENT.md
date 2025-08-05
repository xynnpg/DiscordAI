# Railway Deployment Guide

## 🚀 Deploying to Railway

### Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Push your code to GitHub
3. **Discord Bot Token**: Get from Discord Developer Portal
4. **OpenRouter API Key**: Get from [openrouter.ai](https://openrouter.ai)

### Step 1: Prepare Your Repository

Make sure your repository has these files:
- `Procfile` - Tells Railway how to run your app
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version
- `railway.json` - Railway configuration
- `.gitignore` - Excludes sensitive files

### Step 2: Deploy to Railway

1. **Connect to Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Add Environment Variables**:
   - Go to your project's "Variables" tab
   - Add these environment variables:

```
DISCORD_BOT_TOKEN=your_discord_bot_token_here
GUILD_ID=your_guild_id_here
FLASK_SECRET_KEY=your-secret-key-here
```

3. **Add PostgreSQL Database** (Optional):
   - Go to "New" → "Database" → "PostgreSQL"
   - Railway will automatically add `DATABASE_URL` to your variables

### Step 3: Configure Discord Bot

1. **Update Bot Invite URL**:
   - Go to Discord Developer Portal
   - Update your bot's OAuth2 redirect URL to your Railway domain
   - Add your Railway domain to "Allowed Redirects"

2. **Update Bot Permissions**:
   - Ensure your bot has these permissions:
     - Send Messages
     - Use Slash Commands
     - Read Message History

### Step 4: Test Your Deployment

1. **Check Health**: Visit `https://your-app.railway.app/health`
2. **Test Web Interface**: Visit `https://your-app.railway.app/`
3. **Test Discord Bot**: Use `/ping` in Discord

### Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `DISCORD_BOT_TOKEN` | Your Discord bot token | ✅ |
| `GUILD_ID` | Your Discord server ID | ✅ |
| `FLASK_SECRET_KEY` | Secret key for Flask sessions | ✅ |
| `DATABASE_URL` | Database connection string | ❌ (auto-added by Railway) |
| `PORT` | Port for the web server | ❌ (auto-set by Railway) |

### Troubleshooting

#### Bot Not Responding
- Check if `DISCORD_BOT_TOKEN` is correct
- Verify the bot is online in your server
- Check Railway logs for errors

#### Web Interface Not Loading
- Check Railway logs for Flask errors
- Verify all environment variables are set
- Check if the health endpoint responds

#### Database Issues
- If using PostgreSQL, wait for Railway to provision the database
- Check if `DATABASE_URL` is properly set
- Look for database connection errors in logs

### Monitoring

1. **Railway Dashboard**: Monitor CPU, memory, and network usage
2. **Logs**: Check application logs for errors
3. **Health Check**: Use `/health` endpoint to verify status

### Scaling

- Railway automatically scales based on traffic
- Upgrade your plan for more resources if needed
- Monitor usage in the Railway dashboard

### Security Notes

- Never commit `.env` files to your repository
- Use strong, unique secrets for `FLASK_SECRET_KEY`
- Regularly rotate your Discord bot token and API keys
- Enable Railway's automatic HTTPS

### Cost Optimization

- Railway charges based on usage
- Consider using the free tier for development
- Monitor your usage in the Railway dashboard
- Scale down during low-traffic periods

## 🎉 Success!

Your Discord AI bot is now deployed and running on Railway! 

- **Web Interface**: `https://your-app.railway.app/`
- **Health Check**: `https://your-app.railway.app/health`
- **Discord Bot**: Available in your server with slash commands 