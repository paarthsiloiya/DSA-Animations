from manim import *

# manim -ql -p SearchingAlgorithms.py BinarySearch
config.frame_width = 16
config.frame_height = 9

BASECOL = ManimColor.from_hex("#ebe7f3")
TEXTCOL = ManimColor.from_hex("#000000")
SELCOL = ManimColor.from_hex("#7a5bae")
SORTCOL = ManimColor.from_hex("#4a2a90")

LAYOT_SCALE = 2.4
FSIZE = 40
FONT = 'JetBrains Mono'

SWAP_FONT_SIZE = 38         # For "Found!", "SORT!", etc.
EXPLANATORY_FONT_SIZE = 30  # For step-by-step explanations
DEGREE_FONT_SIZE = 17      # For "Low", "High", "Mid", etc.

NODE_COL = BASECOL
EDGE_COL = SELCOL
POINTER_FONT_COLOR = SORTCOL


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
        return self.circle.animate.set_fill(color=TEXTCOL), self.text.animate.set_color(color=BASECOL)

class UndirectedGraphs(Scene):
    def construct(self):
        vertices = [4, 3, 2, 0, 1]
        edges = [(0, 2), (0, 1), (1, 3), (4, 1), (4, 2), (2, 3), (3, 4)]
        degrees = {0: 2, 1: 3, 2: 3, 3: 3, 4: 3}

        graph = Graph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_config={"stroke_color": EDGE_COL, "stroke_width": 6})
        
        graph.center()

        nodes = list(graph.vertices.values())
        graphVertices = graph.vertices
        for _ in range(len(vertices)):
            self.play(*[FadeIn(nodes[_])], run_time=0.3)
            self.wait(0.1)

        self.wait(1)

        self.play(graphVertices[1].Select(), run_time=0.5)
        nodeSurr = DashedVMobject(SurroundingRectangle(graphVertices[1], color=TEXTCOL, buff=0.15, corner_radius=0.6))
        nodeText = Text("Node", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, UP, buff=0.1)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(graphVertices[1].Clear() ,Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

        self.wait(1.3)

        for i, item in enumerate(graph.edges.items()):
            points, edge = item
            n1, n2 = edges[i]
            self.play(graphVertices[n1].Select(), graphVertices[n2].Select(), run_time=0.5)
            pointText = Text(f"{points[0]}-{points[1]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(edge.get_center(), direction=rotate_vector(edge.get_unit_vector(), PI / 2), buff=0.2)
            self.play(Create(edge), run_time=0.5)
            self.play(Write(pointText), run_time=0.2)

            if i == 0:
                # self.play(edge.animate.set_stroke(color=TEXTCOL), run_time=0.3)
                self.wait(0.1)
                nodeSurr = DashedVMobject(SurroundingRectangle(edge, color=TEXTCOL, buff=0.1, corner_radius=0.1), num_dashes=30).scale([1, 0.7, 1])
                nodeText = Text("Edge", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, RIGHT, buff=0.1)
                self.play(Create(nodeSurr), run_time=0.5)
                self.wait(0.2)
                self.play(Write(nodeText), run_time=0.5)
                self.wait(1.3)
                self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)
                self.wait(0.1)
                # self.play(edge.animate.set_stroke(color=EDGE_COL), run_time=0.3)
                # self.wait(1.3)

            self.wait(0.6)
            self.play(Unwrite(pointText), run_time=0.2)
            self.wait(0.1)
            self.play(graphVertices[n1].Clear(), graphVertices[n2].Clear(), run_time=0.5)
            self.wait(0.5)

        degreesGroup = VGroup()
        for i, v in enumerate(vertices):
            degreeText = Text(str(degrees[v]), font=FONT, color=TEXTCOL, font_size=DEGREE_FONT_SIZE).next_to(nodes[i], DOWN, buff=0)
            # self.play(Write(degreeText), run_time=0.2)
            degreesGroup.add(degreeText)
            self.wait(0.3)
        
        degreesGroup.shift([-0.25, 0, 0])
        self.play(FadeIn(degreesGroup, lag_ratio=0.1), run_time=0.5)

        nodeSurr = DashedVMobject(SurroundingRectangle(degreesGroup.submobjects[-1], color=TEXTCOL, buff=0.1, corner_radius=0.15))
        nodeText = Text("Degree", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeSurr, DOWN, buff=0.08)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

        self.wait(2)


class DirectedGraphs(Scene):
    def construct(self):
        vertices = [0, 1, 2, 3, 4]
        edges = [(0,1), (0,2), (2,1), (3,2), (4,2)]

        indegrees = {0: 0, 1: 2, 2: 3, 3: 0, 4: 0}
        exdegrees = {0: 2, 1: 0, 2: 1, 3: 1, 4: 1}

        layout = {
            0: [-2.6, -1, 0],
            1: [-2.6, 2, 0],
            2: [0, 2, 0],
            3: [0, -1, 0],
            4: [2, 0.5, 0],
        }

        for l in layout.values():
            l[0] *= LAYOT_SCALE
            l[1] *= LAYOT_SCALE

        graph = DiGraph(vertices, edges, layout=layout,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_config={"stroke_color": EDGE_COL, "stroke_width": 6})
        
        graph.center()

        # self.add(graph)
        nodes = list(graph.vertices.values())
        for _ in range(len(vertices)):
            self.play(*[FadeIn(nodes[_])], run_time=0.3)
            self.wait(0.1)

        self.wait(1)

        nodeSurr = DashedVMobject(SurroundingRectangle(nodes[-1], color=TEXTCOL, buff=0.1, corner_radius=0.6))
        nodeText = Text("Node", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, UP, buff=0.1)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

        self.wait(1.3)

        for i, item in enumerate(graph.edges.items()):
            points, edge = item
            dir = rotate_vector(edge.get_unit_vector(), -PI/2)
            pointText = Text(f"({points[0]}-{points[1]})", font=FONT, color=TEXTCOL, font_size=FSIZE).move_to(edge.get_center() + dir)
            self.play(Create(edge), run_time=0.5)
            self.play(Write(pointText), run_time=0.2)

            if i == 0:
                # self.play(edge.animate.set_stroke(color=TEXTCOL), run_time=0.3)
                self.wait(0.1)
                nodeSurr = DashedVMobject(SurroundingRectangle(edge, color=TEXTCOL, buff=0.1, corner_radius=0.1), num_dashes=30)
                nodeText = Text("Edge", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, LEFT, buff=0.1)
                self.play(Create(nodeSurr), run_time=0.5)
                self.wait(0.2)
                self.play(Write(nodeText), run_time=0.5)
                self.wait(1.5)
                self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)
                self.wait(0.1)
                # self.play(edge.animate.set_stroke(color=EDGE_COL), run_time=0.3)
                # self.wait(1.3)

            self.wait(0.3)
            self.play(Unwrite(pointText), run_time=0.2)
            self.wait(0.5)


        self.wait(0.2)

        indegreeVGroup = VGroup()
        exdegreeVGroup = VGroup()
        for i, v in enumerate(vertices):
            indegreeText = Text(str(indegrees[v]), font=FONT, color=TEXTCOL, font_size=20, stroke_width=1, stroke_color=WHITE, weight=HEAVY).next_to(nodes[i], DOWN, buff=0)
            exdegreeText = Text(str(exdegrees[v]), font=FONT, color=TEXTCOL, font_size=20, stroke_width=1, stroke_color=WHITE, weight=HEAVY).next_to(nodes[i], DOWN, buff=0)
            indegreeVGroup.add(indegreeText)
            exdegreeVGroup.add(exdegreeText)
        
        indegreeVGroup.shift([0.4, 0, 0])
        exdegreeVGroup.shift([-0.4, 0, 0])
        self.play(FadeIn(indegreeVGroup, lag_ratio=0.1), run_time=0.5)
        self.play(FadeIn(exdegreeVGroup, lag_ratio=0.1), run_time=0.5)


        self.wait(1)