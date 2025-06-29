from manim import *
from typing import Any
import numpy as np

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

WEIGHT_FONT_SIZE = 25         # For "Found!", "SORT!", etc.
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


class WeightedLine(Line):
    def __init__(
        self,
        *args: Any,
        weight: str | int | float | None = None,
        weight_config: dict | None = None,
        weight_alpha: float = 0.5,
        bg_config: dict | None = None,
        add_bg: bool = True,
        **kwargs: Any,
    ):
        self.weight = weight
        self.alpha = weight_alpha
        self.add_bg = add_bg
        super().__init__(*args, **kwargs)

        self.weight_config = {
            "color": TEXTCOL,
            "font_size": WEIGHT_FONT_SIZE,
        }

        if weight_config:
            self.weight_config.update(weight_config)

        self.bg_config = {
            "color": config.background_color,
            "opacity": 1,
        }
        if bg_config:
            self.bg_config.update(bg_config)

        if self.weight is not None:
            self._add_weight()

    def _add_weight(self):
        point = self.point_from_proportion(self.alpha)
        label = Text(str(self.weight), **self.weight_config)
        label.move_to(point)

        if self.add_bg:
            label.add_background_rectangle(**self.bg_config)
            label.background_rectangle.height += SMALL_BUFF

        self.add(label)


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


class AdjecencyMatrixUD(Scene):
    def construct(self):
        vertices = [0, 1, 2, 3, 4]
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 3), (2, 4), (4, 3)]
        degrees = {0: 2, 1: 3, 2: 3, 3: 3, 4: 3}

        graph = Graph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_config={"stroke_color": EDGE_COL, "stroke_width": 6})
        
        graph.to_edge(LEFT, buff=1.2)
        self.play(Create(graph), run_time=5)
        self.wait(2)

        graphVertices = graph.vertices

        adjecencyMatrix = np.zeros((len(vertices), len(vertices)), dtype=int)

        matrixTable = IntegerTable(
            adjecencyMatrix,
            row_labels=[Text(str(v)) for v in vertices],
            col_labels=[Text(str(v)) for v in vertices],
            include_outer_lines=True,
            v_buff=0.5,
            h_buff=0.8,
        )

        for mob in matrixTable.get_entries():
            mob.set_color(TEXTCOL)

        for line in matrixTable.get_horizontal_lines() + matrixTable.get_vertical_lines():
            line.set_stroke(color=EDGE_COL, width=3.5)
        
        matrixTable.to_edge(RIGHT, buff=1.2)
        
        self.play(matrixTable.create(), Write(Text("Adjecency Matrix", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(matrixTable, UP, 0.3)), run_time=1.5)   
        self.wait(1.2)

        for u, v in edges:
            self.play(
                graphVertices[u].Select(), graphVertices[v].Select(),
                graph.edges[(u, v)].animate.set_stroke(color=TEXTCOL, width=7),
                run_time=0.5
            )
            ent_to_update1 = matrixTable.get_entries_without_labels(pos=(u+1, v+1))
            ent_to_update2 = matrixTable.get_entries_without_labels(pos=(v+1, u+1))
            cell_to_update1 = matrixTable.get_cell(pos=(u+2, v+2), color=SORTCOL).set_stroke(color=SORTCOL, width=7)
            cell_to_update2 = matrixTable.get_cell(pos=(v+2, u+2), color=SORTCOL).set_stroke(color=SORTCOL, width=7)
            adjecencyMatrix[u][v] = 1
            adjecencyMatrix[v][u] = 1

            self.play(
                matrixTable.get_row_labels()[u].animate.set_color(SORTCOL),
                matrixTable.get_row_labels()[v].animate.set_color(SORTCOL),
                matrixTable.get_col_labels()[u].animate.set_color(SORTCOL),
                matrixTable.get_col_labels()[v].animate.set_color(SORTCOL),
                run_time=0.5
            )
            
            self.play(FadeIn(cell_to_update1, cell_to_update2), run_time=0.2)

            self.play(
                ReplacementTransform(
                    ent_to_update1, Integer(1).set_color(TEXTCOL).move_to(ent_to_update1)
                ),
                ReplacementTransform(
                    ent_to_update2, Integer(1).set_color(TEXTCOL).move_to(ent_to_update2)
                ),
                run_time=0.7
            )
            self.play(
                graphVertices[u].Clear(), graphVertices[v].Clear(), 
                graph.edges[(u, v)].animate.set_stroke(color=EDGE_COL, width=6),
                FadeOut(cell_to_update1, cell_to_update2), 
                matrixTable.get_row_labels()[u].animate.set_color(TEXTCOL),
                matrixTable.get_row_labels()[v].animate.set_color(TEXTCOL),
                matrixTable.get_col_labels()[u].animate.set_color(TEXTCOL),
                matrixTable.get_col_labels()[v].animate.set_color(TEXTCOL),
                run_time=0.5)
            
            self.wait(2)

        self.wait(4)



class AdjecencyListUD(Scene):
    def construct(self):
        def get_adjacency_list_VGroup(adjacency_list):
            # adjacency_text.to_edge(UP, buff=0.5)
            # self.play(Write(adjacency_text), run_time=1.5)

            adjacency_list_group = VGroup()
            for vertex, neighbors in adjacency_list.items():
                vertex_text = Text(f"{vertex}: ", font_size=FSIZE, font=FONT, color=TEXTCOL)
                neighbors_text = Text(", ".join(map(str, neighbors)), font_size=FSIZE, font=FONT, color=TEXTCOL)
                line = VGroup(vertex_text, neighbors_text).arrange(RIGHT, buff=0.3)
                adjacency_list_group.add(line)
            
            adjacency_list_group.arrange(DOWN, buff=0.5, aligned_edge=LEFT)

            adjacency_text = Text("Adjacency List", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(adjacency_list_group, UP, buff=1, aligned_edge=LEFT)
            
            return VGroup(adjacency_list_group, adjacency_text).next_to(graph, RIGHT, buff=2)

        vertices = [0, 1, 2, 3, 4]
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 3), (2, 4), (4, 3)]
        degrees = {0: 2, 1: 3, 2: 3, 3: 3, 4: 3}

        graph = Graph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_config={"stroke_color": EDGE_COL, "stroke_width": 6})
        
        graph.to_edge(LEFT, buff=1.2)
        self.play(Create(graph), run_time=5)
        self.wait(2)

        graphVertices = graph.vertices

        adjecencyList = {v: [] for v in vertices}
        adjecencyListVGroup = get_adjacency_list_VGroup(adjecencyList)
        self.play(Create(adjecencyListVGroup), run_time=0.5)

        for u, v in edges:
            self.play(
                graphVertices[u].Select(), graphVertices[v].Select(),
                graph.edges[(u, v)].animate.set_stroke(color=TEXTCOL, width=7),
                run_time=0.5
            )

            adjecencyList[u].append(v)
            adjecencyList[v].append(u)

            self.play(
                adjecencyListVGroup[0].submobjects[u].animate.set_color(SELCOL),
                adjecencyListVGroup[0].submobjects[v].animate.set_color(SELCOL),
                run_time=0.5
            )

            self.wait(0.6)

            newAdjacencyListVGroup = get_adjacency_list_VGroup(adjecencyList)
            self.play(ReplacementTransform(adjecencyListVGroup, newAdjacencyListVGroup), run_time=0.5)
            adjecencyListVGroup = newAdjacencyListVGroup

            self.play(
                graphVertices[u].Clear(), graphVertices[v].Clear(), 
                graph.edges[(u, v)].animate.set_stroke(color=EDGE_COL, width=6),
                run_time=0.5)
            
            self.wait(2)

        self.wait(2)


