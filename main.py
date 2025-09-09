import discord
from discord.ext import commands
from config import BOT_TOKEN, NAMES_MAP

# Intents are required for member info
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

@bot.command()
async def take_ra(ctx):
    """Output all player names in channel."""
    if ctx.author.voice:
        voice_channel = ctx.author.voice.channel
        members = voice_channel.members
        rows = []

        for m in members:
            output_name = NAMES_MAP.get(m.name, m.display_name)
            rows.append(output_name)

        results = "\n".join(rows)

        await ctx.send(results)
    else:
        await ctx.send("❌ You’re not in a voice channel.")


@bot.command()
async def get_all_names(ctx):
    """Outputs all names associated to members in channel"""
    if ctx.author.voice:
        voice_channel = ctx.author.voice.channel
        members = voice_channel.members

        rows = [f"{m.display_name}\t{m.name}#{m.discriminator}" for m in members]
        results = "\n".join(rows)

        await ctx.send(results)
    else:
        await ctx.send("❌ You’re not in a voice channel.")


bot.run(BOT_TOKEN)
