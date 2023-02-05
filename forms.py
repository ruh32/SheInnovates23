from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
class AssignForm:
    date = StringField('Due Date')
    professor = StringField('Professor/Class')
    name = StringField('Name of Assignment')
    description = StringField('Description')
    button = SubmitField("Add")

