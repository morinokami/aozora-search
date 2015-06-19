from flask import render_template, redirect, request, url_for
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
    if request.method == 'GET':
        form = SearchForm()
        q = request.args.get('q')
        query = {'match': {'main_text': q}}
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


@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@main.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')
