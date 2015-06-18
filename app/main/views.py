from flask import render_template, url_for
from . import main
from .forms import SearchForm


@main.route('/', methods=['GET'])
def index():
    form = SearchForm()
    return render_template('index.html', form=form)


@main.route('/search', methods=['GET', 'POST'])
def search():
    return "search res"


@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@main.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')
