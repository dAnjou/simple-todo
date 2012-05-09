from bottle import route, run, template, redirect
import peewee

db = peewee.SqliteDatabase('database.db')

class Todo(peewee.Model):
    todo = peewee.TextField()

    class Meta:
        database = db

@route('/')
def index():
    return template('index', todos=Todo.select())

@route('/add', method='POST')
def add(todo=None):
    todo = todo.strip()
    if todo and not todo == "":
        Todo.create(todo=todo)
    redirect('/')

@route('/delete', method='POST')
def delete(id=None):
    if id:
        t = Todo.get(id)
        t.delete_instance()
    redirect('/')

run(host='0.0.0.0', port=8080, debug=True)