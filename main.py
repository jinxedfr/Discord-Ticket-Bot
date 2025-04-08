import discord

import ezcord

bot = ezcord.Bot(
    intents=discord.Intents.all(),
    error_webhook_url="https://discord.com/api/webhooks/1359265764116402236/jbOHrgfrfuC1CVdLk4uUv1j40asMNvmDuOnDA8P36pL8n6TWxtAWNxr_s5keIViUrlgO",  # Replace with your webhook URL
    language="de",
)

if __name__ == "__main__":
    bot.load_cogs("cogs")  # Load all cogs in the "cogs" folder
    bot.run("")  # Replace with your bot token