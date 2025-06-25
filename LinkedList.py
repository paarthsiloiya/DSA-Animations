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
EXPLANATORY_FONT_SIZE = 40  # For step-by-step explanations
POINTER_FONT_SIZE = 28      # For pointer labels (if any)

SWAP_FONT_COLOR = SORTCOL
EXPLANATORY_FONT_COLOR = TEXTCOL
POINTER_FONT_COLOR = SORTCOL

class Node():
    def __init__(self, value : int):
        self.value = value
        self.next : Node = None
        self.selfAddress = '0x' + str(random.randint(1000, 9999))

    def setValues(self):
        self.nextAddress = self.next.selfAddress
        self.valueText = Text(text=str(self.value), font_size=90, color=TEXTCOL, font=FONT)
        self.selfAddressText = Text(self.selfAddress, font_size=21, color=TEXTCOL, font=FONT)
        self.nextAddressText = Text(self.nextAddress, font_size=25, color=TEXTCOL, font=FONT)
        
        self.valueTextGroup = VGroup(
            self.valueText,
            Rectangle(height=1.6, width=1.6, color=SORTCOL)
        )
        self.selfAddressGroup = VGroup(
            self.selfAddressText,
            Rectangle(height=0.55, width=1.6, color=SORTCOL)
        )
        self.nextAddressGroup = VGroup(
            self.nextAddressText,
            Rectangle(height=0.55, width=1.6, color=SORTCOL)
        )

        self.element = VGroup(
            self.nextAddressGroup,
            self.valueTextGroup,
            self.selfAddressGroup,
        )
        self.element.arrange(DOWN, buff=0, center=True)

    def getElement(self):
        return self.element
    


class DoubleNode():
    def __init__(self, value : int):
        self.value = value
        self.next : DoubleNode = None
        self.prev : DoubleNode = None
        self.selfAddress = '0x' + str(random.randint(1000, 9999))

    def setValues(self):
        self.nextAddress = self.next.selfAddress
        self.prevAddress = self.prev.selfAddress
        self.valueText = Text(text=str(self.value), font_size=90, color=TEXTCOL, font=FONT)
        self.selfAddressText = Text(self.selfAddress, font_size=21, color=TEXTCOL, font=FONT)
        self.nextAddressText = Text(self.nextAddress, font_size=25, color=TEXTCOL, font=FONT)
        self.prevAddressText = Text(self.prevAddress, font_size=25, color=TEXTCOL, font=FONT)
        
        self.valueTextGroup = VGroup(
            self.valueText,
            Rectangle(height=1.6, width=1.6, color=SORTCOL)
        )
        self.selfAddressGroup = VGroup(
            self.selfAddressText,
            Rectangle(height=0.55, width=1.6, color=SORTCOL)
        )
        self.nextAddressGroup = VGroup(
            self.nextAddressText,
            Rectangle(height=0.55, width=1.6, color=SORTCOL)
        )

        self.prevAddressGroup = VGroup(
            self.prevAddressText,
            Rectangle(height=0.55, width=1.6, color=SORTCOL)
        )

        self.element = VGroup(
            self.nextAddressGroup,
            self.valueTextGroup,
            self.prevAddressGroup,
            self.selfAddressGroup,
        )
        self.element.arrange(DOWN, buff=0, center=True)

    def getElement(self):
        return self.element



