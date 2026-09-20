import time
import requests
from threading import Thread
from flask import Flask

# 1. نظام إبقاء السيرفر مستيقظاً دائماً على Render مجاناً
app = Flask('')
@app.route('/')
def home():
    return "البوت شغال 24 ساعة بأمان بنجاح!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# ⚠️ بيانات التلغرام الحقيقية الخاصة بك مدمجة وجاهزة تماماً
TELEGRAM_TOKEN = '8071465759:AAF4i_BK1vR-fH_q2fS7S6wWvHwY3M4mS0I'
CHAT_ID = '790982863'

DEX_API = "https://dexscreener.com"
PAIRS_API = "https://dexscreener.com"
RUGCHECK_API = "https://rugcheck.xyz{}/report"

def send_to_telegram(text):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    except: pass

def main_scanner_loop():
    print("🤖 بدأ البوت بمراقبة شبكة Solana بتعديلات الزخم الذكية...")
    seen_tokens = set()
    while True:
        try:
            res = requests.get(DEX_API)
            if res.status_code == 200:
                for profile in res.json():
                    if profile.get('chainId') != 'solana': continue
                    token_address = profile.get('tokenAddress')
                    if token_address in seen_tokens: continue
                    seen_tokens.add(token_address)
                    
                    pair_res = requests.get(f"{PAIRS_API}{token_address}")
                    if pair_res.status_code != 200 or not pair_res.json().get('pairs'): continue
                    pair = pair_res.json()['pairs']
                    
                    # 🟢 فلتر 1: فحص العمر والسيولة (عقد < ساعة | سيولة >= 25k)
                    age_ms = time.time() - (pair.get('pairCreatedAt', 0) / 1000)
                    liquidity = pair.get('liquidity', {}).get('usd', 0)
                    if age_ms > 3600 or liquidity < 25000: continue
                    
                    # 🟢 فلتر 2: فحص الزخم العضوي المتوازن (فتح السقف الأعلى للـ 5 دقائق)
                    vol_5m = pair.get('volume', {}).get('m5', 0)
                    vol_1h = pair.get('volume', {}).get('h1', 0)
                    tx_1h = pair.get('txns', {}).get('h1', {}).get('buys', 0) + pair.get('txns', {}).get('h1', {}).get('sells', 0)
                    
                    if vol_5m < 15000 or vol_1h < 100000 or tx_1h < 500: continue
                    
                    # 🟢 فلتر 3: مصفوفة الأمان الحصين (RugCheck)
                    rug_res = requests.get(RUGCHECK_API.format(token_address))
                    if rug_res.status_code != 200: continue
                    rug_data = rug_res.json()
                    
                    # منع الصلاحيات الخطرة (Mint و Freeze يجب أن تكون ملغاة تماماً)
                    if rug_data.get('mintAuthority') is not None or rug_data.get('freezeAuthority') is not None: continue
                    
                    # فحص نسبة استحواذ أول 10 محافظ (أقل من 30% لتناسب واقع السوق الحقيقي)
                    holders = rug_data.get('holders', [])[:10]
                    if sum([h.get('pct', 0) for h in holders]) >= 30: continue
                    
                    # 📢 إرسال التنبيه الفوري مع رابط الشارت السريع
                    token_name = pair.get('baseToken', {}).get('name', 'Unknown')
                    price = pair.get('priceUsd', '0')
                    dex_url = f"https://dexscreener.com{token_address}"
                    
                    msg = (
                        f"🟢 *[تنفيذ أمر الدخول]*\n"
                        f"• *اسم العملة:* {token_name}\n"
                        f"• *العقد (CA):* `{token_address}`\n"
                        f"• *سعر الدخول:* \\${price}\n"
                        f"• *رابط الشارت:* [اضغط هنا لفتح DexScreener]({dex_url})"
                    )
                    send_to_telegram(msg)
        except: pass
        time.sleep(15)

if __name__ == "__main__":
    t = Thread(target=main_scanner_loop)
    t.start()
    run_web_server()
