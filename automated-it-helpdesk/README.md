# Automated IT Helpdesk & Event Log Incident Monitor

An automated IT support operations tool built with Python, SQLite, and Streamlit. The system continuously monitors application and server logs for critical system failures (such as brute-force failed logins, memory exhaustion, and service downtime), automatically logs support tickets in a local database, and presents an interactive incident queue for support technicians.

---

## Features

- **Automated Incident Logging:** Detects specific error patterns (`FAILED_LOGIN`, `OUT_OF_MEMORY`, `SERVICE_DOWN`) based on configurable threshold rules.
- **Relational Storage:** Stores all tickets with status tracking, timestamps, and priority levels using SQLite.
- **Technician Dashboard:** Interactive Streamlit web interface with real-time metrics, search filtering, and status progression (`Open` -> `In Progress` -> `Resolved`).
- **Manual Ticket Intake:** Self-service sidebar form allowing end users to submit general IT tickets.
- **Webhook Alert Support:** Integrated notification hook capable of pushing instant high-priority alerts to channels like Discord or Slack.

---

## Tech Stack

- **Language:** Python
- **Database:** SQLite
- **Frontend / Dashboard:** Streamlit
- **Data Manipulation:** pandas
- **Automation / Scripting:** Regular Expressions (`re`), `requests`

---

## How to Run Locally

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/automated-it-helpdesk.git](https://github.com/YOUR_USERNAME/automated-it-helpdesk.git)
cd automated-it-helpdesk