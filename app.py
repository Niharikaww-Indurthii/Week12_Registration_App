from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('myForm.html')


@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username', '').strip()
    password = request.form.get('pwd', '')

    # Server-side checks complement the browser-side Selenium-tested validation.
    if not username:
        return render_template('myForm.html', error='Username cannot be empty.'), 400
    if not password:
        return render_template('myForm.html', error='Password cannot be empty.'), 400
    if len(password) < 6 or not any(ch.isdigit() for ch in password) or not any(ch.isalpha() for ch in password):
        return render_template('myForm.html', error='Password must be at least 6 characters long and contain a letter and a number.'), 400

    return render_template('greeting.html', name=username)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
