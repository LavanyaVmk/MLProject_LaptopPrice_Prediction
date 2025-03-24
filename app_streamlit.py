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

        /* Form container => narrower, with left margin so it's "a little away" */
        .form-container {{
            margin-top: 40px;
            margin-left: 100px; /* Adjust as needed */
            width: 40%;         /* Adjust as needed */
            background: rgba(255,255,255,0.4);
            padding: 20px;
            border-radius: 10px;
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

        /* Text inputs => smaller, turquoise border, fill 80% of the container */
        div[data-baseweb="input"] {{
            border: 2px solid #40E0D0; /* Turquoise */
            border-radius: 10px;
            background: #f0fff0;
            color: #000;
            height: 35px;
            padding: 0 6px;
            font-size: 20px;
            width: 40%; /* 40% of .form-container */
            margin-bottom: 6px;
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
        .price-box:hover {{
            transform: scale(1.05);
            box-shadow: 0 0 0 6px rgba(65,105,225,0.5);
        }}
    </style>
""", unsafe_allow_html=True)

# LEFT-PINNED TITLE
st.markdown("""
<div class="title-container">
    <div class="title-box">
        &#128187; Laptop Price Predictor
    </div>
</div>
""", unsafe_allow_html=True)

# MAIN FORM CONTAINER
st.markdown("<div class='form-container'>", unsafe_allow_html=True)

# Input Fields
company = st.selectbox('Brand', df['Company'].unique())
laptop_type = st.selectbox('Type', df['TypeName'].unique())
ram = st.selectbox('Memory (RAM in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])
touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])
hdd = st.selectbox('Hard Drive (HDD in GB)', [0, 128, 256, 512, 1024, 2048])
weight = st.number_input('Weight (in Kg)', min_value=0.0, step=0.1)
ips = st.selectbox('IPS Display', ['No', 'Yes'])
ssd = st.selectbox('Solid State Drive (SSD in GB)', [0, 8, 128, 256, 512, 1024])
screen_size = st.slider('Screen Size (in inches)', 10.0, 18.0, 13.0)
resolution = st.selectbox('Screen Resolution', [
    '1920x1080', '1366x768', '1600x900', '3840x2160',
    '3200x1800', '2880x1800', '2560x1600', '2560x1440', '2304x1440'
])
cpu = st.selectbox('Processor (CPU)', df['Cpu brand'].unique())
gpu = st.selectbox('Graphics Card (GPU)', df['Gpu brand'].unique())
os = st.selectbox('Operating System', df['os'].unique())

# Predict Button
predict_button = st.button('Predict Price')

if predict_button:
    # Convert Yes/No to 1/0
    touchscreen_val = 1 if touchscreen == 'Yes' else 0
    ips_val = 1 if ips == 'Yes' else 0
    X_res, Y_res = map(int, resolution.split('x'))
    ppi = ((X_res ** 2) + (Y_res ** 2)) ** 0.5 / screen_size

    query = np.array([
        company, laptop_type, ram, weight, touchscreen_val, ips_val, ppi,
        cpu, hdd, ssd, gpu, os
    ]).reshape(1, -1)

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
