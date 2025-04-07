import pandas as pd
from scipy.stats import ttest_ind
import statsmodels.stats.multitest as multitest

# Function to calculate engagement
def calculate_engagement(df):
    df['engagement'] = df['favorite_count'] / df['view_count']
    return df

# Function to get engagement analysis string using AI
def get_engagement_string(df, generate_text):
    prompt = "Analyze the following tweets and their engagement rates. Provide insights into what drives engagement:\n\n"
    for _, row in df.iterrows():
        prompt += f"Tweet: {row['text']}\nEngagement: {row['engagement']:.4f}\n\n"
    return generate_text(prompt)

# Function to compute keyword engagement analysis
def compute_keyword_engagement(df, keyword_string):
    keywords = keyword_string.split(',')
    results = []

    for keyword in keywords:
        keyword = keyword.strip()
        df['contains_keyword'] = df['text'].str.contains(keyword, case=False)

        # Engagement for tweets with and without the keyword
        engagement_true = df[df['contains_keyword']]['engagement']
        engagement_false = df[~df['contains_keyword']]['engagement']

        # Perform t-test
        t_stat, p_value = ttest_ind(engagement_true, engagement_false, nan_policy='omit')

        # Append results
        results.append({
            'keyword': keyword,
            'pvalue': p_value,
            'engagement_true': engagement_true.mean(),
            'engagement_false': engagement_false.mean()
        })

    # Create DataFrame and apply Benjamini-Hochberg correction
    df_keywords = pd.DataFrame(results)
    corrected_pvalues = multitest.multipletests(df_keywords['pvalue'], method='fdr_bh')[1]
    df_keywords['pvalue_bh'] = corrected_pvalues

    return df_keywords

# Function to create a persona tweet
def create_persona_tweet(topic, df, engagement_analysis_string, generate_text):
    prompt = f"Create a tweet about '{topic}' in the voice of the user. Use the following insights about their tweets:\n\n"
    prompt += f"{engagement_analysis_string}\n\n"
    prompt += "Here are some of their previous tweets:\n"
    for _, row in df.iterrows():
        prompt += f"Tweet: {row['text']}\nEngagement: {row['engagement']:.4f}\n\n"

    tweet_text = generate_text(prompt)
    
    # Format tweet as HTML for display
    tweet_html = f"<div style='border:1px solid #ccc; padding:10px; border-radius:5px;'>{tweet_text}</div>"
    return tweet_html
