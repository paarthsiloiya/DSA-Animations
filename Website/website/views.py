from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/dsa')
def dsa():
    return render_template('DSA/dsa.html', user=current_user)

@views.route('/data structures')
def data_structures():
    return render_template('DSA/data_structures.html', user=current_user)

@views.route('/algorithms')
def algorithms():
    return render_template('DSA/algorithms.html', user=current_user)

@views.route('/arrays')
def arrays():
    return render_template('Arrays/arrays.html', user=current_user)

@views.route('/2D arrays')
def _2Darrays():
    return render_template('Arrays/2Darrays.html', user=current_user)

@views.route('/searching algorithms')
def searching_algorithms():
    return render_template('SearchingAlgorithms/searching_algorithms.html', user=current_user)

@views.route('/linear search')
def linear_search():
    return render_template('SearchingAlgorithms/linear_search.html', user=current_user)

@views.route('/binary search')
def binary_search():
    return render_template('SearchingAlgorithms/binary_search.html', user=current_user)

@views.route('/sorting algorithms')
def sorting_algorithms():
    return render_template('SortingAlgorithms/sorting_algorithms.html', user=current_user)

@views.route('/bubble sort')
def bubble_sort():
    return render_template('SortingAlgorithms/bubble_sort.html', user=current_user)

@views.route('/insertion sort')
def insertion_sort():
    return render_template('SortingAlgorithms/insertion_sort.html', user=current_user)