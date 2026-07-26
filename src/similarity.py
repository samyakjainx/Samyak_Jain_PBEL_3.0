"""
similarity.py
--------------
Computes similarity between a Job Description and candidate resumes.

Two strategies are implemented:
    1. Semantic similarity using Sentence-Transformers embeddings
       (preferred — captures meaning, not just keyword overlap).
    2. TF-IDF + cosine similarity (fallback — used automatically if
       the Sentence-Transformers model cannot be loaded, e.g. no
       internet access on first run to download the model).

The public function `compute_similarity_scores` always returns a
result, transparently falling back if the primary model is unavailable.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

_MODEL = None
_MODEL_LOAD_ATTEMPTED = False
_MODEL_NAME = "all-MiniLM-L6-v2"


def _get_sentence_transformer():
    """
    Lazily loads the Sentence-Transformers model exactly once per
    session. Returns None if the library/model isn't available,
    so callers can gracefully fall back to TF-IDF.
    """
    global _MODEL, _MODEL_LOAD_ATTEMPTED

    if _MODEL is not None:
        return _MODEL

    if _MODEL_LOAD_ATTEMPTED:
        return None

    _MODEL_LOAD_ATTEMPTED = True
    try:
        from sentence_transformers import SentenceTransformer
        _MODEL = SentenceTransformer(_MODEL_NAME)
        return _MODEL
    except Exception:
        return None


def semantic_similarity(jd_text: str, resume_texts: list) -> list:
    """
    Computes cosine similarity between JD and each resume using
    dense sentence embeddings.

    Args:
        jd_text: cleaned job description text.
        resume_texts: list of cleaned resume text strings.

    Returns:
        List of similarity scores (0-1 float) in the same order as
        resume_texts, or None if the model is unavailable.
    """
    model = _get_sentence_transformer()
    if model is None:
        return None

    try:
        jd_embedding = model.encode([jd_text], convert_to_numpy=True)
        resume_embeddings = model.encode(resume_texts, convert_to_numpy=True)
        scores = cosine_similarity(jd_embedding, resume_embeddings)[0]
        # Clip to [0, 1] since cosine similarity of embeddings can be slightly negative
        scores = np.clip(scores, 0, 1)
        return scores.tolist()
    except Exception:
        return None


def tfidf_similarity(jd_text: str, resume_texts: list) -> list:
    """
    Computes cosine similarity between JD and each resume using
    TF-IDF vectorization. Used as a reliable fallback when the
    Sentence-Transformers model can't be loaded.

    Args:
        jd_text: cleaned job description text.
        resume_texts: list of cleaned resume text strings.

    Returns:
        List of similarity scores (0-1 float) in the same order as
        resume_texts.
    """
    documents = [jd_text] + resume_texts

    # Guard against completely empty corpus (would break the vectorizer)
    if not any(doc.strip() for doc in documents):
        return [0.0] * len(resume_texts)

    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
    except ValueError:
        # Happens if vocabulary ends up empty after stopword removal
        return [0.0] * len(resume_texts)

    jd_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]

    scores = cosine_similarity(jd_vector, resume_vectors)[0]
    return scores.tolist()


def compute_similarity_scores(jd_text: str, resume_texts: list) -> dict:
    """
    Main entry point: computes similarity scores using the best
    available method.

    Args:
        jd_text: cleaned job description text.
        resume_texts: list of cleaned resume text strings.

    Returns:
        dict with:
            - "scores": list of similarity scores (0-1), aligned to resume_texts
            - "method": "semantic" or "tfidf" (whichever was actually used)
    """
    scores = semantic_similarity(jd_text, resume_texts)
    method = "semantic"

    if scores is None:
        scores = tfidf_similarity(jd_text, resume_texts)
        method = "tfidf"

    return {"scores": scores, "method": method}
