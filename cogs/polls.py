if __name__ == "__main__":
    print("This is a cog file and cannot be run directly.")
    exit()

import logging
import discord
from discord.ext import commands
from discord import app_commands
import datetime

class PollsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')
        self.emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
    poll_group = app_commands.Group(name="poll", description="Commands for creating and managing polls")
    
    @poll_group.command(name="yesno", description="Create a quick yes/no poll")
    async def yesno(self, interaction: discord.Interaction, question: str):
        self.logger.info(f"{interaction.user} created a yes/no poll in {interaction.channel} on {interaction.guild}.")
        
        embed = discord.Embed(
            title="📊 Yes/No Poll",
            description=question,
            color=discord.Color(0xe898ff)
        )
        
        embed.add_field(name="Options", value="👍 Yes\n👎 No", inline=False)
        embed.set_footer(text=f"Poll by {interaction.user.display_name}")
        embed.timestamp = datetime.datetime.now()
        
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        
        await message.add_reaction("👍")
        await message.add_reaction("👎")
    
    @poll_group.command(name="multiple", description="Create a poll with up to 10 options")
    async def multiple(self, interaction: discord.Interaction, question: str, options: str):
        self.logger.info(f"{interaction.user} created a poll in {interaction.channel} on {interaction.guild}.")
        
        option_list = options.split(",")
        if len(option_list) < 2:
            await interaction.response.send_message("Please provide at least 2 options separated by commas.", ephemeral=True)
            return
            
        if len(option_list) > 10:
            await interaction.response.send_message("You can only have up to 10 options in a poll.", ephemeral=True)
            return
            
        embed = discord.Embed(
            title="📊 Poll",
            description=question,
            color=discord.Color(0xe898ff)
        )
        
        option_text = ""
        for i, option in enumerate(option_list):
            option_text += f"{self.emoji_numbers[i]} {option.strip()}\n"
            
        embed.add_field(name="Options", value=option_text, inline=False)
        embed.set_footer(text=f"Poll by {interaction.user.display_name}")
        embed.timestamp = datetime.datetime.now()
        
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        
        for i in range(len(option_list)):
            await message.add_reaction(self.emoji_numbers[i])

async def setup(bot):
    polls_cog = PollsCog(bot)
    await bot.add_cog(polls_cog)
    bot.register_app_command_group(polls_cog.poll_group)
