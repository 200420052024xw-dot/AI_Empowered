from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

def llm(query, prompt, model):

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}
        ]
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('API_KEY')}",
        "Content-Type": "application/json"
    }

    response = requests.post(os.getenv("BASE_URL"), json=payload, headers=headers)

    return response.json()["choices"][0]["message"]["content"]


def view_llm(query):
    payload = json.dumps({
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """请将图片中的文字内容提取出来，并保持与原始PDF中尽可能一致的逻辑结构。
                    要求：
                    1. 保留段落结构，保持自然换行。
                    2. 如果有标题，请识别并在输出中使用合适的层级标识（如“# 一级标题”，“## 二级标题”）。
                    3. 如果有公式、特殊符号，请尽量用文本表示。
                    输出内容时，只输出识别后的文字和结构，不要添加额外说明。
                    """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": query                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    })

    headers = {
        "Authorization": f"Bearer {os.getenv('API_KEY_OPENAI')}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST",os.getenv("BASE_URL_OPENAI") , headers=headers, data=payload)

    data = response.json()
    print(data["choices"][0]["message"]["content"])

    return data
