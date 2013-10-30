import unittest
import urllib.request
import re

from unittest.mock import Mock, patch

from rick import *
from models import *
from bottle import HTTPError

import initdb

class TestRickBot(unittest.TestCase):
	
	@classmethod
	def setUp(self):
		initdb.main()


	@classmethod
	def tearDown(self):
		pass


	def test_clean_text(self):
		
		bad_text = "abc123 熊貓 \uFFFD"
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
		quotes = [q.text for q in Quote.select().join(Person).where(Person.name == "Rick")]
		self.assertIn(rick_quote, quotes)

		response = index_name("Joel")
		QUOTE_RE = r"<h2>(.*?)</h2>"
		joel_quote = re.search(QUOTE_RE, response).group(1)
		quotes = [q.text for q in Quote.select().join(Person).where(Person.name == "Joel")]
		self.assertIn(joel_quote, quotes)

	def test_index_name_fail_on_bad_input(self):
		with self.assertRaises(HTTPError):
			 index_name("earg")


if __name__ == '__main__':
	unittest.main()