# SOC Log Analyzer

A web-based tool that analyzes SSH authentication logs and detects brute force attacks and possible compromised logins, with a simple dashboard for SOC analysts.

**Live demo:** coming soon

## Features

- Upload an SSH `auth.log` file or try the built-in sample log
- Detects brute force attacks (5 or more failed logins from one IP)
- Flags suspicious repeated failures (3 or more failed logins from one IP)
- Flags possible compromised logins (successful login from an external IP after failed attempts)
- Shows usernames tried by each attacking IP
- Dashboard with stats cards, severity-based alerts table and a bar chart of failed logins by IP

## Tech Stack

- Python 3
- Flask
- Jinja2 templates
- Chart.js
- Gunicorn (production server)
- Deployed on Render

## Detection Rules

| Severity | Rule |
|----------|------|
| CRITICAL | Successful login from a public IP that had failed attempts before |
| HIGH | 5 or more failed logins from the same IP (brute force) |
| MEDIUM | 3 or 4 failed logins from the same IP |

## Run Locally

```
git clone https://github.com/Bhawna45/soc-log-analyzer.git
cd soc-log-analyzer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## Project Structure

```
soc-log-analyzer/
├── app.py            # Flask app and routes
├── analyzer.py       # Log parsing and detection logic
├── requirements.txt
├── templates/
│   └── index.html    # Dashboard page
└── sample_logs/
    └── auth.log      # Sample SSH log for testing
```

## Future Improvements

- Support for Apache/Nginx logs (SQL injection, port scan patterns)
- IP reputation lookup using AbuseIPDB
- Export alerts as CSV or PDF report
- Time-based detection (failures within a short window)

## Author

Mandeep, cyber security student and SOC enthusiast.