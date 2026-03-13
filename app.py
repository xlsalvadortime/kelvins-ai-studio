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
with tab2:
    st.markdown("#### Business Details")
    cal_business = st.text_input("Business Name", key="cal_biz")
    cal_industry = st.text_input("Industry", key="cal_ind")
    cal_focus = st.text_input("Monthly Focus", key="cal_focus")
    cal_platforms = st.multiselect("Platforms", ["Instagram", "Twitter/X", "Facebook", "LinkedIn"], default=["Instagram", "Facebook"], key="cal_p")
    cal_tone = st.radio("Tone", ["Professional", "Casual", "Luxury", "Fun"], horizontal=True, key="cal_t")
    posts_per_week = st.slider("Posts per week", 2, 7, 3)
    
    if st.button("Generate Full Month Calendar"):
        if not cal_business or not cal_focus or not cal_platforms:
            st.warning("Please fill in all fields")
        elif not api_key:
            st.warning("No API key found")
        else:
            with st.spinner("Building your calendar... 30 seconds"):
                try:
                    client = anthropic.Anthropic(api_key=api_key)
                    prompt = "Create a 4-week social media calendar for: Business: " + cal_business + ". Industry: " + cal_industry + ". Focus: " + cal_focus + ". Tone: " + cal_tone + ". Platforms: " + ", ".join(cal_platforms) + ". Posts per week: " + str(posts_per_week) + ". Use WEEK 1, WEEK 2 etc as headers. Include platform, day, caption, hashtags for each post."
                    msg = client.messages.create(model="claude-opus-4-6", max_tokens=8192, messages=[{"role": "user", "content": prompt}])
                    result = msg.content[0].text
                    st.success("Calendar ready!")
                    st.markdown(result)
                    st.download_button("Download Calendar", result, file_name="calendar.txt")
                except Exception as e:
                    st.error("Error: " + str(e))
