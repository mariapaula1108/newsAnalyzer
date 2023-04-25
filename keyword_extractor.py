from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

def extract_keywords(file_content):
    tokens = word_tokenize(file_content)
    stop_words = set(stopwords.words('english'))
    keywords = [token.lower() for token in tokens if token.lower() not in stop_words and token.isalpha()]
    keyword_count = Counter(keywords)
    top_keywords = [keyword for keyword, count in keyword_count.most_common(5)]
    return top_keywords
