if __name__ == "__main__":
    print("This is a cog file and cannot be run directly.")
    exit()

import logging
import discord
from discord.ext import commands
from discord import SlashCommandGroup
import random
from datetime import datetime
import aiohttp
from io import BytesIO

class ActionsCog(commands.Cog):
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
                        tmp_url = data.get("url")
                else:
                    return None
        async with aiohttp.ClientSession() as session:
            async with session.get(tmp_url) as resp:
                if resp.status != 200:
                    return None
                data = await resp.read()
        file_type = tmp_url.split(".")[-1]
        file = discord.File(BytesIO(data), filename=f"{action}.{file_type}")
        return file

    actions_group = SlashCommandGroup(name="actions", description="Commands for expressing actions")
    
    @actions_group.command(name="hug", description="Send a virtual hug to someone special")
    async def hug(self, ctx: discord.ApplicationContext, user: discord.Member):
        self.logger.info(f"{ctx.author} hugged {user} using /actions hug command in {ctx.channel} on {ctx.guild}.")
        
        file = await self.get_action_gif("hug")
        if file is None:
            await ctx.respond("Could not fetch hug GIF.")
            return
        embed = discord.Embed(
            title="Virtual Hug!",
            description=f"{ctx.author.mention} sent a hug to {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=f"attachment://{file.filename}")
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        await ctx.respond(embed=embed, file=file)
    
    @actions_group.command(name="pat", description="Give someone a gentle head pat")
    async def pat(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} patted {user} using /actions pat command in {ctx.channel} on {ctx.guild}.")
        
        file = await self.get_action_gif("pat")
        if file is None:
            await ctx.respond("Could not fetch pat GIF.")
            return
        embed = discord.Embed(
            title="Head Pat!",
            description=f"{ctx.author.mention} patted {user.mention}",
            color=discord.Color(0xe898ff) 
        )
        embed.set_image(url=f"attachment://{file.filename}")
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        await ctx.respond(embed=embed, file=file)
    
    @actions_group.command(name="cuddle", description="Cuddle with someone for warmth and comfort")
    async def cuddle(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} cuddled {user} using /actions cuddle command in {ctx.channel} on {ctx.guild}.")
        
        file = await self.get_action_gif("cuddle")
        if file is None:
            await ctx.respond("Could not fetch cuddle GIF.")
            return
        embed = discord.Embed(
            title="Cuddle Time!",
            description=f"{ctx.author.mention} cuddled with {user.mention}",
            color=discord.Color(0xe898ff) 
        )
        embed.set_image(url=f"attachment://{file.filename}")
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        await ctx.respond(embed=embed, file=file)
    
    @actions_group.command(name="angry", description="Show anger towards someone")
    async def angry(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} is angry at {user} using /actions angry command.")
        
        file = await self.get_action_gif("angry")
        if file is None:
            await ctx.respond("Could not fetch angry GIF.")
            return
        embed = discord.Embed(
            title="Angry!",
            description=f"{ctx.author.mention} is angry at {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=f"attachment://{file.filename}")
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        await ctx.respond(embed=embed, file=file)
    
    @actions_group.command(name="bite", description="Playfully bite someone")
    async def bite(self, ctx, user: discord.Member):
        file = await self.get_action_gif("bite")
        if file is None:
            await ctx.respond("Could not fetch bite GIF.")
            return
        embed = discord.Embed(
            title="Nom!", 
            description=f"{ctx.author.mention} bit {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=f"attachment://{file.filename}")
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        await ctx.respond(embed=embed, file=file)
        
    @actions_group.command(name="blush", description="Blush at someone")
    async def blush(self, ctx, user: discord.Member):
        file = await self.get_action_gif("blush")
        if file is None:
            await ctx.respond("Could not fetch blush GIF.")
            return
        embed = discord.Embed(
            title="Blush!", 
            description=f"{ctx.author.mention} is blushing at {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=f"attachment://{file.filename}")
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        await ctx.respond(embed=embed, file=file)
        
    @actions_group.command(name="comfy", description="Get comfortable with someone")
    async def comfy(self, ctx, user: discord.Member):
        file = await self.get_action_gif("comfy")
        if file is None:
            await ctx.respond("Could not fetch comfy GIF.")
            return
        embed = discord.Embed(
            title="Comfy!", 
            description=f"{ctx.author.mention} got comfortable with {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=f"attachment://{file.filename}")
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        await ctx.respond(embed=embed, file=file)

def setup(bot):
    bot.add_cog(ActionsCog(bot))

