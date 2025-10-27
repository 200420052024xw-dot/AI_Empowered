from API.api_siliconflow import llm
from service.tool import get_prompt,load_toml

def comment_create(content,user_title,user_information):
    prompt_comment_create = get_prompt(load_toml("agent/commentator/commentator_information.toml")["prompt"],content=content,user_title=user_title,user_information=user_information)
    comment_result = llm(content,prompt_comment_create,load_toml("agent/commentator/commentator_information.toml")["model"])
    return comment_result