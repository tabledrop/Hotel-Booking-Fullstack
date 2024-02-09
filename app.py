from flask import Flask, render_template

# calls Flask API, sets template folder for HTML documents, static folder for CSS/JS files
app = Flask(__name__, template_folder="templates", static_folder="static")

# creates 127.0.0.1:5000/ url
@app.route('/')
def home():
    return render_template('home.html')

# 127.0.0.1:5000/rooms url
@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

# 127.0.0.1:5000/login
@app.route('/login')
def login():
    return render_template('login.html')

# 127.0.0.1:5000/sign-up
@app.route('/sign-up')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
