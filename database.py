from flask_sqlalchemy import SQLAlchemy
from main import app
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey

db = SQLAlchemy(app)

class User(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        username = db.Column(db.String(200), nullable = False)
        email = db.Column(db.String(200), nullable = False)
        password = db.Column(db.String(200), nullable = False)
        is_store_manager = db.Column(db.Integer, default= 0)
        user_cart = relationship('Cart', backref='user', lazy=True)

    
        def __repr__(self):
            return '<User %r>' % self.username

class Section(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        name = db.Column(db.String(200), nullable = False)
        products = relationship('Product', backref='section', lazy=True, order_by='desc(Product.id)', cascade="all, delete-orphan")


class Product(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        name = db.Column(db.String(200), nullable = False)
        price = db.Column(db.Integer, nullable = False)
        expiry_date = db.Column(db.DateTime , default = datetime.now())
        quantity_available = db.Column(db.Integer, nullable = False)
        section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)  # Define a foreign key to establish the relationship
        description = db.Column(db.String(200), nullable = False)

class Cart(db.Model):
    id= db.Column(db.Integer, primary_key = True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Define a foreign key to establish the relationship
    quantity = db.Column(db.Integer, nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.now())
    is_purchased = db.Column(db.Integer, default= 0)
    product_id = db.Column(db.Integer, ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    car_product = relationship('Product', backref='cart', lazy=True)


def initialize_database(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

        # Add your initial data here
        # ...

if __name__ == "__main__":
    from main import app  # Importing app from your main module
    initialize_database(app)