import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")  # e.g., "Mclovvinssecret/myyweightloss"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def update_data_json(weight, bodyfat):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/data.json"

    # Get current file content
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return False, "Failed to fetch data.json"
    
    content = r.json()
    sha = content["sha"]
    data = json.loads(requests.get(content["download_url"]).text)

    # Append new data
    data["history"].append({
        "weight": weight,
        "bodyfat": bodyfat
    })

    # Commit new version
    new_content = json.dumps(data, indent=2)
    commit_msg = f"Update data: {weight}kg, {bodyfat}%"
    put_data = {
        "message": commit_msg,
        "content": new_content.encode("utf-8").decode("utf-8").encode("base64").decode("utf-8"),
        "sha": sha
    }
    response = requests.put(url, headers=headers, json=put_data)
    return response.status_code == 200, response.text

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    msg = request.json["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")

    if text.startswith("/update"):
        parts = text.split()
        if len(parts) != 3:
            reply = "Usage: /update <weight_kg> <bodyfat_%>"
        else:
            try:
                weight = float(parts[1])
                bodyfat = float(parts[2])
                ok, status = update_data_json(weight, bodyfat)
                reply = "✅ Data updated!" if ok else f"❌ Failed to update: {status}"
            except:
                reply = "❌ Invalid numbers. Usage: /update 50.3 15.2"
        
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params={
            "chat_id": chat_id,
            "text": reply
        })

    return "ok"
