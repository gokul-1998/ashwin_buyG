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
        id = db.Column(db.Integer, primary_key = True)
        name = db.Column(db.String(200), nullable = False)

class Product(db.Model):
        id = db.Column(db.Integer, primary_key = True)
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
    return render_template('admin_dashboard.html')

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username='admin').first()
        if admin is None:
            admin = User(username='admin',email='admin@admin.com',password='admin',is_store_manager=1)
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)