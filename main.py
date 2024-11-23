import os
import sys
import asyncio
import json
import re
import aiohttp
import discord
import datetime
import logging
import random
import requests
from discord.ext import commands
from tenacity import retry, stop_after_attempt, wait_fixed
from logging.handlers import RotatingFileHandler

# Utility functions
def uninstall_and_install():
    os.system(
        "pip uninstall discord -y && pip uninstall discord.py -y && pip uninstall discord.py-self -y && pip install -r requirements.txt"
    )

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def restart_script():
    log("Restarting script due to hard error...", save=True)
    try:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except OSError as e:
        log(f"Failed to restart script: {e}", save=True)
        sys.exit(1)

def is_blacklisted(user_id):
    return str(user_id) in BOT_BLACKLIST or (client.user and user_id == client.user.id)

def log(content, do_everyone=False, save=False):
    if save:
        logging.info(content)
    if do_everyone:
        content = f"@everyone {content}"
    print(f"[!] LOG: {content}")

# Run the uninstall and install on startup
uninstall_and_install()
clear_console()

# Set up Discord API base URL
BASE_URL = "https://discord.com/api/v9"

# Load config data
def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        log("Configuration file not found. Exiting...", save=True)
        sys.exit(1)
    except json.JSONDecodeError:
        log("Invalid JSON format in config file. Exiting...", save=True)
        sys.exit(1)

config_data = load_config()

# Extracting configuration
TOKEN = config_data.get("Token", [None])[0]  # Extract the token from the list
WEBHOOK = config_data.get("Webhook")
BOT_BLACKLIST = set(config_data.get("BotBlacklist", []))
WEBHOOK_NOTIFICATION = config_data.get("WebhookNotification", True)  # Set default to True if not specified

if not TOKEN:
    raise ValueError("Discord bot token is not set in config.json")

# Set up logging
log_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log_file_handler = RotatingFileHandler('logs.txt', maxBytes=5 * 1024 * 1024, backupCount=5)  # 5MB per file, up to 5 backups
log_file_handler.setFormatter(log_formatter)
logging.basicConfig(level=logging.INFO, handlers=[log_file_handler])

# User-Agent list to avoid detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]

# Random hardware identifiers to avoid detection
DEVICE_IDS = [
    "a1b2c3d4e5f6g7h8i9j0",
    "098f6bcd4621d373cade4e832627b4f6",
    "e5b3d9c7a1f8h2g4i0j7k6l5m9n8o3p1",
    "d41d8cd98f00b204e9800998ecf8427e",
    "1a2b3c4d5e6f7g8h9i0jklmnopqrstu"
]

# Extra headers for stealth
HEADERS_EXTRA = [
    "X-Super-Properties",
    "X-Fingerprint",
    "X-Debug-Options"
]

# Nitro Sniper Settings (do not extract these settings from the script)
NITRO_SETTINGS = {
    "max_snipes": 5,
    "cooldown_time": 3600  # 1 hour cooldown
}

