from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class JoinForm(Form):
    planning = StringField('Planning', validators=[DataRequired(message="No planning meeting selected.")])
    password = PasswordField('Password', validators=[DataRequired(message="No password entered.")])
    name = StringField('Name', validators=[DataRequired(message="No name was entered.")])