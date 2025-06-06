# AI Search Bot for Slack (Render Deployment)

This is a simple Slack bot that responds to `/ai-search [tag]` commands by searching recent messages with a matching emoji in a specified channel.

## Supported Tags
- ideas → :bulb:
- warnings → :warning:
- docs → :books:
- pinned → :pushpin:

## 🧪 To Deploy on Render
1. Fork or clone this repo.
2. Create a new Web Service on [https://render.com](https://render.com)
3. Connect your GitHub repo or upload manually.
4. Add the environment variable `SLACK_BOT_TOKEN`.
5. Set the path `/ai-search` as the endpoint in your Slack Slash Command.