import streamlit as st
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
key = os.getenv("AZURE_LANGUAGE_KEY")

# Initialize Azure client
client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Streamlit UI
st.set_page_config(page_title="Sentiment Analysis App", layout="wide")
st.title("🔍 Azure Sentiment Analysis App")

st.write("Enter multiple reviews (one per line):")

user_input = st.text_area("Reviews", height=200, placeholder="Type or paste reviews here...")

if st.button("Analyze Sentiment"):
    if not user_input.strip():
        st.error("Please enter at least one review.")
    else:
        # Convert input text into list of reviews (one per line)
        reviews = [line.strip() for line in user_input.split("\n") if line.strip()]

        st.info(f"Analyzing {len(reviews)} reviews...")

        # Call Azure
        response = client.analyze_sentiment(documents=reviews)

        # Counters
        positive = neutral = negative = 0

        st.subheader("📊 Sentiment Results:")

        for i, doc in enumerate(response):
            if doc.sentiment == "positive":
                positive += 1
                color = "green"
            elif doc.sentiment == "neutral":
                neutral += 1
                color = "gray"
            else:
                negative += 1
                color = "red"

            st.markdown(
                f"""
                <div style="padding:10px; border-radius:5px; background-color:{color}; color:white; margin-bottom:10px;">
                    <strong>Review {i+1}:</strong> {reviews[i]}  
                    <br>
                    <strong>Sentiment:</strong> {doc.sentiment.upper()}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Summary Section
        st.subheader("✔ Summary")
        st.write(f"**Positive:** {positive}")
        st.write(f"**Neutral:** {neutral}")
        st.write(f"**Negative:** {negative}")

        # Alert section for negative reviews
        if negative > 0:
            st.error("⚠️ Warning: Negative Reviews Found!")
