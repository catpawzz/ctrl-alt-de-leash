if __name__ == "__main__":
    print("This is a cog file and cannot be run directly.")
    exit()

import logging
import discord
from discord.ext import commands
from discord import app_commands
import random
from datetime import datetime
import aiohttp

class AffectionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')
        self.api_base_url = "https://api.cat-space.net/api/sfw/gifs/"
        
    async def get_action_gif(self, action):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_base_url}{action}") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("status") == "success" and data.get("url"):
                        return data.get("url")
                return None

    
    affection_group = app_commands.Group(name="affection", description="Commands for expressing affection")
    
    @affection_group.command(name="hug", description="Send a virtual hug to someone special")
    async def hug(self, interaction: discord.Interaction, user: discord.Member):
        self.logger.info(f"{interaction.user} hugged {user} using /affection hug command in {interaction.channel} on {interaction.guild}.")
        
        gif_url = await self.get_action_gif("hug")
        
        embed = discord.Embed(
            title="Virtual Hug!",
            description=f"{interaction.user.mention} sent a hug to {user.mention}",
            color=discord.Color(0xe898ff) 
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await interaction.response.send_message(embed=embed)
    
    @affection_group.command(name="pat", description="Give someone a gentle head pat")
    async def pat(self, interaction: discord.Interaction, user: discord.Member):
        self.logger.info(f"{interaction.user} patted {user} using /affection pat command in {interaction.channel} on {interaction.guild}.")
        
        gif_url = await self.get_action_gif("pat")
        
        embed = discord.Embed(
            title="Head Pat!",
            description=f"{interaction.user.mention} patted {user.mention}",
            color=discord.Color(0xe898ff) 
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await interaction.response.send_message(embed=embed)
    
    @affection_group.command(name="cuddle", description="Cuddle with someone for warmth and comfort")
    async def cuddle(self, interaction: discord.Interaction, user: discord.Member):
        self.logger.info(f"{interaction.user} cuddled {user} using /affection cuddle command in {interaction.channel} on {interaction.guild}.")
        
        gif_url = await self.get_action_gif("cuddle")
        
        embed = discord.Embed(
            title="Cuddle Time!",
            description=f"{interaction.user.mention} cuddled with {user.mention}",
            color=discord.Color(0xe898ff) 
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await interaction.response.send_message(embed=embed)
    
    
    @affection_group.command(name="angry", description="Show anger towards someone")
    async def angry(self, interaction: discord.Interaction, user: discord.Member):
        self.logger.info(f"{interaction.user} is angry at {user} using /affection angry command.")
        
        gif_url = await self.get_action_gif("angry")
        
        embed = discord.Embed(
            title="Angry!",
            description=f"{interaction.user.mention} is angry at {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await interaction.response.send_message(embed=embed)
    
    
    @affection_group.command(name="bite", description="Playfully bite someone")
    async def bite(self, interaction: discord.Interaction, user: discord.Member):
        gif_url = await self.get_action_gif("bite")
        embed = discord.Embed(
            title="Nom!", description=f"{interaction.user.mention} bit {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        await interaction.response.send_message(embed=embed)
        
    @affection_group.command(name="blush", description="Blush at someone")
    async def blush(self, interaction: discord.Interaction, user: discord.Member):
        gif_url = await self.get_action_gif("blush")
        embed = discord.Embed(
            title="Blush!", description=f"{interaction.user.mention} is blushing at {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        await interaction.response.send_message(embed=embed)
        
    @affection_group.command(name="comfy", description="Get comfortable with someone")
    async def comfy(self, interaction: discord.Interaction, user: discord.Member):
        gif_url = await self.get_action_gif("comfy")
        embed = discord.Embed(
            title="Comfy!", description=f"{interaction.user.mention} got comfortable with {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        await interaction.response.send_message(embed=embed)
        
    

async def setup(bot):
    affection_cog = AffectionCog(bot)
    await bot.add_cog(affection_cog)
    
    bot.register_app_command_group(affection_cog.affection_group)

