import streamlit as st
import pandas as pd
from genai import GenAI
from utils import calculate_engagement, get_engagement_string, compute_keyword_engagement, create_persona_tweet

# Initialize GenAI once
if 'genai' not in st.session_state:
    st.session_state.genai = GenAI(openai_api_key=st.secrets["OPENAI_API_KEY"])

@st.cache_data
def load_data():
    return pd.read_csv('TwExportly_aoc_tweets_2025_01_30.csv')

st.title("Twitter Engagement Analyzer")
page = st.sidebar.radio("Navigation", ["Engagement", "Keywords", "Generate Tweet"])

df = load_data()
df = calculate_engagement(df)

if page == "Engagement":
    st.header("Engagement Analysis")
    st.dataframe(df[['text', 'engagement']])
    
    if st.button("Analyze Patterns"):
        analysis = get_engagement_string(df, st.session_state.genai)
        st.subheader("Engagement Insights")
        st.write(analysis)

elif page == "Keywords":
    st.header("Keyword Impact")
    keywords = st.text_input("Enter comma-separated keywords:")
    
    if st.button("Analyze Keywords") and keywords:
        keywords_df = compute_keyword_engagement(df, keywords)
        if not keywords_df.empty:
            st.dataframe(keywords_df.sort_values('pvalue_bh'))
        else:
            st.warning("No valid keywords to analyze")

elif page == "Generate Tweet":
    st.header("Tweet Generator")
    topic = st.text_input("Enter tweet topic:")
    
    if st.button("Generate") and topic:
        engagement_analysis = get_engagement_string(df, st.session_state.genai)
        tweet_text = create_persona_tweet(topic, df, engagement_analysis, st.session_state.genai)
        st.markdown(st.session_state.genai.display_tweet(tweet_text), unsafe_allow_html=True)

