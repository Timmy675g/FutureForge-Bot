import discord

class StartUI(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Find My Career",
        emoji="🎯",
        style=discord.ButtonStyle.green
    )
    async def find_my_career(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            """
# Let's Find Your Ideal Career!!

I'm going to ask you a few questions to understand your interests and recommend careers that suit you.

### Tell me about yourself?

You can mention:
• Your hobbies
• Subjects you enjoy
• Skills you already have
• Things you like doing

### For Example :

> I enjoy coding and solving problems.

> I love drawing and designing.

> I like helping people.

**Type your answer in this channel to begin.**

*(AI analysis is coming soon. For now, this is a placeholder :].)*
""",
        )