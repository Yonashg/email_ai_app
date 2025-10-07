# services/fetch_gmail.py
import imaplib
import email
import os
from dotenv import load_dotenv

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()

EMAIL_ADDRESS = os.getenv("GMAIL_USER")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

if not EMAIL_ADDRESS or not APP_PASSWORD:
    raise ValueError("❌ Missing Gmail credentials. Please set GMAIL_USER and GMAIL_APP_PASSWORD in your .env file.")


# ---------------------------
# Helper: Extract email body
# ---------------------------
def clean_body(msg):
    """Extract and clean email body safely."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True)
                    if body:
                        return body.decode(errors="ignore")
                except Exception:
                    continue
    else:
        try:
            body = msg.get_payload(decode=True)
            if body:
                return body.decode(errors="ignore")
        except Exception:
            pass
    return ""  # fallback if no body found


# ---------------------------
# Main function: Fetch emails
# ---------------------------
def fetch_emails(n=5):
    """
    Fetch the latest `n` emails from Gmail.
    Returns a list of dicts with subject, from, and body.
    """
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_ADDRESS, APP_PASSWORD)
        mail.select("inbox")

        # Search all emails
        status, data = mail.search(None, "ALL")
        if status != "OK" or not data or not data[0]:
            return []

        email_ids = data[0].split()
        latest_ids = email_ids[-n:]

        emails = []
        for e_id in reversed(latest_ids):
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            if status != "OK":
                continue

            raw_msg = msg_data[0][1]
            msg = email.message_from_bytes(raw_msg)

            subject = msg.get("subject") or "(No Subject)"
            sender = msg.get("from") or "(Unknown Sender)"
            body = clean_body(msg) or "(No content found)"

            emails.append({
                "subject": subject,
                "from": sender,
                "body": body
            })

        return emails

    except imaplib.IMAP4.error as e:
        raise Exception(f"❌ IMAP authentication failed: {e}")
    except Exception as e:
        raise Exception(f"❌ Unexpected error fetching emails: {e}")
