# Discord Giveaway and Nitro Sniper Selfbot

## Overview 🚀

Welcome to the **Discord Giveaway and Nitro Sniper Selfbot**, a powerful automation tool designed to **automatically join Discord giveaways** and **instantly redeem Discord Nitro codes**. With state-of-the-art **stealth features** to minimize detection risk, this selfbot provides an efficient solution for maximizing your chances of **winning Discord giveaways** and **securing Discord Nitro codes**. Please note that **selfbotting is against Discord's Terms of Service**, and using this bot may result in an account ban. **Use at your own risk**.

This tool is ideal for users searching for a reliable, fast, and stealthy way to automate **Nitro code redemptions**, **giveaway participation**, and **event tracking** on Discord. Whether you are interested in winning **free Discord Nitro** or becoming the fastest in **giveaway sniping**, this selfbot delivers.

## Key Features 🌟

- 🎉 **Automatic Giveaway Participation**: Automatically enters Discord giveaways by clicking buttons or adding emoji reactions, maximizing your chances of winning prizes.
- ⚡ **Instant Nitro Code Sniper**: Instantly detects and attempts to redeem Discord Nitro gift codes as soon as they are posted, ensuring you are among the first to redeem.
- 🕵️ **Stealth Features for Low Detection**: Utilizes randomized User Agents, device identifiers, and custom HTTP headers to disguise bot activity, effectively reducing the risk of detection by Discord.
- 🔔 **Webhook Notifications**: Provides real-time notifications via a configured webhook to keep you updated on successful snipes, giveaway wins, and other critical events.
- 📜 **Comprehensive Logging**: Logs all actions, such as giveaway participation and Nitro redemptions, to both console and log files for easy tracking and debugging.
- 🔍 **Advanced Detection and Monitoring**: Analyzes both message content and embedded fields to ensure thorough detection of giveaways and Nitro codes across different Discord channels.
- 📤 **Automated Direct Messages**: Sends direct messages to giveaway hosts after winning, showing gratitude and providing a personalized touch.
- 📊 **Customizable Settings**: Offers detailed configuration options through `config.json` to allow for full control over the bot's behavior.

## Disclaimer ⚠️

This bot is intended for **educational purposes only**. Using it may violate Discord's Terms of Service and result in account suspensions or bans. The author takes no responsibility for any misuse or consequences resulting from the use of this tool. **Use at your own risk**.

## Requirements 📋

- **Python 3.7+**: Ensure compatibility and optimal performance by using Python 3.7 or higher.
- **Dependencies**: Install dependencies such as `aiohttp`, `discord.py-self`, and others via `requirements.txt`.

## Installation 💻

1. 📂 **Clone the Repository**

   ```bash
   git clone https://github.com/kubaam/Discord-Giveaway-and-Nitro-Sniper-Selfbot
   cd Discord-Giveaway-and-Nitro-Sniper-Selfbot
   ```

2. 📦 **Install Dependencies**
   Ensure you have Python 3.7+ installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

3. ⚙️ **Configure Settings**

   - Copy `config.json.example` to `config.json`.
   - Open `config.json` and add your **Discord Token**, **Webhook URL**, and other settings such as **BotBlacklist** and **WebhookNotification**.

