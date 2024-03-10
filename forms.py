from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, DateField, IntegerField
from wtforms.validators import DataRequired, URL


# WTForm for creating a todo
class CreateToDoForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description")
    due_date = DateField("Due Date")
    priority = IntegerField("Priority")
    submit = SubmitField("Add Task")


# WTForm for editing a todo
class EditToDoForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description")
    due_date = DateField("Due Date")
    priority = IntegerField("Priority")
    completion = RadioField("Task completed", choices=[(False, "no"), (True, "yes")])
    submit = SubmitField("Edit")