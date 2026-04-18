# AI Resume Screening Pipeline

**Innomatics Research Labs — GenAI Orchestration Project**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/LangChain-LCEL-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/LangSmith-Enabled-green?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" />
</p>

---

## Overview

This project implements a **production-grade AI orchestration pipeline** for evaluating candidate resumes against job descriptions (JD).

Unlike traditional single-prompt approaches, this system follows a **modular, multi-stage architecture using LangChain**, ensuring:

- Structured data extraction  
- Deterministic and explainable scoring  
- Reduced hallucinations  
- Full observability and traceability  

The pipeline converts:

**Unstructured Resume → Structured JSON → Deterministic Evaluation → Human Insights**

---

## Objective

The goal of this project is to build a **transparent, auditable, and scalable resume evaluation system** that:

- Eliminates black-box LLM decision-making  
- Uses controlled JSON outputs instead of free text  
- Applies deterministic Python logic for scoring  
- Generates clear explanations for hiring managers  
- Provides full traceability using LangSmith  

---

## System Architecture

The pipeline is divided into **four distinct stages**, each designed for control, accuracy, and modularity.

---

### Step 1 — Skill Extraction  
`chains/extract_chain.py`

**Purpose:**  
Convert unstructured resume text into structured JSON.

**Implementation Details:**

- Uses `PromptTemplate` + `JsonOutputParser`  
- Strict schema enforcement  
- LLM is explicitly instructed:  

> Do NOT infer missing information  

**Output Example:**

```json
{
  "skills": ["Python", "SQL"],
  "tools": ["Docker"],
  "experience_years": 2
}
```

---

### Step 2 — Skill Matching  
`chains/match_chain.py`

**Purpose:**  
Compare extracted resume data with JD requirements.

**Implementation Details:**

- Matches:
  - Required skills  
  - Bonus skills  
  - Tools  
  - Experience  

**Output Example:**

```json
{
  "matched_skills": ["Python"],
  "missing_skills": ["Machine Learning"],
  "matched_tools": ["Docker"],
  "experience_met": false
}
```

---

### Step 3 — Hybrid Scoring  
`chains/score_chain.py`

**Purpose:**  
Generate a final score out of 100 using **deterministic + AI hybrid logic**

**Design Philosophy:**

- Avoid LLM-based math  
- Use Python for scoring  
- Use LLM only for qualitative judgment  

**Score Distribution:**

| Component       | Weight |
|----------------|--------|
| Required Skills | 40%    |
| Bonus Skills    | 20%    |
| Tools           | 20%    |
| Experience      | 10%    |
| Relevance (LLM) | 10%    |

**Key Feature:**

- Uses a mini LLM chain (`relevance_chain`) for domain alignment scoring  

---

### Step 4 — Explanation Generation  
`chains/explain_chain.py`

**Purpose:**  
Convert structured results into human-readable summaries.

**Implementation Details:**

- Disables JSON mode  
- Generates 3–8 sentence evaluation summaries  
- Designed for hiring managers  

---

## Tech Stack

| Technology    | Purpose                       |
|---------------|------------------------------|
| LangChain     | Pipeline orchestration (LCEL) |
| Groq API      | Ultra-fast LLM inference      |
| LangSmith     | Observability & debugging     |
| Python        | Deterministic scoring logic   |

---

## APIs Used

### Groq API

- Model: `llama-3.1-8b-instant`

**Benefits:**

- Fast inference  
- Free for developers  
- Strong JSON generation capability  

---

### LangSmith

- Full pipeline tracing  
- Debugging support  
- Run comparison  
- Performance monitoring  

---

## Dependencies

```bash
pip install langchain langchain-core langchain-groq langsmith python-dotenv
```

---

## Setup Guide

### 1. Get API Keys

- Groq API Key → https://console.groq.com/  
- LangSmith API Key → https://smith.langchain.com/  

---

### 2. Create Virtual Environment

#### Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

#### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install langchain langchain-core langchain-groq langsmith python-dotenv
```

---

### 4. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=resume-screening-innomatics
```

---

### 5. Run the Pipeline

```bash
python main.py
```

**Output:**

- Console results  
- `results.json` file  

---

## Sample Evaluation Results

### Strong Candidate

**Score:** 89/100  

This candidate demonstrates strong alignment with the job requirements, including proficiency in Python, machine learning, and deep learning.

---

### Average Candidate

**Score:** 47/100  

This candidate shows partial alignment with the job requirements but lacks several advanced skills.

---

### Weak Candidate

**Score:** 37/100  

This candidate has limited alignment with the required skills and does not meet expectations.

---

### Buggy Candidate (Debug Case)

**Score:** 47/100  

This test case intentionally introduces a scoring inconsistency to demonstrate debugging using LangSmith.

**Insight:**

- Detect mismatches in extracted data  
- Identify scoring inconsistencies  
- Trace pipeline execution  

---

## Design Decisions

### Deterministic Scoring

- Eliminates hallucinated numerical outputs  
- Ensures consistent evaluation  

### Strict JSON Enforcement

- Prevents pipeline crashes  
- Guarantees structured outputs  

### Modular Architecture

- Each step is independently testable  
- Easy to scale or extend  

---

## Edge Case Handling

| Scenario           | Handling Strategy                              |
|------------------|-----------------------------------------------|
| Missing experience | Defaults to `experience_met = false`          |
| Empty JD skills    | Prevents division errors                      |
| Invalid LLM output | Enforces strict JSON parsing                  |

---

## Debugging with LangSmith

### Bug Simulation

```python
experience_met = True
```

### Debug Flow

- Filter runs using: `candidate = buggy`  
- Compare normal vs buggy runs  
- Identify mismatches in scoring  

---

## Key Advantages

- Transparent pipeline  
- High performance using Groq  
- Reduced hallucination risk  
- Developer-friendly debugging  
- Production-ready design  

---

## Conclusion

This project demonstrates how to build a **robust, explainable AI system** by combining:

- Structured LLM outputs  
- Deterministic logic  
- Modular orchestration  

It serves as a strong foundation for **HR tech, ATS systems, and AI-powered hiring platforms**.

---

## Author

**Devupalli Harsha**  
Feb 2026 GenAI Internship  
Innomatics Research Labs
