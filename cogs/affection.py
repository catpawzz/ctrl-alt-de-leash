import logging
import discord
from discord.ext import commands
import random
from datetime import datetime

class AffectionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')
        
        self.hug_gifs = [
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbThhNWR4cTVrZGpuZnFobmNibmVyYXJxdmRnY3hhbzNjampqcDhxYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/GMFUrC8E8aWoo/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbThhNWR4cTVrZGpuZnFobmNibmVyYXJxdmRnY3hhbzNjampqcDhxYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/qscdhWs5o3yb6/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbThhNWR4cTVrZGpuZnFobmNibmVyYXJxdmRnY3hhbzNjampqcDhxYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/PHZ7v9tfQu0o0/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbThhNWR4cTVrZGpuZnFobmNibmVyYXJxdmRnY3hhbzNjampqcDhxYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/od5H3PmEG5EVq/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbThhNWR4cTVrZGpuZnFobmNibmVyYXJxdmRnY3hhbzNjampqcDhxYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ZQN9jsRWp1M76/giphy.gif",
            "https://media.giphy.com/media/5eyhBKLvYhafu/giphy.gif?cid=ecf05e47hh0mm7nk95qv953z9vg6sfvp4tp7mojrfjqetump&ep=v1_gifs_search&rid=giphy.gif&ct=g",
            "https://media.giphy.com/media/VXP04aclCaUfe/giphy.gif?cid=ecf05e47cy36uwf4c3gyaascvtsvk8jrqw96pwnb29daqfnq&ep=v1_gifs_search&rid=giphy.gif&ct=g"
        ]
        
        self.pat_gifs = [
            "https://media.giphy.com/media/109ltuoSQT212w/giphy.gif",
            "https://media.giphy.com/media/ARSp9T7wwxNcs/giphy.gif",
            "https://media.giphy.com/media/ye7OTQgwmVuVy/giphy.gif",
            "https://media.giphy.com/media/Z7x24IHBcmV7W/giphy.gif",
            "https://media.giphy.com/media/L2z7dnOduqEow/giphy.gif",
            "https://media.giphy.com/media/5tmRHwTlHAA9WkVxTU/giphy.gif",
            "https://media.giphy.com/media/osYdfUptPqV0s/giphy.gif"
        ]
        
        self.cuddle_gifs = [
            "https://media.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif",
            "https://media.giphy.com/media/ZQN9jsRWp1M76/giphy.gif",
            "https://media.giphy.com/media/143v0Z4767T15e/giphy.gif",
            "https://media.giphy.com/media/du8yT5dStTeMg/giphy.gif",
            "https://media.giphy.com/media/IRUb7GTCaPU8E/giphy.gif"
        ]
        
        self.tackle_gifs = [
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcGRyaG9mbjZkYnBwOWI5eXNqd2dsemMxZWNnN3kzN3d5am4xODRjMCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/uXXPhr8D6HSXS/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcGRyaG9mbjZkYnBwOWI5eXNqd2dsemMxZWNnN3kzN3d5am4xODRjMCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/kz0qWS2lAqtdAnEmEM/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcGRyaG9mbjZkYnBwOWI5eXNqd2dsemMxZWNnN3kzN3d5am4xODRjMCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/G6fmc0H5xpZDO/giphy.gif",
            "https://media.giphy.com/media/us8FXd0EtOXXa/giphy.gif?cid=ecf05e472huzjeuacr80dbh862i4chzosp6y07kjqas8rvhd&ep=v1_gifs_search&rid=giphy.gif&ct=g"
        ]

    # Create an affection command group
    affection = discord.commands.SlashCommandGroup(
        "affection", 
        "Commands for expressing affection",
        integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install}
    )
    
    @affection.command(
        name="hug",
        description="Send a virtual hug to someone special"
    )
    async def hug(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} hugged {user} using /affection hug command in {ctx.channel} on {ctx.guild}.")
        
        random_hug = random.choice(self.hug_gifs)
        
        embed = discord.Embed(
            title="Virtual Hug!",
            description=f"{ctx.author.mention} sent a hug to {user.mention}",
            color=discord.Color(0xe898ff) 
        )
        embed.set_image(url=random_hug)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
    
    @affection.command(
        name="pat",
        description="Give someone a gentle head pat"
    )
    async def pat(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} patted {user} using /affection pat command in {ctx.channel} on {ctx.guild}.")
        
        random_pat = random.choice(self.pat_gifs)
        
        embed = discord.Embed(
            title="Head Pat!",
            description=f"{ctx.author.mention} patted {user.mention}",
            color=discord.Color(0xe898ff) 
        )
        embed.set_image(url=random_pat)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
    
    @affection.command(
        name="cuddle",
        description="Cuddle with someone for warmth and comfort"
    )
    async def cuddle(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} cuddled {user} using /affection cuddle command in {ctx.channel} on {ctx.guild}.")
        
        random_cuddle = random.choice(self.cuddle_gifs)
        
        embed = discord.Embed(
            title="Cuddle Time!",
            description=f"{ctx.author.mention} cuddled with {user.mention}",
            color=discord.Color(0xe898ff) 
        )
        embed.set_image(url=random_cuddle)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
    
    @affection.command(
        name="tackle",
        description="Playfully tackle someone to the ground"
    )
    async def tackle(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} tackled {user} using /affection tackle command in {ctx.channel} on {ctx.guild}.")
        
        random_tackle = random.choice(self.tackle_gifs)
        
        embed = discord.Embed(
            title="Tackle!",
            description=f"{ctx.author.mention} tackled {user.mention}",
            color=discord.Color(0xe898ff) 
        )
        embed.set_image(url=random_tackle)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(AffectionCog(bot))