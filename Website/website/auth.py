from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<h1>Login Page</h1><p>Please enter your credentials to log in.</p>"

@auth.route('/signup')
def signup():
    return "<h1>Signup Page</h1><p>Create a new account by filling out the form below.</p>"

@auth.route('/logout')
def logout():
    return "<h1>Logout Page</h1><p>You have been logged out successfully.</p>"