class DirectedGraphs(Scene):
    def construct(self):
        vertices = [4, 3, 2, 0, 1]
        edges = [(0, 2), (0, 1), (1, 3), (4, 1), (4, 2), (2, 3), (3, 4)]

        graph = DiGraph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
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
            pointText = Text(f"{points[0]}->{points[1]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(edge.get_center(), direction=rotate_vector(edge.get_unit_vector(), PI / 2), buff=0.2)
            self.play(Create(edge), run_time=0.5)
            self.play(Write(pointText), run_time=0.2)

            if i == 0:
                # self.play(edge.animate.set_stroke(color=TEXTCOL), run_time=0.3)
                self.wait(0.1)
                nodeSurr = DashedVMobject(SurroundingRectangle(edge, color=TEXTCOL, buff=0.1, corner_radius=0.1), num_dashes=30)
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

        indegrees = {0: 0, 1: 2, 2: 2, 3: 2, 4: 1}
        exdegrees = {0: 2, 1: 1, 2: 1, 3: 1, 4: 2}

        indegreeVGroup = VGroup()
        exdegreeVGroup = VGroup()
        for i, v in enumerate(vertices):
            indegreeText = Text(str(indegrees[v]), font=FONT, color=TEXTCOL, font_size=DEGREE_FONT_SIZE).next_to(nodes[i], DOWN, buff=0)
            exdegreeText = Text(str(exdegrees[v]), font=FONT, color=TEXTCOL, font_size=DEGREE_FONT_SIZE).next_to(nodes[i], DOWN, buff=0)
            indegreeVGroup.add(indegreeText)
            exdegreeVGroup.add(exdegreeText)
        
        indegreeVGroup.shift([0.25, 0, 0])
        exdegreeVGroup.shift([-0.25, 0, 0])

        self.play(FadeIn(indegreeVGroup, lag_ratio=0.1), run_time=0.5)
        self.wait(1.5)
        nodeSurr = DashedVMobject(SurroundingRectangle(indegreeVGroup.submobjects[-1], color=TEXTCOL, buff=0.1, corner_radius=0.15))
        nodeText = Text("Indegree", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeSurr, DOWN + RIGHT, buff=0.08)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

        self.wait(2)

        self.play(FadeIn(exdegreeVGroup, lag_ratio=0.1), run_time=0.5)
        self.wait(1.5)
        nodeSurr = DashedVMobject(SurroundingRectangle(exdegreeVGroup.submobjects[-1], color=TEXTCOL, buff=0.1, corner_radius=0.15))
        nodeText = Text("Exdegree", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeSurr, DOWN + LEFT, buff=0.08)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

        self.wait(2)


class WeightedUDGraphs(Scene):
    def construct(self):
        vertices = [4, 3, 2, 0, 1]
        wedges = [(0, 1, 10), (0, 3, 18), (1, 2, 20), (1, 3, 6), (2, 4, 8), (3, 4, 70)]
        edges = [(i, j) for i, j, _ in wedges]
        degrees = {0: 2, 1:3, 2:1, 3: 3, 4:2}
        edge_config = {(i, j):{'weight': w, "stroke_color": EDGE_COL, "stroke_width": 6} for i, j, w in wedges}

        graph = Graph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_type=WeightedLine,
                      edge_config=edge_config)
        

        self.play(Create(graph), run_time=3)
        # self.play(FadeIn(*graph.vertices.values(), lag_ratio=0.15), run_time=3)
        # self.play(FadeIn(*graph.edges.values(), lag_ratio=0.15), run_time=3)
        self.wait(2)

