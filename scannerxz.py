import time
import requests
from threading import Thread
from flask import Flask

app = Flask('')
@app.route('/')
def home():
    return "بوت قنص السيولة الحية يعمل بنجاح!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# بيانات التلغرام الصحيحة الخاصة بك
TELEGRAM_TOKEN = '8071465759:AAF4i_BK1vR-fH_q2fS7S6wWvHwY3M4mS0I'
CHAT_ID = '790982863'

SOLANA_BOOSTS_API = "https://api.dexscreener.com/token-boosts/latest/v1"
PAIRS_API = "https://dexscreener.com"

def send_to_telegram(text):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        res = requests.post(url, json=payload)
        print(f"Telegram Request Sent: {res.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def main_scanner_loop():
    print("🤖 بدأ محرك الكسح السريع...")
    seen_tokens = set()
    
    # محاولة إرسال متكررة ومضمونة للاختبار فور الإقلاع
    for i in range(3):
        send_to_telegram(f"🔔 *فحص اتصال رقم {i+1}:* البوت شغال والربط مستقر تماماً! جاري ضخ الصفقات...")
        time.sleep(2)
        
    while True:
        try:
            res = requests.get(SOLANA_BOOSTS_API)
            if res.status_code == 200 and isinstance(res.json(), list):
                for token_data in res.json():
                    if token_data.get('chainId') != 'solana': continue
                    token_address = token_data.get('tokenAddress')
                    
                    if token_address in seen_tokens: continue
                    seen_tokens.add(token_address)
                    
                    pair_res = requests.get(f"{PAIRS_API}{token_address}")
                    if pair_res.status_code != 200: continue
                    
                    pairs_list = pair_res.json().get('pairs', [])
                    if not pairs_list: continue
                    
                    pair = pairs_list[0]
                    
                    # 🟢 تعديل ذكي: فلاتر مرنة وفورية جداً للاختبار والتأكد من وصول الصفقات
                    liquidity = pair.get('liquidity', {}).get('usd', 0)
                    if liquidity < 5000: continue # خفضنا السيولة لـ 5 آلاف فقط لنصطاد سريعاً
                    
                    token_name = pair.get('baseToken', {}).get('name', 'Unknown')
                    price = pair.get('priceUsd', '0')
                    dex_url = f"https://dexscreener.com{token_address}"
                    
                    msg = (
                        f"🟢 *[تنفيذ أمر الدخول - إشارة حية]*\n\n"
                        f"• *اسم العملة:* {token_name}\n"
                        f"• *العقد:* `{token_address}`\n"
                        f"• *السعر:* {price} USD\n\n"
                        f"🔗 *رابط الشارت:* [اضغط هنا لفتح DexScreener]({dex_url})"
                    )
                    send_to_telegram(msg)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(10)

if __name__ == "__main__":
    t = Thread(target=main_scanner_loop)
    t.start()
    run_web_server()
