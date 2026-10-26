import random
from typing import ClassVar

import networkx as nx
from common import Node, animate_traversal, play_surrounding_node_animation, remove_edge_visual
from env_config import *
from manim import *
from synced import SyncedScene

random.seed(32)

# Override specific font sizes for Trees
EXPLANATORY_FONT_SIZE = 30  # For step-by-step explanations
POINTER_FONT_SIZE = 20      # For pointer labels (if any)


class TreeExplanation(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "class Node:",
        "    def __init__(self, data):",
        "        self.data = data",
        "        self.children = []     # one node, many children",
        "",
        "root = Node(\"A\")             # the root: the node with no parent",
        "",
        "def add_child(parent, data):",
        "    child = Node(data)",
        "    parent.children.append(child)   # the parent -> child edge",
        "    return child",
        "",
        "b = add_child(root, \"B\")     # B and C are the root's children",
        "c = add_child(root, \"C\")",
        "add_child(b, \"D\")            # D is a child of B",
        "add_child(c, \"F\")            # F, G, H are C's children: siblings",
        "add_child(c, \"L\")            # insert: grow the tree anywhere",
        "",
        "# delete: removing a node detaches its whole subtree",
        "root.children.remove(b)      # ...and one tree becomes a forest",
    ]

    def construct(self):
        G = nx.Graph()

        for i in range(11):
            G.add_node(chr(65 + i))  # Adding nodes A, B, C, ..., K

        G.add_edges_from([
            ("A", "B"), ("A", "C"),
            ("B", "D"), ("B", "E"),
            ("C", "F"), ("C", "G"), ("C", "H"),
            ("D", "I"), ("D", "J"),
            ("E", "K")
        ])
        
        tree = Graph(
                    vertices=list(G.nodes), 
                    edges=list(G.edges), 
                    vertex_mobjects={v : Node(v) for v in list(G.nodes)},
                    edge_config={"stroke_color": EDGE_COL, "stroke_width": 6},
                    layout="tree", 
                    layout_scale=4,
                    root_vertex="A"
                )

        self.code_step("declare")
        self.play(Create(tree),run_time=6)

        self.wait(2)

        self.code_step("node")
        play_surrounding_node_animation(self, tree, "B", "Node", UP)
        self.wait(0.5)
        self.code_step("root")
        play_surrounding_node_animation(self, tree, "A", "Root Node", UP)
        self.wait(0.5)
        self.code_step("parent")
        play_surrounding_node_animation(self, tree, "D", "Parent\nNode", RIGHT)
        self.code_step("child")
        play_surrounding_node_animation(self, tree, "I", "Child\nNode", RIGHT)
        self.wait(0.5)

        self.code_step("siblings")
        self.play(
            tree.vertices["F"].Select(), 
            tree.vertices["G"].Select(), 
            tree.vertices["H"].Select(), 
            run_time=0.5
        )
        nodeSurr = DashedVMobject(SurroundingRectangle(tree.vertices["F"], tree.vertices["G"], tree.vertices["H"], color=TEXTCOL, buff=0.15, corner_radius=0.6), num_dashes=35)
        nodeText = Text("Siblings", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, DOWN, buff=0.1)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(
            tree.vertices["F"].Clear(),
            tree.vertices["G"].Clear(),
            tree.vertices["H"].Clear(),
            Uncreate(nodeSurr), 
            Unwrite(nodeText), 
            run_time=0.5, lag_ratio=0.1
        )


        self.wait(0.5)
        
        self.code_step("subtree")
        self.play(
            tree.vertices["D"].Select(), 
            tree.vertices["I"].Select(), 
            tree.vertices["J"].Select(), 
            run_time=0.5
        )
        nodeSurr = DashedVMobject(SurroundingRectangle(tree.vertices["D"], tree.vertices["I"], tree.vertices["J"], color=TEXTCOL, buff=0.15, corner_radius=0.6), num_dashes=35)
        nodeText = Text("Subtree", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, DOWN, buff=0.1)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(
            tree.vertices["D"].Clear(),
            tree.vertices["I"].Clear(),
            tree.vertices["J"].Clear(),
            Uncreate(nodeSurr), 
            Unwrite(nodeText), 
            run_time=0.5, lag_ratio=0.1
        )

        self.wait(0.5)

        self.code_step("leaf")
        self.play(
            tree.vertices["K"].Select(), 
            tree.vertices["I"].Select(), 
            tree.vertices["J"].Select(), 
            tree.vertices["H"].Select(), 
            tree.vertices["G"].Select(), 
            tree.vertices["F"].Select(), 
            run_time=0.5
        )
        nodeSurr = VGroup(
            DashedVMobject(SurroundingRectangle(tree.vertices["K"], tree.vertices["I"], tree.vertices["J"], color=TEXTCOL, buff=0.15, corner_radius=0.6), num_dashes=35),
            DashedVMobject(SurroundingRectangle(tree.vertices["H"], tree.vertices["G"], tree.vertices["F"], color=TEXTCOL, buff=0.15, corner_radius=0.6), num_dashes=35)
        )
        nodeText = Text("Leaf Nodes", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(tree.vertices["K"], LEFT, buff=1)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(
            tree.vertices["K"].Clear(),
            tree.vertices["I"].Clear(),
            tree.vertices["J"].Clear(),
            tree.vertices["H"].Clear(),
            tree.vertices["G"].Clear(),
            tree.vertices["F"].Clear(),
            Uncreate(nodeSurr), 
            Unwrite(nodeText), 
            run_time=0.5, lag_ratio=0.1
        )

        self.wait(1)

        # Add new node L connected to G
        operation_text = Text("Inserting Node", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.2)
        self.play(Write(operation_text), run_time=0.5)

        new_node = "L"
        new_edge = ("G", new_node)

        # Add to underlying graph structure
        G.add_node(new_node)
        G.add_edge(*new_edge)

        # Add vertex and edge to tree
        new_pos = tree.vertices["G"].get_center() + DOWN * 1.5
        new_vertex = Node(new_node)
        
        tree._add_vertex(new_node, vertex_mobject=new_vertex, position=new_pos)
        self.code_step("insert")
        self.play(Create(tree.vertices[new_node]))
        self.wait(0.5)
        tree._add_edge(("G", new_node))
        self.play(Create(tree.edges[("G", new_node)]))
        self.wait(0.5)
        self.play(Unwrite(operation_text), run_time=0.5)

        self.wait(1)

        operation_text = Text("Deleting Node", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.2)
        self.play(Write(operation_text), run_time=0.5)

        del_node = "K"
        self.code_step("delete")
        self.play(FadeOut(tree.edges[("E", del_node)]))
        tree._remove_edge(("E", del_node))
        G.remove_edge("E", del_node)
        self.play(FadeOut(tree.vertices[del_node]))
        tree._remove_vertex(del_node)
        G.remove_node(del_node)

        self.wait(0.5)
        self.play(Unwrite(operation_text), run_time=0.5)

        self.wait(1.5)

        #Creating Forest
        operation_text = Text("FOREST", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.2)
        self.play(Write(operation_text), run_time=0.5)

        self.code_step("forest")
        self.play(FadeOut(tree.edges[("A", "B")]))
        tree._remove_edge(("A", "B"))
        G.remove_edge("A", "B")

        components = list(nx.connected_components(G))

        for i, component in enumerate(components):
            sub_nodes = [tree.vertices[v] for v in component]

            surr_rect = DashedVMobject(
                SurroundingRectangle(VGroup(*sub_nodes), color=TEXTCOL, buff=0.2, corner_radius=0.6),
                num_dashes=50
            )

            label = Text(f"Tree {i + 1}", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(surr_rect, UP, buff=0.2)

            self.play(Create(surr_rect), run_time=1)
            self.play(Write(label), run_time=0.5)
            self.wait(1)
            self.play(Uncreate(surr_rect), Unwrite(label), run_time=0.5)
            self.wait(0.2)

        self.wait(2)


class TreeBFS(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "from collections import deque",
        "",
        "# demo tree: A-(B, C), B-(D, E), C-(F, G, H), D-(I, J), E-(K)",
        "root = build_tree()",
        "",
        "def bfs(root):",
        "    order = []",
        "    queue = deque([root])       # FIFO: the oldest node leaves first",
        "    while queue:",
        "        current = queue.popleft()",
        "        order.append(current.data)   # visit",
        "        for child in current.children:",
        "            queue.append(child)      # discoveries join at the rear",
        "    return order",
        "",
        "bfs(root)   # A B C D E F G H I J K",
    ]

    def construct(self):
        G = nx.Graph()

        for i in range(11):
            G.add_node(chr(65 + i))  # Adding nodes A, B, C, ..., K

        G.add_edges_from([
            ("A", "B"), ("A", "C"),
            ("B", "D"), ("B", "E"),
            ("C", "F"), ("C", "G"), ("C", "H"),
            ("D", "I"), ("D", "J"),
            ("E", "K")
        ])
        
        tree = Graph(
                    vertices=list(G.nodes), 
                    edges=list(G.edges)[::-1], 
                    vertex_mobjects={v : Node(v) for v in list(G.nodes)},
                    edge_config={"stroke_color": EDGE_COL, "stroke_width": 6},
                    layout="tree", 
                    layout_scale=4,
                    root_vertex="A"
                )

        tree.to_edge(LEFT, buff=1.2)
        self.code_step("declare")
        self.play(Create(tree), run_time=2)
        self.wait(1)

        # Build adjacency list for tree traversal
        adjacencyList = {v: [] for v in G.nodes}
        for u, v in G.edges:
            adjacencyList[u].append(v)
            adjacencyList[v].append(u)

        s = "A"

        # Show starting node selection
        start_text = Text(f"Starting from node {s}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).to_edge(RIGHT, buff=1.2)
        self.play(Write(start_text), run_time=1)
        self.wait(1)

        def bfs_neighbors(v):
            self.code_step("visit")
            return sorted(adjacencyList[v])

        def bfs_on_visit(current, neighbor):
            self.code_step("discover")

        animate_traversal(self, tree, adjacencyList, s, start_text,
                          explanatory_font_size=EXPLANATORY_FONT_SIZE,
                          neighbors_of=bfs_neighbors,
                          on_visit=bfs_on_visit)


class TreeDFS(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "# demo tree: A-(B, C), B-(D, E), C-(F, G, H), D-(I, J), E-(K)",
        "root = build_tree()",
        "",
        "def dfs(root):",
        "    order = []",
        "    stack = [root]             # LIFO: the newest node leaves first",
        "    while stack:",
        "        current = stack.pop()",
        "        order.append(current.data)   # visit",
        "        for child in reversed(current.children):",
        "            stack.append(child)",
        "    return order",
        "",
        "dfs(root)   # A B D I J E K C F G H",
    ]

    def construct(self):
        G = nx.Graph()

        for i in range(11):
            G.add_node(chr(65 + i))  # Adding nodes A, B, C, ..., K

        G.add_edges_from([
            ("A", "B"), ("A", "C"),
            ("B", "D"), ("B", "E"),
            ("C", "F"), ("C", "G"), ("C", "H"),
            ("D", "I"), ("D", "J"),
            ("E", "K")
        ])
        
        tree = Graph(
                    vertices=list(G.nodes), 
                    edges=list(G.edges)[::-1], 
                    vertex_mobjects={v : Node(v) for v in list(G.nodes)},
                    edge_config={"stroke_color": EDGE_COL, "stroke_width": 6},
                    layout="tree", 
                    layout_scale=4,
                    root_vertex="A"
                )

        tree.to_edge(LEFT, buff=1.2)
        self.code_step("declare")
        self.play(Create(tree), run_time=2)
        self.wait(1)

        # Build adjacency list for tree traversal
        adjacencyList = {v: [] for v in G.nodes}
        for u, v in G.edges:
            adjacencyList[u].append(v)
            adjacencyList[v].append(u)

        s = "A"

        # Show starting node selection
        start_text = Text(f"Starting from node {s}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).to_edge(RIGHT, buff=1.2)
        self.play(Write(start_text), run_time=1)
        self.wait(1)

        def dfs_neighbors(v):
            self.code_step("visit")
            return sorted(adjacencyList[v], reverse=True)

        def dfs_on_visit(current, neighbor):
            self.code_step("discover")

        animate_traversal(self, tree, adjacencyList, s, start_text,
                          use_stack=True,
                          explanatory_font_size=EXPLANATORY_FONT_SIZE,
                          neighbors_of=dfs_neighbors,
                          on_visit=dfs_on_visit)


class InOrderTraversal(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "# demo tree: A-(B, C), B-(D, E), D-(H, I), C-(F, G), E-(J)",
        "",
        "def inorder(node):",
        "    if node is None:",
        "        return",
        "    inorder(node.left)      # 1. the left subtree",
        "    visit(node)             # 2. the root",
        "    inorder(node.right)     # 3. the right subtree",
        "",
        "inorder(root)   # H D I B J E A F C G",
    ]

    def construct(self):
        G = nx.Graph()

        for i in range(10):
            G.add_node(chr(65 + i))  # Adding nodes A, B, C, ..., J

        G.add_edges_from([
            ("A", "B"), ("A", "C"),
            ("B", "D"), ("B", "E"),
            ("C", "F"), ("C", "G"),
            ("D", "H"), ("D", "I"),
            ("E", "J")
        ])
        
        tree = Graph(
                    vertices=list(G.nodes), 
                    edges=list(G.edges)[::-1], 
                    vertex_mobjects={v : Node(v) for v in list(G.nodes)},
                    edge_config={"stroke_color": EDGE_COL, "stroke_width": 6},
                    layout="tree", 
                    layout_scale=4,
                    root_vertex="A"
                )

        tree.to_edge(LEFT, buff=1.2)
        self.code_step("declare")
        self.play(Create(tree), run_time=2)
        self.wait(1)

        # Build adjacency list for tree traversal
        adjacencyList = {v: [] for v in G.nodes}
        for u, v in G.edges:
            adjacencyList[u].append(v)
            adjacencyList[v].append(u)

        # Show starting explanation
        start_text = Text("In-Order Traversal: Left → Root → Right", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.3)
        self.code_step("title")
        self.play(Write(start_text), run_time=1)
        self.wait(1)

        # Initialize empty order display
        visited_order = []
        order_text = Text("Order: ", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.3)
        self.code_step("call")
        self.play(Unwrite(start_text), Write(order_text), run_time=1)
        self.wait(1)

        def inorder_recursive(node, parent, visited_order):
            nonlocal order_text
            
            children = [child for child in sorted(adjacencyList[node]) if child != parent]
            
            # Go to left subtree first
            if len(children) > 0:
                left_child = children[0]

                # Show movement to left child
                move_text = Text(f"Going to left subtree: {left_child}",
                               font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(tree, RIGHT, buff=0).shift(LEFT)
                self.code_step("left")
                self.play(Write(move_text), run_time=0.5)

                # Highlight the path
                self.play(
                    tree.vertices[node].Select(),
                    tree.edges[(node, left_child)].animate.set_stroke(color=BLUE, width=8),
                    run_time=0.5
                )

                self.play(Unwrite(move_text), run_time=0.3)
                self.wait(0.3)

                # Recursively traverse left subtree
                inorder_recursive(left_child, node, visited_order)

                # Reset edge color after traversal
                self.play(tree.edges[(node, left_child)].animate.set_stroke(color=EDGE_COL, width=6), run_time=0.3)

            # Process current node (Root)
            processing_text = Text(f"Processing node {node}",
                                 font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(tree, RIGHT, buff=0.3)
            self.code_step("visit")
            self.play(Write(processing_text), run_time=0.5)
            
            # Highlight current node
            self.play(tree.vertices[node].Highlight(), run_time=0.5)
            self.wait(0.5)
            
            # Add to visited order and update display
            visited_order.append(node)
            new_order_text = Text(f"Order: {' → '.join(visited_order)}", 
                                 font=FONT, color=TEXTCOL, font_size=FSIZE).move_to(order_text)
            self.play(ReplacementTransform(order_text, new_order_text), run_time=0.5)
            order_text = new_order_text
            
            position_text = Text(f"Added {node} at position {len(visited_order)}", 
                               font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE-4).next_to(processing_text, DOWN, buff=0.5)
            self.play(Write(position_text), run_time=0.3)
            self.wait(0.8)
            
            self.play(Unwrite(processing_text), Unwrite(position_text), run_time=0.3)
            
            # Go to right subtree
            if len(children) > 1:
                right_child = children[1]

                # Show movement to right child
                move_text = Text(f"Going to right subtree: {right_child}",
                                font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(tree, RIGHT, buff=0).shift(LEFT)
                self.code_step("right")
                self.play(Write(move_text), run_time=0.5)

                # Highlight the path
                self.play(
                    tree.vertices[node].Select(),
                    tree.edges[(node, right_child)].animate.set_stroke(color=GREEN, width=8),
                    run_time=0.5
                )

                self.play(Unwrite(move_text), run_time=0.3)
                self.wait(0.3)

                # Recursively traverse right subtree
                inorder_recursive(right_child, node, visited_order)

                # Reset edge color after traversal
                self.play(tree.edges[(node, right_child)].animate.set_stroke(color=EDGE_COL, width=6), run_time=0.3)

        # Start the animated traversal
        inorder_recursive("A", None, visited_order)
        self.play(Unwrite(order_text), run_time=1.5)
        self.wait(2)


class PreOrderTraversal(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "# demo tree: A-(B, C), B-(D, E), D-(H, I), C-(F, G), E-(J)",
        "",
        "def preorder(node):",
        "    if node is None:",
        "        return",
        "    visit(node)             # 1. the root first",
        "    preorder(node.left)     # 2. then the left subtree",
        "    preorder(node.right)    # 3. then the right subtree",
        "",
        "preorder(root)   # A B D H I E J C F G",
    ]

    def construct(self):
        G = nx.Graph()

        for i in range(10):
            G.add_node(chr(65 + i))  # Adding nodes A, B, C, ..., J

        G.add_edges_from([
            ("A", "B"), ("A", "C"),
            ("B", "D"), ("B", "E"),
            ("C", "F"), ("C", "G"),
            ("D", "H"), ("D", "I"),
            ("E", "J")
        ])
        
        tree = Graph(
                    vertices=list(G.nodes), 
                    edges=list(G.edges)[::-1], 
                    vertex_mobjects={v : Node(v) for v in list(G.nodes)},
                    edge_config={"stroke_color": EDGE_COL, "stroke_width": 6},
                    layout="tree", 
                    layout_scale=4,
                    root_vertex="A"
                )

        tree.to_edge(LEFT, buff=1.2)
        self.code_step("declare")
        self.play(Create(tree), run_time=2)
        self.wait(1)

        # Build adjacency list for tree traversal
        adjacencyList = {v: [] for v in G.nodes}
        for u, v in G.edges:
            adjacencyList[u].append(v)
            adjacencyList[v].append(u)

        # Show starting explanation
        start_text = Text("Pre-Order Traversal: Root → Left → Right", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.3)
        self.code_step("title")
        self.play(Write(start_text), run_time=1)
        self.wait(1)

        # Initialize empty order display
        visited_order = []
        order_text = Text("Order: ", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.3)
        self.code_step("call")
        self.play(Unwrite(start_text), Write(order_text), run_time=1)
        self.wait(1)

        def preorder_recursive(node, parent, visited_order):
            nonlocal order_text

            children = [child for child in sorted(adjacencyList[node]) if child != parent]

            # Process current node first (Root)
            processing_text = Text(f"Processing node {node}",
                                 font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(tree, RIGHT, buff=0.3)
            self.code_step("visit")
            self.play(Write(processing_text), run_time=0.5)
            
            # Highlight current node
            self.play(tree.vertices[node].Highlight(), run_time=0.5)
            self.wait(0.5)
            
            # Add to visited order and update display
            visited_order.append(node)
            new_order_text = Text(f"Order: {' → '.join(visited_order)}", 
                                 font=FONT, color=TEXTCOL, font_size=FSIZE).move_to(order_text)
            self.play(ReplacementTransform(order_text, new_order_text), run_time=0.5)
            order_text = new_order_text
            
            position_text = Text(f"Added {node} at position {len(visited_order)}", 
                               font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE-4).next_to(processing_text, DOWN, buff=0.5)
            self.play(Write(position_text), run_time=0.3)
            self.wait(0.8)
            
            self.play(Unwrite(processing_text), Unwrite(position_text), run_time=0.3)
            
            # Go to left subtree
            if len(children) > 0:
                left_child = children[0]

                # Show movement to left child
                move_text = Text(f"Going to left subtree: {left_child}",
                               font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(tree, RIGHT, buff=0).shift(LEFT)
                self.code_step("left")
                self.play(Write(move_text), run_time=0.5)

                # Highlight the path
                self.play(
                    tree.vertices[node].Select(),
                    tree.edges[(node, left_child)].animate.set_stroke(color=BLUE, width=8),
                    run_time=0.5
                )

                self.play(Unwrite(move_text), run_time=0.3)
                self.wait(0.3)

                # Recursively traverse left subtree
                preorder_recursive(left_child, node, visited_order)

                # Reset edge color after traversal
                self.play(tree.edges[(node, left_child)].animate.set_stroke(color=EDGE_COL, width=6), run_time=0.3)

            # Go to right subtree
            if len(children) > 1:
                right_child = children[1]

                # Show movement to right child
                move_text = Text(f"Going to right subtree: {right_child}",
                                font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(tree, RIGHT, buff=0).shift(LEFT)
                self.code_step("right")
                self.play(Write(move_text), run_time=0.5)

                # Highlight the path
                self.play(
                    tree.vertices[node].Select(),
                    tree.edges[(node, right_child)].animate.set_stroke(color=GREEN, width=8),
                    run_time=0.5
                )

                self.play(Unwrite(move_text), run_time=0.3)
                self.wait(0.3)

                # Recursively traverse right subtree
                preorder_recursive(right_child, node, visited_order)

                # Reset edge color after traversal
                self.play(tree.edges[(node, right_child)].animate.set_stroke(color=EDGE_COL, width=6), run_time=0.3)

        # Start the animated traversal
        preorder_recursive("A", None, visited_order)
        self.play(Unwrite(order_text), run_time=1.5)
        self.wait(2)


class PostOrderTraversal(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "# demo tree: A-(B, C), B-(D, E), D-(H, I), C-(F, G), E-(J)",
        "",
        "def postorder(node):",
        "    if node is None:",
        "        return",
        "    postorder(node.left)     # 1. the left subtree",
        "    postorder(node.right)    # 2. the right subtree",
        "    visit(node)              # 3. the root last",
        "",
        "postorder(root)   # H I D J E B F G C A",
    ]

    def construct(self):
        G = nx.Graph()

        for i in range(10):
            G.add_node(chr(65 + i))  # Adding nodes A, B, C, ..., J

        G.add_edges_from([
            ("A", "B"), ("A", "C"),
            ("B", "D"), ("B", "E"),
            ("C", "F"), ("C", "G"),
            ("D", "H"), ("D", "I"),
            ("E", "J")
        ])
        
        tree = Graph(
                    vertices=list(G.nodes), 
                    edges=list(G.edges)[::-1], 
                    vertex_mobjects={v : Node(v) for v in list(G.nodes)},
                    edge_config={"stroke_color": EDGE_COL, "stroke_width": 6},
                    layout="tree", 
                    layout_scale=4,
                    root_vertex="A"
                )

        tree.to_edge(LEFT, buff=1.2)
        self.code_step("declare")
        self.play(Create(tree), run_time=2)
        self.wait(1)

        # Build adjacency list for tree traversal
        adjacencyList = {v: [] for v in G.nodes}
        for u, v in G.edges:
            adjacencyList[u].append(v)
            adjacencyList[v].append(u)

        # Show starting explanation
        start_text = Text("Post-Order Traversal: Left → Right → Root", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.3)
        self.code_step("title")
        self.play(Write(start_text), run_time=1)
        self.wait(1)

        # Initialize empty order display
        visited_order = []
        order_text = Text("Order: ", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.3)
        self.code_step("call")
        self.play(Unwrite(start_text), Write(order_text), run_time=1)
        self.wait(1)

        def postorder_recursive(node, parent, visited_order):
            nonlocal order_text

            children = [child for child in sorted(adjacencyList[node]) if child != parent]

            # Go to left subtree first
            if len(children) > 0:
                left_child = children[0]

                # Show movement to left child
                move_text = Text(f"Going to left subtree: {left_child}",
                               font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(tree, RIGHT, buff=0).shift(LEFT)
                self.code_step("left")
                self.play(Write(move_text), run_time=0.5)

                # Highlight the path
                self.play(
                    tree.vertices[node].Select(),
                    tree.edges[(node, left_child)].animate.set_stroke(color=BLUE, width=8),
                    run_time=0.5
                )

                self.play(Unwrite(move_text), run_time=0.3)
                self.wait(0.3)

                # Recursively traverse left subtree
                postorder_recursive(left_child, node, visited_order)

                # Reset edge color after traversal
                self.play(tree.edges[(node, left_child)].animate.set_stroke(color=EDGE_COL, width=6), run_time=0.3)

            # Go to right subtree
            if len(children) > 1:
                right_child = children[1]

                # Show movement to right child
                move_text = Text(f"Going to right subtree: {right_child}",
                                font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(tree, RIGHT, buff=0).shift(LEFT)
                self.code_step("right")
                self.play(Write(move_text), run_time=0.5)

                # Highlight the path
                self.play(
                    tree.vertices[node].Select(),
                    tree.edges[(node, right_child)].animate.set_stroke(color=GREEN, width=8),
                    run_time=0.5
                )

                self.play(Unwrite(move_text), run_time=0.3)
                self.wait(0.3)

                # Recursively traverse right subtree
                postorder_recursive(right_child, node, visited_order)

                # Reset edge color after traversal
                self.play(tree.edges[(node, right_child)].animate.set_stroke(color=EDGE_COL, width=6), run_time=0.3)

            # Process current node last (Root)
            processing_text = Text(f"Processing node {node}",
                                 font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(tree, RIGHT, buff=0.3)
            self.code_step("visit")
            self.play(Write(processing_text), run_time=0.5)
            
            # Highlight current node
            self.play(tree.vertices[node].Highlight(), run_time=0.5)
            self.wait(0.5)
            
            # Add to visited order and update display
            visited_order.append(node)
            new_order_text = Text(f"Order: {' → '.join(visited_order)}", 
                                 font=FONT, color=TEXTCOL, font_size=FSIZE).move_to(order_text)
            self.play(ReplacementTransform(order_text, new_order_text), run_time=0.5)
            order_text = new_order_text
            
            position_text = Text(f"Added {node} at position {len(visited_order)}", 
                               font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE-4).next_to(processing_text, DOWN, buff=0.5)
            self.play(Write(position_text), run_time=0.3)
            self.wait(0.8)
            
            self.play(Unwrite(processing_text), Unwrite(position_text), run_time=0.3)

        # Start the animated traversal
        postorder_recursive("A", None, visited_order)
        self.play(Unwrite(order_text), run_time=1.5)
        self.wait(2)


class BinaryTreeExplanation(Scene):
    def construct(self):
        def build_binary_tree(labels):
            G = nx.Graph()
            n = len(labels)
            G.add_nodes_from(labels)

            for i in range(n):
                left = 2 * i + 1
                right = 2 * i + 2
                if left < n:
                    G.add_edge(labels[i], labels[left])
                if right < n:
                    G.add_edge(labels[i], labels[right])

            return G
        

        def highlight_subtree(tree, root, text="Subtree", color=WHITE, font="Arial", fsize=24):
            # Recursively collect all nodes in subtree
            def collect_subtree_nodes(node, edges, visited):
                visited.add(node)
                for child in [v for u, v in edges if u == node]:
                    if child not in visited:
                        collect_subtree_nodes(child, edges, visited)
                return visited

            # Gather subtree nodes starting from root
            edges = [(str(u), str(v)) for u, v in tree.edges]
            subtree_nodes = sorted(collect_subtree_nodes(root, edges, set()))

            # 1. Highlight nodes
            self.play(*[tree.vertices[n].Select() for n in subtree_nodes], run_time=0.5)

            # 2. Create dashed surround box and label
            surround = SurroundingRectangle(*[tree.vertices[n] for n in subtree_nodes], color=color, buff=0.15, corner_radius=0.6)
            nodeSurr = DashedVMobject(surround, num_dashes=35)
            nodeText = Text(text, font=font, color=color, font_size=fsize).next_to(nodeSurr, DOWN, buff=0.1)
            self.play(Create(nodeSurr), run_time=0.5)
            self.wait(0.2)
            self.play(Write(nodeText), run_time=0.5)
            self.wait(1.5)

            # 3. Clear and uncreate
            self.play(
                *[tree.vertices[n].Clear() for n in subtree_nodes],
                Uncreate(nodeSurr),
                Unwrite(nodeText),
                run_time=0.5, lag_ratio=0.1
            )



        labels = [chr(65 + i) for i in range(11)]
        G = build_binary_tree(labels)
        
        tree = Graph(
                    vertices=list(G.nodes), 
                    edges=list(G.edges), 
                    vertex_mobjects={v : Node(v) for v in list(G.nodes)},
                    edge_config={"stroke_color": EDGE_COL, "stroke_width": 6},
                    layout="tree", 
                    layout_scale=4,
                    root_vertex="A"
                )

        self.play(Create(tree),run_time=6)

        self.wait(2)

        play_surrounding_node_animation(self, tree, "B", "Node", UR)
        self.wait(0.5)
        play_surrounding_node_animation(self, tree, "A", "Root Node", UP)
        self.wait(0.7)

        for root in ["B", "D", "E", "C", "G", "F"]:  # or automate this via non-leaf detection
            highlight_subtree(tree, root, text="Subtree", color=TEXTCOL, font=FONT, fsize=FSIZE)
            self.wait(0.2)
        
        self.wait(2)


class TernaryTreeExplanation(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "# a ternary tree: every node holds at most three children",
        "",
        "class Node:",
        "    def __init__(self, data):",
        "        self.data = data",
        "        self.children = []     # up to three children",
        "",
        "# complete ternary tree on 11 nodes, stored as a flat list",
        "tree = [\"A\", \"B\", \"C\", \"D\", \"E\", \"F\", \"G\", \"H\", \"I\", \"J\", \"K\"]",
        "",
        "# node i's children sit at index 3*i + 1, 3*i + 2 and 3*i + 3",
        "def child(i, k):",
        "    return 3 * i + k            # k = 1, 2 or 3",
        "",
        "root = tree[0]                 # the root: index 0",
        "",
        "# every node roots its own subtree - e.g. B's subtree:",
        "subtree_of_B = [\"B\", \"E\", \"F\", \"G\"]",
    ]

    def construct(self):
        def build_ternary_tree(labels):
            G = nx.Graph()
            n = len(labels)
            G.add_nodes_from(labels)

            for i in range(n):
                left = 3 * i + 1
                middle = 3 * i + 2
                right = 3 * i + 3
                if left < n:
                    G.add_edge(labels[i], labels[left])
                if middle < n:
                    G.add_edge(labels[i], labels[middle])
                if right < n:
                    G.add_edge(labels[i], labels[right])

            return G

        def highlight_subtree(tree, root, text="Subtree", color=WHITE, font="Arial", fsize=24):
            def collect_subtree_nodes(node, edges, visited):
                visited.add(node)
                for child in [v for u, v in edges if u == node]:
                    if child not in visited:
                        collect_subtree_nodes(child, edges, visited)
                return visited

            edges = [(str(u), str(v)) for u, v in tree.edges]
            subtree_nodes = sorted(collect_subtree_nodes(root, edges, set()))

            self.play(*[tree.vertices[n].Select() for n in subtree_nodes], run_time=0.5)

            surround = SurroundingRectangle(*[tree.vertices[n] for n in subtree_nodes], color=color, buff=0.15, corner_radius=0.6)
            nodeSurr = DashedVMobject(surround, num_dashes=35)
            nodeText = Text(text, font=font, color=color, font_size=fsize).next_to(nodeSurr, DOWN, buff=0.1)
            self.play(Create(nodeSurr), run_time=0.5)
            self.wait(0.2)
            self.play(Write(nodeText), run_time=0.5)
            self.wait(1.5)

            self.play(
                *[tree.vertices[n].Clear() for n in subtree_nodes],
                Uncreate(nodeSurr),
                Unwrite(nodeText),
                run_time=0.5, lag_ratio=0.1
            )

        labels = [chr(65 + i) for i in range(11)]
        G = build_ternary_tree(labels)

        tree = Graph(
            vertices=list(G.nodes),
            edges=list(G.edges),
            vertex_mobjects={v: Node(v) for v in list(G.nodes)},
            edge_config={"stroke_color": EDGE_COL, "stroke_width": 6},
            layout="tree",
            layout_scale=5,
            root_vertex="A"
        )

        self.code_step("declare")
        self.play(Create(tree), run_time=6)
        self.wait(2)

        self.code_step("node")
        play_surrounding_node_animation(self, tree, "B", "Node", UR)
        self.wait(0.5)
        self.code_step("root")
        play_surrounding_node_animation(self, tree, "A", "Root Node", UP)
        self.wait(0.7)

        for root in ["B", "E", "F", "G", "C", "D"]:
            self.code_step("subtree")
            highlight_subtree(tree, root, text="Subtree", color=TEXTCOL, font=FONT, fsize=FSIZE)
            self.wait(0.2)

        self.wait(2)


class TreeListCorrelation(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "# the same tree, stored as a flat list",
        "tree = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]   # index = position in the list",
        "",
        "def left_child(i):",
        "    return 2 * i + 1          # the left child's index",
        "",
        "def right_child(i):",
        "    return 2 * i + 2          # the right child's index",
        "",
        "def parent(i):",
        "    return (i - 1) // 2       # the parent's index",
        "",
        "i = 3",
        "print(tree[left_child(i)])   # tree[7]",
        "print(tree[right_child(i)])  # tree[8]",
        "print(tree[parent(i)])       # tree[1]",
    ]

    def construct(self):
        G = nx.Graph()

        for i in range(9):
            G.add_node(i)  # Adding nodes A, B, C, ..., K

        G.add_edges_from([
            (0, 1), (0, 2),
            (1, 3), (1, 4),
            (2, 5), (2, 6),
            (3, 7), (3, 8),
            (4, 9)
        ])
        
        tree = Graph(
                    vertices=list(G.nodes), 
                    edges=list(G.edges)[::-1], 
                    vertex_mobjects={v : Node(v) for v in list(G.nodes)},
                    edge_config={"stroke_color": EDGE_COL, "stroke_width": 6},
                    layout="tree", 
                    layout_scale=2.7,
                    root_vertex=0
                ).to_corner(DL, buff=0.7)
        

        list_rep = VGroup(*[Node(i) for i in range(10)])
        list_rep.arrange(RIGHT, buff=0.2).to_corner(UL, buff=0.7)

        self.code_step("declare-tree")
        self.play(Create(tree),run_time=4)
        self.code_step("declare-list")
        self.play(Create(list_rep), run_time=4)

        nodeSurr = DashedVMobject(SurroundingRectangle(tree, color=TEXTCOL, buff=0.15, corner_radius=0.6), num_dashes=40)
        nodeText = Text("Tree", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, RIGHT, buff=0.2)
        self.code_step("tree-label")
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

        self.wait(1)

        nodeSurr = DashedVMobject(SurroundingRectangle(list_rep, color=TEXTCOL, buff=0.15, corner_radius=0.6), num_dashes=40)
        nodeText = Text("List Representation of Tree", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, DOWN, buff=0.2)
        self.code_step("list-label")
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)


        NodeText = Text("Node: ", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE)
        LCText = Text("Left Child: ", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE)
        RCText = Text("Right Child: ", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE)
        PText = Text("Parent: ", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE)
        self.play(Write(
            VGroup(NodeText, LCText, RCText, PText).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(tree, RIGHT, buff=0.7, aligned_edge=UP)
        ))

        for i in range(9):
            self.code_step("node-i")
            self.play(
                tree.vertices[i].Select(),
                list_rep[i].Select(),
                run_time=0.5
            )

            self.wait(0.2)

            left_child = 2 * i + 1
            right_child = 2 * i + 2
            parent = (i - 1) // 2 if i > 0 else None

            NodeTex = MathTex(r"i = " + str(i), font_size=EXPLANATORY_FONT_SIZE + 10, color=TEXTCOL).next_to(NodeText, RIGHT, buff=0.2)
            LCTextTex = MathTex(r"2 \times i + 1 = " + str(left_child), font_size=EXPLANATORY_FONT_SIZE + 10, color=TEXTCOL).next_to(LCText, RIGHT, buff=0.2)
            RCTextTex = MathTex(r"2 \times i + 2 = " + str(right_child), font_size=EXPLANATORY_FONT_SIZE + 10, color=TEXTCOL).next_to(RCText, RIGHT, buff=0.2)
            PTextTex = MathTex(r"\lfloor \frac{i - 1}{2} \rfloor = " + str(parent), font_size=EXPLANATORY_FONT_SIZE + 10, color=TEXTCOL).next_to(PText, RIGHT, buff=0.2)


            nodeSurrLC, nodeSurrRC, nodeSurrP = None, None, None

            if left_child < len(tree.vertices):
                nodeSurrLC = VGroup(
                    DashedVMobject(SurroundingRectangle(list_rep[left_child], color=TEXTCOL, buff=0, corner_radius=0.52)),
                    Text("Left\nChild", font=FONT, color=TEXTCOL, font_size=POINTER_FONT_SIZE).next_to(list_rep[left_child], DOWN, buff=0.2)
                )
            if right_child < len(tree.vertices):
                nodeSurrRC = VGroup(
                    DashedVMobject(SurroundingRectangle(list_rep[right_child], color=TEXTCOL, buff=0, corner_radius=0.52)),
                    Text("Right\nChild", font=FONT, color=TEXTCOL, font_size=POINTER_FONT_SIZE).next_to(list_rep[right_child], DOWN, buff=0.2)
                )
            if parent is not None:
                nodeSurrP = VGroup(
                    DashedVMobject(SurroundingRectangle(list_rep[parent], color=TEXTCOL, buff=0, corner_radius=0.52)),
                    Text("Parent", font=FONT, color=TEXTCOL, font_size=POINTER_FONT_SIZE).next_to(list_rep[parent], DOWN, buff=0.2)
                )


            self.code_step("formulas")
            self.play(
                Write(NodeTex),
                Write(LCTextTex),
                Write(RCTextTex),
                Write(PTextTex),
                run_time=0.5
            )

            if nodeSurrLC:
                self.code_step("left")
                self.play(Create(nodeSurrLC), run_time=0.5)
            if nodeSurrRC:
                self.code_step("right")
                self.play(Create(nodeSurrRC), run_time=0.5)
            if nodeSurrP:
                self.code_step("parent")
                self.play(Create(nodeSurrP), run_time=0.5)
            
            self.wait(1.5)
            
            if nodeSurrLC:
                self.play(Uncreate(nodeSurrLC), run_time=0.5)
            if nodeSurrRC:
                self.play(Uncreate(nodeSurrRC), run_time=0.5)
            if nodeSurrP:
                self.play(Uncreate(nodeSurrP), run_time=0.5)

            self.play(
                tree.vertices[i].Clear(),
                list_rep[i].Clear(),
                Unwrite(NodeTex),
                Unwrite(LCTextTex),
                Unwrite(RCTextTex),
                Unwrite(PTextTex),
                run_time=0.5
            )
            self.wait(0.2)

        self.wait(2)


class MaxHeap(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "# a max-heap: every parent >= its children (array form)",
        "heap = []",
        "",
        "def insert(heap, value):",
        "    heap.append(value)              # join at the next free slot (level order)",
        "    i = len(heap) - 1",
        "    while i > 0:",
        "        parent = (i - 1) // 2",
        "        if heap[i] > heap[parent]:  # child larger than the parent?",
        "            heap[i], heap[parent] = heap[parent], heap[i]   # swap up",
        "            i = parent",
        "        else:",
        "            break                   # parent >= child: heap property holds",
        "",
        "for value in [2, 7, 26, 25, 19, 17, 1, 90, 3, 36]:",
        "    insert(heap, value)",
        "",
        "print(heap)   # [90, 36, 17, 25, 26, 7, 1, 2, 3, 19]",
    ]

    def construct(self):
        def insert(value):
            new_node = Node(value)
            new_node.set_z_index(2)
            tree_node.append(new_node)
            max_heap.append(value)

            i = len(tree_node) - 1
            parent_index = (i - 1) // 2

            is_left_child = i % 2 == 1

            level_of_parent = np.floor(np.log2(parent_index + 1))

            if i == 0:
                new_node.to_edge(UP, buff=0.5)
            elif is_left_child:
                new_node.move_to(tree_node[parent_index].get_center() + (DOWN * 1.5) + (LEFT * (len(list_of_vertices) - level_of_parent - 7)))
            elif not is_left_child:
                new_node.move_to(tree_node[parent_index].get_center() + (DOWN * 1.5) + (RIGHT * (len(list_of_vertices) - level_of_parent - 7)))

            explanatory_text = Text(f"Inserting {value}", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(DOWN, buff=1.9)
            self.code_step("call")
            self.play(Write(explanatory_text), run_time=0.5)
            self.wait(0.3)

            self.code_step("append")
            self.play(Create(new_node), run_time=0.5)
            if parent_index >= 0:
                self.play(Create(Line(tree_node[parent_index].get_center(), new_node.get_center(), color=EDGE_COL, stroke_width=6)))

            if parent_index >= 0:
                while i > 0 and max_heap[i] > max_heap[parent_index]:
                    sub_explanatory_text1 = Text(f"{max_heap[i]} > {max_heap[parent_index]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                    sub_explanatory_text2 = Text(f"Swapping {max_heap[i]} with {max_heap[parent_index]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_explanatory_text1, DOWN, buff=0.2)

                    self.code_step("swap")
                    self.play(
                        tree_node[i].Select(),
                        tree_node[parent_index].Select(),
                        Write(sub_explanatory_text1),
                        Write(sub_explanatory_text2),
                        run_time=0.5
                    )

                    self.wait(0.2)

                    self.play(
                        tree_node[i].animate.move_to(tree_node[parent_index].get_center()),
                        tree_node[parent_index].animate.move_to(tree_node[i].get_center())
                    )

                    # Swap in the heap
                    max_heap[i], max_heap[parent_index] = max_heap[parent_index], max_heap[i]
                    # Swap in the tree node representation
                    tree_node[i], tree_node[parent_index] = tree_node[parent_index], tree_node[i]

                    self.wait(0.2)

                    self.play(
                        tree_node[i].Clear(),
                        tree_node[parent_index].Clear(),
                        Unwrite(sub_explanatory_text1),
                        Unwrite(sub_explanatory_text2),
                        run_time=0.5
                    )

                    i = parent_index
                    parent_index = (i - 1) // 2

                self.wait(0.1)

                if parent_index >= 0:
                    sub_explanatory_text1 = Text(f"{max_heap[i]} <= {max_heap[parent_index]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                    sub_explanatory_text2 = Text(f"{max_heap[i]} is now in the correct position", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_explanatory_text1, DOWN, buff=0.2)
                    self.code_step("settle")
                    self.play(
                        Write(sub_explanatory_text1),
                        Write(sub_explanatory_text2),
                        run_time=0.5
                    )
                    self.wait(0.5)
                    self.play(
                        Unwrite(sub_explanatory_text1),
                        Unwrite(sub_explanatory_text2),
                        run_time=0.5
                    )
                    self.wait(0.2)

            self.wait(0.4)
            self.play(Unwrite(explanatory_text), run_time=0.5)
            

        list_of_vertices = [2,7,26,25,19,17,1,90,3,36]
        max_heap = []
        tree_node = []

        for i in list_of_vertices:
            insert(i)

        self.wait(2)


class MinHeap(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "# a min-heap: every parent <= its children (array form)",
        "heap = []",
        "",
        "def insert(heap, value):",
        "    heap.append(value)              # join at the next free slot (level order)",
        "    i = len(heap) - 1",
        "    while i > 0:",
        "        parent = (i - 1) // 2",
        "        if heap[i] < heap[parent]:  # child smaller than the parent?",
        "            heap[i], heap[parent] = heap[parent], heap[i]   # swap up",
        "            i = parent",
        "        else:",
        "            break                   # parent <= child: heap property holds",
        "",
        "for value in [26, 7, 2, 25, 19, 17, 1, 90, 36, 3]:",
        "    insert(heap, value)",
        "",
        "print(heap)   # [1, 3, 2, 26, 19, 17, 7, 90, 36, 25]",
    ]

    def construct(self):
        def insert(value):
            new_node = Node(value)
            new_node.set_z_index(2)
            tree_node.append(new_node)
            min_heap.append(value)

            i = len(tree_node) - 1
            parent_index = (i - 1) // 2

            is_left_child = i % 2 == 1

            level_of_parent = np.floor(np.log2(parent_index + 1))

            if i == 0:
                new_node.to_edge(UP, buff=0.5)
            elif is_left_child:
                new_node.move_to(tree_node[parent_index].get_center() + (DOWN * 1.5) + (LEFT * (len(list_of_vertices) - level_of_parent - 7)))
            elif not is_left_child:
                new_node.move_to(tree_node[parent_index].get_center() + (DOWN * 1.5) + (RIGHT * (len(list_of_vertices) - level_of_parent - 7)))

            explanatory_text = Text(f"Inserting {value}", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(DOWN, buff=1.9)
            self.code_step("call")
            self.play(Write(explanatory_text), run_time=0.5)
            self.wait(0.3)

            self.code_step("append")
            self.play(Create(new_node), run_time=0.5)
            if parent_index >= 0:
                self.play(Create(Line(tree_node[parent_index].get_center(), new_node.get_center(), color=EDGE_COL, stroke_width=6)))

            if parent_index >= 0:
                while i > 0 and min_heap[i] < min_heap[parent_index]:
                    sub_explanatory_text1 = Text(f"{min_heap[i]} < {min_heap[parent_index]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                    sub_explanatory_text2 = Text(f"Swapping {min_heap[i]} with {min_heap[parent_index]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_explanatory_text1, DOWN, buff=0.2)

                    self.code_step("swap")
                    self.play(
                        tree_node[i].Select(),
                        tree_node[parent_index].Select(),
                        Write(sub_explanatory_text1),
                        Write(sub_explanatory_text2),
                        run_time=0.5
                    )

                    self.wait(0.2)

                    self.play(
                        tree_node[i].animate.move_to(tree_node[parent_index].get_center()),
                        tree_node[parent_index].animate.move_to(tree_node[i].get_center())
                    )

                    # Swap in the heap
                    min_heap[i], min_heap[parent_index] = min_heap[parent_index], min_heap[i]
                    # Swap in the tree node representation
                    tree_node[i], tree_node[parent_index] = tree_node[parent_index], tree_node[i]

                    self.wait(0.2)

                    self.play(
                        tree_node[i].Clear(),
                        tree_node[parent_index].Clear(),
                        Unwrite(sub_explanatory_text1),
                        Unwrite(sub_explanatory_text2),
                        run_time=0.5
                    )

                    i = parent_index
                    parent_index = (i - 1) // 2

                self.wait(0.1)

                if parent_index >= 0:
                    sub_explanatory_text1 = Text(f"{min_heap[parent_index]} <= {min_heap[i]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                    sub_explanatory_text2 = Text(f"{min_heap[i]} is now in the correct position", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_explanatory_text1, DOWN, buff=0.2)
                    self.code_step("settle")
                    self.play(
                        Write(sub_explanatory_text1),
                        Write(sub_explanatory_text2),
                        run_time=0.5
                    )
                    self.wait(0.5)
                    self.play(
                        Unwrite(sub_explanatory_text1),
                        Unwrite(sub_explanatory_text2),
                        run_time=0.5
                    )
                    self.wait(0.2)

            self.wait(0.4)
            self.play(Unwrite(explanatory_text), run_time=0.5)
            

        list_of_vertices = [26,7,2,25,19,17,1,90,36,3]
        min_heap = []
        tree_node = []

        for i in list_of_vertices:
            insert(i)

        self.wait(2)



class BinarySearchTreeInsertion(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "# insert into a binary search tree: < goes left, >= goes right",
        "",
        "def insert(node, value):",
        "    if node is None:",
        "        return Node(value)        # empty slot found - place the node",
        "    if value < node.data:",
        "        node.left = insert(node.left, value)",
        "    else:",
        "        node.right = insert(node.right, value)",
        "    return node",
        "",
        "root = None",
        "for value in [26, 7, 2, 25, 19, 47, 1, 90, 36, 3]:",
        "    root = insert(root, value)",
    ]

    def construct(self):
        def insert_bst(value):
            new_node = Node(value)
            new_node.set_z_index(2)
            explanatory_text = Text(f"Inserting {value}", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(DOWN, buff=1.9)
            self.code_step("call")
            self.play(Write(explanatory_text), run_time=0.5)
            self.wait(0.3)

            if not bst_root:
                # First node becomes the root
                new_node.to_edge(UP, buff=0.5)
                bst_root.append((value, new_node))
                tree_node_map[value] = new_node
                G.add_node(value)
                self.code_step("root")
                self.play(Create(new_node), run_time=0.5)
            else:
                current_value, current_node = bst_root[0]
                parent_value = None

                index = 0  # Start from root index

                nodeSurr = DashedVMobject(SurroundingRectangle(current_node, color=TEXTCOL, buff=0, corner_radius=0.52))
                nodeSurr.set_z_index(3)
                self.code_step("cursor")
                self.play(Create(nodeSurr), run_time=0.5)
                self.wait(0.2)

                while True:
                    parent_value = current_value
                    parent_node = current_node

                    self.code_step("cursor")
                    self.play(nodeSurr.animate.move_to(current_node.get_center()), run_time=0.5)

                    if value < current_value:
                        next_index = 2 * index + 1
                        sub_explanatory_text1 = Text(f"{value} < {current_value}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                        sub_explanatory_text2 = Text(f"Going to the Left Child of {current_value}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_explanatory_text1, DOWN, buff=0.2)
                        self.code_step("left")
                        self.play(
                            Write(sub_explanatory_text1),
                            Write(sub_explanatory_text2),
                            run_time=0.5
                        )
                        self.wait(0.6)
                        self.play(
                            Unwrite(sub_explanatory_text1),
                            Unwrite(sub_explanatory_text2),
                            run_time=0.5
                        )
                        self.wait(0.2)
                    else:
                        next_index = 2 * index + 2
                        sub_explanatory_text1 = Text(f"{value} >= {current_value}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                        sub_explanatory_text2 = Text(f"Going to the Right Child of {current_value}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_explanatory_text1, DOWN, buff=0.2)
                        self.code_step("right")
                        self.play(
                            Write(sub_explanatory_text1),
                            Write(sub_explanatory_text2),
                            run_time=0.5
                        )
                        self.wait(0.6)
                        self.play(
                            Unwrite(sub_explanatory_text1),
                            Unwrite(sub_explanatory_text2),
                            run_time=0.5
                        )
                        self.wait(0.2)

                    if next_index not in bst_tree:
                        break
                    else:
                        current_value = bst_tree[next_index]
                        current_node = tree_node_map[current_value]
                        index = next_index


                # Place the new node
                parent_node = tree_node_map[parent_value]
                is_left = value < parent_value

                # Heuristic horizontal offset based on level
                level = int(np.log2(next_index + 1))
                offset = RIGHT if not is_left else LEFT
                new_node.move_to(parent_node.get_center() + (DOWN * 1.5) + offset * (4 - level))

                G.add_node(value)
                G.add_edge(parent_value, value)

                self.code_step("place")
                self.play(Create(new_node), run_time=0.5)
                self.play(Create(Line(parent_node.get_center(), new_node.get_center(), color=EDGE_COL, stroke_width=6)))

                # Update data structures
                bst_tree[next_index] = value
                bst_indices[value] = next_index
                tree_node_map[value] = new_node

                self.play(Uncreate(nodeSurr),run_time=0.5)

            self.wait(0.4)
            self.play(Unwrite(explanatory_text), run_time=0.5)

        list_of_vertices = [26, 7, 2, 25, 19, 47, 1, 90, 36, 3]
        bst_root = []
        bst_tree = {}
        bst_indices = {}
        tree_node_map = {}
        G = nx.Graph()

        for val in list_of_vertices:
            insert_bst(val)

        self.wait(2)


class BinarySearchTreeDeletion(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "def delete(node, value):",
        "    if node is None:",
        "        return None                    # value not in the tree",
        "    if value < node.data:",
        "        node.left = delete(node.left, value)",
        "    elif value > node.data:",
        "        node.right = delete(node.right, value)",
        "    else:                               # found the node",
        "        if node.left is None:           # case: no left child",
        "            return node.right",
        "        if node.right is None:         # case: no right child",
        "            return node.left",
        "        # two children: replace with the in-order successor",
        "        successor = leftmost(node.right)   # go right, then leftmost",
        "        node.data = successor.data",
        "        node.right = delete(node.right, successor.data)",
        "    return node",
    ]

    def construct(self):
        def insert_bst(value):
            new_node = Node(value)
            new_node.set_z_index(2)

            if not bst_root:
                new_node.to_edge(UP, buff=0.5)
                bst_root.append((value, new_node))
                tree_node_map[value] = new_node
                # Add root to bst_tree and bst_indices (this was missing!)
                bst_tree[0] = value
                bst_indices[value] = 0
                G.add_node(value)
                self.play(Create(new_node), run_time=0.5)
            else:
                current_value, _ = bst_root[0]
                parent_value = None

                index = 0  # Start from root index

                while True:
                    parent_value = current_value

                    if value < current_value:
                        next_index = 2 * index + 1
                    else:
                        next_index = 2 * index + 2

                    if next_index not in bst_tree:
                        break
                    else:
                        current_value = bst_tree[next_index]
                        index = next_index


                # Place the new node
                parent_node = tree_node_map[parent_value]
                is_left = value < parent_value

                # Heuristic horizontal offset based on level
                level = int(np.log2(next_index + 1))
                offset = RIGHT if not is_left else LEFT
                new_node.move_to(parent_node.get_center() + (DOWN * 1.5) + offset * (4 - level))

                G.add_node(value)
                G.add_edge(parent_value, value)

                self.play(Create(new_node), run_time=0.1)
                self.play(Create(Line(parent_node.get_center(), new_node.get_center(), color=EDGE_COL, stroke_width=6)), run_time=0.1)

                # Update data structures
                bst_tree[next_index] = value
                bst_indices[value] = next_index
                tree_node_map[value] = new_node


        def find_successor(node_value):
            """Find the inorder successor (smallest value in right subtree)"""
            current_index = bst_indices[node_value]
            right_index = 2 * current_index + 2
            
            if right_index not in bst_tree:
                return None
                
            # Create a successor search indicator
            current_value = bst_tree[right_index]
            current_node = tree_node_map[current_value]

            successor_search_surr = DashedVMobject(SurroundingRectangle(current_node, color=BLUE, buff=0, corner_radius=0.52))
            successor_search_surr.set_z_index(3)

            sub_explanatory_text = Text(f"Finding successor: go right to {current_value}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE-5).to_edge(DOWN, buff=2.7)
            self.code_step("successor")
            self.play(Create(successor_search_surr), Write(sub_explanatory_text), run_time=0.5)
            self.wait(0.3)

            # Go to right subtree and find leftmost node
            current_index = right_index
            while True:
                left_index = 2 * current_index + 1
                if left_index not in bst_tree:
                    break

                # Move to left child
                left_value = bst_tree[left_index]
                left_node = tree_node_map[left_value]

                self.play(Unwrite(sub_explanatory_text), run_time=0.3)
                sub_explanatory_text = Text(f"Go left to {left_value}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE-5).to_edge(DOWN, buff=2.7)
                self.code_step("successor")
                self.play(
                    successor_search_surr.animate.move_to(left_node.get_center()),
                    Write(sub_explanatory_text),
                    run_time=0.5
                )
                self.wait(0.3)
                current_index = left_index
            
            # Found the successor
            successor_value = bst_tree[current_index]
            self.play(Unwrite(sub_explanatory_text), run_time=0.3)
            sub_explanatory_text = Text(f"Successor found: {successor_value}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE-5).to_edge(DOWN, buff=2.7)
            self.play(Write(sub_explanatory_text), run_time=0.5)
            self.wait(0.5)
            
            # Clean up the search indicator
            self.play(Uncreate(successor_search_surr), Unwrite(sub_explanatory_text), run_time=0.5)
            
            return successor_value

        def delete_bst(value):
            explanatory_text = Text(f"Deleting {value}", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(DOWN, buff=1.9)
            self.code_step("call")
            self.play(Write(explanatory_text), run_time=0.5)
            self.wait(0.3)

            if value not in tree_node_map:
                sub_explanatory_text = Text(f"Value {value} not found in tree", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                self.play(Write(sub_explanatory_text), run_time=0.5)
                self.wait(1)
                self.play(Unwrite(sub_explanatory_text), Unwrite(explanatory_text), run_time=0.5)
                return
            
            # First, animate the search for the node to delete
            if len(bst_root) > 0:
                current_value, current_node = bst_root[0]
                current_index = 0
                
                # Create search indicator
                search_surr = DashedVMobject(SurroundingRectangle(current_node, color=ORANGE, buff=0, corner_radius=0.52))
                search_surr.set_z_index(3)

                search_explanatory_text = Text(f"Searching for {value}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                self.code_step("search")
                self.play(Create(search_surr), Write(search_explanatory_text), run_time=0.5)
                self.wait(0.3)

                # Perform the search animation
                while current_value != value:
                    if value < current_value:
                        next_index = 2 * current_index + 1
                        direction_text = f"{value} < {current_value}, go left"
                        self.code_step("go-left")
                    else:
                        next_index = 2 * current_index + 2
                        direction_text = f"{value} >= {current_value}, go right"
                        self.code_step("go-right")
                    
                    if next_index not in bst_tree:
                        break
                        
                    next_value = bst_tree[next_index]
                    next_node = tree_node_map[next_value]
                    
                    # Show direction and move search indicator
                    self.play(Unwrite(search_explanatory_text), run_time=0.3)
                    search_explanatory_text = Text(direction_text, font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                    self.play(
                        search_surr.animate.move_to(next_node.get_center()),
                        Write(search_explanatory_text),
                        run_time=0.5
                    )
                    self.wait(0.3)
                    
                    current_value = next_value
                    current_node = next_node
                    current_index = next_index
                
                # Found the node
                self.play(Unwrite(search_explanatory_text), run_time=0.3)
                search_explanatory_text = Text(f"Found {value}!", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                self.code_step("found")
                self.play(Write(search_explanatory_text), run_time=0.5)
                self.wait(0.5)
                
                # Clean up search animation
                self.play(Uncreate(search_surr), Unwrite(search_explanatory_text), run_time=0.5)
            
            node_to_delete = tree_node_map[value]
            node_index = bst_indices[value]
            
            # Highlight the node to be deleted
            nodeSurr = DashedVMobject(SurroundingRectangle(node_to_delete, color=TEXTCOL, buff=0, corner_radius=0.52))
            nodeSurr.set_z_index(3)
            self.play(Create(nodeSurr), run_time=0.5)
            self.wait(0.2)
            
            left_index = 2 * node_index + 1
            right_index = 2 * node_index + 2
            has_left = left_index in bst_tree
            has_right = right_index in bst_tree
            
            if not has_left and not has_right:
                # Case 1: Leaf node
                sub_explanatory_text = Text(f"{value} is a leaf node - simply remove it", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                self.code_step("case-leaf")
                self.play(Write(sub_explanatory_text), run_time=0.5)
                self.wait(1)
                
                # Remove the edge to parent (if not root)
                if node_index != 0:
                    parent_index = (node_index - 1) // 2
                    parent_value = bst_tree[parent_index]
                    remove_edge_visual(self, G, parent_value, value, tree_node_map[parent_value], node_to_delete)
                
                # Remove the node
                self.play(FadeOut(node_to_delete), FadeOut(nodeSurr), run_time=0.5)
                
                # Update data structures
                del bst_tree[node_index]
                del bst_indices[value]
                del tree_node_map[value]
                G.remove_node(value)
                
                # If deleting root node, clear bst_root
                if node_index == 0:
                    bst_root.clear()
                
                self.play(Unwrite(sub_explanatory_text), run_time=0.5)
                
            elif has_left and not has_right:
                # Case 2: Only left child
                left_value = bst_tree[left_index]
                left_node = tree_node_map[left_value]

                sub_explanatory_text = Text(f"{value} has only left child - replace with {left_value}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                self.code_step("case-left")
                self.play(Write(sub_explanatory_text), run_time=0.5)
                self.wait(1)
                
                # Remove the edge to parent (if not root)
                if node_index != 0:
                    parent_index = (node_index - 1) // 2
                    parent_value = bst_tree[parent_index]
                    remove_edge_visual(self, G, parent_value, value, tree_node_map[parent_value], node_to_delete)
                
                # Also remove edge between deleted node and its left child
                remove_edge_visual(self, G, value, left_value, node_to_delete, left_node)
                
                # Move left child to parent's position
                self.play(left_node.animate.move_to(node_to_delete.get_center()), run_time=0.5)
                self.play(FadeOut(node_to_delete), FadeOut(nodeSurr), run_time=0.5)
                
                # Add new edge from parent to the moved child (if not root)
                if node_index != 0:
                    parent_index = (node_index - 1) // 2
                    parent_value = bst_tree[parent_index]
                    parent_node = tree_node_map[parent_value]
                    G.add_edge(parent_value, left_value)
                    self.play(Create(Line(parent_node.get_center(), left_node.get_center(), color=EDGE_COL, stroke_width=6)), run_time=0.3)
                
                # Update data structures
                bst_tree[node_index] = left_value
                bst_indices[left_value] = node_index
                del bst_tree[left_index]
                del bst_indices[value]
                del tree_node_map[value]
                tree_node_map[left_value] = left_node
                
                # If deleting root node, update bst_root
                if node_index == 0:
                    bst_root[0] = (left_value, left_node)
                
                self.play(Unwrite(sub_explanatory_text), run_time=0.5)
                
            elif not has_left and has_right:
                # Case 3: Only right child
                right_value = bst_tree[right_index]
                right_node = tree_node_map[right_value]

                sub_explanatory_text = Text(f"{value} has only right child - replace with {right_value}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                self.code_step("case-right")
                self.play(Write(sub_explanatory_text), run_time=0.5)
                self.wait(1)
                
                # Remove the edge to parent (if not root)
                if node_index != 0:
                    parent_index = (node_index - 1) // 2
                    parent_value = bst_tree[parent_index]
                    remove_edge_visual(self, G, parent_value, value, tree_node_map[parent_value], node_to_delete)
                
                # Also remove edge between deleted node and its right child
                remove_edge_visual(self, G, value, right_value, node_to_delete, right_node)
                
                # Move right child to parent's position
                self.play(right_node.animate.move_to(node_to_delete.get_center()), run_time=0.5)
                self.play(FadeOut(node_to_delete), FadeOut(nodeSurr), run_time=0.5)
                
                # Add new edge from parent to the moved child (if not root)
                if node_index != 0:
                    parent_index = (node_index - 1) // 2
                    parent_value = bst_tree[parent_index]
                    parent_node = tree_node_map[parent_value]
                    G.add_edge(parent_value, right_value)
                    self.play(Create(Line(parent_node.get_center(), right_node.get_center(), color=EDGE_COL, stroke_width=6)), run_time=0.3)
                
                # Update data structures
                bst_tree[node_index] = right_value
                bst_indices[right_value] = node_index
                del bst_tree[right_index]
                del bst_indices[value]
                del tree_node_map[value]
                tree_node_map[right_value] = right_node
                
                # If deleting root node, update bst_root
                if node_index == 0:
                    bst_root[0] = (right_value, right_node)
                
                self.play(Unwrite(sub_explanatory_text), run_time=0.5)
                
            else:
                # Case 4: Two children - replace with successor
                successor_value = find_successor(value)
                
                if successor_value is None:
                    # This shouldn't happen for a node with two children, but just in case
                    sub_explanatory_text = Text(f"Error: No successor found for {value}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                    self.play(Write(sub_explanatory_text), run_time=0.5)
                    self.wait(1)
                    self.play(Unwrite(sub_explanatory_text), Unwrite(explanatory_text), FadeOut(nodeSurr), run_time=0.5)
                    return
                
                successor_node = tree_node_map[successor_value]
                
                sub_explanatory_text1 = Text(f"{value} has two children", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                sub_explanatory_text2 = Text(f"Replace with successor {successor_value}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_explanatory_text1, DOWN, buff=0.2)

                self.code_step("replace")
                self.play(Write(sub_explanatory_text1), Write(sub_explanatory_text2), run_time=0.5)
                
                # Highlight successor
                successor_surr = DashedVMobject(SurroundingRectangle(successor_node, color=GREEN, buff=0, corner_radius=0.52))
                successor_surr.set_z_index(3)
                self.play(Create(successor_surr), run_time=0.5)
                self.wait(1)
                
                # Replace the value in the node
                new_node = Node(successor_value)
                new_node.move_to(node_to_delete.get_center())
                new_node.set_z_index(2)
                
                self.play(
                    FadeOut(node_to_delete),
                    Create(new_node),
                    run_time=0.5
                )
                
                # Update the tree_node_map for the replaced node
                del tree_node_map[value]  # Remove the old mapping first
                
                # Save the original successor position before updating indices
                original_successor_index = bst_indices[successor_value]
                
                # Update the successor to take the deleted node's position
                tree_node_map[successor_value] = new_node
                bst_tree[node_index] = successor_value
                bst_indices[successor_value] = node_index
                
                # Remove the original value from bst_indices (important!)
                del bst_indices[value]
                
                # If deleting root node, update bst_root
                if node_index == 0:
                    bst_root[0] = (successor_value, new_node)
                
                # Now we need to remove the successor from its original position
                # The successor will have at most one child (right child)
                successor_right_index = 2 * original_successor_index + 2
                
                # Remove the edge to the original successor's parent
                self.code_step("remove-successor")
                if original_successor_index != 0:
                    successor_parent_index = (original_successor_index - 1) // 2
                    successor_parent_value = bst_tree[successor_parent_index]
                    remove_edge_visual(self, G, successor_parent_value, successor_value, tree_node_map[successor_parent_value], successor_node)
                
                if successor_right_index in bst_tree:
                    # Successor has a right child, move it up
                    successor_right_value = bst_tree[successor_right_index]
                    successor_right_node = tree_node_map[successor_right_value]
                    
                    # Remove edge between successor and its right child
                    remove_edge_visual(self, G, successor_value, successor_right_value, successor_node, successor_right_node)
                    
                    # Move the right child to successor's position
                    bst_tree[original_successor_index] = successor_right_value
                    bst_indices[successor_right_value] = original_successor_index
                    del bst_tree[successor_right_index]
                    
                    # Move the visual node
                    self.play(successor_right_node.animate.move_to(successor_node.get_center()), run_time=0.5)
                    
                    # Add new edge from successor's parent to the moved child (if successor wasn't root)
                    if original_successor_index != 0:
                        successor_parent_index = (original_successor_index - 1) // 2
                        successor_parent_value = bst_tree[successor_parent_index]
                        successor_parent_node = tree_node_map[successor_parent_value]
                        G.add_edge(successor_parent_value, successor_right_value)
                        self.play(Create(Line(successor_parent_node.get_center(), successor_right_node.get_center(), color=EDGE_COL, stroke_width=6)), run_time=0.3)
                else:
                    # Successor is a leaf, just remove it
                    del bst_tree[original_successor_index]
                
                # Clean up successor references
                if successor_value in bst_indices and bst_indices[successor_value] != node_index:
                    del bst_indices[successor_value]
                
                # Fade out the original successor node
                self.play(FadeOut(successor_node), run_time=0.5)
                
                # Now delete the successor from its original position
                self.play(FadeOut(successor_surr), run_time=0.5)
                self.play(Unwrite(sub_explanatory_text1), Unwrite(sub_explanatory_text2), run_time=0.5)
                
                self.play(FadeOut(nodeSurr), run_time=0.5)
            
            self.wait(0.4)
            self.play(Unwrite(explanatory_text), run_time=0.5)

        list_of_vertices = [26, 7, 2, 25, 19, 47, 1, 90, 36, 3, 34]
        bst_root: list[tuple[int, Node]] = []
        bst_tree: dict[int, int] = {}
        bst_indices: dict[int, int] = {}
        tree_node_map: dict[int, Node] = {}
        G = nx.Graph()

        for val in list_of_vertices:
            insert_bst(val)

        delete_bst(1)
        self.wait(0.5)
        delete_bst(25)
        self.wait(0.5)
        delete_bst(26)


class UnionFind(SyncedScene):
    DISPLAY_CODE: ClassVar[list[str]] = [
        "class UnionFind:",
        "    def __init__(self, size):",
        "        self.parent = [i for i in range(size)]  # each element starts alone",
        "        self.rank = [0] * size",
        "",
        "    def find(self, x):",
        "        if self.parent[x] != x:",
        "            self.parent[x] = self.find(self.parent[x])  # path compression",
        "        return self.parent[x]",
        "",
        "    def union(self, x, y):",
        "        root_x = self.find(x)",
        "        root_y = self.find(y)",
        "        if root_x == root_y:",
        "            return False                # already the same set",
        "        if self.rank[root_x] < self.rank[root_y]:",
        "            self.parent[root_x] = root_y",
        "        elif self.rank[root_x] > self.rank[root_y]:",
        "            self.parent[root_y] = root_x",
        "        else:",
        "            self.parent[root_y] = root_x",
        "            self.rank[root_x] += 1       # union by rank",
        "        return True",
    ]

    def construct(self):
        def findParent(v):
            if parent[v] != v:
                return findParent(parent[v])
            else:
                return v

        def union(u, v):
            sub_operation_text = Text(f"Union({u}, {v})", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(operation_text, DOWN, buff=0.5)
            self.code_step("call")
            self.play(Write(sub_operation_text), run_time=0.5)
            self.wait(0.5)
            self.play(
                index_to_node[u].SelectHighlight(),
                index_to_node[v].SelectHighlight(),
                run_time=0.5
            )

            c_old = findParent(u)
            c_old_node = index_to_node[c_old]
            sub_operation_text1 = Text(f"Find({u}) => {c_old}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_operation_text, DOWN, buff=0.2)
            self.code_step("find-u")
            self.play(Write(sub_operation_text1), run_time=0.5)
            self.wait(0.5)
            self.play(c_old_node.Highlight())
            self.play(Unwrite(sub_operation_text1), run_time=0.5)

            self.wait(0.1)

            c_new = findParent(v)
            c_new_node = index_to_node[c_new]
            sub_operation_text1 = Text(f"Find({v}) => {c_new}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_operation_text, DOWN, buff=0.2)
            self.code_step("find-v")
            self.play(Write(sub_operation_text1), run_time=0.5)
            self.wait(0.5)
            self.play(c_new_node.Highlight())
            self.play(Unwrite(sub_operation_text1), run_time=0.5)

            if c_old == c_new:
                return

            if len(members[c_new]) == 1:
                shift = LEFT
            elif len(members[c_new]) == 2:
                shift = RIGHT
            else:
                shift = 2.5 * RIGHT
            
            displacement = (c_new_node.get_center() - c_old_node.get_center()) + DOWN + shift

            for x in members[c_old]:
                members[c_new].append(x)
                member_vgroup[c_new].add(index_to_node[x])
                is_child.add(x)

            parent[c_old] = c_new

            self.code_step("merge")
            for x in members[c_old]:
                self.play(
                    index_to_node[x].animate.shift(displacement),
                    run_time=0.5
                )

            edge = Line(
                c_old_node.get_center(),
                c_new_node.get_center(),
                color=EDGE_COL,
                stroke_width=6
            )

            edge.add_updater(
                lambda m: m.put_start_and_end_on(
                    c_old_node.get_center(),
                    c_new_node.get_center()
                )
            )

            self.play(Create(edge), run_time=0.5)

            self.play(
                index_to_node[u].Reset(),
                index_to_node[v].Reset(),
                c_old_node.Reset(),
                c_new_node.Reset(),
                Unwrite(sub_operation_text),
                run_time=0.5
            )

            sets = calculate_arrangement()
            self.code_step("representative")
            self.play(
                sets.animate.arrange(RIGHT, buff=0.7).next_to(operation_text, DOWN, buff=2.3),
                
                run_time=0.5
            )

            self.play(c_new_node.Select())

            self.wait(0.5)

        def calculate_arrangement():
            sets = VGroup()
            for v in members:
                if v not in is_child:
                    sets.add(member_vgroup[v])
            
            return sets

        list_of_vertices = [26,7,2,25,19,17,1,90,3]

        parent = {v : v for v in list_of_vertices}
        members = {v : [v] for v in list_of_vertices}

        index_to_node = {v : Node(v).set_z_index(2) for v in list_of_vertices}
        member_vgroup = {v : VGroup(index_to_node[v]) for v in list_of_vertices}
        is_child = set()

        sets = calculate_arrangement()
        sets.arrange(RIGHT, buff=0.7)
        self.code_step("init")
        self.play(Create(sets), run_time=2)
        self.play(*[index_to_node[v].Select() for v in list_of_vertices], run_time=0.5)
        self.wait(0.5)

        nodeSurr = DashedVMobject(SurroundingRectangle(member_vgroup[7], color=TEXTCOL, buff=0.15, corner_radius=0.6))
        nodeText = Text("Set", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, UP, buff=0.1)
        self.code_step("set")
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

        operation_text = Text("Union Operation", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.6)
        self.code_step("union-start")
        self.play(Write(operation_text), run_time=0.5)
        self.wait(0.5)

        union(26, 7)

        nodeSurr = DashedVMobject(SurroundingRectangle(member_vgroup[7], color=TEXTCOL, buff=0.15, corner_radius=0.6), num_dashes=25)
        nodeText = Text("Union Set", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, UP, buff=0.1)
        self.code_step("union-set")
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

        self.wait(0.5)

        nodeSurr = DashedVMobject(SurroundingRectangle(index_to_node[7], color=TEXTCOL, buff=0.15, corner_radius=0.6))
        nodeText = Text("     Set\nRepresentative", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeSurr, UP, buff=0.1)
        self.code_step("representative")
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

        union(2, 25)
        union(2, 19)
        union(2, 26)
        union(1, 17)
        union(90, 1)
        union(90, 3)
        union(2, 1)

        self.wait(0.6)

        self.play(Unwrite(operation_text), run_time=0.5)
        sets = calculate_arrangement()
        self.play(sets.animate.center())
        self.wait(2)