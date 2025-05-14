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
    
    @misc_group.command(name="define", description="Get the definition of a word or phrase")
    async def define(self, ctx, word: discord.Option(str, "The word to define", required=True)):
        await ctx.defer()  
        
        
        word = word.strip().lower()
        
        
        api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        
                        embed = discord.Embed(
                            title=f"📖 Definition of '{word}'",
                            color=discord.Color(0xe898ff)
                        )
                        
                        
                        if data and isinstance(data, list) and len(data) > 0:
                            entry = data[0]
                            
                            
                            phonetics = next((item for item in entry.get("phonetics", []) if item.get("text")), None)
                            if phonetics and phonetics.get("text"):
                                embed.description = f"*Pronunciation: {phonetics.get('text')}*"
                            
                            
                            meanings = entry.get("meanings", [])
                            for meaning in meanings[:3]:  
                                part_of_speech = meaning.get("partOfSpeech", "")
                                definitions = meaning.get("definitions", [])
                                
                                if definitions:
                                    
                                    definition_text = definitions[0].get("definition", "No definition found")
                                    example = definitions[0].get("example", "")
                                    
                                    field_value = f"{definition_text}"
                                    if example:
                                        field_value += f"\n\n*Example: \"{example}\"*"
                                        
                                    embed.add_field(
                                        name=f"as {part_of_speech.capitalize()}", 
                                        value=field_value, 
                                        inline=False
                                    )
                            
                            
                            if len(embed.fields) == 0:
                                embed.add_field(
                                    name="No Definition", 
                                    value="No detailed definition found for this word.", 
                                    inline=False
                                )
                        else:
                            embed.add_field(
                                name="Error", 
                                value="Unexpected API response format.", 
                                inline=False
                            )
                            
                    elif response.status == 404:
                        embed = discord.Embed(
                            title=f"📖 Definition of '{word}'",
                            description="No definition found for this word.",
                            color=discord.Color(0xe898ff)
                        )
                    else:
                        embed = discord.Embed(
                            title="Error",
                            description=f"Failed to fetch definition (HTTP {response.status})",
                            color=discord.Color(0xe898ff)
                        )
                    
                    embed.set_footer(text="Ctrl + Alt + De-leash")
                    embed.timestamp = datetime.datetime.now()
                    
                    await ctx.respond(embed=embed)
                    
        except Exception as e:
            self.logger.error(f"Error fetching word definition: {str(e)}")
            await ctx.respond(f"An error occurred while fetching the definition: {str(e)}")

    @misc_group.command(name="wiki", description="Search Wikipedia for information")
    async def wiki(self, ctx, query: discord.Option(str, "Search query", required=True)):
        await ctx.defer()  
        
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": 3,  
            "srprop": "snippet"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                
                async with session.get(search_url, params=search_params) as search_resp:
                    if search_resp.status != 200:
                        await ctx.respond(f"Error searching Wikipedia (HTTP {search_resp.status})")
                        return
                    
                    search_data = await search_resp.json()
                    search_results = search_data.get("query", {}).get("search", [])
                    
                    if not search_results:
                        embed = discord.Embed(
                            title="Wikipedia Search",
                            description=f"No results found for '{query}'",
                            color=discord.Color(0xe898ff)
                        )
                        embed.set_footer(text="Ctrl + Alt + De-leash")
                        embed.timestamp = datetime.datetime.now()
                        await ctx.respond(embed=embed)
                        return
                    
                    
                    embed = discord.Embed(
                        title=f"📚 Wikipedia Results for '{query}'",
                        color=discord.Color(0xe898ff)
                    )
                    
                    
                    for i, result in enumerate(search_results[:3]):
                        page_title = result.get("title")
                        page_id = result.get("pageid")
                        
                        
                        summary_params = {
                            "action": "query",
                            "format": "json",
                            "prop": "extracts|info",
                            "exintro": "1",  
                            "explaintext": "1",  
                            "inprop": "url",
                            "pageids": str(page_id)  
                        }
                        
                        async with session.get(search_url, params=summary_params) as summary_resp:
                            if summary_resp.status != 200:
                                embed.add_field(
                                    name=f"{i+1}. {page_title}",
                                    value=f"Error fetching summary (HTTP {summary_resp.status})",
                                    inline=False
                                )
                                continue
                            
                            summary_data = await summary_resp.json()
                            page_data = summary_data.get("query", {}).get("pages", {}).get(str(page_id), {})
                            
                            extract = page_data.get("extract", "No summary available.")
                            url = page_data.get("fullurl", f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}")
                            
                            
                            if len(extract) > 300:
                                extract = extract[:297] + "..."
                            
                            embed.add_field(
                                name=f"{i+1}. {page_title}",
                                value=f"{extract}\n\n[Read more...]({url})",
                                inline=False
                            )
                    
                    embed.set_footer(text="Source: Wikipedia • Ctrl + Alt + De-leash")
                    embed.timestamp = datetime.datetime.now()
                    
                    await ctx.respond(embed=embed)
        
        except Exception as e:
            self.logger.error(f"Error fetching Wikipedia information: {str(e)}")
            await ctx.respond(f"An error occurred while searching Wikipedia: {str(e)}")


    @misc_group.command(name="meaning", description="Get the meaning of internet slang and acronyms")
    async def meaning(self, ctx, term: discord.Option(str, "Abbreviation or slang term (e.g., 'iirc', 'brb')", required=True)):
        
        acronyms = {
            
            "afk": "Away From Keyboard",
            "brb": "Be Right Back",
            "btw": "By The Way",
            "fyi": "For Your Information",
            "gg": "Good Game",
            "gtg": "Got To Go",
            "idk": "I Don't Know",
            "iirc": "If I Recall Correctly",
            "imho": "In My Humble Opinion",
            "imo": "In My Opinion",
            "lmao": "Laughing My [Posterior] Off",
            "lmk": "Let Me Know",
            "lol": "Laughing Out Loud",
            "ngl": "Not Gonna Lie",
            "np": "No Problem",
            "omg": "Oh My God",
            "omw": "On My Way",
            "rn": "Right Now",
            "rofl": "Rolling On Floor Laughing",
            "smh": "Shaking My Head",
            "tbh": "To Be Honest",
            "tfw": "That Feeling When",
            "til": "Today I Learned",
            "tldr": "Too Long; Didn't Read",
            "ttyl": "Talk To You Later",
            "ty": "Thank You",
            "wfh": "Working From Home",
            "wtf": "What The [Flip]",
            "yolo": "You Only Live Once",
            "asap": "As Soon As Possible",
            "atm": "At The Moment",
            "bff": "Best Friends Forever",
            "dw": "Don't Worry",
            "ffs": "For [Flip's] Sake",
            "ftw": "For The Win",
            "hmu": "Hit Me Up",
            "icymi": "In Case You Missed It",
            "imk": "In My Knowledge",
            "iirl": "If In Real Life",
            "jk": "Just Kidding",
            "nbd": "No Big Deal",
            "nvm": "Never Mind",
            "otw": "On The Way",
            "pov": "Point Of View",
            "smol": "Small (intentional misspelling)",
            "sus": "Suspicious",
            "tba": "To Be Announced",
            "tbc": "To Be Continued",
            "thx": "Thanks",
            "wdym": "What Do You Mean",
            "wym": "What You Mean",
            
            
            "ama": "Ask Me Anything",
            "dm": "Direct Message",
            "fomo": "Fear Of Missing Out",
            "nsfw": "Not Safe For Work",
            "op": "Original Poster",
            "tl;dr": "Too Long; Didn't Read",
            "alt": "Alternative Account",
            "fb": "Facebook",
            "ig": "Instagram",
            "irl": "In Real Life",
            "rt": "Retweet",
            "sm": "Social Media",
            "tbt": "Throwback Thursday",
            "yt": "YouTube",
            "pfp": "Profile Picture",
            "ratioed": "When replies/quotes outnumber likes",
            "shadowban": "Hidden restriction on content visibility",
            
            
            "afk": "Away From Keyboard",
            "aoe": "Area Of Effect",
            "bg": "Background or Battleground",
            "buff": "Beneficial Effect",
            "debuff": "Negative Effect",
            "dps": "Damage Per Second",
            "hp": "Health Points",
            "mmorpg": "Massively Multiplayer Online Role-Playing Game",
            "moba": "Multiplayer Online Battle Arena",
            "nerf": "Reduction in power",
            "npc": "Non-Player Character",
            "pve": "Player Versus Environment",
            "pvp": "Player Versus Player",
            "afk": "Away From Keyboard",
            "aggro": "Aggression (drawing enemy attention)",
            "alt": "Alternative Character",
            "bot": "Robot (AI-controlled player)",
            "cd": "Cooldown",
            "fps": "First-Person Shooter",
            "gg ez": "Good Game Easy (often used sarcastically)",
            "gg wp": "Good Game Well Played",
            "gl hf": "Good Luck Have Fun",
            "lfg": "Looking For Group",
            "mana": "Magic Points/Energy",
            "meta": "Most Effective Tactics Available",
            "mob": "Mobile Object/Monster",
            "noob": "Newbie (inexperienced player)",
            "rng": "Random Number Generator",
            "rpg": "Role-Playing Game",
            "rts": "Real-Time Strategy",
            "tank": "Character designed to absorb damage",
            "xp": "Experience Points",
            "apm": "Actions Per Minute",
            
            
            "api": "Application Programming Interface",
            "css": "Cascading Style Sheets",
            "html": "Hypertext Markup Language",
            "ide": "Integrated Development Environment",
            "json": "JavaScript Object Notation",
            "os": "Operating System",
            "sql": "Structured Query Language",
            "ui": "User Interface",
            "ux": "User Experience",
            "vm": "Virtual Machine",
            "ai": "Artificial Intelligence",
            "aws": "Amazon Web Services",
            "cli": "Command Line Interface",
            "cpu": "Central Processing Unit",
            "crud": "Create, Read, Update, Delete",
            "css": "Cascading Style Sheets",
            "ddos": "Distributed Denial of Service",
            "dns": "Domain Name System",
            "gui": "Graphical User Interface",
            "http": "Hypertext Transfer Protocol",
            "iot": "Internet of Things",
            "ip": "Internet Protocol",
            "lan": "Local Area Network",
            "ml": "Machine Learning",
            "npm": "Node Package Manager",
            "oop": "Object-Oriented Programming",
            "php": "PHP: Hypertext Preprocessor",
            "ram": "Random Access Memory",
            "saas": "Software as a Service",
            "sdk": "Software Development Kit",
            "ssd": "Solid State Drive",
            "url": "Uniform Resource Locator",
            "voip": "Voice Over Internet Protocol",
            "wan": "Wide Area Network",
            
            
            "asap": "As Soon As Possible",
            "b2b": "Business to Business",
            "b2c": "Business to Consumer",
            "ceo": "Chief Executive Officer",
            "cfo": "Chief Financial Officer",
            "cto": "Chief Technology Officer",
            "eod": "End of Day",
            "hr": "Human Resources",
            "kpi": "Key Performance Indicator",
            "pto": "Paid Time Off",
            "roi": "Return on Investment",
            "swot": "Strengths, Weaknesses, Opportunities, Threats",
            "wfh": "Work From Home",
            "cob": "Close of Business",
            "eob": "End of Business",
            "ooo": "Out of Office",
            "poc": "Proof of Concept",
            "pr": "Public Relations"
        }
        
        
        clean_term = term.strip().lower()
        
        embed = discord.Embed(
            title=f"📚 Meaning of '{term}'",
            color=discord.Color(0xe898ff)
        )
        
        
        if clean_term in acronyms:
            meaning = acronyms[clean_term]
            embed.description = f"**{clean_term.upper()}** = {meaning}"
        else:
            embed.description = f"I don't know the meaning of '{term}'. 😕"
            
            
            similar_terms = [k for k in acronyms.keys() if clean_term in k or k in clean_term]
            if similar_terms:
                suggestions = "\n".join([f"• **{term.upper()}**: {acronyms[term]}" for term in similar_terms[:5]])
                embed.add_field(name="Did you mean one of these?", value=suggestions, inline=False)
            
            
            embed.add_field(
                name="Need more terms?",
                value="This is a limited selection of common acronyms and internet slang. More terms will be added over time.",
                inline=False
            )
            
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await ctx.respond(embed=embed)

        @misc_group.command(name="randomcat", description="Get a random cat picture")
        async def randomcat(self, ctx, cat: discord.Option(str, "Cat to display", 
                                                          choices=["yumi"], 
                                                          required=True, 
                                                          default="yumi")):
            await ctx.defer()
            
            api_url = f"https://api.cat-space.net/api/sfw/images/cat-{cat}"
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(api_url) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            if data.get("status") == "success" and data.get("url"):
                                embed = discord.Embed(
                                    title=f"Random {cat.capitalize()} Cat Picture",
                                    color=discord.Color(0xe898ff)
                                )
                                embed.set_image(url=data["url"])
                                embed.set_footer(text="Ctrl + Alt + De-leash")
                                embed.timestamp = datetime.datetime.now()
                                
                                await ctx.respond(embed=embed)
                            else:
                                await ctx.respond(f"Failed to get a cat picture: {data.get('status', 'Unknown error')}")
                        else:
                            await ctx.respond(f"Failed to fetch cat picture (HTTP {response.status})")
            
            except Exception as e:
                self.logger.error(f"Error fetching cat picture: {str(e)}")
                await ctx.respond(f"An error occurred while fetching a cat picture: {str(e)}")

def setup(bot):
    bot.add_cog(MiscCog(bot))