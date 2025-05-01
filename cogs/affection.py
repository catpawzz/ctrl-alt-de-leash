import logging
import discord
from discord.ext import commands
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
        
    affection = discord.commands.SlashCommandGroup(
        "affection", 
        "Commands for expressing affection"
    )
    
    @affection.command(name="hug", description="Send a virtual hug to someone special")
    async def hug(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} hugged {user} using /affection hug command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("hug")
        
        embed = discord.Embed(
            title="Virtual Hug!",
            description=f"{ctx.author.mention} sent a hug to {user.mention}",
            color=discord.Color(0xe898ff) 
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
    
    @affection.command(name="pat", description="Give someone a gentle head pat")
    async def pat(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} patted {user} using /affection pat command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("pat")
        
        embed = discord.Embed(
            title="Head Pat!",
            description=f"{ctx.author.mention} patted {user.mention}",
            color=discord.Color(0xe898ff) 
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
    
    @affection.command(name="cuddle", description="Cuddle with someone for warmth and comfort")
    async def cuddle(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} cuddled {user} using /affection cuddle command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("cuddle")
        
        embed = discord.Embed(
            title="Cuddle Time!",
            description=f"{ctx.author.mention} cuddled with {user.mention}",
            color=discord.Color(0xe898ff) 
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
    
    @affection.command(name="angry", description="Show anger towards someone")
    async def angry(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} is angry at {user} using /affection angry command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("angry")
        
        embed = discord.Embed(
            title="Angry!",
            description=f"{ctx.author.mention} is angry at {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
    
    @affection.command(name="bite", description="Playfully bite someone")
    async def bite(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} bit {user} using /affection bite command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("bite")
        
        embed = discord.Embed(
            title="Nom!",
            description=f"{ctx.author.mention} bit {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
        
    @affection.command(name="blush", description="Blush at someone")
    async def blush(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} blushed at {user} using /affection blush command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("blush")
        
        embed = discord.Embed(
            title="Blush!",
            description=f"{ctx.author.mention} is blushing at {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
        
    @affection.command(name="comfy", description="Get comfortable with someone")
    async def comfy(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} got comfy with {user} using /affection comfy command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("comfy")
        
        embed = discord.Embed(
            title="Comfy!",
            description=f"{ctx.author.mention} got comfortable with {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
        
    @affection.command(name="cry", description="Cry in front of someone")
    async def cry(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} cried to {user} using /affection cry command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("cry")
        
        embed = discord.Embed(
            title="Crying!",
            description=f"{ctx.author.mention} is crying to {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
        
    @affection.command(name="dance", description="Dance with someone")
    async def dance(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} danced with {user} using /affection dance command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("dance")
        
        embed = discord.Embed(
            title="Dance Time!",
            description=f"{ctx.author.mention} is dancing with {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
        
    @affection.command(name="fluff", description="Fluff someone's hair or fur")
    async def fluff(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} fluffed {user} using /affection fluff command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("fluff")
        
        embed = discord.Embed(
            title="Fluff!",
            description=f"{ctx.author.mention} fluffed {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
        
    @affection.command(name="kiss", description="Kiss someone special")
    async def kiss(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} kissed {user} using /affection kiss command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("kiss")
        
        embed = discord.Embed(
            title="Kiss!",
            description=f"{ctx.author.mention} kissed {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
        
    @affection.command(name="lay", description="Lay down with someone")
    async def lay(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} lay with {user} using /affection lay command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("lay")
        
        embed = discord.Embed(
            title="Laying Down!",
            description=f"{ctx.author.mention} is laying down with {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
        
    @affection.command(name="lick", description="Give someone a lick")
    async def lick(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} licked {user} using /affection lick command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("lick")
        
        embed = discord.Embed(
            title="Lick!",
            description=f"{ctx.author.mention} licked {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
        
    @affection.command(name="poke", description="Poke someone to get their attention")
    async def poke(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} poked {user} using /affection poke command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("poke")
        
        embed = discord.Embed(
            title="Poke!",
            description=f"{ctx.author.mention} poked {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
        
    @affection.command(name="pout", description="Pout at someone")
    async def pout(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} pouted at {user} using /affection pout command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("pout")
        
        embed = discord.Embed(
            title="Pouting!",
            description=f"{ctx.author.mention} is pouting at {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
        
    @affection.command(name="slap", description="Slap someone")
    async def slap(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} slapped {user} using /affection slap command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("slap")
        
        embed = discord.Embed(
            title="Slap!",
            description=f"{ctx.author.mention} slapped {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
        
    @affection.command(name="smile", description="Smile at someone")
    async def smile(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} smiled at {user} using /affection smile command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("smile")
        
        embed = discord.Embed(
            title="Smile!",
            description=f"{ctx.author.mention} is smiling at {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
        
    @affection.command(name="tail", description="Wag your tail at someone")
    async def tail(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} wagged their tail at {user} using /affection tail command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("tail")
        
        embed = discord.Embed(
            title="Tail Wag!",
            description=f"{ctx.author.mention} is wagging their tail at {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)
        
    @affection.command(name="tickle", description="Tickle someone")
    async def tickle(self, ctx, user: discord.Member):
        self.logger.info(f"{ctx.author} tickled {user} using /affection tickle command in {ctx.channel} on {ctx.guild}.")
        
        gif_url = await self.get_action_gif("tickle")
        
        embed = discord.Embed(
            title="Tickle!",
            description=f"{ctx.author.mention} tickled {user.mention}",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=gif_url)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.now()
        
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(AffectionCog(bot))

