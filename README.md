# 🧬 EVO Pump.fun Alert Bot

**Automatic pump.fun trending alerts for Telegram channel**

---

## 🚀 Quick Deploy (5 Minutes)

### 1. Prerequisites
- GitHub account (free)
- Render account (free)
- Bot token & Channel ID (have both already)

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
├── evo_alert_bot.py      # Main bot script
├── requirements.txt      # Dependencies
└── README.md            # This file
```

**Important:** evo_alert_bot.py already configured with your credentials!

---

### 4. Deploy to Render

1. Sign up: https://render.com/ (use GitHub login - easiest)
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

### 5. Verify Deployment

1. Check Render logs (should show "EVO ALERT BOT STARTED")
2. Check your Telegram channel **@EvoAlerts**
3. Should see startup message:
   ```
   🧬 EVO ALERT BOT STARTED 🧬
   Bot is now monitoring pump.fun...
   ```
4. If you see it → **SUCCESS! ✅**

---

## 🔧 Configuration

All thresholds already set to reasonable defaults:

| Setting | Current Value | Description |
|---------|---------------|-------------|
| MIN_VOLUME_SOL | 10 | Min volume (SOL) in 5min |
| MIN_HOLDERS | 50 | Min holder count |
| MAX_AGE_MINUTES | 30 | Max token age (minutes) |
| MIN_LIQUIDITY_USD | 1000 | Min liquidity (USD) |
| VOLUME_SPIKE_PERCENT | 200 | Volume spike threshold |
| CHECK_INTERVAL_SECONDS | 30 | How often to check |
| MAX_ALERTS_PER_HOUR | 10 | Anti-spam limit |

---

## 📋 Alert Types

The bot sends 4 types of alerts:

1. **🧬 Trending Alert** - New token entering pump.fun trending
2. **🚨 Volume Spike** - Sudden volume increase
3. **🚀 Fast Mover** - Token pumping >100% in 5min
4. **🎓 Graduation Alert** - Token nearing bonding curve completion
5. **📊 Hourly Recap** - Summary of trending tokens

---

## 🔄 Updating the Bot

1. Edit `evo_alert_bot.py` on GitHub
2. Commit changes
3. Render **auto-deploys** within 1-2 minutes
4. Check Render logs to confirm update

---

## 🆘 Troubleshooting

### Bot not sending alerts?
- ✅ Check Render logs for errors
- ✅ Verify bot is **admin** in your Telegram channel
- ✅ Check Channel ID: must include `-100` prefix
- ✅ Wait for first trending token to appear (may take minutes)

### Rendering errors?
- ✅ Python version: must be Python 3.8+
- ✅ Requirements.txt format correct
- ✅ Environment variables set correctly

### Too many/too few alerts?
- Adjust thresholds in `evo_alert_bot.py` (see Configuration section above)
- Redeploy after changes

---

## 🎯 Testing Locally (Optional)

If you want to test before deploying:

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

- **Render Dashboard:** View logs, restart service, check uptime
- **Telegram Channel:** Real-time alerts
- **GitHub:** Code version history

---

## 🧬 EVO Branding

All alerts include EVO branding:
- 🧬 EVO emoji
- "Evolve or Die" tagline
- EVO Agents signature

---

## 💡 Next Steps

After bot is running:

1. ✅ Verify alerts are working
2. ✅ Test different alert types
3. ✅ Share channel with EVO holders
4. ✅ Plan Stage 2: Add smart money tracking
5. ✅ Plan Stage 3: Multi-chain support

---

## 📞 Support

- **Render Docs:** https://render.com/docs
- **Python Telegram Bot:** https://github.com/python-telegram-bot
- **pump.fun API:** https://pumpportal.fun/api

---

**Created:** March 26, 2026  
**For:** EVO Agents  
**Status:** ✅ READY TO DEPLOY

---

## ✅ Pre-Flight Checklist

Before deploying, ensure:

- [x] GitHub repo created
- [x] Files uploaded (3 files)
- [x] Render account created
- [x] Environment variables set (both required)
- [x] Bot added as admin to @EvoAlerts
- [x] Bot token valid
- [x] Channel ID correct (with -100 prefix)

---

**Now deploy!** 🚀
