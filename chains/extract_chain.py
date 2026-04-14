from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def build_extract_chain(llm, prompt_path: str = "prompts/extract_skills_prompt.txt"):
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()

    prompt = PromptTemplate(
        input_variables=["resume_text"],
        template=template,
    )

    chain = prompt | llm | JsonOutputParser()

    return chain.with_config(
        run_name="ExtractSkillsChain",
        tags=["step=extract"],
        metadata={"step": "skill_extraction", "version": "1.0"},
    )