from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/about')
def about():
    return 'About Page'

@app.route('/contact')
def contact():
    return 'Contact Page'

@app.route('/user/<username>')
def user(username):
    return 'User %s' % username


if __name__ == '__main__':
    app.run(debug=True)