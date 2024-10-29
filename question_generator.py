from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_content(content):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that classifies content into categories. Only respond with one word that represents the most relevant category."
            },
            {
                "role": "user",
                "content": f"Classify the following content into one word (e.g., Tech, Finance, Healthcare, Education, Entertainment): {content}"
            }
        ],
        max_tokens=1
    )
    classification = completion.choices[0].message.content.strip()
    return classification

def generate_questions(industry):
    prompt = (
        f"Generate 5 multiple-choice questions to understand a user's interests within the {industry} industry. "
        "Each question should have a 'question' field and an 'options' field with 3-4 possible answers. "
        "Please format the response as a JSON array of objects like this: "
        '[{"question": "Sample question?", "options": ["Option 1", "Option 2", "Option 3"]}]'
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a question-generating assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    
    raw_response = response.choices[0].message.content.strip()
    print("Raw OpenAI Response:", raw_response)
    
    cleaned_response = re.sub(r"^```json|```$", "", raw_response).strip()
    
    try:
        questions_json = json.loads(cleaned_response)
        if not isinstance(questions_json, list) or not questions_json:
            questions_json = [{"error": "Failed to generate structured questions"}]
    except json.JSONDecodeError:
        questions_json = [{"error": "Failed to parse JSON"}]
    
    return questions_json
