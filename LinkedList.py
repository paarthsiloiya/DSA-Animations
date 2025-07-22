from manim import *
from manim.utils.unit import Percent, Pixels
import random

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
EXPLANATORY_FONT_SIZE = 32  # For step-by-step explanations
POINTER_FONT_SIZE = 28      # For pointer labels (if any)

SELF_ADDRESS_FONT_SIZE = 21
NEXT_ADDRESS_FONT_SIZE = 25
VALUE_FONT_SIZE = 90
NODE_WIDTH = 1.6

SWAP_FONT_COLOR = SORTCOL
EXPLANATORY_FONT_COLOR = TEXTCOL
POINTER_FONT_COLOR = SORTCOL

class Node(VGroup):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.next : Node = None
        self.selfAddress = random.randint(1000, 9999)
        self.nextAddress = 0 if self.next is None else self.next.selfAddress

    def setValues(self):
        self.selfAddressText = Text(f"0x{self.selfAddress}", font_size=SELF_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT)
        self.selfAddressGroup = VGroup(
            self.selfAddressText,
            Rectangle(width=NODE_WIDTH, height=0.6, color=SORTCOL)
        )

        if self.next is None:
            self.nextAddressText = Text("NULL", font_size=NEXT_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT)
        else:
            self.nextAddressText = Text(f"0x{self.nextAddress}", font_size=NEXT_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT)
        self.nextAddressGroup = VGroup(
            self.nextAddressText,
            Rectangle(width=NODE_WIDTH, height=0.6, color=SORTCOL)
        )

        self.valueText = Text(str(self.value), font_size=VALUE_FONT_SIZE, color=TEXTCOL, font=FONT)
        self.valueTextGroup = VGroup(
            self.valueText,
            Rectangle(width=NODE_WIDTH, height=1.6, color=SORTCOL)
        )

        self.add(
            self.selfAddressGroup,
            self.valueTextGroup,
            self.nextAddressGroup,
        )
        self.arrange(DOWN, buff=0.0)

    def updateSelfAddress(self, new_address):
        self.selfAddress = new_address
        new_self_address_text = Text(f"0x{self.selfAddress}", font_size=SELF_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT).move_to(self.selfAddressText)
        return self.selfAddressText.animate.become(new_self_address_text)
    
    def updateNext(self, new_node):
        self.next : Node = new_node
        self.nextAddress = 0 if self.next is None else self.next.selfAddress
        if self.next is None:
            new_next_address_text = Text("NULL", font_size=NEXT_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT).move_to(self.nextAddressText)
        else:
            new_next_address_text = Text(f"0x{self.nextAddress}", font_size=NEXT_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT).move_to(self.nextAddressText)
        return self.nextAddressText.animate.become(new_next_address_text)
 

