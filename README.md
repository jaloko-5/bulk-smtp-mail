# bulk‑smtp‑mail

This repository contains sample scripts for sending email messages in bulk
via an SMTP server without being flagged as spam. Two implementations
are provided:

* **Python** – `smtp_bulk_mailer.py` uses the built‑in `smtplib` library to send plain text messages over a secure SSL/TLS connection. It reads recipient addresses from a CSV file and sends each email sequentially with a configurable delay.
* **Node.js** – `smtpMailer.js` leverages the popular `nodemailer` package to send messages. Recipients are read from a newline‑separated text file, and you can send both plain text and HTML bodies.

> ⚠️ **Important**: Always ensure that your recipients have opted in to
> receive your emails and comply with your SMTP provider’s sending
> policies. Sending unsolicited bulk email can result in your account
> being suspended or blacklisted.

## Features

* Sends messages individually to each recipient
* Configurable delay between sends to respect rate limits
* Credentials and configuration via environment variables
* Simple usage with minimal dependencies

## Getting Started

### 1. Clone or download this repository

You can either clone the repo via Git or download the ZIP from GitHub.

```bash
git clone https://github.com/<YOUR_USERNAME>/bulk-smtp-mail.git
cd bulk-smtp-mail
```

### 2. Prepare your recipient list

For the **Python** script, create a `recipients.csv` file with one email address per line. For example:

```
user1@example.com
user2@example.com
user3@example.com
```

For the **Node.js** script, create a `recipients.txt` file with the same format (one email address per line).

### 3. Configure environment variables

Both scripts read SMTP credentials and other settings from environment
variables. The exact variables used differ slightly between the Python
and Node.js versions:

| Variable         | Description                                    | Python | Node.js |
|------------------|------------------------------------------------|:------:|:-------:|
| `SMTP_SERVER`    | SMTP server host (e.g. `smtp.gmail.com`)       | ✔️     |        |
| `SMTP_HOST`      | SMTP server host (same as above)               |        | ✔️      |
| `SMTP_PORT`      | Port for SMTP server (e.g. `465`)              | ✔️     | ✔️      |
| `SMTP_USERNAME`  | SMTP account username/login                    | ✔️     |        |
| `SMTP_USER`      | SMTP account username/login                    |        | ✔️      |
| `SMTP_PASSWORD`  | SMTP account password or app password          | ✔️     |        |
| `SMTP_PASS`      | SMTP account password (same as above)          |        | ✔️      |
| `SMTP_SENDER`    | Email address to appear in the `From` header   | ✔️     |        |
| `SMTP_FROM`      | Email address to appear in the `From` header   |        | ✔️      |
| `EMAIL_SUBJECT`  | Default subject line (optional)                | ✔️     | ✔️      |
| `EMAIL_BODY`     | Default plain text body (optional)             | ✔️     |        |
| `EMAIL_TEXT`     | Default plain text body (optional)             |        | ✔️      |
| `EMAIL_HTML`     | Default HTML body (optional)                   |        | ✔️      |
| `EMAIL_DELAY`    | Delay between sends (seconds for Python, milliseconds for Node) | ✔️     | ✔️      |

You can set these variables in your shell session or define them in a `.env` file and use a tool like [dotenv](https://www.npmjs.com/package/dotenv) for Node.js.

### 4. Running the Python script
Ensure you have Python 3 installed. The script uses only the standard library, so no extra packages are required. From the repository root:

```bash
# Set environment variables (example for Gmail)
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="465"
export SMTP_USERNAME="your@gmail.com"
export SMTP_PASSWORD="your_app_password"
export SMTP_SENDER="your@gmail.com"

python smtp_bulk_mailer.py \
    --subject "Hello from Python" \
    --body "This is a test bulk email sent from Python." \
    --recipients recipients.csv \
    --delay 2
```

The `--delay` option specifies the pause (in seconds) between each email. Adjust it to stay within your provider’s limits.

### 5. Running the Node.js script

Install Node.js (version 14+ recommended) and install the nodemailer dependency:

```bash
npm install nodemailer
```

Set the environment variables and run the script:

```bash
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="465"
export SMTP_USER="your@gmail.com"
export SMTP_PASS="your_app_password"
export SMTP_FROM="your@gmail.com"
export EMAIL_SUBJECT="Hello from Node.js"
export EMAIL_TEXT="This is a test bulk email sent from Node.js."
export EMAIL_DELAY="2000" # 2 seconds

node smtpMailer.js recipients.txt
```

### 6. Tips for avoiding spam flags

* **Obtain consent** – Only send emails to recipients who have explicitly opted in.
* **Personalize your messages** – Varying the subject and body slightly can improve deliverability.
* **Throttle your sends** – Use a delay between messages (as shown) instead of blasting all emails at once.
* **Use proper authentication** – Configure SPF, DKIM and DMARC records on your domain to establish trust with receiving servers.
* **Monitor bounce and complaint rates** – Remove invalid addresses and handle unsubscribes promptly.

## Contributing

If you find a bug or want to enhance these scripts, feel free to open an issue or submit a pull request. Contributions are welcome!

## License

This repository does not specify a license and is provided "as is". If you intend to reuse the code in your own projects, please credit the author appropriately or choose a suitable license.
