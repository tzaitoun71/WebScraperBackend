from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_content(content):
    # Create a message for classification using the "gpt-4o-mini" model
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
        max_tokens=1  # Limit to 1 token to encourage a one-word response
    )
    
    # Extract and clean the classification result
    classification = completion.choices[0].message.content.strip()
    return classification
