# Import os so we can check if files exist on the computer
import os

# Import re (regular expressions) to search for specific words inside text lines
import re

# Import requests so Python can send web messages (like Discord or Slack webhooks)
import requests

# Import our create_ticket function from the ticket_manager file we made earlier
from ticket_manager import create_ticket

# If you have a Discord or Slack webhook URL, paste it between the quotes
WEBHOOK_URL = ""

# The name of the log text file we want to read and inspect
LOG_FILE = "system_activity.log"

# Rules for what to look for:
# - category: what group it belongs to
# - priority: how dangerous it is
# - threshold: how many times it must happen before making a ticket
PATTERNS = {
    "FAILED_LOGIN": {
        "category": "Security",
        "priority": "High",
        "threshold": 3,
    },
    "OUT_OF_MEMORY": {
        "category": "Hardware",
        "priority": "Critical",
        "threshold": 1,
    },
    "SERVICE_DOWN": {
        "category": "Infrastructure",
        "priority": "High",
        "threshold": 1,
    },
}


def send_webhook_alert(title, priority):
    # If no webhook URL is set, just stop and do nothing
    if not WEBHOOK_URL:
        return

    # Prepare the message text that will show up in Discord/Slack
    payload = {"content": f"🚨 **IT Alert [{priority}]**: {title}"}

    try:
        # Send an HTTP POST request with our message to the webhook link
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        # If the internet fails or the link is bad, print the error instead of crashing
        print(f"Webhook failed: {e}")


def scan_log():
    # If the log file does not exist yet, warn us and stop
    if not os.path.exists(LOG_FILE):
        print(f"Waiting for {LOG_FILE} to be created...")
        return

    # Open and read all lines from the log file
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    # Create a counter for each error word, starting at 0
    # Example: {"FAILED_LOGIN": 0, "OUT_OF_MEMORY": 0, "SERVICE_DOWN": 0}
    event_counts = {k: 0 for k in PATTERNS}

    # Go through every line in the log file one by one
    for line in lines:
        for event in PATTERNS:
            # If the error word is found inside this line, add 1 to its count
            if re.search(event, line):
                event_counts[event] += 1

    # Check if any error happened enough times to trigger a ticket
    for event, count in event_counts.items():
        config = PATTERNS[event]

        # If the count is equal to or greater than our threshold limit
        if count >= config["threshold"]:
            # Make a clear ticket title explaining the problem
            ticket_title = (
                f"Automated Incident: {event} detected ({count} occurrences)"
            )

            # Save the ticket into our database
            ticket_id = create_ticket(
                title=ticket_title,
                category=config["category"],
                priority=config["priority"],
                source="LogMonitorDaemon",  # Tells us this was made by our bot, not a human
            )

            # Print to terminal so we can see it working
            print(f"[!] Created Ticket #{ticket_id}: {ticket_title}")

            # Send a notification message to Discord/Slack
            send_webhook_alert(ticket_title, config["priority"])


# Run this when you run: python log_monitor.py
if __name__ == "__main__":
    scan_log()