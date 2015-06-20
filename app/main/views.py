from flask import abort, render_template, redirect, request, url_for
from . import main
from .forms import SearchForm, AdvancedSearchForm

from elasticsearch import Elasticsearch

es = Elasticsearch()


@main.route('/', methods=['GET'])
def index():
    form = SearchForm()
    return render_template('index.html', form=form)


@main.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        form = SearchForm()
        q = request.args.get('q')
        query = {'match': {'main_text': {'query': q, 'operator': 'and'}}}
        highlight = {'fields': {'main_text': {}}}
        if request.args.get('page') and request.args.get('page').isdigit():
            page = int(request.args.get('page'))
            from_ = (page - 1) * 10
        else:
            page = 1
            from_ = 0
        res = es.search(index='aozora-search', body={'query': query, 'highlight': highlight, 'from': from_})
        total = res['hits']['total']
        return render_template('search.html', res=res, page=page, pagenate=range(1, (total - 1) // 10 + 2), q=q)
    else:
        return 'not yet'


@main.route('/advanced-search', methods=['GET'])
def advanced_search():
    form = AdvancedSearchForm()
    print(dir(form))
    return render_template('advanced_search.html', form=form)


@main.route('/book/<int:book_id>', methods=['GET'])
def book(book_id):
    query = {
        'filtered': {
            'query': {
                'match_all': {}
            },
            'filter': {
                'term': {
                    'book_id': book_id
                }
            }
        }
    }
    res = es.search(index='aozora-search', body={'query': query})
    if res['hits']['total']:
        q = request.args.get('q')
        if q is None:
            abort(404)
        query = {
            "filtered": {
                "query": {
                    "match": {
                        "main_text": q
                    }
                },
                "filter": {
                    "term": {
                        "book_id": book_id
                    }
                }
            }
        }
        highlight = {'fields': {'main_text': {}}}
        hits = es.search(index='aozora-search', body={'query': query, 'highlight': highlight})
        return render_template('book.html', res=res['hits']['hits'][0]['_source'], hits=hits['hits']['hits'][0]['highlight']['main_text'])
    else:
        abort(404)


@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@main.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')
