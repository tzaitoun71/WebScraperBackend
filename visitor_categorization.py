from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def categorize_user_profile(industry, questions, responses):
    categorization_prompt = (
        f"The visitor is interested in the {industry} industry. Based on the following questions and responses, "
        "categorize the user's profile in a few words, taking into account their interests within this industry. "
        "Please respond with only the categorization, without any extra words or formatting.\n\n"
        "Questions and Answers:\n"
    )

    for i, (question, answer) in enumerate(zip(questions, responses)):
        categorization_prompt += f"Q{i+1}: {question}\nA{i+1}: {answer}\n"
    
    categorization_prompt += "\nProvide a concise categorization based on the answers and industry context."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a categorizing assistant who identifies visitor profiles based on their answers to multiple-choice questions."},
            {"role": "user", "content": categorization_prompt}
        ],
        max_tokens=50
    )

    user_profile = response.choices[0].message.content.strip()
    return user_profile
