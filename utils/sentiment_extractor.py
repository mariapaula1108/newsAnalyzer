import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')

def analyze_pdf_sentiment(pdf_content):
    s = SentimentIntensityAnalyzer()
    paragraph_sent = {}
    paragraph_keys = {}

    # Split PDF content into paragraphs
    paragraphs = pdf_content.split('\n')

    for i, paragraph in enumerate(paragraphs):
        if len(paragraph) >= 90:
            sentences = sent_tokenize(paragraph)
            if len(sentences) == 0:
                continue
            sentence_scores = [s.polarity_scores(sentence) for sentence in sentences]

            paragraph_scores = {}

            for key in sentence_scores[0].keys():
                paragraph_scores[key] = sum([score[key] for score in sentence_scores]) / len(sentence_scores)
            
            paragraph_key = f'Paragraph {i+1}'
            paragraph_sent[paragraph_key] = paragraph_scores

            # Extract keywords from the paragraph
            tokens = word_tokenize(paragraph)
            stop_words = set(stopwords.words('english'))
            keywords = [token.lower() for token in tokens if token.lower() not in stop_words and token.isalpha()]

            key_dict = {}
            for keyword in keywords:
                if keyword in key_dict:
                    key_dict[keyword] += 1
                else:
                    key_dict[keyword] = 1

            sorted_keywords = sorted(key_dict.items(), key=lambda x: x[1], reverse=True)

            main_keywords = sorted_keywords[0:4]

            main_k = []
            for pair in main_keywords:
                main_k.append(pair[0])

            paragraph_keys[paragraph_key] = main_k

    return paragraph_sent
