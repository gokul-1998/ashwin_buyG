from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

users = []

class User:
    def __init__(self,id, username, email, password,is_store_manager):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.is_store_manager = is_store_manager
    
    def __repr__(self):
        return '<User %r>' % self.username

admin = User(1,'admin','admin@admin','admin',1)
users.append(admin)

class Section:
    def __init__(self,id, name):
        self.id = id
        self.name = name

class Product:
    def __init__(self,id, name, price,expiry_date, quantity_available, section_id, description):
        self.id = id
        self.name = name
        self.price = price # rate per unit  (e.g. 1kg)
        self.expiry_date = expiry_date
        self.quantity_available = quantity_available
        self.section_id = section_id
        self.description = description

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup',methods =['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        id= len(users)+1
        user = User(id,username,email,password,0)
        users.append(user)
        print(users)
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login',methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email,password)
        for user in users:
            if user.email == email and user.password == password:
                print("inside if condition")
                return redirect(url_for('user_dashboard',user=user))
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/user_dashboard/<int:user_id>')
def user_dashboard(user_id):
    return render_template('user_dashboard.html',user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)