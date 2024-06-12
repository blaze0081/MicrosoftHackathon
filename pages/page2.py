import streamlit as st
import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
# OpenAI API Key

# Sample prompt
sample_prompt = """You are a medical practitioner and an expert in analyzing medical-related images working for a very reputed hospital. You will be provided with images and you need to identify the anomalies, any disease or health issues. You need to generate the result in detailed manner. Write all the findings, next steps, recommendation, etc. You only need to respond if the image is related to a human body and health issues. You must have to answer but also write a disclaimer saying that "Consult with a Doctor before making any decisions".

Remember, if certain aspects are not clear from the image, it's okay to state 'Unable to determine based on the provided image.'

Now analyze the image and answer the above questions in the same structured manner defined above."""

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

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

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_dict = response.json()

    # Extracting the main message content
    main_message_content = response_dict['choices'][0]['message']['content']
    return main_message_content

# Streamlit app
st.title("Medical Image Analysis")
st.write("Upload an image to get analysis and recommendations.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)


if st.button('Analyze Image'):
    if uploaded_file is None:
        st.write("No image uploaded")
    else:
        analysis_result = analyze_image(uploaded_file)
        st.write("Analysis Result:")
        st.write(analysis_result)