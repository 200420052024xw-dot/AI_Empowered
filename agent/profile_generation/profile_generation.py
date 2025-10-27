from API.api_siliconflow import llm
from service.tool import get_prompt,load_toml

def profile_generation(content,user_title,user_information):
    prompt_profile_create = get_prompt(load_toml("agent/profile_generation/profile_generation.toml")["prompt"],content=content,user_title=user_title,user_information=user_information)
    profile_result = llm(content,prompt_profile_create,load_toml("agent/profile_generation/profile_generation.toml")["model"])
    return profile_result