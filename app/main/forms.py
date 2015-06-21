from flask.ext.wtf import Form
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import Required


class SearchForm(Form):
    q = StringField('', validators=[Required()])
    submit = SubmitField('検索')


class AdvancedSearchForm(Form):
    q = StringField('キーワード:', validators=[Required()])
    title = StringField('タイトル:')
    author = StringField('著者名:')
    publisher = StringField('底本の出版社名:')
    category1 = SelectField(choices=[])
    category2 = SelectField(choices=[])
    category3 = SelectField(choices=[])
    submit = SubmitField('検索')
