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

`!browse`
> Browse all available careers.

`!career <career name>`
> View detailed information about a career.

`!roadmap <career>`
> View the learning roadmap for a career.

*(More commands will be available soon!)*

## Upcoming Features :

🎯 Career Recommendations
📚 Browse Careers
⚖️ Compare Careers
🛣️ Career Roadmaps
🤖 AI Career Chat ( Powered by CloudFlare AI )

FutureForge v0.1-Alpha
""")
    
@bot.command(name="browse")
async def browse_command(ctx):
    careers = db.get_all_careers()

    if not careers:
        await ctx.send("❌ No careers found in the database.")
        return

    embed = discord.Embed( # Embed is much more nicer than just texts actually
        title="FutureForge Career Database",
        description=f"Currently featuring **{len(careers)}** careers across multiple industries.", # Found this cool lines on Youtube, it basically shows how many careers are in the DB!
        color=discord.Color.blue()
    )

    categories = {}

    for category, title in careers:
        categories.setdefault(category, []).append(title)

    for category, titles in categories.items():
        embed.add_field(
            name=f"📂 {category}",
            value="\n".join(f"• {title}" for title in titles),
            inline=False
        )

    await ctx.send(embed=embed)
    
@bot.command(name="career")
async def career_command(ctx, *, career_name: str):
    career = db.get_career_by_name(career_name)

    if not career:
        await ctx.send(f"❌ Career **'{career_name}'** was not found.")
        return

    career_id = career[0]
    title = career[1]
    category = career[2]
    description = career[3]
    salary_min = career[4]
    salary_max = career[5]

    skills = db.get_skills(career_id)
    interests = db.get_interests(career_id)

    embed = discord.Embed(
        title=f"💼 {title}",
        description=description,
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📂 Category",
        value=category,
        inline=True
    )

    embed.add_field(
        name="💰 Salary",
        value=f"Rp {salary_min:,} - Rp {salary_max:,}",
        inline=True
    )

    embed.add_field(
        name="🛠 Skills",
        value="\n".join(f"• {skill}" for skill in skills) if skills else "No skills available.",
        inline=False
    )

    embed.add_field(
        name="🎯 Interests",
        value="\n".join(f"• {interest}" for interest in interests) if interests else "No interests available.",
        inline=False
    )

    embed.set_footer(text="FutureForge Career Database")

    await ctx.send(embed=embed)
    
@bot.command(name="roadmap")
async def roadmap_command(ctx, *, career_name: str):

    career = db.get_career_by_name(career_name)

    if not career:
        await ctx.send(f"❌ Career **'{career_name}'** was not found.")
        return

    career_id = career[0]
    title = career[1]

    roadmap = db.get_roadmap(career_id)

    if not roadmap:
        await ctx.send(f"⚠️ No roadmap is available for **{title}** yet.")
        return

    steps = "\n".join(
        f"🔹 **Step {step_number}:** {step}"
        for step_number, step in roadmap
    )

    embed = discord.Embed(
        title=f"{title} Roadmap",
        description="Follow these recommended learning steps:",
        color=discord.Color.green()
    )

    embed.add_field(
        name="Learning Path",
        value=steps,
        inline=False
    )

    embed.set_footer(
        text="FutureForge • Learning Roadmap"
    )

    await ctx.send(embed=embed)
    
@bot.command(name="about")
async def about_command(ctx):

    embed = discord.Embed(
        title="About FutureForge",
        description="**FutureForge** is an AI powered career advisor designed to help students explore careers, discover learning paths, and make informed decisions about their future.",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="✨ Features",
        value=(
            "🎯 AI Career Recommendations\n"
            "📚 Browse Career Database\n"
            "💼 Career Information\n"
            "🛣️ Learning Roadmaps\n"
            "🤖 AI Career Chat"
        ),
        inline=False
    )

    embed.add_field(
        name="🛠 Built With",
        value=(
            "• Python\n"
            "• Discord.py\n"
            "• SQLite\n"
            "• Cloudflare AI"
        ),
        inline=True
    )

    embed.add_field(
        name="🎓 Project",
        value=(
            "FutureForge\n"
            "Version: v1.0"
        ),
        inline=True
    )
    
    embed.add_field(
        name="FutureForge Development",
        value="Timmy675g",
        inline=True
    )

    embed.set_footer(
        text="FutureForge • Helping Students Build Their Future"
    )

    await ctx.send(embed=embed)
    
bot.run(TOKEN)