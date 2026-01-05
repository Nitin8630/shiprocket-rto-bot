from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ========= ENV VARIABLES =========
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SHIPROCKET_TOKEN = os.getenv("SHIPROCKET_TOKEN")  # Optional, for validation
# =================================

def send_telegram_message(message: str):
    """Send message to Telegram chat."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("❌ Telegram send failed:", e)

@app.route('/')
def home():
    return "✅ Shiprocket Webhook Bot is running!"

@app.route('/shiprocket-webhook', methods=['POST'])
def shiprocket_webhook():
    """Handle Shiprocket webhook (must be POST and open access)."""
    data = request.get_json(silent=True)
    print("📦 Received Webhook:", data)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

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
        print("✅ Telegram message sent")

    return jsonify({"success": True}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
