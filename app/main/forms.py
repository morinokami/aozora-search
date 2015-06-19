from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class SearchForm(Form):
    q = StringField('', validators=[Required()])
    submit = SubmitField('検索')
