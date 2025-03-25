import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download("punkt")
nltk.download("stopwords")

def preprocess_text(text):
    stop_words = set(stopwords.words("english"))
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    return sentences, words