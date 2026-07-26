"""
skills.py
----------
Extracts recognizable technical and soft skills from cleaned text.

Approach:
    - Maintains a curated master skill dictionary covering common
      tech, data, and business-role skills.
    - Matches skills against text using whole-word / phrase matching
      (so "java" doesn't falsely match inside "javascript").
    - Supports multi-word skills (e.g. "machine learning", "power bi").
    - Can be extended by simply adding entries to MASTER_SKILLS.

This keyword-based approach is intentionally transparent and
explainable to recruiters (vs. a black-box NER model), while still
being easy to extend with spaCy PhraseMatcher if more coverage is
needed later.
"""

import re

# ----------------------------------------------------------------
# Master skill dictionary, grouped by category (grouping is used
# only for display purposes; matching is done over the flat list).
# ----------------------------------------------------------------
MASTER_SKILLS = {
    "Programming Languages": [
        "python", "java", "c++", "c#", "javascript", "typescript", "go", "golang",
        "rust", "kotlin", "swift", "php", "ruby", "r", "scala", "matlab", "sql",
        "c", "perl", "dart",
    ],
    "Web Development": [
        "html", "css", "react", "angular", "vue", "node.js", "nodejs", "express",
        "django", "flask", "fastapi", "next.js", "bootstrap", "tailwind",
        "rest api", "graphql", "webpack",
    ],
    "Data Science & AI/ML": [
        "machine learning", "deep learning", "artificial intelligence",
        "natural language processing", "nlp", "computer vision",
        "data science", "data analysis", "data visualization",
        "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
        "pandas", "numpy", "opencv", "hugging face", "transformers",
        "generative ai", "llm", "large language models", "statistics",
        "predictive modeling", "feature engineering",
    ],
    "Databases": [
        "mysql", "postgresql", "mongodb", "sqlite", "oracle", "redis",
        "cassandra", "firebase", "dynamodb", "elasticsearch",
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "jenkins", "ci/cd", "terraform", "ansible", "linux", "git", "github",
        "gitlab", "bitbucket", "devops", "microservices",
    ],
    "Data Tools & BI": [
        "excel", "power bi", "tableau", "looker", "spark", "hadoop",
        "airflow", "etl", "big data", "data warehousing",
    ],
    "Soft Skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "critical thinking", "time management", "adaptability",
        "collaboration", "project management", "presentation",
        "negotiation", "stakeholder management",
    ],
    "Project & Process": [
        "agile", "scrum", "kanban", "jira", "confluence", "waterfall",
    ],
}

# Flattened list of all skills for fast lookup, longest phrases first
# so multi-word skills are matched before their sub-strings.
ALL_SKILLS = sorted(
    {skill for group in MASTER_SKILLS.values() for skill in group},
    key=len,
    reverse=True,
)


def _build_skill_pattern(skill: str) -> str:
    """
    Builds a regex pattern for a skill that matches it as a whole
    word/phrase, handling special characters like '++' or '#'.
    """
    escaped = re.escape(skill)
    return rf"(?<!\w){escaped}(?!\w)"


# Pre-compile patterns once for performance
_SKILL_PATTERNS = {skill: re.compile(_build_skill_pattern(skill)) for skill in ALL_SKILLS}


def extract_skills(clean_text: str) -> set:
    """
    Extracts the set of known skills found in a cleaned text string.

    Args:
        clean_text: lowercased, cleaned text (output of preprocessing.clean_text).

    Returns:
        A set of matched skill names (lowercase, as defined in MASTER_SKILLS).
    """
    if not clean_text:
        return set()

    found = set()
    for skill, pattern in _SKILL_PATTERNS.items():
        if pattern.search(clean_text):
            found.add(skill)

    return found


def categorize_skills(skill_set: set) -> dict:
    """
    Groups a flat set of skills back into their categories for
    nicer display in the UI.

    Args:
        skill_set: set of skill strings.

    Returns:
        dict mapping category name -> sorted list of matched skills
        (only categories with at least one match are included).
    """
    categorized = {}
    for category, skills in MASTER_SKILLS.items():
        matched = sorted(skill_set.intersection(skills))
        if matched:
            categorized[category] = matched
    return categorized


def compare_skills(jd_skills: set, resume_skills: set) -> dict:
    """
    Compares candidate skills against JD-required skills.

    Args:
        jd_skills: set of skills required by the job description.
        resume_skills: set of skills found in the candidate's resume.

    Returns:
        dict with:
            - "matched": skills present in both JD and resume
            - "missing": skills required by JD but absent from resume
            - "extra": skills in resume but not required by JD
            - "match_ratio": fraction of JD skills covered (0.0 - 1.0)
    """
    matched = jd_skills.intersection(resume_skills)
    missing = jd_skills.difference(resume_skills)
    extra = resume_skills.difference(jd_skills)

    match_ratio = (len(matched) / len(jd_skills)) if jd_skills else 0.0

    return {
        "matched": sorted(matched),
        "missing": sorted(missing),
        "extra": sorted(extra),
        "match_ratio": round(match_ratio, 4),
    }
