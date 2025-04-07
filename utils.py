import pandas as pd
from scipy.stats import ttest_ind
import statsmodels.stats.multitest as multitest

def calculate_engagement(df):
    df['engagement'] = df['favorite_count'] / df['view_count']
    return df

def get_engagement_string(df, genai_instance):
    prompt = "Analyze these tweets and engagement rates (favorites/views):\n"
    for _, row in df.iterrows():
        prompt += f"- {row['text']} (Engagement: {row['engagement']:.4f})\n"
    return genai_instance.generate_text(prompt)

def compute_keyword_engagement(df, keyword_string):
    keywords = [k.strip() for k in keyword_string.split(',')]
    results = []
    
    for keyword in keywords:
        contains = df['text'].str.contains(keyword, case=False)
        eng_true = df[contains]['engagement'].dropna()
        eng_false = df[~contains]['engagement'].dropna()
        
        if eng_true.empty or eng_false.empty:
            continue
            
        t_stat, p_val = ttest_ind(eng_true, eng_false)
        results.append({
            'keyword': keyword,
            'pvalue': p_val,
            'engagement_true': eng_true.mean(),
            'engagement_false': eng_false.mean()
        })
    
    df_keywords = pd.DataFrame(results)
    if not df_keywords.empty:
        df_keywords['pvalue_bh'] = multitest.multipletests(df_keywords['pvalue'], method='fdr_bh')[1]
    return df_keywords

def create_persona_tweet(topic, df, engagement_analysis, genai_instance):
    prompt = f"Create a tweet about {topic} using this engagement analysis:\n{engagement_analysis}\n\nExample tweets:\n"
    for _, row in df.sample(3).iterrows():
        prompt += f"- {row['text']}\n"
    return genai_instance.generate_text(prompt)
