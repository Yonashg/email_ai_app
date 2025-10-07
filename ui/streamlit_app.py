import sys
import os
import streamlit as st

# Add project root to sys.path so imports always work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.categorize import categorize_email
from models.summarize import summarize_email
from services.ollama_reply import draft_reply
from db.database import init_db, insert_email, fetch_emails
from services.fetch_gmail import fetch_emails as fetch_from_gmail


# -----------------------------
# Initialize
# -----------------------------
init_db()
st.set_page_config(page_title="AI Email Assistant", layout="wide")
st.title("📧 AI Email Assistant")


# -----------------------------
# Helper to process an email
# -----------------------------
def process_email(email_text: str):
    """Categorize, summarize, and draft reply for a given email."""
    with st.spinner("Categorizing..."):
        category = categorize_email(email_text)

    with st.spinner("Summarizing..."):
        summary = summarize_email(email_text)

    with st.spinner("Generating draft reply..."):
        reply = draft_reply(email_text)

    # Save in DB
    insert_email(email_text, category, summary, reply)

    # Display results
    st.subheader("📌 Category")
    st.write(category)

    st.subheader("📝 Summary")
    st.write(summary)

    st.subheader("✍️ Suggested Reply")
    st.text_area("Reply", value=reply, height=200)


# -----------------------------
# Tabs
# -----------------------------
tab1, tab2 = st.tabs(["Process Email", "History"])

with tab1:
    st.markdown("### ✉️ Process an Email")

    mode = st.radio("Choose input method:", ["Paste manually", "Fetch from Gmail"])

    if mode == "Paste manually":
        email_text = st.text_area("Paste your email content here:", height=250)
        if st.button("Process Email"):
            if email_text.strip():
                process_email(email_text)
            else:
                st.warning("Please paste an email first!")

    elif mode == "Fetch from Gmail":
        num_emails = st.number_input(
            "Number of latest emails to fetch", min_value=1, max_value=20, value=1
        )
        if st.button("Fetch & Process"):
            try:
                emails = fetch_from_gmail(n=num_emails)
                if not emails:
                    st.info("No emails found in your Gmail inbox.")
                else:
                    for i, email_data in enumerate(emails, start=1):
                        subject = email_data.get("subject") or "(No subject)"
                        sender = email_data.get("from") or "(Unknown sender)"
                        body_preview = email_data.get("body") or "(No content found)"  # ✅ fallback

                        st.markdown(f"#### Email {i}: {subject}")
                        st.write("From:", sender)
                        st.write("Body (first 500 chars):", body_preview[:500], "...")
                        process_email(body_preview)
                        st.divider()
            except Exception as e:
                st.error(f"Failed to fetch emails: {e}")

with tab2:
    st.subheader("📜 Processed Emails History")
    rows = fetch_emails()
    if rows:
        for row in rows:
            st.markdown(f"**ID:** {row[0]} | **Category:** {row[2]}")
            st.write(f"📧 Content: {row[1][:200]}...")
            st.write(f"📝 Summary: {row[3]}")
            st.write(f"✍️ Reply: {row[4]}")
            st.divider()
    else:
        st.info("No emails processed yet.")
