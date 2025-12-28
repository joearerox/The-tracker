import streamlit as st

def apply_styling():
    # This hides the default "Streamlit" menu to make it look like an app
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def show_rainbow_border():
    """Injects a temporary rainbow border animation."""
    st.markdown("""
    <style>
    @keyframes border-rotate {
        0% { border-image-source: linear-gradient(0deg, red, orange, yellow, green, blue, indigo, violet); }
        50% { border-image-source: linear-gradient(180deg, red, orange, yellow, green, blue, indigo, violet); }
        100% { border-image-source: linear-gradient(360deg, red, orange, yellow, green, blue, indigo, violet); }
    }
    .stApp {
        border: 10px solid;
        border-image-slice: 1;
        border-width: 5px;
        border-image-source: linear-gradient(to left, #743ad5, #d53a9d);
        animation: border-rotate 2s infinite linear;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.toast("🌈 Points Added! Great work!")
  
