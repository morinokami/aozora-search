from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class SearchForm(Form):
    text = StringField('', validators=[Required()])
    submit = SubmitField('検索')

