import spacy
from transformers import pipeline

# Load SpaCy model once
nlp = spacy.load("en_core_web_sm")

def extractive_summary(text, max_sentences=3):
    doc = nlp(text)
    # Sort sentences by length and pick top ones
    sorted_sents = sorted(doc.sents, key=lambda s: -len(s.text))
    summary = ' '.join([sent.text for sent in sorted_sents[:max_sentences]])
    return summary.strip()

def abstractive_summary(text, model_name="facebook/bart-large-cnn"):
    summarizer = pipeline("summarization", model=model_name)
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']
