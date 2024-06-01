import discord
from config import PHOTOBOT_KEY
import random
import asyncio
import os
import math
import threading

def listen_for_console_input():
    while True:
        command = input()
        if command == "save":
            save_xp_to_file(user_message_counts)
            print("XP saved.")

threading.Thread(target=listen_for_console_input, daemon=True).start()


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

emoji_map = {
    0: "<:zero:1219277173014270052>",
    1: "<:jeden:1219277208929959937>",
    2: "<:dwa:1219277207550169129>",
    3: "<:trzy:1219277704277528586>",
    4: "<:cztery:1219277705300803680>",
    5: "<:pi:1219277706558963756>",
    6: "<:sze:1219277708467376128>",
    7: "<:siedem:1219277709579128843>",
    8: "<:osiem:1219277711172698113>",
    9: "<:dziewi:1219277712384856254>",
    10: "<:dziesi:1219277713525964860>"
}

@bot.command(description="Lets you see your level") 
async def level(ctx): 
    user_id = ctx.author.id
    xp = user_message_counts.get(user_id, 0)
    levelf = 0.3 * math.sqrt (xp)
    level = int(levelf)
    prcntf = (levelf - level) * 1000
    prcnt = (int(prcntf)) / 10
    fullbarsf = prcnt / 10
    fullbars = int(fullbarsf)
    bars = "<:dziesi:1219277713525964860>" * fullbars
    semibarf = prcnt - (fullbars*10)
    semibar = int(semibarf)
    selected_emoji = emoji_map[semibar]
    emptybarsno = 10 - fullbars -1
    emptybars = "<:zero:1219277173014270052>" * int(emptybarsno)
    await ctx.respond(f"You have {xp} xp \n That is level {level}! \n thats {prcnt}% of the way there to the next level\n{bars + selected_emoji + emptybars}")

# @bot.command(description="Counts the total number of messages sent by a user across all channels in the server.")
# async def count_all_messages(ctx, user: discord.Member):
#     message_count =  0
#     for channel in ctx.guild.channels:
#         if isinstance(channel, discord.TextChannel):  # Ensure we're only counting messages in text channels
#             async for message in channel.history(limit=None):  # Fetch all messages in the channel
#                 if message.author == user:
#                     message_count +=  1
#     await ctx.respond(f"{user.name} has sent {message_count} messages across all channels in this server.")

# @bot.command(description="Counts the total number of messages sent by a user in the current channel.")
# async def count_messages(ctx, user: discord.Member):
#     message_count =  0
#     async for message in ctx.channel.history(limit=None):
#         if message.author == user:
#             message_count +=  1
#     await ctx.respond(f"{user.name} has sent {message_count} messages in this channel.")

@bot.command(description="preview levels") 
async def levels(ctx): 
    await ctx.respond(f"# roles: \n <@&1207111158000263259> - level 10 \n <@&1207111456659742730> - level 20 \n <@&1207113962228023298> - level 30 \n <@&1207113104492863578> - level 40 \n <@&1207111046863785994> - level 60 \n <@&1207103055103926302> - level 80 \n <@&1207111660376948777> - level 90 \n <@&1205492582512332810> - level 100 \n <@&1207102955333882016>  - level 120 \n <@&1207112059796455434> - level 140")

@bot.command(description="check leaderboard")
async def top(ctx):
    sorted_users = sorted(user_message_counts.items(), key=lambda item: item[1], reverse=True)
    top_ten_users = sorted_users[:10]
    top_ten_strings = [f"<@{user}>: {score}" for user, score in top_ten_users]
    await ctx.respond("\n".join(top_ten_strings))

bot.run(PHOTOBOT_KEY)
