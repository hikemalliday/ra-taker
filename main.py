import os
import discord
from discord.ext import commands
from discord import app_commands
import logging
import traceback
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
REST_URI = os.getenv("REST_URI")
API_KEY = os.getenv("API_KEY")

NAMES_MAP = {
    "titanuk": "Titanuk",
    "silikten": "Silikten",
    "chestrockwell3419": "Big G",
    "saltycrackers": "Salty",
    "saltyn123": "Saltyn",
    "thors8694": "Mcoy",
    "balutlv": "Gream",
    "pok1858": "Pok",
    "grixus.": "Grixus",
    "hurl_": "Hurl",
    "goblin6644#0": "Last Boss",
    "noni3115": "Noni",
    "shinaba": "Shinaba",
    "shody123": "Shody",
    "ungh": "Ungh",
    "lethdar": "Lethdar",
    "leggomayne": "Heelah",
    "baronjune": "baronjune",
    "fatalwan": "Fatalwan",
    "keep__": "Keep",
    "nuke9859": "Nuke",
    "willan": "Willan",
    "kano4861": "Kano",
    "ksah": "Ksah",
    ".ziero": "Rayd(lieth)",
    "blueflower9": "Blueflower",
    "cythix.ip": "Kugaz",
    "koidokenmachete": "Machete",
    "cybercop": "Cybercop",
    "plag5944": "Sars",
    "noidia": "Noidz",
    "nba4400": "Nba",
    ".firenz": "Firenz",
    "ckombobreaker": "Ezpk",
    "mortii2940": "Mortii",
    "nocsucow": "Nocsucow",
    "ledbedder": "Ledbedder",
    "malagen": "Malagen",
    "knife8187": "Knife",
    "charming2340": "Charming",
    "lucidnpc": "Genedin",
    "rukmok": "Rukmok",
    "themerkd": "Gasoline",
    "vaporize1334": "Vaporise",
    "reptoid_sol": "Reptoid",
    "frodo4827": "Frodo",
    "metroyd.": "Metroyd",
    "deimos888": "Deimos",
    "strut": "Strut",
    "hazelnut0339": "Hazelnut",
    "in_spir_e": "Inspire",
    ".vantaris": "Violence",
    "krunchh.": "Krunchh",
    "bodied3": "Bodied",
    "birdop": "Birdop",
    "_sharknado": "Sharknado",
    "pnboots": "Boomwiz",
    "delune": "Delune",
    "tranch1144": "Tranch",
    "akp3533": "Kap",
    "blarg2k": "Blarg2k",
    "nuke4265": "Wisecrak",
    "hagard_69334": "Hagard",
    "skitter5007": "Skitter",
    "beihr": "Beihr",
    "boat6918": "boat",
    "darkhorn.": "darkhorn",
    "little8858": "Little",
    "nerfed1": "Nerfed",
    "kringe1060": "Kringe",
    "smooth7398": "Taquisha",
    "haydnt.": "Brobb",
    "godhandgu": "Tune",
    "ticeshotit": "Slimelord",
    "cornisthebest": "Mendl",
    ".faldorf": "Faldorf",
    "_visible": "Visible",
    "hyjal_": "Acarer",
    "biglimey": "Biglime",
    "lizard_eq99": "Shakirra",
    "goatassin": "Goatassin",
    "warlockezorn": "Zorn/Demonstab",
    "vanco_lash": "Vanco",
    "billieboyo": "Sangre",
    "durant2323": "Iovvdovvn",
    "producer": "Producer",
    "schnnow": "Jokong/Jessie",
    "aseplanker": "Azzar",
    "moochie.kitty": "Ninja",
    "uaeb": "Uaeb",
    "shivalry3pt": "Threepeat",
    "caldwillis": "Herban",
    "mochadrone1975": "Exam",
    "awakening6572": "Taeter",
    "lazzarus1969": "Herbsaint",
    "skeeter_": "Skeeter",
    "aygok": "Aygok",
    "o.g._mobbs": "Mandelgar",
    "rawbinurhood": "Rawbin",
    "jefu4791": "Jefu",
    "boogs1332": "Ohhso",
    "loritheandras": " Lori/Theandras",
    "re.ef": "Reef",
    "kajoo": "Kajoo",
    "bigr_": "Ajax",
    "pdunny": "Bannin/Haywire",
    "namji": "Partymike",
    "poopypants5181": "Reon",
    "amberr08053": "Amberr",
    "strikkerr": "Strikerr",
    "jore9716": "Ranjore",
    ".thievin": "Gram",
    "ginlok": "Rickjames",
}

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


