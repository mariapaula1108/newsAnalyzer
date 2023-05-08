import unittest
from utils.keyword_extractor import extract_keywords
from utils.sentiment_extractor import analyze_pdf_sentiment
from utils.topic_extractor import extract_topics
from utils.extract_entities import extract_entities
from utils.search_web import search_web
from utils.search_files import search_files
from urllib.parse import urlparse



class TestKeywordExtractor(unittest.TestCase):
    def test_extract_keywords(self):
        text = "The quick brown fox jumps over the lazy dog."
        keywords = extract_keywords(text)
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)


class TestSentimentExtractor(unittest.TestCase):
    def test_search_web(self):
        query = "artificial intelligence"
        urls = search_web(query)
        self.assertIsInstance(urls, str)
        url_list = urls.split('\n')
        for url in url_list:
            parsed_url = urlparse(url)
            self.assertTrue(parsed_url.scheme in ('http', 'https'))
            self.assertTrue(parsed_url.netloc)


class TestEntityExtractor(unittest.TestCase):

    def test_extract_entities(self):
        text = "Barack Obama was the 44th president of the United States."
        entities = extract_entities(text)
        self.assertIsInstance(entities, dict)
        self.assertIn('PERSON', entities)
        self.assertIn('GPE', entities)
        self.assertIn('ORG', entities)
        self.assertIn('ADDRESS', entities)
        self.assertIn('Barack Obama', entities['PERSON'])
        

class TestSearchFiles(unittest.TestCase):

    def test_search_files(self):
        # NOTE: This test assumes that you have a predefined email and search query in your database
        # You need to replace 'test@email.com' with a valid email and 'search_query' with a valid query
        email = 'test@email.com'
        search_query = 'search_query'
        search_results = search_files(email, search_query)
        self.assertIsInstance(search_results, list)


if __name__ == '__main__':
    unittest.main()
