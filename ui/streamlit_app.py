import sys
import os
# Add project root to sys.path so imports always work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# ui/streamlit_app.py
import streamlit as st
from models.categorize import categorize_email
from models.summarize import summarize_email
from services.ollama_reply import draft_reply
from db.database import init_db, insert_email, fetch_emails



# Initialize database
init_db()

st.set_page_config(page_title="AI Email Assistant", layout="wide")
st.title("📧 AI Email Assistant")

tab1, tab2 = st.tabs(["Process Email", "History"])

with tab1:
    email_text = st.text_area("Paste your email content here:", height=250)

    if st.button("Process Email"):
        if email_text.strip():
            with st.spinner("Categorizing..."):
                category = categorize_email(email_text)
            with st.spinner("Summarizing..."):
                summary = summarize_email(email_text)
            with st.spinner("Generating draft reply..."):
                reply = draft_reply(email_text)

            # Save to database
            insert_email(email_text, category, summary, reply)

            st.subheader("📌 Category")
            st.write(category)

            st.subheader("📝 Summary")
            st.write(summary)

            st.subheader("✍️ Suggested Reply")
            st.text_area("Reply", value=reply, height=200)
        else:
            st.warning("Please paste an email first!")

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
