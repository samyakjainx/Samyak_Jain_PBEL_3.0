"""
ranking.py
-----------
Fuses similarity scores and skill-match scores into a single final
match percentage per candidate, then ranks all candidates.

Final Score Formula:
    final_score = (SIMILARITY_WEIGHT * semantic_similarity)
                + (SKILL_WEIGHT * skill_match_ratio)

Weights are tunable constants below. The default (60% semantic
similarity, 40% skill coverage) balances "overall contextual fit"
with "explicit required-skill coverage", which recruiters tend to
find intuitive.
"""

import pandas as pd

# Tunable weighting between contextual similarity and explicit skill coverage
SIMILARITY_WEIGHT = 0.6
SKILL_WEIGHT = 0.4


def compute_final_score(similarity_score: float, skill_match_ratio: float) -> float:
    """
    Combines similarity and skill-match ratio into one final score.

    Args:
        similarity_score: 0-1 float, semantic/TF-IDF similarity to JD.
        skill_match_ratio: 0-1 float, fraction of required skills present.

    Returns:
        Final match score as a percentage (0-100), rounded to 2 decimals.
    """
    final = (SIMILARITY_WEIGHT * similarity_score) + (SKILL_WEIGHT * skill_match_ratio)
    return round(final * 100, 2)


def build_ranking_table(candidates: list) -> pd.DataFrame:
    """
    Builds a sorted ranking DataFrame from a list of candidate result
    dictionaries.

    Args:
        candidates: list of dicts, each containing:
            - "name": candidate/file display name
            - "similarity_score": 0-1 float
            - "skill_match_ratio": 0-1 float
            - "matched_skills": list of matched skill strings
            - "missing_skills": list of missing skill strings
            - "extra_skills": list of extra skill strings

    Returns:
        pandas DataFrame sorted by final match score, descending,
        with an added "Rank" column starting at 1.
    """
    rows = []
    for c in candidates:
        final_score = compute_final_score(c["similarity_score"], c["skill_match_ratio"])
        rows.append({
            "Candidate": c["name"],
            "Match Score (%)": final_score,
            "Semantic Similarity (%)": round(c["similarity_score"] * 100, 2),
            "Skill Coverage (%)": round(c["skill_match_ratio"] * 100, 2),
            "Matched Skills": ", ".join(c["matched_skills"]) if c["matched_skills"] else "-",
            "Missing Skills": ", ".join(c["missing_skills"]) if c["missing_skills"] else "-",
            "Extra Skills": ", ".join(c["extra_skills"]) if c["extra_skills"] else "-",
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df = df.sort_values(by="Match Score (%)", ascending=False).reset_index(drop=True)
    df.insert(0, "Rank", df.index + 1)
    return df


def get_score_category(match_score: float) -> str:
    """
    Maps a numeric match score to a human-friendly category label,
    used for color-coded badges in the UI.

    Args:
        match_score: 0-100 float.

    Returns:
        One of "Excellent Match", "Good Match", "Average Match", "Weak Match".
    """
    if match_score >= 80:
        return "Excellent Match"
    elif match_score >= 60:
        return "Good Match"
    elif match_score >= 40:
        return "Average Match"
    else:
        return "Weak Match"
