import pandas as pd
from src.feedback_analyzer import analyze_feedback

df = pd.read_csv("data/feedback/feedback.csv")

df["analysis"] = df["feedback"].apply(analyze_feedback)
df.to_csv("data/feedback/feedback_analysis_output.csv", index=False)

print(df.head())
