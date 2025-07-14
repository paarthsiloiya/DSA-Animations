from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/dsa')
# @login_required
def dsa():
    return render_template('dsa.html', user=current_user)

@views.route('/data structures')
def data_structures():
    return render_template('data_structures.html', user=current_user)

@views.route('/algorithms')
def algorithms():
    return render_template('algorithms.html', user=current_user)

@views.route('/arrays')
def arrays():
    return render_template('arrays.html', user=current_user)

@views.route('/2D arrays')
def _2Darrays():
    return render_template('2Darrays.html', user=current_user)

@views.route('/searching algorithms')
def searching_algorithms():
    return render_template('searching_algorithms.html', user=current_user)

@views.route('/linear search')
def linear_search():
    return render_template('linear_search.html', user=current_user)

@views.route('/binary search')
def binary_search():
    return render_template('binary_search.html', user=current_user)