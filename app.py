from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# Telegram Bot Details
BOT_TOKEN = "8058949440:AAG1_z41ml8IwIPaZe1eaB3DNeSpD1_I8uQ"
SEARCH_CHANNEL_ID = "-1003847474748"  # Update this to your actual search channel ID
FORWARD_CHANNEL_USERNAME = "@new_new_akay"  # Update this to your actual forward channel username

# Get Updates URL
GET_UPDATES_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

# Search Function
def search_movie_in_channel(movie_name):
    search_url = f"https://t.me/s/{SEARCH_CHANNEL_ID[1:]}"
    response = requests.get(search_url)
    return movie_name.lower() in response.text.lower()

# Forward Function
def forward_message(message_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/forwardMessage"
    params = {
        "chat_id": FORWARD_CHANNEL_USERNAME,
        "from_chat_id": SEARCH_CHANNEL_ID,
        "message_id": message_id
    }
    requests.post(url, params=params)

# Get Direct Link Function
def get_direct_link():
    response = requests.get(GET_UPDATES_URL)
    updates = response.json().get("result", [])
    for update in reversed(updates):
        if "channel_post" in update and update["channel_post"]["chat"]["username"] == FORWARD_CHANNEL_USERNAME[1:]:
            return f"https://t.me/{FORWARD_CHANNEL_USERNAME[1:]}/{update['channel_post']['message_id']}"
    return None

# API Endpoint
@app.route('/search_movie', methods=['POST'])
def search_movie():
    data = request.json
    movie_name = data.get("movie_name")

    if search_movie_in_channel(movie_name):
        message_id = 12345  # Replace this with the actual message ID based on your logic
        forward_message(message_id)
        time.sleep(2)
        
        # Get the direct link after forwarding
        link = get_direct_link()
        if link:
            return jsonify({"status": "success", "link": link}), 200
        return jsonify({"status": "error", "message": "Link not found"}), 404
    return jsonify({"status": "error", "message": "Movie not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
