from flask import Flask, render_template

app= Flask(__name__)

@app.route('/')
def home():
    return render_template('home_screen.html')
@app.route('/go_premium')
def go_premium():
    return render_template('go_premium.html')
@app.route('/login_screen')
def login():
    return render_template('login_screen.html')
@app.route('/register_screen')
def register():
    return render_template('register_screen.html')
@app.route('/forgotpass')
def forgotpass():
    return render_template('forgot_password.html')

if __name__ == '__main__':
    app.run()