@bot.tree.command(name="take_ra", description="Send the raid to approve for members in your voice channel")
@app_commands.describe(raid_name="Name of the raid")
async def take_ra(interaction: discord.Interaction, raid_name: str):
    try:
        user = interaction.user
        # Role check
        if not any(role.name == "Officers" for role in getattr(user, "roles", [])):
            return await interaction.response.send_message(
                "❌ You need the Officers role to use this command.", ephemeral=True
            )

        # Voice channel check
        if isinstance(user, discord.Member) and user.voice and user.voice.channel:
            voice_channel = user.voice.channel
            members = voice_channel.members
            rows = [[m.display_name, m.name] for m in members]

            payload = {
                "raid_name": raid_name,
                "players_list": rows
            }

            response = requests.post(
                REST_URI,
                json=payload,
                headers={"Authorization": f"Api-Key {API_KEY}"},
                # verify=False  # Disable SSL verification for expired cert
            )

            if response.status_code in (200, 201):
                await interaction.response.send_message(
                    f"✅ Success: 'raid to approve' `{raid_name}` has been sent to website"
                )
            else:
                await interaction.response.send_message(
                    "❌ Error: could not send 'raid to approve' to website, DM Grixus pls"
                )

            # Send the list of names as a follow-up
            names_to_show = [m.display_name for m in members]
            await interaction.followup.send("\n".join(names_to_show))
        else:
            await interaction.response.send_message("❌ You’re not in a voice channel.", ephemeral=True)
    except Exception as e:
        logger.exception("take_ra crashed")
        await interaction.response.send_message(f"❌ take_ra failed: `{e}`", ephemeral=True)


@bot.event
async def on_ready():
    await bot.tree.sync()
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


ALLOWED_ROLES = {"Officers", "Leader", "Comms"}


@bot.tree.command(name="mute", description="Mute everyone in your voice channel except Officers/Leader/Comms")
async def mute(interaction: discord.Interaction):
    try:
        user = interaction.user

        # Officer role check
        if not any(role.name == "Officers" for role in getattr(user, "roles", [])):
            return await interaction.response.send_message(
                "❌ You need the Officers role to use this command.", ephemeral=True
            )

        # Voice channel check
        if not (isinstance(user, discord.Member) and user.voice and user.voice.channel):
            return await interaction.response.send_message(
                "❌ You’re not in a voice channel.", ephemeral=True
            )

        voice_channel = user.voice.channel
        members = voice_channel.members

        muted = []
        skipped = []

        for m in members:
            # Skip privileged roles
            if any(r.name in ALLOWED_ROLES for r in m.roles):
                skipped.append(m.display_name)
                continue

            try:
                await m.edit(mute=True)
                muted.append(m.display_name)
            except Exception as e:
                logger.warning(f"Failed to mute {m.display_name}: {e}")

        msg = "🔇 **Muting complete:**\n"
        # msg += f"**Muted:** {', '.join(muted) if muted else 'None'}\n"
        # msg += f"**Skipped:** {', '.join(skipped) if skipped else 'None'}"

        await interaction.response.send_message(msg)

    except Exception as e:
        logger.exception("mute_ra crashed")
        await interaction.response.send_message(f"❌ mute_ra failed: `{e}`", ephemeral=True)



@bot.tree.command(name="unmute", description="Unmute everyone in your voice channel")
async def unmute(interaction: discord.Interaction):
    try:
        user = interaction.user

        # Officer role check
        if not any(role.name == "Officers" for role in getattr(user, "roles", [])):
            return await interaction.response.send_message(
                "❌ You need the Officers role to use this command.", ephemeral=True
            )

        # Voice channel check
        if not (isinstance(user, discord.Member) and user.voice and user.voice.channel):
            return await interaction.response.send_message(
                "❌ You’re not in a voice channel.", ephemeral=True
            )

        voice_channel = user.voice.channel
        members = voice_channel.members

        unmuted = []

        for m in members:
            try:
                await m.edit(mute=False)
                unmuted.append(m.display_name)
            except Exception as e:
                logger.warning(f"Failed to unmute {m.display_name}: {e}")

        await interaction.response.send_message(
            f"🔊 **Everyone unmuted."
        )

    except Exception as e:
        logger.exception("unmute_ra crashed")
        await interaction.response.send_message(f"❌ unmute_ra failed: `{e}`", ephemeral=True)


bot.run(BOT_TOKEN)
