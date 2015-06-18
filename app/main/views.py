from flask import render_template, url_for
from . import main
from .forms import SearchForm

from elasticsearch import Elasticsearch

es = Elasticsearch()


@main.route('/', methods=['GET'])
def index():
    form = SearchForm()
    return render_template('index.html', form=form)


@main.route('/search', methods=['GET', 'POST'])
def search():
    res = es.search(index="aozora-search", body={"query": {"match_all": {}}})
    return 'Got %d Hits:' % res['hits']['total']


@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@main.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')
