# models/summarize.py
from transformers import pipeline

# Load summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_email(text):
    summary = summarizer(text, max_length=60, min_length=15, do_sample=False)
    return summary[0]['summary_text']
