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

class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')
    
    misc_group = SlashCommandGroup(name="misc", description="Miscellaneous utility commands")
    
    @misc_group.command(name="choose", description="Choose between multiple options")
    async def choose(self, ctx, options: discord.Option(str, "Comma-separated options", required=True)):
        choices = [option.strip() for option in options.split(",") if option.strip()]
        
        if len(choices) < 2:
            await ctx.respond("Please provide at least two options separated by commas")
            return
        
        choice = random.choice(choices)
        
        embed = discord.Embed(
            title="Random Choice",
            description=f"🤔 I choose: **{choice}**",
            color=discord.Color(0xe898ff)
        )
        
        embed.add_field(name="All Options", value="\n".join([f"• {option}" for option in choices]), inline=False)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(MiscCog(bot))