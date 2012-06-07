from bottle import route, run, template, redirect, debug, static_file, request
import peewee

db = peewee.SqliteDatabase('database.db')

class Todo(peewee.Model):
    todo = peewee.TextField()
    priority = peewee.CharField()

    class Meta:
        database = db

db.connect()

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

@route('/')
def index():
    return template('index', todos=Todo.select())

@route('/l/<list_id>')
def list(list_id):
    pass

@route('/add', method='POST')
def add():
    todo = request.forms.todo
    priority = request.forms.priority
    if todo and not todo.strip() == "":
        t = Todo()
        t.todo = todo
        if priority:
            t.priority = priority
        t.save()
    redirect('/')

@route('/delete', method='POST')
def delete():
    todo_id = request.forms.todo_id
    if todo_id.startswith('todo-'):
        t = Todo.get(id=int(todo_id[5:]))
        t.delete_instance()
    return "success"

if __name__ == '__main__':
    debug(True)
    run(host='0.0.0.0', port=8080, reloader=True)
