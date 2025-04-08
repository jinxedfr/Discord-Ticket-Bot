import discord

import ezcord

bot = ezcord.Bot(
    intents=discord.Intents.all(),
    error_webhook_url="",  # Replace with your webhook URL
    language="de",
)

if __name__ == "__main__":
    bot.load_cogs("cogs")  # Load all cogs in the "cogs" folder
    bot.run("")  # Replace with your bot token
