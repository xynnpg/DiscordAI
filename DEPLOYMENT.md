# Railway Deployment Guide

## Prerequisites

Before deploying, ensure you have:

- **Railway Account**: Sign up at [railway.app](https://railway.app)
- **Discord Bot Token**: Get from [Discord Developer Portal](https://discord.com/developers/applications)
- **OpenRouter API Key**: Get from [openrouter.ai](https://openrouter.ai)

## Features Included

This deployment includes:

- 🤖 **Discord AI Bot** with slash commands
- 🧠 **Conversation Memory** - AI remembers previous conversations per user
- 🌐 **Web Interface** for model management
- 🔒 **Per-User Privacy** - each user's conversations are separate
- 📊 **Memory Management** - users can view and clear their conversation history

## Step-by-Step Deployment

### One-Click Deploy (Recommended)

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/discord-ai)

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

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DISCORD_BOT_TOKEN` | Your Discord bot token | **Yes** | None |
| `FLASK_SECRET_KEY` | Secret key for Flask sessions | **Yes** | None |
| `GUILD_ID` | Your Discord server ID | No | None |
| `DATABASE_URL` | PostgreSQL connection string | No | Auto-provided by Railway |
| `PORT` | Port for the web server | No | Auto-set by Railway |
| `UI_PASSWORD` | Password for accessing the web interface | No | None |

### Important Notes:
- **PostgreSQL Database**: Railway automatically provides a PostgreSQL database for conversation memory
- **Memory Storage**: All conversation history is stored securely in the database
- **GUILD_ID**: Optional - bot works in all servers if not specified

## Post-Deployment Setup

### 1. Add AI Models
After deployment:
1. Visit your Railway app URL (e.g., `https://your-app.railway.app`)
2. Add AI models through the web interface
3. Configure OpenRouter API keys for each model

### 2. Test Discord Commands
Test these commands in your Discord server:
- `/ping` - Check if bot is working
- `/models` - View available AI models
- `/change <model>` - Select an AI model
- `/ask <question>` - Ask AI with memory context
- `/memory_info` - View conversation statistics
- `/clear_memory` - Reset conversation history

### 3. Memory Features
The bot automatically:
- Creates database tables for conversation history
- Stores each user's conversations separately
- Provides context-aware AI responses
- Allows users to manage their own memory

## Tutorial

For a complete visual deployment guide, visit: **[Discord AI Setup Guide](https://xynnpg.github.io/DiscordAI/)**

This tutorial provides:
- Step-by-step Railway deployment instructions
- Environment variable configuration
- Post-deployment verification steps
- Memory feature walkthrough

## Discord Commands Reference

| Command | Description | Memory Feature |
|---------|-------------|----------------|
| `/ping` | Check bot status | - |
| `/ask <content>` | Ask AI question | ✅ Context-aware |
| `/change <model>` | Switch AI model | - |
| `/models` | List available models | - |
| `/memory_info` | View conversation stats | ✅ User statistics |
| `/clear_memory` | Reset conversation history | ✅ Privacy control |

## Troubleshooting

### Bot Not Responding

**Symptoms**: Bot appears offline or doesn't respond to commands

**Solutions**:
- Verify `DISCORD_BOT_TOKEN` is correct
- Check if the bot is online in your server
- Review Railway logs for connection errors
- Ensure bot has proper permissions

### Web Interface Not Loading

**Symptoms**: Website returns errors or doesn't load

**Solutions**:
- Check Railway logs for Flask startup errors
- Verify all environment variables are set
- Test the health endpoint: `/health`
- Ensure no syntax errors in your code

### Database Issues

**Symptoms**: Database connection errors or missing data

**Solutions**:
- Wait for PostgreSQL to fully provision (1-2 minutes)
- Verify `DATABASE_URL` is properly set
- Check for database connection errors in logs
- Restart deployment if database is stuck

### Common Error Messages

| Error | Solution |
|-------|----------|
| "Service unavailable" | Check Flask app startup in logs |
| "Bot not responding" | Verify Discord token and permissions |
| "Database connection failed" | Wait for PostgreSQL provisioning |
| "Environment variable missing" | Add required variables in Railway dashboard |

## Monitoring & Maintenance

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

## Security Best Practices

### Environment Security
- Never commit `.env` files to your repository
- Use strong, unique secrets for `FLASK_SECRET_KEY`
- Regularly rotate your Discord bot token and API keys
- Enable Railway's automatic HTTPS

### Access Control
- Use strong, unique API keys for each model
- Limit bot permissions to minimum required
- Monitor usage for unusual activity
- Regularly review and update security settings

## Cost Optimization

### Railway Pricing
- **Free Tier**: Limited resources, good for development
- **Paid Plans**: More resources and features
- **Usage-Based**: Pay for what you use

### Optimization Tips
- Monitor usage in Railway dashboard
- Scale down during low-traffic periods
- Review and optimize resource usage
- Consider free tier for development

## Success Checklist

After deployment, verify:

- **Health Check**: `/health` endpoint responds
- **Web Interface**: Accessible at your Railway URL
- **Discord Bot**: Responds to `/ping` command
- **Model Management**: Can add/edit models via web interface
- **AI Chat**: `/ask` command works with your models
- **Environment Variables**: All required variables set
- **Database**: PostgreSQL connected (if using)

## Getting Help

If you encounter issues:

1. **Check Railway Logs**: Look for specific error messages
2. **Verify Environment Variables**: Ensure all required variables are set
3. **Test Locally**: Try running the app locally first
4. **Review Documentation**: Check other guides in this repository
5. **Visit Tutorial**: Use the [Discord AI Setup Guide](https://xynnpg.github.io/DiscordAI/) for visual instructions
6. **Community Support**: Reach out for help if needed

---

**Congratulations! Your Discord AI bot is now deployed and running on Railway!**

- **Web Interface**: `https://your-app.railway.app/`
- **Health Check**: `https://your-app.railway.app/health`
- **Discord Bot**: Available in your server with slash commands 
