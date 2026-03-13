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
tab1, tab2 = st.tabs(["Single Posts", "Full Month Calendar"])

with tab1:
    st.markdown("#### Business Details")
    business_name = st.text_input("Business Name", placeholder="e.g. Mama Tolu Kitchen")
    industry = st.text_input("Industry", placeholder="e.g. Restaurant, Real Estate")
    topic = st.text_input("What to promote?", placeholder="e.g. Weekend jollof rice special")
    platforms = st.multiselect("Platforms", ["Instagram", "Twitter/X", "Facebook", "LinkedIn"], default=["Instagram", "Facebook"])
    tone = st.radio("Tone", ["Professional", "Casual", "Luxury", "Fun"], horizontal=True)
    num_posts = st.slider("Posts per platform", 1, 10, 3)
    client_email = st.text_input("Client Email (optional)")
    
    if st.button("Generate Posts"):
        if not business_name or not topic or not platforms:
            st.warning("Please fill in all fields")
        elif not api_key:
            st.warning("No API key found")
        else:
            with st.spinner("Generating..."):
                try:
                    client = anthropic.Anthropic(api_key=api_key)
                    prompt = "Create " + str(num_posts) + " posts for " + ", ".join(platforms) + ". Business: " + business_name + ". Industry: " + industry + ". Topic: " + topic + ". Tone: " + tone + ". Use platform names as headers. Add hashtags and emojis."
                    msg = client.messages.create(model="claude-opus-4-6", max_tokens=4096, messages=[{"role": "user", "content": prompt}])
                    result = msg.content[0].text
                    st.success("Done!")
                    st.markdown(result)
                    st.download_button("Download", result, file_name="posts.txt")
                except Exception as e:
                    st.error("Error: " + str(e))
