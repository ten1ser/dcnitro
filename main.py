import os
from dotenv import load_dotenv
import json
from server import keep_alive

keep_alive()
load_dotenv()

discord_token = os.getenv('Token')
webhook_url = os.getenv('Webhook')

with open('config.json', 'r') as f:
    config = json.load(f)

def run_command(command: str):
    """Runs a shell command."""
    try:
        os.system(command)
    except Exception as e:
        log(f"Failed to run command '{command}': {e}", save=True, level=logging.ERROR)

def clear_console():
    """Clears the console."""
    os.system("cls" if os.name == "nt" else "clear")

# Run uninstall and install command before importing other libraries
run_command("pip uninstall discord discord.py discord.py-self -y && pip install -r requirements.txt")

clear_console()

import sys
import asyncio
import json
import re
import aiohttp
import discord
import datetime
import logging
import random
import dataclasses
from discord.ext import commands
from tenacity import retry, stop_after_attempt, wait_exponential
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, List, Union
import platform

# Configuration Management
@dataclasses.dataclass
class Config:
    token: str
    webhook: Optional[str]
    bot_blacklist: List[str]
    webhook_notification: bool
    user_agents: List[str]
    device_ids: List[str]
    nitro_settings: Dict[str, Union[int, float]]

    @staticmethod
    def load_config(filepath: str = "config.json") -> 'Config':
        try:
            with open(filepath, "r", encoding='utf-8') as f:
                data = json.load(f)
                return Config(
                    token=data.get("Token", [None])[0],
                    webhook=data.get("Webhook"),
                    bot_blacklist=data.get("BotBlacklist", []),
                    webhook_notification=data.get("WebhookNotification", True),
                    user_agents=data.get("UserAgents", []),
                    device_ids=data.get("DeviceIds", []),
                    nitro_settings=data.get("NitroSettings", {})
                )
        except (FileNotFoundError, json.JSONDecodeError) as e:
            log(f"Configuration file error: {e}. Exiting...", save=True, level=logging.ERROR)
            sys.exit(1)

# Load config data from config.json
config = Config.load_config()

# Utility functions
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=60))
def run_command(command: str):
    """Runs a shell command."""
    try:
        os.system(command)
    except Exception as e:
        log(f"Failed to run command '{command}': {e}", save=True, level=logging.ERROR)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=60))
def clear_console():
    """Clears the console."""
    os.system("cls" if os.name == "nt" else "clear")

async def restart_script():
    """Restarts the current script."""
    log("Restarting script due to hard error...", save=True)
    try:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except OSError as e:
        log(f"Failed to restart script: {e}", save=True, level=logging.ERROR)
        sys.exit(1)

def is_blacklisted(user_id: int) -> bool:
    """Checks if a user is blacklisted."""
    return str(user_id) in config.bot_blacklist or (client.user and user_id == client.user.id)

def log(content: str, notify_everyone: bool = False, save: bool = False, level: int = logging.INFO):
    """Logs content, optionally notifying everyone and saving to a file."""
    formatted_content = f"[!] LOG: {content}"
    if save:
        logging.log(level, formatted_content)
    if notify_everyone:
        formatted_content = f"@everyone {formatted_content}"
    try:
        print(formatted_content)
    except UnicodeEncodeError:
        print(formatted_content.encode('utf-8', errors='ignore').decode('utf-8'))

async def send_webhook_notification(title: str, description: str, content: str = "", color: int = 16732345, footer_text: str = "Giveaway Sniper", avatar_url: str = "https://i.imgur.com/44N46up.gif"):
    """Sends a notification to a webhook."""
    if config.webhook_notification and config.webhook:
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
            try:
                async with session.post(config.webhook, json=data) as response:
                    if response.status != 204:
                        log(f"Failed to send webhook notification: {response.status} - {await response.text()}", save=True, level=logging.ERROR)
            except aiohttp.ClientError as e:
                log(f"Failed to send webhook notification due to network error: {e}", save=True, level=logging.ERROR)

# Set up logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log_file_handler = RotatingFileHandler('logs.txt', maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8')
log_file_handler.setFormatter(log_formatter)
logging.basicConfig(level=logging.INFO, handlers=[log_file_handler])

