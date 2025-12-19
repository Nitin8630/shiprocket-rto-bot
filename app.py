from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ========== CONFIG ==========
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SHIPROCKET_TOKEN = os.getenv("SHIPROCKET_TOKEN")  # your secret for webhook verification
# =============================

def send_telegram_message(message):
    """Send a message to your Telegram chat."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

@app.route('/')
def home():
    return "✅ Shiprocket Webhook Bot is running!"

@app.route('/shiprocket-webhook', methods=['POST'])
def shiprocket_webhook():
    """Receive webhook updates from Shiprocket."""
    data = request.get_json()
    print("📦 Webhook Data:", data)

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # 1️⃣ Verify the token
    received_token = data.get("token")
    if received_token != SHIPROCKET_TOKEN:
        print("❌ Invalid token received!")
        return jsonify({"error": "Unauthorized"}), 403

    # 2️⃣ Process RTO orders
    order_id = data.get("order_id")
    status = data.get("status", "")
    courier = data.get("courier_name", "Unknown")

    if "rto" in status.lower():
        message = (
            f"⚠️ RTO Alert!\n"
            f"Order ID: {order_id}\n"
            f"Courier: {courier}\n"
            f"Status: {status}"
        )
        send_telegram_message(message)
        print("✅ Telegram message sent!")

    return jsonify({"success": True}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
