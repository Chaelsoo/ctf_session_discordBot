import discord
from discord.ext import commands ,tasks
from dataclasses import dataclass
import datetime


BOT_TOKEN = "MTE0MTg0NDcyMjU2NzA5NDM2Mg.GBupKB.vzDZMCIRJ3n3x1wbTrz4ci4XbKK4w-yu48_4FQ"
CHANNEL_ID = 1163937946659983502
MAX_SESSION_TIME_MINUTES = 45


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0 
    
    
session = Session()

 
@bot.event
async def on_ready():
    print("Hello, Batman here")
    channel = bot.get_channel(CHANNEL_ID)
    # await channel.send("Hello! ")
    
    
# @bot.command()
# async def add(ctx, *arr):  # Accepts any number of arguments of any type
#     await ctx.send(f"Hello! You entered: {', '.join(map(str, arr))}")

@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
async def break_reminder():

    # Ignore the first execution of this command.
    if break_reminder.current_loop == 0:
        return

    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Take a break!** You've been studying for {MAX_SESSION_TIME_MINUTES} minutes.")

    
    
@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    break_reminder.start()
    await ctx.send(f"New session started at {human_readable_time}")


@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active!")
        return

    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    break_reminder.stop()
    await ctx.send(f"Session ended after {human_readable_duration}. Did You Solve any Challenges, hopefully ? :) ")

    
bot.run(token=BOT_TOKEN)
