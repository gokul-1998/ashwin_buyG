from datetime import datetime
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     content = db.Column(db.String(200), nullable = False)
#     completed = db.Column(db.Integer, default= 0)
#     date_created = db.Column(db.DateTime , default = datetime.now())


#     def __repr__(self):
#         return '<Task %r>' % self.id
    
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
        products = relationship('Product', backref='section', lazy=True)

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
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # Define a foreign key to establish the relationship
    quantity = db.Column(db.Integer, nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.now())
    is_purchased = db.Column(db.Integer, default= 0)
    car_product = relationship('Product', backref='cart', lazy=True)
import os
# if os.path.exists("./test.db"):
#     os.remove("./test.db")
if not os.path.exists("./test.db"):
    with app.app_context():
            db.create_all()
            admin = User.query.filter_by(username='admin').first()
            if admin is None:
                admin = User(id=1,username='admin',email='admin@admin.com',password='admin',is_store_manager=1)
                db.session.add(admin)
                #db.session.commit()


                c1=Section(id=1,name="Fruits")
                c2=Section(id=2,name="Vegetables")
                c3=Section(id=3,name="Dairy")
                db.session.add(c1)
                db.session.add(c2)
                db.session.add(c3)
                # db.session.flush()
                p1=Product(id=1,name="Apple",price=50,expiry_date=datetime(2022,1,1),quantity_available=10,section_id=1,description="Good for health")
                p2=Product(id=2,name="Banana",price=60,expiry_date=datetime(2022,1,1),quantity_available=10,section_id=1,description="Good for health")
                p3=Product(id=3,name="Tomato",price=70,expiry_date=datetime(2022,1,1),quantity_available=10,section_id=2,description="Good for health")
                p4=Product(id=4,name="Potato",price=80,expiry_date=datetime(2022,1,1),quantity_available=10,section_id=2,description="Good for health")
                db.session.add(p1)
                db.session.add(p2)
                db.session.add(p3)
                db.session.add(p4)
                # db.session.flush()
                u1=User(id=2,username="gok",email="gok@gm.com",password="admin",is_store_manager=0)
                db.session.add(u1)
                # db.session.flush()
                c1=Cart(id=1,user_id=2,product_id=1,quantity=1)
                c2=Cart(id=2,user_id=2,product_id=2,quantity=1)
                db.session.add(c1)
                db.session.add(c2)
                db.session.commit()
                user=User.query.all()
                print(user[0].user_cart)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup',methods =['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username,email=email,password=password,is_store_manager=0)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding new user'
            
    return render_template('signup.html')

@app.route('/login',methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email,password)
        users=User.query.all()
        for user in users:
            if user.email == email and user.password == password and user.email!="admin@admin.com":
                print("inside if condition")
                return redirect(f'/user_dashboard/{user.id}')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/user_dashboard/<int:user_id>',methods =['GET'])
def user_dashboard(user_id):
    cats = Section.query.all()
    user = User.query.get_or_404(user_id)
    products = Product.query.all()
    query = request.args.get('query', '').lower()
    if query:
        products = Product.query.filter(Product.name.contains(query)).all()
        return render_template('user_dashboard.html',cats = cats,user=user,products = products,query=query)
    for i in cats:
        print(i.name)
        print(i.products)
    
    return render_template('user_dashboard.html',cats = cats, user=user,products = products)



@app.route('/admin_dashboard')
def admin_dashboard():
    section=Section.query.all()
    return render_template('admin_dashboard.html',blahblah=section)

