import os
import pickle
import numpy as np
import streamlit as st

# Page configuration
st.set_page_config(page_title="Laptop Price Predictor", layout="wide")

# Load model and data
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))



# Custom CSS
st.markdown(f"""
    <style>
    /* Hide default Streamlit headers/footers */
    header[data-testid="stHeader"] {{ display: none }}
    footer[data-testid="stFooter"] {{ display: none }}
    
    /* Background styling */
    .stApp {{
        background: url("https://github.com/LavanyaVmk/Laptop-Price-Prediction-ML/blob/main/img1.jpeg?raw=true") no-repeat center center fixed;
        background-size: cover;
    }}
    
    /* Main container adjustments */
    .block-container {{
        padding-left: 8% !important;
        padding-right: 50% !important;
    }}
    
    /* Title styling */
    .title-container {{
        margin-top: 15px;
        text-align: left;
        margin-bottom: 30px;
    }}
    .title-box {{
        display: inline-block;
        width: 80%;
        background-color: #fffd37;
        color: #1900ff;
        font-size: 35px;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 0 50px 50px 0;
        box-shadow: 0 0 0 4px rgba(65,105,225,0.5);
    }}
    
    /* Form container */
    .form-container {{
        margin-top: 20px;
        margin-left: -2px;
        width: 50%;
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0,0,0,0.2);
    }}
    
    /* SELECTBOX styling */
    div[data-testid="stSelectbox"] > div:first-child {{
        border: 2px solid #39FF14 !important;
        border-radius: 10px !important;
        background: #f0fff0 !important;
        padding: 4px 12px !important;
        transition: all 0.3s ease !important;
    }}
    div[data-testid="stSelectbox"]:hover > div:first-child {{
        box-shadow: 0 0 10px #39FF14 !important;
    }}
    
    /* NUMBER INPUT styling */
    div[data-testid="stNumberInput"] > div:first-child {{
        border: 2px solid #39FF14 !important;
        border-radius: 10px !important;
        background: #f0fff0 !important;
        height: 45px !important;
        padding: 0 10px !important;
    }}
    div[data-testid="stNumberInput"]:hover > div:first-child {{
        box-shadow: 0 0 10px #39FF14 !important;
    }}
    
    /* SLIDER styling */
    div[data-testid="stSlider"] > div > div > div[data-baseweb="slider-track"] {{
        border: 2px solid #39FF14 !important;
        border-radius: 10px !important;
        background: #f0fff0 !important;
        height: 28px !important;
    }}
    div[data-testid="stSlider"]:hover > div > div > div[data-baseweb="slider-track"] {{
        box-shadow: 0 0 10px #39FF14 !important;
    }}
    
    /* LABEL styling */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSlider"] label {{
        color: #FF5B00 !important;
        font-weight: bold !important;
        font-size: 20px !important;
        margin-bottom: 8px !important;
    }}
    
    /* Predict button styling */
    .stButton > button {{
        background-color: #4169E1 !important;
        color: #fffd37 !important;
        border-radius: 8px !important;
        padding: 12px 25px !important;
        font-size: 22px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        margin-top: 20px !important;
    }}
    .stButton > button:hover {{
        background-color: #39FF14 !important;
        color: #000 !important;
        transform: scale(1.05) rotate(2deg);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
    }}
    
    /* Price display styling */
    .price-box {{
        background-color: #fffd37;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 27px;
        font-weight: bold;
        margin: 30px auto 0 auto;
        box-shadow: 0 0 0 4px rgba(65,105,225,0.5);
        animation: pulse 1.5s infinite;
    }}
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.02); }}
        100% {{ transform: scale(1); }}
    }}
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<div class="title-container">
    <div class="title-box">
        &#128187; Laptop Price Predictor
    </div>
</div>
""", unsafe_allow_html=True)

# Input Form
with st.container():
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    
    # Input fields
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

    # Prediction logic
    if st.button('Predict Price'):
        # Convert inputs
        touchscreen_val = 1 if touchscreen == 'Yes' else 0
        ips_val = 1 if ips == 'Yes' else 0
        X_res, Y_res = map(int, resolution.split('x'))
        ppi = ((X_res**2 + Y_res**2)**0.5)/screen_size
        
        # Create query array
        query = np.array([company, laptop_type, ram, weight, touchscreen_val,
                         ips_val, ppi, cpu, hdd, ssd, gpu, os]).reshape(1, -1)
        
        # Predict and display
        price = int(np.exp(pipe.predict(query)[0]))
        st.markdown(f"""
        <div class='price-box'>
            🏷️ Estimated Price: <span style="color: #d80000;">₹{price:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)