import json
import os

from flask import abort, render_template, redirect, request, url_for
from . import main
from .forms import SearchForm, AdvancedSearchForm

from .search import SearchEngine

engine = SearchEngine()


@main.route('/', methods=['GET'])
def index():
    form = SearchForm()
    return render_template('index.html', form=form)


@main.route('/search', methods=['GET'])
def search():
    form = SearchForm()
    q = request.args.get('q')
    if not q:
        redirect('/')  # not work
    if request.args.get('page') and request.args.get('page').isdigit():
        page = int(request.args.get('page'))
    else:
        page = 1

    res, total = engine.search(q, page)
    query_str = 'q={}'.format(q)
    num_page = (total - 1) // 10 + 2
    if page > num_page or page < 1:
        page = 1
        res, total = engine.search(q, page)

    if num_page <= 10:
        start, end = 1, num_page
    else:
        if num_page - page > 10:
            start = page
            end = page + 10
        else:
            start = num_page - 10
            end = num_page
    return render_template('search.html', res=res, query_str=query_str, page=page, pagenate=range(start, end), q=q)
    # return render_template('search.html', res=res, query_str=query_str, page=page, pagenate=range(1, (total - 1) // 10 + 2), q=q)


@main.route('/advanced-search', methods=['GET'])
def advanced_search():
    form = AdvancedSearchForm(action='/advanced-search')

    if len(request.args):
        q = request.args.get('q')
        title = request.args.get('title')
        author = request.args.get('author')
        publisher = request.args.get('publisher')
        category1 = request.args.get('category1')
        category2 = request.args.get('category2')
        category3 = request.args.get('category3')
        if request.args.get('page') and request.args.get('page').isdigit():
            page = int(request.args.get('page'))
        else:
            page = 1
        if not any([q, author]):
            return render_template('advanced_search_top.html', form=form)

        res, total = engine.advanced_search(q, title, author, publisher, category1, category2, category3, page)
        query_str = 'q={}&author={}&publisher={}&category1={}&category2={}&category3={}'.format(q, author, publisher, category1, category2, category3)
        num_page = (total - 1) // 10 + 2
        if page > num_page or page < 1:
            page = 1
            res, total = engine.search(q, page)

        if num_page <= 10:
            start, end = 1, num_page
        else:
            if num_page - page > 10:
                start = page
                end = page + 10
            else:
                start = num_page - 10
                end = num_page
        return render_template('search.html', res=res, query_str=query_str, page=page, pagenate=range(start, end), q=q)

    return render_template('advanced_search_top.html', form=form)


@main.route('/book/<int:book_id>', methods=['GET'])
def book(book_id):
    res = engine.search_book(book_id)
    if res['hits']['total']:
        q = request.args.get('q')
        if q:
            hits = engine.search_inside_book(q, book_id)
            hits = hits['hits']['hits'][0]['highlight']['main_text']
        else:
            hits = None
        category = ', '.join('NDC ' + cat for cat in res['hits']['hits'][0]['_source']['category3'])
        return render_template('book.html', res=res['hits']['hits'][0]['_source'], category=category, hits=hits)
    else:
        abort(404)


@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@main.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')


@main.route('/data/<int:level>', methods=['GET'])
def data(level):
    base = os.path.dirname(os.path.abspath(__file__)) + '/../static/data'
    if level == 1 or level == 2 or level == 3:
        path = os.path.join(base, 'table' + str(level) + '.json')
        return open(path).read()
    else:
        return '{}'
