import pandas as pd
import openai

openai.api_key = "sk-..."  # replace with your key

def analyze_feedback(feedback_text):
    prompt = f"""
You are an AI HR assistant. Analyze the employee feedback.

Feedback: "{feedback_text}"

Return:
- Sentiment: Positive / Neutral / Negative
- Attrition Risk: Yes / No / Maybe
- Reason:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response['choices'][0]['message']['content']
