if __name__ == "__main__":
    print("This is a cog file and cannot be run directly.")
    exit()

import logging
import discord
from discord.ext import commands, tasks
from discord import SlashCommandGroup
import datetime
import re
import asyncio

class RemindersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('bot.py')
        self.reminders = {}
        self.check_reminders.start()
        
    def cog_unload(self):
        self.check_reminders.cancel()
        
    @tasks.loop(seconds=30)
    async def check_reminders(self):
        current_time = datetime.datetime.now()
        for user_id, user_reminders in list(self.reminders.items()):
            for reminder_id, reminder in list(user_reminders.items()):
                if current_time >= reminder['time']:
                    user = self.bot.get_user(user_id)
                    if user:
                        embed = discord.Embed(
                            title="⏰ Reminder",
                            description=reminder['message'],
                            color=discord.Color(0xe898ff)
                        )
                        embed.set_footer(text=f"Reminder ID: {reminder_id}")
                        embed.timestamp = current_time
                        await user.send(embed=embed)
                    del user_reminders[reminder_id]
                    if not user_reminders:
                        del self.reminders[user_id]
                        
    reminder_group = SlashCommandGroup(name="reminder", description="Commands for managing reminders")
    
    @reminder_group.command(name="set", description="Set a reminder")
    async def reminder_set(self, ctx, time: str, message: str):
        self.logger.info(f"{ctx.author} set a reminder in {ctx.channel} on {ctx.guild}.")
        
        # Parse time string
        time_regex = re.compile(r'(\d+)([hms])')
        matches = time_regex.findall(time.lower())
        
        if not matches:
            await ctx.respond("Invalid time format. Use format like '1h30m' or '45m'", ephemeral=True)
            return
            
        reminder_time = datetime.datetime.now()
        for amount, unit in matches:
            if unit == 'h':
                reminder_time += datetime.timedelta(hours=int(amount))
            elif unit == 'm':
                reminder_time += datetime.timedelta(minutes=int(amount))
            elif unit == 's':
                reminder_time += datetime.timedelta(seconds=int(amount))
                
        # Store reminder
        if ctx.author.id not in self.reminders:
            self.reminders[ctx.author.id] = {}
            
        reminder_id = len(self.reminders[ctx.author.id]) + 1
        self.reminders[ctx.author.id][reminder_id] = {
            'time': reminder_time,
            'message': message
        }
        
        # Send confirmation
        embed = discord.Embed(
            title="⏰ Reminder Set",
            description=f"I'll remind you about:\n{message}",
            color=discord.Color(0xe898ff)
        )
        embed.add_field(name="Time", value=time, inline=True)
        embed.add_field(name="Reminder ID", value=str(reminder_id), inline=True)
        embed.set_footer(text=f"Reminder set by {ctx.author.display_name}")
        embed.timestamp = datetime.datetime.now()
        
        await ctx.respond(embed=embed)
        
    @reminder_group.command(name="list", description="List your active reminders")
    async def reminder_list(self, ctx):
        self.logger.info(f"{ctx.author} listed their reminders in {ctx.channel} on {ctx.guild}.")
        
        if ctx.author.id not in self.reminders or not self.reminders[ctx.author.id]:
            await ctx.respond("You don't have any active reminders.", ephemeral=True)
            return
            
        embed = discord.Embed(
            title="⏰ Your Reminders",
            color=discord.Color(0xe898ff)
        )
        
        for reminder_id, reminder in self.reminders[ctx.author.id].items():
            time_left = reminder['time'] - datetime.datetime.now()
            hours = time_left.seconds // 3600
            minutes = (time_left.seconds % 3600) // 60
            seconds = time_left.seconds % 60
            
            time_str = ""
            if time_left.days > 0:
                time_str += f"{time_left.days}d "
            if hours > 0:
                time_str += f"{hours}h "
            if minutes > 0:
                time_str += f"{minutes}m "
            if seconds > 0:
                time_str += f"{seconds}s"
                
            embed.add_field(
                name=f"Reminder {reminder_id}",
                value=f"Message: {reminder['message']}\nTime left: {time_str}",
                inline=False
            )
            
        embed.set_footer(text=f"Reminders for {ctx.author.display_name}")
        embed.timestamp = datetime.datetime.now()
        
        await ctx.respond(embed=embed)
        
    @reminder_group.command(name="cancel", description="Cancel a reminder")
    async def reminder_cancel(self, ctx, reminder_id: int):
        self.logger.info(f"{ctx.author} cancelled a reminder in {ctx.channel} on {ctx.guild}.")
        
        if ctx.author.id not in self.reminders or reminder_id not in self.reminders[ctx.author.id]:
            await ctx.respond(f"Reminder {reminder_id} not found.", ephemeral=True)
            return
            
        del self.reminders[ctx.author.id][reminder_id]
        if not self.reminders[ctx.author.id]:
            del self.reminders[ctx.author.id]
            
        embed = discord.Embed(
            title="⏰ Reminder Cancelled",
            description=f"Reminder {reminder_id} has been cancelled.",
            color=discord.Color(0xe898ff)
        )
        embed.set_footer(text=f"Reminder cancelled by {ctx.author.display_name}")
        embed.timestamp = datetime.datetime.now()
        
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(RemindersCog(bot))
