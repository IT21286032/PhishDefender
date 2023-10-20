import streamlit as st
import subprocess
import os
import joblib

from url_feature_extraction import featureExtraction
import pandas as pd

feature_names = ['length_url', 'ip', 'nb_at', 'https_token', 'nb_subdomains',
                 'prefix_suffix', 'shortening_service', 'nb_redirection',
                 'nb_external_redirection', 'iframe', 'onmouseover', 'right_clic',
                 'web_traffic', 'dns_record']



# Check if joblib is installed, and if not, install it
try:
    import joblib
except ImportError:
    st.write("Installing joblib...")
    subprocess.check_call(["pip", "install", "joblib"])
    st.write("joblib installed successfully. Please restart the app.")

# Function to load models from the models directory with added debugging information
def load_models():
    models = {}
    models_directory = 'models'  # Models are saved in the 'models' directory adjacent to the Streamlit script

    # Model file names
    model_file_names = [
        'Decision Tree_model.pkl',
        'Multilayer Perceptrons_model.pkl',
        'Random Forest_model.pkl',
        'SVM_model.pkl',
        'XGBoost_model.pkl'
    ]

    # Load each model using joblib
    for model_file in model_file_names:
        model_path = f'models/{model_file}'
        # Check if the model file exists
        if not os.path.exists(model_path):
            st.error(f"The model file '{model_path}' does not exist.")
            continue

        # Extract model name from the file name (remove "_model.pkl" and convert underscores to spaces)
        model_name = model_file.replace('_model.pkl', '').replace('_', ' ')

        # Load the model
        try:
            models[model_name] = joblib.load(model_path)

            #st.success(f"Successfully loaded model '{model_name}' from path '{model_path}'.")

            #st.success(f"Successfully loaded model '{model_name}' from path '{model_path}'.")

        except Exception as e:
            st.error(f"Error loading model '{model_name}' from path '{model_path}': {e}")

    return models

models = load_models()


# ... (rest of the Streamlit app remains unchanged) ...



# ... (rest of the Streamlit app remains unchanged) ...


st.title('Phishing Website Detection using Machine Learning')
st.write('This ML-based app is developed for educational purposes. The objective of the app is detecting phishing websites only using content data. Not URL!'
         ' You can see the details of the approach, dataset, and feature set if you click on _"See The Details"_. ')

with st.expander("PROJECT DETAILS:"):
    
    st.subheader('Approach')
    st.write('I used _supervised learning_ to classify phishing and legitimate websites. '
             'I benefit from content-based approach and focus on html of the websites. '
             'Also, I used scikit-learn for the ML models.'
             )
    st.write('For this educational project, '
             'I created my own data set and defined features, some from the literature and some based on manual analysis. '
             'I used requests library to collect data, BeautifulSoup module to parse and extract features. ')
    st.write('The source code and data sets are available in the below Github link:')
    st.write('_https://github.com/emre-kocyigit/phishing-website-detection-content-based_')

    st.subheader('Data set')
    st.write('I used _"phishtank.org"_ & _"tranco-list.eu"_ as data sources.')
    st.write('Totally 26584 websites ==> **_16060_ legitimate** websites | **_10524_ phishing** websites')
    st.write('Data set was created in October 2022.')

with st.expander('EXAMPLE PHISHING URLs:'):
    st.write('_https://rtyu38.godaddysites.com/_')
    st.write('_https://karafuru.invite-mint.com/_')
    st.write('_https://defi-ned.top/h5/#/_')
    st.caption('REMEMBER, PHISHING WEB PAGES HAVE SHORT LIFECYCLE! SO, THE EXAMPLES SHOULD BE UPDATED!')
    
# User selects a model
choice = st.selectbox("Please select your machine learning model",
                     ['Decision Tree', 'Random Forest', 'Multilayer Perceptrons', 'XGBoost', 'SVM'])

st.write(f'{choice} is selected')

# Check if a URL is phishing or legitimate





# Check if a URL is phishing or legitimate

url = st.text_input('Enter the URL')
if st.button('Check!'):
    # Load the selected model
    selected_model = models[choice]

    try:
        # Extract features from the URL
        url_features = featureExtraction(url)
        
        # Ensure the extracted features match the expected number of features
        if len(url_features) != len(feature_names):
            st.error(f"Feature mismatch! Expected {len(feature_names)} features but got {len(url_features)}")
            st.stop()  # Stop execution
        
        # Convert to DataFrame
        df = pd.DataFrame([url_features], columns=feature_names)
        
        # Make prediction using the selected model
        result = selected_model.predict(df.values)

        if result == 0:
            st.success("This web page seems legitimate!")
        else:
            st.warning("Attention! This web page is a potential phishing site!")
    except Exception as e:
        st.error(f"An error occurred while processing the URL: {e}")

