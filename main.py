"""
main.py
AI Resume Screening Pipeline
Runs 3 candidate cases + 1 intentional bug case for LangSmith debugging.
"""

import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from chains.extract_chain  import build_extract_chain
from chains.match_chain    import build_match_chain
from chains.score_chain    import build_relevance_chain, compute_score
from chains.explain_chain  import build_explain_chain

# ─── 1. Environment ──────────────────────────────────────────────────────────
# Load API keys from the .env file
load_dotenv()

# ─── 2. LLM ──────────────────────────────────────────────────────────────────
base_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
json_llm = base_llm.bind(response_format={"type": "json_object"})

# ─── 3. Chains ───────────────────────────────────────────────────────────────
extract_chain   = build_extract_chain(json_llm)
match_chain     = build_match_chain(json_llm)
relevance_chain = build_relevance_chain(json_llm)
explain_chain   = build_explain_chain(base_llm) # Uses base_llm so it can output normal text

# ─── 4. Sample Data ──────────────────────────────────────────────────────────
JOB_DESCRIPTION = """
We are hiring a Machine Learning Engineer at a growing AI startup.
Required Skills:   Python, machine learning, deep learning, data preprocessing, model deployment
Required Tools:    Python, TensorFlow or PyTorch, scikit-learn, Docker, Git
Bonus Skills:      MLOps, cloud platforms (AWS or GCP), NLP, computer vision
Required Experience: 3+ years in machine learning or a closely related field
"""

STRONG_RESUME = """
John Doe | Senior ML Engineer
5 years total experience.
Skills: Python, machine learning, deep learning, data preprocessing,
        model deployment, NLP, computer vision, MLOps, team collaboration.
Tools:  Python, TensorFlow, PyTorch, scikit-learn, Docker, Git, AWS, MLflow.
Experience:
  Senior ML Engineer — TechCorp (3 years): deployed deep learning NLP models.
  ML Engineer — DataStart (2 years): built scikit-learn preprocessing pipelines.
Education: M.S. Computer Science, Stanford University.
"""

AVERAGE_RESUME = """
Jane Smith | Data Scientist
2 years experience.
Skills: Python, machine learning, data preprocessing, statistical analysis, communication.
Tools:  Python, scikit-learn, Git, Jupyter Notebook, Pandas.
Experience:
  Data Scientist — Analytics Co. (2 years): built ML classification models.
Education: B.S. Statistics, University of Michigan.
"""

WEAK_RESUME = """
Alex Brown | Junior Web Developer
6 months internship experience.
Skills: HTML, CSS, JavaScript, basic Python, teamwork.
Tools:  JavaScript, React, CSS, Python (beginner).
Experience:
  Frontend Intern — WebAgency (6 months): built React UI components.
Education: B.S. Computer Science, Local State University.
"""

# ─── 5. Pipeline ─────────────────────────────────────────────────────────────
def run_pipeline(resume_text, job_description, candidate_type, force_bug=False):
    """
    Execute all 4 pipeline steps for one candidate.
    """
    tag = f"candidate={candidate_type}"

    # Step 1 — Extract
    extracted = extract_chain.with_config(
        tags=[tag], run_name=f"Extract-{candidate_type}"
    ).invoke({"resume_text": resume_text})

    # Step 2 — Match
    matches = match_chain.with_config(
        tags=[tag], run_name=f"Match-{candidate_type}"
    ).invoke({
        "extracted_features": json.dumps(extracted),
        "job_description":    job_description,
    })

    # Step 3a — Relevance (LLM)
    rel_out = relevance_chain.with_config(
        tags=[tag], run_name=f"Relevance-{candidate_type}"
    ).invoke({
        "match_results":  json.dumps(matches),
        "job_description": job_description,
    })
    rel_score = float(rel_out.get("relevance_score", 5.0))

    # Step 3b — Deterministic Score
    if force_bug:
        matches_for_score = {**matches, "experience_met": True}
    else:
        matches_for_score = matches

    breakdown   = compute_score(matches_for_score, rel_score)
    final_score = breakdown["total_score"]

    # Step 4 — Explain
    explanation = explain_chain.with_config(
        tags=[tag], run_name=f"Explain-{candidate_type}"
    ).invoke({
        "score":              str(final_score),
        "match_results":      json.dumps(matches),
        "extracted_features": json.dumps(extracted),
    })

    return {
        "candidate_type":     candidate_type,
        "extracted_features": extracted,
        "match_results":      matches,
        "score_breakdown":    breakdown,
        "score":              final_score,
        "explanation":        explanation,
    }

# ─── 6. Execute ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    runs = [
        (STRONG_RESUME,  "strong",  False),
        (AVERAGE_RESUME, "average", False),
        (WEAK_RESUME,    "weak",    False),
        (WEAK_RESUME,    "buggy",   True),
    ]

    all_results = []
    for resume, ctype, bug in runs:
        print(f"\n{'='*55}\n  {ctype.upper()} candidate\n{'='*55}")
        result = run_pipeline(resume, JOB_DESCRIPTION, ctype, force_bug=bug)
        all_results.append(result)
        print(f"  Score: {result['score']}")
        print(f"  {result['explanation'][:180]}...")

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print("\n✓ results.json saved")
    print("✓ LangSmith traces: https://smith.langchain.com")