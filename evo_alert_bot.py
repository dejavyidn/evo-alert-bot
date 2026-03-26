import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from telegram import Bot
import logging

# ═══════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════

TELEGRAM_BOT_TOKEN = "8457251646:AAHHtWJXdQOmgug1fYkCCdDRZUsAsqoD_WE"
TELEGRAM_CHANNEL_ID = "-1003753283528"

# Alert Thresholds
MIN_VOLUME_SOL = 10
MIN_HOLDERS = 50
MAX_AGE_MINUTES = 30
MIN_LIQUIDITY_USD = 1000
VOLUME_SPIKE_PERCENT = 200

# Monitoring Settings
CHECK_INTERVAL_SECONDS = 30
MAX_ALERTS_PER_HOUR = 10

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

PUMP_FUN_API = "https://api.pump.fun"

class AlertTracker:
    def __init__(self):
        self.alerts_sent = []
        self.alerted_tokens = set()
    
    def can_alert(self, token_mint: str) -> bool:
        if token_mint in self.alerted_tokens:
            return False
        
        one_hour_ago = datetime.now() - timedelta(hours=1)
        recent_alerts = [t for t in self.alerts_sent if t > one_hour_ago]
        
        if len(recent_alerts) >= MAX_ALERTS_PER_HOUR:
            return False
        
        return True
    
    def record_alert(self, token_mint: str):
        self.alerts_sent.append(datetime.now())
        self.alerted_tokens.add(token_mint)
        two_hours_ago = datetime.now() - timedelta(hours=2)
        self.alerts_sent = [t for t in self.alerts_sent if t > two_hours_ago]

alert_tracker = AlertTracker()

async def send_telegram_message(message: str, parse_mode: str = "HTML"):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID,
            text=message,
            parse_mode=parse_mode
        )
        logger.info("Alert sent successfully")
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")

async def send_trending_alert(token_data: dict):
    message = f"""
🧬 <b>TRENDING ALERT</b> 🧬

New token entering pump.fun trending!

🪙 <b>{token_data.get('name', 'Unknown')}</b> ({token_data.get('symbol', 'UNKNOWN')})
🔗 <code>{token_data.get('mint', 'N/A')}</code>
📈 MC: ${token_data.get('market_cap_usd', 0):,.2f}
💰 Volume: {token_data.get('volume_sol', 0):.2f} SOL (5min)
💧 Liquidity: ${token_data.get('liquidity_usd', 0):,.2f}
🔥 Holders: {token_data.get('holder_count', 0):,}
⏰ Age: {token_data.get('age_minutes', 0)} minutes
📊 Trending Rank: #{token_data.get('trending_rank', 'N/A')}

🔗 <a href="https://pump.fun/{token_data.get('mint', '')}">View on pump.fun</a>
📈 <a href="https://dexscreener.com/solana/{token_data.get('mint', '')}">View on Dexscreener</a>

Early opportunity? DYOR! 👀

<i>"Evolve or Die"</i> 🧬
- EVO Agents
"""
    await send_telegram_message(message)

async def send_volume_spike_alert(token_data: dict):
    message = f"""
🚨 <b>VOLUME SPIKE DETECTED</b> 🚨

Token pumping on pump.fun!

🪙 <b>${token_data.get('symbol', 'UNKNOWN')}</b>
📈 +{token_data.get('volume_change_percent', 0)}% volume (5min)
💰 Volume: {token_data.get('volume_sol', 0):.2f} SOL
📊 Buys: {token_data.get('buy_count', 0)} | Sells: {token_data.get('sell_count', 0)}
🐋 Buy/Sell Ratio: {token_data.get('buy_sell_ratio', 0):.2f}
📈 MC: ${token_data.get('market_cap_usd', 0):,.2f}
⏰ Age: {token_data.get('age_minutes', 0)} minutes

Bonding curve: {token_data.get('bonding_curve_percent', 0):.1f}%

Might pump soon! ⏰

DYOR! NFA! 🧬
"""
    await send_telegram_message(message)

async def send_fast_mover_alert(token_data: dict):
    message = f"""
🚀 <b>FAST MOVER DETECTED</b> 🚀

Token pumping hard!

🪙 <b>${token_data.get('symbol', 'UNKNOWN')}</b>
📈 +{token_data.get('price_change_percent', 0)}% in 5 minutes
💰 MC: ${token_data.get('market_cap_usd_old', 0):,.2f} → ${token_data.get('market_cap_usd', 0):,.2f}
🔥 Volume: ${token_data.get('volume_usd', 0):,.2f} (5min)
📊 Holders: {token_data.get('holder_count', 0):,} (+{token_data.get('holder_change', 0)})
⏰ Age: {token_data.get('age_minutes', 0)} minutes

🔗 <a href="https://pump.fun/{token_data.get('mint', '')}">View on pump.fun</a>

Catch the momentum! 👀

DYOR! 🧬
"""
    await send_telegram_message(message)

