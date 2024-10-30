from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_content_based_questions(content):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates intent-based questions with multiple-choice options based directly on the content of a website."},
            {"role": "user", "content": f"Generate 5 multiple-choice questions (with options) that help identify a visitor's intent for this content. Ensure questions are related to the website's primary themes and format the response as a JSON array of question objects. Content: {content}"}
        ],
        max_tokens=500
    )
    
    # Get the response content and remove backticks
    raw_response = completion.choices[0].message.content.strip().replace("```json", "").replace("```", "")
    print("Raw OpenAI Response:", raw_response)  # For debugging
    
    try:
        # Attempt to parse JSON directly
        questions_json = json.loads(raw_response)
    except json.JSONDecodeError:
        # Fallback if parsing fails
        questions_json = [{"error": "Failed to parse JSON completely"}]
    
    return questions_json
