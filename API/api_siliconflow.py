from dotenv import load_dotenv
import requests
import os

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
