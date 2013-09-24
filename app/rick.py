#!/usr/bin/python3
import configparser
import logging
import sqlite3
from datetime import datetime

# Bottle.py imports
from bottle import Bottle, run, template, static_file, request, redirect


version = "3.5.9"

# Constants
DB_FILE = 'rick.db'

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


# Database functions
def get_quote_from_db(id_no=None):
    '''Retreive a random saying from the DB'''
    if not id_no:
        result, idx, name = query_db(
            "SELECT saying, id, name FROM sayings ORDER BY RANDOM() LIMIT 1", DB_FILE)[0]
    else:
        result, idx, name = query_db(
            "SELECT saying, id, name FROM sayings WHERE id = ?",
            DB_FILE, params=(id_no,))[0]
        # return the saying, index, and name quote's source so we can generate the static link
    return (result.encode("8859", "ignore").decode("utf8", "ignore"), idx, name)


def insert_quote_into_db(text,name):
    '''Insert the saying into the DB'''
    now_date = str(datetime.now().replace(microsecond=0))  # No microseconds
    val_text = clean_text(text)
    source_name = clean_text(name)
    logging.info("INSERTING {} into DB".format(val_text))
    insert_db("INSERT INTO sayings (date, saying, name) VALUES (?,?,?)",
              (now_date, val_text, source_name), DB_FILE)


def alpha_only(text):
    '''Strips a string down to no whitespace or punctuation'''
    return "".join(c.lower() for c in text if c.isalnum())


def check_no_dupe(text):
    '''Uses built in hasing to detect duplicates'''
    dupes = set()
    results = query_db("SELECT saying FROM sayings", DB_FILE)
    for row in results:
        quote = alpha_only(row[0])
        dupes.add(hash(quote))
    inst_text = alpha_only(text)
    if hash(inst_text) in dupes:
        logging.error("Quote '{}' is a duplicate".format(text))
        return False
    else:
        return True


def query_db(query, db, params=None):
    '''Generic db function. Send query with optional kwonly params'''
    with sqlite3.connect(db) as db:
        cur = db.cursor()
        if params:
            logging.info("Sending Query: {} with {}".format(query, params))
            res = cur.execute(query, params).fetchall()
        else:
            logging.info("Sending Query: {}".format(query))
            res = cur.execute(query).fetchall()
        return res


def insert_db(query, vals, db):
    '''Generic db function. Insert query with vals'''
    with sqlite3.connect(db) as db:
        cur = db.cursor()
        try:
            logging.info("Inserting: {} --> {}".format(query, vals))
            cur.execute(query, vals)
            db.commit()
        except Exception as e:
            logging.error("Something went wrong: {}".format(str(e)))


def list_all():
    '''returns all sayings from the table'''
    return query_db("SELECT * FROM sayings", DB_FILE)


def clean_text(text):
    '''cleans text from common messes'''
    if text.lstrip().startswith('...'):  # kuldge for Pip
        return text.lstrip(" \t") \
                   .replace("\uFFFD", "'")

    else:
        return text.lstrip(" .\t") \
                   .replace("\uFFFD", "'")


def search(keyword):
    '''simple search `keyword` in string test'''
    all_quotes = list_all()
    search_results = [row for row in all_quotes
                      if keyword in row[2].lower()]
    return search_results


# ROUTES
@app.route('/static/<filename:path>')
def send_static(filename):
    '''define routes for static files'''
    return static_file(filename, root='static')


@app.route('/favicon.ico', method='GET')
def get_favicon():
    '''route for favicon'''
    return static_file('favicon.ico', root='static')


@app.route('/')
def index():
    '''Returns the index page with a randomly chosen RickQuote'''
    logging.info("{} requested a random quote".format(request.remote_addr))
    quote, quote_no, name = get_quote_from_db()
    share_link = "{}quote/{}".format(request.url, str(quote_no))
    return template('rickbot', rickquote=quote, shareme=share_link, persons=["Rick", "Tyler", "Evan"])


@app.route('/rick.py')
def redirect_to_index():
    '''Redirect old bookmarks'''
    redirect('/')


@app.route('/quote', method="POST")
def put_quote():
    '''route for submitting quote'''
    logging.info("{} is submitting a quote".format(request.remote_addr))
    unval_quote = request.forms.get('saying')
    name = str(request.forms.get('person'))
    if len(unval_quote) > 4 and check_no_dupe(unval_quote):  # arbitrary len
        insert_quote_into_db(unval_quote, name)
        return '''You are being redirected!
        <meta HTTP-EQUIV="REFRESH" content="1; url=/">'''
    else:
        return "That is a duplicate or is too short"


@app.route('/quote/<quoteno>', method="GET")
def display_quote(quoteno):
    '''route for displaying a specific quote'''
    logging.info("{} is asking for a specific quote".format(
        request.remote_addr))
    try:
        quote = get_quote_from_db(quoteno)[0]
    except:
        redirect('/')  # Silently fail for better experience
    return template('rickbot', rickquote=quote, shareme=request.url, persons=["Rick", "Evan", "Tyler"])


@app.route('/list', method="GET")
def list_all_quotes():
    '''route for listing all quotes'''
    quotes = list_all()
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
    matches = search(keyword.lower())  # results are lowercase
    return template('search', search_results=matches, searchbox=False)


@app.error(404)
def error404(error):
    '''Custom 404 page'''
    return "<h1>No matching route found</h1>"


if __name__ == '__main__':
    run(app=app, **ENVIRON)
