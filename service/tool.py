import tomllib
import json
import os
import re

def get_prompt(file_path,**kwargs):
    with open(file_path,"r+",encoding="utf-8") as pd:
        prompt_template = pd.read()
    prompt_result = prompt_template.format(**kwargs)
    return prompt_result

def load_toml(file_path: str) -> dict:
    with open(file_path, "rb") as f:
        data = tomllib.load(f)
    result = {
        "model": data["llm"]["model"],
        "prompt": data["prompt"]["path"]
    }
    return result




def clean_result(raw_output: str) -> dict:
    try:
        # 1. 去掉前后的 ```json ``` 和 ``` 标记
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", raw_output.strip())
        cleaned = re.sub(r"\n?```$", "", cleaned)

        # 2. 去除多余的空格和换行
        cleaned = cleaned.strip()

        # 3. 转换为字典
        result = json.loads(cleaned)
        return result

    except Exception:
        return raw_output