class NodeExplanation(Scene):
    def construct(self):
        node1 = Node(4)
        node2 = Node(1)
        node1.next = Node(-1)
        node1.next.selfAddress = "NULL"

        node1.setValues()

        self.play(Create(node1.getElement()))
        self.wait(0.4)

        surroundingRectangleNode = DashedVMobject(SurroundingRectangle(node1.getElement(), buff=0.4, corner_radius=0.2, color=SORTCOL), num_dashes=30)
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

        self.play(node1.getElement().animate.shift(LEFT * 1.5))

        node2.next = Node(-1)
        node2.next.selfAddress = "NULL"

        node1.next = node2

        node2.setValues()

        node2.getElement().shift(RIGHT * 1.5)
        self.play(Create(node2.getElement()))

        old_next_text = node1.nextAddressText

        node1.next = node2
        node1.setValues()

        new_next_text = node1.nextAddressText

        new_next_text.move_to(old_next_text)

        start = node1.nextAddressGroup.get_right() + (LEFT * 1.5)
        end = node2.selfAddressGroup.get_left() + (LEFT * 0.1)
        arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
        arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
        arrowhead.move_to(end)
        arrowhead.rotate(angle_of_vector(RIGHT))

        arrow = VGroup(arrowCurve, arrowhead)
        self.play(Create(arrow))
        self.play(ReplacementTransform(old_next_text, new_next_text))

        node1.element.submobjects[0] = node1.nextAddressGroup

        self.wait(1)



