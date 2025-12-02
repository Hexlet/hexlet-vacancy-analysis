import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": os.getenv("AI_KEY"),
    "HTTP-Referer": os.getenv("AI_SITE_URL"),
    "X-Title": os.getenv("AI_SITE_NAME"),
  },
  data=json.dumps({
    "model": os.getenv("AI_MODEL"),
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })
)
