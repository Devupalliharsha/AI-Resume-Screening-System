from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def build_explain_chain(llm, prompt_path: str = "prompts/explanation_prompt.txt"):
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()

    prompt = PromptTemplate(
        input_variables=["score", "match_results", "extracted_features"],
        template=template,
    )

    chain = prompt | llm | StrOutputParser()

    return chain.with_config(
        run_name="ExplainChain",
        tags=["step=explain"],
        metadata={"step": "explanation", "version": "1.0"},
    )