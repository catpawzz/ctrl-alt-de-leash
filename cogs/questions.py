if __name__ == "__main__":
    print("This is a cog file and cannot be run directly.")
    exit()

import logging
import discord
from discord.ext import commands
from discord import SlashCommandGroup
import datetime
import aiohttp

class QuestionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')

    question_group = SlashCommandGroup(
        name="question",
        description="Utility commands for random questions"
    )

    @question_group.command(
        name="question",
        description="Get a random question to know someone better"
    )
    async def question(self, ctx):
        try:
            async with ctx.typing():
                await self._fetch_question(ctx)
        except discord.Forbidden:
            await self._fetch_question(ctx)

    async def _fetch_question(self, ctx):
        question_url = "https://api.cat-space.net/api/text/questions"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(question_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("status") == "success":
                            question = data.get("question")

                            embed = discord.Embed(
                                title="Random Question",
                                description=question,
                                color=discord.Color(0xe898ff)
                            )
                            embed.set_footer(text="Ctrl + Alt + De-leash")
                            embed.timestamp = datetime.datetime.now()

                            await ctx.respond(embed=embed)
                        else:
                            await ctx.respond("Failed to fetch a question. Try again later!")
                    else:
                        await ctx.respond(f"Error: API returned status {response.status}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")
            self.logger.error(f"Question command error: {e}")

def setup(bot):
    bot.add_cog(QuestionCog(bot))
