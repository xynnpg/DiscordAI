# 🔧 Troubleshooting Guide

## 🚨 Issue: Discord Bot Can't Access Models from Web Interface

### 🎯 Symptoms
- ✅ Web interface shows models (like "Uncensored" and "Darius")
- ❌ Discord `/change` command shows "No options match your search"
- ❌ `/models` command shows "No active models available"

### 🔍 Root Cause
The Discord bot and web interface are not properly sharing the same database or there's a timing issue with database initialization.

## 🛠️ Solutions

### 1. **Check Database Connection**
Run the debug command in Discord:
```discord
/debug_db
```

This will show:
- 📊 Total models in database
- ✅ Active models count
- 📋 Details of all models

### 2. **Test Models Command**
Run this command to see what models are available:
```discord
/test_models
```

### 3. **Check Railway Logs**
Look for these error messages in Railway logs:
- 🔌 Database connection errors
- 🌐 Flask app startup issues
- 🤖 Discord bot connection problems

### 4. **Verify Environment Variables**
Make sure these are set in Railway:
- ✅ `DISCORD_BOT_TOKEN`
- ✅ `GUILD_ID`
- ✅ `FLASK_SECRET_KEY`
- ✅ `DATABASE_URL` (should be auto-provided by Railway)

### 5. **Database Migration Issues**
If the database is empty or corrupted:

1. **🌐 Access the web interface** at your Railway URL
2. **➕ Add your models again** through the web interface
3. **✅ Make sure models are set to "Active"**
4. **🧪 Test with `/debug_db` command**

## 🔧 Common Fixes

### If Models Exist But Bot Can't See Them
1. 🔄 Restart the Railway deployment
2. ⏰ Wait 2-3 minutes for full startup
3. 🧪 Try `/debug_db` to verify database connection

### If Database Is Empty
1. 🌐 Go to your Railway URL
2. ➕ Add your AI models through the web interface
3. ✅ Make sure to set them as "Active"
4. 🧪 Test with `/models` command

### If Autocomplete Doesn't Work
1. ⌨️ Try typing the exact model name
2. 📋 Use `/models` to see available options
3. 🔍 Check Railway logs for errors

## 🧪 Debugging Steps

### Step 1: Check Bot Status
```discord
/ping
```
**Expected**: "Pong! 🏓"

### Step 2: Check Database Connection
```discord
/debug_db
```
**Expected**: Shows model count and details

### Step 3: Check Available Models
```discord
/models
```
**Expected**: Lists available models

### Step 4: Test Model Switching
```discord
/change [exact-model-name]
```
**Expected**: Confirms model change

## ✅ Expected Behavior

**After fixing, you should see:**
- ✅ `/debug_db` shows your models with "Active: True"
- ✅ `/models` shows your available models
- ✅ `/change` autocomplete shows your model names
- ✅ `/ask` works with your selected model

## 🔄 If Still Not Working

### 1. **Check Railway Logs**
Look for specific error messages:
- 🔌 Database connection failures
- 🌐 Flask startup errors
- 🤖 Discord bot connection issues

### 2. **Verify OpenRouter API Key**
- ✅ Check if your API key is valid
- ✅ Ensure the key has proper permissions
- ✅ Test the key with a simple API call

### 3. **Ensure Models Are Active**
- ✅ Go to web interface
- ✅ Check that models are marked as "Active"
- ✅ Verify model names match exactly

### 4. **Restart Railway Deployment**
- 🔄 Restart the entire deployment
- ⏰ Wait 3-5 minutes for full startup
- 🧪 Test all commands again

## 🧪 Quick Test

1. 🌐 Go to your Railway URL
2. ➕ Add a test model with your OpenRouter API key
3. ✅ Make sure it's set to "Active"
4. 🤖 In Discord, run `/debug_db`
5. ✅ You should see your test model listed

**If `/debug_db` shows 0 models**, the issue is with database initialization or the web interface isn't properly saving models.

## 📊 Common Error Messages

| Error Message | Possible Cause | Solution |
|---------------|----------------|----------|
| "No options match your search" | Models not in database | Add models via web interface |
| "No active models available" | All models disabled | Enable models in web interface |
| "Database connection failed" | Database not ready | Wait for PostgreSQL provisioning |
| "Bot not responding" | Discord token issue | Check bot token and permissions |
| "Web interface not loading" | Flask startup error | Check Railway logs for errors |

## 🔍 Advanced Debugging

### Database Inspection
If you have database access:
```sql
SELECT * FROM models WHERE active = 1;
```

### Log Analysis
Check Railway logs for:
- 🔌 Connection strings
- 🌐 Flask startup messages
- 🤖 Discord bot events
- 📊 Database queries

### Network Testing
Test connectivity:
- 🌐 Web interface accessibility
- 🔌 Database connection
- 🤖 Discord API connection

## 🆘 Getting Additional Help

If the issue persists:

1. **📋 Check [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** for setup issues
2. **📖 Review [DEPLOYMENT.md](DEPLOYMENT.md)** for configuration problems
3. **🔍 Examine Railway logs** for specific error messages
4. **🧪 Test locally** to isolate the issue
5. **📞 Seek community support** with specific error details

## 🎯 Prevention Tips

### Best Practices
- ✅ Always test locally before deploying
- ✅ Use strong, unique environment variables
- ✅ Monitor Railway logs regularly
- ✅ Keep models organized in web interface
- ✅ Regular database backups (if possible)

### Monitoring
- 📊 Check health endpoint regularly
- 🔍 Monitor Discord bot status
- 📋 Track model usage and performance
- ⚠️ Set up alerts for critical errors

---

**🔧 This troubleshooting guide should resolve most common issues. If problems persist, check the logs for specific error messages.** 