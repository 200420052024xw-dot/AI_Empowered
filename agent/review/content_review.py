from API.api_siliconflow import llm
from service.tool import get_prompt,load_toml


def content_review(content,user_title,user_information):
    prompt_comment_create = get_prompt(
        load_toml("agent\\review\content_review.toml")["prompt"],
        content=content,
    )
    comment_result = llm(
        content,
        prompt_comment_create,
        load_toml("agent\\review\content_review.toml")["model"]
    )
    return comment_result