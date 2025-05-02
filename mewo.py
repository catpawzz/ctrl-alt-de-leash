import logging
import discord
from discord.ext import commands, tasks
from discord import app_commands

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
        intents.dm_messages = True
        intents.dm_reactions = True
        
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            intents=intents,
            application_id=os.getenv('APPLICATION_ID'),
            sync_commands=False,
            sync_commands_debug=True
        )
        
        self.start_time = time.time()
        self.logger = setup_logger()
        self.guild_ids = [int(gid) for gid in os.getenv('GUILD_IDS', '').split(',') if gid]
        
        
        self.synced = False
        
        self._registered_command_groups = set()
        self._loaded_extensions = []
        
        self.setup_events()
    
    
    def register_app_command_group(self, group):
        """Safely register an app command group, avoiding duplicates"""
        group_name = group.name
        if group_name in self._registered_command_groups:
            self.logger.warning(f"Command group '{group_name}' already registered, skipping")
            return False
        
        try:
            self._registered_command_groups.add(group_name)
            self.tree.add_command(group)
            self.logger.info(f"Registered command group: {group_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error registering command group '{group_name}': {e}")
            return False
    
    async def setup_hook(self):
        print("\n⚙️ Setup hook called - this should appear before on_ready")
        self.logger.info("Setting up bot...")
        
        
        self._registered_command_groups.clear()
        
        
        print("\n🔄 Loading extensions from setup_hook...")
        await self.load_extensions_async()
        print("✅ Extensions loading process complete\n")
        
    async def on_ready(self):
        self.logger.info(f"Bot is ready! Logged in as {self.user} (ID: {self.user.id})")
        self.logger.info(f"Bot is in {len(self.guilds)} guilds")
        
        
        if not self.synced:
            await self.sync_all_commands()
            self.synced = True
            
        display_name = os.getenv('BOT_NAME')
        if display_name and self.user.display_name != display_name:
            try:
                await self.user.edit(username=display_name)
                self.logger.info(f"Changed bot display name to: {display_name}")
            except discord.HTTPException as e:
                self.logger.error(f"Failed to change display name: {e}")
    
    def setup_events(self):
        
        @self.event
        async def on_connect():
            self.logger.info("Connected to Discord!")
            print("\n📡 Connected to Discord!")
            
        @self.event
        async def on_disconnect():
            self.logger.warning("Disconnected from Discord!")
    
    async def sync_all_commands(self):
        self.logger.info("Syncing commands globally and to development guilds")
        
        
        all_commands = [cmd.name for cmd in self.tree.get_commands()]
        self.logger.info(f"Command tree has {len(all_commands)} commands to sync: {', '.join(all_commands)}")
        
        if not all_commands:
            self.logger.warning("No commands found in command tree! Check that your cogs are properly adding commands.")
            return
            
        try:
            
            self.logger.info("Clearing any existing command sync state")
            await self.tree.sync(guild=None)
            
            if not self.guild_ids:
                self.logger.info("No guild IDs provided, syncing only globally")
                synced = await self.tree.sync()
                self.logger.info(f"Synced {len(synced)} commands globally: {', '.join([cmd.name for cmd in synced]) if synced else 'none'}")
            else:
                
                synced = await self.tree.sync()
                self.logger.info(f"Synced {len(synced)} commands globally: {', '.join([cmd.name for cmd in synced]) if synced else 'none'}")
                
                
                for guild_id in self.guild_ids:
                    guild = discord.Object(id=guild_id)
                    self.tree.copy_global_to(guild=guild)
                    guild_synced = await self.tree.sync(guild=guild)
                    self.logger.info(f"Synced {len(guild_synced)} commands to guild ID {guild_id}")
        except Exception as e:
            self.logger.error(f"Error syncing commands: {e}")
            print(f"❌ Error syncing commands: {e}")
    
    async def load_extensions_async(self):
        """Load all cogs from the cogs directory using asynchronous methods"""
        self.logger.info("Loading extensions asynchronously...")
        
        
        self._loaded_extensions = []
        
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
        loaded = await self._recursive_load_extensions_async(cogs_dir, 'cogs')
        self._loaded_extensions.extend(loaded)
        print(f"🏁 Finished loading extensions. Total loaded: {len(self._loaded_extensions)}")
        
    async def _recursive_load_extensions_async(self, dir_path, package_path):
        """Recursively load all extensions from directories"""
        loaded_extensions = []
        
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            
            if os.path.isfile(item_path) and item.endswith('.py') and not item.startswith('__'):
                extension_name = f'{package_path}.{item[:-3]}'
                
                
                if extension_name in self._loaded_extensions:
                    self.logger.warning(f"Extension {extension_name} already loaded, skipping")
                    continue
                    
                try:
                    self.logger.info(f"Loading extension: {extension_name}")
                    await self.load_extension(extension_name)
                    loaded_extensions.append(extension_name)
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
                    
                    
                    if package_extension in self._loaded_extensions:
                        self.logger.warning(f"Package {package_extension} already loaded, skipping")
                        continue
                        
                    try:
                        self.logger.info(f"Loading package: {package_extension}")
                        await self.load_extension(package_extension)
                        loaded_extensions.append(package_extension)
                        self.logger.info(f"Loaded package: {package_extension}")
                        print(f"📦 Loaded package: {package_extension}")
                    except Exception as e:
                        self.logger.error(f"Failed to load package: {package_extension}")
                        self.logger.error(f"Error: {str(e)}")
                        print(f"❌ Error loading package: {package_extension}")
                    
                    
                    sub_loaded = await self._recursive_load_extensions_async(item_path, f'{package_path}.{item}')
                    loaded_extensions.extend(sub_loaded)
                    
        return loaded_extensions

    def load_extensions(self):
        """Legacy synchronous method - keeping for compatibility"""
        loop = asyncio.get_event_loop()
        loop.create_task(self.load_extensions_async())


def setup_logger():
    logger = logging.getLogger('mewo.py')
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

def run_bot():
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