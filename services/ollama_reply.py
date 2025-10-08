# services/ollama_reply.py
import ollama

def draft_reply(email_text: str) -> str:
    """
    Generate a polite and concise draft reply using Ollama.
    Uses a lightweight model to avoid memory issues.
    """
    try:
        # Use a lightweight model instead of big 'mistral'
        MODEL_NAME = "gemma:2b" \
        ""   # alternatives: "gemma:2b", "llama2:7b-chat"

        # Truncate long emails to avoid memory overload
        truncated_email = email_text[:1000] if email_text else "(No content)"

        prompt = f"Draft a polite and concise reply to the following email:\n\n{truncated_email}\n\nReply:"

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an assistant that writes professional, polite email replies."},
                {"role": "user", "content": prompt},
            ],
        )

        # Extract generated reply
        if response and "message" in response and "content" in response["message"]:
            return response["message"]["content"].strip()

        return "(No reply generated)"

    except Exception as e:
        return f"❌ Ollama error: {e}"
