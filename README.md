# 🚀 AI Resume Screening Pipeline

### 🏢 *Innomatics Research Labs — GenAI Orchestration Project*

---

## 📌 Overview

✨ This project implements a **production-grade AI orchestration pipeline** for evaluating candidate resumes against job descriptions (JD).

Unlike traditional single-prompt approaches, this system follows a:

> 🧠 **Modular, multi-stage architecture using LangChain**

### ✅ Key Highlights

* Structured data extraction
* Deterministic and explainable scoring
* Reduced hallucinations
* Full observability and traceability

📊 The pipeline transforms:

```
Unstructured Resume → Structured JSON → Deterministic Evaluation → Human Insights
```

---

## 🎯 Objective

Build a **transparent, auditable, and scalable** resume evaluation system that:

* ❌ Eliminates black-box LLM decisions
* ✅ Uses controlled JSON outputs
* ✅ Applies deterministic Python scoring
* ✅ Generates clear hiring insights
* ✅ Enables full traceability with LangSmith

---

## 🏗️ System Architecture

The system is divided into **4 powerful stages**:

```
Extraction → Matching → Scoring → Explanation
```

---

## 🔹 Step 1 — Skill Extraction

📁 `chains/extract_chain.py`

### 🎯 Purpose

Convert raw resume text → structured JSON

### ⚙️ Implementation

* `PromptTemplate` + `JsonOutputParser`
* Strict schema enforcement
* 🚫 No inference allowed

> “Do NOT infer missing information”

### 📤 Output Example

```json
{
  "skills": ["Python", "SQL"],
  "tools": ["Docker"],
  "experience_years": 2
}
```

---

## 🔹 Step 2 — Skill Matching

📁 `chains/match_chain.py`

### 🎯 Purpose

Compare resume vs job description

### ⚙️ Implementation

* Matches:

  * Required skills
  * Bonus skills
  * Tools
  * Experience

### 📤 Output Example

```json
{
  "matched_skills": ["Python"],
  "missing_skills": ["Machine Learning"],
  "matched_tools": ["Docker"],
  "experience_met": false
}
```

---

## 🔹 Step 3 — Hybrid Scoring

📁 `chains/score_chain.py`

### 🎯 Purpose

Generate final score (out of 100)

### 🧠 Design Philosophy

```
❌ Avoid LLM math  
✅ Use Python for scoring  
✅ Use LLM for reasoning
```

### 📊 Score Breakdown

| Component       | Weight |
| --------------- | ------ |
| Required Skills | 40%    |
| Bonus Skills    | 20%    |
| Tools           | 20%    |
| Experience      | 10%    |
| Relevance (LLM) | 10%    |

### 🔥 Key Feature

* Mini LLM chain → `relevance_chain`

---

## 🔹 Step 4 — Explanation Generation

📁 `chains/explain_chain.py`

### 🎯 Purpose

Convert results → human-friendly insights

### ⚙️ Implementation

* JSON mode disabled
* Generates **3–8 sentence summaries**
* Tailored for hiring managers

---

## ⚙️ Tech Stack

| 🧩 Technology | 🚀 Purpose                |
| ------------- | ------------------------- |
| LangChain     | Pipeline orchestration    |
| Groq API      | Ultra-fast LLM inference  |
| LangSmith     | Observability & debugging |
| Python        | Deterministic scoring     |

---

## 🔌 APIs Used

### 🧠 Groq API

* Model: `llama-3.1-8b-instant`

**Benefits:**

* ⚡ Fast inference
* 💸 Free for developers
* 🧩 Strong JSON support

---

### 🔍 LangSmith

* Full pipeline tracing
* Debugging & monitoring
* Run comparison

---

## 📦 Dependencies

```bash
pip install langchain langchain-core langchain-groq langsmith python-dotenv
```

### 📚 Breakdown

* `langchain` → Core framework
* `langchain-core` → Prompt + chain logic
* `langchain-groq` → Groq integration
* `langsmith` → Debugging
* `python-dotenv` → Env handling

---

## 🛠️ Setup Guide

### 1️⃣ Get API Keys

* Groq → https://console.groq.com/
* LangSmith → https://smith.langchain.com/

---

### 2️⃣ Create Virtual Environment

#### 🪟 Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

####  Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install langchain langchain-core langchain-groq langsmith python-dotenv
```

---

### 4️⃣ Configure Environment

Create `.env`:

```env
GROQ_API_KEY=your_groq_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=resume-screening-innomatics
```

---

### 5️⃣ Run the Pipeline

```bash
python main.py
```

---

## 📊 Sample Outputs

### 🟢 Strong Candidate

**Score:** 89/100

> Strong alignment with skills like Python, ML, DL.

---

### 🟡 Average Candidate

**Score:** 47/100

> Partial match, lacks advanced skills.

---

### 🔴 Weak Candidate

**Score:** 37/100

> Limited alignment, missing key skills.

---

### 🐞 Buggy Candidate

**Score:** 47/100

⚠️ Intentional inconsistency for debugging

**Insight:**
LangSmith helps detect mismatches in:

* Extracted data
* Matching logic
* Final scoring

---

## 🧠 Design Decisions

### ✅ Deterministic Scoring

* No hallucinated numbers
* Fully consistent results

### ✅ Strict JSON Enforcement

* Prevents crashes
* Ensures structured outputs

### ✅ Modular Design

* Easy testing
* Easy scaling

---

## ⚠️ Edge Case Handling

| Scenario           | Strategy                |
| ------------------ | ----------------------- |
| Missing experience | Default = false         |
| Empty JD skills    | Prevent division errors |
| Invalid LLM output | Enforce JSON strictly   |

---

## 🐞 Debugging with LangSmith

### 🔧 Bug Simulation

```python
experience_met = True
```

### 🔍 Debug Flow

* Filter:

```
candidate = buggy
```

* Compare runs
* Identify mismatches

---

## 📊 Key Advantages

* 🔍 Transparent pipeline
* ⚡ High performance
* 🧠 Reduced hallucinations
* 🛠️ Easy debugging
* 📈 Production-ready

---

## 🏁 Conclusion

This project shows how to build a:

> 🧠 **Robust + Explainable AI System**

By combining:

* Structured LLM outputs
* Deterministic logic
* Modular orchestration

🎯 Perfect for:

* HR Tech
* ATS Systems
* AI Hiring Platforms

---

## 👨‍💻 Author

**Devupalli Harsha**
📅 Feb 2026 GenAI Internship
🏢 Innomatics Research Labs

---

⭐ *If you found this useful, consider starring the repo!*
