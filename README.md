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

# 🚀 Live Demo

🔗 **Web Application**

> **Deployed Streamlit link :**

```
https://samyak-jain-ibm-pbel-03.streamlit.app/
```

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
├── DOCUMENTATION.md
│
├── assets/                     # Logos/banners for the UI
├── data/
│   ├── sample_jd.txt            # Sample Job Description
│   └── sample_resumes/          # Sample candidate resumes (.docx)
│
├── src/
│   ├── _init_.py
|   ├── parser.py                 # PDF/DOCX text extraction
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
git clone https://github.com/samyakjainx/Samyak_Jain_PBEL_3.0.git
cd Samyak_Jain_PBEL_3.0

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


| Home | Upload | Dashboard 1|
|---|---|---|
| <img width="2880" height="1720" alt="home" src="https://github.com/user-attachments/assets/56be7bab-e7ab-4ae5-bd42-dd7aa593dcc3" /> | <img width="2860" height="1632" alt="upload" src="https://github.com/user-attachments/assets/5297881e-a058-47c4-9e2e-fed99505284b" /> | <img width="2866" height="1632" alt="dashboard-1" src="https://github.com/user-attachments/assets/31e71f43-ccfd-4a41-bb7d-32b56ae6b127" /> |

| Dashboard 2| Candidate Explorer | About |
|---|---|---|
| <img width="2860" height="1632" alt="dashboard-2" src="https://github.com/user-attachments/assets/5ca5e395-377d-4b5a-ac18-df58c3e79e26" /> | <img width="2864" height="1628" alt="candidate" src="https://github.com/user-attachments/assets/37ea8b10-1535-4ebf-ac3c-cf5e58ab96ea" /> | <img width="2866" height="1634" alt="about" src="https://github.com/user-attachments/assets/8f6c77af-9b73-4f9b-bbe7-4168e8accfb0" /> |

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

**Samyak Jain**
AI Intern, IBM PBEL

📧 jain.sam1905@gmail.com · 
🔗 https://www.linkedin.com/in/samyakjain-ai/ · 
🔗 https://github.com/samyakjainx

---

<div align="center">

⭐ If you found this project useful, consider giving it a star on GitHub!

</div>
