import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def classify_content(content):
    prompt = f"Based on the following content, determine the most relevant industry category (e.g., Tech, Finance, Healthcare, Education, Entertainment):\n\n{content}"
    response = openai.Completion.create(
        model="gpt-4o-mini",
        prompt=prompt,
        max_tokens=20
    )
    classification = response.choices[0].text.strip()
    return classification
