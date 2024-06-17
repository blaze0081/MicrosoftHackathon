import openai

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = 'API'

def get_gpt3_response(prompt_text):
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use other engines like "text-curie-001" based on your requirement
        prompt=prompt_text,
        max_tokens=100,  # Adjust the max tokens based on your needs
        n=1,
        stop=None,
        temperature=0.7
    )
    
    return response.choices[0].text.strip()

# Sample text to prompt GPT-3.5
sample_text = "Write a short story about a cat who learns to play the piano."

response_text = get_gpt3_response(sample_text)
print(response_text)
