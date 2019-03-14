from flask import Flask,render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap=Bootstrap(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.route('/login')
def login():
    return render_template('login.html')

@app.errorhandler(404)
def not_found(err):
    return render_template('404.html'),404


@app.errorhandler(500)
def server_error(err):
    return render_template('500.html'),500