class NodeExplanation(Scene):
    def construct(self):
        node1 = Node(4)
        node2 = Node(1)

        node1.setValues()

        self.play(Create(node1))
        self.wait(0.4)

        surroundingRectangleNode = DashedVMobject(SurroundingRectangle(node1, buff=0.4, corner_radius=0.2, color=SORTCOL), num_dashes=30)
        self.play(Create(surroundingRectangleNode))
        explanatoryText = Text("NODE", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(surroundingRectangleNode, LEFT).shift(LEFT * 1.2)
        explanatoryText = VGroup(
            explanatoryText,
            Arrow(start=explanatoryText.get_right(), end=surroundingRectangleNode.get_left(), color=SORTCOL, tip_shape=StealthTip, max_stroke_width_to_length_ratio=4, max_tip_length_to_length_ratio=0.2)
        )

        self.play(Write(explanatoryText))
        self.wait(0.7)
        self.play(Unwrite(explanatoryText), FadeOut(surroundingRectangleNode))
        self.wait(0.3)

        explanatoryTextGroup = VGroup()

        explanatoryText = Text("Address of\nthis node", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(node1.selfAddressGroup, LEFT).shift(LEFT)
        explanatoryText = VGroup(
            explanatoryText,
            Arrow(start=explanatoryText.get_right(), end=node1.selfAddressGroup.get_left(), color=SORTCOL, tip_shape=StealthTip, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1)
        )
        self.play(Write(explanatoryText))
        explanatoryTextGroup.add(explanatoryText)


        explanatoryText = Text("Value of\nthis node", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(node1.valueTextGroup, LEFT).shift(LEFT)
        explanatoryText = VGroup(
            explanatoryText,
            Arrow(start=explanatoryText.get_right(), end=node1.valueTextGroup.get_left(), color=SORTCOL, tip_shape=StealthTip, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1)
        )
        self.play(Write(explanatoryText))
        explanatoryTextGroup.add(explanatoryText)


        explanatoryText = Text("Address of\nnext node", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(node1.nextAddressGroup, LEFT).shift(LEFT)
        explanatoryText = VGroup(
            explanatoryText,
            Arrow(start=explanatoryText.get_right(), end=node1.nextAddressGroup.get_left(), color=SORTCOL, tip_shape=StealthTip, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1)
        )
        self.play(Write(explanatoryText))
        explanatoryTextGroup.add(explanatoryText)

        self.wait(1.2)

        self.play(Unwrite(explanatoryTextGroup))

        self.play(node1.animate.shift(LEFT * 1.5))

        node1.next = node2

        node2.setValues()

        node2.shift(RIGHT * 1.5)
        self.play(Create(node2))


        start = node1.nextAddressGroup.get_right()
        end = node2.selfAddressGroup.get_left() + (LEFT * 0.1) 
        arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
        arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
        arrowhead.move_to(end)
        arrowhead.rotate(angle_of_vector(RIGHT))

        arrow = VGroup(arrowCurve, arrowhead)
        self.play(Create(arrow))
        self.play(node1.updateNext(node2))

        self.wait(1)

    
class CreateLinkedList(Scene):
    def construct(self):
        def make_dynamic_bezier_updater(start_mobj, end_mobj, offset_start=RIGHT*0.2, offset_end=LEFT*0.1):
            def updater(curve):
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
        
        values = [5, 2, 4, 6, 3, 1]
        nodes : list[Node] = []
        current : Node = None
        prev : Node = None
        nodeGroup = VGroup()

        head = Node(values[0])
        head.setValues()
        self.play(Create(head), run_time=0.8)

        self.add(nodeGroup)
        
        nodeGroup.add(head)
        nodes.append(head)

        for i in range(1, len(values)):
            newNode = Node(values[i])
            newNode.setValues()
            self.play(Create(newNode.shift(RIGHT * i * 2)), run_time=0.8)
            nodeGroup.add(newNode)
            nodes.append(newNode)
            
            self.play(nodeGroup.animate.arrange(RIGHT, 1), run_time=1)

            current = nodes[i]
            prev = nodes[i - 1]

            start = prev.nextAddressGroup.get_right()
            end = newNode.selfAddressGroup.get_left() + (LEFT * 0.1) 
            arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
            arrowCurve.add_updater(make_dynamic_bezier_updater(prev.nextAddressGroup, newNode.selfAddressGroup, 0, LEFT * 0.1))
            arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
            arrowhead.move_to(end)
            arrowhead.rotate(angle_of_vector(RIGHT))
            arrowhead.add_updater(make_arrowhead_updater(arrowCurve))

            arrow = VGroup(arrowCurve, arrowhead)
            self.play(Create(arrow), run_time=0.6)
            self.play(prev.updateNext(newNode), run_time=0.5)
            self.wait(0.5)

        self.wait(1)

        surroundingRectangleNode = DashedVMobject(SurroundingRectangle(nodeGroup.submobjects[0], color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
        self.play(Create(surroundingRectangleNode), run_time=0.5)
        explanatorText = Text("Head", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeGroup.submobjects[0], UP, buff=0.6)
        self.play(Write(explanatorText), run_time=0.5)
        self.wait(0.3)
        self.play(FadeOut(surroundingRectangleNode), FadeOut(explanatorText), run_time=0.3)

        self.wait(0.3)
        
        surroundingRectangleNode = DashedVMobject(SurroundingRectangle(nodeGroup.submobjects[-1], color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
        self.play(Create(surroundingRectangleNode), run_time=0.5)
        explanatorText = Text("Tail", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeGroup.submobjects[-1], UP, buff=0.6)
        self.play(Write(explanatorText), run_time=0.5)
        self.wait(0.3)
        self.play(FadeOut(surroundingRectangleNode), FadeOut(explanatorText), run_time=0.3)

        self.wait(1)


class TraverseLinkedList(Scene):
    def construct(self):
        def make_dynamic_bezier_updater(start_mobj, end_mobj, offset_start=RIGHT*0.2, offset_end=LEFT*0.1):
            def updater(curve):
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

        values = [5, 2, 4, 6, 3, 1]
        nodes : list[Node] = []
        head : Node = None
        current : Node = None

        nodeGroup = VGroup()
        arrows = VGroup()
        curves = VGroup()

        for value in values:
            newNode = Node(value)
            newNode.setValues()
            nodes.append(newNode)
            nodeGroup.add(newNode)

        nodeGroup.arrange(RIGHT, 1)
        self.play(FadeIn(nodeGroup))

        for i, node in enumerate(nodes[:-1]):
            
            start = node.nextAddressGroup.get_right()
            end = nodes[i + 1].selfAddressGroup.get_left() + (LEFT * 0.1)
            arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
            arrowCurve.add_updater(make_dynamic_bezier_updater(node.nextAddressGroup, nodes[i + 1].selfAddressGroup, 0, LEFT * 0.1))
            arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
            arrowhead.move_to(end)
            arrowhead.rotate(angle_of_vector(RIGHT))
            arrowhead.add_updater(make_arrowhead_updater(arrowCurve))

            curves.add(arrowCurve)
            arrow = VGroup(arrowCurve, arrowhead)
            arrows.add(arrow)
            self.play(Create(arrow), run_time=0.6)

            self.play(node.updateNext(nodes[i + 1]), run_time=0.1)

        self.wait(0.7)

        surroundingRectangleNode = DashedVMobject(SurroundingRectangle(nodes[0], color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
        self.play(Create(surroundingRectangleNode))
        self.wait(0.5)

        for arrow,node in zip(curves, nodes[1:]):
            pulse_dot = Dot(radius=0.15, color=WHITE)
            self.add(pulse_dot)

            self.play(
                MoveAlongPath(pulse_dot, arrow),
                run_time=1.2,
                rate_func=linear
            )

            self.remove(pulse_dot)
            self.wait(0.1)
            self.play(surroundingRectangleNode.animate.move_to(node), run_time=0.3)
            self.wait(0.3)

        self.play(FadeOut(surroundingRectangleNode))

        self.wait(1)


class LinkedListLength(Scene):
    def construct(self):
        def make_dynamic_bezier_updater(start_mobj, end_mobj, offset_start=RIGHT*0.2, offset_end=LEFT*0.1):
            def updater(curve):
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

        values = [5, 2, 4, 6, 3, 1]
        nodes : list[Node] = []
        head : Node = None
        current : Node = None

        nodeGroup = VGroup()
        arrows = VGroup()
        curves = VGroup()
        
        for value in values:
            newNode = Node(value)
            newNode.setValues()
            nodes.append(newNode)
            nodeGroup.add(newNode)

        nodeGroup.arrange(RIGHT, 1)
        self.play(FadeIn(nodeGroup))

        for i, node in enumerate(nodes[:-1]):
            
            start = node.nextAddressGroup.get_right()
            end = nodes[i + 1].selfAddressGroup.get_left() + (LEFT * 0.1)
            arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
            arrowCurve.add_updater(make_dynamic_bezier_updater(node.nextAddressGroup, nodes[i + 1].selfAddressGroup, 0, LEFT * 0.1))
            arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
            arrowhead.move_to(end)
            arrowhead.rotate(angle_of_vector(RIGHT))
            arrowhead.add_updater(make_arrowhead_updater(arrowCurve))

            curves.add(arrowCurve)
            arrow = VGroup(arrowCurve, arrowhead)
            arrows.add(arrow)
            self.play(Create(arrow), run_time=0.6)

            self.play(node.updateNext(nodes[i + 1]), run_time=0.1)

        self.wait(0.7)

        surroundingRectangleNode = DashedVMobject(SurroundingRectangle(nodes[0], color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
        self.play(Create(surroundingRectangleNode))
        self.wait(0.5)

        LengthText = Text(f"Length: 1", color=TEXTCOL, font=FONT, font_size=FSIZE).to_edge(UP, buff=1.0)
        self.play(Write(LengthText))
        i = 1

        for arrow,node in zip(curves, nodes[1:]):
            pulse_dot = Dot(radius=0.15, color=WHITE)
            self.add(pulse_dot)

            self.play(
                MoveAlongPath(pulse_dot, arrow),
                run_time=0.5,
                rate_func=linear
            )

            self.remove(pulse_dot)
            self.wait(0.1)
            i += 1
            self.play(surroundingRectangleNode.animate.move_to(node), run_time=0.3)
            self.play(LengthText.animate.become(Text(f"Length: {i}", color=TEXTCOL, font=FONT, font_size=FSIZE).to_edge(UP, buff=1.0)))
            self.wait(0.3)

        self.play(FadeOut(surroundingRectangleNode))

        self.wait(1)


class InsertNode(Scene):
    def construct(self):
        def make_dynamic_bezier_updater(start_mobj, end_mobj, offset_start=RIGHT*0.2, offset_end=LEFT*0.1):
            def updater(curve):
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


        values = [5, 2, 6, 3, 1]
        nodes : list[Node] = []
        nodeGroup = VGroup()
        arrows = []

        for value in values:
            newNode = Node(value)
            newNode.setValues()
            nodes.append(newNode)
            nodeGroup.add(newNode)

        nodeGroup.arrange(RIGHT, 1)
        self.play(Create(nodeGroup))

        for i, node in enumerate(nodes[:-1]):
            
            start = node.nextAddressGroup.get_right()
            end = nodes[i + 1].selfAddressGroup.get_left() + (LEFT * 0.1)
            arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
            arrowCurve.add_updater(make_dynamic_bezier_updater(node.nextAddressGroup, nodes[i + 1].selfAddressGroup, 0, LEFT * 0.1))
            arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
            arrowhead.move_to(end)
            arrowhead.rotate(angle_of_vector(RIGHT))
            arrowhead.add_updater(make_arrowhead_updater(arrowCurve))

            arrow = VGroup(arrowCurve, arrowhead)
            arrows.append(arrow)
            self.play(Create(arrow), run_time=0.6)

            self.play(node.updateNext(nodes[i + 1]), run_time=0.1)

        self.wait(0.5)
        self.play(nodeGroup.animate.shift(DOWN * 1.5))
        self.wait(1)

        newNode = Node(4)
        newNode.setValues()
        self.play(Create(newNode.shift(UP * 2.5).shift(LEFT * 1.5)), run_time=0.5)

        tempRect = DashedVMobject(SurroundingRectangle(newNode, color=SORTCOL, buff=0.2, corner_radius=0.2), 30)
        tempText = Text("New Node", color=SORTCOL, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(tempRect, LEFT, buff=0.2)
        self.play(Create(tempRect), Write(tempText))
        self.wait(0.5)
        self.play(FadeOut(tempRect), FadeOut(tempText))

        self.wait(1)

        pos = 1

        prevNode = nodes[pos]
        nextNode = nodes[pos + 1]

        self.wait(0.2)
        itterationRectangle = DashedVMobject(SurroundingRectangle(nodes[0], color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
        self.play(Create(itterationRectangle))
        for i in range(0, pos + 1):
            self.play(itterationRectangle.animate.move_to(nodes[i]), run_time=0.2)
            self.wait(0.2)

        # self.play(itterationRectangle.animate.move_to(newNode), run_time=0.3)
        self.wait(0.4)

        start = newNode.nextAddressGroup.get_right()
        end = nextNode.selfAddressGroup.get_left() + (LEFT * 0.1)
        arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
        arrowCurve.add_updater(make_dynamic_bezier_updater(newNode.nextAddressGroup, nextNode.selfAddressGroup, 0, LEFT * 0.1))
        arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
        arrowhead.move_to(end)
        arrowhead.rotate(angle_of_vector(RIGHT))
        arrowhead.add_updater(make_arrowhead_updater(arrowCurve))

        arrow = VGroup(arrowCurve, arrowhead)
        arrows.insert(pos, arrow)
        self.play(Create(arrow), run_time=0.6)

        self.play(newNode.updateNext(nextNode), run_time=0.3)

        self.wait(1)

        nodeGroup.insert(pos+1, newNode)

        self.play(Uncreate(arrows[pos+1]), run_time=0.3)
        self.wait(0.2)

        start = prevNode.nextAddressGroup.get_right()
        end = newNode.selfAddressGroup.get_left() + (LEFT * 0.1)
        arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
        arrowCurve.add_updater(make_dynamic_bezier_updater(prevNode.nextAddressGroup, newNode.selfAddressGroup, 0, LEFT * 0.1))
        arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
        arrowhead.move_to(end)
        arrowhead.rotate(angle_of_vector(RIGHT))
        arrowhead.add_updater(make_arrowhead_updater(arrowCurve))

        arrow = VGroup(arrowCurve, arrowhead)
        arrows.insert(pos, arrow)
        self.play(Create(arrow), run_time=0.6)

        self.play(prevNode.updateNext(newNode), run_time=0.3)
        self.wait(0.5)
        self.play(Uncreate(itterationRectangle), run_time=0.3)
        self.wait(0.6)
        self.play(nodeGroup.animate.arrange(RIGHT, 1), run_time=0.5)

        self.wait(1)


class Deletion(Scene):
    def construct(self):
        def make_dynamic_bezier_updater(start_mobj, end_mobj, offset_start=RIGHT*0.2, offset_end=LEFT*0.1):
            def updater(curve):
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

        values = [5, 2, 4, 6, 3, 1]
        nodes : list[Node] = []
        head : Node = None
        current : Node = None
        nodeGroup = VGroup()

        for value in values:
            newNode = Node(value)
            newNode.setValues()
            nodes.append(newNode)
            nodeGroup.add(newNode)

        nodeGroup.arrange(RIGHT, 1)
        self.play(FadeIn(nodeGroup))

        arrows = VGroup()
        for i in range(len(nodes) - 1): 
            start = nodes[i].nextAddressGroup.get_right()
            end = nodes[i + 1].selfAddressGroup.get_left() + (LEFT * 0.1)
            arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
            arrowCurve.add_updater(make_dynamic_bezier_updater(nodes[i].nextAddressGroup, nodes[i + 1].selfAddressGroup, 0, LEFT * 0.1))
            arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
            arrowhead.move_to(end)
            arrowhead.rotate(angle_of_vector(RIGHT))
            arrowhead.add_updater(make_arrowhead_updater(arrowCurve))

            arrow = VGroup(arrowCurve, arrowhead)
            arrows.add(arrow)
            self.play(Create(arrow), run_time=0.6)
            self.play(nodes[i].updateNext(nodes[i + 1]), run_time=0.1)

        self.wait(0.5)

        pos = 2
        delNode = nodes[pos]

        itterRectangle = DashedVMobject(SurroundingRectangle(nodes[0], color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
        self.play(Create(itterRectangle))

        for i in range(pos):
            self.play(itterRectangle.animate.move_to(nodes[i]), run_time=0.2)
            self.wait(0.2)

        tempRectangle = DashedVMobject(SurroundingRectangle(delNode, color=SORTCOL, buff=0.2, corner_radius=0.2), 30)
        tempText = Text("Temporary", color=SWAP_FONT_COLOR, font=FONT, font_size=SWAP_FONT_SIZE).next_to(tempRectangle, UP, buff=0.2)
        self.play(Create(tempRectangle), Write(tempText))

        self.wait(0.3)

        self.play(
            Uncreate(arrows.submobjects[pos-1]), 
            nodes[pos - 1].updateNext(None),
            run_time=0.3
        )

        self.wait(0.2)

        self.play(VGroup(delNode, tempRectangle, tempText).animate.shift(UP * 2),run_time=0.3)

        self.wait(0.5)

        self.play(
            Uncreate(arrows.submobjects[pos]),
            delNode.updateNext(None),
            run_time=0.3
        )

        self.wait(0.5)

        start = nodes[pos - 1].nextAddressGroup.get_right()
        end = nodes[pos + 1].selfAddressGroup.get_left() + (LEFT * 0.1)
        arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
        arrowCurve.add_updater(make_dynamic_bezier_updater(nodes[pos - 1].nextAddressGroup, nodes[pos + 1].selfAddressGroup, 0, LEFT * 0.1))
        arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
        arrowhead.move_to(end)
        arrowhead.rotate(angle_of_vector(RIGHT))
        arrowhead.add_updater(make_arrowhead_updater(arrowCurve))

        arrow = VGroup(arrowCurve, arrowhead)
        arrows.add(arrow)
        self.play(Create(arrow), run_time=0.6)
        self.play(nodes[pos - 1].updateNext(nodes[pos + 1]), run_time=0.1)

        self.wait(0.2)
        self.play(FadeOut(itterRectangle), run_time=0.2)

        self.wait(0.5)

        self.play(FadeOut(VGroup(delNode, tempRectangle, tempText)))
        nodeGroup.remove(delNode)

        self.wait(0.2)
        self.play(nodeGroup.animate.arrange(RIGHT, 1), run_time=0.5)

        self.wait(1)


class ListRotation(Scene):
    def construct(self):
        def make_dynamic_bezier_updater(start_mobj, end_mobj, offset_start=RIGHT*0.2, offset_end=LEFT*0.1):
            def updater(curve):
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

        values = [5, 2, 6, 3, 1]
        nodes : list[Node] = []
        head : Node = None
        current : Node = None
        nodeGroup = VGroup()

        for value in values:
            newNode = Node(value)
            newNode.setValues()
            nodes.append(newNode)
            nodeGroup.add(newNode)

        # nodeGroup.arrange(RIGHT, 1)

        arc_radius = 6
        num_objects = len(nodes)
        arc_angle = -PI / 2

        arc = ArcBetweenPoints(LEFT * arc_radius, RIGHT * arc_radius, angle=arc_angle, color=SORTCOL).center().shift(UP)
        # self.add(arc)

        for i in range(num_objects):
            nodes[i].move_to(arc.point_from_proportion(i / (num_objects - 1)))
        
        self.play(FadeIn(nodeGroup))

        arrows = VGroup()
        for i in range(len(nodes) - 1): 
            start = nodes[i].nextAddressGroup.get_right()
            end = nodes[i + 1].selfAddressGroup.get_left() + (LEFT * 0.1)
            arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
            arrowCurve.add_updater(make_dynamic_bezier_updater(nodes[i].nextAddressGroup, nodes[i + 1].selfAddressGroup, 0, LEFT * 0.1))
            arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
            arrowhead.move_to(end)
            arrowhead.rotate(angle_of_vector(RIGHT))
            arrowhead.add_updater(make_arrowhead_updater(arrowCurve))

            arrow = VGroup(arrowCurve, arrowhead)
            arrows.add(arrow)
            self.play(Create(arrow), run_time=0.6)
            self.play(nodes[i].updateNext(nodes[i + 1]), run_time=0.1)

        self.wait(1)

        k = 2 # Number of rotations


        for i in range(k):
            itterRectangle = DashedVMobject(SurroundingRectangle(nodes[0], color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
            self.play(Create(itterRectangle))
            self.wait(0.2)

            headRectangle = DashedVMobject(SurroundingRectangle(nodes[0], color=SORTCOL, buff=0.2, corner_radius=0.2), 30)
            headLabel = Text("Head", color=SWAP_FONT_COLOR, font=FONT, font_size=SWAP_FONT_SIZE).next_to(headRectangle, DOWN, buff=0.2)
            self.play(Create(headRectangle), Write(headLabel))

            temphead = nodes[0]
            headRectangle.add_updater(lambda m: m.move_to(temphead))
            headLabel.add_updater(lambda m: m.next_to(headRectangle, DOWN, buff=0.2))
            self.wait(0.2)

            newHeadRectangle = DashedVMobject(SurroundingRectangle(nodes[1], color=SORTCOL, buff=0.2, corner_radius=0.2), 30)
            newHeadLabel = Text("New Head", color=SWAP_FONT_COLOR, font=FONT, font_size=SWAP_FONT_SIZE).next_to(newHeadRectangle, DOWN, buff=0.2)
            self.play(Create(newHeadRectangle), Write(newHeadLabel))

            tempNewHead = nodes[1]
            newHeadRectangle.add_updater(lambda m: m.move_to(tempNewHead))
            newHeadLabel.add_updater(lambda m: m.next_to(newHeadRectangle, DOWN, buff=0.2))
            self.wait(0.2)

            current = nodes[0]

            while current.next is not None:
                self.play(itterRectangle.animate.move_to(current), run_time=0.2)
                current = current.next
                self.wait(0.5)

            itterRectangle.add_updater(lambda m: m.move_to(current))

            delNode = nodes.pop(0)
            delArrow = arrows.submobjects.pop(0)

            self.play(Uncreate(delArrow), run_time=0.3)
            self.play(delNode.updateNext(None), run_time=0.3)
            self.wait(0.1)
            self.play(delNode.animate.center().shift(DOWN * 2), run_time=0.3)

            self.wait(0.3)

            for i in range(num_objects - 1):
                self.play(nodes[i].animate.move_to(arc.point_from_proportion(i / (num_objects - 1))), run_time=0.3)

            self.wait(0.3)
            
            nodes.append(delNode)
            nodeGroup.add(nodeGroup.submobjects.pop(0))

            self.play(delNode.animate.move_to(arc.point_from_proportion(1)), run_time=0.3)

            start = nodes[-2].nextAddressGroup.get_right()
            end = delNode.selfAddressGroup.get_left() + (LEFT * 0.1)
            arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
            arrowCurve.add_updater(make_dynamic_bezier_updater(nodes[-2].nextAddressGroup, delNode.selfAddressGroup, 0, LEFT * 0.1))
            arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
            arrowhead.move_to(end)
            arrowhead.rotate(angle_of_vector(RIGHT))
            arrowhead.add_updater(make_arrowhead_updater(arrowCurve))

            arrow = VGroup(arrowCurve, arrowhead)
            arrows.add(arrow)
            self.play(Create(arrow), run_time=0.6)
            self.play(nodes[-2].updateNext(delNode), run_time=0.1)

            self.wait(0.3)
            self.play(Uncreate(itterRectangle), FadeOut(headRectangle), FadeOut(headLabel), FadeOut(newHeadRectangle), FadeOut(newHeadLabel), run_time=0.3)
            self.wait(0.5)

        
        self.wait(1)

        self.play(
            nodeGroup.animate.arrange(RIGHT, 1).center(),
            run_time=0.5
        )

        self.wait(1)


class DoubleNode(VGroup):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.next : DoubleNode = None
        self.prev : DoubleNode = None
        self.selfAddress = random.randint(1000, 9999)
        self.nextAddress = 0 if self.next is None else self.next.selfAddress
        self.prevAddress = 0 if self.prev is None else self.prev.selfAddress

    def setValues(self):
        self.selfAddressText = Text(f"0x{self.selfAddress}", font_size=SELF_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT)
        self.selfAddressGroup = VGroup(
            self.selfAddressText,
            Rectangle(width=NODE_WIDTH, height=0.6, color=SORTCOL)
        )

        if self.next is None:
            self.nextAddressText = Text("NULL", font_size=NEXT_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT)
        else:
            self.nextAddressText = Text(f"0x{self.nextAddress}", font_size=NEXT_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT)
        self.nextAddressGroup = VGroup(
            self.nextAddressText,
            Rectangle(width=NODE_WIDTH, height=0.6, color=SORTCOL)
        )

        if self.prev is None:
            self.prevAddressText = Text("NULL", font_size=NEXT_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT)
        else:
            self.prevAddressText = Text(f"0x{self.prevAddress}", font_size=NEXT_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT)
        self.prevAddressGroup = VGroup(
            self.prevAddressText,
            Rectangle(width=NODE_WIDTH, height=0.6, color=SORTCOL)
        )

        self.valueText = Text(str(self.value), font_size=VALUE_FONT_SIZE, color=TEXTCOL, font=FONT)
        self.valueTextGroup = VGroup(
            self.valueText,
            Rectangle(width=NODE_WIDTH, height=1.6, color=SORTCOL)
        )

        self.add(
            self.prevAddressGroup,
            self.selfAddressGroup,
            self.valueTextGroup,
            self.nextAddressGroup,
        )
        self.arrange(DOWN, buff=0.0)

    def updateSelfAddress(self, new_address):
        self.selfAddress = new_address
        new_self_address_text = Text(f"0x{self.selfAddress}", font_size=SELF_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT).move_to(self.selfAddressText)
        return self.selfAddressText.animate.become(new_self_address_text)
    
    def updateNext(self, new_node):
        self.next : DoubleNode = new_node
        self.nextAddress = 0 if self.next is None else self.next.selfAddress
        if self.next is None:
            new_next_address_text = Text("NULL", font_size=NEXT_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT).move_to(self.nextAddressText)
        else:
            new_next_address_text = Text(f"0x{self.nextAddress}", font_size=NEXT_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT).move_to(self.nextAddressText)
        return self.nextAddressText.animate.become(new_next_address_text)
 
    def updatePrev(self, new_node):
        self.prev : DoubleNode = new_node
        self.prevAddress = 0 if self.prev is None else self.prev.selfAddress
        if self.prev is None:
            new_prev_address_text = Text("NULL", font_size=NEXT_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT).move_to(self.prevAddressText)
        else:
            new_prev_address_text = Text(f"0x{self.prevAddress}", font_size=NEXT_ADDRESS_FONT_SIZE, color=TEXTCOL, font=FONT).move_to(self.prevAddressText)
        return self.prevAddressText.animate.become(new_prev_address_text)
    

class DoubleNodeExplanation(Scene):
    def construct(self):
        node1 = DoubleNode(4)
        node2 = DoubleNode(1)

        node1.setValues()
        node2.setValues()

        self.play(Create(node1))
        self.wait(0.4)

        surroundingRectangleNode = DashedVMobject(SurroundingRectangle(node1, buff=0.4, corner_radius=0.2, color=SORTCOL), num_dashes=30)
        self.play(Create(surroundingRectangleNode))
        explanatoryText = Text("NODE", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(surroundingRectangleNode, LEFT).shift(LEFT * 1.2)
        explanatoryText = VGroup(
            explanatoryText,
            Arrow(start=explanatoryText.get_right(), end=surroundingRectangleNode.get_left(), color=SORTCOL, tip_shape=StealthTip, max_stroke_width_to_length_ratio=4, max_tip_length_to_length_ratio=0.2)
        )

        self.play(Write(explanatoryText), run_time=0.5)
        self.wait(0.7)
        self.play(Unwrite(explanatoryText), FadeOut(surroundingRectangleNode), run_time=0.5)
        self.wait(0.3)

        explanatoryTextGroup = VGroup()

        explanatoryText = Text("Address of\nprevious node", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(node1.prevAddressGroup, LEFT).shift(LEFT * 0.7).shift(UP * 0.5)
        explanatoryText = VGroup(
            explanatoryText,
            Arrow(start=explanatoryText.get_right(), end=node1.prevAddressGroup.get_left(), color=SORTCOL, tip_shape=StealthTip, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1)
        )
        self.play(Write(explanatoryText), run_time=0.5)
        explanatoryTextGroup.add(explanatoryText)

        explanatoryText = Text("Address of\nthis node", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(node1.selfAddressGroup, LEFT).shift(LEFT)
        explanatoryText = VGroup(
            explanatoryText,
            Arrow(start=explanatoryText.get_right(), end=node1.selfAddressGroup.get_left(), color=SORTCOL, tip_shape=StealthTip, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1)
        )
        self.play(Write(explanatoryText), run_time=0.5)
        explanatoryTextGroup.add(explanatoryText)


        explanatoryText = Text("Value of\nthis node", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(node1.valueTextGroup, LEFT).shift(LEFT)
        explanatoryText = VGroup(
            explanatoryText,
            Arrow(start=explanatoryText.get_right(), end=node1.valueTextGroup.get_left(), color=SORTCOL, tip_shape=StealthTip, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1)
        )
        self.play(Write(explanatoryText), run_time=0.5)
        explanatoryTextGroup.add(explanatoryText)


        explanatoryText = Text("Address of\nnext node", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(node1.nextAddressGroup, LEFT).shift(LEFT)
        explanatoryText = VGroup(
            explanatoryText,
            Arrow(start=explanatoryText.get_right(), end=node1.nextAddressGroup.get_left(), color=SORTCOL, tip_shape=StealthTip, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1)
        )
        self.play(Write(explanatoryText), run_time=0.5)
        explanatoryTextGroup.add(explanatoryText)

        self.wait(1.2)

        self.play(Unwrite(explanatoryTextGroup))

        self.play(node1.animate.shift(LEFT * 1.5))


        node2.shift(RIGHT * 1.5)
        self.play(Create(node2))


        start = node1.nextAddressGroup.get_right()
        end = node2.selfAddressGroup.get_left() + (LEFT * 0.1) 
        arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
        arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
        arrowhead.move_to(end)
        arrowhead.rotate(angle_of_vector(RIGHT))

        arrow = VGroup(arrowCurve, arrowhead)
        self.play(Create(arrow))
        self.play(node1.updateNext(node2))

        self.wait(1)

        start = node2.prevAddressGroup.get_left()
        end = node1.selfAddressGroup.get_right() + (RIGHT * 0.1)
        arrowCurve = CubicBezier(start, start + LEFT, end + RIGHT, end, color=SORTCOL)
        arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
        arrowhead.move_to(end)
        arrowhead.rotate(angle_of_vector(LEFT))

        arrow = VGroup(arrowCurve, arrowhead)
        self.play(Create(arrow))
        self.play(node2.updatePrev(node1))

        self.wait(1)


class CreateDoublyLinkedList(Scene):
    def construct(self):
        def make_dynamic_bezier_updater_front(start_mobj, end_mobj, offset_start=RIGHT*0.2, offset_end=LEFT*0.1):
            def updater(curve):
                start = start_mobj.get_right() + offset_start
                end = end_mobj.get_left() + offset_end
                control1 = start + RIGHT
                control2 = end + LEFT
                curve.become(CubicBezier(start, control1, control2, end, color=curve.color))
            return updater
        
        def make_dynamic_bezier_updater_back(start_mobj, end_mobj, offset_start=RIGHT*0.2, offset_end=LEFT*0.1):
            def updater(curve):
                start = start_mobj.get_left() + offset_start
                end = end_mobj.get_right() + offset_end
                control1 = start + LEFT
                control2 = end + RIGHT
                curve.become(CubicBezier(start, control1, control2, end, color=curve.color))
            return updater

        def make_arrowhead_updater(bezier_curve, offset=0.01):
            def updater(arrowhead):
                end_point = bezier_curve.point_from_proportion(1)
                direction = bezier_curve.point_from_proportion(1) - bezier_curve.point_from_proportion(1 - offset)
                arrowhead.move_to(end_point)
                arrowhead.set_angle(angle_of_vector(direction))
            return updater
        
        values = [5, 2, 4, 6, 3, 1]
        # nodes : list[DoubleNode] = [DoubleNode(data) for data in values]

        
        # for i in range(1, len(values)):
        #     nodes[i].prev = nodes[i - 1]
        #     nodes[i - 1].next = nodes[i]

        # head = nodes[0]

        # for node in nodes:
        #     node.setValues()


        head = DoubleNode(values[0])
        head.setValues()
        current = head

        nodeGroup = VGroup(head)
        nodeGroup.arrange(RIGHT, buff=1)
        self.play(FadeIn(nodeGroup))

        forwardArrows = VGroup()
        backwardArrows = VGroup()

        for data in values[1:]:
            node = DoubleNode(data)
            current.next = node
            node.prev = current
            node.setValues()
            node.next_to(nodeGroup, RIGHT, buff=1)

            self.play(Create(node))
            nodeGroup.add(node)
            self.play(nodeGroup.animate.arrange(RIGHT, buff=1))

            if current.next is not None:
                start = current.nextAddressGroup.get_right()
                end = current.next.selfAddressGroup.get_left() + (LEFT * 0.1)
                arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
                arrowCurve.add_updater(make_dynamic_bezier_updater_front(current.nextAddressGroup, current.next.selfAddressGroup, 0, LEFT * 0.1))
                arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
                arrowhead.move_to(end)
                arrowhead.rotate(angle_of_vector(RIGHT))
                arrowhead.add_updater(make_arrowhead_updater(arrowCurve))

                arrow = VGroup(arrowCurve, arrowhead)
                forwardArrows.add(arrow)
                self.play(Create(arrow), run_time=0.6)
                self.play(current.updateNext(current.next), run_time=0.1)

            if node.prev is not None:
                start = node.prevAddressGroup.get_left()
                end = node.prev.selfAddressGroup.get_right() + (RIGHT * 0.1)
                arrowCurve = CubicBezier(start, start + LEFT, end + RIGHT, end, color=SORTCOL)
                arrowCurve.add_updater(make_dynamic_bezier_updater_back(node.prevAddressGroup, node.prev.selfAddressGroup, 0, RIGHT * 0.1))
                arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
                arrowhead.move_to(end)
                arrowhead.rotate(angle_of_vector(LEFT))
                arrowhead.add_updater(make_arrowhead_updater(arrowCurve))

                arrow = VGroup(arrowCurve, arrowhead)
                backwardArrows.add(arrow)
                self.play(Create(arrow), run_time=0.6)
                self.play(node.updatePrev(node.prev), run_time=0.1)

            current = node

        self.wait(1)
        
