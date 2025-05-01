import streamlit as st
import string
import textstat

st.set_page_config(page_title="Smart Text Summarizer", layout="centered")

# Title
st.title("📜 Smarter Text Summarizer")

# Input
input_text = st.text_area("Paste your paragraph here:", height=300)

# Custom stopwords list (basic version)
custom_stopwords = set([
    'the', 'is', 'in', 'and', 'to', 'of', 'a', 'from', 'for', 'on', 'with', 'at', 'by', 'an', 'as', 'be', 'has', 'have', 'are', 'was', 'were', 'or', 'that', 'this', 'but', 'their', 'it'
])

# Simple tokenization
def simple_tokenize(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.lower().split()
    return words

# Summarizer function (improved)
def summarize_text(text, top_n=2):
    words = simple_tokenize(text)
    freq = {}
    for word in words:
        if word not in custom_stopwords:
            freq[word] = freq.get(word, 0) + 1

    sentences = text.split('.')
    sentence_scores = {}
    for sent in sentences:
        sent_words = simple_tokenize(sent)
        for word in sent_words:
            if word in freq:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + freq[word]

    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:top_n]
    return '. '.join([sent.strip() for sent in summarized_sentences if sent.strip() != '']) + '.'

# Keywords extraction (better version)
def extract_keywords(text, top_k=5):
    words = simple_tokenize(text)
    freq = {}
    for word in words:
        if word not in custom_stopwords:
            freq[word] = freq.get(word, 0) + 1
    sorted_keywords = sorted(freq.items(), key=lambda item: item[1], reverse=True)
    return [word for word, count in sorted_keywords[:top_k]]

# Button
if st.button("Summarize"):
    if input_text.strip() == "":
        st.error("Please paste some text to summarize.")
    else:
        with st.spinner('Summarizing...'):
            summary = summarize_text(input_text)
            keywords = extract_keywords(input_text)
            readability = textstat.flesch_reading_ease(input_text)

        # Results
        st.success("✅ Done!")

        st.subheader("📜 Summary:")
        st.write(summary)

        st.subheader("🔑 Top Keywords:")
        st.info(", ".join(keywords))

        st.subheader("📈 Readability Score:")
        if readability >= 70:
            level = "Easy"
        elif readability >= 50:
            level = "Medium"
        else:
            level = "Hard"
        st.write(f"Level: **{level}** (Score: {readability:.2f})")
