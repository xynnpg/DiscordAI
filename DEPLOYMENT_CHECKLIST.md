# ✅ Railway Deployment Checklist

## 🔧 Environment Variables Setup

### Required Variables
Set these environment variables in your Railway dashboard:

| Variable | Description | Example |
|----------|-------------|---------|
| `DISCORD_BOT_TOKEN` | Your Discord bot token from Discord Developer Portal | `MTM5ODY2ODEzMzM4MzkyOTg4Ng.GIbhD8.3cGw4I6ps4SecKK8tckVvOf3h7wgAI4y48WW5Q` |
| `GUILD_ID` | Your Discord server (guild) ID | `1398670692077142037` |
| `FLASK_SECRET_KEY` | A random secret key for Flask sessions | `your-super-secret-key-here` |
| `UI_PASSWORD` | Password for accessing the web interface (optional, for security) | `your-secure-password` |

### Optional Variables
| Variable | Description | Status |
|----------|-------------|--------|
| `DATABASE_URL` | Database connection string | Auto-provided by Railway |
| `PORT` | Port for the web server | Auto-set by Railway |

## 🚀 Deployment Steps

### 🚀 One-Click Deploy (Recommended)

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/cozy-comfort)

Click the button above for instant deployment!

**Template Details:**
- **Category**: AI/ML
- **Variables**: 3 required (GUILD_ID, UI_PASSWORD, DISCORD_BOT_TOKEN)
- **Database**: PostgreSQL (optional but recommended)
- **Stack**: Full-stack Discord bot + web interface

### Manual Deployment

### 1. Prepare Your Repository
- ✅ Push your code to GitHub
- ✅ Ensure all required files are present:
  - `Procfile`
  - `requirements.txt`
  - `runtime.txt`
  - `railway.json`
  - `.gitignore`

### 2. Connect to Railway
- ✅ Go to [railway.app](https://railway.app)
- ✅ Click "New Project"
- ✅ Select "Deploy from GitHub repo"
- ✅ Choose your repository
- ✅ Wait for initial deployment (2-3 minutes)

### 3. Configure Environment Variables
- ✅ Go to your project's "Variables" tab
- ✅ Add all required environment variables
- ✅ Double-check values for accuracy
- ✅ Save changes

### 4. Add Database (Optional)
- ✅ Go to "New" → "Database" → "PostgreSQL"
- ✅ Wait for database provisioning (1-2 minutes)
- ✅ Verify `DATABASE_URL` appears in variables

### 5. Test Deployment
- ✅ Check health endpoint: `your-railway-url/health`
- ✅ Test web interface: `your-railway-url/`
- ✅ Test Discord bot: `/ping` command

## 🔍 Troubleshooting Guide

### Health Check Fails
**Symptoms**: Health endpoint returns error or doesn't respond

**Solutions**:
1. ✅ Check that all environment variables are set
2. ✅ Verify your Discord bot token is valid
3. ✅ Check Railway logs for error messages
4. ✅ Ensure your bot has proper permissions in Discord

### Discord Bot Doesn't Connect
**Symptoms**: Bot appears offline or doesn't respond to commands

**Solutions**:
1. ✅ Verify the bot token is correct
2. ✅ Check that the bot is invited to your server
3. ✅ Ensure the bot has proper permissions
4. ✅ Review Railway logs for connection errors

### Web Interface Doesn't Work
**Symptoms**: Website doesn't load or shows errors

**Solutions**:
1. ✅ Check that Flask is starting properly
2. ✅ Verify the `/health` endpoint is accessible
3. ✅ Check Railway logs for Flask errors
4. ✅ Ensure all environment variables are set

### Database Issues
**Symptoms**: Database connection errors or missing data

**Solutions**:
1. ✅ Wait for PostgreSQL to fully provision
2. ✅ Verify `DATABASE_URL` is properly set
3. ✅ Check for database connection errors in logs
4. ✅ Restart deployment if database is stuck

## 🧪 Testing Checklist

### Web Interface Testing
- ✅ **Homepage Loads**: Visit your Railway URL
- ✅ **Add Model**: Can add new AI models
- ✅ **Edit Model**: Can modify existing models
- ✅ **Toggle Models**: Can enable/disable models
- ✅ **Delete Models**: Can remove unused models

### Discord Bot Testing
- ✅ **Basic Response**: `/ping` command works
- ✅ **Model Selection**: `/change` command with autocomplete
- ✅ **Model List**: `/models` shows available models
- ✅ **AI Chat**: `/ask` command works with selected model

### Database Testing
- ✅ **Model Persistence**: Models saved through web interface
- ✅ **User Preferences**: User model selections are saved
- ✅ **Data Integrity**: No data corruption or loss

## 📊 Common Issues & Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Service unavailable** | Website returns 503 error | Check Flask app startup in logs |
| **Bot not responding** | Bot offline or silent | Verify Discord token and permissions |
| **Database errors** | Connection or data issues | Wait for PostgreSQL provisioning |
| **Environment missing** | App crashes on startup | Add required variables in Railway |
| **Model not found** | `/change` shows no options | Add models via web interface |
| **AI not responding** | `/ask` fails | Check OpenRouter API key and model status |

## 🔒 Security Checklist

### Environment Security
- ✅ No sensitive data in code repository
- ✅ Strong, unique secrets for `FLASK_SECRET_KEY`
- ✅ Discord bot token is secure
- ✅ API keys are properly managed

### Access Control
- ✅ Bot has minimum required permissions
- ✅ Web interface is properly secured
- ✅ Database access is restricted
- ✅ HTTPS is enabled (automatic on Railway)

## 📈 Performance Monitoring

### Resource Usage
- ✅ Monitor CPU usage in Railway dashboard
- ✅ Check memory consumption
- ✅ Track network bandwidth
- ✅ Set up alerts for resource limits

### Application Health
- ✅ Regular health check monitoring
- ✅ Log analysis for errors
- ✅ Response time monitoring
- ✅ Error rate tracking

## 🎯 Post-Deployment Verification

After successful deployment, verify:

### Core Functionality
- ✅ **Health Endpoint**: `/health` responds correctly
- ✅ **Web Interface**: Accessible and functional
- ✅ **Discord Bot**: Responds to commands
- ✅ **Model Management**: Can add/edit models
- ✅ **AI Chat**: `/ask` works with models

### Security & Performance
- ✅ **Environment Variables**: All required variables set
- ✅ **Database**: Connected and functional
- ✅ **HTTPS**: Enabled and working
- ✅ **Logs**: No critical errors

### User Experience
- ✅ **Bot Commands**: All slash commands work
- ✅ **Autocomplete**: Model selection works
- ✅ **Error Handling**: Graceful error messages
- ✅ **Response Times**: Acceptable performance

## 🆘 Getting Help

If you encounter issues:

1. **📋 Check this checklist** for common solutions
2. **📖 Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for detailed guides
3. **🔍 Check Railway logs** for specific error messages
4. **🧪 Test locally** to isolate issues
5. **📞 Seek support** if problems persist

---

**🎉 Ready to deploy! Follow this checklist step by step for a smooth deployment experience.** 