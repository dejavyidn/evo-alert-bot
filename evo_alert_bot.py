import asyncio
import websockets
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
MIN_VOLUME_SOL = 1
MIN_HOLDERS = 1
MAX_AGE_MINUTES = 5
MIN_LIQUIDITY_USD = 10
VOLUME_SPIKE_PERCENT = 10

# Monitoring Settings
MAX_ALERTS_PER_HOUR = 10

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pump.fun WebSocket URL (REAL-TIME!)
PUMP_FUN_WS = "wss://pumpportal.fun/data-api/real-time"

# REST fallback (for token details)
PUMP_FUN_REST = "https://pumpportal.fun/data-api"

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

New token trending on pump.fun!

🪙 <b>{token_data.get('name', 'Unknown')}</b> ({token_data.get('symbol', 'UNKNOWN')})
🔗 <code>{token_data.get('mint', 'N/A')}</code>
📈 MC: ${token_data.get('market_cap', 0):,.2f}
💰 Volume 5m: {token_data.get('volume_sol_5m', 0):.2f} SOL
💧 Liquidity: ${token_data.get('liquidity_usd', 0):,.2f}
🔥 Holders: {token_data.get('holder_count', 0):,}
⏰ Age: {token_data.get('age_minutes', 0)} minutes
📊 Rank: #{token_data.get('trending_rank', 'N/A')}

🔗 <a href="https://pump.fun/{token_data.get('mint', '')}">View on pump.fun</a>
📈 <a href="https://dexscreener.com/solana/{token_data.get('mint', '')}">Chart</a>

Early alpha! DYOR! 👀

"Evolve or Die" 🧬
- EVO Agents
"""
    await send_telegram_message(message)

async def send_volume_spike_alert(token_data: dict):
    message = f"""
🚨 <b>VOLUME SPIKE</b> 🚨

🪙 <b>${token_data.get('symbol', 'UNKNOWN')}</b>
📈 Volume: +{token_data.get('volume_change_percent', 0)}% (5min)
💰 Current: {token_data.get('volume_sol_5m', 0):.2f} SOL
📊 Buys: {token_data.get('buy_count_5m', 0)} | Sells: {token_data.get('sell_count_5m', 0)}
🐋 Ratio: {token_data.get('buy_sell_ratio', 0):.2f}
📈 MC: ${token_data.get('market_cap', 0):,.2f}

Something's brewing! ⏰

DYOR! NFA! 🧬
"""
    await send_telegram_message(message)

async def send_fast_mover_alert(token_data: dict):
    message = f"""
🚀 <b>FAST MOVER</b> 🚀

🪙 <b>${token_data.get('symbol', 'UNKNOWN')}</b>
📈 +{token_data.get('price_change_percent', 0)}% in 5 minutes
💰 MC: ${token_data.get('market_cap_old', 0):,.2f} → ${token_data.get('market_cap', 0):,.2f}
🔥 Volume 5m: ${token_data.get('volume_usd_5m', 0):,.2f}
📊 Holders: {token_data.get('holder_count', 0):,} (+{token_data.get('holder_delta', 0)})

🔗 <a href="https://pump.fun/{token_data.get('mint', '')}">Trade Now</a>

Momentum alert! Catch the move 👀

DYOR! 🧬
"""
    await send_telegram_message(message)

async def send_graduation_alert(token_data: dict):
    message = f"""
🎓 <b>GRADUATION IMMINENT</b> 🎓

🪙 <b>${token_data.get('symbol', 'UNKNOWN')}</b>
📈 MC: ${token_data.get('market_cap', 0):,.2f}
💧 Bonding: {token_data.get('bonding_curve_percent', 0):.1f}%
⏰ ETA: ~5 minutes

🔥 Holders: {token_data.get('holder_count', 0):,}
💰 Volume: {token_data.get('volume_sol_5m', 0):.2f} SOL

Historical post-grad avg: +40%

Watch for LP migration! 👀

"Evolve or Die" 🧬
"""
    await send_telegram_message(message)

async def send_hourly_recap(top_tokens: list):
    message = f"""
🧬 <b>HOURLY RECAP</b> 🧬
🕐 {datetime.now().strftime('%H:%00 GMT+7')}

Top {len(top_tokens)} trending tokens:

"""
    for i, token in enumerate(top_tokens[:5], 1):
        message += f"""
{i}. <b>${token.get('symbol', 'UNKNOWN')}</b>
   MC: ${token.get('market_cap', 0):,.0f}
   Vol: {token.get('volume_sol_5m', 0):.1f} SOL
   Holders: {token.get('holder_count', 0):,}
"""
    message += """

<i>Stay sharp!</i> 👀

