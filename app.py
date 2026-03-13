import streamlit as st
import anthropic

st.set_page_config(page_title="Kelvins AI Studio", layout="wide")

api_key = ""
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except:
    pass

with st.sidebar:
    st.markdown("### Settings")
    if not api_key:
        api_key = st.text_input("API Key", type="password")
    else:
        st.success("API Key loaded")

st.markdown("## Kelvins AI Studio")
st.markdown("AI-powered social media content")
st.markdown("---")
