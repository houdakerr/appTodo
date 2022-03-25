from lib2to3.pytree import Node
from unicodedata import name
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import time
app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "todo.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
import http.client, urllib
conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": "aa5dj194ac43oz9251ji13w2z82w31",
    "user": "uf5dmo6ycj73gb53swhd6s1eye7cqp",
    "message": "hello world",
  }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    done = db.Column(db.Boolean)
    dateRappel = db.Column(db.Date)
    #timeRappel = db.Column(db.Date)
 
    #dateAdded = db.Column(db.DateTime, default=datetime.now())
    

def create_note(text,dateRappel):
    dateRappel  = datetime.strptime(dateRappel,"%Y-%m-%d")
    #timeRappel  = datetime.strptime(timeRappel,"%H:%M")
    note = Note(text=text, dateRappel=dateRappel)
    db.session.add(note)
    db.session.commit()
    db.session.refresh(note)


def read_notes():
    return db.session.query(Note).all()


def update_note(note_id, text,done):
    db.session.query(Note).filter_by(id=note_id).update({
        "text": text,
      
        "done": True if done == "on" else False

    })
    db.session.commit()


def delete_note(note_id):
    db.session.query(Note).filter_by(id=note_id).delete()
    db.session.commit()

#,request.form['timeRappel']
@app.route("/", methods=["POST", "GET"])
def view_index():
    if request.method == "POST":
        create_note(request.form['text'] ,request.form['dateRappel'] )
    return render_template("index.html", notes=read_notes())


@app.route("/edit/<note_id>", methods=["POST", "GET"])
def edit_note(note_id):
    if request.method == "POST":
        update_note(note_id, text=request.form['text'], done=request.form['done'])
    elif request.method == "GET":
        delete_note(note_id)
    return redirect("/", code=302)



#list of all tasks in json 
@app.route('/api/all.json')
def liste_task_api():
    liste=db.session.query(Note).all()
    responses = {x.id: x.text for x in liste}
    return responses

#add task in json 
@app.route('/api/add.json')
def add_note_api():
    tache = request.args.get("name")
    create_note(tache)

    liste=db.session.query(Note).all()
    responses = {x.id: x.text for x in liste}
    return responses


#delete task in json 
@app.route('/api/delete.json')
def delete_note_api():
    tache_id = request.args.get("id")
    delete_note(tache_id)

    liste=db.session.query(Note).all()
    responses = {x.id: x.text for x in liste}
    return responses

#edit task 
@app.route('/api/modifierTache')
def modifier_note_by_api():
    tache_id = request.args.get("id")
    name = request.args.get("name")
    update_note(tache_id,name,False)

    liste=db.session.query(Note).all()
    responses = {x.id: x.text for x in liste}
    return responses







if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)



