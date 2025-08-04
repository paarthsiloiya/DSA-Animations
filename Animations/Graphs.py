from manim import *
from typing import Any
import numpy as np
from env_config import *

# Override specific font sizes for Graphs
EXPLANATORY_FONT_SIZE = 30  # For step-by-step explanations


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
            "buff": 0.1,
        }
        if bg_config:
            self.bg_config.update(bg_config)

        if self.weight is not None:
            self._add_weight()

    def _add_weight(self):
        point = self.point_from_proportion(self.alpha)
        self.label = Text(str(self.weight), **self.weight_config)
        self.label.move_to(point)

        if self.add_bg:
            self.label.add_background_rectangle(**self.bg_config)
            self.label.background_rectangle.height += SMALL_BUFF

        self.add(self.label)

    def _get_weight_mob(self):
        return self.label
    
    def select_line(self):
        return self.animate.set_stroke(color=EDGE_COL, width=12), self.label.animate.set_stroke(color=TEXTCOL, width=0.2)
    
    def deselect_line(self):
        return self.animate.set_stroke(color=EDGE_COL, width=6), self.label.animate.set_stroke(color=TEXTCOL, width=0.2)

    def highlight_line(self):
        return self.animate.set_color(color=TEXTCOL), self.label.animate.set_stroke(color=TEXTCOL, width=0.2)
    
    def clear_line(self):
        return self.animate.set_color(color=EDGE_COL), self.label.animate.set_stroke(color=TEXTCOL, width=0.2)
    


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
                line = VGroup(vertex_text, neighbors_text).arrange(RIGHT, buff=0.3, aligned_edge=UP)
                adjacency_list_group.add(line)
            
            adjacency_list_group.arrange(DOWN, buff=0.5, aligned_edge=LEFT)

            adjacency_text = Text("Adjacency List", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(adjacency_list_group, UP, buff=1, aligned_edge=LEFT)
            
            return VGroup(adjacency_list_group, adjacency_text).next_to(graph, RIGHT, buff=2, aligned_edge=UP)

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


class UndirectedGraphBFS(Scene):
    def construct(self):
        vertices = [4, 1, 2, 3, 6, 7, 5]
        edges = [(1,2),(1,4),(2,4),(2,3),(2,5),(3,6),(5,6),(5,7),(6,7)]

        graph = Graph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_config={"stroke_color": EDGE_COL, "stroke_width": 7}
                      ).scale(1.4)
        
        graph.to_edge(LEFT, buff=1.2)

        nodes = list(graph.vertices.values())
        BFSTree = []
        graphVertices = graph.vertices
        self.play(Create(graph), run_time=2)
        self.wait(1)

        adjacencyList = {v: [] for v in vertices}
        for u, v in edges:
            adjacencyList[u].append(v)
            adjacencyList[v].append(u)

        visited = {v: False for v in vertices}
        s = 1

        # Show starting node selection
        start_text = Text(f"Starting from node {s}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).to_edge(RIGHT, buff=1.2)
        self.play(Write(start_text), run_time=1)
        self.wait(1)

        visited[s] = True
        queue = [s]

        # Show queue initialization (constant at top)
        queue_text = Text(f"Queue: [{', '.join(map(str, queue))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.5).shift(RIGHT * 4)
        self.play(Unwrite(start_text), Write(queue_text), run_time=1)
        self.wait(1)

        while queue:
            current = queue.pop(0)
            # Update queue display (constant at top)
            new_queue_text = Text(f"Queue: [{', '.join(map(str, queue))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).move_to(queue_text)
            self.play(ReplacementTransform(queue_text, new_queue_text), run_time=0.5)
            queue_text = new_queue_text
            
            
            # Update explanation for current processing
            processing_text = Text(f"Processing node {current}", 
                                 font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(graph, RIGHT, buff=1.2)
            self.play(Write(processing_text), run_time=0.8)

            self.play(graphVertices[current].Highlight(), run_time=0.5)
            self.wait(0.3)

            neighbors_found = []
            for neighbor in adjacencyList[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
                    neighbors_found.append(neighbor)

                    # Show neighbor discovery temporarily
                    discovery_text = Text(f"Found unvisited neighbor {neighbor}", 
                                        font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE-4).next_to(processing_text, DOWN, buff=0.5)
                    self.play(Write(discovery_text), run_time=0.3)

                    self.play(
                        graphVertices[neighbor].Select(),
                        graph.edges[(current, neighbor)].animate.set_stroke(color=TEXTCOL),
                        run_time=0.5
                    )

                    BFSTree.append((current, neighbor))

                    self.wait(0.5)
                    
                    # Update queue display (constant at top)
                    new_queue_text = Text(f"Queue: [{', '.join(map(str, queue))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).move_to(queue_text)
                    self.play(ReplacementTransform(queue_text, new_queue_text), run_time=0.5)
                    queue_text = new_queue_text

                    # Fade out the discovery text
                    self.play(Unwrite(discovery_text), run_time=0.3)
                    self.wait(0.2)

            if not neighbors_found:
                no_neighbors_text = Text(f"No unvisited neighbors for {current}", 
                                       font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE-4).next_to(processing_text, DOWN, buff=0.5)
                self.play(Write(no_neighbors_text), run_time=0.5)
                self.wait(0.8)
                self.play(Unwrite(no_neighbors_text), run_time=0.3)

            self.play(Unwrite(processing_text), run_time=0.2)
            self.wait(0.5)

        self.play(Unwrite(queue_text), run_time=1.5)
        self.wait(2)
        self.play(graph.animate.remove_edges(*[edge for edge in graph.edges if edge not in BFSTree]), run_time=1.5)
        self.wait(0.5)
        self.play(graph.animate.center())
        self.wait(2)


class UndirectedGraphDFS(Scene):
    def construct(self):
        vertices = [4, 1, 2, 3, 6, 7, 5]
        edges = [(1,2),(1,4),(2,4),(2,3),(2,5),(3,6),(5,6),(5,7),(6,7)]

        graph = Graph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_config={"stroke_color": EDGE_COL, "stroke_width": 7}
                      ).scale(1.4)
        
        graph.to_edge(LEFT, buff=1.2)

        nodes = list(graph.vertices.values())
        DFSTree = []
        graphVertices = graph.vertices
        self.play(Create(graph), run_time=2)
        self.wait(1)

        adjacencyList = {v: [] for v in vertices}
        for u, v in edges:
            adjacencyList[u].append(v)
            adjacencyList[v].append(u)

        visited = {v: False for v in vertices}
        s = 1

        # Show starting node selection
        start_text = Text(f"Starting from node {s}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).to_edge(RIGHT, buff=1.2)
        self.play(Write(start_text), run_time=1)
        self.wait(1)

        visited[s] = True
        stack = [s]

        # Show stack initialization (constant at top)
        stack_text = Text(f"Stack: [{', '.join(map(str, stack))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.5).shift(RIGHT * 4)
        self.play(Unwrite(start_text), Write(stack_text), run_time=1)
        self.wait(1)

        while stack:
            current = stack.pop()  # DFS uses pop() from end (LIFO)
            # Update stack display (constant at top)
            new_stack_text = Text(f"Stack: [{', '.join(map(str, stack))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).move_to(stack_text)
            self.play(ReplacementTransform(stack_text, new_stack_text), run_time=0.5)
            stack_text = new_stack_text
            
            # Update explanation for current processing
            processing_text = Text(f"Processing node {current}", 
                                 font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(graph, RIGHT, buff=1.2)
            self.play(Write(processing_text), run_time=0.8)

            self.play(graphVertices[current].Highlight(), run_time=0.5)
            self.wait(0.3)

            neighbors_found = []
            # For DFS, we often want to process neighbors in reverse order to maintain left-to-right visual order
            for neighbor in reversed(adjacencyList[current]):
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
                    neighbors_found.append(neighbor)

                    # Show neighbor discovery temporarily
                    discovery_text = Text(f"Found unvisited neighbor {neighbor}", 
                                        font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE-4).next_to(processing_text, DOWN, buff=0.5)
                    self.play(Write(discovery_text), run_time=0.3)

                    self.play(
                        graphVertices[neighbor].Select(),
                        graph.edges[(current, neighbor)].animate.set_stroke(color=TEXTCOL),
                        run_time=0.5
                    )

                    DFSTree.append((current, neighbor))

                    self.wait(0.5)
                    
                    # Update stack display (constant at top)
                    new_stack_text = Text(f"Stack: [{', '.join(map(str, stack))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).move_to(stack_text)
                    self.play(ReplacementTransform(stack_text, new_stack_text), run_time=0.5)
                    stack_text = new_stack_text

                    # Fade out the discovery text
                    self.play(Unwrite(discovery_text), run_time=0.3)
                    self.wait(0.2)

            if not neighbors_found:
                no_neighbors_text = Text(f"No unvisited neighbors for {current}", 
                                       font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE-4).next_to(processing_text, DOWN, buff=0.5)
                self.play(Write(no_neighbors_text), run_time=0.5)
                self.wait(0.8)
                self.play(Unwrite(no_neighbors_text), run_time=0.3)

            self.play(Unwrite(processing_text), run_time=0.2)
            self.wait(0.5)

        self.play(Unwrite(stack_text), run_time=1.5)
        self.wait(2)
        self.play(graph.animate.remove_edges(*[edge for edge in graph.edges if edge not in DFSTree]), run_time=1.5)
        self.wait(0.5)
        self.play(graph.animate.center())
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


class AdjecencyMatrixD(Scene):
    def construct(self):
        vertices = [0, 1, 2, 3, 4]
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 3), (2, 4), (4, 3)]
        degrees = {0: 2, 1: 3, 2: 3, 3: 3, 4: 3}

        graph = DiGraph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
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
                graph.edges[(u, v)].animate.set_color(color=TEXTCOL),
                run_time=0.5
            )
            ent_to_update1 = matrixTable.get_entries_without_labels(pos=(u+1, v+1))
            cell_to_update1 = matrixTable.get_cell(pos=(u+2, v+2), color=SORTCOL).set_stroke(color=SORTCOL, width=7)
            adjecencyMatrix[u][v] = 1

            self.play(
                matrixTable.get_row_labels()[u].animate.set_color(SORTCOL),
                matrixTable.get_col_labels()[v].animate.set_color(SORTCOL),
                run_time=0.5
            )
            
            self.play(FadeIn(cell_to_update1), run_time=0.2)

            self.play(
                ReplacementTransform(
                    ent_to_update1, Integer(1).set_color(TEXTCOL).move_to(ent_to_update1)
                ),
                run_time=0.7
            )
            self.play(
                graphVertices[u].Clear(), graphVertices[v].Clear(), 
                graph.edges[(u, v)].animate.set_color(color=EDGE_COL),
                FadeOut(cell_to_update1), 
                matrixTable.get_row_labels()[u].animate.set_color(TEXTCOL),
                matrixTable.get_col_labels()[v].animate.set_color(TEXTCOL),
                run_time=0.5
            )
            
            self.wait(2)

        self.wait(4)


class DirectedGraphBFS(Scene):
    def construct(self):
        vertices = [4, 1, 2, 3, 6, 7, 5]
        edges = [(1,2),(1,4),(2,4),(2,3),(2,5),(3,6),(5,6),(5,7),(6,7)]

        graph = Graph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_config={"stroke_color": EDGE_COL, "stroke_width": 7},
                      edge_type=DAGArrow,
                ).scale(1.4)
        
        graph.to_edge(LEFT, buff=1.2)

        nodes = list(graph.vertices.values())
        BFSTree = []
        graphVertices = graph.vertices
        self.play(Create(graph), run_time=2)
        self.wait(1)

        adjacencyList = {v: [] for v in vertices}
        for u, v in edges:
            adjacencyList[u].append(v)

        visited = {v: False for v in vertices}
        s = 1

        # Show starting node selection
        start_text = Text(f"Starting from node {s}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).to_edge(RIGHT, buff=1.2)
        self.play(Write(start_text), run_time=1)
        self.wait(1)

        visited[s] = True
        queue = [s]

        # Show queue initialization (constant at top)
        queue_text = Text(f"Queue: [{', '.join(map(str, queue))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.5).shift(RIGHT * 4)
        self.play(Unwrite(start_text), Write(queue_text), run_time=1)
        self.wait(1)

        while queue:
            current = queue.pop(0)
            # Update queue display (constant at top)
            new_queue_text = Text(f"Queue: [{', '.join(map(str, queue))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).move_to(queue_text)
            self.play(ReplacementTransform(queue_text, new_queue_text), run_time=0.5)
            queue_text = new_queue_text
            
            
            # Update explanation for current processing
            processing_text = Text(f"Processing node {current}", 
                                 font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(graph, RIGHT, buff=1.2)
            self.play(Write(processing_text), run_time=0.8)

            self.play(graphVertices[current].Highlight(), run_time=0.5)
            self.wait(0.3)

            neighbors_found = []
            for neighbor in adjacencyList[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
                    neighbors_found.append(neighbor)

                    # Show neighbor discovery temporarily
                    discovery_text = Text(f"Found unvisited neighbor {neighbor}", 
                                        font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE-4).next_to(processing_text, DOWN, buff=0.5)
                    self.play(Write(discovery_text), run_time=0.3)

                    self.play(
                        graphVertices[neighbor].Select(),
                        graph.edges[(current, neighbor)].animate.set_color(color=TEXTCOL),
                        run_time=0.5
                    )

                    BFSTree.append((current, neighbor))

                    self.wait(0.5)
                    
                    # Update queue display (constant at top)
                    new_queue_text = Text(f"Queue: [{', '.join(map(str, queue))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).move_to(queue_text)
                    self.play(ReplacementTransform(queue_text, new_queue_text), run_time=0.5)
                    queue_text = new_queue_text

                    # Fade out the discovery text
                    self.play(Unwrite(discovery_text), run_time=0.3)
                    self.wait(0.2)

            if not neighbors_found:
                no_neighbors_text = Text(f"No unvisited neighbors for {current}", 
                                       font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE-4).next_to(processing_text, DOWN, buff=0.5)
                self.play(Write(no_neighbors_text), run_time=0.5)
                self.wait(0.8)
                self.play(Unwrite(no_neighbors_text), run_time=0.3)

            self.play(Unwrite(processing_text), run_time=0.2)
            self.wait(0.5)

        self.play(Unwrite(queue_text), run_time=1.5)
        self.wait(2)
        self.play(graph.animate.remove_edges(*[edge for edge in graph.edges if edge not in BFSTree]), run_time=1.5)
        self.wait(0.5)
        self.play(graph.animate.center())
        self.wait(2)


class DirectedGraphDFS(Scene):
    def construct(self):
        vertices = [4, 1, 2, 3, 6, 7, 5]
        edges = [(1,2),(1,4),(2,4),(2,3),(2,5),(3,6),(5,6),(5,7),(6,7)]

        graph = Graph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_config={"stroke_color": EDGE_COL, "stroke_width": 7},
                      edge_type=DAGArrow,
                ).scale(1.4)
        
        graph.to_edge(LEFT, buff=1.2)

        nodes = list(graph.vertices.values())
        DFSTree = []
        graphVertices = graph.vertices
        self.play(Create(graph), run_time=2)
        self.wait(1)

        adjacencyList = {v: [] for v in vertices}
        for u, v in edges:
            adjacencyList[u].append(v)

        visited = {v: False for v in vertices}
        s = 1

        # Show starting node selection
        start_text = Text(f"Starting from node {s}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).to_edge(RIGHT, buff=1.2)
        self.play(Write(start_text), run_time=1)
        self.wait(1)

        visited[s] = True
        stack = [s]

        # Show stack initialization (constant at top)
        stack_text = Text(f"Stack: [{', '.join(map(str, stack))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.5).shift(RIGHT * 4)
        self.play(Unwrite(start_text), Write(stack_text), run_time=1)
        self.wait(1)

        while stack:
            current = stack.pop()  # DFS uses pop() from end (LIFO)
            # Update stack display (constant at top)
            new_stack_text = Text(f"Stack: [{', '.join(map(str, stack))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).move_to(stack_text)
            self.play(ReplacementTransform(stack_text, new_stack_text), run_time=0.5)
            stack_text = new_stack_text
            
            # Update explanation for current processing
            processing_text = Text(f"Processing node {current}", 
                                 font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(graph, RIGHT, buff=1.2)
            self.play(Write(processing_text), run_time=0.8)

            self.play(graphVertices[current].Highlight(), run_time=0.5)
            self.wait(0.3)

            neighbors_found = []
            # For DFS with directed graphs, we process neighbors in reverse order to maintain visual consistency
            for neighbor in reversed(adjacencyList[current]):
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
                    neighbors_found.append(neighbor)

                    # Show neighbor discovery temporarily
                    discovery_text = Text(f"Found unvisited neighbor {neighbor}", 
                                        font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE-4).next_to(processing_text, DOWN, buff=0.5)
                    self.play(Write(discovery_text), run_time=0.3)

                    self.play(
                        graphVertices[neighbor].Select(),
                        graph.edges[(current, neighbor)].animate.set_color(color=TEXTCOL),
                        run_time=0.5
                    )

                    DFSTree.append((current, neighbor))

                    self.wait(0.5)
                    
                    # Update stack display (constant at top)
                    new_stack_text = Text(f"Stack: [{', '.join(map(str, stack))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).move_to(stack_text)
                    self.play(ReplacementTransform(stack_text, new_stack_text), run_time=0.5)
                    stack_text = new_stack_text

                    # Fade out the discovery text
                    self.play(Unwrite(discovery_text), run_time=0.3)
                    self.wait(0.2)

            if not neighbors_found:
                no_neighbors_text = Text(f"No unvisited neighbors for {current}", 
                                       font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE-4).next_to(processing_text, DOWN, buff=0.5)
                self.play(Write(no_neighbors_text), run_time=0.5)
                self.wait(0.8)
                self.play(Unwrite(no_neighbors_text), run_time=0.3)

            self.play(Unwrite(processing_text), run_time=0.2)
            self.wait(0.5)

        self.play(Unwrite(stack_text), run_time=1.5)
        self.wait(2)
        self.play(graph.animate.remove_edges(*[edge for edge in graph.edges if edge not in DFSTree]), run_time=1.5)
        self.wait(0.5)
        self.play(graph.animate.center())
        self.wait(2)


class AdjecencyListD(Scene):
    def construct(self):
        def get_adjacency_list_VGroup(adjacency_list):
            # adjacency_text.to_edge(UP, buff=0.5)
            # self.play(Write(adjacency_text), run_time=1.5)

            adjacency_list_group = VGroup()
            for vertex, neighbors in adjacency_list.items():
                vertex_text = Text(f"{vertex}: ", font_size=FSIZE, font=FONT, color=TEXTCOL)
                neighbors_text = Text(", ".join(map(str, neighbors)), font_size=FSIZE, font=FONT, color=TEXTCOL)
                line = VGroup(vertex_text, neighbors_text).arrange(RIGHT, buff=0.3, aligned_edge=UP)
                adjacency_list_group.add(line)
            
            adjacency_list_group.arrange(DOWN, buff=0.5, aligned_edge=LEFT)

            adjacency_text = Text("Adjacency List", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(adjacency_list_group, UP, buff=1, aligned_edge=LEFT)
            
            return VGroup(adjacency_list_group, adjacency_text).next_to(graph, RIGHT, buff=2, aligned_edge=UP)

        vertices = [0, 1, 2, 3, 4]
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 3), (2, 4), (4, 3)]
        degrees = {0: 2, 1: 3, 2: 3, 3: 3, 4: 3}

        graph = DiGraph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
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
                graph.edges[(u, v)].animate.set_color(color=TEXTCOL),
                run_time=0.5
            )

            adjecencyList[u].append(v)

            self.play(
                adjecencyListVGroup[0].submobjects[u].animate.set_color(SELCOL),
                run_time=0.5
            )

            self.wait(0.6)

            newAdjacencyListVGroup = get_adjacency_list_VGroup(adjecencyList)
            self.play(ReplacementTransform(adjecencyListVGroup, newAdjacencyListVGroup), run_time=0.5)
            adjecencyListVGroup = newAdjacencyListVGroup

            self.play(
                graphVertices[u].Clear(), graphVertices[v].Clear(), 
                graph.edges[(u, v)].animate.set_color(color=EDGE_COL),
                run_time=0.5)
            
            self.wait(2)

        self.wait(2)

class WeightedUDGraphs(Scene):
    def construct(self):
        vertices = [3, 2, 0, 1, 4]
        wedges = [(0, 1, 10), (0, 3, 18), (1, 2, 20), (1, 3, 6), (2, 4, 8), (3, 4, 70)]
        edges = [(i, j) for i, j, _ in wedges]
        degrees = {0: 2, 1:3, 2:1, 3: 3, 4:2}
        edge_config = {(i, j):{'weight': w, "stroke_color": EDGE_COL, "stroke_width": 6} for i, j, w in wedges}

        graph = Graph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_type=WeightedLine,
                      edge_config=edge_config)
        
        # self.play(Create(graph), run_time=6)
        # self.wait(1)

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
            pointText = Text(f"{points[0]}-{points[1]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(edge.get_center(), direction=rotate_vector(edge.get_unit_vector(), PI / 2), buff=0.35)
            self.play(Create(edge), run_time=0.5)
            self.play(Write(pointText), run_time=0.2)

            if i == 0:
                # self.play(edge.animate.set_stroke(color=TEXTCOL), run_time=0.3)
                self.wait(0.1)
                nodeSurr = DashedVMobject(SurroundingRectangle(edge, color=TEXTCOL, buff=0.1, corner_radius=0.1), num_dashes=30).scale([0.7, 0.7, 1])
                nodeText = Text("Edge", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, LEFT, buff=0.15)
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

        self.wait(1)
        nodeSurr = DashedVMobject(SurroundingRectangle(list(graph.edges.values())[-1]._get_weight_mob(), color=TEXTCOL, buff=0.03, corner_radius=0.2))
        nodeText = Text("Weight", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeSurr, RIGHT + DOWN, buff=0.01)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)  

        self.wait(2)


class WeightedAdjecencyMatrixUD(Scene):
    def construct(self):
        vertices = [0, 1, 2, 3, 4]
        wedges = [(0, 1, 10), (0, 3, 18), (1, 2, 20), (1, 3, 6), (2, 4, 8), (3, 4, 70)]
        edges = [(i, j) for i, j, _ in wedges]
        degrees = {0: 2, 1:3, 2:1, 3: 3, 4:2}
        edge_config = {(i, j):{'weight': w, "stroke_color": EDGE_COL, "stroke_width": 6} for i, j, w in wedges}

        graph = Graph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_type=WeightedLine,
                      edge_config=edge_config)
        
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

        for u, v, w in wedges:
            self.play(
                graphVertices[u].Select(), graphVertices[v].Select(),
                *graph.edges[(u, v)].highlight_line(),
                run_time=0.5
            )
            ent_to_update1 = matrixTable.get_entries_without_labels(pos=(u+1, v+1))
            ent_to_update2 = matrixTable.get_entries_without_labels(pos=(v+1, u+1))
            cell_to_update1 = matrixTable.get_cell(pos=(u+2, v+2), color=SORTCOL).set_stroke(color=SORTCOL, width=7)
            cell_to_update2 = matrixTable.get_cell(pos=(v+2, u+2), color=SORTCOL).set_stroke(color=SORTCOL, width=7)
            adjecencyMatrix[u][v] = w
            adjecencyMatrix[v][u] = w

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
                    ent_to_update1, Integer(w).set_color(TEXTCOL).move_to(ent_to_update1)
                ),
                ReplacementTransform(
                    ent_to_update2, Integer(w).set_color(TEXTCOL).move_to(ent_to_update2)
                ),
                run_time=0.7
            )

            self.play(
                graphVertices[u].Clear(), graphVertices[v].Clear(), 
                FadeOut(cell_to_update1, cell_to_update2), 
                matrixTable.get_row_labels()[u].animate.set_color(TEXTCOL),
                matrixTable.get_row_labels()[v].animate.set_color(TEXTCOL),
                matrixTable.get_col_labels()[u].animate.set_color(TEXTCOL),
                matrixTable.get_col_labels()[v].animate.set_color(TEXTCOL),
                *graph.edges[(u, v)].clear_line(),
                run_time=0.5)
            
            self.wait(2)

        self.wait(4)


class WeightedAdjecencyListUD(Scene):
    def construct(self):
        def get_adjacency_list_VGroup(adjacency_list):
            # adjacency_text.to_edge(UP, buff=0.5)
            # self.play(Write(adjacency_text), run_time=1.5)

            adjacency_list_group = VGroup()
            for vertex, wneighbors in adjacency_list.items():
                vertex_text = Text(f"{vertex}: ", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL)
                neighbors_text = Text(", ".join(map(str, wneighbors)), font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL)
                line = VGroup(vertex_text, neighbors_text).arrange(RIGHT, buff=0.3, aligned_edge=UP)
                adjacency_list_group.add(line)
            
            adjacency_list_group.arrange(DOWN, buff=0.5, aligned_edge=LEFT)

            adjacency_text = Text("Adjacency List", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(adjacency_list_group, UP, buff=1, aligned_edge=LEFT)
            
            return VGroup(adjacency_list_group, adjacency_text).next_to(graph, RIGHT, buff=1.7, aligned_edge=UP)

        vertices = [0, 1, 2, 3, 4]
        wedges = [(0, 1, 10), (0, 3, 18), (1, 2, 20), (1, 3, 6), (2, 4, 8), (3, 4, 70)]
        edges = [(i, j) for i, j, _ in wedges]
        degrees = {0: 2, 1:3, 2:1, 3: 3, 4:2}
        edge_config = {(i, j):{'weight': w, "stroke_color": EDGE_COL, "stroke_width": 6} for i, j, w in wedges}

        graph = Graph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_type=WeightedLine,
                      edge_config=edge_config)
        
        graph.to_edge(LEFT, buff=1.2)
        self.play(Create(graph), run_time=5)
        self.wait(2)

        graphVertices = graph.vertices

        adjecencyList = {v: [] for v in vertices}
        adjecencyListVGroup = get_adjacency_list_VGroup(adjecencyList)
        self.play(Create(adjecencyListVGroup), run_time=0.5)

        for u, v, w in wedges:
            self.play(
                graphVertices[u].Select(), graphVertices[v].Select(),
                *graph.edges[(u, v)].highlight_line(),
                run_time=0.5
            )

            adjecencyList[u].append({v, w})
            adjecencyList[v].append({u, w})

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
                *graph.edges[(u, v)].clear_line(),
                run_time=0.5)
            
            self.wait(2)

        self.wait(4)


class WeightedDGraphs(Scene):
    def construct(self):
        vertices = [3, 2, 0, 1, 4]
        wedges = [(0, 1, 10), (0, 3, 18), (1, 2, 20), (1, 3, 6), (2, 4, 8), (3, 4, 70)]
        edges = [(i, j) for i, j, _ in wedges]
        degrees = {0: 2, 1:3, 2:1, 3: 3, 4:2}
        edge_config = {(i, j):{'weight': w, "stroke_color": EDGE_COL, "stroke_width": 6} for i, j, w in wedges}

        graph = DiGraph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_type=WeightedLine,
                      edge_config=edge_config)
        
        # self.play(Create(graph), run_time=6)
        # self.wait(1)

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
            pointText = Text(f"{points[0]}-{points[1]}", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(edge.get_center(), direction=rotate_vector(edge.get_unit_vector(), PI / 2), buff=0.35)
            self.play(Create(edge), run_time=0.5)
            self.play(Write(pointText), run_time=0.2)

            if i == 0:
                # self.play(edge.animate.set_stroke(color=TEXTCOL), run_time=0.3)
                self.wait(0.1)
                nodeSurr = DashedVMobject(SurroundingRectangle(edge, color=TEXTCOL, buff=0.1, corner_radius=0.1), num_dashes=30).scale([0.7, 1, 1])
                nodeText = Text("Edge", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, LEFT, buff=0.15)
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

        self.wait(1)
        nodeSurr = DashedVMobject(SurroundingRectangle(list(graph.edges.values())[-1]._get_weight_mob(), color=TEXTCOL, buff=0.07, corner_radius=0.2))
        nodeText = Text("Weight", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeSurr, RIGHT + DOWN, buff=0.01)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)  

        self.wait(2)


class WeightedAdjecencyMatrixD(Scene):
    def construct(self):
        vertices = [0, 1, 2, 3, 4]
        wedges = [(0, 1, 10), (0, 3, 18), (1, 2, 20), (1, 3, 6), (2, 4, 8), (4, 3, 70)]
        edges = [(i, j) for i, j, _ in wedges]
        degrees = {0: 2, 1:3, 2:1, 3: 3, 4:2}
        edge_config = {(i, j):{'weight': w, "stroke_color": EDGE_COL, "stroke_width": 6} for i, j, w in wedges}

        graph = DiGraph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_type=WeightedLine,
                      edge_config=edge_config)
        
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

        for u, v, w in wedges:
            self.play(
                graphVertices[u].Select(), graphVertices[v].Select(),
                *graph.edges[(u, v)].highlight_line(),
                run_time=0.5
            )
            ent_to_update1 = matrixTable.get_entries_without_labels(pos=(u+1, v+1))
            cell_to_update1 = matrixTable.get_cell(pos=(u+2, v+2), color=SORTCOL).set_stroke(color=SORTCOL, width=7)
            adjecencyMatrix[u][v] = w

            self.play(
                matrixTable.get_row_labels()[u].animate.set_color(SORTCOL),
                matrixTable.get_col_labels()[v].animate.set_color(SORTCOL),
                run_time=0.5
            )
            
            self.play(FadeIn(cell_to_update1), run_time=0.2)

            self.play(
                ReplacementTransform(
                    ent_to_update1, Integer(w).set_color(TEXTCOL).move_to(ent_to_update1)
                ),
                run_time=0.7
            )

            self.play(
                graphVertices[u].Clear(), graphVertices[v].Clear(), 
                FadeOut(cell_to_update1), 
                matrixTable.get_row_labels()[u].animate.set_color(TEXTCOL),
                matrixTable.get_col_labels()[v].animate.set_color(TEXTCOL),
                *graph.edges[(u, v)].clear_line(),
                run_time=0.5
            )
            
            self.wait(2)

        self.wait(4)


class WeightedAdjecencyListD(Scene):
    def construct(self):
        def get_adjacency_list_VGroup(adjacency_list):
            # adjacency_text.to_edge(UP, buff=0.5)
            # self.play(Write(adjacency_text), run_time=1.5)

            adjacency_list_group = VGroup()
            for vertex, wneighbors in adjacency_list.items():
                vertex_text = Text(f"{vertex}: ", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL)
                neighbors_text = Text(", ".join(map(str, wneighbors)), font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL)
                line = VGroup(vertex_text, neighbors_text).arrange(RIGHT, buff=0.3, aligned_edge=UP)
                adjacency_list_group.add(line)
            
            adjacency_list_group.arrange(DOWN, buff=0.5, aligned_edge=LEFT)

            adjacency_text = Text("Adjacency List", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(adjacency_list_group, UP, buff=1, aligned_edge=LEFT)
            
            return VGroup(adjacency_list_group, adjacency_text).next_to(graph, RIGHT, buff=1.7, aligned_edge=UP)

        vertices = [0, 1, 2, 3, 4]
        wedges = [(0, 1, 10), (0, 3, 18), (1, 2, 20), (1, 3, 6), (2, 4, 8), (4, 3, 70)]
        edges = [(i, j) for i, j, _ in wedges]
        degrees = {0: 2, 1:3, 2:1, 3: 3, 4:2}
        edge_config = {(i, j):{'weight': w, "stroke_color": EDGE_COL, "stroke_width": 6} for i, j, w in wedges}

        graph = Graph(vertices, edges, layout='circular', layout_scale=LAYOT_SCALE,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_type=WeightedLine,
                      edge_config=edge_config)
        
        graph.to_edge(LEFT, buff=1.2)
        self.play(Create(graph), run_time=5)
        self.wait(2)

        graphVertices = graph.vertices

        adjecencyList = {v: [] for v in vertices}
        adjecencyListVGroup = get_adjacency_list_VGroup(adjecencyList)
        self.play(Create(adjecencyListVGroup), run_time=0.5)

        for u, v, w in wedges:
            self.play(
                graphVertices[u].Select(), graphVertices[v].Select(),
                *graph.edges[(u, v)].highlight_line(),
                run_time=0.5
            )

            adjecencyList[u].append({v, w})

            self.play(
                adjecencyListVGroup[0].submobjects[u].animate.set_color(SELCOL),
                run_time=0.5
            )

            self.wait(0.6)

            newAdjacencyListVGroup = get_adjacency_list_VGroup(adjecencyList)
            self.play(ReplacementTransform(adjecencyListVGroup, newAdjacencyListVGroup), run_time=0.5)
            adjecencyListVGroup = newAdjacencyListVGroup

            self.play(
                graphVertices[u].Clear(), graphVertices[v].Clear(), 
                *graph.edges[(u, v)].clear_line(),
                run_time=0.5)
            
            self.wait(2)

        self.wait(4)


class Dijkstra(Scene):
    def construct(self):
        def add_dist(dist):
            distMob = VGroup()
            for i, distance in dist.items():
                distText = str(int(distance)) if distance != np.inf else "∞"
                distTextMob = Text(distText, font_size=WEIGHT_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(graphVertices[i], UP, buff=0.2)
                distMob.add(distTextMob)

            return distMob

        vertices = [0, 1, 2, 3, 4, 5, 6]
        wedges = [(0, 1, 10), (0, 2, 80), (1, 2, 6), (1, 4, 20), (2, 3, 70), (4, 5, 50), (4, 6, 5), (5, 6, 10)]
        edges = [(i, j) for i, j, _ in wedges]

        adj_list = {v: [] for v in vertices}
        for i, j, w in wedges:
            adj_list[i].append((j,w))

        scale = 1.4

        layout = {
            0: [0 * scale, 3 * scale, 0],
            1: [-1 * scale, 1.5 * scale, 0],
            2: [1 * scale, 1.5 * scale, 0],
            3: [2.2 * scale, 0 * scale, 0],
            4: [0.2 * scale, 0 * scale, 0],
            5: [-1 * scale, -1.5 * scale, 0],
            6: [1.5 * scale, -1.5 * scale, 0],
        }

        edge_config = {(i, j):{'weight': w, "stroke_color": EDGE_COL, "stroke_width": 6} for i, j, w in wedges}

        graph = DiGraph(vertices, edges, layout=layout, #layout='circular', layout_scale=3,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_type=WeightedLine,
                      edge_config=edge_config).center()
        
        self.play(Create(graph), run_time=6)
        self.wait(0.5)
        self.play(graph.animate.to_edge(LEFT, buff=1.3), run_time=1.5)
        self.wait(1)

        graphVertices = graph.vertices

        start = 0
        dist = {i: float('inf') for i in range(len(vertices))}
        
        distMob = add_dist(dist)
        self.play(FadeIn(distMob))

        dist[start] = 0 

        nodeSurr = DashedVMobject(SurroundingRectangle(graphVertices[0], color=TEXTCOL, buff=0.15, corner_radius=0.6))
        nodeText = Text("Starting Node", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeSurr, RIGHT, buff=0.1)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)


        newDistMob = add_dist(dist)
        self.play(ReplacementTransform(distMob, newDistMob), run_time=0.5)
        distMob = newDistMob

        self.wait(1)

        nodeSurr = DashedVMobject(SurroundingRectangle(distMob[2], color=TEXTCOL, buff=0.08, corner_radius=0.06))
        nodeText = Text("<- Current Best Distance\n      From Start", font=FONT, color=TEXTCOL, font_size=WEIGHT_FONT_SIZE).next_to(nodeSurr, RIGHT, buff=0.08).shift(DOWN * 0.1)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(0.7)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)  
        self.wait(0.7)
        

        visited = set()

        while len(visited) < len(vertices):
            min_node = None
            explanatory_text = Text("Selecting the unvisited \nnode with the minimum \ntentative distance", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(graph, RIGHT, buff=0.8).shift(UP * 0.2)
            self.play(Write(explanatory_text), run_time=0.5)
            self.wait(0.4)
            for node in range(len(vertices)):
                if node not in visited and (min_node is None or dist[node] < dist[min_node]):
                    min_node = node

            if min_node is None:
                break
            
            visited.add(min_node)

            subExplanatory_text = Text("Selected Node: " + str(min_node), font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(explanatory_text, DOWN, buff=0.5)
            self.play(Write(subExplanatory_text), run_time=0.5)
            self.wait(0.1)
            self.play(graphVertices[min_node].Select())
            self.wait(0.3)
            self.play(FadeOut(explanatory_text, subExplanatory_text), run_time=0.5)
            self.wait(0.4)
            explanatory_text = Text("Updating distances \nto the neighbouring \nnodes", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(graph, RIGHT, buff=0.8).shift(UP * 0.2)
            self.play(Write(explanatory_text), run_time=0.5)
            self.wait(0.7)

            for neighbor, weight in adj_list[min_node]:
                if neighbor not in visited:
                    nodeSurr = DashedVMobject(SurroundingRectangle(graphVertices[neighbor], color=TEXTCOL, buff=0, corner_radius=0.52))
                    self.play(Create(nodeSurr), run_time=0.3)
                    self.wait(0.1)
                    self.play(graph.edges[(min_node, neighbor)].highlight_line())
                    self.wait(0.4)

                    new_dist = dist[min_node] + weight
                    
                    subExplanatory_text = Text(f"New Distance = {dist[min_node]} + {weight}", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(explanatory_text, DOWN, buff=0.5)
                    self.play(Write(subExplanatory_text), run_time=0.2)
                    self.wait(0.6)
                    self.play(FadeOut(subExplanatory_text), run_time=0.2)
                    self.wait(0.4)
                    if new_dist < dist[neighbor]:
                        dist_test = str(dist[neighbor]) if dist[neighbor] != float('inf') else "∞"
                        subExplanatory_text = Text(f"{new_dist} < {dist_test}", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(explanatory_text, DOWN, buff=0.5)
                        self.play(Write(subExplanatory_text), run_time=0.2)
                        self.wait(0.5)

                        dist[neighbor] = new_dist

                        # newDistMob = add_dist(dist)
                        # self.play(ReplacementTransform(distMob, newDistMob), run_time=0.5)
                        # distMob = newDistMob
                        self.play(distMob.submobjects[neighbor].animate.become(
                            Text(str(int(dist[neighbor])), font_size=WEIGHT_FONT_SIZE, font=FONT, color=TEXTCOL).move_to(distMob.submobjects[neighbor])
                        ))
                        self.wait(0.2)
                    else:
                        subExplanatory_text = Text(f"{new_dist} > {dist[neighbor]}", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(explanatory_text, DOWN, buff=0.5)
                        self.play(Write(subExplanatory_text), run_time=0.2)
                        self.wait(0.5)
                    
                    self.play(FadeOut(subExplanatory_text), run_time=0.2)
                    self.wait(0.2)
                    self.play(FadeOut(nodeSurr), graph.edges[(min_node, neighbor)].clear_line(), run_time=0.2)
                else:
                    nodeSurr = DashedVMobject(SurroundingRectangle(graphVertices[neighbor], color=SELCOL, buff=0, corner_radius=0.52))
                    self.play(Create(nodeSurr), run_time=0.3)
                    self.wait(0.1)
                    subExplanatory_text = Text(f"Node {neighbor} already visited", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(explanatory_text, DOWN, buff=0.5)
                    self.play(Write(subExplanatory_text), run_time=0.2)
                    self.wait(0.6)
                    self.play(FadeOut(subExplanatory_text, nodeSurr), run_time=0.2)

            self.play(FadeOut(explanatory_text), run_time=0.5)
            
            explanatory_text = Text("Marking the selected \nnode as visited", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(graph, RIGHT, buff=0.8).shift(UP * 0.2)
            self.play(Write(explanatory_text), run_time=0.3)
            self.wait(0.4)
            self.play(graphVertices[min_node].Clear(), run_time=0.5)
            self.play(*graphVertices[min_node].Highlight())
            self.play(FadeOut(explanatory_text), run_time=0.2)
            
        self.wait(0.2)

        self.play(VGroup(graph, distMob).animate.center())

        self.wait(4)


class BellmanFord(Scene):
    def construct(self):
        def add_dist(dist):
            distMob = VGroup()
            for i, distance in dist.items():
                distText = str(int(distance)) if distance != np.inf else "∞"
                distTextMob = Text(distText, font_size=WEIGHT_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(graphVertices[i], UP, buff=0.2)
                if i == 2:
                    distTextMob.shift(LEFT * 0.4).shift(DOWN * 0.15)
                distMob.add(distTextMob)

            return distMob

        vertices = [0, 1, 2, 3, 4, 5, 6, 7]
        wedges = [(0, 7, 8), (0, 1, 10), (7, 6, 1), (6, 1, -4), (1, 5, 2), (6, 5, -1), (5, 2, -2), (2, 1, 1), (2, 3, 1), (3, 4, 3), (4, 5, -1)]
        edges = [(i, j) for i, j, _ in wedges]

        scale = 1.8

        layout = {
            0: [-0.8 * scale, 0.3 * scale, 0],
            1: [-1.5 * scale, -1.1 * scale, 0],
            7: [0.8 * scale, 0.3 * scale, 0],
            6: [1.5 * scale ,-1.1 * scale, 0],
            5: [0 * scale ,-2.2 * scale, 0],
            2: [-1.5 * scale ,-3.3 * scale, 0],
            3: [0 * scale ,-3.3 * scale, 0],
            4: [1.5 * scale ,-3.3 * scale, 0],
        }

        edge_config = {(i, j):{'weight': w, "stroke_color": EDGE_COL, "stroke_width": 6} for i, j, w in wedges}

        graph = DiGraph(vertices, edges, layout=layout, #layout='circular', layout_scale=3,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_type=WeightedLine,
                      edge_config=edge_config).center()
        
        self.play(Create(graph), run_time=6)
        self.wait(0.5)
        self.play(graph.animate.to_edge(LEFT, buff=1.3), run_time=1.5)
        self.wait(1)

        graphVertices = graph.vertices

        start = 0
        dist = {i: float('inf') for i in range(len(vertices))}

        dist[start] = 0

        distMob = add_dist(dist)
        self.play(FadeIn(distMob))
        self.wait(1)

        for _ in range(len(vertices) - 1):
            itterText = Text(f"Iteration {_}", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(graph, RIGHT, buff=1.7).shift(UP * 0.6)
            self.play(Write(itterText), run_time=0.2)

            for u, v, weight in wedges:
                edgeText = Text(f"{u} -> {v} ({weight})", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(itterText, DOWN, buff=0.5)
                self.play(Write(edgeText), run_time=0.2)
                self.play(
                    graphVertices[u].Select(),
                    graphVertices[v].Select(),
                    graph.edges[(u, v)].highlight_line(),
                    run_time=0.3
                )

                self.wait(0.1)

                distV = str(dist[v]) if dist[v] != float('inf') else "∞"
                if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                    explanatoryText = Text(f"Updating : {dist[u]} + {weight} < {distV}", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(edgeText, DOWN, buff=0.8)
                    self.play(Write(explanatoryText), run_time=0.2)
                    
                    dist[v] = dist[u] + weight

                    self.play(distMob.submobjects[v].animate.become(
                        Text(str(int(dist[v])), font_size=WEIGHT_FONT_SIZE, font=FONT, color=TEXTCOL).move_to(distMob.submobjects[v])
                    ))
                    self.wait(0.2)

                    self.play(FadeOut(explanatoryText), run_time=0.2)
                    self.wait(0.1)
                else:
                    explanatoryText = Text(f"No Update : {dist[u]} + {weight} >= {distV}", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(edgeText, DOWN, buff=0.8)
                    self.play(Write(explanatoryText), run_time=0.2)
                    self.wait(0.6)
                    self.play(FadeOut(explanatoryText), run_time=0.2)
                    self.wait(0.1)

                self.play(
                    FadeOut(edgeText),
                    graphVertices[u].Clear(),
                    graphVertices[v].Clear(),
                    graph.edges[(u, v)].clear_line(),
                    run_time=0.1
                )
                self.wait(0.1)
            
            self.wait(0.1)
            self.play(FadeOut(itterText), run_time=0.2)
            self.wait(0.2)

        self.wait(2)
        self.play(VGroup(graph, distMob).animate.center())
        self.wait(4)


class FloydWarshall(Scene):
    def construct(self):
        def get_path(u, v, nextMatrix):
            if nextMatrix[u][v] == -1:
                return []  # No path
            path = [u]
            while u != v:
                u = nextMatrix[u][v]
                if u == -1:
                    return []  # No complete path
                path.append(u)
            return path
        
        
        vertices = [0, 1, 2, 3, 4, 5, 6, 7]
        wedges = [(0, 7, 8), (0, 1, 10), (7, 6, 1), (6, 1, -4), (1, 5, 2), (6, 5, -1), (5, 2, -2), (2, 1, 1), (2, 3, 1), (3, 4, 3), (4, 5, -1)]
        edges = [(i, j) for i, j, _ in wedges]

        scale = 1.5

        layout = {
            0: [-0.8 * scale, 0.3 * scale, 0],
            1: [-1.5 * scale, -1.1 * scale, 0],
            7: [0.8 * scale, 0.3 * scale, 0],
            6: [1.5 * scale ,-1.1 * scale, 0],
            5: [0 * scale ,-2.2 * scale, 0],
            2: [-1.5 * scale ,-3.3 * scale, 0],
            3: [0 * scale ,-3.3 * scale, 0],
            4: [1.5 * scale ,-3.3 * scale, 0],
        }

        edge_config = {(i, j):{'weight': w, "stroke_color": EDGE_COL, "stroke_width": 6} for i, j, w in wedges}

        graph = DiGraph(vertices, edges, layout=layout, #layout='circular', layout_scale=3,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_type=WeightedLine,
                      edge_config=edge_config).center()
        
        self.play(Create(graph), run_time=6)
        self.wait(0.5)
        self.play(graph.animate.to_edge(LEFT, buff=0.8), run_time=1.5)
        self.wait(1)

        graphVertices = graph.vertices

        adjMatrix = np.full((len(vertices), len(vertices)), np.inf)
        np.fill_diagonal(adjMatrix, 0)
        for u, v, w in wedges:
            adjMatrix[u][v] = w


        adjMatrixText = []
        for u in range(len(vertices)):
            row = []
            for v in range(len(vertices)):
                if adjMatrix[u][v] == np.inf:
                    row.append(MathTex(r"\infty", font_size=EXPLANATORY_FONT_SIZE, color=TEXTCOL))
                else:
                    row.append(Text(str(int(adjMatrix[u][v])), font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL, weight=THIN))
            adjMatrixText.append(row)

        
        matrixTable = MobjectTable(
            adjMatrixText,
            row_labels=[Text(str(v), font_size=FSIZE, font=FONT) for v in vertices],
            col_labels=[Text(str(v), font_size=FSIZE, font=FONT) for v in vertices],
            include_outer_lines=True,
            v_buff=0.3,
            h_buff=0.4,
            top_left_entry = MathTex("SP_1", font_size=FSIZE),
        )

        for mob in matrixTable.get_entries():
            mob.set_color(TEXTCOL)

        for line in matrixTable.get_horizontal_lines() + matrixTable.get_vertical_lines():
            line.set_stroke(color=EDGE_COL, width=3.5)
        
        
        SP_Text = Text("Shortest Pair", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(matrixTable, UP, 0.3)
        self.play(Create(VGroup(matrixTable, SP_Text).next_to(graph, RIGHT, buff=1)), run_time=1.5)   
        self.wait(1.2)


        self.play(VGroup(graph, matrixTable, SP_Text).animate.shift(DOWN * 0.6))

        nextMatrix = np.full((len(vertices), len(vertices)), -1)
        for u, v, w in wedges:
            nextMatrix[u][v] = v  # direct edge goes to v


        ittrText = Text(f"Iteration : 1", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(graph, UP, buff=1)
        for k in range(1, len(vertices)):
            kittrText = Text(f"Iteration : {k+1}", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(graph, UP, buff=1)
            # nodeSurr = DashedVMobject(SurroundingRectangle(graphVertices[k], color=TEXTCOL, buff=0, corner_radius=0.52))
            self.play(matrixTable.get_entries(pos=(1,1)).animate.become(
                MathTex(f"SP_{k+1}", font_size=FSIZE, color=TEXTCOL).move_to(matrixTable.get_entries(pos=(1,1))),
                ),
                ittrText.animate.become(kittrText),
                # Create(nodeSurr),
                run_time=0.5
            )
            for u in range(len(vertices)):
                for v in range(len(vertices)):
                    if adjMatrix[u][v] > adjMatrix[u][k] + adjMatrix[k][v]:
                        uvText = int(adjMatrix[u][v]) if adjMatrix[u][v] != np.inf else "∞"
                        explanatoryText = Text(f"{u} -> {v} : {uvText} > {int(adjMatrix[u][k])} + {int(adjMatrix[k][v])}", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(SP_Text, UP, buff=0.6)
                        self.play(Write(explanatoryText), run_time=0.2)
                        self.wait(0.3)

                        ent_to_update1 = matrixTable.get_entries_without_labels(pos=(u+1, v+1))
                        cell_to_update1 = matrixTable.get_cell(pos=(u+2, v+2), color=SORTCOL).set_stroke(color=SORTCOL, width=7)
                        
                        adjMatrix[u][v] = adjMatrix[u][k] + adjMatrix[k][v]
                        nextMatrix[u][v] = nextMatrix[u][k]

                        path1 = get_path(u, k, nextMatrix)
                        path2 = get_path(k, v, nextMatrix)[1:] if nextMatrix[k][v] != -1 else []
                        full_path = path1 + path2 
                        evaluated_edges = [(full_path[i], full_path[i+1]) for i in range(len(full_path)-1)]
                        edges_to_highlight = [graph.edges[e] for e in evaluated_edges if e in graph.edges]

                        self.play(
                            graphVertices[u].Select(), graphVertices[v].Select(),
                            *[edge.highlight_line() for edge in edges_to_highlight],
                            run_time=0.3
                        )

                        self.wait(0.4)
                        self.play(FadeIn(cell_to_update1), run_time=0.2)
                        self.wait(0.2)

                        self.play(
                            matrixTable.get_entries_without_labels(pos=(u+1, v+1)).animate.become(
                                Text(str(int(adjMatrix[u][v])), font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL, weight=THIN).move_to(ent_to_update1)
                            ),
                            run_time=0.4
                        )
                        
                        self.wait(0.6)

                        self.play(
                            graphVertices[u].Clear(), graphVertices[v].Clear(),
                            *[edge.clear_line() for edge in edges_to_highlight],
                            Unwrite(explanatoryText), FadeOut(cell_to_update1),
                            run_time=0.3
                        )
                    
                    self.wait(0.1)
        self.wait(4)


class PrimsMCST(Scene):
    def construct(self):
        vertices = [0, 1, 2, 3, 4, 5, 6]
        wedges = [(0, 1, 10), (0, 2, 80), (1, 2, 6), (1, 4, 20), (2, 3, 70), (4, 5, 50), (4, 6, 5), (6, 5, 10)]
        edges = [(i, j) for i, j, _ in wedges]

        adj_list = {v: [] for v in vertices}
        for i, j, w in wedges:
            adj_list[i].append((j,w))
            adj_list[j].append((i,w))

        scale = 1.4

        layout = {
            0: [0 * scale, 3 * scale, 0],
            1: [-1 * scale, 1.5 * scale, 0],
            2: [1 * scale, 1.5 * scale, 0],
            3: [2.2 * scale, 0 * scale, 0],
            4: [0.2 * scale, 0 * scale, 0],
            5: [-1 * scale, -1.5 * scale, 0],
            6: [1.5 * scale, -1.5 * scale, 0],
        }

        edge_config = {(i, j):{'weight': w, "stroke_color": EDGE_COL, "stroke_width": 6} for i, j, w in wedges}

        graph = Graph(vertices, edges, layout=layout, #layout='circular', layout_scale=3,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_type=WeightedLine,
                      edge_config=edge_config).center()
        
        self.play(Create(graph), run_time=6)
        self.wait(0.5)
        self.play(graph.animate.to_edge(LEFT, buff=1.5), run_time=1.5)
        self.wait(1)

        graphVertices = graph.vertices

        visited, distance, TreeEdge, minCost = {}, {}, [], 0

        minCostText = Text("Minimum Cost: 0", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(graph, RIGHT, buff=1.3).shift(UP * 2)
        self.play(Write(minCostText), run_time=0.5)

        for v in vertices:
            visited[v] = False
            distance[v] = float('inf')

        visited[0] = True
        for v, d in adj_list[0]:
            distance[v] = d

        explanatoryText = Text(f"Selecting the egde with \nminimum weight connected \nto MST", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(graph, RIGHT, buff=1.3).shift(UP * 0.2)
        self.play(Write(explanatoryText), run_time=0.5)
        for i in range(1, len(vertices)):
            mindist = float('inf')
            nextv = None
            for u in vertices:
                for v, d in adj_list[u]:
                    if visited[u] and (not visited[v]):
                        try:
                            self.play(*graph.edges[(u, v)].select_line(), run_time = 0.3)
                            self.wait(0.3)
                            self.play(*graph.edges[(u, v)].deselect_line(), run_time = 0.2)
                        except KeyError:
                            self.play(*graph.edges[(v, u)].select_line(),run_time = 0.3)
                            self.wait(0.3)
                            self.play(*graph.edges[(v, u)].deselect_line(), run_time = 0.2)
                        
                        if d < mindist:
                            mindist = d
                            nextv = v
                            nexte = (u, v)

            subExplanatoryText = Text(f"Selected Edge: {nexte}, weight: {mindist}", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(explanatoryText, DOWN, buff=0.5)
            self.play(Write(subExplanatoryText), run_time=0.5)
            self.wait(0.4)
            
            visited[nextv] = True
            TreeEdge.append(nexte)
            minCost += mindist
            
            try:
                self.play(
                    *graph.edges[nexte].highlight_line(),
                    run_time=0.5
                )
            except KeyError:
                self.play(
                    *graph.edges[(nexte[1], nexte[0])].highlight_line(),
                    run_time=0.5
                )

            self.wait(0.2)

            self.play(
                minCostText.animate.become(
                    Text(f"Minimum Cost: {minCost}", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(graph, RIGHT, buff=1.7).shift(UP * 1.5)
                ),
                run_time=0.5
            )

            self.wait(0.3)
            
            self.play(FadeOut(subExplanatoryText), run_time=0.5)

            for v, d in adj_list[nextv]:
                if not visited[v] and d < distance[v]:
                    distance[v] = d

        
        # print(minCost)
        self.wait(1)
        self.play(
            FadeOut(explanatoryText),
            FadeOut(minCostText),
            run_time=0.5
        )
        self.wait(0.2)
        self.play(
            graph.animate.center(),
            run_time=0.5
        )

        self.wait(0.7)

        edges_not_in_mst = [e for e in graph.edges if e not in TreeEdge]
        self.play(
            FadeOut(*[graph.edges[e] for e in edges_not_in_mst]),
        )

        self.wait(4)
        # treeEdges = [graph.edges[e] for e in TreeEdge if e in graph.edges]


class KruskalMCST(Scene):
    def construct(self):
        vertices = [0, 1, 2, 3, 4, 5, 6]
        wedges = [(0, 1, 10), (0, 2, 80), (1, 2, 6), (1, 4, 20), (2, 3, 70), (4, 5, 50), (4, 6, 5), (5, 6, 10)]
        edges = [(i, j) for i, j, _ in wedges]

        adj_list = {v: [] for v in vertices}
        for i, j, d in wedges:
            adj_list[i].append((j,d))
            adj_list[j].append((i,d))

        scale = 1.4

        layout = {
            0: [0 * scale, 3 * scale, 0],
            1: [-1 * scale, 1.5 * scale, 0],
            2: [1 * scale, 1.5 * scale, 0],
            3: [2.2 * scale, 0 * scale, 0],
            4: [0.2 * scale, 0 * scale, 0],
            5: [-1 * scale, -1.5 * scale, 0],
            6: [1.5 * scale, -1.5 * scale, 0],
        }

        edge_config = {(i, j):{'weight': w, "stroke_color": EDGE_COL, "stroke_width": 6} for i, j, w in wedges}

        graph = Graph(vertices, edges, layout=layout, #layout='circular', layout_scale=3,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_type=WeightedLine,
                      edge_config=edge_config).center()
        
        self.play(Create(graph), run_time=6)
        self.wait(0.5)
        self.play(graph.animate.to_edge(LEFT, buff=1.5), run_time=1.5)
        self.wait(1)

        graphVertices = graph.vertices

        edgesK, component, TreeEdge, minCost = [], {}, [], 0

        for u in adj_list:
            edgesK.extend([(d, u, v) for v, d in adj_list[u]])
            component[u] = u

        edgesK = sorted(edgesK, key=lambda x: x[0])  # Sort edges by weight

        minCostText = Text("Minimum Cost: 0", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(graph, RIGHT, buff=1.7).shift(UP * 2)
        self.play(Write(minCostText), run_time=0.5)
        self.wait(0.3)
        explanatoryText = Text("Selecting edge with the \nsmallest weights that do \nnot create a cycle in \nthe MST", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(graph, RIGHT, buff=1.3).shift(UP * 0.2)
        self.play(Write(explanatoryText), run_time=0.5)
        self.wait(0.5)
        
        for d, u, v in edgesK:
            if component[u] != component[v]:
                TreeEdge.append((u, v))

                subExplanatoryText = Text(f"Selected Edge: ({u}, {v}), weight: {d}", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(explanatoryText, DOWN, buff=0.5)
                self.play(Write(subExplanatoryText), run_time=0.5)

                self.wait(0.2)

                self.play(
                    *graph.edges[(u, v)].highlight_line(),
                    run_time=0.5
                )

                c = component[u]

                minCost += d
                self.play(
                    minCostText.animate.become(
                        Text(f"Minimum Cost: {minCost}", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(graph, RIGHT, buff=1.7).shift(UP * 2)
                    ),
                    run_time=0.5
                )

                self.wait(0.2)
                self.play(FadeOut(subExplanatoryText), run_time=0.5)

                for w in adj_list:
                    if component[w] == c:
                        component[w] = component[v]

        self.wait(1)
        self.play(
            FadeOut(explanatoryText),
            FadeOut(minCostText),
            run_time=0.5
        )

        explanatoryText = Text("All Components \nare connected", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(graph, RIGHT, buff=1.3).shift(UP * 0.2)
        self.play(Write(explanatoryText), run_time=0.5)
        self.wait(0.4)
        self.play(FadeOut(explanatoryText),run_time=0.5)

        self.wait(0.2)
        self.play(
            graph.animate.center(),
            run_time=0.5
        )

        self.wait(0.7)
        edges_not_in_mst = [e for e in graph.edges if e not in TreeEdge]
        self.play(
            FadeOut(*[graph.edges[e] for e in edges_not_in_mst]),
        )

        self.wait(4)


class DAGArrow(Arrow): #There was some wierd bug with DiGraph, that it was not placing the arrow center to center of the vertices, so I had to create a custom arrow class
    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(buff=0.46, *args, **kwargs)

class TopologicalSort(Scene):
    def construct(self):
        from collections import deque
        vertices = [0, 1, 2, 3, 4, 5, 6, 7]
        verticesGraph = [3, 1, 2, 0, 4, 7, 6, 5]
        edges = [(0,2), (0,3), (0,4), (1,2), (1,7), (2,5), (3,5), (3,7), (4,7), (5,6), (6,7)]
        
        adj_list = {v: [] for v in vertices}
        for i, j in edges:
            adj_list[i].append(j)

        graph = Graph(verticesGraph, edges, layout='circular', layout_scale=2.7,
                      vertex_mobjects={v : Node(v) for v in vertices},
                      edge_config={"stroke_color": EDGE_COL, "stroke_width": 6},
                      edge_type=DAGArrow,)
                
        self.play(Create(graph), run_time=6)
        self.wait(0.5)
        self.play(graph.animate.to_edge(LEFT, buff=0.5), run_time=1.5)
        self.wait(1)

        graphVertices = graph.vertices


        indegree, topSort, zerodegreeq = {v:0 for v in vertices}, [], deque()

        for u in adj_list:
            for v in adj_list[u]:
                indegree[v] += 1


        indegreeVgroup = VGroup()
        for v in vertices:
            indegreeVgroup.add(
                Text(str(indegree[v]), font_size=WEIGHT_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(graphVertices[v], DOWN, buff=0.1)
            )

        self.play(FadeIn(indegreeVgroup, lag_ratio=0.1), run_time=0.5)
        self.wait(0.5)
        nodeSurr = DashedVMobject(SurroundingRectangle(indegreeVgroup.submobjects[1], color=TEXTCOL, buff=0.1, corner_radius=0.15))
        nodeText = Text("<-Indegree", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeSurr, RIGHT, buff=0.08)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

        for v in vertices:
            if indegree[v] == 0:
                zerodegreeq.append(v)

        explanatoryText = Text(f"Selecting the vertex\nwith zero indegree", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(graph, RIGHT, buff=0.7).shift(UP * 0.2)
        self.play(Write(explanatoryText), run_time=0.5)

        topSortVGroup = VGroup(Text("t")).shift(UP * 3.4).shift(LEFT * 2.5)

        while zerodegreeq:
            curr_vertex = zerodegreeq.popleft()
            subExplanatoryText = Text(f"Selected Vertex: {curr_vertex}", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(explanatoryText, DOWN, buff=0.5)
            self.play(Write(subExplanatoryText), run_time=0.5)
            self.wait(0.4)
            self.play(graphVertices[curr_vertex].Select(), run_time=0.5)
            self.wait(0.3)

            topSort.append(curr_vertex)
            indegree[curr_vertex] -= 1

            for adj_vertex in adj_list[curr_vertex]:
                indegree[adj_vertex] -= 1

                self.play(FadeOut(graph.edges[(curr_vertex, adj_vertex)]))
                self.remove(graph.edges[(curr_vertex, adj_vertex)])
                self.wait(0.2)

                self.play(
                    indegreeVgroup.submobjects[adj_vertex].animate.become(
                        Text(str(indegree[adj_vertex]), font_size=WEIGHT_FONT_SIZE, font=FONT, color=TEXTCOL).move_to(indegreeVgroup.submobjects[adj_vertex])
                    )
                )

                if indegree[adj_vertex] == 0:
                    zerodegreeq.append(adj_vertex)

            self.wait(0.2)
            self.play(FadeOut(indegreeVgroup.submobjects[curr_vertex]))
            self.remove(indegreeVgroup.submobjects[curr_vertex])
            self.wait(0.1)
            self.play(graphVertices[curr_vertex].animate.next_to(topSortVGroup, RIGHT, buff=0.27))
            topSortVGroup.add(graphVertices[curr_vertex])
            self.wait(0.3)
            self.play(FadeOut(subExplanatoryText), run_time=0.5)
            self.wait(0.2)

        self.play(FadeOut(explanatoryText), run_time=0.5)
        self.wait(0.3)
        self.play(topSortVGroup.animate.center())
        self.wait(4)