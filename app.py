from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 從 Render 設定的環境變數中讀取
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

@app.route('/')
def home():
    return "✅ Flask is working on Render!"

@app.route('/trade', methods=['GET', 'POST'])
def receive_trade():
    if request.method == 'POST':
        direction = request.form.get('direction')
        price = request.form.get('price')
    else:
        direction = request.args.get('direction')
        price = request.args.get('price')

    if direction and price:
        message = f"📢 *AutoTradeX 交易訊號*\n➡️ 方向：*{direction}*\n💰 價格：*{price}*"
        send_telegram_message(message)
        return '✅ 訊息已發送'
    else:
        return '❗ 缺少參數 direction 或 price', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
