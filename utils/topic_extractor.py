import re
from gensim import corpora, models
from gensim.parsing.preprocessing import STOPWORDS
import nltk
nltk.download('wordnet')
import sklearn
from nltk.stem import WordNetLemmatizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

def tokenize_and_lemmatize(text):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in re.split('\W+', text.lower()) if token not in STOPWORDS and len(token) > 2]


def extract_topics(text, n_topics=3, n_words=5):
    # Preprocess the text
    processed_text = tokenize_and_lemmatize(text)
    
    # Create a CountVectorizer instance
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    
    # Vectorize the preprocessed text
    text_vectorized = vectorizer.fit_transform(processed_text)
    
    # Create an LDA instance
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=5, learning_method='online', learning_offset=50., random_state=0)
    
    # Fit the LDA model
    lda.fit(text_vectorized)
    
    # Extract the top n_words for each topic
    topic_keywords = []
    for topic_idx, topic in enumerate(lda.components_):
        top_keywords = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-n_words - 1:-1]]
        print(top_keywords)
    return top_keywords
