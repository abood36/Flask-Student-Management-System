from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, Email, Length

class StudentForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired(), Length(max=120)])
    last_name = StringField("Last name", validators=[Optional(), Length(max=120)])
    email = StringField("Email", validators=[Optional(), Email(), Length(max=180)])
    roll = StringField("Roll number", validators=[Optional(), Length(max=30)])
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=2000)])
    submit = SubmitField("Save")

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")
