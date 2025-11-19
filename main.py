import discord
from discord.ext import commands
import logging
import traceback
import requests
from config import BOT_TOKEN, NAMES_MAP, REST_URI, API_KEY

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
    # Silently ignore ANY command that doesn't exist
    if isinstance(error, commands.CommandNotFound):
        return  # ← Silent fail for all unknown commands

    # Only log + report REAL errors (permissions, crashes, etc.)
    tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
    logger.error(f"Command error '{ctx.invoked_with}': {error}\n{tb}")
    await ctx.send(f"Error: `{error}`")


@bot.command()
@commands.has_role("Officers")
async def take_ra(ctx):
    try:
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            members = voice_channel.members
            rows = [NAMES_MAP.get(m.name, m.display_name) for m in members]
            await ctx.send("\n".join(rows))
            await ctx.send(rows)
        else:
            await ctx.send("❌ You’re not in a voice channel.")
    except Exception as e:
        logger.exception("take_ra crashed")
        await ctx.send(f"❌ take_ra failed: `{e}`")


@bot.command()
@commands.has_role("Officers")
async def take_ra_and_post(ctx):
    try:
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            members = voice_channel.members
            rows = [NAMES_MAP.get(m.name, m.display_name) for m in members]
            response = requests.post(
                REST_URI,
                data={"players_list": rows},
                headers={
                    "Api-Key": API_KEY,
                }
            )
            if response.status_code in (200, 201):
                await ctx.send("Success: 'raid to approve' has been sent to website ✔")
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


@bot.command()
@commands.has_role("Officers")
async def take_all(ctx):
    """Collects all members from all voice channels, excluding AFK"""
    try:
        guild = ctx.guild
        afk_channel = guild.afk_channel  # AFK channel can be None if not set

        collected_members = []

        for channel in guild.voice_channels:
            if afk_channel and channel.id == afk_channel.id:
                continue  # skip AFK channel

            for member in channel.members:
                collected_members.append(NAMES_MAP.get(member.name, member.display_name))

        if collected_members:
            await ctx.send("\n".join(collected_members))
        else:
            await ctx.send("❌ No members found in any non-AFK voice channels.")
    except Exception as e:
        logger.exception("take_all crashed")
        await ctx.send(f"❌ take_all failed: `{e}`")


bot.run(BOT_TOKEN)
