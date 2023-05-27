import discord
import datetime
from const import INTENTS, TOKEN

client = discord.Client(intents=INTENTS)
tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    command_count = 0
    for commands in tree.walk_commands():
        command_count += 1
    print(f'Logged in as user: {client.user}')
    print(f'{command_count} commands have been synced.')


@tree.command(name='mute', description='Mutes a user.')
@discord.app_commands.checks.has_permissions(mute_members=True)
async def mute(interaction, user: discord.Member, time: str, reason: str=None):
    await interaction.response.defer()
    number = time[:-1]
    duration = time[-1:].lower()
    if duration == 's':
        duration = datetime.timedelta(seconds=int(number))
        time = f'{number} seconds.'
    elif duration == 'm':
        duration = datetime.timedelta(minutes=int(number))
        time = f'{number} minutes.'
    elif duration == 'h':
        duration = datetime.timedelta(hours=int(number))
        time = f'{number} hours.'
    elif duration == 'd':
        duration = datetime.timedelta(days=int(number))
        time = f'{number} days.'
    await user.timeout(duration, reason=reason+f' | Muted by {interaction.user}')
    await interaction.followup.send(f'User {user}, has been muted for {time}.\nReason: {reason}')


@tree.command(name='unmute', description='Unmute a user.')
@discord.app_commands.checks.has_permissions(mute_members=True)
async def mute(interaction, user: discord.Member):
    await user.timeout(datetime.timedelta(0))
    await interaction.followup.send(f'User {user}, has been unmuted.')    


@tree.command(name='kick', description='Kicks a user.')
@discord.app_commands.checks.has_permissions(kick_members=True)
async def ban(interaction, user: discord.Member, reason: str=None):
    await interaction.response.defer()   
    await user.kick(reason=reason+f' | Kicked by {interaction.user}')
    await interaction.followup.send(f'User {user}, has been kicked.\nReason: {reason}')


@tree.command(name='ban', description='Bans a user.')
@discord.app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction, user: discord.Member, reason: str):
    await interaction.response.defer()  
    await user.ban(reason=reason+f' | Banned by {interaction.user}')
    await interaction.followup.send(f'User {user}, has been banned.\nReason: {reason}')


@tree.command(name='unban', description='Unbans a user.')
@discord.app_commands.checks.has_permissions(ban_members=True)
async def unban_command(interaction, user_id: str):
    user_id = int(user_id)
    guild = interaction.guild
    user = await client.fetch_user(user_id)
    await guild.unban(user)
    await interaction.response.send_message(f'User ID {user_id} has been unbanned.')



client.run(TOKEN)