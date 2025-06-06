from flask import Flask, request
import requests
import os

app = Flask(__name__)

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
CHANNEL = "#may-the-ai-be-with-you"
HEADERS = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
}

EMOJI_MAP = {
    "ideas": ":bulb:",
    "warnings": ":warning:",
    "docs": ":books:",
    "pinned": ":pushpin:"
}

@app.route("/ai-search", methods=["POST"])
def ai_search():
    data = request.form
    query = data.get("text", "").strip().lower()
    response_url = data.get("response_url")

    emoji = EMOJI_MAP.get(query, ":bulb:")
    search_query = f"in:{CHANNEL} {emoji}"

    r = requests.get("https://slack.com/api/search.messages", headers=HEADERS, params={
        "query": search_query,
        "count": 5
    })

    if not r.ok:
        return "Error querying Slack API", 500

    results = r.json()
    messages = results.get("messages", {}).get("matches", [])

    if not messages:
        reply = f"No results found for `{query}` in {CHANNEL}."
    else:
        reply = f"*Top results for `{query}`:*\n"
        for msg in messages:
            text = msg.get("text", "")[:80].replace("\n", " ")
            permalink = msg.get("permalink", "#")
            reply += f"• <{permalink}|View Message>: _{text}_\n"

    requests.post(response_url, json={"text": reply})
    return "", 200