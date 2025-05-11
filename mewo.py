import logging
import discord
from discord.ext import commands, tasks
from discord import application_command as app_commands
from discord import IntegrationType
from dotenv import load_dotenv
import os
import datetime
import time
import sys
import asyncio
import signal
import colorlog


load_dotenv()

class Bot(commands.AutoShardedBot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.reactions = True
        intents.dm_messages = True
        super().__init__(
            intents=intents,
            sync_commands=True,
            default_command_integration_types=[IntegrationType.user_install, IntegrationType.guild_install]
        )
        
        self.start_time = time.time()
        self.logger = setup_logger()
        self.load_extensions()
        
    def load_extensions(self) -> None:
        """Load all cogs from the cogs directory"""
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.load_extension(f'cogs.{filename[:-3]}')
                    self.logger.info(f"Loaded extension: {filename}")
                except Exception as e:
                    self.logger.error(f"Failed to load extension: {filename}")
                    self.logger.error(f"Error: {str(e)}")
                    print(f"Error loading extension: {filename}")
                    print(f"Error: {str(e)}")
        
    async def on_ready(self):
        print("""\033[95m
       ::::::::      :::     :::::::::  :::  
     :+:    :+:   :+: :+:   :+:    :+: :+:   
    +:+         +:+   +:+  +:+    +:+ +:+    
   +#+        +#++:++#++: +#+    +:+ +#+     
  +#+        +#+     +#+ +#+    +#+ +#+      
 #+#    #+# #+#     #+# #+#    #+# #+#       
########  ###     ### #########  ########## 
\033[97m-------------------------------------------------
\033[90mMade by @catpawzz and @Snupai
I like my cat and meow this code is scuffed :3
\033[97m-------------------------------------------------
\033[91mWARNING: Please make sure this bot can only be
     installed as a user app, not on a server!
     It is not ready for that yet.          
\033[97m-------------------------------------------------\033[0m
        """)
        self.logger.info(f"Bot is ready! Logged in as {self.user} (ID: {self.user.id})")
        self.logger.info(f"Bot is in {len(self.guilds)} guilds")
        self.logger.info(f"Bot has been installed by {len(self.users)} users")

        
        display_name = os.getenv('BOT_NAME')
        if display_name and self.user.display_name != display_name:
            try:
                await self.user.edit(username=display_name)
                self.logger.info(f"Changed bot display name to: {display_name}")
            except discord.HTTPException as e:
                self.logger.error(f"Failed to change display name: {e}")

def setup_logger():
    logger = logging.getLogger('mewo.py')
    logger.setLevel(logging.DEBUG)
    
    # Console handler with colors
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Color formatter with emojis
    color_formatter = colorlog.ColoredFormatter(
        '%(log_color)s[%(asctime)s] %(levelname)-2s%(reset)s: %(message_emoji)s',
        datefmt='%H:%M:%S',
        log_colors={
            'DEBUG': 'blue',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    
    # Custom filter to add emojis based on log level
    class EmojiFilter(logging.Filter):
        def filter(self, record):
            if record.levelno == logging.DEBUG:
                record.message_emoji = f"🔍 {record.msg}"
            elif record.levelno == logging.INFO:
                record.message_emoji = f"ℹ️ {record.msg}"
            elif record.levelno == logging.WARNING:
                record.message_emoji = f"⚠️ {record.msg}"
            elif record.levelno == logging.ERROR:
                record.message_emoji = f"❌ {record.msg}"
            elif record.levelno == logging.CRITICAL:
                record.message_emoji = f"🚨 {record.msg}"
            else:
                record.message_emoji = record.msg
            return True
    
    emoji_filter = EmojiFilter()
    console_handler.addFilter(emoji_filter)
    console_handler.setFormatter(color_formatter)
    
    # File handler for persistent logs
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    file_handler = logging.FileHandler(
        os.path.join(log_dir, f'bot_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('[%(asctime)s] %(levelname)-2s: %(message_emoji)s', 
                                      datefmt='%H:%M:%S')
    file_handler.addFilter(emoji_filter)
    file_handler.setFormatter(file_formatter)
    
    # Add both handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def run_bot():
    bot = Bot()
    bot.logger.info("Starting application...")
    
    # Debug token loading
    token = os.getenv('BOT_TOKEN')
    if not token:
        bot.logger.critical("No BOT_TOKEN found in environment variables")
        print("❌ No BOT_TOKEN found in environment variables")
        sys.exit(1)
    
    # Create cogs directory if it doesn't exist
    cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
        bot.logger.info(f"Created cogs directory at: {cogs_dir}")
    
    # Set up signal handlers
    def signal_handler(signum, frame):
        bot.logger.warning("Received shutdown signal. Gracefully shutting down...")
        print("\n🛑 Received shutdown signal. Gracefully shutting down...")
        bot._shutdown = True
        asyncio.create_task(bot.close())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        bot.run(os.getenv('BOT_TOKEN'))
    except Exception as e:
        bot.logger.critical(f"Critical error running bot: {e}")
        print(f"\n❌ Critical error running bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_bot()
                                                                          
#                                                                                        
#                                ⣀⣀⣰⡀                                                     
#                          ⢀⣀⡰⠼⠎⠇⠃⢡⡞⣀⣀⣀⣰⣰⣰⣰⣀⣀⣀                                            
#                      ⢀⣠⡸⠞⠇⠁    ⠸⠟⠇⠃        ⠃⠃⠏⠼⢴⣐⡀         Such a silly cat in the code                             
#                   ⢀⣠⠜⠇⠁                         ⢂⣻⠔             how'd he land here?! 
#                ⣀⡸⠞⠃⠁                           ⣠⠞⠁                                      
#             ⢀⡸⠞⠃                            ⢀⡨⠟⠁                                        
#          ⢀⣠⠞⠇                               ⠂⠋⠭⣰⡀                                       
#        ⣀⡸⠇⠁               ⣀⡀                    ⠋⢴⣀                                     
#       ⠪⣗              ⢀⡸⠎⢇⣿⣿⡿⢴⡀       ⢸⣷⠭⣐        ⠋⢵⡀                    ⢀⣠⣸⠼⢼⣼⢼⣴⡀      
#        ⠊⢽⣀            ⡞  ⣾⣿⣿⣽⣀⣿       ⣿⣾⡕⠫⠔      ⠼⠼⣼⡿             ⣀⣀⣰⣰⣰⣼⣾⠏⠃   ⢫⡔⠂⣿⣔     
#        ⢠⡾⠇         ⣠  ⢁ ⢪⣿⣿⣿⣿⣿⡿       ⣿⣿⡕          ⠂⠯⢴⡀     ⣀⣰⣸⣾⣿⣿⣿⣿⣿⣿⣿⣿⡕       ⠐⠒⢫     
#        ⠃⠏⠼⣐       ⡸⠇⠵⡸⠇ ⠂⢿⣿⣿⣿⠟⠁     ⠨⠐⢯⡿   ⣠⣴ ⢠    ⢀⣸⠟⠁  ⣀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡕        ⢨⡿     
#           ⠋⢽⣐⡀            ⠂⠃    ⣀         ⢪⡕⠪⠜⠇ ⣀⣠⣰⣿⣼⣼⣴⣰⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣵      ⢀⣸⠟⠁     
#             ⠂⠋⠍⠼⠰⣰⣐⣀⡀     ⣀⣀⣀⡀  ⠋⠏⠍⢎⣀⣀⣀⣰⠸⠞⠇  ⣠⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣐   ⢨⡿⠁       
#                   ⣸⣗⣁⣀⣀⣠⡐⣺⠇ ⠂⠁   ⠂⠏⢿⣳⠷⣰⣰⣰⣰⡰⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣼⡿⠁        
#      ⣀⡰⠼⠌⠬⠏⠌⠼⠴⣐⡀   ⠃⠃⠃⠃⠁⢨⡕          ⠋⢵⡀  ⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁         
#    ⢀⡾⠇         ⠋⢽⣐      ⢪⡑   ⢠⡀      ⠂⣽⡀⣨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠇           
#    ⡾⠁            ⠋⣵     ⢪⡕   ⠂⡕       ⠊⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠇             
#    ⡕              ⠂⣵    ⢪⡕    ⢯       ⢨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠏⠃                
#    ⢯⡐              ⠪⡔   ⠪⡕    ⢪⡔      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣐                
#     ⠋⠴⣰⣀⣀⣠⣰⣐        ⢿    ⡕    ⠊⡕     ⢪⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣴⡀              
#            ⠃⠭⣴⡀     ⠊⣔   ⡕     ⣽     ⢪⣕⢪⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠏⣏⣃⣃⣳⣃⣃⠏⢽⡐             
#              ⠂⠯⡐     ⠋⣴⡀ ⡕     ⢯     ⠂⢿⡐⢯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠏⠯⣿⣿⠿⠿⠏⠏⠿⠿⢿⣿⣽             
#                ⢿      ⠂⠋⠼⣽     ⢪⡔     ⠂⣿⣐⠫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠇⠁    ⠋⣰       ⢫⡕            
#                ⠊⢵      ⢠⡞      ⢪⡕      ⠊⢿⣽⣒⠋⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇       ⢬⣫⡕      ⠂⣿            
#                 ⠂⠯⣰⣀⡀⢀⡰⠟       ⠊⡕        ⠯⣿⣽⣴⣒⡋⠏⠿⢿⣿⣿⣿⣿⣿⣿⣑      ⣰ ⢪⣿⠅      ⢀⣿            
#                    ⠃⡻⠇          ⣿⢵⡀       ⠂⠏⢿⣿⣿⣽⣼⣰⣰⣰⣰⣰⣰⣿⣿⣽⣴⣐⣀⣀⣠⣿⡸⠟⠁       ⣪⡗            
#                    ⢪⡕ ⣨   ⡀     ⢿⠂⢭⡐         ⠂⠋⠏⠿⠿⠿⠿⠿⠿⠿⠿⠏⠃ ⢂⣻⡟⠃⠁         ⣨⡟             
#                    ⠊⣵⡀⢿   ⡕     ⣺⠕ ⠋⠴⣐                   ⢀⣰⡾⠇         ⢀⣠⡾⠇              
#                     ⠂⠃⠏⠝⠬⠴⢽⡰⠼⠌⠌⠎⠇⠏⠬⠴⣰⣂⣏⣼⣰⣀⣀          ⢀⣀⣰⡼⢿⣿⣰⣀⣀   ⢀⣀⣠⣰⡾⠏⠃                
#                                        ⠃ ⠃⠋⠏⠏⠭⠼⠼⠼⠼⠼⠏⠏⠇⠃⠁   ⠃⠃⠃⠏⠏⠏⠇⠃⠃                    
#                                                                                         
#                                                                                         