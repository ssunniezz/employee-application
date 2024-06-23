from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class StateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=80)])
    submit = SubmitField('Submit')


class PositionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    details = StringField('Details', validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('Submit')


class DepartmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    manager = SelectField('Manager', coerce=int, validators=[Optional()])
    submit = SubmitField('Submit')


class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    address = StringField('Address', validators=[DataRequired(), Length(min=1, max=200)])
    position = SelectField('Position', coerce=int, validators=[DataRequired()])
    department = SelectField('Department', coerce=int, validators=[DataRequired()])
    state = SelectField('State', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')


class SearchEmployeeForm(FlaskForm):
    position = SelectField('Position', coerce=int, validators=[Optional()])
    department = SelectField('Department', coerce=int, validators=[Optional()])
    state = SelectField('State', coerce=int, validators=[Optional()])
    submit = SubmitField('Search')