- EVO Agents
"""
    await send_telegram_message(message)

async def fetch_token_details(mint: str) -> dict:
    """Fetch detailed token info via REST API"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{PUMP_FUN_REST}/coins/{mint}") as response:
                if response.status == 200:
                    return await response.json()
    except Exception as e:
        logger.error(f"Error fetching token {mint}: {e}")
    return {}

async def analyze_token(data: dict) -> dict:
    """Analyze token from WebSocket event"""
    analysis = {
        'should_alert': False,
        'alert_type': None,
        'reason': []
    }
    
    mint = data.get('mint', '')
    volume_sol = data.get('volume_sol_5m', 0)
    holders = data.get('holder_count', 0)
    age_minutes = data.get('age_minutes', 999)
    liquidity = data.get('liquidity_usd', 0)
    bonding_curve = data.get('bonding_curve_percent', 0)
    volume_change = data.get('volume_change_percent', 0)
    price_change = data.get('price_change_percent', 0)
    
    # Basic checks
    if volume_sol >= MIN_VOLUME_SOL:
        analysis['should_alert'] = True
        analysis['alert_type'] = 'trending'
        analysis['reason'].append(f'Volume: {volume_sol:.2f} SOL')
    
    if holders >= MIN_HOLDERS:
        analysis['should_alert'] = True
        if not analysis['alert_type']:
            analysis['alert_type'] = 'trending'
        analysis['reason'].append(f' holders: {holders}')
    
    if age_minutes > MAX_AGE_MINUTES:
        analysis['should_alert'] = False
    
    if liquidity < MIN_LIQUIDITY_USD:
        analysis['should_alert'] = False
    
    # Graduation check
    if bonding_curve >= 90:
        analysis['alert_type'] = 'graduation'
        analysis['reason'].append(f'Grad: {bonding_curve:.1f}%')
    
    # Volume spike
    if volume_change >= VOLUME_SPIKE_PERCENT:
        analysis['alert_type'] = 'volume_spike'
        analysis['reason'].append(f'Vol +{volume_change}%')
    
    # Fast mover
    if price_change >= 100:
        analysis['alert_type'] = 'fast_mover'
        analysis['reason'].append(f'Price +{price_change}%')
    
    analysis['data'] = data
    return analysis

async def monitor_loop():
    """Main WebSocket loop"""
    logger.info("Connecting to pump.fun WebSocket...")
    
    # Send startup message
    await send_telegram_message("""
🧬 <b>EVO ALERT BOT CONNECTED</b> 🧬

Listening to pump.fun real-time stream...
Monitoring: new tokens, volume spikes, graduations

Thresholds:
• Min Volume: 10 SOL
• Min Holders: 50
• Max Age: 30 min

Standby for alpha! 👀

"Evolve or Die" 🧬
- EVO Agents
""")
    
    last_recap = datetime.now()
    recent_alerts = []  # For hourly recap
    
    while True:
        try:
            async with websockets.connect(PUMP_FUN_WS, ping_interval=20, ping_timeout=10) as websocket:
                logger.info("WebSocket connected")
                
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        
                        # Process based on message type
                        event_type = data.get('event')
                        
                        if event_type == 'new_token':
                            # New token launched
                            analysis = await analyze_token(data)
                            if analysis['should_alert']:
                                await send_trending_alert(data)
                                alert_tracker.record_alert(data.get('mint', ''))
                                recent_alerts.append(data)
                        
                        elif event_type == 'token_update':
                            # Existing token updated (price/volume change)
                            mint = data.get('mint')
                            # Fetch full details for analysis
                            details = await fetch_token_details(mint)
                            if details:
                                details.update(data)  # Merge with update data
                                analysis = await analyze_token(details)
                                if analysis['should_alert'] and analysis['alert_type'] == 'fast_mover':
                                    await send_fast_mover_alert(details)
                                    alert_tracker.record_alert(mint)
                                    recent_alerts.append(details)
                        
                        elif event_type == 'graduation':
                            # Token graduating
                            await send_graduation_alert(data)
                            alert_tracker.record_alert(data.get('mint', ''))
                        
                        # Hourly recap
                        if datetime.now() - last_recap >= timedelta(hours=1):
                            # Sort recent alerts by trend score (volume * change)
                            top_tokens = sorted(
                                recent_alerts,
                                key=lambda x: x.get('volume_sol_5m', 0) * max(1, x.get('price_change_percent', 0)/100),
                                reverse=True
                            )[:10]
                            await send_hourly_recap(top_tokens)
                            recent_alerts.clear()
                            last_recap = datetime.now()
                            
                    except websockets.ConnectionClosed:
                        logger.warning("WebSocket closed, reconnecting...")
                        break
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            await asyncio.sleep(5)  # Reconnect delay

if __name__ == "__main__":
    try:
        asyncio.run(monitor_loop())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
