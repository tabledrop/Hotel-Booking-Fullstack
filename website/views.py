from flask import Blueprint, render_template
from flask import request


views = Blueprint('views', __name__)

# 127.0.0.1:5000/rooms url
@views.route('/rooms')
def rooms():
    return render_template('rooms.html')

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/book')
def book():
    return render_template('book.html')

@views.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    name = request.form.get('name')
    email = request.form.get('email')
    check_in_date = request.form.get('check_in_date')
    nights = request.form.get('nights')
    # Here you can process the form data, for example, by saving it to a database
    # Then, you can render a confirmation page
    return render_template('confirmation.html', name=name, email=email, check_in_date=check_in_date, nights=nights)