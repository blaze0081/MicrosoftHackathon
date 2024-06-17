# MicrosoftHackathon
# MedChat App

This repository contains a Streamlit application called **MedChat App**. The application leverages OpenAI's GPT-4 and GPT-3.5-turbo models to provide medical image analysis and chat-based medical consultation. Additionally, it includes a disease prediction page using a machine learning model.

Application made for Microsoft Hackathon by Bhaskar Mishra & Tanmay Sharma

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/blaze0081/MicrosoftHackathon.git
    cd medchat-app
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the environment variables**:
    - Create a `.env` file in the root directory of the project.
    - Add your OpenAI API key to the `.env` file:
    ```
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

1. **Run the Streamlit application**:
    ```bash
    streamlit run app.py
    ```

2. **Access the application**:
    - Open your web browser and go to `http://localhost:8501`.

## Features

### Homepage

- **Medical Image Analysis**:
    - Upload a medical image in JPG, JPEG, or PNG format.
    - Click on "Analyze Image" to get a detailed analysis of the uploaded image, including anomalies, diseases, and recommendations.

- **Chatbot**:
    - Engage with a chatbot by entering symptoms or asking medical-related questions.
    - The chatbot will respond with potential diagnoses or relevant medical information.

### Disease Calculator Page

- **Disease Prediction**:
    - Select your symptoms from a multiselect dropdown.
    - Click on "Predict" to get a possible disease prediction along with the probability.
