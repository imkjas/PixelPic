from flask import Flask, render_template, request, redirect, url_for,session
import pyrebase
from requests.exceptions import HTTPError

firebaseConfig={
    'apiKey': "AIzaSyAU64526sGBB8ZP-M7mgocQkSbyAFJ3klM",
    'authDomain': "pixelpix-4dbb5.firebaseapp.com",
    'databaseURL': "https://pixelpix-4dbb5-default-rtdb.firebaseio.com",
    'projectId': "pixelpix-4dbb5",
    'storageBucket': "pixelpix-4dbb5.appspot.com",
    'messagingSenderId': "574563555513",
    'appId': "1:574563555513:web:333039f782b9e0b87aa368",
    'measurementId': "G-XD1HMR66RR"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def check_user_logged_in():
    if 'user_id' in session:
        return True
    else:
        return False


@app.route('/')
def home():
    user_logged_in = check_user_logged_in()

    return render_template('home_screen.html', user_logged_in=user_logged_in)


@app.route('/go_premium')
def go_premium():
    user_logged_in = check_user_logged_in() 

    return render_template('go_premium.html', user_logged_in=user_logged_in)


@app.route('/login_screen', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            login = auth.sign_in_with_email_and_password(email, password)
            session['user_id'] = login['idToken']
            return redirect(url_for('home'))
        except:
            error_message = "Invalid email or password"
            return render_template('login_screen.html', error_message=error_message)

    return render_template('login_screen.html')


@app.route('/register_screen', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        if len(password) < 6:
            error_message = 'Password should be at least 6 characters.'
            return render_template('register_screen.html', error_message=error_message)

        if not username or not first_name or not last_name:
            error_message = 'Please fill in all the required fields.'
            return render_template('register_screen.html', error_message=error_message)

        try:
            user = auth.create_user_with_email_and_password(email, password)
            return render_template('login_screen.html')
        except HTTPError as e:
            if e.response is not None and e.response.content:
                error_message = e.response.json()['error']['message']
            else:
                error_message = 'An error occurred during registration.'
            return render_template('register_screen.html', error_message=error_message)

    return render_template('register_screen.html')


@app.route('/forgotpass')
def forgotpass():
    return render_template('forgot_password.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()