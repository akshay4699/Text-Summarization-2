import streamlit as st
from summarizer import extractive_summary, abstractive_summary

st.set_page_config(page_title="Text Summarizer", layout="wide")

st.title("📝 Text Summarization App")
st.write("Choose between Extractive or Abstractive summarization methods.")

# Text input
text_input = st.text_area("Paste your text below:", height=300)

# Method choice
method = st.radio("Choose summarization type:", ["Extractive", "Abstractive"])

# Button
if st.button("Summarize"):
    if not text_input.strip():
        st.warning("Please enter some text to summarize.")
    else:
        with st.spinner("Generating summary..."):
            if method == "Extractive":
                summary = extractive_summary(text_input)
            else:
                summary = abstractive_summary(text_input)
        st.subheader("Summary:")
        st.success(summary)
