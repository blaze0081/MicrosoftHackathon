import streamlit as st
from codes.DiseaseModel import DiseaseModel
from codes.helper import prepare_symptoms_array
import numpy as np

st.title("Model 1")

# Create disease class and load ML model
disease_model = DiseaseModel()
disease_model.load_model('models/saved_models/random_forest_model.json')

# Title
st.write('# Disease Prediction using Machine Learning')

symptoms = st.multiselect('What are your symptoms?', options=disease_model.all_symptoms)

X = prepare_symptoms_array(symptoms)

if st.button('Predict'):
    if np.count_nonzero(X) == 0:  # Check if X is a zero vector
        st.write('## Please enter your Symptoms')
    else:
        # Run the model with the python script
        prediction, prob = disease_model.predict(X)
        if prob < 0.1:  # Check if the probability is less than 10%
            st.write('## Cannot judge based on given symptoms\n ### Provide more symptoms if possible')
        else:
            st.write(f'## Disease: {prediction} with {prob*100:.2f}% probability')

            tab1, tab2 = st.tabs(["Description", "Precautions"])

            with tab1:
                st.write(disease_model.describe_predicted_disease())

            with tab2:
                precautions = disease_model.predicted_disease_precautions()
                for i in range(4):
                    st.write(f'{i+1}. {precautions[i]}')
