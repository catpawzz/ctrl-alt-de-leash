
import logging
import discord
from discord.ext import commands, tasks

from dotenv import load_dotenv
import os
import datetime
import time
import sys
import asyncio


load_dotenv()

class Bot(commands.AutoShardedBot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            intents=intents,
            application_id=os.getenv('APPLICATION_ID'),
            
            sync_commands=True
        )
        
        
        
        self.start_time = time.time()
        self.logger = setup_logger()
        
        
        self.setup_events()
        
    def setup_events(self):
        
        @self.event
        async def on_ready():
            self.logger.info(f"Bot is ready! Logged in as {self.user} (ID: {self.user.id})")
            self.logger.info(f"Bot is in {len(self.guilds)} guilds")
            
            
            
            self.logger.info("Commands set to sync automatically with sync_commands=True")
            self.logger.info("Note: Global commands may take up to an hour to update")
            
            
            print("\n🔄 Loading extensions from on_ready event...")
            
            self.load_extensions()
            print("✅ Extensions loading process complete\n")
            
            
            display_name = os.getenv('BOT_NAME')
            if display_name and self.user.display_name != display_name:
                try:
                    await self.user.edit(username=display_name)
                    self.logger.info(f"Changed bot display name to: {display_name}")
                except discord.HTTPException as e:
                    self.logger.error(f"Failed to change display name: {e}")
                    
        @self.event
        async def on_connect():
            self.logger.info("Connected to Discord!")
            print("\n📡 Connected to Discord!")
            
        @self.event
        async def on_disconnect():
            self.logger.warning("Disconnected from Discord!")
        
    async def setup_hook(self):
        """This is called when the bot starts up"""
        print("\n⚙️ Setup hook called - this should appear before on_ready")
        self.logger.info("Setting up bot...")
            
    
    def load_extensions(self):
        """Load all cogs from the cogs directory using synchronous methods"""
        self.logger.info("Loading extensions synchronously...")
        
        
        current_file = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file)
        cogs_dir = os.path.join(current_dir, 'cogs')
        
        print(f"🔍 Current file: {current_file}")
        print(f"📂 Looking for cogs in: {cogs_dir}")
        
        
        if not os.path.exists(cogs_dir):
            print(f"⚠️ WARNING: Cogs directory '{cogs_dir}' does not exist!")
            self.logger.warning(f"Cogs directory '{cogs_dir}' does not exist!")
            os.makedirs(cogs_dir)
            print(f"📁 Created empty cogs directory at '{cogs_dir}'")
            return
        
        
        cog_files = [f for f in os.listdir(cogs_dir) 
                    if os.path.isfile(os.path.join(cogs_dir, f)) and f.endswith('.py')]
        if not cog_files and not [d for d in os.listdir(cogs_dir) 
                                if os.path.isdir(os.path.join(cogs_dir, d))]:
            print(f"⚠️ WARNING: No Python files found in cogs directory '{cogs_dir}'!")
            self.logger.warning(f"No Python files found in cogs directory '{cogs_dir}'")
            return
            
        print(f"🔍 Found {len(cog_files)} potential cog files in '{cogs_dir}'")
        self._recursive_load_extensions(cogs_dir, 'cogs')
        print(f"🏁 Finished loading extensions")
            
    
    def _recursive_load_extensions(self, dir_path, package_path):
        """Recursively load all extensions from directories"""
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            
            
            if os.path.isfile(item_path) and item.endswith('.py') and not item.startswith('__'):
                extension_name = f'{package_path}.{item[:-3]}'
                try:
                    self.logger.info(f"Loading extension: {extension_name}")
                    
                    self.load_extension(extension_name)
                    self.logger.info(f"Loaded extension: {extension_name}")
                    
                    print(f"✅ Loaded cog: {extension_name}")
                except Exception as e:
                    self.logger.error(f"Failed to load extension: {extension_name}")
                    self.logger.error(f"Error: {str(e)}")
                    print(f"❌ Error loading extension: {extension_name}")
                    print(f"Error: {str(e)}")
            
            
            elif os.path.isdir(item_path) and not item.startswith('__'):
                
                if os.path.exists(os.path.join(item_path, '__init__.py')):
                    
                    package_extension = f'{package_path}.{item}'
                    try:
                        self.logger.info(f"Loading package: {package_extension}")
                        
                        self.load_extension(package_extension)
                        self.logger.info(f"Loaded package: {package_extension}")
                        
                        print(f"📦 Loaded package: {package_extension}")
                    except Exception as e:
                        self.logger.error(f"Failed to load package: {package_extension}")
                        self.logger.error(f"Error: {str(e)}")
                        print(f"❌ Error loading package: {package_extension}")
                    
                    
                    
                    self._recursive_load_extensions(item_path, f'{package_path}.{item}')


def setup_logger():
    """
    Setup the logger.
    """
    
    logger = logging.getLogger('mewo.py')
    logger.setLevel(logging.DEBUG)

    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    
    logger.addHandler(console_handler)

    return logger

def run_bot():
    """Initialize and run the bot"""
    load_dotenv()
    bot = Bot()
    
    
    bot.logger.info("Starting bot...")
    
    try:
        
        bot.run(os.getenv('BOT_TOKEN'))
    except Exception as e:
        print(f"Critical error running bot: {e}")  
        bot.logger.error(f"Critical error running bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_bot()