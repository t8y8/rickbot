import unittest
from webtest import TestApp, AppError
import urllib.request
import re

from rick import *

from bottle import HTTPError, HTTPResponse

import initdb


class TestRickBot(unittest.TestCase):

    @classmethod
    def setUp(self):
        initdb.main()

    @classmethod
    def tearDown(self):
        pass

    def test_clean_text(self):

        bad_text = " \t abc123 熊貓 \uFFFD"
        cleaned = clean_text(bad_text)

        self.assertEqual(cleaned, "abc123 熊貓 '")

    def test_get_person(self):

        rick = Person.get(Person.name == "Rick")
        joel = Person.get(Person.name == "Joel")
        self.assertEqual(rick.name, "Rick")
        self.assertEqual(joel.name, "Joel")

    def test_search(self):
        keyword = "America"
        results = search(keyword)
        self.assertIn(keyword, results[0].text)

        keyword = "fox"
        results = search(keyword)
        self.assertIn(keyword, results[0].text)

    def test_quote_on_index_page(self):
        response = index()
        quotes = Quote.select()
        self.assertTrue(any([q.text in response for q in quotes]))

    def test_static_link_valid(self):
        response = index()
        LINK_RE = r"<a[^>]*>([^<]+)</a>"
        url = re.findall(LINK_RE, response)[0]
        self.assertTrue(url)

    def test_index_name(self):
        response = index_name("Rick")
        QUOTE_RE = r"<h2>(.*?)</h2>"
        rick_quote = re.search(QUOTE_RE, response).group(1)
        quotes = [q.text for q in Quote.select().join(
            Person).where(Person.name == "Rick")]
        self.assertIn(rick_quote, quotes)

        response = index_name("Joel")
        QUOTE_RE = r"<h2>(.*?)</h2>"
        joel_quote = re.search(QUOTE_RE, response).group(1)
        quotes = [q.text for q in Quote.select().join(
            Person).where(Person.name == "Joel")]
        self.assertIn(joel_quote, quotes)

    def test_index_name_fail_on_bad_input(self):
        with self.assertRaises(HTTPError):
            index_name("earg")

    def test_insert_quote(self):
        test_app = TestApp(app)
        resp = test_app.post(
            '/quote', {'person': "Joel", "saying": "This is the best post ever 我愛你"})
        self.assertEqual(resp.status, "200 OK")

    def test_insert_quote_and_check(self):
        test_app = TestApp(app)
        test_quote = "This is a good quote with unicode 我愛你"
        resp = test_app.post(
            '/quote', {'person': "Rick", "saying": test_quote})
        quotes = [q.text for q in Quote.select()]
        self.assertTrue(test_quote in quotes)

    def test_display_quote_success(self):
        quote = Quote.get(Quote.id == 3).text
        assert quote in display_quote(3)

    def test_display_quote_failure(self):
        with self.assertRaises(HTTPResponse):
            display_quote(77)

    def test_search_page(self):
        test_app = TestApp(app)
        keyword = "America"
        resp = test_app.get('/search/America')
        self.assertEqual(resp.status, "200 OK")
        self.assertIn(keyword, resp)

    def test_list_all(self):
        # Regexes
        PERSON_RE = r"<h2>(.*?)</h2>"
        LIST_QUOTE_RE = r"<a.+/quote/\d+.*>"
        
        #Test Application
        test_app = TestApp(app)
        
        #Expecteds
        person_count = sum([1 for i in Person.select()])
        quote_count = sum([1 for i in Quote.select()])
        
        #Do it
        resp = test_app.get('/list')
        response_person_count = len(re.findall(PERSON_RE, str(resp)))
        response_quote_count = len(re.findall(LIST_QUOTE_RE, str(resp)))
        
        #Assertions
        self.assertEqual(person_count, response_person_count)
        self.assertEqual(quote_count, response_quote_count)

if __name__ == '__main__':
    unittest.main()
