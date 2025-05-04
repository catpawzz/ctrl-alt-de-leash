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
import os
import base64

class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')
    
    misc_group = SlashCommandGroup(name="misc", description="Miscellaneous utility commands")
    
    @misc_group.command(name="choose", description="Choose between multiple options")
    async def choose(self, ctx, options: discord.Option(str, "Comma-separated options", required=True)):
        choices = [option.strip() for option in options.split(",") if option.strip()]
        
        if len(choices) < 2:
            await ctx.respond("Please provide at least two options separated by commas")
            return
        
        choice = random.choice(choices)
        
        embed = discord.Embed(
            title="Random Choice",
            description=f"🤔 I choose: **{choice}**",
            color=discord.Color(0xe898ff)
        )
        
        embed.add_field(name="All Options", value="\n".join([f"• {option}" for option in choices]), inline=False)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await ctx.respond(embed=embed)
    
    @misc_group.command(name="coding_time", description="Show catpawz's coding time stats")
    async def coding_time(self, ctx):
        await ctx.defer()
        
        API_BASE = "https://" + os.getenv('WAKATIME_URL') + "/api"
        API_KEY = f"Basic {base64.b64encode(os.getenv('WAKATIME_KEY').encode()).decode()}"
        HEADERS = {"Authorization": API_KEY}
        
        embed = discord.Embed(
            title="🧑‍💻 Catpawz's Coding Stats",
            description="Tracking programming time with Wakapi",
            color=discord.Color(0xe898ff)
        )
        
        try:
            async with aiohttp.ClientSession(headers=HEADERS) as session:
                async with session.get(f"{API_BASE}/summary?interval=today") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        self.logger.debug(f"Today's data: {data}")
                        total_seconds = 0
                        for project in data.get("projects", []):
                            total_seconds += project.get("total", 0)
                        hours = int(total_seconds // 3600)
                        minutes = int((total_seconds % 3600) // 60)
                        today_value = f"**{hours}h {minutes}m** today"
                        languages = data.get("languages", [])
                        if languages:
                            top_langs = sorted(languages, key=lambda x: x.get("total", 0), reverse=True)[:3]
                            lang_stats = []
                            for lang in top_langs:
                                mins = int(lang.get("total", 0) // 60)
                                if mins > 0:
                                    lang_stats.append(f"{lang.get('key')}: {mins}m")
                            
                            if lang_stats:
                                today_value += "\n**Top languages:**\n" + "\n".join(f"• {s}" for s in lang_stats)
                        embed.add_field(name="Today's Coding Time", value=today_value, inline=False)
                    else:
                        error_text = await resp.text()
                        self.logger.error(f"API error ({resp.status}): {error_text}")
                        embed.add_field(name="Today's Coding Time", value=f"Failed to fetch data (HTTP {resp.status})", inline=False)
                async with session.get(f"{API_BASE}/summary?interval=last_30_days") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        total_seconds = 0
                        for project in data.get("projects", []):
                            total_seconds += project.get("total", 0)
                            
                        total_hours = round(total_seconds / 3600, 1)
                        embed.add_field(
                            name="Last 30 Days", 
                            value=f"**{total_hours}h** of coding in the last month", 
                            inline=False
                        )
                async with session.get(f"{API_BASE}/summary?interval=all_time") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        total_seconds = 0
                        for project in data.get("projects", []):
                            total_seconds += project.get("total", 0)
                        total_hours = round(total_seconds / 3600, 1)
                        embed.add_field(
                            name="All Time Stats", 
                            value=f"**{total_hours}h** total tracked coding time", 
                            inline=False
                        )
        
        except Exception as e:
            self.logger.error(f"Error fetching Wakapi stats: {str(e)}")
            embed.add_field(name="Error", value=f"Failed to fetch detailed stats: {str(e)}", inline=False)
        
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(MiscCog(bot))