if __name__ == "__main__":
    print("This is a cog file and cannot be run directly.")
    exit()

import logging
import discord
from discord.ext import commands
from discord import app_commands
import random
import datetime
import asyncio

class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')
        
    game_group = app_commands.Group(name="game", description="Fun games to play with friends")
    
    @game_group.command(name="roll", description="Roll one or more dice with the specified number of sides")
    async def roll(self, interaction: discord.Interaction, dice: int = 1, sides: int = 6):
        if dice < 1 or dice > 10:
            await interaction.response.send_message("Please roll between 1 and 10 dice.", ephemeral=True)
            return
            
        if sides < 2 or sides > 100:
            await interaction.response.send_message("Dice must have between 2 and 100 sides.", ephemeral=True)
            return
            
        results = [random.randint(1, sides) for _ in range(dice)]
        total = sum(results)
        
        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"Rolling {dice}d{sides}",
            color=discord.Color(0xe898ff)
        )
        
        if dice > 1:
            embed.add_field(name="Results", value=f"{results}", inline=False)
            embed.add_field(name="Total", value=f"**{total}**", inline=False)
        else:
            embed.add_field(name="Result", value=f"**{total}**", inline=False)
            
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await interaction.response.send_message(embed=embed)
    
    @game_group.command(name="rps", description="Play rock-paper-scissors against the bot")
    @app_commands.choices(choice=[
        app_commands.Choice(name="Rock", value="rock"),
        app_commands.Choice(name="Paper", value="paper"),
        app_commands.Choice(name="Scissors", value="scissors"),
    ])
    async def rps(self, interaction: discord.Interaction, choice: str):
        bot_choice = random.choice(["rock", "paper", "scissors"])
        
        embed = discord.Embed(
            title="Rock, Paper, Scissors",
            color=discord.Color(0xe898ff)
        )
        
        embed.add_field(name="Your choice", value=choice.capitalize(), inline=True)
        embed.add_field(name="My choice", value=bot_choice.capitalize(), inline=True)
        
        if choice == bot_choice:
            result = "It's a tie!"
        elif (choice == "rock" and bot_choice == "scissors") or \
             (choice == "scissors" and bot_choice == "paper") or \
             (choice == "paper" and bot_choice == "rock"):
            result = "You win!"
        else:
            result = "I win!"
            
        embed.add_field(name="Result", value=result, inline=False)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await interaction.response.send_message(embed=embed)
    
    @game_group.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        
        embed = discord.Embed(
            title="Coin Flip",
            description=f"The coin landed on: **{result}**",
            color=discord.Color(0xe898ff)
        )
        
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    games_cog = GamesCog(bot)
    await bot.add_cog(games_cog)
    bot.register_app_command_group(games_cog.game_group)
