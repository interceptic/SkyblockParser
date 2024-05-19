import asyncio
import discord
from discord.ext import commands
from get_data.info import thingg
import json
import datetime

message_id = None
intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(intents=intents, slash_command_prefix='/')  

with open("config.json", "r") as conf:
    config = json.load(conf)

ALLOWED_USER_IDS = [config['ALLOWED_USER_IDS']]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Made by Interceptic"))
    await bot.sync_commands()
    await main()

@bot.slash_command(name='ign', description='Add or remove a user',)
async def ign(
    interaction: discord.Interaction,
    username: str,
    remove: bool,
):
    if interaction.author.id in ALLOWED_USER_IDS:
        if remove:
            if username in ign_list:
                ign_list.remove(username) 
                save_list()
                await interaction.response.send_message(f'Username "{username}" removed from the list.', ephemeral=True)
            else:
                await interaction.response.send_message(f'"{username}" not found in the list.', ephemeral=True)

        else:
            await interaction.response.send_message(f'Username "{username}" added to the list.', ephemeral=True)
            ign_list.append(username)
            save_list()
        return
    else:
        await interaction.response.send_message("Sorry, you don't have permission to run this command :( ", ephemeral=True)

@bot.slash_command(name='update', description='Update embed early',)
async def update(interaction: discord.Interaction):
    s = len(ign_list) * 20
    a = s / 60
    m = round(a)
    if m == 0:
        m = 1
    if interaction.author.id in ALLOWED_USER_IDS:    
        await interaction.response.send_message((f"Updating the embed with {ign_list}, please wait {m} minutes :)"), ephemeral=True)
        await update_message()
        return
    else:
        await interaction.response.send_message("Sorry, you don't have permission to run this command :( ", ephemeral=True)

@bot.slash_command(name='list', description ="What igns are currently in the list!")
async def list(interaction: discord.Interaction):
    if interaction.author.id in ALLOWED_USER_IDS:    
        await interaction.response.send_message((f"{ign_list}"), ephemeral=True)
    else:
        await interaction.response.send_message("Sorry, you don't have permission to run this command :( ", ephemeral=True)
def load_list():
    global ign_list
    try:
        with open("igns.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        pass 
ign_list = load_list()

        
def save_list():
    with open("igns.json", "w") as f:
        json.dump(ign_list, f)

async def main():
    if message_id is None:
        await send_embed()
    else:
        while True:
            try:
                await update_message()
            except Exception as e:
                print(e)
            await asyncio.sleep(1800)    


async def send_embed():
    global message_id
    if message_id is not None:
        await main()
    else: 
        embed = discord.Embed(
            title='The purse of your accounts: ',
            description='',
            color=0xFF4CAE,
            )
        for i in range(0, len(ign_list)):
            purse = await thingg(ign_list[i])
            if 'B' in purse:
                embed.add_field(name=f"{ign_list[i]} purse: \n {purse}", value='', inline=False)
            else:
                embed.add_field(name=f"{ign_list[i]} purse: \n {purse}", value='', inline=False)
        channel = bot.get_channel(config['CHANNEL'])
        embed.set_footer(text='Made by interceptic', icon_url='https://cdn.discordapp.com/avatars/1227394151847297148/a_17e8e189d32a91dc7a40f25a1ebcd9c0.webp?size=160')
        embed.timestamp = datetime.datetime.now()
        message = await channel.send(embed=embed)
        message_id = message.id
        print(message_id)
        return

async def update_message():
    channel = bot.get_channel(config['CHANNEL'])
    try:
        message = await channel.fetch_message(message_id)
        embed = discord.Embed(
            title='Updated purse of your accounts:',
            description='',
            color=0xFF4CAE,
        )
        for i in range(len(ign_list)):
            purse = await thingg(ign_list[i])
            if 'B' in purse:
                embed.add_field(name=f"{ign_list[i]} purse: \n {purse}", value='', inline=False)
            else:
                embed.add_field(name=f"{ign_list[i]} purse: \n{purse}", value='', inline=False)
        
        embed.set_footer(text='Made by interceptic', icon_url='https://cdn.discordapp.com/avatars/1227394151847297148/a_17e8e189d32a91dc7a40f25a1ebcd9c0.webp?size=160')
        embed.timestamp = datetime.datetime.now()

        await message.edit(embed=embed)
        print(f"Message with ID {message_id} has been updated")
    except discord.NotFound:
        print(f"Message with ID {message_id} not found")
    return



@bot.slash_command(name='purses', description='Purse of users')
async def purses(interaction: discord.Interaction):
    if interaction.author.id in ALLOWED_USER_IDS:       
        embed = discord.Embed(
                title='The purse of your accounts: ',
                description='',
                color=0xFF4CAE,
            )
        await interaction.response.send_message(f'Collecting data from api... please wait :D', ephemeral=True)
        for i in range(0, len(ign_list)):
            purse = await thingg(ign_list[i])
            if 'B' in purse:
                embed.add_field(name=f"{ign_list[i]} purse: \n{purse}", value='', inline=False)
            else:
                embed.add_field(name=f"{ign_list[i]} purse: \n{purse}", value='', inline=False)
        channel = interaction.channel
        embed.set_footer(text='Made by interceptic', icon_url='https://cdn.discordapp.com/avatars/1227394151847297148/a_17e8e189d32a91dc7a40f25a1ebcd9c0.webp?size=160')
        embed.timestamp = datetime.datetime.now()

        await channel.send(embed=embed)
        return
    else:
        await interaction.response.send_message("Sorry, you don't have permission to run this command :( ", ephemeral=True)

bot.run(config['TOKEN'])
bot.sync_commands()
