from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def determine_visitor_intent(questions, responses):
    prompt = (
        "Based on the following questions and responses, determine the visitor's intent:\n\n"
        "Questions and Responses:\n" + 
        "\n".join([f"Q: {q}\nA: {a}" for q, a in zip(questions, responses)]) +
        "\n\nSummarize the visitor's intent in one sentence."
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that categorizes visitor intent based on provided questions and responses."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )

    intent = completion.choices[0].message.content.strip()
    return intent
