# imports for web service fullstack
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from datetime import datetime
from datetime import date
import pandas as pd

# Flask init config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservations.db'  # SQLite database file
app.config['SQALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'



# User model for Flask-Login
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


# Reservation model
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='reservations')
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    num_guests = db.Column(db.Integer, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html')

from predict import predict_model
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    today = date.today()
    if request.method == 'POST':
        # get data from form
        selected_date = request.form['selectedDate']
        season = request.form['season']

        # parse data from form to appropriate Pandas DataFrame
        selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
        year = selected_date_obj.year
        month = selected_date_obj.month
        day = selected_date_obj.day
        weekday = selected_date_obj.weekday()

        dataframe = pd.DataFrame({
            'year': [year],
            'month': [month],
            'day': [day],
            'season': [season],
            'day_of_week': [weekday]
            })

        predicted_bookings = predict_model(dataframe)
        return redirect(url_for('result', predicted_bookings=predicted_bookings))

    return render_template('predict.html', today=today)

@app.route('/result', methods=['GET','POST'])
def result():
    if request.method == 'POST':
        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['day'])
        season = int(request.form['season'])
        day_of_week = int(request.form['day_of_week'])

    predicted_bookings = request.args.get('predicted_bookings')

    return render_template('result.html', predicted_bookings=predicted_bookings)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    reservations = current_user.reservations
    return render_template('dashboard.html', reservations=reservations)


@app.route('/make_reservation', methods=['GET', 'POST'])
@login_required
def make_reservation():
    today = date.today()
    if request.method == 'POST':
        check_in_date_str = request.form['check_in_date']
        check_out_date_str = request.form['check_out_date']
        num_guests = request.form['num_guests']
        if check_out_date_str < check_in_date_str:
            flash('Check out date must not be less then Check in date.', 'danger')
        else:


            # Convert date strings to date objects
            check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d').date()


            reservation = Reservation(
                user=current_user,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                num_guests=num_guests
            )

            db.session.add(reservation)
            db.session.commit()

            flash('Reservation successful', 'success')
            return redirect(url_for('dashboard'))

    return render_template('make_reservation.html', today=today)


migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
