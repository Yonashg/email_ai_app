from transformers import pipeline

# Load zero-shot classification model once
try:
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
except Exception as e:
    classifier = None
    print(f"⚠️ Failed to load model: {e}")

# Candidate categories
CATEGORIES = ["Work", "Personal", "Promotions", "Spam", "Important", "Other"]

def categorize_email(email_text: str) -> str:
    """
    Categorize an email using zero-shot classification.
    Falls back to 'Other' if classification fails or email is empty.
    """
    if not email_text or not email_text.strip():
        return "Other"

    if classifier is None:
        return "(Categorization model unavailable)"

    try:
        result = classifier(
            email_text,
            candidate_labels=CATEGORIES,
            multi_label=False
        )

        if result and "labels" in result and len(result["labels"]) > 0:
            return result["labels"][0]
        else:
            return "Other"

    except Exception as e:
        return f"(Categorization failed: {e})"
