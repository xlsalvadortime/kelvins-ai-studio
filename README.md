# Kelvin's AI Studio

Professional AI-powered social media content generator built with Claude AI.

## Features
- Single post generator (up to 10 posts per platform)
- Full month content calendar (4 weeks)
- Brand color customization
- Copy to clipboard for each post
- Email delivery notification
- Download as text file
- Supports Instagram, Twitter/X, Facebook, LinkedIn

## Deploy to Streamlit Cloud (Free & Permanent)

### Step 1 — Upload to GitHub
1. Go to github.com and create a free account
2. Click "New Repository"
3. Name it: kelvins-ai-studio
4. Upload all files from this folder

### Step 2 — Deploy on Streamlit Cloud
1. Go to streamlit.io and sign up free
2. Click "New App"
3. Connect your GitHub account
4. Select your repository: kelvins-ai-studio
5. Main file: app.py
6. Click Deploy!

### Step 3 — Add Your API Key
1. In Streamlit Cloud, go to App Settings
2. Click "Secrets"
3. Add: ANTHROPIC_API_KEY = "your-sk-ant-key-here"
4. Save — your app is now live 24/7!

## Your permanent URL will be:
https://kelvins-ai-studio.streamlit.app

## Local Testing
```
pip install anthropic streamlit
streamlit run app.py
```
