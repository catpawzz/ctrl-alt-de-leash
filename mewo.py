# mewo.py
import logging
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import datetime
import time
import sys
import asyncio

# Load the environment variables from .env file
load_dotenv()

class Bot(commands.AutoShardedBot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(intents=intents, sync_commands=True)
        self.start_time = time.time()
        self.logger = setup_logger()
        
        # Load all cogs
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

# Create a logger with timestamp in the file name
def setup_logger():
    """
    Setup the logger.
    """
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(logs_dir, f"bot_{timestamp}.log")
    logger = logging.getLogger('mewo.py')
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set the log level
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the file handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def run_bot():
    """Initialize and run the bot"""
    load_dotenv()
    bot = Bot()
    
    try:
        bot.run(os.getenv('BOT_TOKEN'))
        bot.logger.info("Bot started")
        bot.logger.info(f"Bot is running as {bot.user.name} in {len(bot.guilds)} guilds")
    except Exception as e:
        bot.logger.error(f"Error running bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_bot()