# Import datetime to get current time timestamps for our logs
from datetime import datetime
# Import random so the computer can pick different errors by chance
import random
# Import time so we can add short delays if needed
import time

# The log file we want to write into
LOG_FILE = "system_activity.log"

# A list of realistic IT errors and normal events
SAMPLE_EVENTS = [
    "INFO: User admin logged in successfully.",
    "INFO: Scheduled backup completed.",
    "WARNING: FAILED_LOGIN from IP 192.168.1.105",
    "ERROR: OUT_OF_MEMORY on Web-Server-02",
    "CRITICAL: SERVICE_DOWN - PaymentGatewayAPI not responding",
]


def generate_fake_logs(num_entries=10):
    # Open the log file in 'append' mode ('a') so we don't delete old lines
    with open(LOG_FILE, "a") as f:
        for _ in range(num_entries):
            # Pick a random event from our list
            event = random.choice(SAMPLE_EVENTS)

            # Get current timestamp
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Write the formatted log line to the file
            f.write(f"{now} {event}\n")

    print(f"Successfully added {num_entries} new events to {LOG_FILE}.")


# Run this when executing: python generate_logs.py
if __name__ == "__main__":
    generate_fake_logs(15)