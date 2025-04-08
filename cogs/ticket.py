import discord
from discord.ext import commands
import json, os, io, asyncio
from chat_exporter import chat_exporter

CONFIG_PATH = "config/config.json"

def save_config(data):
    os.makedirs("config", exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return None
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

class SetupModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Ticket Setup")
        self.add_item(discord.ui.InputText(label="Panel Titel"))
        self.add_item(discord.ui.InputText(label="Panel Beschreibung"))
        self.add_item(discord.ui.InputText(label="Button Text"))
        self.add_item(discord.ui.InputText(label="Kategorie-ID"))
        self.add_item(discord.ui.InputText(label="Support-Rollen (Komma-getrennt)"))

    async def callback(self, interaction: discord.Interaction):
        config = {
            "ticket_settings": {
                "category_id": self.children[3].value.strip(),
                "support_roles": [r.strip() for r in self.children[4].value.split(",")],
                "ticket_name": "ticket-{username}",
                "log_channel": str(interaction.channel.id)
            },
            "embeds": {
                "ticket_panel": {
                    "title": self.children[0].value,
                    "description": self.children[1].value,
                    "color": 3447003,
                    "button_label": self.children[2].value
                },
                "ticket_created": {
                    "title": "Willkommen im Ticket",
                    "description": "Ein Supporter meldet sich gleich!",
                    "color": 5763719
                }
            }
        }

        save_config(config)

        embed = discord.Embed(
            title=config["embeds"]["ticket_panel"]["title"],
            description=config["embeds"]["ticket_panel"]["description"],
            color=config["embeds"]["ticket_panel"]["color"]
        )
        view = TicketView(config)
        await interaction.response.send_message(embed=embed, view=view)

class TicketView(discord.ui.View):
    def __init__(self, config):
        super().__init__(timeout=None)
        self.config = config

    @discord.ui.button(label="🎫 Ticket eröffnen", style=discord.ButtonStyle.primary, custom_id="open_ticket")
    async def open_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=int(self.config["ticket_settings"]["category_id"]))
        support_roles = [int(r) for r in self.config["ticket_settings"]["support_roles"]]

        name = self.config["ticket_settings"]["ticket_name"].replace("{username}", interaction.user.name)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        for role_id in support_roles:
            role = guild.get_role(role_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True)

        channel = await guild.create_text_channel(name, category=category, overwrites=overwrites)

        embed_data = self.config["embeds"]["ticket_created"]
        embed = discord.Embed(title=embed_data["title"], description=embed_data["description"], color=embed_data["color"])
        view = TicketControls(interaction.user.id)

        await channel.send(content=interaction.user.mention, embed=embed, view=view)
        await interaction.response.send_message(f"🎟️ Ticket erstellt: {channel.mention}", ephemeral=True)

class TicketControls(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(label="🔒 Ticket schließen", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_ticket(self, button, interaction: discord.Interaction):
        await interaction.response.defer()

        transcript = await chat_exporter.export(
            interaction.channel,
            tz_info="Europe/Berlin",
            military_time=True,
            bot=interaction.client
        )

        if transcript:
            file = discord.File(
                io.BytesIO(transcript.encode()),
                filename=f"transcript-{interaction.channel.name}.html"
            )
            try:
                user = await interaction.client.fetch_user(self.user_id)
                await user.send("📄 Dein Ticket-Transkript:", file=file)
            except discord.Forbidden:
                await interaction.followup.send("⚠️ Konnte keine DM sendens.", ephemeral=True)

        embed = discord.Embed(
            title="🎟️ Ticket geschlossen",
            description=f"{interaction.user.mention} hat das Ticket geschlossen. Das Transkript wurde per DM gesendet.",
            color=discord.Color.red()
        )
        await interaction.channel.send(embed=embed)
        await asyncio.sleep(10)  # Cooldown von 10 Sekunden
        await interaction.channel.delete()

class ChannelEmbedModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Ticket Embed bearbeiten")
        self.add_item(discord.ui.InputText(label="Neuer Titel"))
        self.add_item(discord.ui.InputText(label="Neue Beschreibung"))

    async def callback(self, interaction: discord.Interaction):
        config = load_config()
        config["embeds"]["ticket_created"]["title"] = self.children[0].value
        config["embeds"]["ticket_created"]["description"] = self.children[1].value
        save_config(config)

        embed = discord.Embed(
            title=self.children[0].value,
            description=self.children[1].value,
            color=config["embeds"]["ticket_created"]["color"]
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="setup_tickets", description="Ticket-System initialisieren")
    async def setup_tickets(self, ctx):
        await ctx.send_modal(SetupModal())

    @discord.slash_command(name="ticketchannel_setup", description="Ändere das Embed im Ticket-Channel")
    async def ticket_embed_setup(self, ctx):
        await ctx.send_modal(ChannelEmbedModal())

def setup(bot):
    bot.add_cog(TicketSystem(bot))
