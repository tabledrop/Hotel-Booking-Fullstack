from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

# 127.0.0.1:5000/login
@auth.route('/login')
def login():
    return render_template('login.html')

# 127.0.0.1:5000/sign-up
@auth.route('/sign-up')
def signup():
    return render_template('signup.html')