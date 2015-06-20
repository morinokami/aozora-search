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
    return render_template('search.html', res=res, query_str=query_str, page=page, pagenate=range(1, (total - 1) // 10 + 2), q=q)


@main.route('/advanced-search', methods=['GET'])
def advanced_search():
    form = AdvancedSearchForm(action='/advanced-search')

    if len(request.args):
        q = request.args.get('q')
        author = request.args.get('author')
        if request.args.get('page') and request.args.get('page').isdigit():
            page = int(request.args.get('page'))
        else:
            page = 1
        if not any([q, author]):
            return render_template('advanced_search_top.html', form=form)

        res, total = engine.advanced_search(q, author, page)
        query_str = 'q={}&author={}'.format(q, author)
        return render_template('search.html', res=res, query_str=query_str, page=page, pagenate=range(1, (total - 1) // 10 + 2), q=q)

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
        return render_template('book.html', res=res['hits']['hits'][0]['_source'], hits=hits)
    else:
        abort(404)


@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@main.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')
