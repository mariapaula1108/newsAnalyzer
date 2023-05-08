from nltk.tokenize import sent_tokenize

def sentences_keyword(paragraph, keyword):
    sentences = sent_tokenize(paragraph)
    keyword_sentences = [sentence for sentence in sentences if keyword.lower() in sentence.lower()]
    return keyword_sentences
