from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, IntegerField, SubmitField
from wtforms.validators import NumberRange, DataRequired

max_value = 10 ** 4

class UsersForm(FlaskForm):
    email = StringField('Domain')
    count = IntegerField('Counter', validators=[DataRequired(), NumberRange(min=1, max=max_value)])
    submit = SubmitField('Generate')


class VcfForm(FlaskForm):
    count = IntegerField('Counter', validators=[DataRequired(), NumberRange(min=1, max=max_value)])
    submit = SubmitField('Generate')


class SerialsForm(FlaskForm):
    count = IntegerField('Counter', validators=[DataRequired(), NumberRange(min=1, max=max_value)])
    submit = SubmitField('Generate')
