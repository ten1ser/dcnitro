# Discord Giveaway and Nitro Sniper Selfbot

![Logo](https://files.oaiusercontent.com/file-LGrDOJboN4Xx0kzlEJWmpTms?se=2024-11-19T13%3A30%3A00Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D3dada67e-c593-42be-aaaa-a636db131f94.webp&sig=c3BfPx0XYOj9MA8hyjCsVpXNADRSCtl0qZ7XZveKhPM%3D)

## Overview 🚀

This Discord selfbot script automatically participates in giveaways and redeems Discord Nitro codes...


This Discord selfbot script automatically participates in giveaways and redeems Discord Nitro codes as fast as possible. It aims to operate stealthily to avoid detection by using randomized headers, user agents, and device identifiers. **Use at your own risk**—selfbotting violates Discord's Terms of Service and may result in an account ban.

This tool is ideal for users looking for a **Discord Nitro sniper** and **giveaway bot** that integrates directly with their account, automating **Nitro code redemption** and giveaway participation to maximize success.

## Features 🌟

- 🎉 **Giveaway Participation**: Joins Discord giveaways by clicking buttons or adding emoji reactions.
- ⚡ **Instant Nitro Sniper**: Quickly detects and attempts to redeem Discord Nitro gift codes.
- 🕵️ **Stealth Features**: Uses randomized User Agents, device identifiers, and request headers to reduce detection risks.
- 🔔 **Webhook Notifications**: Sends real-time notifications to a configured webhook to track snipes and winnings.
- 📝 **Logging**: Logs important actions to both console and file for review.
- 🔍 **Hidden Features**: Added stealth options for reducing detection from Discord's anti-bot systems.

## Disclaimer ⚠️

This bot is for **educational purposes** only. Using unauthorized bots on a Discord user account is against Discord's Terms of Service and may result in your account being permanently banned. The author is not responsible for any misuse or bans resulting from the use of this bot.

## Requirements 📋

- Python 3.7+ (recommended for optimal performance with Discord bots)
- `aiohttp`, `discord.py` (selfbot version), and other dependencies listed in `requirements.txt`

## Installation 💻

1. 📂 **Clone the Repository**

   ```bash
   git clone https://github.com/kubaam/Discord-Giveaway-and-Nitro-Sniper-Selfbot
   cd Discord-Giveaway-and-Nitro-Sniper-Selfbot
   ```

2. 📦 **Install Dependencies**
   Ensure you have Python 3.7+ installed. Then run:

   ```bash
   pip install -r requirements.txt
   ```

3. ⚙️ **Configure Settings**

   - Copy `config.json.example` to `config.json`.
   - Open `config.json` and add your **Discord Token**, **Webhook URL**, and other optional settings like **BotBlacklist** and **WebhookNotification**.

4. ▶️ **Run the Bot**

   ```bash
   python main.py
   ```

   ![Bot Running in Windows CMD](https://github.com/kubaam/Discord-Giveaway-and-Nitro-Sniper-Selfbot/blob/main/assets/cmd.png)

   *Screenshots have been added to illustrate the bot's functions and provide a better understanding of its operations.*

## Configuration 🔧

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

## Features in Detail 💎

### 1. ⚡ Instant Nitro Sniper

- **Nitro Code Detection**: Scans incoming messages for `discord.gift/` URLs and attempts to redeem them instantly using the provided user token.
- **Feedback Handling**: Differentiates between "Invalid code" and "Captcha required" for better clarity on the redemption status.
- **Stealth Measures**: Implements various headers and randomized user agents to avoid detection.

   ![Nitro Redeem Attempt Webhook Notify](https://github.com/kubaam/Discord-Giveaway-and-Nitro-Sniper-Selfbot/blob/main/assets/nitroredeem.png)

### 2. 🎉 Giveaway Sniper

- **Automatic Entry**: Joins giveaways by clicking interactive buttons or adding emoji reactions.
- **Improved Detection**: Automatically detects giveaway messages and joins by reacting.
- **Prize Notifications**: Sends webhook notifications and attempts to DM the giveaway creator if you win.
- **Better Prize Extraction**: Uses enhanced logic to accurately extract and display the giveaway prize.

   ![Giveaway Sniped Webhook Notify](https://github.com/kubaam/Discord-Giveaway-and-Nitro-Sniper-Selfbot/blob/main/assets/gwsniped.png)

   ![Giveaway Won Webhook Notify](https://github.com/kubaam/Discord-Giveaway-and-Nitro-Sniper-Selfbot/blob/main/assets/gwwon.png)

### 3. 🕵️ Stealth Features

- **Randomized Headers**: Adds `X-Super-Properties`, `X-Fingerprint`, and other headers to mimic legitimate Discord client behavior.
- **User Agent Rotation**: Utilizes a list of common user agents to make requests appear from various devices.
- **Randomized Device Identifiers**: Randomizes hardware identifiers in headers to further avoid detection.
- **Rate Limit Handling**: Added logic to respect Discord's rate limits and retry after a cooldown period.

### 4. 🔔 Logging and Notifications

- **Comprehensive Logging**: Logs to `logs.txt` to keep track of important events such as snipes, warnings, and errors.
- **Webhook Notifications**: Sends real-time updates to a configured webhook URL, detailing successful Nitro redemptions or giveaway wins.
- **Improved Formatting**: Webhook messages are formatted with descriptive titles, colored embeds, and author/location details.

   ![Bot Connected Webhook Notify](https://github.com/kubaam/Discord-Giveaway-and-Nitro-Sniper-Selfbot/blob/main/assets/connect.png)

## Important Functions 🔑

- **check_nitro_codes**: Detects and redeems Nitro codes as soon as they are posted.
- **handle_giveaway_reaction**: Reacts to giveaway messages, either clicking buttons or adding emojis.
- **detect_giveaway_win_message**: Detects when a win message is posted and sends notifications, optionally DMing the giveaway creator.
- **BotConnectedInfo**: Notifies when the bot successfully connects to Discord, with account details.

## Avoiding Detection 🚫

- **Custom Headers & Device IDs**: Uses custom headers to closely mimic Discord client requests.
- **Rotating User Agents**: Chooses a user-agent string from a predefined list to simulate requests from different devices.
- **Random Device Identifiers**: Randomizes device and fingerprint identifiers to make each request unique.
- **Rate Limit Respect**: Implements a `Retry-After` mechanism for 429 HTTP responses to avoid getting rate-limited further.

## Warning ⚠️

**Discord Nitro sniper**, **Discord giveaway bot**, and other selfbots are strictly against Discord's Terms of Service. Use this script at your own risk, and only on test accounts that you are willing to lose.

## Contributing 🤝

If you appreciate my hard work and would like to support me, you can do so with any amount on PayPal: [paypal.me/JakubAmbrus](https://paypal.me/JakubAmbrus)

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License 📜

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements 🙏

- Thanks to the contributors of `discord.py` and other Python packages that made this project possible.

**Note**: This bot is for **educational purposes** only. Misuse, including violating Discord's Terms of Service, can lead to a ban or other legal consequences.

