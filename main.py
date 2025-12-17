
import os
from dotenv import load_dotenv

import json

load_dotenv()

from groq import Groq

try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    # A cleaner way to handle this in a function is to set client to None
    print(f"Error initializing Groq client: {e}")
    client = None

# print("AI Email Personalizer Setup")

# profile_input = input("Enter the recipient's LinkedIn URL or Bio : \n")
# product_input = input("Enter the  product or services you are offering : \n")
# goal_input = input("Enter Your Goal (eg: partnership,customer, investor) : \n")

# print("Processing inputs and generating email...")
# print("-----------------------------------------")

def generate_email(profile_input: str,product_input: str,goal_input: str) -> dict:

    if client is None:
        return {"subject": "Error","body": "API Client not initialized.Check GROQ_API_KEY. " }

    system_instruction = (" You are an expert, highly professional Email Personalizer"
                      "Your goal is to write a concise, compelling cold email based on the user-provided context"
                      "Always maintain a respect and direct tone"
                      )

    user_prompt = (f""" 
        Using the following information , generate a  highly personalized cold email (max 4 sentences) and an optimized subject line.
    
    RECIPIENT CONTEXT (for personalization):
    - LinkedIn/Bio: {profile_input}
    
    User Offering:
    - Product/Service Description: {product_input}
    
    User Goal: 
    - Goal/Intent: {goal_input}
    
    The email must be formatted as a single JSON object with keys 'subject' and 'body'.
""")


    try:
        chat_completion = client.chat.completions.create(
        messages=[
            {
            "role": "system",
            "content": system_instruction,
            },
        {
        "role": "user",
        "content": user_prompt ,}
    ],
     model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
        ai_response = json.loads(chat_completion.choices[0].message.content)
        return {
        "subject": ai_response.get('subject', 'N/A'),
        "body": ai_response.get('body', 'N/A')
        }
    # print("\n AI Generated Email")
    # print("---------------------")
    # print(f"SUBJECT: {ai_response.get('subject','N/A')}")
    # print(f"BODY: {ai_response.get('body','N/A')}")

    except Exception as e:
        return {"subject": "Generation error", "body": f"An error occured during llm call: {e}"}
    # print(f"\n An error occured during LLM call: {e}")
    # print("Please check the API key, network connection, or prompt format")


