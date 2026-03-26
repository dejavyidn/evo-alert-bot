# 🧬 EVO Pump.fun Alert Bot

**Real-time pump.fun monitoring via WebSocket for Telegram alerts**

---

## 🚀 Deploy on Ubuntu VPS (Git Clone)

### Step 1: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `evo-alert-bot`
3. Set to **Public**
4. **Leave empty** (don't initialize)
5. Create repository
6. Upload 3 files: `evo_alert_bot.py`, `requirements.txt`, `README.md`

---

### Step 2: Setup Ubuntu VPS

```bash
# 1. SSH to your VPS
ssh user@your-vps-ip

# 2. Install dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y

# 3. Clone repository
cd /home/user
git clone https://github.com/yourusername/evo-alert-bot.git
cd evo-alert-bot

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 3: Test Bot (Before Systemd)

```bash
# Ensure credentials in evo_alert_bot.py:
# TELEGRAM_BOT_TOKEN = "8457251646:AAHHtWJXdQOmgug1fYkCCdDRZUsAsqoD_WE"
# TELEGRAM_CHANNEL_ID = "-1003753283528"

# Run bot
python evo_alert_bot.py

# Check Telegram channel @EvoAlerts for startup message
# If seen: SUCCESS! Press Ctrl+C to stop test
```

---

### Step 4: Setup Systemd Service (Auto-Restart)

```bash
# Create service file
sudo nano /etc/systemd/system/evo-alert-bot.service
```

Paste this:
```ini
[Unit]
Description=EVO Pump.fun Alert Bot
After=network.target

[Service]
Type=simple
User=user
WorkingDirectory=/home/user/evo-alert-bot
Environment="PATH=/home/user/evo-alert-bot/venv/bin"
Environment="TELEGRAM_BOT_TOKEN=8457251646:AAHHtWJXdQOmgug1fYkCCdDRZUsAsqoD_WE"
Environment="TELEGRAM_CHANNEL_ID=-1003753283528"
ExecStart=/home/user/evo-alert-bot/venv/bin/python /home/user/evo-alert-bot/evo_alert_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable evo-alert-bot
sudo systemctl start evo-alert-bot
sudo systemctl status evo-alert-bot
```

**Expected:** `active (running)`

---

### Step 5: Monitor Bot

```bash
# View logs
sudo journalctl -u evo-alert-bot -f

# Check status
sudo systemctl status evo-alert-bot

# Restart (after update)
sudo systemctl restart evo-alert-bot

# Stop
sudo systemctl stop evo-alert-bot
```

---

## 🔧 How It Works

### WebSocket Real-Time
```
wss://pumpportal.fun/data-api/real-time
```
- Push notifications (instant)
- Events: `new_token`, `token_update`, `graduation`
- Auto-reconnect on disconnect

### Alert Types

| Alert | Trigger |
|-------|---------|
| **🧬 Trending** | Volume ≥10 SOL (5min) + Volume ≥200% OR Fast mover (+100%) / Graduation (≥90%) |

**Hourly Recap** at top of every hour

---

## 📋 Configuration

Edit `evo_alert_bot.py`:

```python
MIN_VOLUME_SOL = 10          # Min volume (SOL) in 5min
MIN_HOLDERS = 50             # Min holder count
MAX_AGE_MINUTES = 30         # Max token age (ignore older)
MIN_LIQUIDITY_USD = 1000     # Min liquidity (USD)
VOLUME_SPIKE_PERCENT = 200   # Volume spike threshold (%)
MAX_ALERTS_PER_HOUR = 10     # Anti-spam limit
```

After editing:
```bash
sudo systemctl restart evo-alert-bot
```

---

## 🆘 Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: websockets` | `pip install -r requirements.txt` |
| No alerts | Lower `MIN_VOLUME_SOL` to 5 / Check channel ID |
| Bot offline | `sudo systemctl status evo-alert-bot` |
| "Forbidden" | Add bot as admin to channel |
| WebSocket disconnect | Normal - auto-reconnects |

---

## 🔄 Update Bot

```bash
cd /home/user/evo-alert-bot
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart evo-alert-bot
```

---

## 🎯 Expected Result

Channel @EvoAlerts should show:
```
🧬 EVO ALERT BOT CONNECTED 🧬
Listening to pump.fun real-time stream...
Thresholds: • Min Volume: 10 SOL • Min Holders: 50
Standby for alpha! 👀
- EVO Agents
```

---

## 📊 Technical Details

- **Memory:** ~50MB
- **CPU:** Minimal
- **Connection:** Outbound 443 only (Telegram + pump.fun)
- **Python:** 3.8+
- **Libraries:** `python-telegram-bot==20.7`, `aiohttp==3.9.1`, `websockets==12.0`

---

## ✅ Pre-Flight Checklist

- [ ] GitHub repo `evo-alert-bot` created (Public)
- [ ] Bot added as admin to @EvoAlerts
- [ ] VPS Ubuntu ready with SSH access
- [ ] `git clone` repository to `/home/user/evo-alert-bot`
- [ ] Virtual environment created + dependencies installed
- [ ] Systemd service configured & started
- [ ] Startup message appears in Telegram channel

---

**Ready? Run the commands above!** 🚀

Need help? Send `sudo journalctl -u evo-alert-bot --since "5 min ago"` output.
