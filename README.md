# 🎫 Discord Ticket Bot (mit ezcord)

Ein vollautomatischer Discord Ticket-Bot mit Slash Commands, GUI-Setup, Transkript-Export und mehr – geschrieben mit [`ezcord`]([https://github.com/NullDev/ezcord](https://github.com/tibue99/ezcord)) und `chat-exporter`.

**Repository:** [github.com/jinxedfr/Discord-Ticket-Bot](https://github.com/jinxedfr/Discord-Ticket-Bot)

> Kontakt: **jinxed.fr** auf Discord ✉️

---

## ✅ Features

- 🎟️ Slash-Befehl `/setup_tickets` zur Ticket-Erstellung
- 📋 Slash-Befehl `/ticketchannel_setup` zur Embed-Anpassung
- 💬 Interaktive Modals für Setup
- 🔒 Ticket schließen mit Transkript
- 📄 HTML-Export via [`chat-exporter`](https://pypi.org/project/chat-exporter)
- 📦 Konfiguration in `config/config.json`
- 🔁 Persistente Buttons nach Restart
- 🕙 10s Cooldown nach Schließen, bevor der Channel gelöscht wird

---

## 🚀 Installation & Setup

### 🔧 Voraussetzungen
- Python 3.10+
- Abhängigkeiten: `ezcord`, `chat-exporter`, `discord.py`

### 📁 `requirements.txt`
```txt
ezcord
discord.py
chat-exporter
```

### 🛠️ Startdatei: `main.py`
```python
import discord
import ezcord

bot = ezcord.Bot(
    intents=discord.Intents.all(),
    error_webhook_url="https://discord.com/api/webhooks/DEIN_WEBHOOK",
    language="de",
)

if __name__ == "__main__":
    bot.load_cogs("cogs")
    bot.run("DEIN_TOKEN")
```

### ▶️ Bot starten
```bash
pip install -r requirements.txt
python main.py
```

---

## 🧩 Slash-Befehle

### `/setup_tickets`
> Initialisiert das Ticketsystem per Modal-Eingabe.

### `/ticketchannel_setup`
> Ändert Titel und Beschreibung des Embeds, das beim Öffnen im Ticket erscheint.

---

## 📄 Transkripte

Beim Klick auf **🔒 Ticket schließen**:
- Das Transkript wird automatisch als `.html` mit `chat-exporter` erstellt
- Wird **per DM** an den User gesendet (nicht öffentlich)
- Danach erscheint ein Embed "🎟️ Ticket geschlossen"
- Nach 10 Sekunden wird der Channel automatisch gelöscht

---

## 🗃 Beispiel: `config/config.json`
```json
{
  "ticket_settings": {
    "category_id": "1234567890",
    "support_roles": ["123456789012345678"],
    "ticket_name": "ticket-{username}",
    "log_channel": "123456789012345678"
  },
  "embeds": {
    "ticket_panel": {
      "title": "Support",
      "description": "Klick auf den Button um ein Ticket zu eröffnen.",
      "color": 3447003,
      "button_label": "🎫 Ticket eröffnen"
    },
    "ticket_created": {
      "title": "Willkommen im Ticket",
      "description": "Ein Supporter meldet sich gleich!",
      "color": 5763719
    }
  }
}
```

---

## 📬 Hilfe & Support
> ✉️ **Discord:** `jinxed.fr`

Öffne ein [Issue](https://github.com/jinxedfr/Discord-Ticket-Bot/issues) oder erstelle eine PR für Feature-Ideen oder Bugfixes 🙌

---

## 🧾 Lizenz
MIT License
