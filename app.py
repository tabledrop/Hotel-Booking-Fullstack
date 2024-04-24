# imports for web service fullstack
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from datetime import datetime, timedelta
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
        selected_date1 = datetime.strptime(request.form['firstDate'], '%Y-%m-%d').date()
        selected_date2 = datetime.strptime(request.form['secondDate'], '%Y-%m-%d').date()

        date_range = [(selected_date1 + timedelta(days=i)).strftime("%A, %B %d") for i in range((selected_date2 - selected_date1).days + 1)]
        date_range = ' . '.join(date_range)
        #print(date_range)
        adults = int(request.form['adults'])

        # parse data from form to appropriate Pandas DataFrame
        selected_date_obj1 = selected_date1
        selected_date_obj2 = selected_date2

        dataframe = pd.DataFrame({
            'year': [0],
            'month': [0],
            'day': [0],
            'season': [0],
            'adults': [0],
            'day_of_week': [0]
            })

        i = 0
        while selected_date_obj1 != selected_date_obj2 + timedelta(days=1):
            year = selected_date_obj1.year
            month = selected_date_obj1.month
            day = selected_date_obj1.day
            weekday = selected_date_obj1.weekday()
            season = 0
            if month == 12 or month == 1 or month == 2:
                season = 3
            elif month == 3 or month == 4 or month == 5:
                season = 0
            elif month == 6 or month == 7 or month == 8:
                season = 1
            elif month == 9 or month == 10 or month == 11:
                season = 2

            dataframe.loc[i] = [year, month, day, season, adults, weekday]

            selected_date_obj1 += timedelta(days=1)
            i += 1

        predicted_bookings = predict_model(dataframe)
        return redirect(url_for('result', predicted_bookings=predicted_bookings, date_range=date_range))

    return render_template('predict.html', today=today)

@app.route('/result', methods=['GET','POST'])
def result():
    if request.method == 'POST':
       selected_date1 = request.form['firstDate']
       selected_date2 = request.form['secondDate']

    predicted_bookings = request.args.get('predicted_bookings')
    date_range = request.args.get('date_range')
    predicted_bookings_list = [int(booking) for booking in predicted_bookings.split()]

    return render_template('result.html', predicted_bookings=predicted_bookings_list, date_range=date_range)

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
