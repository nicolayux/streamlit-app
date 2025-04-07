import os
import openai
import re

class GenAI:
    def __init__(self, openai_api_key):
        self.client = openai.Client(api_key=openai_api_key)
        
    def generate_text(self, prompt, instructions='You are a helpful AI assistant', model="gpt-4"):
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content

    def display_tweet(self, text):
        return f'''<div style="border:1px solid #e1e8ed; border-radius:12px; padding:15px; margin:10px 0; font-family:system-ui;">
            <div style="font-weight:bold; margin-bottom:8px;">AI Persona</div>
            <div>{text}</div>
        </div>'''

