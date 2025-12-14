
import os
from dotenv import load_dotenv

load_dotenv()

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

print("AI Email Personalizer Setup")

profile_input = input("Enter the recipient's LinkedIn URL or Bio : \n")
product_input = input("Enter the  product or services you are offering : \n")
goal_input = input("Enter Your Goal (eg: partnership,customer, investor) : \n")

print("Processing inputs and generating email...")
print("-----------------------------------------")

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
    import json
    ai_response = json.loads(chat_completion.choices[0].message.content)

    print("\n AI Generated Email")
    print("---------------------")
    print(f"SUBJECT: {ai_response.get('subject','N/A')}")
    print(f"BODY: {ai_response.get('body','N/A')}")

except Exception as e:
    print(f"\n An error occured during LLM call: {e}")
    print("Please check the API key, network connection, or prompt format")


