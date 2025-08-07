// SMTP Bulk Mailer (Node.js)
//
// This script sends emails in bulk using the nodemailer library. Each
// email is sent individually with a configurable delay between sends to
// minimize the risk of being flagged as spam. Recipient addresses are
// loaded from a newline‑separated text file. SMTP credentials and
// connection details are taken from environment variables.
//
// Usage:
//   1. Create a text file (e.g. `recipients.txt`) with one email address per line.
//   2. Set environment variables:
//        SMTP_HOST  – SMTP server host name (e.g. 'smtp.gmail.com')
//        SMTP_PORT  – SMTP server port (e.g. '465')
//        SMTP_USER  – SMTP username
//        SMTP_PASS  – SMTP password or app password
//        SMTP_FROM  – Address to appear in the 'From' header
//        EMAIL_SUBJECT – (optional) subject line
//        EMAIL_TEXT    – (optional) plain text body
//        EMAIL_HTML    – (optional) HTML body
//        EMAIL_DELAY   – (optional) delay between sends, in milliseconds
//   3. Install dependencies:
//        npm install nodemailer
//   4. Run:
//        node smtpMailer.js recipients.txt
//
// Note: Always obtain consent from your recipients and comply with your
// mail provider's sending limits. Adjust the EMAIL_DELAY variable to
// throttle your sends accordingly.

const nodemailer = require('nodemailer');
const fs = require('fs');

/**
 * Pause execution for a given duration.
 * @param {number} ms Delay in milliseconds
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Send bulk emails using nodemailer.
 * @param {Object} config SMTP configuration and sender details.
 * @param {string[]} recipients List of recipient email addresses.
 * @param {string} subject Email subject line.
 * @param {string} text Plain text body.
 * @param {string} html HTML body.
 * @param {number} delay Delay between sends, in milliseconds.
 */
async function sendBulkEmails(config, recipients, subject, text, html, delay) {
  const transporter = nodemailer.createTransport({
    host: config.host,
    port: config.port,
    secure: config.secure,
    auth: {
      user: config.user,
      pass: config.pass
    }
  });

  for (const recipient of recipients) {
    const mailOptions = {
      from: config.from,
      to: recipient,
      subject,
      text,
      html
    };
    try {
      const info = await transporter.sendMail(mailOptions);
      console.log(`Sent to ${recipient}: ${info.messageId}`);
    } catch (err) {
      console.error(`Failed to send to ${recipient}: ${err}`);
    }
    if (delay > 0) {
      await sleep(delay);
    }
  }
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error('Usage: node smtpMailer.js <recipients-file>');
    process.exit(1);
  }
  const recipientsFile = args[0];
  const fileContents = fs.readFileSync(recipientsFile, 'utf-8');
  const recipients = fileContents.split(/\r?\n/).map(line => line.trim()).filter(Boolean);

  const config = {
    host: process.env.SMTP_HOST || 'smtp.gmail.com',
    port: parseInt(process.env.SMTP_PORT || '465', 10),
    secure: (process.env.SMTP_PORT || '465') === '465',
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
    from: process.env.SMTP_FROM || process.env.SMTP_USER
  };
  if (!config.user || !config.pass) {
    console.error('SMTP_USER and SMTP_PASS environment variables must be set.');
    process.exit(1);
  }

  const subject = process.env.EMAIL_SUBJECT || 'Bulk Email';
  const text = process.env.EMAIL_TEXT || 'Hello, this is a bulk email.';
  const html = process.env.EMAIL_HTML || `<p>${text}</p>`;
  const delay = parseInt(process.env.EMAIL_DELAY || '1000', 10);

  await sendBulkEmails(config, recipients, subject, text, html, delay);
}

main().catch(err => console.error(err));
