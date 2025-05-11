import discord
from discord.ext import commands
from discord import SlashCommandGroup, Option
import pyfiglet
import datetime

class ASCIICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.styles = pyfiglet.FigletFont.getFonts()
        
    ascii_group = SlashCommandGroup(name="ascii", description="Generate ASCII art from text")
    
    @ascii_group.command(name="text", description="Convert text to ASCII art")
    async def ascii_text(self, ctx, 
                         text: Option(str, "Text to convert to ASCII art", required=True),
                         style: Option(str, "ASCII art style", required=False, default="standard", 
                                      choices=["standard", "slant", "banner", "big", "block", "bubble", 
                                              "digital", "ivrit", "mini", "script", "shadow", "small", 
                                              "smscript", "smshadow", "smslant", "doom", "alligator"])):
        if style not in self.styles:
            closest_matches = [s for s in self.styles if style.lower() in s.lower()][:5]
            
            if closest_matches:
                matches_str = "\n".join(closest_matches)
                error_msg = f"Style '{style}' not found. Did you mean one of these?\n{matches_str}"
            else:
                error_msg = f"Style '{style}' not found. Try 'standard', 'slant', 'banner', 'big', or 'block'."
                
            await ctx.respond(error_msg, ephemeral=True)
            return
            
        try:
            fig = pyfiglet.Figlet(font=style)
            ascii_art = fig.renderText(text)
            
            if len(ascii_art) > 4000:
                await ctx.respond("The generated ASCII art is too large to display.", ephemeral=True)
                return
                
            embed = discord.Embed(
                title=f"ASCII Art: {style}",
                description=f"```{ascii_art}```",
                color=discord.Color(0xe898ff)
            )
            embed.set_footer(text="Ctrl + Alt + De-leash")
            embed.timestamp = datetime.datetime.now()
            
            await ctx.respond(embed=embed)
            
        except Exception as e:
            await ctx.respond(f"Error generating ASCII art: {str(e)}", ephemeral=True)
    
    @ascii_group.command(name="styles", description="List available ASCII art styles")
    async def list_styles(self, ctx):
        popular_styles = ["standard", "slant", "banner", "big", "block", "bubble", 
                          "digital", "ivrit", "mini", "script", "shadow", "small", 
                          "smscript", "smshadow", "smslant", "doom", "alligator"]
        
        style_list = "\n".join(popular_styles)
        
        embed = discord.Embed(
            title="Available ASCII Art Styles",
            description=f"Popular styles:\n```{style_list}```\nPlus {len(self.styles) - len(popular_styles)} more styles.",
            color=discord.Color(0xe898ff)
        )
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(ASCIICog(bot))

                                                                                                                            
#                                                                                They're in looooveeeeeeee                                                   
#                                                                                 meow meow meow nyaaaahh                          
#                                                           ⢀⣀                                                                      
#                                               ⣀⣐          ⣺⡿⢿⣴⣐⡀      ⣼⣼⡀                                                         
#                                             ⣠⣾⢿⣿          ⣿⡕ ⠂⠏⢿⣼⣐⡀   ⢪⣿⣽⡐                                                        
#                                           ⣠⣾⠟⠁⢪⣿        ⢀⣸⣿⠄    ⠂⠋⠿⣼⣐ ⢪⣿⠫⣿⣐                                                       
#                                        ⢀⣠⣾⠟⠁  ⣾⣿      ⢀⣸⡿⢯⣿         ⠋⢿⣾⣿⡕⠊⢿⣽⡀                                                     
#                                      ⢀⣸⣿⠟⠁    ⣿⣿    ⢀⣸⡿⢇⣀⣪⣿⣰⣰⣰⣰⣰⣰⣐    ⢫⣿⡕  ⠋⢿⣴⣐                                ⢀⡀                 
#                                    ⢀⣸⡿⠏⠁      ⣿⡕ ⣀⣰⣸⣿⡿⠿⠟⠏⠏⠇⠃⠃⠃⠃⢃⣻⡟    ⢪⣿⡕    ⠋⠿⣿⣴⣐⡀                  ⣀⣀⣰⣰⣸⣼⡼⠿⠿⠿⢯⣿                 
#     ⢠⣼⣼⣼⣼⣼⣰⣰⣰⣰⣰⣰⣰⣰⣰⣰⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣸⡿⠇⠁        ⢿⣽⡿⠟⠃⠁          ⢀⣾⡟  ⢀⣠⣸⣾⣿⠕      ⠂⠋⠯⢿⣽⣴⣐⡀     ⢀⣀⣠⣰⣸⣼⠼⠿⠟⠏⠇⠃⠃      ⣺⡿                 
#      ⢿⣵ ⠂⠃⠃⠃⠃⠃⠃⠃⠃⠃⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⢯⡿⠁          ⠂⠁              ⣾⡟⢀⣠⣼⡿⠟⠃⠁            ⠂⠋⠯⢿⣼⣰⣸⠼⠟⠏⠇⠃⠃              ⢀⣿⡕                 
#      ⠪⣿⡔                         ⠪⠅                          ⣺⣷⣸⡿⠟⠁                    ⠋⢿⣽⡀                   ⢪⣿⠁                 
#       ⢿⣽                                                    ⣢⣿⠿⠇                         ⠋⠅                   ⣿⡗                  
#       ⠂⣿⣕                                                 ⣠⣾⣟⠁                                               ⢪⣿⠅                  
#        ⠫⣿⡐                                                ⠏⠏⠿⠿⣿⣼⣼⣰⣰⣀                                         ⣿⡗                   
#         ⢯⣽⡀                                                   ⣿  ⠃⠃⠋⠏⠴                                      ⣪⣿⠁                   
#         ⠂⢿⣵                                                   ⣿                                            ⢀⣿⡗                    
#          ⠊⣿⣔                         ⣠⡰                      ⢠⣿                                            ⣪⣿                     
#           ⠊⣿⡔                       ⠊⠁               ⠊⠏⠼⠐    ⢪⣿                                           ⢀⣿⠕                     
#            ⠫⣿⡐                                               ⢪⣿                                           ⣺⡟                      
#             ⠊⣿⣐                                              ⢪⣿⣐   ⢵                                     ⠨⠇                       
#              ⠂⢿⣴⡀             ⢀⣀⣰⣰⣼⣼⣼⣾⣿⡿⠕             ⣼⣼⣼⣼⣼⣼⣰⣰⡿⢿⣽⣐ ⠂⢵            ⣠⠕    ⣀⣰⣸⣼⣼⣼⠾⠽⠔   ⢰⣰⣰⣰⣰⣸⣼⣼⣼⡾⢿⣿⡕                  
#                ⠫⣿⣴⡀        ⢠⣸⠿⠟⠏⠃⠃⠁                        ⠃⠃⢫⡕ ⠋⢿⣽⣐             ⠁ ⣀⣸⣾⣿⠿⠏⠇⠃                 ⢀⣾⡟                   
#                 ⠂⢯⣽⣰⣰⣸⡼⠿⠇                         ⣀          ⢪⡕   ⠋⠯⡵             ⡿⠿⠏⠃                     ⢠⣾⠟                    
#               ⠯⣿⡟⠏⠏⠃⠃                                        ⢪⡕                                           ⣸⣿⠇                     
#                ⠂⠯⣴⡀                              ⢀    ⢨      ⣺⡕         ⠈⠄                              ⢠⣾⠟⠁                      
#                  ⠋⢿⣴                      ⣴ ⢀⣀⣰⣸⠞⠇⠯⢽⣰⣰⣾      ⣿⡕   ⢪⡕    ⣀⡀     ⢠                        ⢪⣿⡀                       
#                    ⠯⣽⡐                    ⠋⠏⠏⠇⠁      ⠁⠪      ⣿⡕   ⢪⡝⣴⣀⣠⣘⠃⠋⠼⠴⠸⠼⠌⠃⣵                        ⣿⣕                       
#                    ⢪⣿                                        ⢿⡕   ⢪⠅   ⢫⡐       ⢪⡔                       ⠪⣿⡀                      
#                    ⢪⡿                                        ⢪⡕   ⢫     ⢯⡐       ⣵                        ⣿⣕    ⣀⣰⠼⠼⠾⠿⠼⠼⢼⣰⡀       
#                    ⣿⡕                                        ⢪⡕          ⠫⣴⡀    ⢠⡗               ⢀⣀⣠⣰⣰⣰⣰⣐⣀⢪⣿  ⣠⡾⠇        ⠂⠏⢽⡐     
#                    ⣿⡕                                        ⣿⣿    ⣀⣀⣀⣀⣀⣀⣀⣂⣏⣼⣰⣰⣸⠟             ⣠⣸⡿⠏⠇⠃⠃⠃⠃⠃⠋⠏⠿⠿⢀⡺⠇             ⢯⣔    
#                    ⣿⡕      ⣀⣀⣀⣀⣀⣀⣀⣀⡀                 ⣀⣀⣰⣰⣸⣼⣼⣿⣿⠿⠿⠿⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠌      ⠯⣽⣐           ⡾⠁   ⣀⣀  ⢀⣰⣼⣰    ⢯⣔   
#                    ⣿⣵⣼⡼⠾⠿⠏⠏⠇⠃⠃⠃⣻⠗⠃⠃⠃              ⠈⠎⠃⢁⣠⡸⠾⠏⠇⠃⠁                                  ⠋⢿⣵ ⠠⣼⣼⠴⣰⣰⣐⣀⣪⠕   ⣺⣿⣿⣿⣴⣾⣿⣿⣿⡕    ⣿⡀  
#                    ⠏⠃        ⢀⣾⠕                  ⢀⣸⠞⠇⠁                                         ⠂⠯⣽⡐⠂⠋⠽⣴⣀⠂⠃⠃    ⢿⣿⣿⣿⣿⣿⣿⣿⣿⠁    ⢫⡕  
#                             ⢀⣾⠗                 ⢀⣾⠗⠁                                              ⠋⣿⣐  ⠂⠋⠽⣴⡀    ⠂⢿⣿⣿⣿⣿⣿⡿⠅     ⣿⠕  
#                ⢀⣀⢠⣿⣽⡀       ⣾⠗                 ⣨⣿⣱⠰⠰⠐                                              ⠊⣿⡔     ⣵      ⠋⢿⣿⣿⠟⠁     ⢠⡿   
#                ⢿⣿⣿⣿⣿⡕      ⣺⡗                  ⣿⠃                                                   ⠊⣿⣔    ⢯⡐       ⠂⠁      ⢀⣾⠅   
#                ⠂⠯⣿⣿⡿      ⣨⡿                   ⢿⣐⣰⣰⣰⣐⡀                                               ⠂⢿⣔    ⠫⣴             ⣠⡾⠁    
#                  ⠂⠃      ⢠⣿⠅                    ⠋⠭⢼⣰⣰⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⡀                                    ⠂⢿⣔    ⠂⠭⢴⣀⣀     ⣀⣠⣸⠞⠇      
#                          ⣺⡕                         ⠂⠃⠃⠃⠃⠋⠏⠏⠏⠏⠏⠏⠏⠏⠏⠏⠯⠿⠿⠿⠿⠿⠿⢼⣼⣼⣰⣰⣐⣀                      ⢯⣔      ⠂⠃⠋⠏⠏⠏⠃⠃⠁         
#                         ⢨⡿                                                   ⠂⠃⠃⠏⠏⣿⣼⡀                   ⠂⢿⡐                       
#                         ⣾⠅                                                     ⠠⠜⠇⣁⣪⡕                    ⠂⣿⡐                      
#                        ⢠⡿                                                       ⠘⠎⣫⡟⠁                     ⠊⣽⡀                     
#                        ⣺⡕                                                      ⢀⣠⡾⠇                        ⠫⡵                     
#                       ⢠⣿⠁                                                   ⢀⣠⣼⠟⠃                                                 
#                       ⢪⡿                                               ⢀⣀⣰⣼⠿⠏⠃                                                    
#                       ⠪⠕                                      ⢀⣀⣀⣀⣰⣰⣼⡾⠿⠟⠏⠃                                                        
#                                               ⠰⠰⢰⣰⣰⣰⣰⣼⣼⣼⡼⠼⠼⠾⠿⠟⠏⠏⠇⠃⢫⠁                                                              
#                                                                   ⠂                                                               
#                                                                                                                                   
