# 📄 Project Documentation

## Smart Resume Screening & Candidate Ranking Tool

---

## 1. Project Abstract

Recruitment teams routinely receive hundreds of resumes for a single job opening, making
manual screening slow, inconsistent, and prone to human bias. This project presents an
AI-powered Resume Screening & Candidate Ranking Tool that automates the initial
shortlisting process. The system extracts text from uploaded resumes and a job
description, computes contextual semantic similarity using Sentence-Transformer
embeddings, cross-references extracted skills, and produces a ranked, explainable
shortlist of candidates through an interactive Streamlit dashboard.

---

## 2. Problem Statement

Manual resume screening is:

- **Time-consuming** — recruiters spend hours reading resumes that may not be relevant.
- **Inconsistent** — different reviewers apply different (often implicit) criteria.
- **Keyword-fragile** — many Applicant Tracking Systems (ATS) reject qualified
  candidates simply because their resume phrases a skill differently from the job
  posting (e.g. "NLP" vs. "Natural Language Processing").
- **Lacking transparency** — candidates and recruiters alike rarely know *why* a
  resume was rejected or ranked lower.

There is a need for a tool that is fast, consistent, semantically aware, and transparent
about its reasoning.

---

## 3. Objectives

1. Automatically extract and clean text from PDF/DOCX resumes and job descriptions.
2. Identify relevant technical and soft skills present in both documents.
3. Compute a meaningful similarity score between each resume and the job description
   using contextual (semantic) understanding rather than pure keyword matching.
4. Rank candidates using a transparent, explainable scoring formula.
5. Present results through an intuitive, recruiter-friendly dashboard with visual
   analytics and exportable reports.

---

## 4. Methodology

The system follows a modular pipeline architecture:

1. **Text Extraction** — `PyMuPDF` (primary) and `pdfplumber` (fallback) extract text
   from PDF resumes; `python-docx` handles DOCX files, including table content.
2. **Preprocessing** — Text is lowercased, stripped of URLs/emails/phone numbers,
   tokenized with `NLTK`, filtered against stopword lists, and lemmatized.
3. **Skill Extraction** — A curated, categorized skill dictionary is matched against
   cleaned text using whole-word/phrase regex matching, avoiding false positives
   (e.g. "java" inside "javascript").
4. **Similarity Scoring** — `Sentence-Transformers` (`all-MiniLM-L6-v2`) encodes the
   JD and each resume into dense vector embeddings; cosine similarity measures
   contextual closeness. If the model is unavailable, the system automatically falls
   back to `TF-IDF` + cosine similarity via `scikit-learn`.
5. **Score Fusion & Ranking** — A weighted formula combines semantic similarity (60%)
   and explicit skill coverage (40%) into one final match percentage, and candidates
   are sorted in descending order.
6. **Visualization** — `Plotly` renders interactive bar charts, pie charts, and
   histograms; `WordCloud` visualizes dominant resume themes.

---

## 5. Workflow Diagram (Textual)

```
Upload JD + Resumes
        │
        ▼
Text Extraction (PDF/DOCX)
        │
        ▼
Cleaning & Tokenization
        │
        ▼
Skill Extraction (JD & Resumes)
        │
        ▼
Similarity Scoring (Semantic / TF-IDF)
        │
        ▼
Score Fusion → Final Match %
        │
        ▼
Ranking Table + Dashboard + CSV Export
```

---

## 6. Algorithms Used

| Component | Algorithm / Technique |
|---|---|
| Text extraction | Rule-based parsing (PyMuPDF / pdfplumber / python-docx) |
| Text cleaning | Regex-based normalization, NLTK tokenization & lemmatization |
| Skill matching | Regex whole-word/phrase dictionary matching |
| Semantic similarity | Sentence-BERT embeddings (`all-MiniLM-L6-v2`) + cosine similarity |
| Fallback similarity | TF-IDF vectorization + cosine similarity |
| Ranking | Weighted linear score fusion |

---

## 7. Advantages

- Combines contextual understanding with explicit, explainable skill matching.
- Gracefully degrades to TF-IDF if the semantic model cannot be loaded (e.g. offline
  environments), so the tool never fails to produce a result.
- Modular codebase — each pipeline stage is an independently testable module.
- Fully interactive dashboard requiring no coding knowledge from the end user.
- Exportable CSV reports for integration into existing recruiting workflows.

---

## 8. Limitations

- Skill extraction relies on a curated dictionary; entirely novel or highly niche
  skills not in the dictionary will not be detected.
- Semantic similarity quality depends on the pretrained embedding model's domain
  coverage; highly specialized technical jargon may be less well represented.
- The tool assists screening — it does not account for factors like cultural fit,
  interview performance, or references, and should not be the sole basis for
  hiring decisions.
- Currently supports English-language resumes only.

---

## 9. Future Scope

- Integrate large language models (LLMs) to generate natural-language explanations
  of why a candidate ranked where they did.
- Add named-entity recognition to auto-extract candidate contact details and
  work-experience timelines.
- Support multi-JD batch comparison for recruiters hiring across several roles.
- Build a persistent database layer for tracking candidates across hiring cycles.
- Extend skill dictionary coverage using dynamic, continuously updated skill taxonomies.

---

## 10. Conclusion

The Smart Resume Screening & Candidate Ranking Tool demonstrates how modern NLP
techniques — combining semantic embeddings with transparent skill-gap analysis — can
meaningfully reduce the time and inconsistency involved in early-stage resume
screening, while keeping the final decision-making process interpretable and in the
hands of human recruiters.
