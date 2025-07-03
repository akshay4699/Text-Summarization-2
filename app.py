import streamlit as st
import nltk
nltk.download('punkt')
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

text = st.text_area("📄 Enter your text here:", height=300)

method = st.selectbox("🧪 Choose summarization algorithm:", ["lsa", "lexrank", "luhn"])
num_sentences = st.slider("✂️ Number of summary sentences:", min_value=1, max_value=10, value=3)

# Suggestion based on text length
if len(text.split()) < 150 and method != "luhn":
    st.warning("ℹ️ Tip: For short texts, 'Luhn' may give better summaries.")
elif len(text.split()) > 500 and method != "lexrank":
    st.info("💡 Tip: For long documents, 'LexRank' may produce more relevant summaries.")

if st.button("🚀 Summarize"):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        summary = summarize_text(text, num_sentences, method)

        orig_words, orig_chars = get_text_stats(text)
        summ_words, summ_chars = get_text_stats(summary)

        st.subheader("📊 Original Text Stats")
        st.info(f"Words: {orig_words} | Characters: {orig_chars}")

        st.subheader("📝 Summary")
        st.success(summary)

        st.subheader("📊 Summary Stats")
        st.info(f"Words: {summ_words} | Characters: {summ_chars}")
