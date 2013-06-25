#!/usr/bin/python3
import sqlite3
import random
from bottle import Bottle, run, template, static_file, request, redirect
from datetime import datetime

version = "3.5"

#Constants
DB_FILE = 'rick.db'
PORT = 80
HOST = '0.0.0.0'

app = Bottle()


#Database functions
def get_quote_from_db(id_no=None):
    '''Retreive a random saying from the DB'''
    with sqlite3.connect(DB_FILE) as db:
        cur = db.cursor()
        if not id_no:
            idx_lst = cur.execute('''SELECT id FROM sayings''').fetchall()
            idx = random.choice(idx_lst)[0]  # extracts a random id
        else:
            idx = id_no
        result = cur.execute(
            '''SELECT saying FROM sayings WHERE id = ?''', (idx,))
        # return the saying AND index so we can generate the static link
        return (result.fetchone()[0].encode("8859", "ignore").decode("utf8","ignore"), idx)


def insert_quote_into_db(text):
    '''Insert Rick's saying into the DB'''
    now_date = str(datetime.now().replace(microsecond=0))  # No microseconds
    val_text = clean_text(text)
    with sqlite3.connect(DB_FILE) as db:
        cur = db.cursor()
        cur.execute("INSERT INTO sayings (date, saying) VALUES (?,?)",
                    (now_date, val_text))
        db.commit()


def alpha_only(text):
    return "".join([c.lower() for c in text if c.isalnum()])


def check_no_dupe(text):
    dupes = []
    with sqlite3.connect(DB_FILE) as db:
        cur = db.cursor()
        results = cur.execute('''SELECT id, saying FROM sayings''').fetchall()
        for row in results:
            quote = alpha_only(row[1])
            dupes.append(hash(quote))
    inst_text = alpha_only(text)
    if hash(inst_text) in dupes:
        return False
    else:
        return True

def query_db(query, db):
    with sqlite3.connect(db) as db:
        cur = db.cursor()
        res = cur.execute(query).fetchall()
        return res


def list_all():
    '''returns all sayings from the table'''
    with sqlite3.connect(DB_FILE) as db:
        cur = db.cursor()
        res = cur.execute("SELECT * FROM sayings").fetchall()
        return res


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


#ROUTES
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
    quote_and_saying = get_quote_from_db()
    rick_quote = quote_and_saying[0]
    quote_no = quote_and_saying[1]
    share_link = "{}quote/{}".format(request.url, str(quote_no))
    return template('rickbot', rickquote=rick_quote,
                    shareme=share_link, shareme2=share_link)


@app.route('/rick.py')
def redirect_to_index():
    '''Redirect old bookmarks'''
    redirect('/')


@app.route('/quote', method="POST")
def put_quote():
    '''route for submitting quote'''
    unval_quote = request.forms.get('saying')
    if len(unval_quote) > 4 and check_no_dupe(unval_quote):  # arbitrary len
        insert_quote_into_db(unval_quote)
        return '''You are being redirected!
        <meta HTTP-EQUIV="REFRESH" content="1; url=/">'''
    else:
        return "That is a duplicate or is too short"


@app.route('/quote/<quoteno>', method="GET")
def display_quote(quoteno):
    '''route for displaying a specific quote'''
    try:
        quote_and_saying = get_quote_from_db(quoteno)
    except:
        redirect('/')
    rick_quote = quote_and_saying[0]
    quote_no = quote_and_saying[1]
    return template('rickbot', rickquote=rick_quote,
                    shareme=request.url, shareme2=request.url)


@app.route('/list', method="GET")
def list_all_quotes():
    '''route for listing all quotes'''
    quotes = list_all()
    req_url = request.urlparts[1]
    return template('list', list_of_quotes=quotes, req_url=req_url)


@app.route('/search/<keyword>')
def search_for(keyword):
    '''simple search route'''
    matches = search(keyword.lower())  # results are lowercase
    return template('search', search_results=matches)


@app.error(404)
def error404(error):
    return "<h1>No matching route found</h1>"


if __name__ == '__main__':
    run(app=app, host=HOST, port=PORT, server='cherrypy', reloader=True)
