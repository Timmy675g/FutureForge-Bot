import discord
from discord.ext import commands
from ui import StartUI
from db import Database
from config import TOKEN, DATABASE

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

db = Database(DATABASE)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    
@bot.command(name="start")
async def start_command(ctx):
    await ctx.send(
        """
    **Hi! Welcome to FutureForge! 👋**

    I'm your AI-powered career advisor.

    Here's what I can help you with:

    🎯 Career Recommendations
    📚 Browse Careers
    ⚖️ Compare Careers
    🛣️ Career Roadmaps
    🤖 AI Career Chat (Powered by Cloudflare AI)

    Use `!help` to see all available commands.

    ━━━━━━━━━━━━━━━━━━

    **Click the button below to start your career journey!**
    """,
        view=StartUI()
    )
    
@bot.command(name="help")
async def help_command(ctx):
    await ctx.send("""
# FutureForge Help?

## User Commands :

`!start`
> Displays the welcome message.

`!help`
> Displays this help menu.

*(More commands will be available soon!)*

## Upcoming Features :

🎯 Career Recommendations
📚 Browse Careers
⚖️ Compare Careers
🛣️ Career Roadmaps
🤖 AI Career Chat ( Powered by CloudFlare AI )

FutureForge v0.1-Alpha
""")
    
bot.run(TOKEN)