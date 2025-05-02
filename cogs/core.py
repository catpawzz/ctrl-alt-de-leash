if __name__ == "__main__":
    print("This is a cog file and cannot be run directly.")
    exit()

import logging
import discord
from discord.ext import commands
from discord import app_commands
import datetime
import time

class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')
        self.start_time = time.time()
        
    core_group = app_commands.Group(name="core", description="Core bot commands")
    
    @core_group.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: {latency}ms",
            color=discord.Color(0xe898ff)
        )
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        await interaction.response.send_message(embed=embed)
    
    @core_group.command(name="uptime", description="Check how long the bot has been running")
    async def uptime(self, interaction: discord.Interaction):
        current_time = time.time()
        difference = int(round(current_time - self.bot.start_time))
        uptime_str = str(datetime.timedelta(seconds=difference))
        
        embed = discord.Embed(
            title="⏱️ Bot Uptime",
            description=f"I've been online for: **{uptime_str}**",
            color=discord.Color(0xe898ff)
        )
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    core_cog = CoreCog(bot)
    await bot.add_cog(core_cog)
    
    
    success = bot.register_app_command_group(core_cog.core_group)
    if not success:
        bot.logger.warning("Core commands were not registered due to a duplicate")