from datetime import datetime
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy



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
    
        def __repr__(self):
            return '<User %r>' % self.username

class Section(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        name = db.Column(db.String(200), nullable = False)

class Product(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement=True)
        name = db.Column(db.String(200), nullable = False)
        price = db.Column(db.Integer, nullable = False)
        expiry_date = db.Column(db.DateTime , default = datetime.now())
        quantity_available = db.Column(db.Integer, nullable = False)
        section_id = db.Column(db.Integer, nullable = False)
        description = db.Column(db.String(200), nullable = False)


    



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
            if user.email == email and user.password == password:
                print("inside if condition")
                return redirect(url_for('user_dashboard'))
        return redirect(url_for('login'))
    return render_template('login.html')


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

@app.route('/user_dashboard/<int:user_id>')
def user_dashboard(user_id):
    return render_template('user_dashboard.html',user_id=user_id)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username='admin').first()
        if admin is None:
            admin = User(username='admin',email='admin@admin.com',password='admin',is_store_manager=1)
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)