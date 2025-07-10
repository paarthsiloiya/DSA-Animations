from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        subscribed = request.form.get('subscribe') == 'on'

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(username) < 3:
            flash('Username must be at least 3 characters long.', category='error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password), subscribed=subscribed)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created successfully!', category='success')

            return redirect(url_for('views.home'))
            # print(f"Email: {email}, Username: {username}, Subscribed: {subscribed}")

    return render_template('signup.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))