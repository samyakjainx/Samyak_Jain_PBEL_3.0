<div align="center">

# 🧠 Smart Resume Screening & Candidate Ranking Tool

### An AI-powered recruiter assistant that ranks resumes against a job description in seconds.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

</div>

---

## 📌 Overview

**Smart Resume Screening & Candidate Ranking Tool** helps recruiters compare multiple
candidate resumes against a single Job Description (JD) — automatically, accurately,
and in seconds.

Unlike traditional keyword-only ATS filters, this tool blends:

- 🧬 **Semantic similarity** (Sentence-Transformer embeddings) — understands *meaning*,
  not just exact keyword overlap.
- 🎯 **Explicit skill-gap analysis** — surfaces exactly which required skills each
  candidate has, and which they're missing.

The result: a ranked, explainable shortlist that recruiters can trust and act on
immediately, inside a clean, interactive dashboard.

---

## ✨ Features

| Category | Capabilities |
|---|---|
| 📥 **Input** | Upload one JD + multiple resumes (PDF/DOCX) |
| 🧹 **Processing** | Automatic text extraction, cleaning, tokenization, lemmatization |
| 🧠 **AI Matching** | Semantic similarity via Sentence-Transformers, with TF-IDF fallback |
| 🎯 **Skill Analysis** | Skill extraction, matched/missing/extra skill comparison |
| 🏆 **Ranking** | Weighted final score, sorted candidate leaderboard |
| 📊 **Dashboard** | Metric cards, bar charts, pie charts, histograms, word clouds |
| 🔍 **Explorer** | Searchable, sortable candidate cards with expandable detail views |
| 📤 **Export** | One-click CSV download of the full ranking report |
| 🎨 **UI/UX** | Wide layout, custom CSS, badges, progress bars, tabs, responsive design |

---

## 🏗️ Architecture

```
                ┌────────────────────┐
                │      app.py        │   ← Streamlit UI / orchestration
                └─────────┬──────────┘
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
 ┌─────────────┐   ┌──────────────┐   ┌──────────────┐
 │ parser.py   │   │preprocessing │   │  skills.py   │
 │ PDF/DOCX    │──▶│  .py         │──▶│  extraction  │
 │ extraction  │   │  cleaning    │   │  & compare   │
 └─────────────┘   └──────────────┘   └──────┬───────┘
                                              │
        ┌─────────────────────────────────────┘
        ▼
 ┌──────────────┐    ┌──────────────┐    ┌────────────────┐
 │similarity.py │───▶│  ranking.py  │───▶│visualization.py│
 │ semantic /   │    │ score fusion │    │ charts & clouds│
 │ TF-IDF       │    │ & sorting    │    │                │
 └──────────────┘    └──────────────┘    └────────────────┘
```

**Final Match Score** = `0.6 × Semantic Similarity` + `0.4 × Skill Coverage`

---

## 🛠️ Technology Stack

- **Frontend/App:** Streamlit
- **ML/NLP:** Sentence-Transformers, scikit-learn, spaCy, NLTK
- **Document Parsing:** PyMuPDF, pdfplumber, python-docx
- **Data:** Pandas, NumPy
- **Visualization:** Plotly, Matplotlib, WordCloud

---

## 📂 Folder Structure

```
Smart_Resume_Screening/
│
├── app.py                     # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md
├── LICENSE
├── .gitignore
│
├── assets/                     # Logos/banners for the UI
├── data/
│   ├── sample_jd.txt            # Sample Job Description
│   └── sample_resumes/          # Sample candidate resumes (.docx)
│
├── src/
│   ├── parser.py                 # PDF/DOCX text extraction
│   ├── preprocessing.py          # Text cleaning & tokenization
│   ├── skills.py                 # Skill dictionary & extraction
│   ├── similarity.py             # Semantic + TF-IDF similarity scoring
│   ├── ranking.py                # Score fusion & candidate ranking
│   ├── visualization.py          # Plotly charts & word clouds
│   └── utils.py                  # Shared helper functions
│
└── screenshots/                 # App screenshots for documentation
```

---

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/Smart_Resume_Screening.git
cd Smart_Resume_Screening

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. One-time NLP setup
python -m spacy download en_core_web_sm
python -m nltk.downloader stopwords punkt punkt_tab wordnet
```

---

## ▶️ Usage

```bash
streamlit run app.py
```

Then, in the app:

1. Go to **📤 Upload & Screen**
2. Upload a Job Description (PDF/DOCX) — or try `data/sample_jd.txt`
3. Upload one or more resumes (PDF/DOCX) — sample resumes are provided in
   `data/sample_resumes/`
4. Click **🚀 Run Screening**
5. Explore results in **📊 Dashboard** and **🔍 Candidate Explorer**
6. Download the ranking report as CSV

---

## 📸 Screenshots

> Add your own screenshots to the `screenshots/` folder and reference them below.

| Home | Upload | Dashboard |
|---|---|---|
| `screenshots/home.png` | `screenshots/upload.png` | `screenshots/dashboard.png` |

---

## 🔮 Future Improvements

- [ ] Named-entity recognition for automatic candidate name/contact extraction
- [ ] Support for batch JD comparison (multiple job roles at once)
- [ ] Resume-to-JD explainability report (LLM-generated recruiter summary)
- [ ] User authentication and persistent candidate database
- [ ] Multi-language resume support
- [ ] REST API layer for integration with external ATS platforms

---

## ⚖️ License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**[Your Name]**
AI Intern, IBM PBEL
📧 your.email@example.com · 🔗 [LinkedIn](#) · 🔗 [GitHub](#)

---

<div align="center">

⭐ If you found this project useful, consider giving it a star on GitHub!

</div>
