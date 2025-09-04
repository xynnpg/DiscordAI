import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import threading
import time
import os
from datetime import datetime
from config import Config
from database import db, UserPreference, AIModel, ConversationHistory
from openrouter_client import OpenRouterClient
from flask import Flask
from flask_web import create_app
from team_config import is_team_member

# Global Flask app instance
flask_app = None

def get_flask_app():
    """Get the Flask app instance, creating it if necessary"""
    global flask_app
    if flask_app is None:
        print("🔄 Creating Flask app on demand...")
        flask_app = create_app()
        with flask_app.app_context():
            db.create_all()
    return flask_app

class DiscordBot:
    def __init__(self):
        self.bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
        self.setup_commands()

    def setup_commands(self):
        @self.bot.tree.command(name="ping", description="Check if the bot is working")
        async def ping(interaction: discord.Interaction):
            flask_status = "✅ Ready" if flask_app is not None else "❌ Not Ready"
            flask_id = id(flask_app) if flask_app is not None else "None"
            await interaction.response.send_message(f"Pong! 🏓 Bot is working!\nFlask Status: {flask_status}\nFlask ID: {flask_id}")

        @self.bot.tree.command(name="test_models", description="Test command to check available models")
        async def test_models(interaction: discord.Interaction):
            try:
                app = get_flask_app()
                with app.app_context():
                    available_models = AIModel.query.filter_by(is_active=True).all()
                    model_names = [m.name for m in available_models]
                    await interaction.response.send_message(f"Available models: {model_names}", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"Error: {e}", ephemeral=True)

        @self.bot.tree.command(name="debug_db", description="Debug database connection and models")
        async def debug_db(interaction: discord.Interaction):
            try:
                app = get_flask_app()
                with app.app_context():
                    # Check if we can connect to the database
                    total_models = AIModel.query.count()
                    active_models = AIModel.query.filter_by(is_active=True).count()

                    # Get all models for debugging
                    all_models = AIModel.query.all()
                    model_details = []
                    for model in all_models:
                        model_details.append(f"• {model.name} (Active: {model.is_active})")

                    debug_info = f"**Database Debug Info:**\n"
                    debug_info += f"Total models: {total_models}\n"
                    debug_info += f"Active models: {active_models}\n"
                    debug_info += f"All models:\n" + "\n".join(model_details)

                    await interaction.response.send_message(debug_info, ephemeral=True)

            except Exception as e:
                await interaction.response.send_message(f"❌ Database error: {e}", ephemeral=True)

        @self.bot.tree.command(name="models", description="Show available AI models and your current selection")
        async def models(interaction: discord.Interaction):
            try:
                app = get_flask_app()
                with app.app_context():
                    # Get available models
                    available_models = AIModel.query.filter_by(is_active=True).all()

                    if not available_models:
                        await interaction.response.send_message("❌ No active models available. Please add models through the web interface.")
                        return

                    # Get user's current model
                    user_pref = UserPreference.query.filter_by(user_id=str(interaction.user.id)).first()
                    current_model = user_pref.model_name if user_pref else "None"

                    # Create response message
                    model_list = "\n".join([f"• {model.name}{' (Team Only)' if model.team_only else ''}" for model in available_models])

                    embed = discord.Embed(
                        title="🤖 Available AI Models",
                        description=f"**Your current model:** {current_model}\n\n**Available models:**\n{model_list}",
                        color=0x00ff00
                    )
                    embed.set_footer(text="Use /change to select a different model")

                    await interaction.response.send_message(embed=embed, ephemeral=True)

            except Exception as e:
                print(f"Error in models command: {e}")
                await interaction.response.send_message("❌ An error occurred while loading models.")

        @self.bot.tree.command(name="ask", description="Ask the AI a question")
        @app_commands.describe(content="Your question or message for the AI")
        async def ask(interaction: discord.Interaction, content: str):
            await interaction.response.defer()

            try:
                app = get_flask_app()
                with app.app_context():
                    # Get user's preferred model
                    user_pref = UserPreference.query.filter_by(user_id=str(interaction.user.id)).first()

                    if not user_pref:
                        await interaction.followup.send("❌ You haven't set a model yet! Use `/change` to set your preferred model.")
                        return

                    # Get the AI model configuration
                    ai_model = AIModel.query.filter_by(name=user_pref.model_name, is_active=True).first()

                    if not ai_model:
                        await interaction.followup.send("❌ Your selected model is not available. Please use `/change` to select a different model.")
                        return

                    # Check if model is team-only and user is not in team
                    if ai_model.team_only:
                        user_username = interaction.user.name

                        if not is_team_member(user_username):
                            await interaction.followup.send("❌ This model is restricted to team members only. Please contact the team owner for access.")
                            return

                    # Get conversation history for context
                    user_id = str(interaction.user.id)
                    conversation_history = ConversationHistory.get_conversation_context(user_id, limit=10)

                    # Store user's message
                    ConversationHistory.add_message(user_id, "user", content, user_pref.model_name)

                    # Create OpenRouter client and generate response with context
                    client = OpenRouterClient(ai_model.api_key)
                    response = client.generate_response(ai_model.official_name, content, conversation_history=conversation_history)

                    if response:
                        # Store AI's response
                        ConversationHistory.add_message(user_id, "assistant", response, user_pref.model_name)

                        # Split long responses
                        if len(response) > 2000:
                            chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
                            for i, chunk in enumerate(chunks):
                                if i == 0:
                                    await interaction.followup.send(f"🤖 **AI Response:**\n{chunk}")
                                else:
                                    await interaction.followup.send(chunk)
                        else:
                            await interaction.followup.send(f"🤖 **AI Response:**\n{response}")
                    else:
                        await interaction.followup.send("❌ Sorry, I couldn't generate a response. Please try again.")

            except Exception as e:
                print(f"Error in ask command: {e}")
                await interaction.followup.send("❌ An error occurred while processing your request.")

        @self.bot.tree.command(name="change", description="Change your preferred AI model")
        @app_commands.describe(model="The AI model you want to use")
        async def change(interaction: discord.Interaction, model: str):
            try:
                app = get_flask_app()
                with app.app_context():
                    # Check if the model exists and is active
                    ai_model = AIModel.query.filter_by(name=model, is_active=True).first()

                    if not ai_model:
                        # Get available models
                        available_models = AIModel.query.filter_by(is_active=True).all()
                        model_names = [m.name for m in available_models]

                        await interaction.response.send_message(
                            f"❌ Model '{model}' not found or not active.\n\n"
                            f"Available models: {', '.join(model_names) if model_names else 'None'}"
                        )
                        return

                    # Update or create user preference
                    user_pref = UserPreference.query.filter_by(user_id=str(interaction.user.id)).first()

                    if user_pref:
                        user_pref.model_name = model
                        user_pref.updated_at = datetime.utcnow()
                    else:
                        user_pref = UserPreference(user_id=str(interaction.user.id), model_name=model)
                        db.session.add(user_pref)

                    db.session.commit()

                    # Check if model is team-only
                    team_status = " (Team Only)" if ai_model.team_only else ""
                    await interaction.response.send_message(f"✅ Your preferred model has been changed to: **{model}**{team_status}")

            except Exception as e:
                print(f"Error in change command: {e}")
                await interaction.response.send_message("❌ An error occurred while changing your model.")

        # Define autocomplete function outside the command
        async def change_autocomplete(interaction: discord.Interaction, current: str):
            try:
                app = get_flask_app()
                with app.app_context():
                    # Get available models
                    available_models = AIModel.query.filter_by(is_active=True).all()
                    print(f"Available models: {[m.name for m in available_models]}")
                    print(f"Current input: '{current}'")

                    # Filter models that match the current input
                    matching_models = [
                        model.name for model in available_models
                        if current.lower() in model.name.lower()
                    ]
                    print(f"Matching models: {matching_models}")

                    # Return up to 25 choices (Discord limit)
                    choices = [
                        discord.app_commands.Choice(name=model_name, value=model_name)
                        for model_name in matching_models[:25]
                    ]
                    print(f"Returning choices: {[c.name for c in choices]}")

                    return choices

            except Exception as e:
                print(f"Error in change autocomplete: {e}")
                # Return empty list if there's an error
                return []

        # Add autocomplete to the change command
        change.autocomplete('model')(change_autocomplete)

        @self.bot.tree.command(name="clear_memory", description="Clear your conversation history")
        async def clear_memory(interaction: discord.Interaction):
            try:
                app = get_flask_app()
                with app.app_context():
                    user_id = str(interaction.user.id)

                    # Check if user has any conversation history
                    history_count = ConversationHistory.query.filter_by(user_id=user_id).count()

                    if history_count == 0:
                        await interaction.response.send_message("🤖 You don't have any conversation history to clear.", ephemeral=True)
                        return

                    # Clear user's conversation history
                    ConversationHistory.clear_user_history(user_id)

                    await interaction.response.send_message(f"✅ Cleared {history_count} messages from your conversation history. The AI will no longer remember our previous conversations.", ephemeral=True)

            except Exception as e:
                print(f"Error in clear_memory command: {e}")
                await interaction.response.send_message("❌ An error occurred while clearing your memory.", ephemeral=True)

        @self.bot.tree.command(name="memory_info", description="View information about your conversation memory")
        async def memory_info(interaction: discord.Interaction):
            try:
                app = get_flask_app()
                with app.app_context():
                    user_id = str(interaction.user.id)

                    # Get conversation statistics
                    total_messages = ConversationHistory.query.filter_by(user_id=user_id).count()
                    user_messages = ConversationHistory.query.filter_by(user_id=user_id, role="user").count()
                    ai_messages = ConversationHistory.query.filter_by(user_id=user_id, role="assistant").count()

                    if total_messages == 0:
                        await interaction.response.send_message("🤖 You don't have any conversation history yet. Start chatting with `/ask`!", ephemeral=True)
                        return

                    # Get the most recent conversation
                    recent_messages = ConversationHistory.get_user_history(user_id, limit=5)

                    embed = discord.Embed(
                        title="🧠 Your Conversation Memory",
                        color=0x00ff00
                    )

                    embed.add_field(
                        name="📊 Statistics",
                        value=f"• Total messages: {total_messages}\n• Your messages: {user_messages}\n• AI responses: {ai_messages}",
                        inline=False
                    )

                    if recent_messages:
                        recent_preview = []
                        for msg in reversed(recent_messages[-3:]):  # Show last 3 messages
                            role_emoji = "👤" if msg.role == "user" else "🤖"
                            content_preview = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                            recent_preview.append(f"{role_emoji} {content_preview}")

                        embed.add_field(
                            name="💬 Recent Messages",
                            value="\n".join(recent_preview),
                            inline=False
                        )

                    embed.set_footer(text="Use /clear_memory to reset your conversation history")

                    await interaction.response.send_message(embed=embed, ephemeral=True)

            except Exception as e:
                print(f"Error in memory_info command: {e}")
                await interaction.response.send_message("❌ An error occurred while retrieving memory information.", ephemeral=True)

        @self.bot.event
        async def on_ready():
            print(f'{self.bot.user} has connected to Discord!')
            try:
                synced = await self.bot.tree.sync()
                print(f"Synced {len(synced)} command(s)")
            except Exception as e:
                print(f"Failed to sync commands: {e}")

            # Test database connection on startup
            try:
                app = get_flask_app()
                with app.app_context():
                    # Ensure database tables exist
                    db.create_all()

                    # Check if we have any models
                    model_count = AIModel.query.count()
                    print(f"📊 Database has {model_count} models")

                    if model_count == 0:
                        print("⚠️  No models found in database. Add models through the web interface.")
                    else:
                        active_models = AIModel.query.filter_by(is_active=True).all()
                        print(f"✅ {len(active_models)} active models available")

            except Exception as e:
                print(f"❌ Database error on startup: {e}")

    def run(self):
        self.bot.run(Config.DISCORD_BOT_TOKEN)

def main():
    """Main function for Discord bot when run standalone or in thread"""
    print("🤖 Starting Discord AI Bot...")

    try:
        # Create Flask app for database access
        flask_app = create_app()
        print("✅ Flask app created for Discord bot")

        # Initialize database
        with flask_app.app_context():
            db.create_all()
            print("✅ Database initialized")

        # Start Discord bot
        bot = DiscordBot()
        print("✅ Discord bot initialized")
        bot.run()

    except Exception as e:
        print(f"❌ Discord bot error: {e}")
        raise

if __name__ == "__main__":
    main()
