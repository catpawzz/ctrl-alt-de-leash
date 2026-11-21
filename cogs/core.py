if __name__ == "__main__":
    print("This is a cog file and cannot be run directly.")
    exit()

import logging
import discord
from discord.ext import commands
from discord import SlashCommandGroup
import datetime
import time

class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')
        self.start_time = time.time()
        
    core_group = SlashCommandGroup(name="core", description="Core bot commands")
    
    @core_group.command(name="ping", description="Check the bot's latency")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: {latency}ms",
            color=discord.Color(0xe898ff)
        )
        embed.set_footer(text="Marsh")
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed, ephemeral=True)
    
    @core_group.command(name="uptime", description="Check how long the bot has been running")
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - self.bot.start_time))
        uptime_str = str(datetime.timedelta(seconds=difference))
        
        embed = discord.Embed(
            title="⏱️ Bot Uptime",
            description=f"I've been online for: **{uptime_str}**",
            color=discord.Color(0xe898ff)
        )
        embed.set_footer(text="Marsh")
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed, ephemeral=True)

    @core_group.command(name="avatar", description="Show a user's avatar")
    async def avatar(self, ctx, user: discord.Option(discord.User, "User to show", required=False)):
        user = user or ctx.author
        embed = discord.Embed(
            title=f"🖼️ {user.display_name}'s Avatar",
            color=discord.Color(0xe898ff)
        )
        embed.set_image(url=user.display_avatar.url)
        embed.set_footer(text="Marsh")
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed)

    @core_group.command(name="userinfo", description="Show info about a user")
    async def userinfo(self, ctx, user: discord.Option(discord.User, "User to look up", required=False)):
        user = user or ctx.author
        embed = discord.Embed(
            title=f"👤 {user.display_name}",
            color=discord.Color(0xe898ff)
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="Username", value=str(user), inline=True)
        embed.add_field(name="ID", value=str(user.id), inline=True)
        embed.add_field(name="Bot", value="Yes" if user.bot else "No", inline=True)
        embed.add_field(name="Account created", value=discord.utils.format_dt(user.created_at, "R"), inline=False)
        embed.set_footer(text="Marsh")
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed)

    @core_group.command(name="about", description="Learn about Marsh")
    async def about(self, ctx):
        embed = discord.Embed(
            title="☁️ About Marsh",
            description="Half debugger, half catboy, all vibes.",
            color=discord.Color(0xe898ff)
        )
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Servers", value=str(len(self.bot.guilds)), inline=True)
        embed.add_field(name="Commands", value=str(len(self.bot.application_commands)), inline=True)
        embed.set_footer(text="Marsh")
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(CoreCog(bot))

