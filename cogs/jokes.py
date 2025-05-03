if __name__ == "__main__":
    print("This is a cog file and cannot be run directly.")
    exit()

import logging
import discord
from discord.ext import commands
from discord import SlashCommandGroup
import random
import datetime
import asyncio
import aiohttp

class JokeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')
    
    joke_group = SlashCommandGroup(name="jokes", description="Utility commands for jokes")
    
    @joke_group.command(name="joke", description="Get a random joke")
    async def joke(self, ctx, category: discord.Option(str, "Joke category (bad, dad, programming, pun)", 
                                                    choices=["bad", "dad", "programming", "pun"], 
                                                    required=False)):
        try:
            # Try to use typing indicator
            async with ctx.typing():
                await self._fetch_joke(ctx, category)
        except discord.Forbidden:
            await self._fetch_joke(ctx, category)
    
    async def _fetch_joke(self, ctx, category=None):
        joke_url = f"https://api.cat-space.net/api/text/jokes"
        if category:
            joke_url += f"?category={category}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(joke_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("status") == "success":
                            joke = data.get("joke")
                            joke_category = data.get("category")
                            
                            embed = discord.Embed(
                                title=f"{joke_category.capitalize()} Joke",
                                description=joke,
                                color=discord.Color(0xe898ff)
                            )
                            embed.set_footer(text="Ctrl + Alt + De-leash")
                            embed.timestamp = datetime.datetime.now()
                            
                            await ctx.respond(embed=embed)
                        else:
                            await ctx.respond("Failed to fetch a joke. Try again later!")
                    else:
                        await ctx.respond(f"Error: API returned status {response.status}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")
            self.logger.error(f"Joke command error: {e}")

def setup(bot):
    bot.add_cog(JokeCog(bot))