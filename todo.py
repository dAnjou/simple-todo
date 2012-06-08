from bottle import route, run, template, redirect, debug, static_file, request, abort

from couchdbkit import Server, Document, StringProperty
from couchdbkit.designer import push

couch = Server()
db = couch.get_or_create_db('simple-todo')

push('db/todolist', db)
push('db/todo', db)

class TodoList(Document):
    pass

class Todo(Document):
    title = StringProperty()
    priority = StringProperty()
    todolist = StringProperty()

TodoList.set_db(db)
Todo.set_db(db)

@route('/static/:filepath#.*#')
def server_static(filepath):
    return static_file(filepath, root='./static')

@route('/')
def index():
    todolist = TodoList()
    todolist.save()
    redirect('/%s/' % todolist['_id'])

@route('/l/')
def todolists():
    lists = TodoList.view('todolist/all')
    return template('list', lists=lists)

@route('/:list_id/')
def todolist(list_id):
    todolist = TodoList.get_or_create(list_id)
    all_todos = Todo.view('todo/all')
    todos = []
    for todo in all_todos:
        if todo.todolist == todolist['_id']:
            todos.append(todo)
    return template('index', todos=todos)

@route('/:list_id/add', method='POST')
def add(list_id):
    try:
        todolist = TodoList.get(list_id)
    except:
        abort(404)
    title = request.forms.get('title')
    priority = request.forms.get('priority')
    if title and not title.strip() == "":
        todo = Todo(title=title)
        if priority:
            todo.priority = priority
        todo.todolist = list_id
        todo.save()
    redirect('/%s/' % list_id)

@route('/t/delete', method='POST')
def delete():
    todo_id = request.forms.get('todo_id')
    if todo_id.startswith('todo-'):
        t = Todo.get(todo_id[5:])
        t.delete()
    return "success"

if __name__ == '__main__':
    debug(True)
    run(host='0.0.0.0', port=8080, reloader=True)