class CreateLinkedList(Scene):
    def construct(self):
        values = [5, 2, 4, 6, 3, 1]
        nodes : list[Node] = []

        first_node = Node(values[0])
        first_node.next = Node(-1)
        first_node.next.selfAddress = "NULL"
        first_node.setValues()
        self.play(Create(first_node.getElement()))
        nodes.append(first_node)

        nodeGroup = VGroup(first_node.getElement())
        arrowGroup = VGroup()

        fullGruop = VGroup(nodeGroup, arrowGroup)

        for i in range(1, len(values)):
            prev_node = nodes[-1]

            new_node = Node(values[i])
            new_node.next = Node(-1)
            new_node.next.selfAddress = "NULL"
            new_node.setValues()

            nodes.append(new_node)

            self.play(fullGruop.animate.shift(LEFT * 1.3))

            new_node.getElement().next_to(prev_node.getElement(), RIGHT, buff=1)

            old_next_text = prev_node.nextAddressText

            prev_node.next = new_node
            prev_node.setValues()

            new_next_text = prev_node.nextAddressText
            new_next_text.move_to(old_next_text)

            self.play(Create(new_node.getElement()))
            nodeGroup.add(new_node.getElement())
            
            start = prev_node.nextAddressText.get_right() + (RIGHT * 0.2)
            end = new_node.selfAddressText.get_left() + (LEFT * 0.35)
            curve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
            head = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
            head.move_to(end)
            head.rotate(angle_of_vector(RIGHT))
            arrow = VGroup(curve, head)
            arrowGroup.add(arrow)
            self.play(Create(arrow))

            self.play(ReplacementTransform(old_next_text, new_next_text))

            prev_node.element.submobjects[0] = prev_node.nextAddressGroup

        self.wait(1)

        surroundingRectangleNode = DashedVMobject(SurroundingRectangle(nodeGroup.submobjects[0], color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
        self.play(Create(surroundingRectangleNode))
        explanatorText = Text("Head", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeGroup.submobjects[0], UP, buff=0.6)
        self.play(Write(explanatorText))
        self.wait(0.3)
        self.play(FadeOut(surroundingRectangleNode), FadeOut(explanatorText))

        self.wait(0.3)
        
        surroundingRectangleNode = DashedVMobject(SurroundingRectangle(nodeGroup.submobjects[-1], color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
        self.play(Create(surroundingRectangleNode))
        explanatorText = Text("Tail", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeGroup.submobjects[-1], UP, buff=0.6)
        self.play(Write(explanatorText))
        self.wait(0.3)
        self.play(FadeOut(surroundingRectangleNode), FadeOut(explanatorText))

        self.wait(1)



class TraverseLinkedList(Scene):
    def construct(self):
        values = [5, 2, 4, 6, 3, 1]
        nodes : list[Node] = []
        head : Node = None
        current : Node = None

        for value in values:
            newNode = Node(value)
            if head is None:
                head = newNode
                current = newNode
            else:
                current.next = newNode
                current = newNode
            nodes.append(current)

        for node in nodes:
            if node.next is None:
                node.next = Node(-1)
                node.next.selfAddress = "NULL"
            node.setValues()

        nodeGroup = VGroup(*[node.getElement() for node in nodes])
        nodeGroup.arrange(RIGHT, 1)

        arrows = VGroup()
        curves = VGroup()
        for i in range(len(nodes) - 1): 
            start = nodes[i].nextAddressGroup.get_right()
            end = nodes[i + 1].selfAddressGroup.get_left() + (LEFT * 0.1)
            arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
            arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
            arrowhead.move_to(end)
            arrowhead.rotate(angle_of_vector(RIGHT))

            arrow = VGroup(arrowCurve, arrowhead)
            curves.add(arrowCurve)
            arrows.add(arrow)

        self.play(FadeIn(nodeGroup))
        self.play(Create(arrows), run_time=1.5)

        self.wait(0.7)

        surroundingRectangleNode = DashedVMobject(SurroundingRectangle(nodes[0].getElement(), color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
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
            self.play(surroundingRectangleNode.animate.move_to(node.getElement()), run_time=0.3)
            self.wait(0.3)

        self.play(FadeOut(surroundingRectangleNode))

        self.wait(1)


class Insertion(Scene):
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

        for value in values:
            newNode = Node(value)
            if head is None:
                head = newNode
                current = newNode
            else:
                current.next = newNode
                current = newNode
            nodes.append(current)

        for node in nodes:
            if node.next is None:
                node.next = Node(-1)
                node.next.selfAddress = "NULL"
            node.setValues()

        nodeGroup = VGroup(*[node.getElement() for node in nodes])
        nodeGroup.arrange(RIGHT, 1)

        arrows = VGroup()
        curves = VGroup()
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
            curves.add(arrowCurve)
            arrows.add(arrow)

        self.play(FadeIn(nodeGroup))
        self.play(nodeGroup.animate.shift(DOWN))
        self.play(Create(arrows), run_time=1.5)

        self.wait(0.7)

        newNode = Node(4)
        newNode.next = Node(-1)
        newNode.next.selfAddress = "NULL"
        newNode.setValues()
        newNode.getElement().shift(UP * 2.6)

        self.play(Create(newNode.getElement()))
        self.wait(0.4)

        tempRect = DashedVMobject(SurroundingRectangle(newNode.getElement(), color=SORTCOL, buff=0.2, corner_radius=0.2), 30)
        self.play(Create(tempRect))
        self.wait(0.1)
        tempText = Text("New\nNode", color=SWAP_FONT_COLOR, font=FONT, font_size=SWAP_FONT_SIZE).next_to(tempRect, LEFT, 0.2)
        self.play(Write(tempText))
        self.wait(0.5)
        self.play(FadeOut(tempRect), FadeOut(tempText))
        self.wait(0.2)

        self.play(newNode.getElement().animate.shift(LEFT * 1.2))
        self.wait(0.4)

        itterationRectangle = DashedVMobject(SurroundingRectangle(nodes[0].getElement(), color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
        self.play(Create(itterationRectangle))
        self.wait(0.5)

        pos = 1

        for i in range(1, pos+1):
            self.play(itterationRectangle.animate.move_to(nodeGroup.submobjects[i]))
            self.wait(0.2)
        
        nodeGroup.insert(pos+1, newNode.getElement())
        nodes.insert(pos+1, newNode)
        previousNodeForInsertion = nodes[pos]
        nextNodeForInsertion = nodes[pos+2]

        old_next_text = previousNodeForInsertion.nextAddressText

        previousNodeForInsertion.next = newNode
        previousNodeForInsertion.setValues()
        
        new_next_text = previousNodeForInsertion.nextAddressText
        new_next_text.move_to(old_next_text)

        self.play(Uncreate(arrows.submobjects[pos]))
        start = previousNodeForInsertion.nextAddressText.get_right() + (RIGHT * 0.2)
        end = newNode.selfAddressGroup.get_left() + (LEFT * 0.1)
        arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
        # arrowCurve.add_updater(update_arrow_curve)
        arrowCurve.add_updater(make_dynamic_bezier_updater(previousNodeForInsertion.nextAddressText, newNode.selfAddressGroup, RIGHT * 0.2, LEFT * 0.1))
        arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
        arrowhead.move_to(end)
        arrowhead.rotate(angle_of_vector(RIGHT))
        arrowhead.add_updater(make_arrowhead_updater(arrowCurve))
        arrow = VGroup(arrowCurve, arrowhead)

        self.play(Create(arrow))
        self.wait(0.2)
        self.play(ReplacementTransform(old_next_text, new_next_text))
        self.wait(0.4)

        self.play(itterationRectangle.animate.move_to(newNode.getElement()))
        self.wait(0.3)

        old_next_text = newNode.nextAddressText

        newNode.next = nextNodeForInsertion
        newNode.setValues()
        
        new_next_text = newNode.nextAddressText
        new_next_text.move_to(old_next_text)

        start = newNode.nextAddressText.get_right() + (RIGHT * 0.2)
        end = nextNodeForInsertion.selfAddressGroup.get_left() + (LEFT * 0.1)
        arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
        arrowCurve.add_updater(make_dynamic_bezier_updater(newNode.nextAddressText, nextNodeForInsertion.selfAddressGroup, RIGHT * 0.2, LEFT * 0.1))
        arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
        arrowhead.move_to(end)
        arrowhead.rotate(angle_of_vector(RIGHT))
        arrowhead.add_updater(make_arrowhead_updater(arrowCurve))
        arrow = VGroup(arrowCurve, arrowhead)

        self.play(Create(arrow))
        self.wait(0.2)
        self.play(ReplacementTransform(old_next_text, new_next_text))
        self.wait(0.4)

        self.play(FadeOut(itterationRectangle))
        self.wait(0.3)


        self.play(nodeGroup.animate.arrange(RIGHT, 1))
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

        for value in values:
            newNode = Node(value)
            if head is None:
                head = newNode
                current = newNode
            else:
                current.next = newNode
                current = newNode
            nodes.append(current)

        for node in nodes:
            if node.next is None:
                node.next = Node(-1)
                node.next.selfAddress = "NULL"
            node.setValues()

        nodeGroup = VGroup(*[node.getElement() for node in nodes])
        nodeGroup.arrange(RIGHT, 1)

        arrows = VGroup()
        curves = VGroup()
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
            curves.add(arrowCurve)
            arrows.add(arrow)

        self.play(FadeIn(nodeGroup))
        self.play(Create(arrows), run_time=1.5)

        self.wait(0.5)

        itterationRectangle = DashedVMobject(SurroundingRectangle(nodes[0].getElement(), color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
        self.play(Create(itterationRectangle))
        self.wait(0.5)

        pos = 2
        delNode = nodeGroup.submobjects[pos]

        # Add a label for the node being deleted
        deleteLabel = Text("Delete", color=SWAP_FONT_COLOR, font=FONT, font_size=SWAP_FONT_SIZE).next_to(delNode, UP, buff=0.4)
        self.play(Write(deleteLabel))
        self.wait(0.3)

        for i in range(1, pos + 1):
            self.play(itterationRectangle.animate.move_to(nodeGroup.submobjects[i]))
            self.wait(0.2)


        self.play(itterationRectangle.animate.move_to(delNode))
        tempRectangle = DashedVMobject(SurroundingRectangle(nodes[pos + 1].getElement(), color=SORTCOL, buff=0.2, corner_radius=0.2), 30)
        tempText = Text("Temporary", color=SWAP_FONT_COLOR, font=FONT, font_size=SWAP_FONT_SIZE).next_to(tempRectangle, UP, 0.2)
        self.play(Create(tempRectangle), Write(tempText))
        self.wait(0.2)
        self.play(Uncreate(arrows.submobjects[pos]))        
        self.wait(0.2)
        self.play(Uncreate(arrows.submobjects[pos-1]))

        self.play(FadeOut(delNode), FadeOut(itterationRectangle), FadeOut(deleteLabel))
        nodeGroup.remove(nodeGroup.submobjects[pos])
        nodes.remove(nodes[pos])

        start = nodes[pos - 1].nextAddressGroup.get_right()
        end = nodes[pos].selfAddressGroup.get_left() + (LEFT * 0.1)
        arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
        arrowCurve.add_updater(make_dynamic_bezier_updater(nodes[pos - 1].nextAddressGroup, nodes[pos].selfAddressGroup, 0, LEFT * 0.1))
        arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
        arrowhead.move_to(end)
        arrowhead.rotate(angle_of_vector(RIGHT))
        arrowhead.add_updater(make_arrowhead_updater(arrowCurve))

        arrow = VGroup(arrowCurve, arrowhead)
        self.play(Create(arrow))

        self.wait(0.2)
        self.play(FadeOut(tempRectangle), FadeOut(tempText))
        self.wait(0.2)

        old_self_text = nodes[pos - 1].nextAddressText
        new_next_text = Text(nodes[pos].selfAddress, font_size=25, color=TEXTCOL, font=FONT)
        new_next_text.move_to(old_self_text)
        self.play(ReplacementTransform(old_self_text, new_next_text))
        self.wait(0.4)

        self.play(nodeGroup.animate.arrange(RIGHT, 1))
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

        values = [5, 2, 4, 6, 3, 1]
        nodes : list[Node] = []
        head : Node = None
        current : Node = None

        for value in values:
            newNode = Node(value)
            if head is None:
                head = newNode
                current = newNode
            else:
                current.next = newNode
                current = newNode
            nodes.append(current)

        for node in nodes:
            if node.next is None:
                node.next = Node(-1)
                node.next.selfAddress = "NULL"
            node.setValues()

        nodeGroup = VGroup(*[node.getElement() for node in nodes])
        nodeGroup.arrange(RIGHT, 1)

        def create_arrows(nodes):
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
            return arrows

        arrows = create_arrows(nodes)
        self.play(FadeIn(nodeGroup))
        self.play(Create(arrows), run_time=1.5)
        self.wait(0.7)

        # Highlight the current head
        head_rect = DashedVMobject(SurroundingRectangle(nodeGroup[0], color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
        self.play(Create(head_rect))
        head_label = Text("Head", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeGroup[0], UP, buff=0.6)
        self.play(Write(head_label))
        self.wait(0.5)

        # --- Animate k-rotation ---
        k = 2  # Number of rotations
        for step in range(k):
            # Animate traversal to the last node
            for i in range(len(nodeGroup)-1):
                self.play(head_rect.animate.move_to(nodeGroup[i]), run_time=0.2)
            self.wait(0.2)

            # Animate moving the head node to the tail
            old_head_node = nodes.pop(0)
            nodes.append(old_head_node)
            old_head_visual = nodeGroup.submobjects.pop(0)
            nodeGroup.submobjects.append(old_head_visual)

            # Rearrange the visuals
            self.play(nodeGroup.animate.arrange(RIGHT, 1), run_time=0.7)
            self.wait(0.2)

            # Update next pointers and visuals in data
            for i in range(len(nodes)-1):
                nodes[i].next = nodes[i+1]
            nodes[-1].next = Node(-1)
            nodes[-1].next.selfAddress = "NULL"
            
            for node in nodes:
                node.setValues()

            # Remove old arrows and create new ones
            self.play(FadeOut(arrows))
            arrows = create_arrows(nodes)
            self.play(Create(arrows), run_time=1.0)
            self.wait(0.2)

        # Highlight new head and tail
        self.play(FadeOut(head_rect), FadeOut(head_label))
        new_head_rect = DashedVMobject(SurroundingRectangle(nodeGroup[0], color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
        new_head_label = Text("Head", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeGroup[0], UP, buff=0.6)
        self.play(Create(new_head_rect), Write(new_head_label))
        self.wait(0.3)
        tail_rect = DashedVMobject(SurroundingRectangle(nodeGroup[-1], color=TEXTCOL, buff=0.2, corner_radius=0.2), 30)
        tail_label = Text("Tail", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(nodeGroup[-1], UP, buff=0.6)
        self.play(Create(tail_rect), Write(tail_label))
        self.wait(0.5)
        self.play(FadeOut(new_head_rect), FadeOut(new_head_label), FadeOut(tail_rect), FadeOut(tail_label))

        self.wait(1)



class DoubleNodeExplanation(Scene):
    def construct(self):
        
        node1 = DoubleNode(4)
        node2 = DoubleNode(1)
        node1.next = DoubleNode(-1)
        node1.next.selfAddress = "NULL"
        node1.prev = DoubleNode(-1)
        node1.prev.selfAddress = "NULL"

        node1.setValues()

        self.play(Create(node1.getElement()))
        self.wait(0.4)

        surroundingRectangleNode = DashedVMobject(SurroundingRectangle(node1.getElement(), buff=0.4, corner_radius=0.2, color=SORTCOL), num_dashes=30)
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


        explanatoryText = Text("Address of\nprevious node", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(node1.prevAddressGroup, LEFT).shift(LEFT).shift(DOWN * 0.2)
        explanatoryText = VGroup(
            explanatoryText,
            Arrow(start=explanatoryText.get_right(), end=node1.prevAddressGroup.get_left(), color=SORTCOL, tip_shape=StealthTip, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1)
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

        self.play(node1.getElement().animate.shift(LEFT * 1.5))

        node2.next = DoubleNode(-1)
        node2.next.selfAddress = "NULL"
        node2.prev = DoubleNode(-1)
        node2.prev.selfAddress = "NULL"

        node2.setValues()

        node2.getElement().shift(RIGHT * 1.5)
        self.play(Create(node2.getElement()))

        old_next_text_next = node1.nextAddressText
        old_next_text_prev = node2.prevAddressText

        node1.next = node2
        node1.setValues()

        node2.prev = node1
        node2.setValues()

        new_next_text_next = node1.nextAddressText
        new_next_text_prev = node2.prevAddressText

        new_next_text_next.move_to(old_next_text_next)
        new_next_text_prev.move_to(old_next_text_prev)

        start = node1.nextAddressGroup.get_right() + (LEFT * 1.5)
        end = node2.selfAddressGroup.get_left() + (LEFT * 0.1) + (RIGHT * 1.5)
        arrowCurve = CubicBezier(start, start + RIGHT, end + LEFT, end, color=SORTCOL)
        arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SORTCOL).scale(0.8)
        arrowhead.move_to(end)
        arrowhead.rotate(angle_of_vector(RIGHT))

        arrow = VGroup(arrowCurve, arrowhead)
        self.play(Create(arrow))
        self.play(ReplacementTransform(old_next_text_next, new_next_text_next))

        self.wait(0.7)

        start = node2.prevAddressGroup.get_left() + (RIGHT * 1.5)
        end = node1.selfAddressGroup.get_right() + (LEFT * 1.4)
        arrowCurve = CubicBezier(start, start + LEFT, end + RIGHT, end, color=SELCOL)
        arrowhead = StealthTip(fill_opacity=1, stroke_opacity=1, color=SELCOL).scale(0.8)
        arrowhead.move_to(end)
        arrowhead.rotate(angle_of_vector(LEFT))

        arrow = VGroup(arrowCurve, arrowhead)
        self.play(Create(arrow))
        self.play(ReplacementTransform(old_next_text_prev, new_next_text_prev))

        self.wait(1)