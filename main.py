import discord
from discord.ext import commands

GUILD_ID = "your_id"
VOICE_CHANNEL_ID = "your_id"

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = []
original_names = {}

@bot.event
async def on_ready():
    print(f'Bot ist eingeloggt als {bot.user}')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="Mascn.xyz"
    ))

@bot.event
async def on_voice_state_update(member, before, after):
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return

    if after.channel and after.channel.id == VOICE_CHANNEL_ID:
        if member.id not in queue:
            queue.append(member.id)
            if member.id not in original_names:
                original_names[member.id] = member.nick or member.name

    if before.channel and before.channel.id == VOICE_CHANNEL_ID and not after.channel:
        if member.id in queue:
            queue.remove(member.id)
        if member.id in original_names:
            try:
                await member.edit(nick=original_names[member.id])
            except discord.Forbidden:
                print(f"Kann den Nickname von {member} nicht zurücksetzen (fehlende Rechte).")
            del original_names[member.id]

    await update_nicknames(guild)

async def update_nicknames(guild):
    for index, user_id in enumerate(queue, start=1):
        member = guild.get_member(user_id)
        if member:
            try:
                original_nick = original_names.get(user_id, member.name)
                new_nick = f"({index}) {original_nick}"
                await member.edit(nick=new_nick)
            except discord.Forbidden:
                print(f"Kann den Nickname von {member} nicht ändern (fehlende Rechte).")

bot.run("your_token")
