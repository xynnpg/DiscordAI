import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    GUILD_ID = int(os.getenv('GUILD_ID', 0))
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
    
    # Use PostgreSQL in production, SQLite in development
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_database.db')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1) 