from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, IntegerField, SubmitField
from wtforms.validators import NumberRange, DataRequired


class UsersForm(FlaskForm):
    email = StringField('Email')
    count = IntegerField('Counter', validators=[DataRequired(), NumberRange(min=1, max=10 ** 4)])
    submit = SubmitField('Generate')


class VcfForm(FlaskForm):
    count = IntegerField('Counter', validators=[DataRequired(), NumberRange(min=1, max=10 ** 4)])
    submit = SubmitField('Generate')


class SerialsForm(FlaskForm):
    count = IntegerField('Counter', validators=[DataRequired(), NumberRange(min=1, max=10 ** 4)])
    submit = SubmitField('Generate')
