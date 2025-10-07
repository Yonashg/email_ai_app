# services/ollama_reply.py
import ollama

def draft_reply(email_text: str) -> str:
    """
    Generate a polite and concise draft reply using Ollama.
    Uses safer handling to avoid crashes if Ollama returns empty or malformed responses.
    """
    try:
        prompt = f"Draft a polite and concise reply to the following email:\n\n{email_text}\n\nReply:"

        response = ollama.chat(
            model="mistral",   # make sure 'mistral' is pulled: run `ollama pull mistral`
            messages=[
                {"role": "system", "content": "You are an assistant that writes professional and helpful email replies."},
                {"role": "user", "content": prompt},
            ],
        )

        # Safely extract content
        reply = response.get("message", {}).get("content", "").strip()
        return reply if reply else "(No reply generated.)"

    except ollama.ResponseError as e:
        return f"❌ Ollama response error: {e}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"
