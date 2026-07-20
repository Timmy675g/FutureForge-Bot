import discord
from logic import CareerLogic

logic = CareerLogic()


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
""",
            ephemeral=True
        ) # Only the user who clicked Find My Career sees this message. So if it is in a server other people won't see it.

        def check(message):
            return (
                message.author == interaction.user
                and message.channel == interaction.channel
            )

        try:
            reply = await interaction.client.wait_for(
                "message",
                check=check,
                timeout=300
            )

            keywords = logic.analyze_user(reply.content)

            careers = logic.search_database(keywords)
            careers = logic.rank_results(careers)
            recommendations = logic.create_recommendation(careers)

            if not recommendations:
                await reply.reply(
                    "❌ Sorry, I couldn't find any matching careers. Try describing your interests in more detail."
                )
                return

            embed = discord.Embed(
                title="🎯 Your Career Recommendations",
                description="Here are the careers that best match your interests!",
                color=discord.Color.green()
            )

            for career in recommendations:
                embed.add_field(
                    name=career["title"],
                    value=(
                        f"**Category:** {career['category']}\n"
                        f"**Salary:** Rp{career['salary_min']:,} - Rp{career['salary_max']:,}\n"
                        f"**Score:** {career['score']}"
                    ),
                    inline=False
                )

            await reply.reply(embed=embed)

        except TimeoutError:
            await interaction.followup.send(
                "⌛ You didn't reply within 5 minutes. Click **Find My Career** again whenever you're ready.",
                ephemeral=True
            )