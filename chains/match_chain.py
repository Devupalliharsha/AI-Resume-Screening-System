from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_match_chain(llm, prompt_path: str = "prompts/match_skills_prompt.txt"):
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()

    prompt = PromptTemplate(
        input_variables=["extracted_features", "job_description"],
        template=template,
    )

    chain = prompt | llm | JsonOutputParser()

    return chain.with_config(
        run_name="MatchSkillsChain",
        tags=["step=match"],
        metadata={"step": "skill_matching", "version": "1.0"},
    )