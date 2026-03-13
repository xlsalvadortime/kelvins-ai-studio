import streamlit as st
import anthropic

st.set_page_config(
page_title="Kelvins AI Studio",
page_icon=”*”,
layout=“wide”,
initial_sidebar_state=“collapsed”
)

st.markdown(”””

<style>
[data-testid="stAppViewContainer"] { background-color: #06091a; }
[data-testid="stHeader"] { background-color: #06091a; }
[data-testid="stSidebar"] { background-color: #0c1640; }
.stTextInput input { background-color: #0c1640 !important; color: #e2e8f0 !important; border: 1px solid #1e3a5f !important; border-radius: 10px !important; }
label { color: #94a3b8 !important; }
.stButton > button { background: linear-gradient(135deg, #3b82f6, #6366f1) !important; color: white !important; border: none !important; border-radius: 10px !important; font-weight: 600 !important; width: 100% !important; }
h1, h2, h3 { color: #ffffff !important; }
hr { border-color: #1e3a5f !important; }
</style>

“””, unsafe_allow_html=True)

api_key = “”
try:
api_key = st.secrets[“ANTHROPIC_API_KEY”]
except:
pass

with st.sidebar:
st.markdown(”### Settings”)
if not api_key:
api_key = st.text_input(“Anthropic API Key”, type=“password”, placeholder=“sk-ant-…”)
else:
st.success(“API Key loaded”)
st.markdown(“Kelvins AI Studio - Powered by Claude AI”)

st.markdown(”## Kelvins AI Studio”)
st.markdown(“Professional AI-powered social media content — instantly generated”)
st.markdown(”—”)

c1, c2, c3, c4 = st.columns(4)
c1.metric(“Platforms”, “4”)
c2.metric(“Posts at once”, “20+”)
c3.metric(“Calendar”, “4 Weeks”)
c4.metric(“Delivery”, “30 secs”)
st.markdown(”—”)

tab1, tab2 = st.tabs([“Single Posts”, “Full Month Calendar”])

with tab1:
col_left, col_right = st.columns([1, 1], gap=“large”)
with col_left:
st.markdown(”#### Business Details”)
business_name = st.text_input(“Business Name”, placeholder=“e.g. Mama Tolu Kitchen”)
industry = st.text_input(“Industry”, placeholder=“e.g. Restaurant, Real Estate, Fashion”)
topic = st.text_input(“What do you want to promote?”, placeholder=“e.g. Weekend jollof rice special”)
brand_color = st.color_picker(“Brand Color”, “#3b82f6”)
st.markdown(”#### Content Settings”)
platforms = st.multiselect(“Platforms”, [“Instagram”, “Twitter/X”, “Facebook”, “LinkedIn”], default=[“Instagram”, “Facebook”])
tone = st.radio(“Content Tone”, [“Professional”, “Casual”, “Luxury”, “Fun and Playful”], horizontal=True)
num_posts = st.slider(“Posts per platform”, 1, 10, 3)
st.markdown(”#### Email (Optional)”)
client_email = st.text_input(“Client Email”, placeholder=“client@example.com”)
generate_btn = st.button(“Generate Posts”)

```
with col_right:
    st.markdown("#### Generated Content")
    if generate_btn:
        if not business_name or not topic or not platforms:
            st.warning("Please fill in Business Name, Topic and select at least one Platform.")
        elif not api_key:
            st.warning("Please add your Anthropic API Key in the sidebar.")
        else:
            with st.spinner("Generating your content..."):
                try:
                    client = anthropic.Anthropic(api_key=api_key)
                    prompt = "Create " + str(num_posts) + " social media posts for each of these platforms: " + ", ".join(platforms) + ". Business: " + business_name + ". Industry: " + industry + ". Topic: " + topic + ". Tone: " + tone + ". Use INSTAGRAM, FACEBOOK etc as headers. Number each post. Include hashtags and emojis."
                    message = client.messages.create(model="claude-opus-4-6", max_tokens=4096, messages=[{"role": "user", "content": prompt}])
                    result = message.content[0].text
                    st.success("Content generated successfully!")
                    st.markdown(result)
                    st.download_button("Download Posts", result, file_name=business_name.replace(" ", "_") + "_posts.txt")
                    if client_email and "@" in client_email:
                        st.info("Ready to send to " + client_email + " - download and forward!")
                except Exception as e:
                    st.error("Error: " + str(e))
    else:
        st.info("Fill in the form and click Generate Posts")
```

with tab2:
col_a, col_b = st.columns([1, 1], gap=“large”)
with col_a:
st.markdown(”#### Business Details”)
cal_business = st.text_input(“Business Name”, placeholder=“e.g. Lagos Real Estate”, key=“cal_biz”)
cal_industry = st.text_input(“Industry”, placeholder=“e.g. Real Estate, Restaurant”, key=“cal_ind”)
cal_focus = st.text_input(“Monthly Focus”, placeholder=“e.g. New property launches in Lekki”, key=“cal_focus”)
cal_brand_color = st.color_picker(“Brand Color”, “#3b82f6”, key=“cal_color”)
st.markdown(”#### Calendar Settings”)
cal_platforms = st.multiselect(“Platforms”, [“Instagram”, “Twitter/X”, “Facebook”, “LinkedIn”], default=[“Instagram”, “Facebook”], key=“cal_p”)
cal_tone = st.radio(“Content Tone”, [“Professional”, “Casual”, “Luxury”, “Fun and Playful”], horizontal=True, key=“cal_t”)
posts_per_week = st.slider(“Posts per week per platform”, 2, 7, 3)
cal_email = st.text_input(“Client Email”, placeholder=“client@example.com”, key=“cal_email”)
cal_btn = st.button(“Generate Full Month Calendar”)

```
with col_b:
    st.markdown("#### Your Content Calendar")
    if cal_btn:
        if not cal_business or not cal_focus or not cal_platforms:
            st.warning("Please fill in Business Name, Monthly Focus and select Platforms.")
        elif not api_key:
            st.warning("Please add your Anthropic API Key in the sidebar.")
        else:
            with st.spinner("Building your full month content calendar... about 30 seconds"):
                try:
                    client = anthropic.Anthropic(api_key=api_key)
                    prompt = "Create a complete 4-week social media content calendar for: Business: " + cal_business + ". Industry: " + cal_industry + ". Monthly focus: " + cal_focus + ". Tone: " + cal_tone + ". Platforms: " + ", ".join(cal_platforms) + ". Posts per week per platform: " + str(posts_per_week) + ". Use WEEK 1, WEEK 2 etc as headers with a theme name. For each post include platform, day, caption with emojis, and hashtags."
                    message = client.messages.create(model="claude-opus-4-6", max_tokens=8192, messages=[{"role": "user", "content": prompt}])
                    cal_result = message.content[0].text
                    st.success("Your full month calendar is ready!")
                    st.markdown(cal_result)
                    st.download_button("Download Full Calendar", cal_result, file_name=cal_business.replace(" ", "_") + "_calendar.txt")
                    if cal_email and "@" in cal_email:
                        st.info("Ready to send to " + cal_email + " - download and forward!")
                except Exception as e:
                    st.error("Error: " + str(e))
    else:
        st.info("Fill in the details and click Generate Full Month Calendar")
```

st.markdown(”—”)
st.markdown(“Kelvins AI Studio - Powered by Claude AI”)
