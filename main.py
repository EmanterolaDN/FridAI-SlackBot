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
    "ideas": [":bulb:", ":bombilla:"],
    "warnings": [":warning:", ":advertencia:"],
    "docs": [":books:", ":libros:"],
    "loud": [":loudspeaker:", ":altavoz_sonando:"],
    "hilo": [":thread:", ":hilo:"],
    "pinned": [":pushpin:", ":chincheta:"]
}

@app.route("/ai-search", methods=["POST"])
def ai_search():
    data = request.form
    query = data.get("text", "").strip().lower()
    response_url = data.get("response_url")

    emojis = EMOJI_MAP.get(query, [":bulb:"])
    search_query = f"in:{CHANNEL} " + " OR ".join(emojis)

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
 
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)