from bottle import route, run, template, redirect, debug, static_file, request, abort

from couchdbkit import Server, Document, StringProperty
from couchdbkit.designer import push

try:
    import simplejson as json
except ImportError:
    import json
import mimerender

mimerender = mimerender.BottleMimeRender()

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

render_json = lambda **x: json.dumps({"lists": [l['_id'] for l in x["lists"]]})
render_html = lambda **x: template('list', lists=x["lists"])
render_txt = lambda **x: "\n".join([l['_id'] for l in x["lists"]])

@route('/l/')
@mimerender(
    default = 'html',
    html = render_html,
    json = render_json,
    txt  = render_txt
)
def todolists():
    lists = TodoList.view('todolist/all')
    return {"lists": lists}

render_json = lambda **x: json.dumps(x)
render_html = lambda **x: template('index', todos=x["todos"])
render_txt = lambda **x: "\n".join([y["title"] for y in x["todos"]])

@route('/:list_id/')
@mimerender(
    default = 'html',
    html = render_html,
    json = render_json,
    txt  = render_txt
)
def todolist(list_id):
    todolist = TodoList.get_or_create(list_id)
    all_todos = Todo.view('todo/all')
    todos = []
    for todo in all_todos:
        if todo.todolist == todolist['_id']:
            todos.append(dict(todo, id=todo['_id']))
    return {"todos": todos}

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
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", default='wsgiref', choices=['wsgiref', 'flup'])
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-r", "--reloader", action="store_true")
    args = parser.parse_args()
    debug(args.debug)
    if args.server == 'wsgiref':
        run(reloader=args.reloader)
    if args.server == 'flup':
        run(server='flup', bindAddress='/tmp/simple-todo.sock', reloader=args.reloader)