async def send_graduation_alert(token_data: dict):
    message = f"""
🎓 <b>GRADUATION ALERT</b> 🎓

Token graduating from pump.fun!

🪙 <b>${token_data.get('symbol', 'UNKNOWN')}</b>
📈 MC: ${token_data.get('market_cap_usd', 0):,.2f}
💧 LP migrating to Raydium
⏰ Graduation in: ~{token_data.get('time_to_graduation', 5)} minutes
📊 Bonding curve: {token_data.get('bonding_curve_percent', 0):.1f}%

🔥 Holders: {token_data.get('holder_count', 0):,}
💰 Volume: {token_data.get('volume_sol', 0):.2f} SOL

Historical grad performance:
• Average 1h post-grad: +40%
• Success rate: ~65%

Watch for entry opportunity! 👀

"Evolve or Die" 🧬
"""
    await send_telegram_message(message)

async def send_hourly_recap(top_tokens: list):
    message = f"""
🧬 <b>HOURLY TRENDING RECAP</b> 🧬
🕐 {datetime.now().strftime('%H:%00 GMT+7')}

Top {len(top_tokens)} trending tokens (last hour):

"""
    for i, token in enumerate(top_tokens[:5], 1):
        message += f"""
{i}. <b>${token.get('symbol', 'UNKNOWN')}</b>
   📈 MC: ${token.get('market_cap_usd', 0):,.0f}
   💰 Vol: {token.get('volume_sol', 0):.1f} SOL
   🔥 Holders: {token.get('holder_count', 0):,}
"""
    message += """

<i>Stay ahead of the curve!</i> 👀

DYOR always! 🧬
- EVO Agents
"""
    await send_telegram_message(message)

async def fetch_trending_tokens():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{PUMP_FUN_API}/coins/trending") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('coins', [])
                else:
                    logger.warning(f"Failed to fetch trending: {response.status}")
                    return []
    except Exception as e:
        logger.error(f"Error fetching trending tokens: {e}")
        return []

async def analyze_token(token_data: dict) -> dict:
    analysis = {
        'should_alert': False,
        'alert_type': None,
        'reason': []
    }
    volume_sol = token_data.get('volume_sol', 0)
    if volume_sol >= MIN_VOLUME_SOL:
        analysis['should_alert'] = True
        analysis['alert_type'] = 'trending'
        analysis['reason'].append(f'High volume: {volume_sol:.2f} SOL')
    holders = token_data.get('holder_count', 0)
    if holders >= MIN_HOLDERS:
        analysis['should_alert'] = True
        if not analysis['alert_type']:
            analysis['alert_type'] = 'trending'
        analysis['reason'].append(f'Good holders: {holders}')
    age_minutes = token_data.get('age_minutes', 999)
    if age_minutes > MAX_AGE_MINUTES:
        analysis['should_alert'] = False
    liquidity = token_data.get('liquidity_usd', 0)
    if liquidity < MIN_LIQUIDITY_USD:
        analysis['should_alert'] = False
    bonding_curve = token_data.get('bonding_curve_percent', 0)
    if bonding_curve >= 90:
        analysis['alert_type'] = 'graduation'
        analysis['reason'].append(f'Graduation imminent: {bonding_curve:.1f}%')
    volume_change = token_data.get('volume_change_percent', 0)
    if volume_change >= VOLUME_SPIKE_PERCENT:
        analysis['alert_type'] = 'volume_spike'
        analysis['reason'].append(f'Volume spike: +{volume_change}%')
    price_change = token_data.get('price_change_percent', 0)
    if price_change >= 100:
        analysis['alert_type'] = 'fast_mover'
        analysis['reason'].append(f'Fast mover: +{price_change}%')
    return analysis

async def monitor_loop():
    logger.info("Starting EVO Pump.fun Monitor Bot...")
    logger.info(f"Telegram Channel: {TELEGRAM_CHANNEL_ID}")
    logger.info(f"Check interval: {CHECK_INTERVAL_SECONDS}s")
    await send_telegram_message("""
🧬 <b>EVO ALERT BOT STARTED</b> 🧬

Bot is now monitoring pump.fun for:
✅ Trending tokens
✅ Volume spikes
✅ Fast movers
✅ Graduation alerts

Thresholds:
• Min Volume: 10 SOL
• Min Holders: 50
• Max Age: 30 min
• Max Alerts/Hour: 10

Standby for alpha! 👀

"Evolve or Die" 🧬
- EVO Agents
""")
    last_recap_time = datetime.now()
    while True:
        try:
            trending_tokens = await fetch_trending_tokens()
            logger.info(f"Fetched {len(trending_tokens)} trending tokens")
            for token in trending_tokens[:20]:
                if not alert_tracker.can_alert(token.get('mint', '')):
                    continue
                analysis = await analyze_token(token)
                if analysis['should_alert']:
                    if analysis['alert_type'] == 'trending':
                        await send_trending_alert(token)
                    elif analysis['alert_type'] == 'volume_spike':
                        await send_volume_spike_alert(token)
                    elif analysis['alert_type'] == 'fast_mover':
                        await send_fast_mover_alert(token)
                    elif analysis['alert_type'] == 'graduation':
                        await send_graduation_alert(token)
                    alert_tracker.record_alert(token.get('mint', ''))
                    logger.info(f"Alert sent for {token.get('symbol')}: {analysis['alert_type']}")
            if datetime.now() - last_recap_time >= timedelta(hours=1):
                await send_hourly_recap(trending_tokens)
                last_recap_time = datetime.now()
            await asyncio.sleep(CHECK_INTERVAL_SECONDS)
        except Exception as e:
            logger.error(f"Error in monitor loop: {e}")
            await asyncio.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        asyncio.run(monitor_loop())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
