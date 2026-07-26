"""
preprocessing.py
-----------------
Cleans and normalizes raw text (from resumes or job descriptions)
before it is used for skill extraction or similarity scoring.

Pipeline:
    1. Lowercase the text
    2. Remove URLs, emails, phone numbers
    3. Remove special characters / punctuation (keep alphanumerics)
    4. Tokenize
    5. Remove stopwords
    6. Lemmatize (optional, kept lightweight)
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


def _ensure_nltk_data():
    """
    Ensures required NLTK corpora are available. Downloads them
    silently if missing, so the app doesn't crash on a fresh machine.
    """
    required = {
        "corpora/stopwords": "stopwords",
        "tokenizers/punkt": "punkt",
        "corpora/wordnet": "wordnet",
    }
    for path, package in required.items():
        try:
            nltk.data.find(path)
        except LookupError:
            try:
                nltk.download(package, quiet=True)
            except Exception:
                pass


_ensure_nltk_data()

try:
    STOPWORDS = set(stopwords.words("english"))
except Exception:
    STOPWORDS = set()

LEMMATIZER = WordNetLemmatizer()

# Common resume "noise" words that add little signal to matching
CUSTOM_STOPWORDS = {
    "resume", "curriculum", "vitae", "cv", "name", "email", "phone",
    "address", "contact", "reference", "references", "available",
    "request", "date", "birth", "gender", "nationality",
}


def clean_text(raw_text: str) -> str:
    """
    Basic cleaning: lowercase, strip URLs/emails/phone numbers,
    remove non-alphanumeric characters, collapse whitespace.

    Args:
        raw_text: unprocessed text.

    Returns:
        Cleaned text as a single string.
    """
    if not raw_text:
        return ""

    text = raw_text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\.\S+", " ", text)

    # Remove emails
    text = re.sub(r"\S+@\S+", " ", text)

    # Remove phone numbers (sequences of 7+ digits, with optional separators)
    text = re.sub(r"(\+?\d[\d\-\s]{7,}\d)", " ", text)

    # Keep only letters, numbers, and basic punctuation useful for skills (e.g. "c++", "c#")
    text = re.sub(r"[^a-z0-9\+\#\.\s]", " ", text)

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def tokenize_and_filter(cleaned_text: str) -> list:
    """
    Tokenizes cleaned text and removes stopwords / very short tokens.

    Args:
        cleaned_text: output of clean_text().

    Returns:
        List of filtered, lemmatized tokens.
    """
    if not cleaned_text:
        return []

    try:
        tokens = word_tokenize(cleaned_text)
    except Exception:
        tokens = cleaned_text.split()

    filtered = []
    for token in tokens:
        if len(token) <= 1:
            continue
        if token in STOPWORDS or token in CUSTOM_STOPWORDS:
            continue
        try:
            lemma = LEMMATIZER.lemmatize(token)
        except Exception:
            lemma = token
        filtered.append(lemma)

    return filtered


def preprocess_document(raw_text: str) -> dict:
    """
    Full preprocessing pipeline for a single document.

    Args:
        raw_text: unprocessed extracted text.

    Returns:
        dict with keys:
            - "clean_text": cleaned, human-readable string (for TF-IDF / embeddings)
            - "tokens": list of filtered tokens (for skill matching / word clouds)
    """
    cleaned = clean_text(raw_text)
    tokens = tokenize_and_filter(cleaned)

    return {
        "clean_text": cleaned,
        "tokens": tokens,
        "token_string": " ".join(tokens),
    }
