from transformers import pipeline

# Try loading summarizer once
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    summarizer = None
    print(f"⚠️ Summarizer model could not be loaded: {e}")

def summarize_email(email_text: str) -> str:
    """
    Summarize an email with dynamic max_length to avoid length mismatch errors.
    Falls back gracefully if summarization fails.
    """
    if not email_text or not email_text.strip():
        return "(No content to summarize)"

    if summarizer is None:
        return "(Summarizer unavailable)"

    try:
        input_length = len(email_text.split())

        # For very short emails, just return them as-is
        if input_length < 15:
            return email_text.strip()

        # Dynamically scale lengths
        max_len = min(200, max(20, int(input_length * 0.6)))  # cap max_len to avoid long outputs
        min_len = min(100, max(10, int(input_length * 0.3)))  # ensure some summary length

        summary = summarizer(
            email_text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )

        return summary[0].get("summary_text", "(No summary generated)")

    except Exception as e:
        return f"(Summarization failed: {e})"

