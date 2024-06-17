import streamlit as st
import base64
import requests
import time
import os
import json
from openai import OpenAI

#Load API_KEY FROM .env in same directory
from dotenv import load_dotenv
load_dotenv()


# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
# OpenAI API Key
client = OpenAI(api_key=api_key)

# sample_prompt for GPT Vision 
sample_prompt = """You are a medical practitioner and an expert in analyzing medical-related images working for a very reputed hospital. You will be provided with images and you need to identify the anomalies, any disease or health issues. You need to generate the result in detailed manner. Write all the findings, next steps, recommendation, etc. You only need to respond if the image is related to a human body and health issues. You must have to answer but also write a disclaimer saying that "Consult with a Doctor before making any decisions".

Remember, if certain aspects are not clear from the image, it's okay to state 'Unable to determine based on the provided image.'

Now analyze the image and answer the above questions in the same structured manner defined above."""

# chat_prompt for the CHAT APPLICATION
chat_prompt = "You are a medical doctor, if you are given symptoms reply with the best possible diagnosis."

with st.sidebar:
    st.title('⚕️💬 MedChat App')
        
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using Streamlit and Openai API.
    
                ''')
    
# Reads an image file from a specified path, encodes the image content into a base64 string
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Using model: gpt-4o to infer the results from the base64 string
def analyze_image(image):
    base64_image = base64.b64encode(image.read()).decode('utf-8')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": sample_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    # We get the response as some openai type
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    # Converting it to json for processing and displaying results
    response_dict = response.json()

    # Extracting the main message content
    main_message_content = response_dict['choices'][0]['message']['content']
    return main_message_content

# This functions is to get responses from the chat prompt 
def get_chatbot_response(user_input, chat_prompt):
    # If no match is found, use the OpenAI API
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": chat_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    # Return the main message from the response
    return completion.choices[0].message.content

# Adding thematics to the result
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Streamlit app
st.title("Medical Image Analysis and Chat")
st.write("Upload an image to get analysis and recommendations.")

# Upload the file
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Show the image uploaded
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)


if st.button('Analyze Image'):
    # Edge case if No Image uploaded
    if uploaded_file is None:
        st.write("No image uploaded")
    else:
        # Get the result from chatgpt function
        analysis_result = analyze_image(uploaded_file)
        st.write("Analysis Result:")
        st.write(analysis_result)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Get user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from OpenAI 
    assistant_response = get_chatbot_response(prompt, chat_prompt)
    
    # Display assistant response 
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(assistant_response))
        
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
