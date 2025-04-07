import streamlit as st
import pandas as pd
from genai import generate_text, display_tweet
from utils import calculate_engagement, get_engagement_string, compute_keyword_engagement, create_persona_tweet

# Load data (replace 'tweets.csv' with your actual file)
@st.cache_data
def load_data():
    return pd.read_csv('tweets.csv')

# Main app
st.title("Twitter Engagement Analyzer")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Engagement Analysis", "Keyword Analysis", "Persona Tweet Generator"])

# Load data
df = load_data()

if page == "Engagement Analysis":
    st.header("Engagement Analysis")
    
    # Calculate engagement and display data
    df = calculate_engagement(df)
    st.dataframe(df[['text', 'favorite_count', 'view_count', 'engagement']])
    
    # Generate engagement analysis string using AI
    if st.button("Analyze Engagement"):
        analysis_string = get_engagement_string(df, generate_text)
        st.write("### Engagement Analysis:")
        st.write(analysis_string)

elif page == "Keyword Analysis":
    st.header("Keyword Engagement Analysis")
    
    # Input keywords from user
    keyword_string = st.text_input("Enter keywords (comma-separated):")
    
    if st.button("Analyze Keywords"):
        if keyword_string:
            df_keywords = compute_keyword_engagement(df, keyword_string)
            st.write("### Keyword Engagement Results:")
            st.dataframe(df_keywords)
        else:
            st.warning("Please enter at least one keyword.")

elif page == "Persona Tweet Generator":
    st.header("Persona Tweet Generator")
    
    # Input topic from user
    topic = st.text_input("Enter a topic:")
    
    if st.button("Generate Tweet"):
        if topic:
            # Generate persona tweet using AI
            engagement_analysis_string = get_engagement_string(df, generate_text)
            tweet_html = create_persona_tweet(topic, df, engagement_analysis_string, generate_text)
            
            # Display generated tweet
            display_tweet(tweet_html)
        else:
            st.warning("Please enter a topic.")
