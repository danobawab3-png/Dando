import time
import requests
from threading import Thread
from flask import Flask

# 1. نظام الويب لإبقاء السيرفر مستيقظاً على Render مجاناً
app = Flask('')
@app.route('/')
def home():
    return "تم إصلاح الثغرة البرمجية والبوت يعمل الآن 24 ساعة بنجاح!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# ⚠️ بيانات التلغرام الحقيقية والمصلحة الخاصة بك
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
        print(f"استجابة تلغرام: {res.status_code}")
    except Exception as e:
        print(f"خطأ إرسال تلغرام: {e}")

def main_scanner_loop():
    print("🤖 تم تشغيل محرك الكسح المصلح والمضمون لشبكة Solana...")
    seen_tokens = set()
    
    # 💥 الإرسال الفوري المضمون لإثبات نجاح الاتصال وتفعيل البوت
    send_to_telegram("🔔 *تحديث حاسم:* تم إصلاح ثغرة القراءة البرمجية بنجاح 100%! خط الإرسال السحابي مستيقظ ويقنص الصفقات الحية الآن...")
    
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
                    
                    # ✅ الإصلاح الجذري: أخذ العنصر الأول من القائمة لتجنب الانهيار
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
                    
                    # 🟢 فلتر 3: فحص الأمان الحصين (RugCheck)
                    rug_res = requests.get(RUGCHECK_API.format(token_address))
                    if rug_res.status_code != 200: continue
                    rug_data = rug_res.json()
                    
                    if rug_data.get('mintAuthority') is not None or rug_data.get('freezeAuthority') is not None: continue
                    holders = rug_data.get('holders', [])[:10]
                    if sum([h.get('pct', 0) for h in holders]) >= 30: continue
                    
                    # 📢 بث الإشارة الحية الفورية بالتنسيق الجديد
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
