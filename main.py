import discord
from discord.ext import commands
import logging
import traceback
from config import BOT_TOKEN, NAMES_MAP

logging.basicConfig(
    level=logging.INFO,  # INFO or DEBUG for more detail
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("/app/logs/bot.log", encoding="utf-8"),  # writes to a file inside container
        logging.StreamHandler()  # also prints to Docker logs
    ]
)

logger = logging.getLogger("discord_bot")

# Intents are required for member info
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    logger.info(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")


# Global error handler
@bot.event
async def on_command_error(ctx, error):
    error_text = "".join(traceback.format_exception(type(error), error, error.__traceback__))
    logger.error(f"Error in command {ctx.command}:\n{error_text}")
    await ctx.send(f"❌ Error: `{error}`")


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
async def take_ra(ctx):
    try:
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            members = voice_channel.members
            rows = [NAMES_MAP.get(m.name, m.display_name) for m in members]
            await ctx.send("\n".join(rows))
        else:
            await ctx.send("❌ You’re not in a voice channel.")
    except Exception as e:
        logger.exception("take_ra crashed")
        await ctx.send(f"❌ take_ra failed: `{e}`")


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
