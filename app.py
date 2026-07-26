"""
app.py
-------
Smart Resume Screening & Candidate Ranking Tool
--------------------------------------------------
Main Streamlit application entry point.

This file is intentionally kept focused on UI/orchestration only.
All heavy lifting (parsing, preprocessing, skill extraction,
similarity scoring, ranking, and chart building) lives in the
`src/` package as clean, independently testable modules.

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import time

from src import parser, preprocessing, skills, similarity, ranking, visualization, utils


# ==============================================================
# PAGE CONFIGURATION
# ==============================================================
st.set_page_config(
    page_title="Smart Resume Screening & Candidate Ranking Tool",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==============================================================
# GLOBAL STYLES
# ==============================================================
def load_custom_css():
    st.markdown("""
        <style>
        .main-title {
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(90deg, #4F46E5, #06B6D4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0rem;
        }
        .subtitle {
            font-size: 1.05rem;
            color: #6B7280;
            margin-top: 0rem;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 1.2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        .candidate-card {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 16px;
            padding: 1.3rem 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        }
        .badge {
            display: inline-block;
            padding: 0.25rem 0.7rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            color: white;
        }
        .badge-excellent { background-color: #10B981; }
        .badge-good { background-color: #06B6D4; }
        .badge-average { background-color: #F59E0B; }
        .badge-weak { background-color: #EF4444; }
        footer {visibility: hidden;}
        .app-footer {
            text-align: center;
            color: #9CA3AF;
            font-size: 0.85rem;
            padding-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)


BADGE_CLASS_MAP = {
    "Excellent Match": "badge-excellent",
    "Good Match": "badge-good",
    "Average Match": "badge-average",
    "Weak Match": "badge-weak",
}


# ==============================================================
# SESSION STATE INITIALIZATION
# ==============================================================
def init_session_state():
    defaults = {
        "ranking_df": None,
        "candidate_details": {},
        "jd_text": "",
        "similarity_method": None,
        "processed": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ==============================================================
# CORE PROCESSING PIPELINE
# ==============================================================
def process_resumes(jd_file, resume_files):
    """
    Runs the full screening pipeline: parse -> preprocess -> extract
    skills -> compute similarity -> rank. Populates st.session_state
    with results for the dashboard to render.
    """
    progress_bar = st.progress(0, text="Starting screening pipeline...")

    # --- Step 1: Extract & preprocess Job Description ---
    progress_bar.progress(10, text="Reading job description...")
    jd_raw_text = parser.extract_text(jd_file)
    jd_processed = preprocessing.preprocess_document(jd_raw_text)
    jd_skill_set = skills.extract_skills(jd_processed["clean_text"])

    # --- Step 2: Validate & extract resumes ---
    progress_bar.progress(25, text="Validating uploaded resumes...")
    valid_files, invalid_names = utils.validate_uploaded_files(resume_files)

    if invalid_names:
        st.warning(f"Skipped unsupported files: {', '.join(invalid_names)}")

    if not valid_files:
        progress_bar.empty()
        st.error("No valid PDF/DOCX resumes were found. Please upload valid files.")
        return

    resume_data = []
    total = len(valid_files)
    for i, f in enumerate(valid_files):
        progress_pct = 25 + int(((i + 1) / total) * 35)
        progress_bar.progress(progress_pct, text=f"Extracting text from {f.name}...")

        raw_text = parser.extract_text(f)
        processed = preprocessing.preprocess_document(raw_text)
        candidate_name = utils.clean_candidate_name(f.name)

        resume_data.append({
            "name": candidate_name,
            "raw_text": raw_text,
            "clean_text": processed["clean_text"],
            "token_string": processed["token_string"],
        })

    # --- Step 3: Compute similarity scores (batched for efficiency) ---
    progress_bar.progress(65, text="Computing semantic similarity...")
    resume_texts = [r["clean_text"] for r in resume_data]
    sim_result = similarity.compute_similarity_scores(jd_processed["clean_text"], resume_texts)
    st.session_state["similarity_method"] = sim_result["method"]

    # --- Step 4: Extract skills & compare per candidate ---
    progress_bar.progress(80, text="Analyzing skills...")
    candidates = []
    candidate_details = {}

    for idx, r in enumerate(resume_data):
        resume_skill_set = skills.extract_skills(r["clean_text"])
        comparison = skills.compare_skills(jd_skill_set, resume_skill_set)

        candidates.append({
            "name": r["name"],
            "similarity_score": sim_result["scores"][idx],
            "skill_match_ratio": comparison["match_ratio"],
            "matched_skills": comparison["matched"],
            "missing_skills": comparison["missing"],
            "extra_skills": comparison["extra"],
        })

        candidate_details[r["name"]] = {
            "raw_text": r["raw_text"],
            "token_string": r["token_string"],
            "matched_skills": comparison["matched"],
            "missing_skills": comparison["missing"],
            "extra_skills": comparison["extra"],
        }

    # --- Step 5: Build final ranking table ---
    progress_bar.progress(95, text="Ranking candidates...")
    ranking_df = ranking.build_ranking_table(candidates)

    st.session_state["ranking_df"] = ranking_df
    st.session_state["candidate_details"] = candidate_details
    st.session_state["jd_skill_set"] = jd_skill_set
    st.session_state["jd_text"] = jd_processed["token_string"]
    st.session_state["processed"] = True

    progress_bar.progress(100, text="Done!")
    time.sleep(0.4)
    progress_bar.empty()


# ==============================================================
# SIDEBAR NAVIGATION
# ==============================================================
def render_sidebar():
    with st.sidebar:
        st.markdown("## 🧠 Navigation")
        page = st.radio(
            "Go to",
            ["🏠 Home", "📤 Upload & Screen", "📊 Dashboard", "🔍 Candidate Explorer", "ℹ️ About"],
            label_visibility="collapsed",
        )
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        st.caption(
            f"Similarity Engine: **{st.session_state.get('similarity_method') or 'Not run yet'}**"
        )
        st.caption("Weights: 60% Semantic Similarity · 40% Skill Coverage")
        st.markdown("---")
        st.markdown(
            "<div style='font-size:0.8rem;color:#9CA3AF;'>"
            "Built with Streamlit · Sentence-Transformers · scikit-learn"
            "</div>",
            unsafe_allow_html=True,
        )
        return page


# ==============================================================
# PAGE: HOME
# ==============================================================
def render_home():
    st.markdown('<div class="main-title">Smart Resume Screening & Candidate Ranking Tool</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">An AI-powered recruiter assistant that ranks resumes against a '
        'job description in seconds — combining semantic understanding with explicit skill matching.</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    highlight_cards = [
        ("📄", "Multi-format Parsing", "PDF & DOCX resumes supported out of the box"),
        ("🧬", "Semantic Matching", "Sentence-Transformers understands context, not just keywords"),
        ("🎯", "Skill Gap Analysis", "Instantly see missing and matched skills per candidate"),
        ("📈", "Recruiter Dashboard", "Interactive charts and exportable ranking reports"),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], highlight_cards):
        with col:
            st.markdown(
                f"""<div class="metric-card">
                    <div style="font-size:1.8rem;">{icon}</div>
                    <div style="font-weight:700;margin-top:0.4rem;">{title}</div>
                    <div style="color:#6B7280;font-size:0.85rem;margin-top:0.2rem;">{desc}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("### How it works")
    steps = [
        "**1. Upload** a Job Description and one or more candidate resumes.",
        "**2. The engine extracts and cleans text**, then identifies required and candidate skills.",
        "**3. Similarity is scored** using Sentence-Transformer embeddings (with a TF-IDF fallback).",
        "**4. Candidates are ranked** using a weighted blend of contextual similarity and skill coverage.",
        "**5. Explore results** in an interactive dashboard, and export the ranking as CSV.",
    ]
    for s in steps:
        st.markdown(f"- {s}")

    st.info("👉 Head to **Upload & Screen** in the sidebar to get started.")


# ==============================================================
# PAGE: UPLOAD & SCREEN
# ==============================================================
def render_upload_page():
    st.markdown('<div class="main-title">📤 Upload & Screen</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Upload one job description and multiple candidate resumes to begin screening.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1️⃣ Job Description")
        jd_file = st.file_uploader(
            "Upload Job Description (PDF or DOCX)",
            type=["pdf", "docx"],
            accept_multiple_files=False,
            key="jd_uploader",
        )
        if jd_file:
            st.success(f"Loaded: {jd_file.name}")

    with col2:
        st.subheader("2️⃣ Candidate Resumes")
        resume_files = st.file_uploader(
            "Upload Resumes (PDF or DOCX) — multiple allowed",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            key="resume_uploader",
        )
        if resume_files:
            st.success(f"{len(resume_files)} resume(s) ready")

    st.markdown("---")
    run_col, _ = st.columns([1, 3])
    with run_col:
        run_clicked = st.button("🚀 Run Screening", type="primary", use_container_width=True)

    if run_clicked:
        if not jd_file:
            st.error("Please upload a Job Description before running screening.")
        elif not resume_files:
            st.error("Please upload at least one resume before running screening.")
        else:
            try:
                process_resumes(jd_file, resume_files)
                st.success("Screening complete! Head to the Dashboard to view results.")
                st.balloons()
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")


# ==============================================================
# PAGE: DASHBOARD
# ==============================================================
def render_dashboard():
    st.markdown('<div class="main-title">📊 Recruiter Dashboard</div>', unsafe_allow_html=True)

    if not st.session_state.get("processed"):
        st.warning("No screening results yet. Please go to **Upload & Screen** first.")
        return

    df = st.session_state["ranking_df"]

    if df.empty:
        st.error("No candidates could be processed.")
        return

    # --- Top-level metrics ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Candidates", len(df))
    m2.metric("Top Match Score", f"{df['Match Score (%)'].max()}%")
    m3.metric("Average Match Score", f"{round(df['Match Score (%)'].mean(), 2)}%")
    m4.metric("Similarity Engine", st.session_state.get("similarity_method", "N/A").title())

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["🏆 Ranking Table", "📈 Charts", "☁️ Word Cloud"])

    with tab1:
        search_col, sort_col = st.columns([2, 1])
        with search_col:
            search_term = st.text_input("🔍 Search candidate by name")
        with sort_col:
            sort_order = st.selectbox("Sort by Match Score", ["Descending", "Ascending"])

        display_df = df.copy()
        if search_term:
            display_df = display_df[display_df["Candidate"].str.contains(search_term, case=False, na=False)]

        ascending = sort_order == "Ascending"
        display_df = display_df.sort_values("Match Score (%)", ascending=ascending).reset_index(drop=True)

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        csv_bytes = utils.dataframe_to_csv_bytes(df)
        st.download_button(
            label="⬇️ Download Full Ranking Report (CSV)",
            data=csv_bytes,
            file_name="candidate_ranking_report.csv",
            mime="text/csv",
            use_container_width=False,
        )

    with tab2:
        st.plotly_chart(visualization.build_ranking_bar_chart(df), use_container_width=True)
        st.plotly_chart(visualization.build_match_distribution_chart(df), use_container_width=True)

    with tab3:
        combined_tokens = " ".join(
            details["token_string"] for details in st.session_state["candidate_details"].values()
        )
        wc = visualization.build_wordcloud_image(combined_tokens)
        if wc is not None:
            st.image(wc.to_array(), use_container_width=True, caption="Most frequent terms across all resumes")
        else:
            st.info("Not enough text to generate a word cloud.")


# ==============================================================
# PAGE: CANDIDATE EXPLORER
# ==============================================================
def render_candidate_explorer():
    st.markdown('<div class="main-title">🔍 Candidate Explorer</div>', unsafe_allow_html=True)

    if not st.session_state.get("processed"):
        st.warning("No screening results yet. Please go to **Upload & Screen** first.")
        return

    df = st.session_state["ranking_df"]
    details = st.session_state["candidate_details"]

    for _, row in df.iterrows():
        category = ranking.get_score_category(row["Match Score (%)"])
        badge_class = BADGE_CLASS_MAP.get(category, "badge-average")

        with st.container():
            st.markdown(f"""
                <div class="candidate-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div style="font-size:1.2rem;font-weight:700;">#{row['Rank']} — {row['Candidate']}</div>
                        <span class="badge {badge_class}">{category}</span>
                    </div>
                    <div style="margin-top:0.5rem;font-size:1rem;color:#374151;">
                        Match Score: <b>{row['Match Score (%)']}%</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            with st.expander(f"View details for {row['Candidate']}"):
                c1, c2 = st.columns([1, 1])

                with c1:
                    st.progress(min(int(row["Match Score (%)"]), 100), text="Overall Match")
                    st.plotly_chart(
                        visualization.build_score_breakdown_chart(row.to_dict()),
                        use_container_width=True,
                        key=f"breakdown_{row['Candidate']}",
                    )

                with c2:
                    st.markdown("**✅ Matched Skills**")
                    st.write(utils.format_skill_list(details[row["Candidate"]]["matched_skills"]))
                    st.markdown("**❌ Missing Skills**")
                    st.write(utils.format_skill_list(details[row["Candidate"]]["missing_skills"]))
                    st.markdown("**➕ Additional Skills Found**")
                    st.write(utils.format_skill_list(details[row["Candidate"]]["extra_skills"]))

                st.markdown("**📄 Resume Preview**")
                st.text_area(
                    "Extracted text (preview)",
                    utils.truncate_text(details[row["Candidate"]]["raw_text"], 800),
                    height=150,
                    key=f"preview_{row['Candidate']}",
                    label_visibility="collapsed",
                )


# ==============================================================
# PAGE: ABOUT
# ==============================================================
def render_about():
    st.markdown('<div class="main-title">ℹ️ About This Project</div>', unsafe_allow_html=True)
    st.markdown("""
    **Smart Resume Screening & Candidate Ranking Tool** is an AI-powered application
    that helps recruiters and hiring teams quickly compare multiple candidate resumes
    against a single job description.

    #### Why this approach?
    Traditional keyword-matching ATS systems often reject qualified candidates simply
    because they phrased a skill differently than the job posting. This tool combines:

    - **Semantic similarity** (Sentence-Transformers embeddings) to understand *meaning*,
      not just exact keyword overlap.
    - **Explicit skill-gap analysis** so recruiters can see precisely which required
      skills are missing, at a glance.

    #### Tech Stack
    Streamlit · scikit-learn · Sentence-Transformers · PyMuPDF · pdfplumber ·
    python-docx · spaCy · NLTK · Pandas · NumPy · Plotly · WordCloud

    #### Disclaimer
    This tool is designed to *assist* human recruiters by surfacing relevant signals
    faster — it is not intended to replace human judgment in hiring decisions.
    """)


# ==============================================================
# FOOTER
# ==============================================================
def render_footer():
    st.markdown(
        '<div class="app-footer">Smart Resume Screening & Candidate Ranking Tool · '
        'Built for IBM PBEL Internship Project · © 2026</div>',
        unsafe_allow_html=True,
    )


# ==============================================================
# MAIN APP ENTRY POINT
# ==============================================================
def main():
    load_custom_css()
    init_session_state()

    page = render_sidebar()

    if page == "🏠 Home":
        render_home()
    elif page == "📤 Upload & Screen":
        render_upload_page()
    elif page == "📊 Dashboard":
        render_dashboard()
    elif page == "🔍 Candidate Explorer":
        render_candidate_explorer()
    elif page == "ℹ️ About":
        render_about()

    render_footer()


if __name__ == "__main__":
    main()