# User-Agent list to avoid detection
ALL_USER_AGENTS = config.user_agents

# Random hardware identifiers to avoid detection
DEVICE_IDS = config.device_ids

# Nitro Sniper Settings
NITRO_SETTINGS = config.nitro_settings

# Discord Selfbot Setup
client = commands.Bot(command_prefix=";", help_command=None, self_bot=True)

@client.event
async def on_ready():
    if client.user is not None:
        log(f"Giveaway Sniper is connected to | user: {client.user.name} | id: {client.user.id}")
        await BotConnectedInfo(client.user)

@client.event
async def on_message(message: discord.Message):
    if message.author is None:
        return

    await handle_message_tasks(message)

async def handle_message_tasks(message: discord.Message):
    tasks = [
        handle_nitro_codes(message),
        handle_giveaway_win_message(message),
        handle_bot_message(message)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            log(f"Error during task execution: {result}", save=True, level=logging.ERROR)

async def handle_bot_message(message: discord.Message):
    if message.author.bot and not is_blacklisted(message.author.id):
        await check_giveaway_message(message)

async def handle_nitro_codes(message: discord.Message):
    await check_nitro_codes(message)

async def handle_giveaway_win_message(message: discord.Message):
    await detect_giveaway_win_message(message)

async def NitroInfo(elapsed: str, code: str, status: str):
    """Logs Nitro redemption information and sends a webhook notification."""
    log(f"Elapsed: {elapsed}, Code: {code}, Status: {status}")
    await send_webhook_notification(
        title="🔑 Nitro Code Redemption Status",
        description=f"**Elapsed Time:** `{elapsed}` seconds\n**Code:** `{code}`\n**Status:** {status}",
        content="@everyone" if status == "Successfully redeemed" else "",
        color=3447003,
        footer_text="Nitro Sniper | Status Update",
        avatar_url="https://i.imgur.com/nitro-icon.png"
    )

async def GiveawayInfo(message: discord.Message, action: str, location: str, author: str):
    """Logs giveaway action information and sends a webhook notification."""
    log(f"Sniped a giveaway! {action} Reaction | Location: {location} | Author: {author}")
    await send_webhook_notification(
        title="🎁 Giveaway Sniped!",
        description=f"**Action Taken:** {action}\n**Location:** `{location}`\n**Hosted by:** {author}\n[Click Here to View Message]({message.jump_url})",
        color=15844367,
        footer_text="Giveaway Sniper | Action Report",
        avatar_url="https://i.imgur.com/giveaway-icon.png"
    )

async def GiveawayWinInfo(message: discord.Message, prize: str, location: str, author: str, giveaway_host: Optional[discord.Member]):
    """Logs giveaway win information and sends a webhook notification."""
    if not prize:
        prize = "Unknown Prize"
    log(f"Detected Giveaway Win! Prize: {prize} | Location: {location} | Author: {author} [Click Here]({message.jump_url})", notify_everyone=True, save=True, level=logging.INFO)
    await send_webhook_notification(
        title=f"🏆 Giveaway Win: {prize}",
        description=f"**Congratulations!** You've won a giveaway for **{prize}**!\n**Location:** `{location}`\n**Hosted by:** {author}\n[Click Here to View Winning Message]({message.jump_url})",
        content="@everyone",
        color=3066993,
        footer_text="Giveaway Win | Notification",
        avatar_url="https://i.imgur.com/win-icon.png"
    )
    await send_direct_message(prize, location, author, giveaway_host)

async def send_direct_message(prize: str, location: str, author: str, giveaway_host: Optional[discord.Member]):
    """Sends a direct message to the giveaway host."""
    try:
        if giveaway_host is not None and giveaway_host.id != client.user.id:
            await giveaway_host.send(f"🎉 Your giveaway for **{prize}** has been won!\n**Location:** {location}\n**Winner:** {author}")
    except discord.Forbidden:
        log("Failed to send direct message due to insufficient permissions.", save=True, level=logging.ERROR)
    except discord.HTTPException as e:
        log(f"Failed to send direct message: {e}", save=True, level=logging.ERROR)

async def BotConnectedInfo(user: discord.User):
    """Logs bot connection information and sends a webhook notification."""
    log(f"Giveaway Sniper is connected to | user: {user.name} | id: {user.id}")
    await send_webhook_notification(
        title="✅ Bot Successfully Connected",
        description=f"**Giveaway Sniper is now connected.**\n**User:** `{user.name}`\n**ID:** `{user.id}`",
        color=8311585,
        footer_text="Connection Status",
        avatar_url="https://i.imgur.com/connected-icon.png"
    )

async def redeem_nitro_code(token: str, code: str):
    """Attempts to redeem a Nitro code."""
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}/redeem"
    headers = {
        "Authorization": token,
        "User-Agent": random.choice(ALL_USER_AGENTS),
        "X-Super-Properties": random.choice(DEVICE_IDS),
        "X-Fingerprint": random.choice(DEVICE_IDS),
        "X-Debug-Options": "bugReporterEnabled",
        "Content-Type": "application/json"
    }
    start_time = datetime.datetime.now()

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json={}) as response:
                elapsed = datetime.datetime.now() - start_time
                elapsed_str = f'{elapsed.seconds}.{elapsed.microseconds}'

                if response.status == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    log(f"Rate limited, retrying in {retry_after} seconds...", level=logging.WARNING)
                    await asyncio.sleep(retry_after)
                    await redeem_nitro_code(token, code)
                    return

                try:
                    res_json = await response.json()
                except Exception as e:
                    log(f"Failed to parse response JSON: {e}", level=logging.ERROR)
                    await NitroInfo(elapsed_str, code, f"Failed to parse response JSON: {e}")
                    return

                if res_json.get('message', '').lower() == 'unknown gift code':
                    log(f"Invalid Nitro code: {code}", level=logging.WARNING)
                    await NitroInfo(elapsed_str, code, "Invalid Nitro code")
                elif 'subscription_plan' in res_json:
                    log(f"Successfully redeemed Nitro code: {code}", level=logging.INFO)
                    await NitroInfo(elapsed_str, code, "Successfully redeemed")
                elif res_json.get('message', '').lower() == 'this gift has been redeemed already':
                    log(f"Code already redeemed: {code}", level=logging.INFO)
                    await NitroInfo(elapsed_str, code, "Code already redeemed")
                elif 'retry_after' in res_json:
                    retry_after = res_json['retry_after'] / 1000
                    log(f"Rate limited, retrying in {retry_after} seconds...", level=logging.WARNING)
                    await asyncio.sleep(retry_after)
                    await redeem_nitro_code(token, code)
                else:
                    log(f"Unexpected response while redeeming Nitro code {code}: {res_json}", level=logging.ERROR)
                    await NitroInfo(elapsed_str, code, f"Unexpected response: {res_json}")
        except aiohttp.ClientError as e:
            log(f"Network error while redeeming Nitro code {code}: {e}", level=logging.ERROR)

