from flask import Blueprint, render_template
from flask_login import current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/dsa')
def dsa():
    return render_template('DSA/dsa.html', user=current_user)

@views.route('/data structures')
@views.route('/data-structures')
def data_structures():
    return render_template('DSA/data_structures.html', user=current_user)

@views.route('/algorithms')
def algorithms():
    return render_template('DSA/algorithms.html', user=current_user)

@views.route('/arrays')
def arrays():
    return render_template('Arrays/arrays.html', user=current_user)

@views.route('/2D arrays')
@views.route('/2d-arrays')
def _2Darrays():
    return render_template('Arrays/2Darrays.html', user=current_user)

@views.route('/searching algorithms')
@views.route('/searching-algorithms')
def searching_algorithms():
    return render_template('SearchingAlgorithms/searching_algorithms.html', user=current_user)

@views.route('/linear search')
@views.route('/linear-search')
def linear_search():
    return render_template('SearchingAlgorithms/linear_search.html', user=current_user)

@views.route('/binary search')
@views.route('/binary-search')
def binary_search():
    return render_template('SearchingAlgorithms/binary_search.html', user=current_user)

@views.route('/sorting algorithms')
@views.route('/sorting-algorithms')
def sorting_algorithms():
    return render_template('SortingAlgorithms/sorting_algorithms.html', user=current_user)

@views.route('/bubble sort')
@views.route('/bubble-sort')
def bubble_sort():
    return render_template('SortingAlgorithms/bubble_sort.html', user=current_user)

@views.route('/insertion sort')
@views.route('/insertion-sort')
def insertion_sort():
    return render_template('SortingAlgorithms/insertion_sort.html', user=current_user)

@views.route('/selection sort')
@views.route('/selection-sort')
def selection_sort():
    return render_template('SortingAlgorithms/selection_sort.html', user=current_user)

@views.route('/quick sort')
@views.route('/quick-sort')
def quick_sort():
    return render_template('SortingAlgorithms/quick_sort.html', user=current_user)

@views.route('/merge sort')
@views.route('/merge-sort')
def merge_sort():
    return render_template('SortingAlgorithms/merge_sort.html', user=current_user)

@views.route('/heap sort')
@views.route('/heap-sort')
def heap_sort():
    return render_template('SortingAlgorithms/heap_sort.html', user=current_user)

@views.route('/stack and queue')
@views.route('/stack-and-queue')
def stack_and_queue():
    return render_template('StackAndQueue/stack_and_queue.html', user=current_user)

@views.route('/stack')
def stack():
    return render_template('StackAndQueue/stack.html', user=current_user)

@views.route('/queue')
def queue():
    return render_template('StackAndQueue/queue.html', user=current_user)

@views.route('/linked list')
@views.route('/linked-list')
def linked_list():
    return render_template('LinkedList/linked_list.html', user=current_user)

@views.route('/singly linked list')
@views.route('/singly-linked-list')
def singly_linked_list():
    return render_template('LinkedList/singly_linked_list.html', user=current_user)

@views.route('/doubly linked list')
@views.route('/doubly-linked-list')
def doubly_linked_list():
    return render_template('LinkedList/doubly_linked_list.html', user=current_user)

@views.route('/rotation')
def rotation():
    return render_template('LinkedList/rotation.html', user=current_user)

@views.route('/types-of-trees')
def types_of_trees():
    return render_template('Trees/types_of_trees.html', user=current_user)

@views.route('/tree-traversals')
def tree_traversals():
    return render_template('Trees/tree_traversals.html', user=current_user)

@views.route('/tree-list-correlation')
def tree_list_correlation():
    return render_template('Trees/tree_list_correlation.html', user=current_user)

@views.route('/union-find')
def union_find():
    return render_template('Trees/union_find.html', user=current_user)

@views.route('/binary-search-tree')
def binary_search_tree():
    return render_template('Trees/binary_search_tree.html', user=current_user)

@views.route('/ternary-tree')
def ternary_tree():
    return render_template('Trees/ternary_tree.html', user=current_user)

@views.route('/types-of-heaps')
def types_of_heaps():
    return render_template('Trees/types_of_heaps.html', user=current_user)

@views.route('/avl-tree')
def avl_tree():
    return render_template('AVLTree/avl_tree.html', user=current_user)

@views.route('/b-tree')
def b_tree():
    return render_template('Trees/b_tree.html', user=current_user)

@views.route('/types-of-graphs')
def types_of_graphs():
    return render_template('Graphs/types_of_graphs.html', user=current_user)

@views.route('/graph-representation')
def graph_representation():
    return render_template('Graphs/graph_representation.html', user=current_user)

@views.route('/graph-traversals')
def graph_traversals():
    return render_template('Graphs/graph_traversals.html', user=current_user)

@views.route('/dijkstra-algorithm')
def dijkstra_algorithm():
    return render_template('Graphs/dijkstra_algorithm.html', user=current_user)

@views.route('/bellman-ford-algorithm')
def bellman_ford_algorithm():
    return render_template('Graphs/bellman_ford_algorithm.html', user=current_user)

@views.route('/floyd-warshall-algorithm')
def floyd_warshall_algorithm():
    return render_template('Graphs/floyd_warshall_algorithm.html', user=current_user)

@views.route('/prims-algorithm')
def prims_algorithm():
    return render_template('Graphs/prims_algorithm.html', user=current_user)

@views.route('/kruskal-algorithm')
def kruskal_algorithm():
    return render_template('Graphs/kruskal_algorithm.html', user=current_user)

@views.route('/topological-sort')
def topological_sort():
    return render_template('Graphs/topological_sort.html', user=current_user)

@views.route('/count-inversions')
def count_inversions():
    return render_template('DivideAndConquer/count_inversions.html', user=current_user)

@views.route('/closest-pair')
def closest_pair():
    return render_template('DivideAndConquer/closest_pair.html', user=current_user)

@views.route('/longest-common-subsequence')
def longest_common_subsequence():
    return render_template('DivideAndConquer/longest_common_subsequence.html', user=current_user)

@views.route('/median-of-medians')
def median_of_medians():
    return render_template('DivideAndConquer/median_of_medians.html', user=current_user)

@views.route('/interval-scheduling')
def interval_scheduling():
    return render_template('Greedy/interval_scheduling.html', user=current_user)

@views.route('/huffman-encoding')
def huffman_encoding():
    return render_template('Greedy/huffman_encoding.html', user=current_user)