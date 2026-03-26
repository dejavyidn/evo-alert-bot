# 🧬 EVO Pump.fun Alert Bot

**Real-time pump.fun monitoring via WebSocket for Telegram alerts**

---

## 🚀 Quick Deploy (5 Minutes)

### 1. Prerequisites
- GitHub account (free)
- Render/Railway/Replit account (free)
- Bot token & Channel ID (already configured)

### 2. Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `evo-alert-bot`
3. Set to **Public**
4. Don't initialize with anything
5. Create repository

---

### 3. Upload Files

Upload these 3 files to your repository:

```
evo-alert-bot/
├── evo_alert_bot.py      # Main bot script (WebSocket)
├── requirements.txt      # Dependencies
└── README.md            # This file
```

**Important:** evo_alert_bot.py already configured with your credentials!

---

### 4. Deploy to Render (or Railway/Replit)

#### Render (Recommended - No CC needed after signup)
1. Sign up: https://render.com/ (use GitHub login)
2. Dashboard → **New → Web Service**
3. **Connect Repository:**
   - Select: `evo-alert-bot`
   - Branch: `main`
4. **Configuration:**
   - Name: `evo-alert-bot`
   - Region: Singapore (closest to Indonesia)
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python evo_alert_bot.py`
5. **Environment Variables (CRITICAL!):**
   ```
   TELEGRAM_BOT_TOKEN=8457251646:AAHHtWJXdQOmgug1fYkCCdDRZUsAsqoD_WE
   TELEGRAM_CHANNEL_ID=-1003753283528
   ```
6. **Instance Type:** FREE (750 hours/month - enough for 24/7)
7. Click **Create Web Service**

**Wait 2-5 minutes for build & deploy.**

---

#### Railway (Alternative - No CC)
1. Sign up: https://railway.app/ (with GitHub)
2. New Project → Deploy from GitHub → select `evo-alert-bot`
3. Settings:
   - Runtime: Python
   - Start command: `python evo_alert_bot.py`
   - Build command: `pip install -r requirements.txt`
4. Add environment variables (same as above)
5. Deploy! (free tier: $5/month - more than enough)

---

#### Replit (Easiest - But needs keepalive)
1. Sign up: https://replit.com/ (with GitHub/Google)
2. + Create Repl → Python → Name: `evo-alert-bot`
3. Upload 3 files (drag-drop)
4. Lock icon (Secrets) → Add both env vars
5. Click Run ▶️
6. **IMPORTANT:** Set up UptimeRobot to ping every 5 min (Replit sleeps)

---

### 5. Verify Deployment

1. Check hosting logs (should show "EVO ALERT BOT CONNECTED")
2. Check your Telegram channel **@EvoAlerts**
3. Should see startup message:
   ```
   🧬 EVO ALERT BOT CONNECTED 🧬
   Listening to pump.fun real-time stream...
   ```
4. If you see it → **SUCCESS! ✅**

---

## 🔧 How It Works

### WebSocket Connection (Real-Time!)
```
pumpportal.fun/data-api/real-time (wss://)
```
- **Instant push** - no polling delay
- **Event-driven** - listens for: `new_token`, `token_update`, `graduation`
- **Efficient** - zero wasted requests
- **Reliable** - auto-reconnect on disconnect

### Alert Types

| Alert | Trigger | Description |
|-------|---------|-------------|
| **🧬 Trending** | New token with volume ≥10 SOL | Fresh token entering trending |
| **🚨 Volume Spike** | Volume increase ≥200% in 5min | Sudden buying pressure |
| **🚀 Fast Mover** | Price pump ≥100% in 5min | Token pumping hard |
| **🎓 Graduation** | Bonding curve ≥90% | About to launch to Raydium |
| **📊 Hourly Recap** | Every hour | Top trending summary |

---

## 📋 Configuration

All thresholds in `evo_alert_bot.py`:

```python
MIN_VOLUME_SOL = 10          # Minimum volume (SOL) in 5 minutes
MIN_HOLDERS = 50             # Minimum holder count
MAX_AGE_MINUTES = 30         # Maximum token age (ignore old tokens)
MIN_LIQUIDITY_USD = 1000     # Minimum liquidity (USD)
VOLUME_SPIKE_PERCENT = 200   # Volume spike threshold (%)
MAX_ALERTS_PER_HOUR = 10     # Anti-spam limit
```

**Adjust as needed, then redeploy!**

---

## 🔄 Updating the Bot

1. Edit `evo_alert_bot.py` on GitHub
2. Commit changes
3. Hosting **auto-deploys** within 1-2 minutes
4. Check logs to confirm update

---

## 🆘 Troubleshooting

### Bot not sending alerts?
- ✅ Check hosting logs for errors (WebSocket connection?)
- ✅ Verify bot is **admin** in your Telegram channel
- ✅ Check Channel ID: must include `-100` prefix
- ✅ Wait for first pump.fun activity (may take minutes)
- ✅ Lower `MIN_VOLUME_SOL` to 5 for testing

### "ModuleNotFoundError: websockets"
- ✅ Make sure `requirements.txt` has `websockets==12.0`
- ✅ Build command: `pip install -r requirements.txt`

### WebSocket disconnect?
- ✅ Normal - bot auto-reconnects
- ✅ Check firewall/network (port 443 outbound)

### Too many/too few alerts?
- Adjust thresholds in `evo_alert_bot.py`
- Redeploy after changes

---

## 🎯 Testing Locally (Optional)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run bot locally
python evo_alert_bot.py

# 3. Check your Telegram channel for startup message
# 4. Stop with Ctrl+C when done
```

---

## 📊 Monitoring

- **Hosting Dashboard:** View logs, restart service, check uptime
- **Telegram Channel:** Real-time alerts
- **GitHub:** Code version history

---

## 🧬 EVO Branding

All alerts include EVO branding:
- 🧬 EVO emoji
- "Evolve or Die" tagline
- EVO Agents signature

---

## 💡 Technical Details

- **Language:** Python 3.8+
- **Libraries:**
  - `python-telegram-bot==20.7` - Telegram API
  - `aiohttp==3.9.1` - REST fallback for token details
  - `websockets==12.0` - WebSocket connection to pump.fun
- **Connection:** wss://pumpportal.fun/data-api/real-time
- **Memory:** Lightweight (~50MB RAM)

---

## 📞 Support

- **pump.fun API Docs:** https://pumpportal.fun/api
- **Python Telegram Bot:** https://github.com/python-telegram-bot
- **WebSocket Guide:** https://websockets.readthedocs.io

---

**Created:** March 26, 2026
**For:** EVO Agents
**Status:** ✅ READY TO DEPLOY (WebSocket Real-Time)

---

## ✅ Pre-Flight Checklist

Before deploying, ensure:

- [x] GitHub repo created: `evo-alert-bot` (Public)
- [x] 3 files uploaded (evo_alert_bot.py, requirements.txt, README.md)
- [x] Environment variables set (both required)
- [x] Bot added as admin to @EvoAlerts
- [x] Bot token valid
- [x] Channel ID correct (with -100 prefix)
- [x] requirements.txt includes `websockets==12.0`
- [x] Hosting platform selected (Render/Railway/Replit)

---

**Now deploy!** 🚀

Real-time alerts incoming soon...