4. ▶️ **Run the Bot**

   ```bash
   python main.py
   ```

   ![Bot Running in Windows CMD](https://github.com/kubaam/Discord-Giveaway-and-Nitro-Sniper-Selfbot/blob/main/assets/cmd.png)

## Configuration 🔧

The bot requires a `config.json` file in the root directory with the following fields:

- **Token**: Your Discord user token (Note: Using a selfbot is against Discord's Terms of Service).
- **Webhook**: Webhook URL to send notifications about successful snipes and wins.
- **BotBlacklist**: A list of bot IDs that should be ignored when participating in giveaways.
- **WebhookNotification**: Boolean value to enable or disable webhook notifications.
- **UserAgents**: A list of user agents to be used for randomizing HTTP requests.
- **DeviceIds**: A list of device identifiers used to further randomize and avoid detection.

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
        "1137344054187802664"
    ],
    "UserAgents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "curl/7.68.0",
        "Googlebot/2.1 (+http://www.google.com/bot.html)"
    ],
    "DeviceIds": [
        "a1b2c3d4e5f6g7h8i9j0",
        "098f6bcd4621d373cade4e832627b4f6",
        "1234567890abcdef1234567890abcdef"
    ]
}
```

## Features in Detail 💎

### 1. ⚡ **Instant Nitro Code Sniper**

- **Nitro Code Detection**: Continuously scans incoming messages across Discord channels for `discord.gift/` URLs and attempts to redeem them immediately, giving you a competitive edge in Nitro redemptions.
- **Redemption Feedback**: Provides feedback on whether the code was redeemed successfully, was invalid, or was already used, so you know exactly what happened.
- **Advanced Stealth Measures**: Randomizes HTTP headers and user agents to make the bot appear like a legitimate Discord client, significantly reducing detection risks.
- **Real-Time Webhook Notifications**: Sends detailed webhook notifications to keep you informed of each redemption attempt and its outcome.

   ![Nitro Redeem Attempt Webhook Notify](https://github.com/kubaam/Discord-Giveaway-and-Nitro-Sniper-Selfbot/blob/main/assets/nitroredeem.png)

### 2. 🎉 **Giveaway Sniper**

- **Automatic Entry into Giveaways**: Detects giveaway messages across Discord servers and enters them automatically by clicking buttons or reacting with emojis.
- **Enhanced Prize Recognition**: Uses sophisticated parsing algorithms to accurately identify and display giveaway prizes, ensuring you are always aware of the rewards being offered.
- **Real-Time Notifications for Wins**: Sends webhook notifications as soon as you win a giveaway, so you stay updated without needing to monitor manually.
- **Personalized Direct Messages**: After winning a giveaway, the bot sends a direct message to the giveaway host to thank them, enhancing your interactions with the community.
- **Deep Embed Parsing**: Analyzes all available embed fields—including titles, descriptions, and custom fields—to thoroughly detect giveaway details, ensuring no opportunities are missed.

   ![Giveaway Sniped Webhook Notify](https://github.com/kubaam/Discord-Giveaway-and-Nitro-Sniper-Selfbot/blob/main/assets/gwsniped.png)

   ![Giveaway Won Webhook Notify](https://github.com/kubaam/Discord-Giveaway-and-Nitro-Sniper-Selfbot/blob/main/assets/gwwon.png)

### 3. 🕵️ **Stealth Features**

- **Custom HTTP Headers and Identifiers**: Uses custom headers like `X-Super-Properties` and `X-Fingerprint` to ensure requests closely mimic those made by legitimate Discord clients, making bot activity less detectable.
- **Rotating User Agents**: Each request is made using a random user agent from a predefined list, simulating access from various devices and making bot activity less predictable.
- **Dynamic Device Identifiers**: The bot randomizes device identifiers for every request, making the activity look more natural and reducing detection risks.
- **Rate Limit Handling**: Implements smart rate limit handling using `Retry-After` to respect Discord's rate limits and prevent automated bans.

### 4. 🔔 **Logging and Notifications**

- **Detailed Logging**: Logs all bot activities—including Nitro snipes, giveaway entries, and errors—to a `logs.txt` file for easy tracking and troubleshooting.
- **Webhook Notifications**: Configurable webhook notifications provide real-time updates on all important bot actions, such as Nitro redemptions, giveaway wins, and connection statuses.
- **Connection Updates**: Notifies you when the bot successfully connects to Discord, giving you peace of mind that the bot is running smoothly.

   ![Bot Connected Webhook Notify](https://github.com/kubaam/Discord-Giveaway-and-Nitro-Sniper-Selfbot/blob/main/assets/connect.png)

## Important Functions 🔑

- **`check_nitro_codes()`**: Constantly monitors messages for Nitro codes and attempts to redeem them instantly, providing real-time feedback on the status of each attempt.
- **`handle_giveaway_reaction()`**: Automatically reacts to giveaways using either interactive Discord components or emoji reactions to join as soon as possible.
- **`detect_giveaway_win_message()`**: Detects and responds to giveaway win messages by sending detailed notifications, ensuring you are aware of every win.
- **`notify_giveaway_creator()`**: Sends a personalized direct message to giveaway hosts after a win, thanking them and maintaining good community relations.
- **`BotConnectedInfo()`**: Sends a webhook notification when the bot connects to Discord, displaying relevant account details for verification.

## Stealth and Anti-Detection Strategies 🚫

- **Rotating Custom Headers & Device IDs**: Uses unique headers and device identifiers such as `X-Fingerprint` and randomized device IDs to mimic legitimate Discord client requests.
- **User-Agent Randomization**: Each bot request uses a random user-agent string to simulate different types of devices, further hiding bot activity from detection.
- **Dynamic Device Identifiers**: Continuously changes device fingerprints to make each request appear distinct, effectively reducing the likelihood of detection by Discord's anti-bot algorithms.
- **Smart Rate Limit Compliance**: Manages rate limits intelligently by respecting Discord's `Retry-After` headers to avoid triggering anti-bot detection measures and being rate-limited.

## Warning ⚠️

This bot functions as a **Discord Nitro sniper**, **giveaway sniper**, and general **selfbot**. Using any selfbot, including this one, violates Discord's Terms of Service and may lead to a permanent ban of your account. It is strongly recommended that you use this bot only on secondary or test accounts that you are willing to lose. **Proceed with caution**.

## Contributing 🤝

If you appreciate this project and would like to support further development, consider making a donation via PayPal: [paypal.me/JakubAmbrus](https://paypal.me/JakubAmbrus).

Pull requests are welcome! For significant changes, please open an issue first to discuss your proposed modifications.

## License 📜

This project is licensed under the MIT License. Please see the `LICENSE` file for complete details.

## Acknowledgements 🙏

- Special thanks to the contributors of `discord.py`, `aiohttp`, and other Python libraries that made this project possible.

**Note**: This bot is intended for **educational purposes** only. Improper use, such as violating Discord's Terms of Service, can lead to account bans or other penalties. Always use caution and use this tool only on accounts you can afford to lose.
