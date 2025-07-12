from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/dsa')
# @login_required
def content():
    return render_template('dsa.html', user=current_user)

@views.route('/Data Structures')
def data_structures():
    return render_template('data_structures.html', user=current_user)

@views.route('/Algorithms')
def algorithms():
    return render_template('algorithms.html', user=current_user)

@views.route('/Searching Algorithms')
def searching_algorithms():
    return render_template('searching_algorithms.html', user=current_user)

@views.route('/Linear Search')
def linear_search():
    return render_template('linear_search.html', user=current_user)