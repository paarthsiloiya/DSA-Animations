"""Shared visual building blocks for the scene modules (plan card R1).

One canonical implementation of the classes and helpers that used to be
copy-pasted across the animation files. Colors, fonts and layout constants
come from ``env_config``; scene files import only what they use.
"""

from typing import Any

from env_config import *
from manim import *


class ListElement(VGroup):
    def __init__(self, value: str | int, size: float = 0.8, font_mul: int = 100):
        super().__init__()
        self.size = size
        self.value = value if isinstance(value, str) and value.isalpha() else int(value)
        self.isFound = False
        self.isSorted = False
        self.elementValue = Text(str(value), font_size=(font_mul * self.size), color=TEXTCOL, font=FONT)
        self.circle = Circle(radius=self.size, color=BASECOL, fill_opacity=1)
        self.elementValue.move_to(self.circle.get_center())
        self.add(self.circle, self.elementValue)

    def getListElement(self):
        return self

    def SelectElement(self):
        return self.circle.animate.set_stroke(color=SELCOL, width=10)

    def Select(self):
        return self.circle.animate.set_stroke(color=SELCOL, width=10)

    def ClearSelection(self):
        if not (self.isFound or self.isSorted):
            return self.circle.animate.set_stroke(color=BASECOL)
        return self.circle.animate.set_stroke(color=SORTCOL)

    def Clear(self):
        if not (self.isFound or self.isSorted):
            return self.circle.animate.set_stroke(color=BASECOL)
        return self.circle.animate.set_stroke(color=SORTCOL)

    def MarkFound(self):
        self.isFound = True
        return self.circle.animate.set_fill(color=SORTCOL).set_stroke(width=0), self.elementValue.animate.set_color(color=WHITE)

    def MarkSorted(self):
        self.isSorted = True
        return self.circle.animate.set_fill(color=SORTCOL).set_stroke(width=0), self.elementValue.animate.set_color(color=WHITE)

    def Reset(self):
        self.isSorted = False
        return self.circle.animate.set_fill(color=BASECOL).set_stroke(color=BASECOL), self.elementValue.animate.set_color(color=TEXTCOL)


class Node(VGroup):
    def __init__(self, value, radius: float = 0.5, font_size: int = FSIZE):
        super().__init__()
        self.text = Text(str(value), font=FONT, color=TEXTCOL, font_size=font_size)
        self.circle = Circle(radius=radius, color=NODE_COL, fill_color=NODE_COL, fill_opacity=1, stroke_width=0)
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


class WeightedLine(Line):
    def __init__(
        self,
        *args: Any,
        weight: str | float | None = None,
        weight_config: dict | None = None,
        weight_alpha: float = 0.5,
        weight_font: str | None = None,
        bg_config: dict | None = None,
        add_bg: bool = True,
        standalone_bg: bool = False,
        **kwargs: Any,
    ):
        self.weight = weight
        self.alpha = weight_alpha
        self.add_bg = add_bg
        self.standalone_bg = standalone_bg
        super().__init__(*args, **kwargs)

        self.weight_config = {
            "color": TEXTCOL,
            "font_size": WEIGHT_FONT_SIZE,
        }
        if weight_font is not None:
            self.weight_config["font"] = weight_font

        if weight_config:
            self.weight_config.update(weight_config)

        if standalone_bg:
            self.bg_config = {
                "color": config.background_color,
                "fill_opacity": 1,
                "buff": 0.1,
            }
        else:
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
            if self.standalone_bg:
                self.bg = BackgroundRectangle(self.label, **self.bg_config)
                self.add(self.bg)
            else:
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


def make_dynamic_bezier_updater(start_mobj, end_mobj, offset_start=RIGHT*0.2, offset_end=LEFT*0.1, back=False):
    def updater(curve):
        if back:
            start = start_mobj.get_left() + offset_start
            end = end_mobj.get_right() + offset_end
            control1 = start + LEFT
            control2 = end + RIGHT
        else:
            start = start_mobj.get_right() + offset_start
            end = end_mobj.get_left() + offset_end
            control1 = start + RIGHT
            control2 = end + LEFT
        curve.become(CubicBezier(start, control1, control2, end, color=curve.color))
    return updater


def make_arrowhead_updater(bezier_curve, offset=0.01):
    def updater(arrowhead):
        end_point = bezier_curve.point_from_proportion(1)
        direction = bezier_curve.point_from_proportion(1) - bezier_curve.point_from_proportion(1 - offset)
        arrowhead.move_to(end_point)
        arrowhead.set_angle(angle_of_vector(direction))
    return updater


