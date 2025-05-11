if __name__ == "__main__":
    print("This is a cog file and cannot be run directly.")
    exit()

import logging
import re
import sqlite3
import discord
from discord.ext import commands
from google import genai
from google.genai import types
import os
import datetime
from enum import Enum

class Model(Enum):
    GEMINI_2_0_FLASH = "gemini-2.0-flash" # is the only model that supports google search
    GEMINI_2_0_FLASH_LITE = "gemini-2.0-flash-lite"
    GEMINI_2_0_FLASH_THINKING_EXP_01_21 = "gemini-2.0-flash-thinking-exp-01-21"
    GEMINI_2_5_PRO_EXP_03_25 = "gemini-2.5-pro-exp-03-25"
    GEMINI_2_5_FLASH_PREVIEW_04_17 = "gemini-2.5-flash-preview-04-17"
    
class GoogleAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')
        self.client = genai.Client(api_key=os.getenv("GOOGLE_AI_API_KEY"))

    googleai = discord.SlashCommandGroup(integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install}, name="google-ai", description="Google AI API")

    def split_text(self, text: str, max_length: int = 1900) -> list[str]:
        """
        Splits text into segments of a maximum length while preserving code blocks.

        Args:
            text (str): The text to split.
            max_length (int, optional): The maximum length of each segment. Defaults to 2000.

        Returns:
            list[str]: A list of segments of the text.
        """

        code_block_pattern = re.compile(r'```(.*?)\n(.*?)(?=\n```|\Z)', re.DOTALL)
        segments = []

        while len(text) > max_length:
            match = code_block_pattern.search(text)
            if match:
                text = self._handle_code_block(text, match, segments, max_length)
            else:
                text = self._handle_text_segment(text, segments, max_length)

        if text:
            segments.append(text)

        return segments

    def _handle_code_block(self, text, match, segments, max_length):
        start, end = match.span()
        if start > 0:
            segments.append(text[:start].rstrip())
            text = text[start:]

        code_block_content = match.group(0)
        if len(code_block_content) > max_length:
            split_code_blocks = self.split_text(code_block_content, max_length)
            segments.extend(split_code_blocks)
        else:
            segments.append(code_block_content)

        return text[end:].lstrip()

    def _handle_text_segment(self, text, segments, max_length):
        split_point = self._find_split_point(text, max_length)
        if split_point is None:
            split_point = max_length

        segments.append(text[:split_point].rstrip())
        return text[split_point:].lstrip()

    def _find_split_point(self, text, max_len):
        min_len = max_len // 2
        priority_patterns = [
            r'\n# ',      # Highest priority
            r'\n## ',     # Next priority
            r'\n### ',    # Followed by
            r'\n\d',     # followed by a digit
            r'\n\n',     # Two newlines
            r'\n'         # Single newline
        ]
        for pattern in priority_patterns:
            matches = list(re.finditer(pattern, text))
            for match in reversed(matches):
                if min_len <= match.start() <= max_len:
                    return match.start()
        return None
    
    async def is_user_allowed(self, user):
        # check the allowed_users.sqlite file for the user
        conn = sqlite3.connect('allowed_users.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM allowed_users WHERE user_id = ?', (user.id,))
        result = cursor.fetchone()
        if result:
            return True
        return False

    def create_embed(self, title, content, model_name):
        """Create a standardized embed for AI responses"""
        embed = discord.Embed(
            title=title,
            description=content,
            color=discord.Color(0xe898ff)
        )
        embed.set_footer(text=f"Model: {model_name} | Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        return embed

    def handle_long_response(self, content, question, model_name, max_embed_length=4000):
        """Handle responses that exceed Discord embed limits"""
        if len(content) > max_embed_length:
            chunks = self.split_text(content, max_embed_length)
            if len(chunks) > 6:
                # Create temp file for very long responses
                temp_filename = f"temp_{model_name.lower().replace('.', '_').replace('-', '_')}.txt"
                with open(temp_filename, "w", encoding='utf-8') as file:
                    file.write(content)
                file = discord.File(fp=temp_filename, filename="response.txt")
                embed = self.create_embed(f"Response from {model_name}", f"The response was too long to display. See attached file.", model_name)
                return {"type": "file", "embed": embed, "file": file, "filename": temp_filename}
            else:
                # Create multiple embeds
                embeds = []
                first_embed = self.create_embed(f"Response from {model_name}", chunks[0], model_name)
                embeds.append(first_embed)
                for chunk in chunks[1:]:
                    follow_embed = self.create_embed(f"Response (continued)", chunk, model_name)
                    embeds.append(follow_embed)
                return {"type": "embeds", "embeds": embeds}
        else:
            # Single embed for shorter responses
            embed = self.create_embed(f"Response from {model_name}", content, model_name)
            return {"type": "single", "embed": embed}

    @googleai.command(integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install}, name="gemini_2_0_flash", description="Ask Google AI using Gemini 2.0 Flash model with optional web search")
    async def ask_google_ai(self, ctx, 
                            question: str = discord.Option(str, name="question", description="The question to ask Google AI", required=True),
                            web_search: bool = discord.Option(bool, name="web_search", description="Whether to enable web search", required=False, default=False, store_true=True),
                            ephemeral: bool = discord.Option(bool, name="ephemeral", description="Whether to send the response as an ephemeral message", required=False, default=False, store_true=True)):
        try:
            if not await self.is_user_allowed(ctx.author):
                await ctx.respond(content="You are not allowed to use this command.", ephemeral=True)
                return
            if web_search:
                # Enable web search for the model
                tools=[
                    types.Tool(google_search=types.GoogleSearch())
                ]
                with open("cogs/google_ai_sys_prompts/gemini_2_0_flash_websearch.md", "r", encoding='utf-8') as file:
                    system_prompt = file.read()
                system_prompt = system_prompt.replace("{{userid}}", str(ctx.author.id))
                config = types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=tools
                )
            else:
                with open("cogs/google_ai_sys_prompts/gemini_2_0_flash.md", "r", encoding='utf-8') as file:
                    system_prompt = file.read()
                system_prompt = system_prompt.replace("{{userid}}", str(ctx.author.id))
                config = types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[]
                )
            
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=question),
                    ],
                ),
            ]
            
            await ctx.defer(ephemeral=ephemeral)

            response = self.client.models.generate_content(model=Model.GEMINI_2_0_FLASH.value, 
                                                    contents=contents, 
                                                    config=config)
            content = response.text
            content = content.replace("####", "###") # for discord compatibility

            model_name = "Gemini 2.0 Flash"
            response_data = self.handle_long_response(content, question, model_name)

            if response_data["type"] == "file":
                await ctx.respond(embed=response_data["embed"], file=response_data["file"], ephemeral=ephemeral)
                os.remove(response_data["filename"])
            elif response_data["type"] == "embeds":
                await ctx.respond(embed=response_data["embeds"][0], ephemeral=ephemeral)
                for embed in response_data["embeds"][1:]:
                    await ctx.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                await ctx.respond(embed=response_data["embed"], ephemeral=ephemeral)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}", ephemeral=True)

    @googleai.command(integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install}, name="gemini_2_0_flash_lite", description="Ask Google AI using Gemini 2.0 Flash Lite model")
    async def ask_google_ai_lite(self, ctx, 
                                question: str = discord.Option(str, name="question", description="The question to ask Google AI", required=True),
                                ephemeral: bool = discord.Option(bool, name="ephemeral", description="Whether to send the response as an ephemeral message", required=False, default=False, store_true=True)):
        try:
            if not await self.is_user_allowed(ctx.author):
                await ctx.respond(content="You are not allowed to use this command.", ephemeral=True)
                return
            with open("cogs/google_ai_sys_prompts/gemini_2_0_flash_lite.md", "r", encoding='utf-8') as file:
                system_prompt = file.read()
            system_prompt = system_prompt.replace("{{userid}}", str(ctx.author.id))
            config = types.GenerateContentConfig(
                system_instruction=system_prompt
            )
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=question),
                    ],
                ),
            ]

            await ctx.defer(ephemeral=ephemeral)

            response = self.client.models.generate_content(model=Model.GEMINI_2_0_FLASH_LITE.value, 
                                                    contents=contents, 
                                                    config=config)
            content = response.text
            content = content.replace("####", "###") # for discord compatibility
            
            model_name = "Gemini 2.0 Flash Lite"
            response_data = self.handle_long_response(content, question, model_name)

            if response_data["type"] == "file":
                await ctx.respond(embed=response_data["embed"], file=response_data["file"], ephemeral=ephemeral)
                os.remove(response_data["filename"])
            elif response_data["type"] == "embeds":
                await ctx.respond(embed=response_data["embeds"][0], ephemeral=ephemeral)
                for embed in response_data["embeds"][1:]:
                    await ctx.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                await ctx.respond(embed=response_data["embed"], ephemeral=ephemeral)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}", ephemeral=True)

    @googleai.command(integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install}, name="gemini_2_0_flash_thinking", description="Ask Google AI using Gemini 2.0 Flash Thinking model")
    async def ask_google_ai_thinking_exp_01_21(self, ctx, 
                                                question: str = discord.Option(str, name="question", description="The question to ask Google AI", required=True),
                                                ephemeral: bool = discord.Option(bool, name="ephemeral", description="Whether to send the response as an ephemeral message", required=False, default=False, store_true=True)):
        try:
            if not await self.is_user_allowed(ctx.author):
                await ctx.respond(content="You are not allowed to use this command.", ephemeral=True)
                return
            with open("cogs/google_ai_sys_prompts/gemini_2_0_flash_thinking_exp_01_21.md", "r", encoding='utf-8') as file:
                system_prompt = file.read()
            system_prompt = system_prompt.replace("{{userid}}", str(ctx.author.id))
            config = types.GenerateContentConfig(
                system_instruction=system_prompt
            )
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=question),
                    ],  
                ),
            ]

            await ctx.defer(ephemeral=ephemeral)

            response = self.client.models.generate_content(model=Model.GEMINI_2_0_FLASH_THINKING_EXP_01_21.value, 
                                                    contents=contents, 
                                                    config=config)
            content = response.text 
            content = content.replace("####", "###") # for discord compatibility
            
            model_name = "Gemini 2.0 Flash Thinking"
            response_data = self.handle_long_response(content, question, model_name)

            if response_data["type"] == "file":
                await ctx.respond(embed=response_data["embed"], file=response_data["file"], ephemeral=ephemeral)
                os.remove(response_data["filename"])
            elif response_data["type"] == "embeds":
                await ctx.respond(embed=response_data["embeds"][0], ephemeral=ephemeral)
                for embed in response_data["embeds"][1:]:
                    await ctx.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                await ctx.respond(embed=response_data["embed"], ephemeral=ephemeral)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}", ephemeral=True)

    @googleai.command(integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install}, name="gemini_2_5_pro", description="Ask Google AI using Gemini 2.5 Pro model with optional web search")
    async def ask_google_ai_pro_exp_03_25(self, ctx, 
                                    question: str = discord.Option(str, name="question", description="The question to ask Google AI", required=True),
                                    web_search: bool = discord.Option(bool, name="web_search", description="Whether to enable web search", required=False, default=False, store_true=True),
                                    ephemeral: bool = discord.Option(bool, name="ephemeral", description="Whether to send the response as an ephemeral message", required=False, default=False, store_true=True)):
        try:
            if not await self.is_user_allowed(ctx.author):
                await ctx.respond(content="You are not allowed to use this command.", ephemeral=True)
                return
            if web_search:
                tools=[
                    types.Tool(google_search=types.GoogleSearch())
                ]
                with open("cogs/google_ai_sys_prompts/gemini_2_5_pro_exp_websearch.md", "r", encoding='utf-8') as file:
                    system_prompt = file.read()
                system_prompt = system_prompt.replace("{{userid}}", str(ctx.author.id))
                config = types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=tools
                )
            else:   
                with open("cogs/google_ai_sys_prompts/gemini_2_5_pro_exp.md", "r", encoding='utf-8') as file:
                    system_prompt = file.read()
                system_prompt = system_prompt.replace("{{userid}}", str(ctx.author.id))
                config = types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[]
                )   
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=question),
                    ],  
                ),
            ]

            await ctx.defer(ephemeral=ephemeral)

            response = self.client.models.generate_content(model=Model.GEMINI_2_5_PRO_EXP_03_25.value, 
                                                    contents=contents, 
                                                    config=config)
            content = response.text 
            content = content.replace("####", "###") # for discord compatibility
            
            model_name = "Gemini 2.5 Pro"
            response_data = self.handle_long_response(content, question, model_name)

            if response_data["type"] == "file":
                await ctx.respond(embed=response_data["embed"], file=response_data["file"], ephemeral=ephemeral)
                os.remove(response_data["filename"])
            elif response_data["type"] == "embeds":
                await ctx.respond(embed=response_data["embeds"][0], ephemeral=ephemeral)
                for embed in response_data["embeds"][1:]:
                    await ctx.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                await ctx.respond(embed=response_data["embed"], ephemeral=ephemeral)

        except Exception as e:  
            await ctx.send(f"An error occurred: {e}", ephemeral=True)
            
    @googleai.command(integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install}, name="gemini_2_5_flash", description="Ask Google AI using Gemini 2.5 Flash model with optional web search")
    async def ask_google_ai_flash_preview_04_17(self, ctx, 
                                    question: str = discord.Option(str, name="question", description="The question to ask Google AI", required=True),
                                    web_search: bool = discord.Option(bool, name="web_search", description="Whether to enable web search", required=False, default=False, store_true=True),
                                    ephemeral: bool = discord.Option(bool, name="ephemeral", description="Whether to send the response as an ephemeral message", required=False, default=False, store_true=True)):
        try:
            if not await self.is_user_allowed(ctx.author):
                await ctx.respond(content="You are not allowed to use this command.", ephemeral=True)
                return
            if web_search:
                tools=[
                    types.Tool(google_search=types.GoogleSearch())
                ]
                with open("cogs/google_ai_sys_prompts/gemini_2_5_flash_preview_04_17_websearch.md", "r", encoding='utf-8') as file:
                    system_prompt = file.read()
                system_prompt = system_prompt.replace("{{userid}}", str(ctx.author.id))
                config = types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=tools
                )
            else:   
                with open("cogs/google_ai_sys_prompts/gemini_2_5_flash_preview_04_17.md", "r", encoding='utf-8') as file:
                    system_prompt = file.read()
                system_prompt = system_prompt.replace("{{userid}}", str(ctx.author.id))
                config = types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[]
                )   
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=question),
                    ],  
                ),
            ]

            await ctx.defer(ephemeral=ephemeral)

            response = self.client.models.generate_content(model=Model.GEMINI_2_5_FLASH_PREVIEW_04_17.value, 
                                                    contents=contents, 
                                                    config=config)
            content = response.text 
            content = content.replace("####", "###") # for discord compatibility
            
            model_name = "Gemini 2.5 Flash"
            response_data = self.handle_long_response(content, question, model_name)

            if response_data["type"] == "file":
                await ctx.respond(embed=response_data["embed"], file=response_data["file"], ephemeral=ephemeral)
                os.remove(response_data["filename"])
            elif response_data["type"] == "embeds":
                await ctx.respond(embed=response_data["embeds"][0], ephemeral=ephemeral)
                for embed in response_data["embeds"][1:]:
                    await ctx.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                await ctx.respond(embed=response_data["embed"], ephemeral=ephemeral)

        except Exception as e:  
            await ctx.send(f"An error occurred: {e}", ephemeral=True)


def setup(bot):
    bot.add_cog(GoogleAI(bot))