@app.route('/admin_login',methods =['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email,password)
        users=User.query.all()
        for user in users:
            
            if user.email == email and user.password == password:
                return redirect(url_for('admin_dashboard'))
        return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

@app.route('/add_category',methods =['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        user = Section(name=name)
        try:
                db.session.add(user)
                db.session.commit()
                return redirect('/admin_dashboard')
        except:
                return 'There was an issue adding new user'
    return render_template('add_category.html')

@app.route('/delete_category/<int:id>')
def delete_category(id):
    category_to_delete = Section.query.get_or_404(id)

    try:
        db.session.delete(category_to_delete)
        db.session.commit()
        return redirect('/admin_dashboard')
    except:
        return 'There was a problem deleting that task'
@app.route('/rename_category/<int:id>', methods=['GET', 'POST'])
def rename_category(id):
    section = Section.query.get_or_404(id)

    if request.method == 'POST':
        section.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/admin_dashboard')
        except:
            return 'There was an issue renaming your category'

    else:
        return render_template('rename_category.html', section=section)


@app.route('/add_product/<int:category_id>', methods=['GET', 'POST'])
def add_product(category_id):
    category= Section.query.get_or_404(category_id)
    if request.method == 'POST':
        name = request.form.get('product_name')
        price = request.form.get('price')
        expiry_date = request.form.get('expiry_date')
        quantity_available = request.form.get('quantity_available')
        description = request.form.get('description')

        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')

        new_product = Product(
            name=name,
            price=price,
            expiry_date=expiry_date,
            quantity_available=quantity_available,
            section_id=category.id,  # Set the section_id to the current category
            description=description
        )

        # Add the new product to the database
        db.session.add(new_product)
        db.session.commit()
        return redirect(f"/view_category/{category_id}")
          
    return render_template('add_product.html', category=category)

@app.route('/view_category/<int:category_id>', methods=['GET', 'POST'])
def view_category(category_id):
     category= Section.query.get_or_404(category_id)
     print(category.id,category.name)
     products = Product.query.filter_by(section_id=category_id).all()


     

     return render_template('view_category.html',cat=category,products=products)
@app.route('/delete_product/<int:id>')
def delete_product(id):
    product_to_delete = Product.query.get_or_404(id)
    cat_id=product_to_delete.section_id
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect(f'/view_category/{cat_id}')
    except:
        return 'There was a problem deleting that product'
   
@app.route('/update_product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.get_or_404(id)
    expiry_date_str = product.expiry_date.strftime('%Y-%m-%d')

    if request.method == 'POST':
        product.name = request.form['product_name']
        product.price = request.form['price']
        expiry_date = request.form['expiry_date']
        product.expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')
        product.quantity_available = request.form['quantity_available']
        product.description = request.form['description']

        try:
            db.session.commit()
            return redirect(f'/view_category/{product.section_id}')
        except:

            return 'There was an issue updating your category'

    else:
        return render_template('update_product.html', product=product, date=expiry_date_str)

@app.route('/add_to_cart/<int:user_id>/<int:product_id>', methods=['GET', 'POST'])

def add_to_cart(user_id,product_id):
    user=User.query.get_or_404(user_id)
    product=Product.query.get_or_404(product_id)
    if request.method == 'POST':
         Quantity = request.form['Quantity']
         user_cart_items=Cart.query.filter_by(user_id=user_id,product_id=product_id).first()
         if user_cart_items:
            user_cart_items.quantity+=int(Quantity)
            db.session.commit()
            return redirect(f'/user_dashboard/{user_id}')
         else:
            cart=Cart(user_id=user_id,product_id=product_id,quantity=Quantity)
            db.session.add(cart)
            db.session.commit()
            return redirect(f'/user_dashboard/{user_id}')
     
    return render_template('add_to_cart.html',user=user,product=product)

@app.route('/showcart/<int:user_id>', methods=['GET', 'POST'])

def showcart(user_id):
    user=User.query.get_or_404(user_id)
    cart_items=Cart.query.filter_by(user_id=user_id).all()
    Total=0
    for item in cart_items:
        Total+=item.quantity*item.car_product.price
    return render_template('showcart.html',user=user,cart_items=cart_items,Total=Total)

@app.route('/remove_item/<int:user_id>/<int:item_id>', methods=['GET', 'POST'])

def remove_item(user_id,item_id):
    
    item_to_delete = Cart.query.get_or_404(item_id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(f'/showcart/{user_id}')
    except:
        return 'There was a problem deleting that item'

@app.route('/update_quantity/<int:user_id>/<int:item_id>', methods=['GET', 'POST'])

def update_quantity(user_id,item_id):
    
    #item_to_update = Cart.query.get_or_404(user_id,item_id)
    #above line is same as below line
    item_to_update = Cart.query.filter_by(user_id=user_id,product_id=item_id).first()
    print(item_to_update)
    if request.method == 'POST':
        Quantity = request.form['update_quantity']
        item_to_update.quantity=Quantity
        db.session.commit()
        return redirect(f'/showcart/{user_id}')
    else:
        return render_template('update_quantity.html',item_to_update=item_to_update)
    return render_template('update_quantity.html')

@app.route('/checkout/<int:user_id>', methods=['GET', 'POST'])

def checkout(user_id):
    user=User.query.get_or_404(user_id)
    cart_items=Cart.query.filter_by(user_id=user_id).all()
    Total=0
    for item in cart_items:
        Total+=item.quantity*item.car_product.price
    return render_template('checkout.html',user=user,cart_items=cart_items,Total=Total)

@app.route('/buy/<int:user_id>', methods=['GET', 'POST'])

def buy(user_id):
    
    cart_items=Cart.query.filter_by(user_id=user_id).all()
    # To remove all the cart items from the cart table
    for item in cart_items:
        item.car_product.quantity_available-=item.quantity
        db.session.delete(item)
    db.session.commit()    
    return redirect(f'/user_dashboard/{user_id}')


    # Filter products based on the search query
    filtered_cats = []
    for cat in cats:
        cat.products = [product for product in cat.products if query in product.name.lower()]

        # Add categories with matching products to the filtered_cats list
        if cat.products:
            filtered_cats.append(cat)

    return render_template('user_dashboard.html', cats=filtered_cats, user=user, query=query)


if __name__ == '__main__':
    
    app.run(debug=True)

