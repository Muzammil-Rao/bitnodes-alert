import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def get_bitnodes_count():
    try:
        response = requests.get("https://bitnodes.io/api/v1/snapshots/latest/")
        data = response.json()
        return data["total_nodes"]
    except Exception as e:
        print("Error fetching nodes:", e)
        return None

last_node_count = None

while True:
    current_count = get_bitnodes_count()
    if current_count is None:
        time.sleep(60)
        continue

    if last_node_count is None:
        last_node_count = current_count
        send_telegram_alert(f"🔄 Monitoring started. Current nodes: {current_count}")
    else:
        if abs(current_count - last_node_count) >= 100:
            direction = "📈 Increase" if current_count > last_node_count else "📉 Decrease"
            send_telegram_alert(f"{direction} detected!\nPrevious: {last_node_count}\nCurrent: {current_count}")
            last_node_count = current_count

    time.sleep(300)  # check every 5 minutes
