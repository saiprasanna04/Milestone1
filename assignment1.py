import os
from groq import Groq

groq_api_key = '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'
client = Groq(api_key=groq_api_key)

def generate_response(prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI Assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="mixtral-8x7b-32768"  
    )
    

    return response.choices[0].message.content

def main():
    print("Welcome to the Groq Chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = generate_response(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    main()