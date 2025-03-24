import os
import streamlit as st
import pickle
import numpy as np

# Install dependencies if not already installed
os.system("pip install -r requirements.txt")

# Load the trained model and dataset
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

# Must be the first Streamlit command
st.set_page_config(page_title="Laptop Price Predictor", layout="wide")

# Background Image URL
background_image_url = "https://github.com/LavanyaVmk/Laptop-Price-Prediction-ML/blob/main/img1.jpeg?raw=true"

# Embed CSS
st.markdown(f"""
    <style>
        .stApp {{
            background: url("{background_image_url}") no-repeat center center fixed;
            background-size: 80%;
        }}
        
        /* Title container pinned to the left */
        .title-container {{
            margin-left: 20px;
            margin-top: 30px;
        }}

        /* Title box => 50% of the screen width */
        .title-box {{
            width: 50%;
            background-color: #fffd37;
            color: #1900ff;
            font-size: 36px;
            font-weight: bold;
            padding: 10px 20px;
            border: none;
            border-radius: 0 50px 50px 0;
            box-shadow: 0 0 0 4px rgba(65,105,225,0.5);
        }}

        /* Form container => wider so that text boxes can be 25% inside */
        .form-container {{
            margin-top: 40px;
            width: 60%; /* You can adjust this to suit your layout */
            background: rgba(255,255,255,0.4);
            padding: 20px;
            border-radius: 10px;
            margin-left: 50px;
        }}

        /* Input label styling */
        div[data-testid="stSelectbox"] label,
        div[data-testid="stNumberInput"] label,
        div[data-testid="stSlider"] label {{
            color: #4169E1;
            font-weight: bold;
            font-size: 22px;
            margin-bottom: 5px;
            display: block;
        }}

        /* Text inputs => 25% width, turquoise border */
        div[data-baseweb="input"] {{
            border: 2px solid #40E0D0; /* Turquoise border */
            border-radius: 10px;
            background: #f0fff0;
            color: #000;
            height: 35px;
            padding: 0 6px;
            font-size: 20px;
            width: 25%; /* 1/4 of the container width */
            margin-bottom: 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        }}
        div[data-baseweb="input"]:hover {{
            box-shadow: 0 0 5px rgba(64,224,208,0.6);
        }}

        /* Predict Button */
        .stButton > button {{
            background-color: #4169E1;
            color: #fffd37;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 22px;
            font-weight: bold;
            border: none;
            width: 220px;
            height: 50px;
            transition: transform 0.3s ease-in-out, background-color 0.3s ease-in-out;
        }}
        .stButton > button:hover {{
            background-color: #39FF14;
            color: black;
            transform: scale(1.1) rotate(2deg);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }}

        /* Price Display Box */
        .price-box {{
            background-color: #fffd37;
            padding: 20px;
            border-radius: 20px;
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            width: 70%;
            margin: auto;
            box-shadow: 0 0 0 4px rgba(65,105,225,0.5);
            margin-top: 20px;
            transition: box-shadow 0.3s ease, transform 0.3s ease;
        }}
        .price-box:hover
