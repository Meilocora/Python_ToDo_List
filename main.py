from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_bootstrap import Bootstrap5
from forms import CreateToDoForm, EditToDoForm
from datetime import datetime, date

FILTER = "priority"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Connect to Database
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
Bootstrap5(app)

# TABLE Configuration
class ToDo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    due_date: Mapped[str] = mapped_column(String(250), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=True)
    completion: Mapped[bool] = mapped_column(Boolean, nullable=True)

with app.app_context():
    db.create_all()


def to_bool(input_string):
    if input_string == "True":
        return True
    else:
        return False

@app.route("/")
def home():
    if FILTER == "priority":
        result = db.session.execute(db.select(ToDo).where(ToDo.completion == False).order_by(ToDo.priority))
    elif FILTER == "due_date":
        result = db.session.execute(db.select(ToDo).where(ToDo.completion == False).order_by(ToDo.due_date))
    else:
        result = db.session.execute(db.select(ToDo).where(ToDo.completion == False).order_by(ToDo.title))
    todos = result.scalars().all()
    return render_template("index.html", all_todos=todos, selected_site="dashboard", date=date, datetime=datetime, filter=FILTER)


@app.route("/completed-tasks")
def completed_tasks():
    if FILTER == "priority":
        result = db.session.execute(db.select(ToDo).where(ToDo.completion == True).order_by(ToDo.priority))
    elif FILTER == "due_date":
        result = db.session.execute(db.select(ToDo).where(ToDo.completion == True).order_by(ToDo.due_date))
    else:
        result = db.session.execute(db.select(ToDo).where(ToDo.completion == True).order_by(ToDo.title))
    todos = result.scalars().all()
    return render_template("completed-tasks.html", completed_todos=todos,selected_site="completed_tasks", filter=FILTER)


@app.route("/new-todo", methods=["GET", "POST"])
def add_todo():
    form = CreateToDoForm()
    if form.validate_on_submit():
        new_todo = ToDo(
            title = form.title.data,
            description = form.description.data,
            due_date = form.due_date.data,
            priority = form.priority.data,
            completion = False
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add-todo.html", form=form, selected_site="add_task", filter=FILTER)


@app.route("/edit-cafe/<int:todo_id>", methods=["GET", "POST"])
def edit_todo(todo_id):
    todo = db.get_or_404(ToDo, todo_id)
    edit_form = EditToDoForm(
            title = todo.title,
            description = todo.description,
            due_date = datetime.strptime(todo.due_date, "%Y-%m-%d").date(),
            priority = todo.priority,
            completion = todo.completion
    )
    if edit_form.validate_on_submit():
        todo.title = edit_form.title.data
        todo.description = edit_form.description.data
        todo.due_date =  edit_form.due_date.data
        todo.priority = edit_form.priority.data
        todo.completion = to_bool(edit_form.completion.data)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit-todo.html", form=edit_form)


@app.route("/delete/<int:todo_id>")
def delete_todo(todo_id):
    todo_to_delete = db.get_or_404(ToDo, todo_id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/complete/<int:todo_id>")
def complete_todo(todo_id):
    todo = db.get_or_404(ToDo, todo_id)
    todo.completion = True
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/incomplete/<int:todo_id>")
def incomplete_todo(todo_id):
    todo = db.get_or_404(ToDo, todo_id)
    todo.completion = False
    db.session.commit()
    return redirect(url_for("completed_tasks"))


@app.route("/filter/<string:new_filter>")
def change_filter(new_filter):
    global FILTER
    FILTER = new_filter
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
