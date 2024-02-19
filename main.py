from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


'''new code'''


@app.route('/book')
def book():
    return render_template('book.html')


@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    name = request.form.get('name')
    email = request.form.get('email')
    check_in_date = request.form.get('check_in_date')
    nights = request.form.get('nights')
    # Here you can process the form data, for example, by saving it to a database
    # Then, you can render a confirmation page
    return render_template('confirmation.html', name=name, email=email, check_in_date=check_in_date, nights=nights)


''' '''

if __name__ == '__main__':
    app.run(debug=True)
