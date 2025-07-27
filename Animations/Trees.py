from manim import *
from manim.utils.unit import Percent, Pixels
import random
import networkx as nx

config.frame_width = 16
config.frame_height = 9


BASECOL = ManimColor.from_hex("#ebe7f3")
TEXTCOL = ManimColor.from_hex("#000000")
SELCOL = ManimColor.from_hex("#7a5bae")
SORTCOL = ManimColor.from_hex("#4a2a90")

FSIZE = 40
FONT = 'JetBrains Mono'

random.seed(32)

SWAP_FONT_SIZE = 38         # For "Insert!", "Delete!", etc.
EXPLANATORY_FONT_SIZE = 30  # For step-by-step explanations
POINTER_FONT_SIZE = 20      # For pointer labels (if any)

NODE_COL = BASECOL
EDGE_COL = SELCOL


class Node(VGroup):
    def __init__(self, value):
        super().__init__()
        self.text = Text(str(value), font=FONT, color=TEXTCOL, font_size=FSIZE)
        self.circle = Circle(radius=0.5, color=NODE_COL, fill_color=NODE_COL, fill_opacity=1, stroke_width=0)
        self.text.move_to(self.circle.get_center())
        self.add(self.circle, self.text)

    def Select(self):
        return self.circle.animate.set_stroke(color=SORTCOL, width=10)
    
    def Clear(self):
            return self.circle.animate.set_stroke(color=NODE_COL, width=0)
        
    def Highlight(self):
        return self.circle.animate.set_fill(color=SORTCOL), self.text.animate.set_color(color=BASECOL)
    
    def SelectHighlight(self):
        return self.circle.animate.set_stroke(color=SELCOL, width=10)
    
    def Reset(self):
        return self.circle.animate.set_stroke(color=NODE_COL, width=0).set_fill(color=NODE_COL), self.text.animate.set_color(color=TEXTCOL)


