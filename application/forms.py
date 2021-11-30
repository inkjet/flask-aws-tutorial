from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class EnterDBInfo(FlaskForm):
    dbNotes = TextAreaField(label='Items to add to DB', validators=[DataRequired(), Length(min=0, max=128, message=u'Enter 128 characters or less')])
    dbGreeting = TextAreaField(label='Greeting to add to DB', validators=[DataRequired(), Length(min=0, max=128, message=u'Enter 128 characters or less')])
    submit = SubmitField('Submit')


class RetrieveDBInfo(FlaskForm):
    numRetrieve = IntegerField(label='Number of DB Items to Get', validators=[DataRequired(), NumberRange(min=0, max=10, message=u'Enter a number between 1 and 10')])
    retrieve = SubmitField('Retrieve')
