import re
import spacy
from collections import Counter

nlp = spacy.load('en_core_web_sm')

def clean_text(text):
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    return text

def extract_keywords(text, num_keywords=5):
    cleaned_text = clean_text(text)
    doc = nlp(cleaned_text)
    words = [token.text for token in doc if token.is_stop != True and token.is_punct != True]
    word_freq = Counter(words)
    common_words = word_freq.most_common(num_keywords)
    keyword_list = [word[0] for word in common_words]
    print(keyword_list)
    return keyword_list

