import streamlit as st
from codes.DiseaseModel import DiseaseModel
from codes.helper import prepare_symptoms_array
import numpy as np

st.title("Predict your Disease using Machine Learning")

# Create disease class and load ML model
disease_model = DiseaseModel()
disease_model.load_model('models/saved_models/random_forest_model.json')

# Get the symptoms from codes/DiseaseModel
symptoms = st.multiselect('What are your symptoms?', options=disease_model.all_symptoms)
# Symptoms list
X = prepare_symptoms_array(symptoms)

if st.button('Predict'):
    # Edge case if no symptom is provided
    if np.count_nonzero(X) == 0:  # Check if X is a zero vector
        st.write('## Please enter your Symptoms')
    else:
        # Run the model with the python script
        prediction, prob = disease_model.predict(X)
        if prob < 0.1:  # Check if the probability is less than 10%
            st.write('## Cannot judge based on given symptoms\n ### Provide more symptoms if possible')
        else:
            st.write(f'## Disease: {prediction} with {prob*100:.2f}% probability')

            
            st.write(disease_model.describe_predicted_disease())

            
