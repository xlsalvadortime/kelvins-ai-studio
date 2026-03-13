import streamlit as st
import anthropic
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kelvin's AI Studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">
<style>
  /* ── Reset & Base ── */
  #root > div, .stApp {
    background: #06091a !important;
  }
  
  .block-container {
    padding: 0 !important;
    max-width: 100% !important;
  }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header, .stDeployButton { display: none !important; }
  .stDecoration { display: none !important; }

  /* ── Global text ── */
  * { font-family: 'DM Sans', sans-serif !important; }

  /* ── Hero Section ── */
  .hero {
    background: linear-gradient(160deg, #06091a 0%, #0c1640 50%, #0d1f6e 100%);
    padding: 60px 80px 50px;
    position: relative;
    overflow: hidden;
    border-bottom: 1px solid rgba(99,179,255,0.1);
  }

  .hero::before {
    content: '';
    position: absolute;
    width: 600px; height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
    top: -200px; right: -100px;
    pointer-events: none;
  }

  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.25);
    color: #93c5fd;
    font-size: 11px !important;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 7px 18px;
    border-radius: 100px;
    margin-bottom: 20px;
  }

  .hero-badge::before {
    content: '✦';
    color: #60a5fa;
  }

  .hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 56px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    line-height: 1.05 !important;
    letter-spacing: -1px !important;
    margin-bottom: 14px !important;
  }

  .hero-title span {
    background: linear-gradient(135deg, #60a5fa, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .hero-sub {
    color: #64748b !important;
    font-size: 17px !important;
    font-weight: 300 !important;
    max-width: 500px;
    line-height: 1.6 !important;
  }

  .hero-stats {
    display: flex;
    gap: 48px;
    margin-top: 36px;
    padding-top: 32px;
    border-top: 1px solid rgba(255,255,255,0.06);
  }

  .stat-item { display: flex; flex-direction: column; }
  .stat-num {
    font-family: 'Syne', sans-serif !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #fff !important;
  }
  .stat-label {
    font-size: 12px !important;
    color: #475569 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  /* ── Main Content ── */
  .main-content {
    padding: 50px 80px;
    max-width: 1200px;
    margin: 0 auto;
  }

  /* ── Section Label ── */
  .section-label {
    font-size: 10px !important;
    letter-spacing: 4px !important;
    text-transform: uppercase !important;
    color: #3b82f6 !important;
    margin-bottom: 8px !important;
    font-weight: 500 !important;
  }

  .section-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    color: #fff !important;
    margin-bottom: 28px !important;
  }

  /* ── Input Fields ── */
  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea,
  .stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-size: 15px !important;
    padding: 14px 18px !important;
    transition: border-color 0.2s !important;
  }

  .stTextInput > div > div > input:focus,
  .stTextArea > div > div > textarea:focus {
    border-color: rgba(59,130,246,0.5) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.08) !important;
  }

  .stTextInput label, .stTextArea label,
  .stSelectbox label, .stRadio label,
  .stColorPicker label {
    color: #94a3b8 !important;
    font-size: 13px !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 6px !important;
    font-weight: 400 !important;
  }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 14px !important;
    padding: 6px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    gap: 4px !important;
  }

  .stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    color: #64748b !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    font-weight: 500 !important;
  }

  .stTabs [aria-selected="true"] {
    background: rgba(59,130,246,0.15) !important;
    color: #93c5fd !important;
    border: 1px solid rgba(59,130,246,0.25) !important;
  }

  .stTabs [data-baseweb="tab-panel"] {
    padding-top: 32px !important;
  }

  /* ── Buttons ── */
  .stButton > button {
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.1s !important;
    cursor: pointer !important;
  }

  .stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
  }

  /* ── Post Cards ── */
  .post-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
  }

  .post-card:hover {
    border-color: rgba(59,130,246,0.25);
  }

  .post-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
  }

  .platform-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #60a5fa;
    font-weight: 500;
  }

  .post-content {
    color: #cbd5e1;
    font-size: 15px;
    line-height: 1.7;
    white-space: pre-wrap;
  }

  /* ── Success/Info boxes ── */
  .stSuccess {
    background: rgba(34,197,94,0.08) !important;
    border: 1px solid rgba(34,197,94,0.2) !important;
    border-radius: 12px !important;
    color: #86efac !important;
  }

  .stInfo {
    background: rgba(59,130,246,0.08) !important;
    border: 1px solid rgba(59,130,246,0.2) !important;
    border-radius: 12px !important;
    color: #93c5fd !important;
  }

  .stWarning {
    background: rgba(251,191,36,0.08) !important;
    border: 1px solid rgba(251,191,36,0.2) !important;
    border-radius: 12px !important;
  }

  /* ── Divider ── */
  hr {
    border-color: rgba(255,255,255,0.06) !important;
    margin: 40px 0 !important;
  }

  /* ── Spinner ── */
  .stSpinner > div {
    border-top-color: #3b82f6 !important;
  }

  /* ── Color picker ── */
  .stColorPicker > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    padding: 12px !important;
  }

  /* ── Download button ── */
  .stDownloadButton > button {
    background: rgba(59,130,246,0.1) !important;
    border: 1px solid rgba(59,130,246,0.25) !important;
    color: #93c5fd !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    width: auto !important;
  }

  /* ── Columns gap ── */
  [data-testid="column"] { padding: 0 12px !important; }

  /* ── Radio buttons ── */
  .stRadio > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 12px !important;
    flex-wrap: wrap !important;
  }

  .stRadio > div > label {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    color: #94a3b8 !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">AI-Powered Content Generation</div>
  <div class="hero-title">Kelvin's <span>AI Studio</span></div>
  <div class="hero-sub">Generate professional social media content, full month calendars and branded posts — instantly powered by Claude AI.</div>
  <div class="hero-stats">
    <div class="stat-item"><span class="stat-num">4</span><span class="stat-label">Platforms</span></div>
    <div class="stat-item"><span class="stat-num">20+</span><span class="stat-label">Posts at once</span></div>
    <div class="stat-item"><span class="stat-num">4 Weeks</span><span class="stat-label">Full Calendar</span></div>
    <div class="stat-item"><span class="stat-num">30s</span><span class="stat-label">Generation Time</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Main Content ─────────────────────────────────────────────────────────────
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# ─── API Key (sidebar or hidden) ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    st.markdown("---")
    st.markdown("**About**")
    st.markdown("Built by Kelvin's AI Studio\nPowered by Claude AI")

if not api_key:
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["✦  Single Posts", "📅  Full Month Calendar"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — SINGLE POSTS
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-label">Business Details</div>', unsafe_allow_html=True)

        business_name = st.text_input("Business Name", placeholder="e.g. Mama Tolu Kitchen")
        industry = st.text_input("Industry", placeholder="e.g. Restaurant, Real Estate, Fashion")
        topic = st.text_input("What do you want to promote?", placeholder="e.g. Weekend jollof rice special")
        brand_color = st.color_picker("Brand Color", "#3b82f6")

        st.markdown("---")
        st.markdown('<div class="section-label">Content Settings</div>', unsafe_allow_html=True)

        platforms = st.multiselect(
            "Platforms",
            ["Instagram", "Twitter/X", "Facebook", "LinkedIn"],
            default=["Instagram", "Facebook"]
        )

        tone = st.radio(
            "Content Tone",
            ["Professional", "Casual", "Luxury", "Fun & Playful"],
            horizontal=True
        )

        num_posts = st.slider("Posts per platform", 1, 10, 3)

        st.markdown("---")
        st.markdown('<div class="section-label">Email Delivery (Optional)</div>', unsafe_allow_html=True)
        client_email = st.text_input("Client Email", placeholder="client@example.com")

        generate_btn = st.button("✦ Generate Posts", use_container_width=True)

    with col_right:
        st.markdown('<div class="section-label">Generated Content</div>', unsafe_allow_html=True)

        if generate_btn:
            if not business_name or not topic or not platforms:
                st.warning("Please fill in Business Name, Topic and select at least one Platform.")
            elif not api_key:
                st.warning("Please add your Anthropic API Key in the sidebar.")
            else:
                with st.spinner("Generating your content..."):
                    try:
                        client = anthropic.Anthropic(api_key=api_key)
                        platforms_str = ", ".join(platforms)
                        prompt = (
                            "Create " + str(num_posts) + " social media posts for each of these platforms: " + platforms_str + ".\n"
                            "Business: " + business_name + "\n"
                            "Industry: " + industry + "\n"
                            "Topic: " + topic + "\n"
                            "Tone: " + tone + "\n"
                            "Brand color: " + brand_color + "\n\n"
                            "Format your response clearly with each platform as a section header like '## INSTAGRAM', '## FACEBOOK' etc.\n"
                            "Under each platform, number each post. Include relevant hashtags and emojis.\n"
                            "Make every post unique, engaging and ready to publish."
                        )
                        message = client.messages.create(
                            model="claude-opus-4-6",
                            max_tokens=4096,
                            messages=[{"role": "user", "content": prompt}]
                        )
                        result = message.content[0].text
                        st.session_state["posts_result"] = result
                        st.session_state["posts_business"] = business_name
                        st.success("✓ Content generated successfully!")

                        # Parse and display by platform
                        sections = result.split("##")
                        for section in sections:
                            if section.strip():
                                lines = section.strip().split("\n")
                                platform_name = lines[0].strip()
                                content = "\n".join(lines[1:]).strip()
                                if content:
                                    st.markdown(f"""
                                    <div class="post-card">
                                      <div class="post-header">
                                        <div class="platform-tag">✦ {platform_name}</div>
                                      </div>
                                      <div class="post-content">{content}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    # Copy button
                                    st.code(content, language=None)

                        # Download button
                        st.download_button(
                            "⬇ Download All Posts",
                            result,
                            file_name=business_name.replace(" ", "_") + "_posts.txt",
                            mime="text/plain"
                        )

                        # Email delivery
                        if client_email and "@" in client_email:
                            st.info("📧 Email delivery: Copy your posts above and send manually to " + client_email + ". (Auto-email requires SMTP setup)")

                    except Exception as e:
                        st.error("Error: " + str(e))

        elif "posts_result" not in st.session_state:
            st.markdown("""
            <div style="height:400px; display:flex; flex-direction:column; align-items:center; justify-content:center; opacity:0.3;">
              <div style="font-size:48px; margin-bottom:16px;">✦</div>
              <div style="color:#fff; font-size:16px; font-family:'Syne',sans-serif;">Your content will appear here</div>
              <div style="color:#475569; font-size:13px; margin-top:8px;">Fill in the form and hit Generate</div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — FULL MONTH CALENDAR
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    col_a, col_b = st.columns([1, 1], gap="large")

    with col_a:
        st.markdown('<div class="section-label">Business Details</div>', unsafe_allow_html=True)

        cal_business = st.text_input("Business Name ", placeholder="e.g. Lagos Real Estate")
        cal_industry = st.text_input("Industry ", placeholder="e.g. Real Estate, Restaurant")
        cal_focus = st.text_input("Monthly Focus / Theme", placeholder="e.g. New property launches in Lekki")
        cal_brand_color = st.color_picker("Brand Color ", "#3b82f6")

        st.markdown("---")
        st.markdown('<div class="section-label">Calendar Settings</div>', unsafe_allow_html=True)

        cal_platforms = st.multiselect(
            "Platforms ",
            ["Instagram", "Twitter/X", "Facebook", "LinkedIn"],
            default=["Instagram", "Facebook"]
        )

        cal_tone = st.radio(
            "Content Tone ",
            ["Professional", "Casual", "Luxury", "Fun & Playful"],
            horizontal=True
        )

        posts_per_week = st.slider("Posts per week per platform", 2, 7, 3)

        st.markdown("---")
        cal_email = st.text_input("Client Email ", placeholder="client@example.com")

        cal_btn = st.button("📅 Generate Full Month Calendar", use_container_width=True)

    with col_b:
        st.markdown('<div class="section-label">Your Content Calendar</div>', unsafe_allow_html=True)

        if cal_btn:
            if not cal_business or not cal_focus or not cal_platforms:
                st.warning("Please fill in Business Name, Monthly Focus and select Platforms.")
            elif not api_key:
                st.warning("Please add your Anthropic API Key in the sidebar.")
            else:
                with st.spinner("Building your full month content calendar... this takes about 30 seconds ✦"):
                    try:
                        client = anthropic.Anthropic(api_key=api_key)
                        cal_platforms_str = ", ".join(cal_platforms)
                        prompt = (
                            "Create a complete 4-week social media content calendar for:\n"
                            "Business: " + cal_business + "\n"
                            "Industry: " + cal_industry + "\n"
                            "Monthly focus: " + cal_focus + "\n"
                            "Tone: " + cal_tone + "\n"
                            "Platforms: " + cal_platforms_str + "\n"
                            "Posts per week per platform: " + str(posts_per_week) + "\n\n"
                            "Structure it clearly:\n"
                            "## WEEK 1 — [Theme Name]\n"
                            "## WEEK 2 — [Theme Name]\n"
                            "## WEEK 3 — [Theme Name]\n"
                            "## WEEK 4 — [Theme Name]\n\n"
                            "Under each week, for each post include:\n"
                            "- Platform name\n"
                            "- Day (Monday, Tuesday etc)\n"
                            "- Caption with emojis\n"
                            "- Hashtags\n\n"
                            "Make every post unique, on-brand and ready to publish immediately."
                        )
                        message = client.messages.create(
                            model="claude-opus-4-6",
                            max_tokens=8192,
                            messages=[{"role": "user", "content": prompt}]
                        )
                        cal_result = message.content[0].text
                        st.session_state["cal_result"] = cal_result

                        st.success("✓ Your full month calendar is ready!")

                        # Display weeks
                        weeks = cal_result.split("##")
                        for week in weeks:
                            if week.strip():
                                lines = week.strip().split("\n")
                                week_title = lines[0].strip()
                                week_content = "\n".join(lines[1:]).strip()
                                if week_content:
                                    with st.expander("📅 " + week_title, expanded=True):
                                        st.markdown(
                                            '<div class="post-content" style="color:#cbd5e1;line-height:1.8;">' +
                                            week_content.replace("\n", "<br>") +
                                            '</div>',
                                            unsafe_allow_html=True
                                        )

                        # Download
                        st.download_button(
                            "⬇ Download Full Calendar",
                            cal_result,
                            file_name=cal_business.replace(" ", "_") + "_content_calendar.txt",
                            mime="text/plain"
                        )

                        if cal_email and "@" in cal_email:
                            st.info("📧 Calendar ready to send to " + cal_email + ". Download and forward to your client!")

                    except Exception as e:
                        st.error("Error: " + str(e))

        elif "cal_result" not in st.session_state:
            st.markdown("""
            <div style="height:400px; display:flex; flex-direction:column; align-items:center; justify-content:center; opacity:0.3;">
              <div style="font-size:48px; margin-bottom:16px;">📅</div>
              <div style="color:#fff; font-size:16px; font-family:'Syne',sans-serif;">Your calendar will appear here</div>
              <div style="color:#475569; font-size:13px; margin-top:8px;">Fill in the details and generate your calendar</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:40px; border-top:1px solid rgba(255,255,255,0.05); margin-top:40px;">
  <div style="font-family:'Syne',sans-serif; font-size:18px; font-weight:700; color:#fff; margin-bottom:8px;">
    Kelvin's <span style="background:linear-gradient(135deg,#60a5fa,#818cf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">AI Studio</span>
  </div>
  <div style="color:#334155; font-size:13px;">Powered by Claude AI · Professional Content Generation</div>
</div>
""", unsafe_allow_html=True)
