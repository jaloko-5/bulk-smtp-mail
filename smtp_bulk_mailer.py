#!/usr/bin/env python3
"""
SMTP Bulk Mailer (Python)

This script provides a simple way to send emails in bulk using an SMTP server.
Each message is sent individually with a configurable delay between sends,
which helps avoid being flagged as spam by email providers. The script reads
recipient addresses from a CSV file, constructs a basic text email and
sends it through a secure SSL/TLS connection. Credentials and server
parameters are read from environment variables.

Usage:
    1. Create a CSV file (e.g. ``recipients.csv``) containing one email
       address per line.
    2. Set the following environment variables:
           SMTP_SERVER   - SMTP server host name (e.g. ``smtp.gmail.com``)
           SMTP_PORT     - SMTP server port (e.g. ``465``)
           SMTP_USERNAME - Username/login for the SMTP server
           SMTP_PASSWORD - Password or app‑specific password
           SMTP_SENDER   - Address to appear in the ``From`` header
    3. Run the script:
           python smtp_bulk_mailer.py --subject "Hello" --body "This is a test" \
             --recipients recipients.csv --delay 2

The subject and body can also be provided via environment variables
``EMAIL_SUBJECT`` and ``EMAIL_BODY``. Delay defaults to 1 second.

Note: To comply with bulk email best practices, ensure that your
recipients have opted in to receive your emails and that your SMTP
provider allows sending in bulk. Adjust the delay as needed to stay
within rate limits and to avoid triggering spam filters.
"""

import csv
import os
import time
import ssl
import smtplib
import argparse
from email.message import EmailMessage


def send_bulk_emails(
    smtp_server: str,
    smtp_port: int,
    username: str,
    password: str,
    sender_email: str,
    subject: str,
    body: str,
    recipients_file: str,
    delay: float = 1.0,
) -> None:
    """Send a simple text email to a list of recipients.

    Args:
        smtp_server: Host name of the SMTP server.
        smtp_port: Port number for the SMTP server.
        username: Login name for the server.
        password: Password or app‑specific password.
        sender_email: Address to use in the ``From`` header.
        subject: Subject line of the email.
        body: Plain text body of the email.
        recipients_file: Path to a CSV file containing recipient email addresses.
        delay: Seconds to wait between sending messages.
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(username, password)
        with open(recipients_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row:
                    continue
                recipient = row[0].strip()
                if not recipient:
                    continue
                msg = EmailMessage()
                msg["Subject"] = subject
                msg["From"] = sender_email
                msg["To"] = recipient
                msg.set_content(body)
                try:
                    server.send_message(msg)
                    print(f"Sent to {recipient}")
                except Exception as exc:
                    print(f"Failed to send to {recipient}: {exc}")
                time.sleep(delay)



def main() -> None:
    parser = argparse.ArgumentParser(description="Send bulk emails over SMTP.")
    parser.add_argument(
        "--subject",
        default=os.environ.get("EMAIL_SUBJECT", "Bulk Email"),
        help="Subject line for the email. Can also be set via EMAIL_SUBJECT env var."
    )
    parser.add_argument(
        "--body",
        default=os.environ.get("EMAIL_BODY", "Hello, this is a bulk email."),
        help="Body of the email. Can also be set via EMAIL_BODY env var."
    )
    parser.add_argument(
        "--recipients",
        required=True,
        help="CSV file with recipient email addresses."
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=float(os.environ.get("EMAIL_DELAY", 1.0)),
        help="Delay between sending emails, in seconds. Defaults to 1."
    )
    args = parser.parse_args()

    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 465))
    username = os.environ.get("SMTP_USERNAME")
    password = os.environ.get("SMTP_PASSWORD")
    sender_email = os.environ.get("SMTP_SENDER", username)

    if not (username and password):
        raise SystemExit(
            "SMTP_USERNAME and SMTP_PASSWORD environment variables must be set."
        )

    send_bulk_emails(
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        username=username,
        password=password,
        sender_email=sender_email,
        subject=args.subject,
        body=args.body,
        recipients_file=args.recipients,
        delay=args.delay,
    )


if __name__ == "__main__":
    main()