@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
async def send_webhook_notification(title, description, content="", color=16732345, footer_text="Giveaway Sniper", avatar_url="https://i.imgur.com/44N46up.gif"):
    if WEBHOOK_NOTIFICATION and WEBHOOK:
        data = {
            "content": content,
            "embeds": [{
                "title": title,
                "description": description,
                "color": color,
                "footer": {"text": footer_text}
            }],
            "username": "Giveaway Sniper",
            "avatar_url": avatar_url
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(WEBHOOK, json=data) as response:
                if response.status != 204:
                    log(f"Failed to send webhook notification: {response.status} - {await response.text()}", save=True)

async def NitroInfo(elapsed, code, status):
    log(f"Elapsed: {elapsed}, Code: {code}, Status: {status}")
    await send_webhook_notification(
        title="🔑 Nitro Code Redemption Status",
        description=f"**Elapsed Time:** `{elapsed}` seconds\n**Code:** `{code}`\n**Status:** {status}",
        content="@everyone" if status == "Successfully redeemed" else "",
        color=3447003,  # Blue color
        footer_text="Nitro Sniper | Status Update",
        avatar_url="https://i.imgur.com/nitro-icon.png"
    )

async def GiveawayInfo(message, action, location, author):
    log(f"Sniped a giveaway! {action} Reaction | Location: {location} | Author: {author}")
    await send_webhook_notification(
        title="🎁 Giveaway Sniped!",
        description=f"**Action Taken:** {action}\n**Location:** `{location}`\n**Hosted by:** {author}\n[Click Here to View Message]({message.jump_url})",
        color=15844367,  # Orange color
        footer_text="Giveaway Sniper | Action Report",
        avatar_url="https://i.imgur.com/giveaway-icon.png"
    )

async def GiveawayWinInfo(message, prize, location, author):
    log(f"Detected Giveaway Win! Prize: {prize} | Location: {location} | Author: {author} [Click Here]({message.jump_url})", do_everyone=True, save=True)
    await send_webhook_notification(
        title=f"🏆 Giveaway Win: {prize}",
        description=f"**Congratulations!** You've won a giveaway for **{prize}**!\n**Location:** `{location}`\n**Hosted by:** {author}\n[Click Here to View Winning Message]({message.jump_url})",
        content="@everyone",
        color=3066993,  # Green color
        footer_text="Giveaway Win | Notification",
        avatar_url="https://i.imgur.com/win-icon.png"
    )

async def BotConnectedInfo(user):
    log(f"Giveaway Sniper is connected to | user: {user.name} | id: {user.id}")
    await send_webhook_notification(
        title="✅ Bot Successfully Connected",
        description=f"**Giveaway Sniper is now connected.**\n**User:** `{user.name}`\n**ID:** `{user.id}`",
        color=8311585,  # Purple color
        footer_text="Connection Status",
        avatar_url="https://i.imgur.com/connected-icon.png"
    )

@retry(stop=stop_after_attempt(3), wait=wait_fixed(5)
async def redeem_nitro_code(token, code):
    url = f"{BASE_URL}/entitlements/gift-codes/{code}/redeem"
    headers = {
        "Authorization": f"{token}",
        "User-Agent": random.choice(USER_AGENTS),
        "X-Super-Properties": random.choice(DEVICE_IDS),
        "X-Fingerprint": random.choice(DEVICE_IDS),
        "X-Debug-Options": "bugReporterEnabled",
        "Content-Type": "application/json"  # Add this line
    }
    start_time = datetime.datetime.now()

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json={}) as response:  # Use `json={}` instead of `data=`
            elapsed = datetime.datetime.now() - start_time
            elapsed_str = f'{elapsed.seconds}.{elapsed.microseconds}'
            status = response.status

            if response.status == 429:  # Rate limited
                retry_after = int(response.headers.get("Retry-After", 60))
                log(f"Rate limited, retrying in {retry_after} seconds...")
                await asyncio.sleep(retry_after)
                await redeem_nitro_code(token, code)
                return

            try:
                res_json = await response.json()
            except Exception as e:
                log(f"Failed to parse response JSON: {e}")
                await NitroInfo(elapsed_str, code, f"Failed to parse response JSON: {e}")
                return

            if res_json.get('message', '').lower() == 'unknown gift code':
                log(f"Invalid Nitro code: {code}")
                await NitroInfo(elapsed_str, code, "Invalid Nitro code")
            elif 'subscription_plan' in res_json:
                log(f"Successfully redeemed Nitro code: {code}")
                await NitroInfo(elapsed_str, code, "Successfully redeemed")
            elif res_json.get('message', '').lower() == 'this gift has been redeemed already':
                log(f"Code already redeemed: {code}")
                await NitroInfo(elapsed_str, code, "Code already redeemed")
            elif 'retry_after' in res_json:
                retry_after = res_json['retry_after'] / 1000  # Convert ms to seconds
                log(f"Rate limited, retrying in {retry_after} seconds...")
                await asyncio.sleep(retry_after)
                await redeem_nitro_code(token, code)
            else:
                log(f"Unexpected response while redeeming Nitro code {code}: {res_json}")
                await NitroInfo(elapsed_str, code, f"Unexpected response: {res_json}")




async def check_nitro_codes(message):
    if any(x in message.content.lower() for x in ["discord.gift/", "discordapp.com/gifts/", "discord.com/gifts/"]):
        codes = re.findall(r"discord(?:\.gift|\.com\/gifts|\.app\.com\/gifts)\/([a-zA-Z0-9]+)", message.content)
        if len(codes) > NITRO_SETTINGS['max_snipes']:
            codes = codes[:NITRO_SETTINGS['max_snipes']]  # Limiting to max allowed snipes

        # Initialize usedcodes if the file does not exist
        if not os.path.exists("tried-nitro-codes.txt"):
            with open("tried-nitro-codes.txt", "w") as fp:
                json.dump([], fp)

        with open("tried-nitro-codes.txt", "r") as fp:
            usedcodes = json.load(fp)

        for code in codes:
            if len(code) in [16, 24] and code not in usedcodes:
                usedcodes.append(code)
                with open("tried-nitro-codes.txt", "w") as fp:
                    json.dump(usedcodes, fp)
                try:
                    await redeem_nitro_code(TOKEN, code)
                except Exception as e:
                    log(f"Error redeeming nitro code {code}: {e}")

async def handle_giveaway_reaction(message):
    delay = random.uniform(15, 30)  # Random delay to prevent detection
    await asyncio.sleep(delay)
    try:
        if message and message.guild and message.author:
            location = f"Server: {message.guild.name} | Channel: {message.channel.name}"
            author = message.author.name

            if message.components and message.components[0].children:
                button = message.components[0].children[0]
                if button and hasattr(button, 'click') and button.type == discord.ComponentType.button and button.style in [discord.ButtonStyle.primary, discord.ButtonStyle.success]:
                    await button.click()
                    await GiveawayInfo(message, "Clicked Button", location, author)
            else:
                for reaction in message.reactions:
                    if str(reaction.emoji) == "🎉":
                        await message.add_reaction("🎉")
                        await GiveawayInfo(message, "Reacted with Emoji", location, author)
    except Exception as e:
        log(f"Error handling giveaway reaction: {e}")

async def detect_giveaway_win_message(message):
    keywords = ["won", "winner", "congratulations", "victory"]
    if client.user is None or message.guild is None or message.author is None:
        return

    def check_content(content):
        return any(keyword in content.lower() for keyword in keywords) and client.user.mention in content

    prize = "Unknown Prize"
    prize_match = re.search(r"prize[:\-\s]+(.+?)(\.|\n|$)", message.content, re.IGNORECASE)
    if prize_match:
        prize = prize_match.group(1).strip()

    for embed in message.embeds:
        embed_dict = embed.to_dict()
        for key, value in embed_dict.items():
            if isinstance(value, str):
                if "prize" in value.lower():
                    prize_match = re.search(r"prize[:\-\s]+(.+?)(\.|\n|$)", value, re.IGNORECASE)
                    if prize_match:
                        prize = prize_match.group(1).strip()
                if check_content(value):
                    location = f"Server: {message.guild.name} | Channel: {message.channel.name}"
                    author = message.author.name
                    await GiveawayWinInfo(message, prize, location, author)
                    return

    location = f"Server: {message.guild.name} | Channel: {message.channel.name}"
    author = message.author.name

    if check_content(message.content) or any(
        check_content(embed.to_dict().get("description", "")) or
        any(check_content(value) for key, value in embed.to_dict().items() if isinstance(value, str))
        for embed in message.embeds
    ):
        # Attempt to get the original giveaway join message
        if message.reference:
            join_message = await message.channel.fetch_message(message.reference.message_id)
            join_prize_match = re.search(r"prize[:\-\s]+(.+?)(\.|\n|$)", join_message.content, re.IGNORECASE)
            if join_prize_match:
                prize = join_prize_match.group(1).strip()
            await notify_giveaway_creator(message, prize, join_message)
        await GiveawayWinInfo(message, prize, location, author)

async def check_giveaway_message(message):
    if message.guild is None or message.author is None:
        return
    keywords = [
        "giveaway", "Ends at", "Hosted by", ":gift:", ":tada:", "**giveaway**",
        "🎉", "Winners:", "Entries:", "ends:"
    ]

    def contains_keyword(content):
        return any(keyword in content.lower() for keyword in keywords)

    # Check for keywords in message content and embeds
    if contains_keyword(message.content) or any(
        contains_keyword(embed.to_dict().get("description", "")) or
        contains_keyword(embed.to_dict().get("title", "")) or
        any(contains_keyword(value) for key, value in embed.to_dict().items() if isinstance(value, str))
        for embed in message.embeds
    ):
        await handle_giveaway_reaction(message)

# Discord Selfbot Setup
client = commands.Bot(command_prefix=";", help_command=None, self_bot=True)

@client.event
async def on_ready():
    if client.user is not None:
        log(f"Giveaway Sniper is connected to | user: {client.user.name} | id: {client.user.id}")
        await BotConnectedInfo(client.user)

@client.event
async def on_message(message):
    if message.author is None:
        return

    tasks = [
        check_nitro_codes(message),
        detect_giveaway_win_message(message),
    ]

    # Only check giveaways if the author is a bot and not blacklisted
    if message.author.bot and not is_blacklisted(message.author.id):
        tasks.append(check_giveaway_message(message))

    await asyncio.gather(*tasks)

def main():
    try:
        client.run(TOKEN, reconnect=True)
    except discord.errors.LoginFailure:
        log("Improper token has been passed or two-factor authentication is required. Please check the token in config.json.", save=True)
        handle_two_factor_auth()
    except Exception as e:
        log(f"An error occurred while starting the bot: {e}", save=True)
        restart_script()

def handle_two_factor_auth():
    two_factor_code = input("Enter the two-factor authentication code: ")
    if two_factor_code:
        try:
            client.run(TOKEN, reconnect=True, password=two_factor_code)
        except discord.errors.LoginFailure:
            log("Failed to login with the provided two-factor authentication code. Exiting.", save=True)
            sys.exit(1)
        except Exception as e:
            log(f"An error occurred while handling two-factor authentication: {e}", save=True)
            restart_script()

if __name__ == "__main__":
    main()
