from bottle import route, run, template, redirect, debug, static_file, request, abort

from couchdbkit import Server, Document, StringProperty, ListProperty
from couchdbkit.designer import push

couch = Server()
db = couch.get_or_create_db('simple-todo')

push('db/todolist', db)
push('db/todo', db)

class TodoList(Document):
    todos = ListProperty()

class Todo(Document):
    title = StringProperty()
    priority = StringProperty()

TodoList.set_db(db)
Todo.set_db(db)

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

@route('/')
def index():
    #return template('index', todos=Todo.select())
    l = TodoList.view('todolist/all').first()
    for x in dir(l):
        print type(l[str(x)]), str(x)
    return "lol"

@route('/l/<list_id>')
def list(list_id):
    todolist = TodoList.load(db, list_id)
    if not todolist:
        todolist = TodoList()
        todolist.store(db)
    return todolist.todos

@route('/l/<list_id>/add', method='POST')
def add(list_id):
    todolist = TodoList.load(db, list_id)
    if not todolist:
        abort(404)
    title = request.forms.title
    priority = request.forms.priority
    if title and not title.strip() == "":
        todo = Todo(title=title)
        if priority:
            todo.priority = priority
        todo.store(db)
        todolist.todos.append(todo.id)
    redirect('/l/%s' % todolist.id)

@route('/l/<list_id>/delete', method='POST')
def delete():
    todo_id = request.forms.todo_id
    if todo_id.startswith('todo-'):
        t = Todo.get(id=int(todo_id[5:]))
        t.delete_instance()
    return "success"

if __name__ == '__main__':
    debug(True)
    run(host='0.0.0.0', port=8080, reloader=True)
