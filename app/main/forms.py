from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class SearchForm(Form):
    q = StringField('', validators=[Required()])
    submit = SubmitField('検索')


class AdvancedSearchForm(Form):
    q = StringField('キーワード', validators=[Required()])
    title = StringField('タイトル')
    author = StringField('著者名')
    publisher = StringField('出版社名')
    submit = SubmitField('検索')
