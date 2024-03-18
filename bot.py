import discord
from config import PHOTOBOT_KEY
import random
import asyncio
import os
import math

user_message_counts = {}
bot = discord.Bot()

def save_xp_to_file(user_message_counts):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, 'xp_values.txt')
    with open(file_path, 'w') as file:
        for user_id, xp in user_message_counts.items():
            file.write(f"{user_id}:{xp}\n")

def load_xp_from_file():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, 'xp_values.txt')
    user_message_counts = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                user_id, xp = line.strip().split(':')
                user_message_counts[int(user_id)] = int(xp)
    except FileNotFoundError:
        pass  # File doesn't exist yet, which is fine
    return user_message_counts

user_message_counts = load_xp_from_file()  # Initialize with values from file
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Photography Simulator"))
    async def save_xp_periodically():
        await bot.wait_until_ready()
        while not bot.is_closed():
            save_xp_to_file(user_message_counts)
            await asyncio.sleep(200)  # Wait for  5 minutes

    bot.loop.create_task(save_xp_periodically())


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id
    user_name = message.author.name
    user_message_counts[user_id] = user_message_counts.get(user_id,  0) + random.randint(5,  15)

    # Calculate the user's level
    xp = user_message_counts[user_id]
    levelf =  0.3 * math.sqrt(xp)
    level = int(levelf)

    # Define the roles and their corresponding levels
    roles_levels = {
        10:  1207111158000263259,  # Level  10 role ID
        20:  1207111456659742730,  # Level  20 role ID
        30:  1207113962228023298,  # Level  30 role ID
        40:  1207113104492863578,  # Level  40 role ID
        60:  1207111046863785994,  # Level  60 role ID
        80:  1207103055103926302,  # Level  80 role ID
        90:  1207111660376948777,  # Level  90 role ID
        100:  1205492582512332810,  # Level  100 role ID
        120:  1207102955333882016,  # Level  120 role ID
        140:  1207112059796455434,  # Level  140 role ID
    }

    # Check if the user's level matches any of the roles
    for required_level, role_id in roles_levels.items():
        if required_level + 0.3 >= levelf >= required_level:
            # Fetch the role by ID
            role = discord.utils.get(message.guild.roles, id=role_id)
            if role is not None:
                # Assign the role to the user
                await message.author.add_roles(role)
                print(f"Role for level {required_level} has been assigned to {user_name}.")
            else:
                print(f"Role for level {required_level} not found.")

    # Process commands after checking for role assignment
    # await bot.process_commands(message)

@bot.command(description="Lets you see your level") 
async def level(ctx): 
    user_id = ctx.author.id
    xp = user_message_counts.get(user_id, 0)
    levelf = 0.3 * math.sqrt (xp)
    level = int(levelf)
    prcntf = (levelf - level) * 1000
    prcnt = (int(prcntf)) / 10
    await ctx.respond(f"You have {xp} xp \n That is level {level}! \n thats {prcnt}% of the way there to the next level")
    
@bot.command(description="Counts the total number of messages sent by a user across all channels in the server.")
async def count_all_messages(ctx, user: discord.Member):
    message_count =  0
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):  # Ensure we're only counting messages in text channels
            async for message in channel.history(limit=None):  # Fetch all messages in the channel
                if message.author == user:
                    message_count +=  1
    await ctx.respond(f"{user.name} has sent {message_count} messages across all channels in this server.")

@bot.command(description="Counts the total number of messages sent by a user in the current channel.")
async def count_messages(ctx, user: discord.Member):
    message_count =  0
    async for message in ctx.channel.history(limit=None):
        if message.author == user:
            message_count +=  1
    await ctx.respond(f"{user.name} has sent {message_count} messages in this channel.")

@bot.command(description="preview levels") 
async def levels(ctx): 
    await ctx.respond(f"# roles: \n <@&1207111158000263259> - level 10 \n <@&1207111456659742730> - level 20 \n <@&1207113962228023298> - level 30 \n <@&1207113104492863578> - level 40 \n <@&1207111046863785994> - level 60 \n <@&1207103055103926302> - level 80 \n <@&1207111660376948777> - level 90 \n <@&1205492582512332810> - level 100 \n <@&1207102955333882016>  - level 120 \n <@&1207112059796455434> - level 140")


bot.run(PHOTOBOT_KEY)