#                                                                                                    Even more stupid
#                  Stupid                                                                               ⠪⣿⡔                          
#                         ⣰⡼                                                              ⢨⣐           ⣰⣿⣽⣿⠕                        
#                        ⣺⠗                                                               ⢪⡂⠭⣐⡀        ⠃⠏⠏⠃                         
#                       ⢨⡟               ⢀⣸⢾⡔                                             ⢪⡕  ⠋⢴⣀                ⢀⣀⣰⡰⠼⠌⠏⠏⣽          
#                       ⢪⣕             ⢀⡸⠟⠁⣿⠕               ⣀⣰⣰⡐     ⣾⠽⠼⣼⣰⣐⣀⡀              ⣿    ⠋⠭⣰⡀      ⢀⣀⣰⣰⠼⠞⠏⠃⠃      ⣿          
#                       ⣠⣿⣾⣼         ⣠⡼⠇  ⢠⣿           ⢀⣠⣸⠾⠏⠃⠁⢪⣕     ⣿    ⠃⠋⠏⠏⠯⠿⠽⠼⢼⣼⣰⣰⣰⡸⠼⠟⠏⠿      ⠂⠫⡔⣠⡰⠼⠞⠏⠃⠃             ⣿          
#                       ⠂⠃⠏⠁       ⣠⡾⠇    ⣺⡗       ⢀⣠⣸⠾⠏⠃     ⢪⣿     ⢪⡕            ⣠⡼⠇⠁             ⠁                   ⢪⡿          
#                                ⣠⡾⠅     ⢀⣿⣱⣰⣐⣀⣀⣠⡸⠞⠏⠃         ⢪⣿     ⢪⡕          ⣠⠞⠁                                    ⢪⡕          
#                              ⢀⡾⠇       ⠂⠃⠃⠃⠃⠃⠏⠏⠿⢼⣴⣐⡀        ⢪⣿     ⠂⣵         ⣺⠽⠼⢰⣰⣀                                  ⢪⡕          
#                       ⢀⣀⣀   ⢀⡾⠁                  ⠂⠋⠯⠿⣼⣰⡀    ⢪⣿      ⢯⡀             ⠂⠃⠍⠄                               ⢪⡕          
#       ⢠⣰⡼⠼⠼⠿⠿⠿⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠫⠁                    ⣀⣸⠾⠏⠇⠁    ⣪⡗      ⠪⡕                                                ⣺⠁          
#       ⠂⢿⡐                                      ⢀⡸⠞⠇         ⣾⡕       ⣿                ⠊⠴⣀       ⡸⠅ ⢀⣀⣠⣰⣰⣐⣀            ⡿           
#        ⠊⣽                                      ⠁            ⣿⠁       ⠪⡔          ⣀⣰⡼⠼⣼⣰⡀       ⠂ ⣠⡾⠏⠃⠁ ⠂⠃⠋⢽⣴         ⢀⡕           
#         ⢫⣕                                                 ⢠⡿         ⠫⡐       ⢠⣾⠇⠁   ⠂⠯⣴⡀      ⢨⡟         ⢯⣵        ⢪            
#          ⢯⣔                                 ⢀⣠⣸⣼⢼⣼⣴⣐       ⢪⡕          ⠋⡐      ⣿⠅⢠⡐     ⠋⣵      ⣿⠁⢪⡔        ⣿⡐       ⠖            
#           ⢯⣔              ⢀⣀⣰⣰⣰⣰⣀          ⢠⣿⠇  ⣠⣼⣿⣿⣽⡐     ⣾⠁           ⠂⢔    ⢪⡟ ⢪⣕      ⠋      ⠏ ⢪⡕        ⢯⡕                    
#            ⠫⣴           ⢀⣸⠟⠃⠃ ⢢⣿⣿⣿⣐        ⣿⠅   ⣿⣿⣿⣿⣿⣽     ⠏          ⢬⣼⠼⠼⠼⠾⠟⠏⠏⣽ ⠊⣿               ⢪⡕        ⠪  ⠍⠼⠼⠼⡸⠼⠼⢼⡝          
#             ⠂⢭⣐         ⣾⠅    ⢪⣿⣿⣿⣿⡔       ⡗    ⣿⣿⣿⣿⣿⢯⣀⣰⣰⣰⣰⡼⢾⡿         ⠫⣴⡀     ⠏  ⣿               ⠊⠕                 ⣠⡿⠁          
#               ⠋⠤⡀      ⢪⡗     ⢪⣿⣿⣿⣿⣿       ⠅    ⢯⣿⣿⣿⣿ ⠂⠃⠁  ⢀⣿⠅          ⠊⢿⣐       ⠊      ⠠                          ⣸⠟            
#                 ⠂ ⢀⣀⣰⣸⣼⠺⡕     ⠊⣿⣿⣿⣿⣿            ⠂⢿⣿⣿⠗     ⢀⣾⠅            ⠂⢯⣵                                      ⢠⣾⠇             
#               ⢬⣼⠿⠏⠏⠇⠃   ⠅      ⠫⣿⣿⣿⠗                     ⢠⡿⠅               ⣫⡽          ⠠⠰⣼⠍⠌⠌⢼⣐⣕                ⣠⡾⠇               
#                ⠋⣽⣐              ⠂⠃⠁      ⠃              ⣨⠟⠁               ⢨⡿⠁            ⠪⡐   ⠃⢫                ⠊⣽⡐               
#                 ⠂⠯⣽⣐                                   ⠂⣿⣔                ⣿⠕              ⢭    ⢪⡕                ⢫⣵               
#                   ⠂⣿⡔               ⢠⡀ ⣀⡸⠼⣰⣰⠐           ⠊⣿⡔              ⢨⡿               ⠂⢵⡀ ⢀⣺⠅                ⠊⣿               
#                    ⣿⠅               ⠂⠏⠏⠃                 ⢯⣿              ⢪⣕⣰⡼⠾⠏⠏⠇⠃⠃⠃⠌⠴⣰     ⠋⠏⠇⠁       ⠠⣰⣰⣰⣰⣰⣰⣰⣰⣀ ⣿               
#                   ⢪⡟                                ⣀⣀   ⢪⣿              ⢿⠇⠁     ⢀⣀⣰⠼⠏⠁                 ⠂⢽⣐    ⠂⠋⠯⡿               
#                   ⣾⡕                        ⢀⣠⡸⠼⠜⠎⠏⠏⠏⠏⠏⠏⠽⢾⡟                    ⠈⠿⣓⠃                       ⠋⢽⡐                     
#                   ⣿  ⣀⣀⣠⣰⣰⣰⠐               ⠎⠋⠥⠰⠰⠰⠰⢰⡐                             ⠂⠭⢴⡀                       ⠯⣔                    
#                   ⣿⣸⠿⠏⠃⠃ ⣨⠗                      ⣨⡟⠁                              ⢀⡾⠅                        ⠋⣴                   
#                   ⠿⠅    ⣨⠗                     ⣠⡾⠇                               ⢀⡞                           ⠊⣕                  
#                        ⢠⡟                      ⠃⠯⢼⣐                              ⣪⣡⠸⠌⡼                         ⠊⡔                 
#                        ⢪⠁                         ⠫⣽⡀                            ⠃  ⢨⠅                          ⠊                 
#                        ⠋                       ⢨⣜⠏⠏⠇                                                                              
#                                                 ⠃⠭                                                                                
#                                                                                                                                   
