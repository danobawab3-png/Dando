import time
import requests
from threading import Thread
from flask import Flask

# 1. نظام الويب لإبقاء السيرفر مستيقظاً على Render مجاناً
app = Flask('')
@app.route('/')
def home():
    return "البوت شغال 24 ساعة بنجاح ساحق!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# ⚠️ بيانات التلغرام الحقيقية الخاصة بك مدمجة وجاهزة تماماً
TELEGRAM_TOKEN = '8071465759:AAF4i_BK1vR-fH_q2fS7S6wWvHwY3M4mS0I'
CHAT_ID = '790982863'

SOLANA_BOOSTS_API = "https://dexscreener.com"
PAIRS_API = "https://dexscreener.com"
RUGCHECK_API = "https://rugcheck.xyz{}/report"

def send_to_telegram(text):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        res = requests.post(url, json=payload)
        print(f"Telegram status: {res.status_code}")
    except Exception as e:
        print(f"Telegram error: {e}")

def main_scanner_loop():
    print("🤖 بدأ محرك الفحص العمل بصفة رسمية...")
    seen_tokens = set()
    
    # 🔥 الإرسال الفوري المباشر: بمجرد الإقلاع وبدون انتظار الفلاتر للتأكد من نجاح الرابط
    send_to_telegram("🚀 *تم الاتصال بنجاح ساحق!* البوت حركي الآن ويراقب مجمعات سيولة Solana على مدار الساعة...")
    
    while True:
        try:
            res = requests.get(SOLANA_BOOSTS_API)
            if res.status_code == 200 and isinstance(res.json(), list):
                for token_data in res.json():
                    if token_data.get('chainId') != 'solana': continue
                    token_address = token_data.get('tokenAddress')
                    
                    if token_address in seen_tokens: continue
                    seen_tokens.add(token_address)
                    
                    # جلب تفاصيل التداول والسيولة للزوج
                    pair_res = requests.get(f"{PAIRS_API}{token_address}")
                    if pair_res.status_code != 200: continue
                    
                    pairs_list = pair_res.json().get('pairs', [])
                    if not pairs_list: continue
                    
                    # ✅ الإصلاح البرمجي الصحيح: أخذ المسبح الأول بدقة من القائمة عبر [0]
                    pair = pairs_list[0]
                    
                    # 🟢 فلتر 1: فحص السيولة والعمر
                    age_ms = time.time() - (pair.get('pairCreatedAt', 0) / 1000)
                    liquidity = pair.get('liquidity', {}).get('usd', 0)
                    if age_ms > 3600 or liquidity < 25000: continue
                    
                    # 🟢 فلتر 2: فحص حجم التداول والصفقات
                    vol_5m = pair.get('volume', {}).get('m5', 0)
                    vol_1h = pair.get('volume', {}).get('h1', 0)
                    tx_1h = pair.get('txns', {}).get('h1', {}).get('buys', 0) + pair.get('txns', {}).get('h1', {}).get('sells', 0)
                    if vol_5m < 15000 or vol_1h < 100000 or tx_1h < 500: continue
                    
                    # 🟢 فلتر 3: مصفوفة الأمان (RugCheck)
                    rug_res = requests.get(RUGCHECK_API.format(token_address))
                    if rug_res.status_code != 200: continue
                    rug_data = rug_res.json()
                    
                    if rug_data.get('mintAuthority') is not None or rug_data.get('freezeAuthority') is not None: continue
                    holders = rug_data.get('holders', [])[:10]
                    if sum([h.get('pct', 0) for h in holders]) >= 30: continue
                    
                    # 📢 بث الإشارة الحية الفورية إلى تلغرام
                    token_name = pair.get('baseToken', {}).get('name', 'Unknown')
                    price = pair.get('priceUsd', '0')
                    dex_url = f"https://dexscreener.com{token_address}"
                    
                    msg = (
                        f"🟢 *[تنفيذ أمر الدخول]*\n\n"
                        f"• *اسم العملة:* {token_name}\n"
                        f"• *العقد:* `{token_address}`\n"
                        f"• *السعر:* {price} USD\n\n"
                        f"🔗 *رابط الشارت:* [اضغط هنا لفتح DexScreener]({dex_url})"
                    )
                    send_to_telegram(msg)
        except Exception as e:
            print(f"خطأ مؤقت في الفحص: {e}")
        time.sleep(15)

if __name__ == "__main__":
    t = Thread(target=main_scanner_loop)
    t.start()
    run_web_server()
