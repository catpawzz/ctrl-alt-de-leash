if __name__ == "__main__":
    print("This is a cog file and cannot be run directly.")
    exit()

import logging
import discord
from discord.ext import commands, tasks
from discord import app_commands
import datetime
import asyncio
import re

class RemindersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')
        self.reminders = []
        self.check_reminders.start()
        
    def cog_unload(self):
        self.check_reminders.cancel()
    
    @tasks.loop(seconds=30)
    async def check_reminders(self):
        now = datetime.datetime.now()
        to_remove = []
        
        for reminder in self.reminders:
            if now >= reminder["time"]:
                user = self.bot.get_user(reminder["user_id"])
                if user:
                    embed = discord.Embed(
                        title="⏰ Reminder",
                        description=reminder["message"],
                        color=discord.Color(0xe898ff)
                    )
                    embed.set_footer(text="Ctrl + Alt + De-leash")
                    embed.timestamp = datetime.datetime.now()
                    
                    try:
                        await user.send(embed=embed)
                    except discord.HTTPException:
                        self.logger.error(f"Failed to send reminder to user {user.id}")
                        
                to_remove.append(reminder)
                
        for reminder in to_remove:
            self.reminders.remove(reminder)
    
    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()
    
    
    reminder_group = app_commands.Group(name="reminder", description="Commands for managing reminders")
    
    @reminder_group.command(name="set", description="Set a new reminder for yourself")
    async def reminder_set(self, interaction: discord.Interaction, time: str, message: str):
        self.logger.info(f"{interaction.user} set a reminder in {interaction.channel} on {interaction.guild}.")
        
        time_regex = re.compile(r"(\d+)([mhdw])")
        match = time_regex.match(time)
        
        if not match:
            await interaction.response.send_message("Invalid time format. Use a number followed by m (minutes), h (hours), d (days), or w (weeks).", ephemeral=True)
            return
            
        amount, unit = match.groups()
        amount = int(amount)
        
        if amount <= 0:
            await interaction.response.send_message("Time amount must be positive.", ephemeral=True)
            return
            
        time_delta = None
        unit_text = ""
        
        if unit == "m":
            time_delta = datetime.timedelta(minutes=amount)
            unit_text = f"{amount} minute{'s' if amount != 1 else ''}"
        elif unit == "h":
            time_delta = datetime.timedelta(hours=amount)
            unit_text = f"{amount} hour{'s' if amount != 1 else ''}"
        elif unit == "d":
            time_delta = datetime.timedelta(days=amount)
            unit_text = f"{amount} day{'s' if amount != 1 else ''}"
        elif unit == "w":
            time_delta = datetime.timedelta(weeks=amount)
            unit_text = f"{amount} week{'s' if amount != 1 else ''}"
            
        reminder_time = datetime.datetime.now() + time_delta
        
        self.reminders.append({
            "user_id": interaction.user.id,
            "message": message,
            "time": reminder_time
        })
        
        embed = discord.Embed(
            title="⏰ Reminder Set",
            description=f"I'll remind you in {unit_text}.",
            color=discord.Color(0xe898ff)
        )
        embed.add_field(name="Message", value=message, inline=False)
        embed.add_field(name="Time", value=reminder_time.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @reminder_group.command(name="list", description="View your active reminders")
    async def reminder_list(self, interaction: discord.Interaction):
        user_reminders = [r for r in self.reminders if r["user_id"] == interaction.user.id]
        
        if not user_reminders:
            await interaction.response.send_message("You have no active reminders.", ephemeral=True)
            return
            
        embed = discord.Embed(
            title="Your Reminders",
            description=f"You have {len(user_reminders)} active reminder{'s' if len(user_reminders) != 1 else ''}.",
            color=discord.Color(0xe898ff)
        )
        
        for i, reminder in enumerate(user_reminders):
            time_str = reminder["time"].strftime("%Y-%m-%d %H:%M:%S")
            embed.add_field(
                name=f"Reminder {i+1}",
                value=f"**Message:** {reminder['message']}\n**Time:** {time_str}",
                inline=False
            )
            
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @reminder_group.command(name="cancel", description="Cancel one of your active reminders")
    async def reminder_cancel(self, interaction: discord.Interaction, index: int):
        user_reminders = [r for r in self.reminders if r["user_id"] == interaction.user.id]
        
        if not user_reminders:
            await interaction.response.send_message("You have no active reminders to cancel.", ephemeral=True)
            return
            
        if index < 1 or index > len(user_reminders):
            await interaction.response.send_message(f"Please provide a valid reminder number between 1 and {len(user_reminders)}.", ephemeral=True)
            return
            
        reminder = user_reminders[index-1]
        self.reminders.remove(reminder)
        
        embed = discord.Embed(
            title="Reminder Cancelled",
            description=f"The following reminder has been cancelled:",
            color=discord.Color(0xe898ff)
        )
        embed.add_field(name="Message", value=reminder["message"], inline=False)
        embed.set_footer(text="Ctrl + Alt + De-leash")
        embed.timestamp = datetime.datetime.now()
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    reminder_cog = RemindersCog(bot)
    await bot.add_cog(reminder_cog)
    
    bot.register_app_command_group(reminder_cog.reminder_group)
