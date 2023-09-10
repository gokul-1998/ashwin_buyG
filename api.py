from flask import Flask
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

class Category:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def to_dict(self):
        return {"name": self.name, "id": self.id}


c1=Category("Electronics",1)
c2=Category("Food",2)
c3=Category("Clothes",3)
Categories=[c1,c2,c3]

cat_parser = reqparse.RequestParser()
cat_parser.add_argument('name')
cat_parser.add_argument('id')

class CategoryList(Resource):
    def get(self):
        return [c.__dict__ for c in Categories]
        
    def post(self):
        args = cat_parser.parse_args()
        
        Categories.append(Category(args['name'], args['id']))
        return Categories[-1].to_dict(), 201
    
class Category1(Resource):
    def get(self, id):
        for c in Categories:
            if c.id == int(id):
                return c.to_dict()
                
        return None
        
    def put(self, id):
        args = cat_parser.parse_args()
        for c in Categories:
            if c.id == id:
                c.name = args['name']
                return c.to_dict()
        return None
        
    def delete(self, id):
        for c in Categories:
            if c.id == id:
                Categories.remove(c)
                return c.to_dict()
        return None


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(CategoryList, '/categories')
api.add_resource(Category1, '/categories/<id>')



if __name__ == '__main__':
    app.run(debug=True)