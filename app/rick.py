#!/usr/bin/python3
import configparser
import logging
from models import Person, Quote
from peewee import fn
from datetime import datetime

# Bottle.py imports
from bottle import Bottle, run, template, static_file, request, redirect


__version__ = "3.6"


# Logging
logging.basicConfig(filename="rickbot.log", level=logging.INFO,
                    format='%(levelname)s - [%(asctime)s] %(message)s')

config = configparser.ConfigParser()
config.read('config.ini')

try:
    ENVIRON = config['RICKBOT']
    logging.info("Loaded config.ini")
except:
    ENVIRON = {'host': "127.0.0.1", 'port':
               8080, 'server': 'wsgiref', 'debug': 'true', 'reloader': 'true'}
    logging.info("Loaded default config dict")

# Create the explicit application object
app = Bottle()


def clean_text(text):
    '''cleans text from common messes'''  # TODO: Replace with regex
    cleaned = text.lstrip(" \t")
    cleaned = cleaned.replace("\uFFFD", "'")
    cleaned = cleaned.encode("8859", "ignore").decode("utf8", "ignore")
    return cleaned


def search(keyword):
    '''simple search `keyword` in string test'''
    search_query = Quote.select().where(Quote.text ** "%{}%".format(keyword))
    search_results = [quote for quote in search_query]
    return search_results


# ROUTES
@app.route('/static/<filename:path>')
def send_static(filename):
    '''define routes for static files'''
    return static_file(filename, root='static')


@app.route('/favicon.ico', method='GET')
def get_favicon():
    '''route for favicon'''
    return static_file('favicon.ico', root='')


@app.route('/')
def index():
    '''Returns the index page with a randomly chosen RickQuote'''
    logging.info("{} requested a random quote".format(request.remote_addr))
    quote = Quote.select().order_by(fn.random()).limit(1).get()
    logging.info("requested quote no {}".format(quote.id))
    share_link = "{}quote/{}".format(request.url, str(quote.id))
    persons = [row.name for row in Person.select()]
    return template('rickbot',
                    rickquote=quote.text,
                    shareme=share_link,
                    persons=persons,
                    name=quote.person_id.name)


@app.route('/quote', method="POST")
def insert_quote():
    '''route for submitting quote'''
    unval_quote = clean_text(request.forms.get('saying'))
    name = str(request.forms.get('person'))
    person = Person.get(Person.name == name)
    try:
        Quote.create(person_id=person, text=unval_quote,
                     entered_at=datetime.now()).save()
        return "IT WORKED!"
    except Exception as e:
        return "Shit broke: {}".format(e)


@app.route('/quote/<quoteno>', method="GET")
def display_quote(quoteno):
    '''route for displaying a specific quote'''
    try:
        quote = Quote.select().where(Quote.id == quoteno).get()
    except:
        redirect('/')  # Silently fail for better experience
    persons = [row.name for row in Person.select()]
    return template('rickbot',
                    rickquote=quote.text,
                    shareme=request.url,
                    persons=persons,
                    name=quote.person_id.name)


@app.route('/list', method="GET")
def list_all_quotes():
    '''route for listing all quotes'''
    quotes = [i for i in Quote.select()]
    req_url = request.urlparts[1]  # Send hostname not full url
    return template('list', list_of_quotes=quotes, req_url=req_url)


@app.route('/search')
def search_page():
    '''presents user with a search box and then redirects to serach api'''
    keyword = request.query.get("keyword")
    if keyword:
        redirect('/search/' + keyword)
    return template('search', search_results=None, searchbox=True)


@app.route('/search/<keyword>')
def search_for(keyword=None):
    '''route for actually executing a search'''
    matches = search(keyword)  # results are lowercase
    return template('search', search_results=matches, searchbox=False)


@app.error(404)
def error404(error):
    '''Custom 404 page'''
    return "<h1>No matching route found</h1>"


if __name__ == '__main__':
    run(app=app, **ENVIRON)
