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

class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')
        
    game_group = SlashCommandGroup(name="game", description="Fun games to play with friends")
    
    @game_group.command(name="roll", description="Roll one or more dice with the specified number of sides")
    async def roll(self, ctx, dice: int = 1, sides: int = 6):
        if dice < 1 or dice > 10:
            await ctx.respond("Please roll between 1 and 10 dice.", ephemeral=True)
            return
            
        if sides < 2 or sides > 100:
            await ctx.respond("Dice must have between 2 and 100 sides.", ephemeral=True)
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
        
        await ctx.respond(embed=embed)
    
    @game_group.command(name="rps", description="Play rock-paper-scissors against the bot")
    @discord.option(name="choice", description="Your choice", choices=["rock", "paper", "scissors"])
    async def rps(self, ctx, choice: str):
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
            
        embed.add_field(name="Result", value=result, inline=False, ephemeral=True)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await ctx.respond(embed=embed)
    
    @game_group.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, ctx):
        result = random.choice(["Heads", "Tails"])
        
        embed = discord.Embed(
            title="Coin Flip",
            description=f"The coin landed on: **{result}**",
            color=discord.Color(0xe898ff)
        )
        
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await ctx.respond(embed=embed)
    
    @game_group.command(name="wouldyourather", description="Get a random Would You Rather question")
    async def would_you_rather(self, ctx):
        api_url = "https://api.cat-space.net/api/text/wouldyourather"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        question = data["question"]
                        
                        embed = discord.Embed(
                            title="🤔 Would You Rather",
                            description=question,
                            color=discord.Color(0xe898ff)
                        )
                        
                        embed.set_footer(text="Ctrl + Alt + De-leash")
                        embed.timestamp = datetime.datetime.now()
                        
                        await ctx.respond(embed=embed)
                    else:
                        await ctx.respond(f"Failed to fetch Would You Rather question. API returned status code {response.status}.", ephemeral=True)
        except Exception as e:
            self.logger.error(f"Error fetching Would You Rather: {e}")
            await ctx.respond("An error occurred while trying to fetch a Would You Rather question.", ephemeral=True)
    
    @game_group.command(name="truthordare", description="Play Truth or Dare")
    @discord.option(name="choice", description="Truth or Dare", choices=["truth", "dare"])
    async def truth_or_dare(self, ctx, choice: str):
        api_url = f"https://api.cat-space.net/api/text/truthordare/{choice}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        question = data["question"]
                        title = "🔍 Truth" if choice == "truth" else "🔥 Dare"
                        
                        embed = discord.Embed(
                            title=title,
                            description=question,
                            color=discord.Color(0xe898ff)
                        )
                        
                        embed.set_footer(text="Ctrl + Alt + De-leash")
                        embed.timestamp = datetime.datetime.now()
                        
                        await ctx.respond(embed=embed)
                    else:
                        await ctx.respond(f"Failed to fetch {choice} question. API returned status code {response.status}.", ephemeral=True)
        except Exception as e:
            self.logger.error(f"Error fetching truth or dare: {e}")
            await ctx.respond(f"An error occurred while trying to fetch a {choice} question.", ephemeral=True)

def setup(bot):
    bot.add_cog(GamesCog(bot))