def play_surrounding_node_animation(scene, tree, node, text, dir):
    scene.play(tree.vertices[node].Select(), run_time=0.5)
    nodeSurr = DashedVMobject(SurroundingRectangle(tree.vertices[node], color=TEXTCOL, buff=0.15, corner_radius=0.6))
    nodeText = Text(text, font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, dir, buff=0.1)
    scene.play(Create(nodeSurr), run_time=0.5)
    scene.wait(0.2)
    scene.play(Write(nodeText), run_time=0.5)
    scene.wait(1.5)
    scene.play(tree.vertices[node].Clear(), Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)


def animate_traversal(
    scene,
    graph,
    adjacency_list,
    start,
    start_text,
    *,
    use_stack=False,
    container_shift=0.0,
    processing_buff=0.8,
    explanatory_font_size=EXPLANATORY_FONT_SIZE,
    neighbors_of=None,
    edge_highlight=None,
    on_visit=None,
):
    if neighbors_of is None:
        def neighbors_of(current):
            return adjacency_list[current]
    if edge_highlight is None:
        def edge_highlight(graph, edge):
            return graph.edges[edge].animate.set_stroke(color=TEXTCOL)
    label = "Stack" if use_stack else "Queue"
    visited = {v: False for v in adjacency_list}
    visited[start] = True
    container = [start]

    container_text = Text(f"{label}: [{', '.join(map(str, container))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.5).shift(RIGHT * container_shift)
    scene.play(Unwrite(start_text), Write(container_text), run_time=1)
    scene.wait(1)

    while container:
        if use_stack:
            current = container.pop()
        else:
            current = container.pop(0)
        new_container_text = Text(f"{label}: [{', '.join(map(str, container))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).move_to(container_text)
        scene.play(ReplacementTransform(container_text, new_container_text), run_time=0.5)
        container_text = new_container_text

        processing_text = Text(f"Processing node {current}", 
                             font=FONT, color=TEXTCOL, font_size=explanatory_font_size).next_to(graph, RIGHT, buff=processing_buff)
        scene.play(Write(processing_text), run_time=0.8)

        scene.play(graph.vertices[current].Highlight(), run_time=0.5)
        scene.wait(0.3)

        neighbors_found = []
        for neighbor in neighbors_of(current):
            if not visited[neighbor]:
                visited[neighbor] = True
                container.append(neighbor)
                neighbors_found.append(neighbor)

                discovery_text = Text(f"Found unvisited neighbor {neighbor}", 
                                    font=FONT, color=TEXTCOL, font_size=explanatory_font_size-4).next_to(processing_text, DOWN, buff=0.5)
                scene.play(Write(discovery_text), run_time=0.3)

                scene.play(
                    graph.vertices[neighbor].Select(),
                    edge_highlight(graph, (current, neighbor)),
                    run_time=0.5
                )

                if on_visit is not None:
                    on_visit(current, neighbor)

                scene.wait(0.5)

                new_container_text = Text(f"{label}: [{', '.join(map(str, container))}]", font=FONT, color=TEXTCOL, font_size=FSIZE).move_to(container_text)
                scene.play(ReplacementTransform(container_text, new_container_text), run_time=0.5)
                container_text = new_container_text

                scene.play(Unwrite(discovery_text), run_time=0.3)
                scene.wait(0.2)

        if not neighbors_found:
            no_neighbors_text = Text(f"No unvisited neighbors for {current}", 
                                   font=FONT, color=TEXTCOL, font_size=explanatory_font_size-4).next_to(processing_text, DOWN, buff=0.5)
            scene.play(Write(no_neighbors_text), run_time=0.5)
            scene.wait(0.8)
            scene.play(Unwrite(no_neighbors_text), run_time=0.3)

        scene.play(Unwrite(processing_text), run_time=0.2)
        scene.wait(0.5)

    scene.play(Unwrite(container_text), run_time=1.5)
    scene.wait(2)


def remove_edge_visual(scene, graph, u_value, v_value, u_node, v_node):
    removed = None
    for edge in list(graph.edges):
        if (edge[0] == u_value and edge[1] == v_value) or (edge[0] == v_value and edge[1] == u_value):
            for manim_edge in scene.mobjects:
                if isinstance(manim_edge, Line) and hasattr(manim_edge, 'start') and hasattr(manim_edge, 'end'):
                    start_close = np.allclose(manim_edge.get_start(), u_node.get_center(), atol=0.1)
                    end_close = np.allclose(manim_edge.get_end(), v_node.get_center(), atol=0.1)
                    start_close_rev = np.allclose(manim_edge.get_start(), v_node.get_center(), atol=0.1)
                    end_close_rev = np.allclose(manim_edge.get_end(), u_node.get_center(), atol=0.1)

                    if (start_close and end_close) or (start_close_rev and end_close_rev):
                        scene.play(FadeOut(manim_edge), run_time=0.3)
                        removed = manim_edge
                        break
            graph.remove_edge(*edge)
            return removed
    return None
