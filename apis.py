from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from database import db
from models import User, Section, Product, Cart


class category_api(Resource):
    def get(self):
        cat=db.session.query(Section).all()
        print(cat)
        return "hello world"



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







##
## Actually setup the Api resource routing here
##

