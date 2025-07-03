import os
import streamlit as st
import nltk
from io import StringIO

# Setup NLTK data path
nltk_data_path = os.path.expanduser("~/.nltk_data")
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)

# Download 'punkt' if not already
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", download_dir=nltk_data_path, quiet=True)

# ✅ Monkey patch: create dummy 'punkt_tab' path if sumy tries to call it
try:
    punkt_path = nltk.data.find("tokenizers/punkt")
    fake_punkt_tab = os.path.join(os.path.dirname(punkt_path), "punkt_tab")
    os.makedirs(fake_punkt_tab, exist_ok=True)
except Exception as e:
    st.error(f"Monkey patching for punkt_tab failed: {e}")

    
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer

# Function to summarize text
def summarize_text(text, num_sentences=3, method="lsa"):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    if method == "lsa":
        summarizer = LsaSummarizer()
    elif method == "lexrank":
        summarizer = LexRankSummarizer()
    elif method == "luhn":
        summarizer = LuhnSummarizer()
    else:
        return "Invalid method selected."

    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

# Word/character stats
def get_text_stats(text):
    words = len(text.split())
    characters = len(text)
    return words, characters

# Streamlit UI
st.set_page_config(page_title="🧠 Text Summarizer", layout="centered")
st.title("🧠 Text Summarizer App (Sumy-based)")

# Input method: text or file
input_method = st.radio("Choose input method:", ["Type text", "Upload .txt file"])

text = ""
if input_method == "Type text":
    text = st.text_area("📄 Enter your text here:", height=300)
else:
    uploaded_file = st.file_uploader("📁 Upload a .txt file", type="txt")
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        text = stringio.read()

method = st.selectbox("🧪 Choose summarization algorithm:", ["lsa", "lexrank", "luhn"])
num_sentences = st.slider("✂️ Number of summary sentences:", min_value=1, max_value=10, value=3)

# Suggestion based on text length
if text:
    word_count = len(text.split())
    if word_count < 150 and method != "luhn":
        st.warning("ℹ️ Tip: For short texts, 'Luhn' may give better summaries.")
    elif word_count > 500 and method != "lexrank":
        st.info("💡 Tip: For long documents, 'LexRank' might produce more relevant summaries.")

# Summarize
if st.button("🚀 Summarize"):
    if not text.strip():
        st.warning("Please enter or upload some text first.")
    else:
        summary = summarize_text(text, num_sentences, method)

        # Text stats
        orig_words, orig_chars = get_text_stats(text)
        summ_words, summ_chars = get_text_stats(summary)

        # Display results
        st.subheader("📊 Original Text Stats")
        st.info(f"Words: {orig_words} | Characters: {orig_chars}")

        st.subheader("📝 Summary")
        st.success(summary)

        st.subheader("📊 Summary Stats")
        st.info(f"Words: {summ_words} | Characters: {summ_chars}")

        # Download option
        st.download_button(
            label="📥 Download Summary as .txt",
            data=summary,
            file_name="summary.txt",
            mime="text/plain"
        )
