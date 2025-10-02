import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

# Load credentials
load_dotenv()
USERNAME = os.getenv("GMAIL_USER")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def fetch_emails(n: int = 1):
    """Fetch the latest n emails from Gmail inbox via IMAP."""
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(USERNAME, APP_PASSWORD)

    imap.select("inbox")
    status, messages = imap.search(None, "ALL")
    email_ids = messages[0].split()

    latest_emails = []
    for i in email_ids[-n:]:
        res, msg_data = imap.fetch(i, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Decode subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")

                from_ = msg.get("From")

                # Get body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                latest_emails.append({
                    "from": from_,
                    "subject": subject,
                    "body": body
                })

    imap.close()
    imap.logout()
    return latest_emails
