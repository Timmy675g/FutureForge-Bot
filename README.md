# FutureForge

FutureForge is an AI powered Discord career advisor. Powered by CloudFlare AI Worker, it helps users discover careers based on their interests, skills, and goals in details.

## Reminder :
FutureForge is AI model agnostic, which mean that you are free to choose the AI model that best fits your deployment, performance, and cost requirements so the AI in FutureForge is not responsible for choosing careers. Instead, it performs two important tasks below:

1. Understand user message.
2. Generate a natural explanation for the recommended careers.

## Features

- AI powered career recommendations
- Career database
- Career comparison
- Career roadmaps
- Cloudflare AI integration

## Tech Stack

- Python
- discord.py
- SQLite
- Cloudflare AI Workers
- Git

## Available Commands

`!start` Displays the welcome message and starts FutureForge. ✅ 
`!help` Displays the help menu. ✅ 

## Planned Commands
`!recommend`Get career recommendations based on your interests. 
`!browse` Browse all available careers in the database. 
`!career <name>` View detailed information about a career. 
`!compare` Compare two careers side by side. 
`!roadmap` View the learning roadmap for a career. 
`!about` Learn more about FutureForge. 

## Architecture

User
    ↓
Discord Bot
    ↓
Cloudflare AI Worker ( To Read Available Data in DB )
    ↓
Logic
    ↓
SQLite Database
    ↓
Cloudflare AI Worker ( Gives Response with Custom Texts )
    ↓
Discord Response

## Project Structure

FutureForge/
├── bot.py
├── logic.py
├── database.py
├── ui.py
├── config.py
├── futureforge.db
└── assets/

## Status

- [x] Database initialized
- [x] Bot online
- [x] !start command
- [x] !help command
- [x] Find My Career button
- [ ] AI integration
- [ ] Recommendation engine
- [ ] Career comparison
- [ ] Admin panel

## How Do You Choose Your AI Model?

Here Is The List of AI Models You Can Use with it's Advantages :

- Qwen ( Recommended ) General purpose assistant Excellent reasoning, multilingual support, and great instruction following.

- OpenAI OSS Models	Balanced reasoning	Strong open weight models suitable for production deployments.

- Llama	Self hosted deployments	Many ecosystem with broad community support.

- Gemma	Lightweight deployments	Efficient especially for low resource environments.

Select a model based on your projects needs:

⚡ Fast responses -> Smaller models ( 3B–8B parameters )

🧠 Better reasoning -> Larger models ( 8B+ parameters )

🖥️ Self-hosting -> Llama, Qwen, Gemma, or other open source models

☁️ Cloud deployment -> Any provider compatible with your infrastructure

# Getting Started!

## Notice!

Before running FutureForge, make sure you have:

- Python 3.10 or newer
- A Discord Bot Token
- A Discord Server for testing
- Git (optional)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Timmy675g/FutureForge-Bot.git
cd FutureForge
```

### 2. Install dependencies

```bash
pip install -r requirements.txt 
```

### 3. Configure the bot

Open `config.py` and set:

```python
TOKEN = "YOUR_DISCORD_BOT_TOKEN"
DATABASE = "futureforge.db"
WORKER_URL = "YOUR_WORKER_URL_HERE"
```

### 4. Run the bot

```bash
python bot.py
```

If everything is configured correctly, you should see:

```text
Initializing database...
Bot is ready. Logged in as FutureForge
```

## License

MIT