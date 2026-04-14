from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def compute_score(match_results: dict, relevance_score: float = 5.0) -> dict:
    req_skills    = match_results.get("required_skills_from_jd",  [])
    matched_req   = match_results.get("matched_required_skills",  [])
    bonus_skills  = match_results.get("bonus_skills_from_jd",     [])
    matched_bonus = match_results.get("matched_bonus_skills",      [])
    req_tools     = match_results.get("required_tools_from_jd",   [])
    matched_tools = match_results.get("matched_tools",             [])
    exp_met       = match_results.get("experience_met",            False)

    req_score    = (len(matched_req)   / max(len(req_skills),   1)) * 40
    bonus_score  = (len(matched_bonus) / max(len(bonus_skills), 1)) * 20
    tools_score  = (len(matched_tools) / max(len(req_tools),    1)) * 20
    exp_score    = 10.0 if exp_met else 0.0
    rel_score    = (relevance_score / 10.0) * 10.0

    total = req_score + bonus_score + tools_score + exp_score + rel_score

    return {
        "required_skills_score": round(req_score,   2),
        "bonus_skills_score":    round(bonus_score, 2),
        "tools_score":           round(tools_score, 2),
        "experience_score":      round(exp_score,   2),
        "relevance_score":       round(rel_score,   2),
        "total_score":           round(total,        2),
    }

def build_relevance_chain(llm, prompt_path: str = "prompts/scoring_prompt.txt"):
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()

    prompt = PromptTemplate(
        input_variables=["match_results", "job_description"],
        template=template,
    )

    chain = prompt | llm | JsonOutputParser()

    return chain.with_config(
        run_name="RelevanceChain",
        tags=["step=score"],
        metadata={"step": "relevance_scoring", "version": "1.0"},
    )