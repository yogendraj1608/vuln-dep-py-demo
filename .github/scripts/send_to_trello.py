import os
import json
import requests

# Read alerts passed from GitHub Action
import sys

if len(sys.argv) < 2:
    print("Missing alerts JSON input")
    sys.exit(1)

alerts_json = sys.argv[1]
try:
    alerts = json.loads(alerts_json)
except json.JSONDecodeError:
    print("Invalid JSON received")
    sys.exit(1)

# Trello credentials from GitHub secrets
TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_LIST_ID = os.getenv("TRELLO_LIST_ID")

if not all([TRELLO_KEY, TRELLO_TOKEN, TRELLO_LIST_ID]):
    print("Missing required environment variables.")
    sys.exit(1)

# Trello API endpoint
TRELLO_API = "https://api.trello.com/1/cards"

for alert in alerts:
    title = f"🔒 Dependabot Alert: {alert.get('secret_type', 'Unknown')}"
    desc = f"""
**Repository:** {alert.get('repository', {}).get('full_name', 'N/A')}
**Secret Type:** {alert.get('secret_type')}
**Secret:** {alert.get('secret')}
**Created At:** {alert.get('created_at')}
**State:** {alert.get('state')}
**URL:** {alert.get('html_url', 'N/A')}
"""

    payload = {
        "name": title,
        "desc": desc.strip(),
        "idList": TRELLO_LIST_ID,
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    response = requests.post(TRELLO_API, params=payload)

    if response.status_code == 200:
        print(f"✅ Trello card created: {title}")
    else:
        print(f"❌ Failed to create card: {response.status_code}, {response.text}")
