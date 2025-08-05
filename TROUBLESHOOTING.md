# Troubleshooting Guide

## Issue: Discord Bot Can't Access Models from Web Interface

### Symptoms:
- Web interface shows models (like "Uncensored" and "Darius")
- Discord `/change` command shows "No options match your search"
- `/models` command shows "No active models available"

### Root Cause:
The Discord bot and web interface are not properly sharing the same database or there's a timing issue with database initialization.

### Solutions:

#### 1. **Check Database Connection**
Run the debug command in Discord:
```
/debug_db
```

This will show:
- Total models in database
- Active models count
- Details of all models

#### 2. **Test Models Command**
Run this command to see what models are available:
```
/test_models
```

#### 3. **Check Railway Logs**
Look for these error messages in Railway logs:
- Database connection errors
- Flask app startup issues
- Discord bot connection problems

#### 4. **Verify Environment Variables**
Make sure these are set in Railway:
- `DISCORD_BOT_TOKEN`
- `GUILD_ID`
- `FLASK_SECRET_KEY`
- `DATABASE_URL` (should be auto-provided by Railway)

#### 5. **Database Migration Issues**
If the database is empty or corrupted:

1. **Access the web interface** at your Railway URL
2. **Add your models again** through the web interface
3. **Make sure models are set to "Active"**
4. **Test with `/debug_db` command**

#### 6. **Common Fixes**

**If models exist but bot can't see them:**
1. Restart the Railway deployment
2. Wait 2-3 minutes for full startup
3. Try `/debug_db` to verify database connection

**If database is empty:**
1. Go to your Railway URL
2. Add your AI models through the web interface
3. Make sure to set them as "Active"
4. Test with `/models` command

**If autocomplete doesn't work:**
1. Try typing the exact model name
2. Use `/models` to see available options
3. Check Railway logs for errors

### Debugging Steps:

1. **First, check if the bot is running:**
   ```
   /ping
   ```

2. **Check database connection:**
   ```
   /debug_db
   ```

3. **Check available models:**
   ```
   /models
   ```

4. **Test model switching:**
   ```
   /change [exact-model-name]
   ```

### Expected Behavior:

**After fixing, you should see:**
- `/debug_db` shows your models with "Active: True"
- `/models` shows your available models
- `/change` autocomplete shows your model names
- `/ask` works with your selected model

### If Still Not Working:

1. **Check Railway logs** for specific error messages
2. **Verify your OpenRouter API key** is valid
3. **Ensure models are marked as "Active"** in web interface
4. **Try restarting the Railway deployment**

### Quick Test:

1. Go to your Railway URL
2. Add a test model with your OpenRouter API key
3. Make sure it's set to "Active"
4. In Discord, run `/debug_db`
5. You should see your test model listed

If `/debug_db` shows 0 models, the issue is with database initialization or the web interface isn't properly saving models. 