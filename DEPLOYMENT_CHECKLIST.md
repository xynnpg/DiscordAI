# Railway Deployment Checklist

## Environment Variables Required

Make sure to set these environment variables in your Railway dashboard:

### Required Variables:
- `DISCORD_BOT_TOKEN` - Your Discord bot token from Discord Developer Portal
- `GUILD_ID` - Your Discord server (guild) ID
- `FLASK_SECRET_KEY` - A random secret key for Flask sessions (can be any random string)

### Optional Variables:
- `DATABASE_URL` - Railway will automatically provide this for PostgreSQL
- `PORT` - Railway will automatically set this

## Steps to Deploy:

1. **Push your code to GitHub** (if not already done)
2. **Connect Railway to your GitHub repository**
3. **Set environment variables** in Railway dashboard:
   - Go to your project in Railway
   - Click on "Variables" tab
   - Add the required variables listed above
4. **Deploy** - Railway will automatically deploy when you push changes

## Troubleshooting:

### If healthcheck fails:
1. Check that all environment variables are set
2. Verify your Discord bot token is valid
3. Check Railway logs for error messages
4. Make sure your bot has proper permissions in Discord

### If Discord bot doesn't connect:
1. Verify the bot token is correct
2. Check that the bot is invited to your server
3. Ensure the bot has proper permissions

### If web interface doesn't work:
1. Check that Flask is starting properly
2. Verify the `/health` endpoint is accessible
3. Check Railway logs for Flask errors

## Testing:

1. **Web Interface**: Visit your Railway URL to access the model management interface
2. **Discord Bot**: Use `/ping` command in your Discord server to test the bot
3. **Health Check**: Visit `your-railway-url/health` to verify the service is running

## Common Issues:

- **"Service unavailable"**: Usually means Flask app isn't starting properly
- **"Bot not responding"**: Check Discord bot token and permissions
- **"Database errors"**: Railway should automatically provide DATABASE_URL 