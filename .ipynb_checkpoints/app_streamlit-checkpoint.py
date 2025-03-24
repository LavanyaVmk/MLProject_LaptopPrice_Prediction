import os
os.system("pip install -r requirements.txt")

import streamlit as st
import pickle
import numpy as np

# Load the trained model and dataset
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

# MUST be the first Streamlit command
st.set_page_config(page_title="Laptop Price Predictor", layout="wide")

# Use your GitHub-hosted background image
background_image_url = "https://github.com/LavanyaVmk/Laptop-Price-Prediction-ML/blob/main/img1.jpeg?raw=true"

# Apply custom CSS
st.markdown(f"""
<style>
/* Remove all default margins/padding from HTML, body, and .stApp */
html, body, .stApp {{
    margin: 0 !important;
    padding: 0 !important;
}}

/* Background image => pinned, no top margin */
.stApp {{
    background: url("{background_image_url}") no-repeat center center fixed;
    background-size: 80%;
}}

/* Title container => pinned to left, near top */
.title-container {{
    position: absolute;
    left: 0;
    top: 10px;  /* Adjust as needed */
    padding: 0 0 0 0;
    margin: 0;
    z-index: 9999; /* ensure on top */
}}

/* Title box => no solid border, left side flat, right side curved, royal blue shadow */
.title-box {{
    background-color: #fffd37; /* Sunshine Yellow */
    color: #1900ff; /* Royal Blue text */
    font-size: 32px;
    font-weight: bold;
    padding: 10px 20px;
    border: none;
    border-radius: 0 50px 50px 0; /* left flat, right curved */
    box-shadow: 0 0 0 4px rgba(65,105,225,0.5); /* Royal Blue shadow, transparent style */
    position: relative;
    overflow: hidden;
    display: inline-block;
}}

/* Form container => margin-left to avoid overlap with title */
.form-container {{
    margin-left: 260px; /* Enough to clear the title container on the left */
    margin-top: 40px;   /* Some gap from the top */
    padding: 0 15% !important; /* to center horizontally if needed */
}}

/* Gap below the Predict button => 30px for spacing before price box */
.predict-button-gap {{
    margin-bottom: 30px !important;
}}

/* Input label styling => bigger font, centered */
div[data-testid="stSelectbox"] label, 
div[data-testid="stNumberInput"] label, 
div[data-testid="stSlider"] label {{
    color: #4169E1 !important;
    font-weight: bold;
    font-size: 22px !important;
    text-align: center;
    display: block;
    margin: 0 auto 5px auto;
}}
div[data-testid="stSelectbox"],
div[data-testid="stNumberInput"],
div[data-testid="stSlider"] {{
    width: 100% !important; /* let them fill container width, see container margin for overall alignment */
    color: black !important;
    font-weight: bold !important;
    margin-bottom: 15px !important;
}}

/* Smaller text inputs => ~120px wide, with yellowish border + glow on hover */
div[data-baseweb="input"] {{
    box-sizing: border-box;
    border: 2px solid rgba(255, 255, 0, 0.4) !important; /* yellowish transparent border */
    border-radius: 10px !important;
    background: #f0fff0 !important;
    color: #000 !important;
    height: 36px !important;
    line-height: 26px !important;
    padding: 0 6px !important;
    font-size: 20px !important;
    margin: 3px auto !important;
    width: 120px !important; /* half original ~ 120px */
    display: block !important; 
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05) !important; 
}}
div[data-baseweb="input"]:hover {{
    box-shadow: 0 0 5px rgba(255, 255, 0, 0.6) !important; /* subtle glow */
}}

/* Predict Button => pop-over effect on hover */
.stButton {{
    display: flex;
    justify-content: center;
    margin-bottom: 0 !important;
}}
.stButton > button {{
    background-color: #4169E1 !important;
    color: #fffd37 !important;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 22px !important;
    font-weight: bold;
    margin-top: 10px !important;
    border: none;
    width: 220px;
    height: 50px !important;
    transition: transform 0.3s ease-in-out, background-color 0.3s ease-in-out;
}}
.stButton > button:hover {{
    background-color: #39FF14 !important;
    color: black !important;
    transform: scale(1.1) rotate(2deg);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}}

/* Price Display Box => no solid border, only a subtle royal blue shadow, more curved corners */
.price-box {{
    background-color: #fffd37;
    padding: 20px;
    border-radius: 20px; /* Larger curve */
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    width: 60%;
    margin: auto;
    box-shadow: 0 0 0 4px rgba(65,105,225,0.5);
    transition: box-shadow 0.3s ease, transform 0.3s ease;
    margin-bottom: 30px !important; /* some space at bottom */
}}
.price-box:hover {{
    transform: scale(1.05);
    box-shadow: 0 0 0 6px rgba(65,105,225,0.5);
}}
</style>
""",
unsafe_allow_html=True
)

# Title container => pinned on the left
st.markdown("""
<div class="title-container">
    <div class="title-box">
        <span style="margin-right:8px;">&#128187;</span> Laptop Price Predictor
    </div>
</div>
""", unsafe_allow_html=True)

# Main form container
st.markdown("""<div class="form-container">""", unsafe_allow_html=True)

# Input Fields
company = st.selectbox('**Brand**', df['Company'].unique())
laptop_type = st.selectbox('**Type**', df['TypeName'].unique())
ram = st.selectbox('**Memory (RAM in GB)**', [2, 4, 6, 8, 12, 16, 24, 32, 64])
touchscreen = st.selectbox('**Touchscreen**', ['No', 'Yes'])
hdd = st.selectbox('**Hard Drive (HDD in GB)**', [0, 128, 256, 512, 1024, 2048])
weight = st.number_input('**Weight (in Kg)**', min_value=0.0, step=0.1)
ips = st.selectbox('**IPS Display**', ['No', 'Yes'])
ssd = st.selectbox('**Solid State Drive (SSD in GB)**', [0, 8, 128, 256, 512, 1024])
screen_size = st.slider('**Screen Size (in inches)**', 10.0, 18.0, 13.0)
resolution = st.selectbox('**Screen Resolution**', [
    '1920x1080', '1366x768', '1600x900', '3840x2160',
    '3200x1800', '2880x1800', '2560x1600', '2560x1440', '2304x1440'
])
cpu = st.selectbox('**Processor (CPU)**', df['Cpu brand'].unique())
gpu = st.selectbox('**Graphics Card (GPU)**', df['Gpu brand'].unique())
os = st.selectbox('**Operating System**', df['os'].unique())

# Predict Button with a gap afterwards
predict_button = st.button('Predict Price', key='predict_button')
st.markdown("<div class='predict-button-gap'></div>", unsafe_allow_html=True)

# Price Display (shown only if user clicked predict)
if predict_button:
    touchscreen_val = 1 if touchscreen == 'Yes' else 0
    ips_val = 1 if ips == 'Yes' else 0
    X_res, Y_res = map(int, resolution.split('x'))
    ppi = ((X_res ** 2) + (Y_res ** 2)) ** 0.5 / screen_size

    query = np.array([company, laptop_type, ram, weight, touchscreen_val, ips_val, ppi, cpu, hdd, ssd, gpu, os]).reshape(1, -1)
    predicted_price = int(np.exp(pipe.predict(query)[0]))
    price_inr = f"₹{predicted_price:,.2f}"

    st.markdown(f"""
    <div class='price-box'>
        🏷️ Estimated Laptop Price:
        <span style="color: #d80000;">{price_inr}</span>
    </div>
    """, unsafe_allow_html=True)

# Close form container
st.markdown("</div>", unsafe_allow_html=True)
