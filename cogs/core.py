if __name__ == "__main__":
    print("This is a cog file and cannot be run directly.")
    exit()

import logging
import discord
from discord.ext import commands
from discord.ui import Button, View
import datetime
import time

class GenericCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')

    utility = discord.commands.SlashCommandGroup(
        "utility", 
        "General utility commands"
    )
    
    @utility.command(
        name="ping",
        description="Check the bot's response time and latency"
    )
    async def ping(self, ctx):
        self.logger.info(f"{ctx.author} used /utility ping command in {ctx.channel} on {ctx.guild}.")
        
        discord_latency = self.bot.latency * 1000
        
        start_time = time.perf_counter()
        initial_response = await ctx.respond("Measuring latency...", ephemeral=True)
        rest_latency = (time.perf_counter() - start_time) * 1000
        
        edit_start_time = time.perf_counter()
        response_message = await initial_response.original_response()
        await response_message.edit(content="Updating ping details...")
        edit_latency = (time.perf_counter() - edit_start_time) * 1000
        
        embed = discord.Embed(
            title="Bot Latency",
            description=(
                f":pencil: Edit message: `{edit_latency:.0f}ms`\n"
                f":eyes: Discord: `{discord_latency:.0f}ms`\n"
                f":inbox_tray: RestAction: `{rest_latency:.0f}ms`"
            ),
            color=discord.Color(0xe898ff)
        )
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await response_message.edit(content=None, embed=embed)

    @utility.command(
        name="uptime",
        description="Returns the bot's uptime"
    )
    async def uptime(self, ctx: discord.ApplicationContext):
        current_time = time.time()
        uptime_seconds = int(current_time - self.bot.start_time)
        uptime_string = str(datetime.timedelta(seconds=uptime_seconds))
        
        embed = discord.Embed(
            title="Bot Uptime",
            description=f"I've been online for: `{uptime_string}`",
            color=discord.Color(0xe898ff)
        )
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await ctx.respond(embed=embed, ephemeral=True)
        
def setup(bot):
    bot.add_cog(GenericCog(bot))