async def check_nitro_codes(message: discord.Message):
    """Checks a message for Nitro codes and attempts to redeem them."""
    if any(x in message.content.lower() for x in ["discord.gift/", "discordapp.com/gifts/", "discord.com/gifts/"]):
        codes = re.findall(r"discord(?:\.gift|\.com\/gifts|\.app\.com\/gifts)\/([a-zA-Z0-9]+)", message.content)
        if len(codes) > NITRO_SETTINGS['max_snipes']:
            codes = codes[:NITRO_SETTINGS['max_snipes']]

        if not os.path.exists("tried-nitro-codes.txt"):
            with open("tried-nitro-codes.txt", "w", encoding='utf-8') as fp:
                json.dump([], fp)

        with open("tried-nitro-codes.txt", "r", encoding='utf-8') as fp:
            usedcodes = json.load(fp)

        for code in codes:
            if len(code) in [16, 24] and code not in usedcodes:
                usedcodes.append(code)
                with open("tried-nitro-codes.txt", "w", encoding='utf-8') as fp:
                    json.dump(usedcodes, fp)
                try:
                    await redeem_nitro_code(config.token, code)
                except Exception as e:
                    log(f"Error redeeming nitro code {code}: {e}", level=logging.ERROR)

async def handle_giveaway_reaction(message: discord.Message):
    """Handles reacting to giveaway messages."""
    delay = random.uniform(10, 20)
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
    except discord.HTTPException as e:
        log(f"HTTP error handling giveaway reaction: {e}", level=logging.ERROR)
    except Exception as e:
        log(f"Error handling giveaway reaction: {e}", level=logging.ERROR)

