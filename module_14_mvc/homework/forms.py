from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import InputRequired


class LibraryForm(FlaskForm):

    title = StringField(u'Title', validators=[InputRequired()])
    author = StringField(u'Author', validators=[InputRequired()])


class SearchForm(FlaskForm):

    search = StringField(u'Search', validators=[InputRequired()])
