# 🚀 Railway Deployment Guide

## 📋 Prerequisites

Before deploying, ensure you have:

- ✅ **Railway Account**: Sign up at [railway.app](https://railway.app)
- ✅ **GitHub Repository**: Push your code to GitHub
- ✅ **Discord Bot Token**: Get from [Discord Developer Portal](https://discord.com/developers/applications)
- ✅ **OpenRouter API Key**: Get from [openrouter.ai](https://openrouter.ai)

## 📁 Repository Preparation

Make sure your repository includes these essential files:

| File | Purpose |
|------|---------|
| `Procfile` | Tells Railway how to run your app |
| `requirements.txt` | Python dependencies |
| `runtime.txt` | Python version specification |
| `railway.json` | Railway configuration |
| `.gitignore` | Excludes sensitive files |

## 🚀 Step-by-Step Deployment

### 🚀 One-Click Deploy (Recommended)

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/cozy-comfort)

Click the button above to deploy directly to Railway with our pre-configured template!

**Template Information:**
- **Category**: AI/ML
- **Required Variables**: 3 (GUILD_ID, UI_PASSWORD, DISCORD_BOT_TOKEN)
- **PostgreSQL**: Optional but recommended
- **Full-Stack**: Discord bot + web interface

**After clicking the deploy button:**
1. Connect your GitHub account
2. Set the required environment variables
3. Deploy automatically

### Manual Deployment

### Step 1: Connect to Railway

1. **Create New Project**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Wait for Initial Deploy**
   - Railway will automatically detect your Python app
   - Initial deployment may take 2-3 minutes

### Step 2: Configure Environment Variables

Navigate to your project's "Variables" tab and add:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
GUILD_ID=your_guild_id_here
FLASK_SECRET_KEY=your-secret-key-here
UI_PASSWORD=your-web-interface-password-here
```

**Important**: Replace the placeholder values with your actual credentials.

### Step 3: Add PostgreSQL Database (Optional)

1. **Add Database**
   - Go to "New" → "Database" → "PostgreSQL"
   - Railway will automatically add `DATABASE_URL` to your variables

2. **Wait for Provisioning**
   - Database provisioning takes 1-2 minutes
   - Check the "Variables" tab for the `DATABASE_URL`

### Step 4: Configure Discord Bot

1. **Update OAuth2 Settings**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Select your application
   - Go to "OAuth2" → "General"
   - Add your Railway domain to "Redirects"

2. **Verify Bot Permissions**
   Ensure your bot has these permissions:
   - ✅ Send Messages
   - ✅ Use Slash Commands
   - ✅ Read Message History

### Step 5: Test Your Deployment

1. **Health Check**
   - Visit `https://your-app.railway.app/health`
   - Should return a success response

2. **Web Interface**
   - Visit `https://your-app.railway.app/`
   - Should load the model management interface

3. **Discord Bot**
   - Use `/ping` in your Discord server
   - Should respond with "Pong! 🏓"

## 🔧 Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DISCORD_BOT_TOKEN` | Your Discord bot token | ✅ | None |
| `GUILD_ID` | Your Discord server ID | ✅ | None |
| `FLASK_SECRET_KEY` | Secret key for Flask sessions | ✅ | None |
| `DATABASE_URL` | Database connection string | ❌ | Auto-provided by Railway |
| `PORT` | Port for the web server | ❌ | Auto-set by Railway |
| `UI_PASSWORD` | Password for accessing the web interface | ❌ | None |

## 🔍 Troubleshooting

### Bot Not Responding

**Symptoms**: Bot appears offline or doesn't respond to commands

**Solutions**:
- ✅ Verify `DISCORD_BOT_TOKEN` is correct
- ✅ Check if the bot is online in your server
- ✅ Review Railway logs for connection errors
- ✅ Ensure bot has proper permissions

### Web Interface Not Loading

**Symptoms**: Website returns errors or doesn't load

**Solutions**:
- ✅ Check Railway logs for Flask startup errors
- ✅ Verify all environment variables are set
- ✅ Test the health endpoint: `/health`
- ✅ Ensure no syntax errors in your code

### Database Issues

**Symptoms**: Database connection errors or missing data

**Solutions**:
- ✅ Wait for PostgreSQL to fully provision (1-2 minutes)
- ✅ Verify `DATABASE_URL` is properly set
- ✅ Check for database connection errors in logs
- ✅ Restart deployment if database is stuck

### Common Error Messages

| Error | Solution |
|-------|----------|
| "Service unavailable" | Check Flask app startup in logs |
| "Bot not responding" | Verify Discord token and permissions |
| "Database connection failed" | Wait for PostgreSQL provisioning |
| "Environment variable missing" | Add required variables in Railway dashboard |

## 📊 Monitoring & Maintenance

### Railway Dashboard

1. **Resource Monitoring**
   - Monitor CPU, memory, and network usage
   - Set up alerts for resource limits

2. **Log Analysis**
   - Check application logs for errors
   - Monitor Discord bot connection status

3. **Health Monitoring**
   - Use `/health` endpoint to verify status
   - Set up external monitoring if needed

### Scaling Considerations

- **Automatic Scaling**: Railway scales based on traffic
- **Resource Limits**: Monitor usage in Railway dashboard
- **Cost Optimization**: Consider upgrading plan for more resources
- **Performance**: Monitor response times and error rates

## 🔒 Security Best Practices

### Environment Security
- 🚫 Never commit `.env` files to your repository
- 🔐 Use strong, unique secrets for `FLASK_SECRET_KEY`
- 🔄 Regularly rotate your Discord bot token and API keys
- 🛡️ Enable Railway's automatic HTTPS

### Access Control
- 🔑 Use strong, unique API keys for each model
- 👥 Limit bot permissions to minimum required
- 📊 Monitor usage for unusual activity
- 🔍 Regularly review and update security settings

## 💰 Cost Optimization

### Railway Pricing
- **Free Tier**: Limited resources, good for development
- **Paid Plans**: More resources and features
- **Usage-Based**: Pay for what you use

### Optimization Tips
- 📊 Monitor usage in Railway dashboard
- ⏰ Scale down during low-traffic periods
- 🔍 Review and optimize resource usage
- 💡 Consider free tier for development

## 🎉 Success Checklist

After deployment, verify:

- ✅ **Health Check**: `/health` endpoint responds
- ✅ **Web Interface**: Accessible at your Railway URL
- ✅ **Discord Bot**: Responds to `/ping` command
- ✅ **Model Management**: Can add/edit models via web interface
- ✅ **AI Chat**: `/ask` command works with your models
- ✅ **Environment Variables**: All required variables set
- ✅ **Database**: PostgreSQL connected (if using)

## 🆘 Getting Help

If you encounter issues:

1. **Check Railway Logs**: Look for specific error messages
2. **Verify Environment Variables**: Ensure all required variables are set
3. **Test Locally**: Try running the app locally first
4. **Review Documentation**: Check other guides in this repository
5. **Community Support**: Reach out for help if needed

---

**🎉 Congratulations! Your Discord AI bot is now deployed and running on Railway!**

- **🌐 Web Interface**: `https://your-app.railway.app/`
- **🔍 Health Check**: `https://your-app.railway.app/health`
- **🤖 Discord Bot**: Available in your server with slash commands 