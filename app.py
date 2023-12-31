from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "todo.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    done = db.Column(db.Boolean)
    dateAdded = db.Column(db.DateTime, default=datetime.now())


def create_note(text):
    note = Note(text=text)
    db.session.add(note)
    db.session.commit()
    db.session.refresh(note)


def read_notes():
    return db.session.query(Note).all()


def update_note(note_id, text, done):
    note = db.session.query(Note).get(note_id)
    note.text = text
    note.done = done
    db.session.commit()


def delete_note(note_id):
    note = db.session.query(Note).get(note_id)
    db.session.delete(note)
    db.session.commit()


@app.route("/", methods=["POST", "GET"])
def view_index():
    if request.method == "POST":
        create_note(request.form['text'])
    return render_template("index.html", notes=read_notes())


@app.route("/edit/<note_id>", methods=["POST", "GET"])
def edit_note(note_id):
    if request.method == "POST":
        update_note(
            note_id,
            text=request.form['text'],
            done=True if request.form.get('done') == 'on' else False
        )
    elif request.method == "GET":
        delete_note(note_id)
    return redirect("/", code=302)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
