# Discord Giveaway and Nitro Sniper Selfbot

## Overview
This is a Discord selfbot script designed to participate in giveaways and attempt to redeem Discord Nitro codes as fast as possible. The bot aims to operate stealthily to avoid detection, making use of various headers, user agents, and randomized values. **Use at your own risk**—selfbotting is against Discord's Terms of Service and can result in an account ban.

## Features
- **Instant Nitro Sniper**: Quickly detects and attempts to redeem Nitro gift codes.
- **Giveaway Sniper**: Automatically joins Discord giveaways and claims the prize if you win.
- **Stealth Measures**: Randomized User Agents, hardware identifiers, and additional request headers to minimize detection.
- **Webhook Notifications**: Sends real-time notifications to a configured webhook to keep track of snipes and winnings.
- **Logging**: Logs important actions to both console and file.

## Disclaimer
This bot is for educational purposes only. Selfbotting (using unauthorized bots on a normal Discord user account) is against Discord's Terms of Service and may result in your account being permanently banned. The author is not responsible for any misuse or bans resulting from the use of this bot.

## Requirements
- Python 3.7+
- `aiohttp`, `discord.py` (selfbot version), and other dependencies listed in `requirements.txt`

## Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/discord-giveaway-sniper.git
   cd discord-giveaway-sniper
   ```

2. **Install Dependencies**
   Ensure you have Python 3.7+ installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Settings**
   - Copy `config.json.example` to `config.json`.
   - Open `config.json` and add your **Discord Token**, **Webhook URL**, and other optional settings like **Blacklist** and **WebhookNotification**.

4. **Run the Bot**
   ```bash
   python main.py
   ```

## Configuration
The bot requires a `config.json` file in the root directory with the following fields:
- **Token**: Your Discord user token (Note: Selfbotting is against Discord's TOS).
- **Webhook**: Webhook URL for sending notifications.
- **BotBlacklist**: A list of bot IDs to ignore.
- **WebhookNotification**: Boolean to enable or disable webhook notifications.

Example `config.json`:
```json
{
    "Token": [
        "YOUR_DISCORD_USER_TOKEN"
    ],
    "Webhook": "YOUR_WEBHOOK_URL",
    "WebhookNotification": true,
    "BotBlacklist": [
        "432610292342587392",
        "1156418379050127430",
        "1137344054187802664",
        "1089476688246738985",
        "1154077045903593555",
        "1149106738151305216",
        "1074118427184205974",
        "1093310583266353192",
        "776897904404987946",
        "1164588905065095219",
        "1140615763082879047",
        "646937666251915264",
        "368521195940741122",
        "1028956609382199346",
        "571027211407196161",
        "1071634826341396540",
        "838278395795079209",
        "320731871359008768",
        "1201646718895280148",
        "415773861486002186",
        "1100424685272961135",
        "873722451547291678",
        "1006190394415005788",
        "1153715777594200074",
        "1089935069927456849",
        "669228505128501258",
        "1130083482878623835",
        "716390085896962058",
        "678344927997853742",
        "1274435601470459946",
        "356268235697553409",
        "1275655805093281863",
        "1193672589428654120",
        "751151926959276050"
    ]
}
```

## Features in Detail
### 1. Instant Nitro Sniper
- Scans incoming messages for `discord.gift/` URLs and attempts to redeem them instantly using the provided user token.
- Implements various headers and random user agents to avoid detection.

### 2. Giveaway Sniper
- Automatically detects giveaway messages and reacts to join.
- If you win, it will notify you via webhook and attempt to send a DM to the giveaway creator.

### 3. Stealth Features
- **Randomized Headers**: Adds `X-Super-Properties`, `X-Fingerprint`, and other headers to requests to mimic legitimate Discord client behavior.
- **User Agent Rotation**: Utilizes a list of common user agents to make requests appear from various devices.
- **Hardware Identifiers**: Randomizes device identifiers in headers.

### 4. Logging and Notifications
- Logs to `logs.txt` to keep track of important events such as snipes, warnings, and errors.
- Sends webhook notifications to a configured URL, allowing real-time tracking of successful Nitro redemptions or giveaway winnings.

## Important Functions
- **check_nitro_codes**: Detects and redeems Nitro codes as soon as they are posted.
- **handle_giveaway_reaction**: Automatically reacts to giveaway messages to enter.
- **BotConnectedInfo**: Sends a notification when the bot successfully connects to Discord.

## Avoiding Detection
- **Custom Headers & Device IDs**: Adds multiple custom headers to mimic Discord client requests more closely.
- **Random User-Agent Strings**: Chooses a user-agent string from a predefined list to simulate requests from different devices.

## Warning
Selfbots are strictly against Discord's Terms of Service. If you use this script, you do so at your own risk. It is recommended to only use this on test accounts that you are willing to lose.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements
- Thanks to the contributors of `discord.py` and other Python packages that made this project possible.

**Note**: The use of this bot should be strictly for educational purposes only. Any misuse, including violating Discord's Terms of Service, may result in a ban or other legal consequences.
