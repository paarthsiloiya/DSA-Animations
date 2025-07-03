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
                    edges=list(G.edges), 
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

