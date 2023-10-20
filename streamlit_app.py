import streamlit as st
import subprocess

# Check if joblib is installed, and if not, install it
try:
    import joblib
except ImportError:
    st.write("Installing joblib...")
    subprocess.check_call(["pip", "install", "joblib"])
    st.write("joblib installed successfully. Please restart the app.")

# Function to load models from the models directory
def load_models():
    models = {}
    models_directory = 'models'  # Assuming models are saved in the 'models' directory in your repository

    # Load each model using joblib
    for model_name in ['Decision Tree', 'Random Forest', 'Multilayer Perceptrons', 'XGBoost', 'SVM', 'AutoEncoder']:
        model_path = f'{models_directory}/{model_name}_model.pkl'  # Path to the model file in the models directory
        models[model_name] = joblib.load(model_path)

    return models
models = load_models()


st.title('Phishing Website Detection using Machine Learning')
st.write('This ML-based app is developed for educational purposes. The objective of the app is detecting phishing websites only using content data. Not URL!'
         ' You can see the details of the approach, dataset, and feature set if you click on _"See The Details"_. ')

with st.expander("PROJECT DETAILS"):
    
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
                     ['Decision Tree', 'Random Forest', 'Multilayer Perceptrons', 'XGBoost', 'SVM', 'AutoEncoder'])

print("Selected Choice:", choice)

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

