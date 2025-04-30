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

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def ping(self, ctx):
        """
        Command to check if the bot is online and display latency metrics.
        """
        # Log the command usage
        self.logger.info(f"{ctx.author} used /ping command in {ctx.channel} on {ctx.guild}.")

        # Discord WebSocket latency
        discord_latency = self.bot.latency * 1000  # Convert latency to ms

        # Record the time before sending the response to measure REST API latency
        start_time = time.perf_counter()
        initial_response = await ctx.respond("Talking to Discord :typing:", ephemeral=True)  # Initial response
        rest_latency = (time.perf_counter() - start_time) * 1000  # Convert to ms

        # Measure message edit latency
        edit_start_time = time.perf_counter()
        response_message = await initial_response.original_response()  # Retrieve the original response message
        await response_message.edit(content="Updating ping details...")
        edit_latency = (time.perf_counter() - edit_start_time) * 1000  # Convert to ms

        # Update the message with the final metrics
        await response_message.edit(content=(
            f":pencil: Edit message: `{edit_latency:.0f}ms`\n"
            f":discord: Discord: `{discord_latency:.0f}ms`\n"
            f":download: RestAction: `{rest_latency:.0f}ms`"
        ))

    @commands.slash_command(integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install}, name="uptime", description="Returns the bot's uptime")
    async def uptime(self, ctx: discord.ApplicationContext):
        """
        A slash command to return the bot's uptime.
        """
        current_time = time.time()
        uptime_seconds = int(current_time - self.bot.start_time)
        uptime_string = str(datetime.timedelta(seconds=uptime_seconds))
        await ctx.respond(f"Uptime: {uptime_string}", ephemeral=True)
        
def setup(bot):
    bot.add_cog(GenericCog(bot))