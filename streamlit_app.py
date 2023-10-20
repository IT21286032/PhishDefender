import streamlit as st
import joblib

# Function to load models from the models directory
def load_models():
    models = {}
    models_directory = 'models'  # Assuming models are saved in the 'models' directory in your repository

    # Load each model using joblib
    for model_name in ['Decision Tree', 'Random Forest', 'Multilayer Perceptrons', 'XGBoost', 'SVM', 'AutoEncoder']:
        model_path = f'{models_directory}/{model_name}_model.pkl'  # Path to the model file in the models directory
        models[model_name] = joblib.load(model_path)

    return models

st.title('Phishing Website Detection using Machine Learning')
st.write('This ML-based app is developed for educational purposes. The objective of the app is detecting phishing websites only using content data. Not URL!'
         ' You can see the details of the approach, dataset, and feature set if you click on _"See The Details"_. ')

with st.expander("PROJECT DETAILS"):
    # Your project details content here

# Load models
models = load_models()

# Streamlit UI
st.title('Phishing Website Detection App')
choice = st.selectbox("Please select your machine learning model",
                        ['Decision Tree', 'Random Forest', 'Multilayer Perceptrons', 'XGBoost', 'SVM', 'AutoEncoder'])

# Check if a URL is phishing or legitimate
url = st.text_input('Enter the URL')
if st.button('Check!'):
    # Load the selected model
    selected_model = models[choice]

    try:
        # Perform the necessary processing and make predictions using the selected model
        # (Replace this part with your actual processing logic using the selected model)
        result = selected_model.predict(url)  # Replace 'url' with the processed input data
        if result == 0:
            st.success("This web page seems legitimate!")
        else:
            st.warning("Attention! This web page is a potential phishing site!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
