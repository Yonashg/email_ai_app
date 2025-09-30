# services/ollama_reply.py
import subprocess
import json

def draft_reply(email_text):
    prompt = f"Draft a polite and concise reply to the following email:\n\n{email_text}\n\nReply:"
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode("utf-8"),
        capture_output=True,
    )
    return result.stdout.decode("utf-8").strip()