async def detect_giveaway_win_message(message: discord.Message):
    """Detects messages indicating a giveaway win."""
    keywords = ["won", "winner", "congratulations", "victory"]
    if client.user is None or message.guild is None or message.author is None:
        return

    def check_content(content: str) -> bool:
        return any(keyword in content.lower() for keyword in keywords) and client.user.mention in content

    prize = "Unknown Prize"
    prize_match = re.search(r"prize[:\-\s]+(.+?)(\.|\n|$)", message.content, re.IGNORECASE)
    if prize_match:
        prize = prize_match.group(1).strip()

    giveaway_host = None
    location = f"Server: {message.guild.name} | Channel: {message.channel.name}"
    author = message.author.name

    if message.reference:
        try:
            join_message = await message.channel.fetch_message(message.reference.message_id)
            hosted_by_match = re.search(r"(hosted by|hosted|by) @?([\w\s]+)", join_message.content, re.IGNORECASE)
            if hosted_by_match:
                host_username = hosted_by_match.group(2).strip()
                for member in message.guild.members:
                    if member.name == host_username or member.display_name == host_username:
                        giveaway_host = member
                        break
        except discord.NotFound:
            log(f"Referenced message not found for message ID: {message.reference.message_id}", level=logging.WARNING)
        except discord.Forbidden:
            log(f"Permission denied to fetch referenced message ID: {message.reference.message_id}", level=logging.WARNING)
        except Exception as e:
            log(f"Error fetching referenced message: {e}", level=logging.ERROR)

    for embed in message.embeds:
        embed_dict = embed.to_dict()
        for key, value in embed_dict.items():
            if isinstance(value, str):
                if "prize" in value.lower():
                    prize_match = re.search(r"prize[:\-\s]+(.+?)(\.|\n|$)", value, re.IGNORECASE)
                    if prize_match:
                        prize = prize_match.group(1).strip()
                if check_content(value):
                    await GiveawayWinInfo(message, prize, location, author, giveaway_host)
                    return

    if check_content(message.content) or any(
        check_content(embed.to_dict().get("description", "")) or
        check_content(embed.to_dict().get("title", "")) or
        any(check_content(value) for key, value in embed.to_dict().items() if isinstance(value, str))
        for embed in message.embeds
    ):
        await GiveawayWinInfo(message, prize, location, author, giveaway_host)

async def check_giveaway_message(message: discord.Message):
    """Checks messages for giveaway indications and triggers reaction handling."""
    if message.guild is None or message.author is None:
        return
    keywords = [
        "giveaway", "Ends at", "Hosted by", ":gift:", ":tada:", "**giveaway**",
        "🎉", "Winners:", "Entries:", "ends:"
    ]

    def contains_keyword(content: str) -> bool:
        return any(keyword in content.lower() for keyword in keywords)

    if contains_keyword(message.content) or any(
        contains_keyword(embed.to_dict().get("description", "")) or
        contains_keyword(embed.to_dict().get("title", "")) or
        any(contains_keyword(value) for key, value in embed.to_dict().items() if isinstance(value, str))
        for embed in message.embeds
    ):
        await handle_giveaway_reaction(message)

# Main Function
def main():
    # Set the SelectorEventLoop on Windows to avoid compatibility issues with aiodns
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        client.run(config.token, reconnect=True)
    except discord.errors.LoginFailure:
        log("Improper token has been passed or two-factor authentication is required. Please check the token in config.json.", save=True, level=logging.ERROR)
    except Exception as e:
        log(f"An error occurred while starting the bot: {e}", save=True, level=logging.ERROR)
        asyncio.run(restart_script())

if __name__ == "__main__":
    # Set the encoding of stdout to utf-8 to handle console output
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
    main()