class TreeExplanation(Scene):
    def construct(self):
        def playSurroundingNodeAnimation(node, text, dir):
            self.play(tree.vertices[node].Select(), run_time=0.5)
            nodeSurr = DashedVMobject(SurroundingRectangle(tree.vertices[node], color=TEXTCOL, buff=0.15, corner_radius=0.6))
            nodeText = Text(text, font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, dir, buff=0.1)
            self.play(Create(nodeSurr), run_time=0.5)
            self.wait(0.2)
            self.play(Write(nodeText), run_time=0.5)
            self.wait(1.5)
            self.play(tree.vertices[node].Clear() ,Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

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

        self.play(Create(tree),run_time=6)

        self.wait(2)

        playSurroundingNodeAnimation("B", "Node", UP)
        self.wait(0.5)
        playSurroundingNodeAnimation("A", "Root Node", UP)
        self.wait(0.5)
        playSurroundingNodeAnimation("D", "Parent\nNode", RIGHT)
        playSurroundingNodeAnimation("I", "Child\nNode", RIGHT)
        self.wait(0.5)
        
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


class BinaryTreeExplanation(Scene):
    def construct(self):
        def playSurroundingNodeAnimation(node, text, dir):
            self.play(tree.vertices[node].Select(), run_time=0.5)
            nodeSurr = DashedVMobject(SurroundingRectangle(tree.vertices[node], color=TEXTCOL, buff=0.15, corner_radius=0.6))
            nodeText = Text(text, font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, dir, buff=0.1)
            self.play(Create(nodeSurr), run_time=0.5)
            self.wait(0.2)
            self.play(Write(nodeText), run_time=0.5)
            self.wait(1.5)
            self.play(tree.vertices[node].Clear() ,Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)


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

        playSurroundingNodeAnimation("B", "Node", UR)
        self.wait(0.5)
        playSurroundingNodeAnimation("A", "Root Node", UP)
        self.wait(0.7)

        for root in ["B", "D", "E", "C", "G", "F"]:  # or automate this via non-leaf detection
            highlight_subtree(tree, root, text="Subtree", color=TEXTCOL, font=FONT, fsize=FSIZE)
            self.wait(0.2)
        
        self.wait(2)


class TernaryTreeExplanation(Scene):
    def construct(self):
        def playSurroundingNodeAnimation(node, text, dir):
            self.play(tree.vertices[node].Select(), run_time=0.5)
            nodeSurr = DashedVMobject(SurroundingRectangle(tree.vertices[node], color=TEXTCOL, buff=0.15, corner_radius=0.6))
            nodeText = Text(text, font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, dir, buff=0.1)
            self.play(Create(nodeSurr), run_time=0.5)
            self.wait(0.2)
            self.play(Write(nodeText), run_time=0.5)
            self.wait(1.5)
            self.play(tree.vertices[node].Clear() ,Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

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

        self.play(Create(tree), run_time=6)
        self.wait(2)

        playSurroundingNodeAnimation("B", "Node", UR)
        self.wait(0.5)
        playSurroundingNodeAnimation("A", "Root Node", UP)
        self.wait(0.7)

        for root in ["B", "E", "F", "G", "C", "D"]:
            highlight_subtree(tree, root, text="Subtree", color=TEXTCOL, font=FONT, fsize=FSIZE)
            self.wait(0.2)

        self.wait(2)


class TreeListCorrelation(Scene):
    def construct(self):
        def playSurroundingNodeAnimation(node, text, dir):
            self.play(tree.vertices[node].Select(), run_time=0.5)
            nodeSurr = DashedVMobject(SurroundingRectangle(tree.vertices[node], color=TEXTCOL, buff=0.15, corner_radius=0.6))
            nodeText = Text(text, font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, dir, buff=0.1)
            self.play(Create(nodeSurr), run_time=0.5)
            self.wait(0.2)
            self.play(Write(nodeText), run_time=0.5)
            self.wait(1.5)
            self.play(tree.vertices[node].Clear() ,Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

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
                    vertex_mobjects={v : Node((v)) for v in list(G.nodes)},
                    edge_config={"stroke_color": EDGE_COL, "stroke_width": 6},
                    layout="tree", 
                    layout_scale=2.7,
                    root_vertex=0
                ).to_corner(DL, buff=0.7)
        

        list_rep = VGroup(*[Node(i) for i in range(10)])
        list_rep.arrange(RIGHT, buff=0.2).to_corner(UL, buff=0.7)

        self.play(Create(tree),run_time=4)
        self.play(Create(list_rep), run_time=4)

        nodeSurr = DashedVMobject(SurroundingRectangle(tree, color=TEXTCOL, buff=0.15, corner_radius=0.6), num_dashes=40)
        nodeText = Text("Tree", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, RIGHT, buff=0.2)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

        self.wait(1)

        nodeSurr = DashedVMobject(SurroundingRectangle(list_rep, color=TEXTCOL, buff=0.15, corner_radius=0.6), num_dashes=40)
        nodeText = Text("List Representation of Tree", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, DOWN, buff=0.2)
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


            self.play(
                Write(NodeTex),
                Write(LCTextTex),
                Write(RCTextTex),
                Write(PTextTex),
                run_time=0.5
            )

            if nodeSurrLC:
                self.play(Create(nodeSurrLC), run_time=0.5)
            if nodeSurrRC:
                self.play(Create(nodeSurrRC), run_time=0.5)
            if nodeSurrP:
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


class MaxHeap(Scene):
    def construct(self):
        def insert(value):
            new_node = Node(value)
            new_node.set_z_index(2)
            tree_node.append(new_node)
            max_heap.append(value)
            G.add_node(value)
            
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
            self.play(Write(explanatory_text), run_time=0.5)
            self.wait(0.3)

            self.play(Create(new_node), run_time=0.5)
            G.add_edge(max_heap[parent_index], value)
            self.play(Create(Line(tree_node[parent_index].get_center(), new_node.get_center(), color=EDGE_COL, stroke_width=6)))

            if parent_index >= 0:
                while i > 0 and max_heap[i] > max_heap[parent_index]:
                    sub_explanatory_text1 = Text(f"{max_heap[i]} > {max_heap[parent_index]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                    sub_explanatory_text2 = Text(f"Swapping {max_heap[i]} with {max_heap[parent_index]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_explanatory_text1, DOWN, buff=0.2)
                    
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

                sub_explanatory_text1 = Text(f"{max_heap[i]} <= {max_heap[parent_index]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                sub_explanatory_text2 = Text(f"{max_heap[i]} is now in the correct position", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_explanatory_text1, DOWN, buff=0.2)
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

        G = nx.Graph()

        for i in list_of_vertices:
            insert(i)

        self.wait(2)


class MinHeap(Scene):
    def construct(self):
        def insert(value):
            new_node = Node(value)
            new_node.set_z_index(2)
            tree_node.append(new_node)
            min_heap.append(value)
            G.add_node(value)
            
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
            self.play(Write(explanatory_text), run_time=0.5)
            self.wait(0.3)

            self.play(Create(new_node), run_time=0.5)
            G.add_edge(min_heap[parent_index], value)
            self.play(Create(Line(tree_node[parent_index].get_center(), new_node.get_center(), color=EDGE_COL, stroke_width=6)))

            if parent_index >= 0:
                while i > 0 and min_heap[i] < min_heap[parent_index]:
                    sub_explanatory_text1 = Text(f"{min_heap[i]} < {min_heap[parent_index]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                    sub_explanatory_text2 = Text(f"Swapping {min_heap[i]} with {min_heap[parent_index]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_explanatory_text1, DOWN, buff=0.2)
                    
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

                sub_explanatory_text1 = Text(f"{min_heap[parent_index]} <= {min_heap[i]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                sub_explanatory_text2 = Text(f"{min_heap[i]} is now in the correct position", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_explanatory_text1, DOWN, buff=0.2)
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

        G = nx.Graph()

        for i in list_of_vertices:
            insert(i)

        self.wait(2)



class BinarySearchTree(Scene):
    def construct(self):
        def insert_bst(value):
            new_node = Node(value)
            new_node.set_z_index(2)
            explanatory_text = Text(f"Inserting {value}", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(DOWN, buff=1.9)
            self.play(Write(explanatory_text), run_time=0.5)
            self.wait(0.3)

            if not bst_root:
                # First node becomes the root
                new_node.to_edge(UP, buff=0.5)
                bst_root.append((value, new_node))
                tree_node_map[value] = new_node
                G.add_node(value)
                self.play(Create(new_node), run_time=0.5)
            else:
                current_value, current_node = bst_root[0]
                parent_value = None
                path = []  # Keep track of the traversal path

                current_value, current_node = bst_root[0]
                index = 0  # Start from root index

                nodeSurr = DashedVMobject(SurroundingRectangle(current_node, color=TEXTCOL, buff=0, corner_radius=0.52))
                nodeSurr.set_z_index(3)
                self.play(Create(nodeSurr), run_time=0.5)
                self.wait(0.2)

                while True:
                    parent_value = current_value
                    parent_node = current_node

                    self.play(nodeSurr.animate.move_to(current_node.get_center()), run_time=0.5)

                    if value < current_value:
                        next_index = 2 * index + 1
                        sub_explanatory_text1 = Text(f"{value} < {current_value}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
                        sub_explanatory_text2 = Text(f"Going to the Left Child of {current_value}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_explanatory_text1, DOWN, buff=0.2)
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
        bst_tree = dict()
        bst_indices = dict()
        tree_node_map = dict()
        G = nx.Graph()

        for val in list_of_vertices:
            insert_bst(val)

        self.wait(2)


class UnionFind(Scene):
    def construct(self):
        def findParent(v):
            if parent[v] != v:
                return findParent(parent[v])
            else:
                return v
                
        def union(u, v):
            sub_operation_text = Text(f"Union({u}, {v})", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(operation_text, DOWN, buff=0.5)
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
            self.play(Write(sub_operation_text1), run_time=0.5)
            self.wait(0.5)
            self.play(c_old_node.Highlight())
            self.play(Unwrite(sub_operation_text1), run_time=0.5)

            self.wait(0.1)

            c_new = findParent(v)
            c_new_node = index_to_node[c_new]
            sub_operation_text1 = Text(f"Find({v}) => {c_new}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(sub_operation_text, DOWN, buff=0.2)
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
            self.play(
                sets.animate.arrange(RIGHT, buff=0.7).next_to(operation_text, DOWN, buff=2.3),
                
                run_time=0.5
            )
            # self.play(sets.animate.next_to(operation_text, DOWN, buff=2.3))

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
        self.play(Create(sets), run_time=2)
        self.play(*[index_to_node[v].Select() for v in list_of_vertices], run_time=0.5)
        self.wait(0.5)

        nodeSurr = DashedVMobject(SurroundingRectangle(member_vgroup[7], color=TEXTCOL, buff=0.15, corner_radius=0.6))
        nodeText = Text("Set", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, UP, buff=0.1)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

        operation_text = Text("Union Operation", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.6)
        self.play(Write(operation_text), run_time=0.5)
        self.wait(0.5)

        union(26, 7)
        
        nodeSurr = DashedVMobject(SurroundingRectangle(member_vgroup[7], color=TEXTCOL, buff=0.15, corner_radius=0.6), num_dashes=25)
        nodeText = Text("Union Set", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, UP, buff=0.1)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

        self.wait(0.5)

        nodeSurr = DashedVMobject(SurroundingRectangle(index_to_node[7], color=TEXTCOL, buff=0.15, corner_radius=0.6))
        nodeText = Text("     Set\nRepresentative", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeSurr, UP, buff=0.1)
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