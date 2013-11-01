import configparser
import logging
from models import Person, Quote
from peewee import fn
from datetime import datetime

# Bottle.py imports
from bottle import Bottle, run, template, static_file, request, redirect, abort


__version__ = "3.6.4"

# Logging
logging.basicConfig(filename="rickbot.log", level=logging.INFO,
                    format='%(levelname)s - [%(asctime)s] %(message)s')

config = configparser.ConfigParser()
config.read('config.ini')


try:
    ENVIRON = config['RICKBOT']
    SECRET_KEY = config['SECRET']['PASS']
    logging.info("Loaded config.ini")
except KeyError as e:
    ENVIRON = {
        'host': "127.0.0.1",
        'port': 8080,
        'server': 'wsgiref',
        'debug': 'true',
        'reloader': 'true',
    }
    logging.info("Loaded default config dict")
    SECRET_KEY = "America!!"

# Create the explicit application object
app = Bottle()


def clean_text(text):
    '''
    cleans text by ensuring UTF-8 and stripping some bad characters
    '''
    cleaned = text.lstrip(" \t")\
        .encode("latin1", "ignore")\
        .decode("utf8", "ignore")\
        .replace("\uFFFD", "'")
    return cleaned

def search(keyword):
    '''
    simple search keyword in string test
    '''
    # ** is LIKE in peewee
    search_query = Quote.select().where(Quote.text ** "%{}%".format(keyword))
    search_results = [quote for quote in search_query]
    return search_results


# ROUTES
@app.route('/static/<filename:path>')
def send_static(filename):
    '''
    define routes for static files
    '''
    return static_file(filename, root='static')


@app.route('/favicon.ico', method='GET')
def get_favicon():
    '''
    route for favicon
    '''
    return static_file('favicon.ico', root='')


@app.route('/')
def index():
    '''
    Returns the index page with a randomly chosen RickQuote
    '''
    quote = Quote.select().order_by(fn.random()).get()
    logging.info("%s requested a random quote: %s",
                 request.remote_addr, quote.id)
    persons = [row.name for row in Person.select()]
    return template('rickbot',
                    rickquote=quote,
                    shareme=request.urlparts,
                    persons=persons,
                    name=quote.person_id.name)


@app.route('/quote/<name:re:[a-zA-Z]+>')
def index_name(name):
    '''
    Returns the index page with a randomly chosen RickQuote
    '''
    persons = [row.name for row in Person.select()]

    if name.title() not in persons:
        abort(code=404, text="That person has no quotes saved")

    quote = Quote.select().join(Person).where(
        Person.name == name.title()).order_by(fn.random()).get()
    logging.info("%s requested a random quote from %s: %s",
                 request.remote_addr, quote.person_id.name, quote.id)
    return template('rickbot',
                    rickquote=quote,
                    shareme=request.urlparts,
                    persons=persons,
                    name=quote.person_id.name)


@app.route('/quote', method="POST")
def insert_quote():
    '''
    route for submitting quote
    '''
    unval_quote = clean_text(request.forms.get('saying'))
    if len(unval_quote) < 4:
        abort(code=400, text="That quote is too short.")
    name = str(request.forms.get('person'))
    person = Person.get(Person.name == name)
    try:
        logging.info("Inserting (%s, %s)", name, unval_quote)
        Quote.create(person_id=person, text=unval_quote,
                     entered_at=datetime.now().replace(microsecond=0)).save()
        return "IT WORKED! Please hit 'back' to go back"
    except Exception as e:
        logging.error(
            "could not insert quote (%s, %s), %s", name, unval_quote, str(e))
        return "Shit broke: {}".format(e)


@app.route('/quote/<quoteno>', method="GET")
def display_quote(quoteno):
    '''
    route for displaying a specific quote
    '''
    try:
        quote = Quote.select().where(Quote.id == quoteno).get()
    except:
        redirect('/')  # Silently fail for better experience
    persons = [row.name for row in Person.select()]
    return template('rickbot',
                    rickquote=quote,
                    shareme=request.urlparts,
                    persons=persons,
                    name=quote.person_id.name)


@app.route('/list', method="GET")
def list_all_quotes():
    '''
    route for listing all quotes
    '''
    quotes = [q for q in Quote.select()]
    req_url = request.urlparts[1]  # Send hostname not full url
    return template('list', list_of_quotes=quotes, req_url=req_url)


@app.route('/search')
def search_page():
    '''
    presents user with a search box and then redirects to serach api
    '''
    keyword = request.query.get("keyword")
    if keyword:
        redirect('/search/' + keyword)
    return template('search', search_results=None, searchbox=True)


@app.route('/search/<keyword>')
def search_for(keyword=None):
    '''
    route for actually executing a search
    '''
    matches = search(keyword)  # results are lowercase
    return template('search', search_results=matches, searchbox=False)


@app.route('/addname/<name:re:[a-zA-Z]+>')
def add_name(name):
    secret = request.query.get('secret', '')
    if secret != SECRET_KEY:
        abort(code=403, text="Nope!")
    Person.create(name=name.title()).save()
    return name.title() + " entered"


@app.route('/remove/<id:int>')
def remove_quote(id):
    secret = request.query.get('secret', '')
    if secret != SECRET_KEY:
        abort(code=403, text="Nope!")
    try:
        Quote.get(Quote.id == id).delete_instance()
        logging.info("%s deleted quote %s", request.remote_addr)
        return "Quote {} deleted successfully".format(id)
    except:
        logging.error(
            "The id %s does not exist or has already been deleted", id)
        abort(code=404, text="That id does not exist")


@app.error(404)
def error404(error):
    '''
    Custom 404 page
    '''
    return "<h1>No matching route found</h1>"


if __name__ == '__main__':
    run(app=app, **ENVIRON)
