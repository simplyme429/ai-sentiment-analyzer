import streamlit as st
from textblob import TextBlob
import pandas as pd

st.set_page_config(page_title="AI Sentiment Analyzer", layout="wide")

st.title("🤖 AI Sentiment Analysis Web App")
st.markdown("### Analyze reviews, comments, or social media text")

# Single text analysis
st.subheader("Single Text Analysis")
text = st.text_area("Enter your text here:", height=150, placeholder="Type a product review or tweet...")

if st.button("Analyze Sentiment"):
    if text.strip():
        with st.spinner("Analyzing..."):
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.05:
                st.success(f"✅ Positive Sentiment (Score: {polarity:.2f})")
            elif polarity < -0.05:
                st.error(f"❌ Negative Sentiment (Score: {polarity:.2f})")
            else:
                st.info(f"😐 Neutral Sentiment (Score: {polarity:.2f})")
    else:
        st.warning("Please enter some text!")

# Batch analysis
st.subheader("📊 Batch Analysis - Upload CSV")
uploaded_file = st.file_uploader("Upload CSV file (must have 'text' column)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'text' in df.columns:
        with st.spinner("Analyzing all rows..."):
            results = []
            for _, row in df.iterrows():
                blob = TextBlob(str(row['text']))
                polarity = blob.sentiment.polarity
                sentiment = "Positive" if polarity > 0.05 else "Negative" if polarity < -0.05 else "Neutral"
                results.append({
                    "Original Text": row['text'],
                    "Sentiment": sentiment,
                    "Score": round(polarity, 4)
                })
            result_df = pd.DataFrame(results)
            
            st.success("✅ Analysis Complete!")
            st.dataframe(result_df)
            
            # Simple chart
            st.bar_chart(result_df["Sentiment"].value_counts())
            
            # Download
            csv = result_df.to_csv(index=False)
            st.download_button("📥 Download Results", csv, "sentiment_results.csv")
    else:
        st.error("CSV must have a column named 'text'")

st.caption("Project 1 - Simple AI Sentiment Analyzer | Built for Portfolio")