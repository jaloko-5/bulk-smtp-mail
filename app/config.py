import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////workspace/mystrika_sim.db")
TIMEZONE = os.getenv("TIMEZONE", "UTC")

# Email sending simulation
SEND_REAL_EMAILS = os.getenv("SEND_REAL_EMAILS", "false").lower() == "true"
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# Warm-up and sending defaults
DAILY_WARMUP_START = int(os.getenv("DAILY_WARMUP_START", "5"))
DAILY_WARMUP_MAX = int(os.getenv("DAILY_WARMUP_MAX", "150"))
WARMUP_RAMP_DAYS = int(os.getenv("WARMUP_RAMP_DAYS", "30"))

# Dashboard settings
DASHBOARD_TITLE = os.getenv("DASHBOARD_TITLE", "Mystrika-Inspired Outreach Simulator")
