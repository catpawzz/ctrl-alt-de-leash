import discord
from discord.ext import commands
from discord import SlashCommandGroup, Option
import googletrans
from googletrans import Translator
import datetime

class TranslateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()
        self.languages = {code: name for code, name in googletrans.LANGUAGES.items()}
        
    translate_group = SlashCommandGroup(name="translate", description="Translate text between languages")
    
    @translate_group.command(name="text", description="Translate text to another language")
    async def translate_text(self, ctx, 
                           text: Option(str, "Text to translate", required=True),
                           target_lang: Option(str, "Target language (e.g., en, es, fr, ja)", required=True),
                           source_lang: Option(str, "Source language (leave blank for auto-detect)", required=False, default=None)):
        try:
            if source_lang is None:
                result = await self.translator.translate(text, dest=target_lang)
            else:
                result = await self.translator.translate(text, src=source_lang, dest=target_lang)
                
            source_language = self.languages.get(result.src, result.src)
            target_language = self.languages.get(result.dest, result.dest)
            
            embed = discord.Embed(
                title=f"Translation: {source_language.capitalize()} → {target_language.capitalize()}",
                color=discord.Color(0xe898ff)
            )
            
            embed.add_field(name="Original", value=text, inline=False)
            embed.add_field(name="Translation", value=result.text, inline=False)
            embed.set_footer(text="Ctrl + Alt + De-leash")
            embed.timestamp = datetime.datetime.now()
            
            await ctx.respond(embed=embed)
            
        except Exception as e:
            await ctx.respond(f"Error during translation: {str(e)}", ephemeral=True)
    
    @translate_group.command(name="languages", description="List available language codes")
    async def list_languages(self, ctx):
        language_list = "\n".join([f"`{code}` - {name.capitalize()}" for code, name in list(self.languages.items())[:20]])
        
        embed = discord.Embed(
            title="Available Language Codes",
            description=f"Here are some common language codes:\n{language_list}\n\n*And many more...*",
            color=discord.Color(0xe898ff)
        )
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(TranslateCog(bot))
