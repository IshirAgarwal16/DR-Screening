import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: Groq connection successful"
        }
    ],
)

print(response.choices[0].message.content)