# models/categorize.py
from transformers import pipeline

# Load zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def categorize_email(text):
    candidate_labels = ["work", "personal", "spam", "promotions", "urgent"]
    result = classifier(text, candidate_labels)
    return result["labels"][0]  # Top predicted category
