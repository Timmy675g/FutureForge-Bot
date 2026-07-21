import discord

from ai import AI
from logic import CareerLogic
from profile import UserProfile


logic = CareerLogic()


class StartUI(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def ask_question(self, interaction: discord.Interaction, question: str):
        await interaction.followup.send(question, ephemeral=True)

        def check(message):
            return (
                message.author == interaction.user
                and message.channel == interaction.channel
            )

        reply = await interaction.client.wait_for(
            "message",
            check=check,
            timeout=300
        )

        return reply.content, reply

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

        profile = UserProfile()

        await interaction.response.send_message(
            """
# 👋 Welcome to FutureForge!

I'm your AI powered career advisor.

Before recommending careers, I'd like to know a little about you.

It'll only take around **2 - 3 minutes**.

Let's begin!
""",
            ephemeral=True
        )

        try:
            # Question 1
            profile.name, _ = await self.ask_question(
                interaction,
                "Hi! **What should I call you?**"
            )

            # Question 2
            profile.subjects, _ = await self.ask_question(
                interaction,
                f"Nice to meet you, **{profile.name}**! 😊\n\n"
                "📚 **Which school subjects do you enjoy the most?**\n\n"
                "Example:\n"
                "> Computer Science, Math, English"
            )

            # Question 3
            profile.hobbies, reply = await self.ask_question(
                interaction,
                "🎮 **What kind of hobbies do you enjoy outside school?**\n\n"
                "Example:\n"
                "> Coding, Gaming, Reading"
            )

            # AI will try to Analyse the profile and extract the keywords from the user.

            keywords = AI.analyze_profile(profile)

            print("AI Keywords:", keywords)

            careers = logic.search_database(keywords)
            careers = logic.rank_results(careers)
            recommendations = logic.create_recommendation(careers)

            if not recommendations:
                await reply.reply(
                    "❌ Sorry, I couldn't find any matching careers."
                )
                return

            embed = discord.Embed( # It seemed nice to have embed for the final career recommendation
                title="🎯 Your Career Recommendations",
                description=(
                    f"Based on what you've shared, **{profile.name}**, "
                    "here are the careers that best match your profile!"
                ),
                color=discord.Color.green()
            )

            embed.add_field(
                name="AI Keywords",
                value=", ".join(keywords),
                inline=False
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
                "⌛ You didn't reply within 5 minutes.\n\n"
                "Click **Find My Career** again whenever you're ready.",
                ephemeral=True
            )