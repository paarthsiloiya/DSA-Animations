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
EXPLANATORY_FONT_SIZE = 30  # For step-by-step explanations
POINTER_FONT_SIZE = 28      # For pointer labels (if any)

ELEMENT_BG = BASECOL

BOTTOM_STACK_POS = (0,-2.4,0)
RIGHT_QUEUE_POS = (2.3, 0, 0)

class StackElement():
    def __init__(self, value):
        self.value = value
        self.dataText = Text(str(value), font_size=FSIZE, font=FONT, color=TEXTCOL)
        self.rect = RoundedRectangle(
            width= 4,
            height= self.dataText.height + 0.5,
            fill_color= ELEMENT_BG,
            fill_opacity= 1,
            stroke_color= SELCOL,
            stroke_width= 4,
            corner_radius= 0.2
        )            
        self.element = VGroup(self.rect, self.dataText)

    def get_element(self):
        return self.element
    

class QueueElement():
    def __init__(self, value):
        self.value = value
        self.dataText = Text(str(value), font_size=FSIZE, font=FONT, color=TEXTCOL)
        self.rect = RoundedRectangle(
            width= self.dataText.width + 0.5,
            height= 4,
            fill_color= ELEMENT_BG,
            fill_opacity= 1,
            stroke_color= SELCOL,
            stroke_width= 4,
            corner_radius= 0.2
        )            
        self.element = VGroup(self.rect, self.dataText)

    def get_element(self):
        return self.element
    

class Stack(Scene):
    def construct(self):
        stackContainer = VGroup(
            RoundedRectangle(
                width= 4.25,
                height= 6,
                fill_color= config.background_color,
                fill_opacity= 1,
                stroke_color= TEXTCOL,
                stroke_width= 6,
                corner_radius= 0.2
            ),
            Rectangle(
                width= 5,
                height= 0.3,
                fill_color= config.background_color,
                fill_opacity= 1,
                stroke_width= 0
            ).shift(UP * 2.95),
        )

        self.add(stackContainer)

        surrRect = DashedVMobject(RoundedRectangle(
            width= 5.25,
            height= 7,
            stroke_color=TEXTCOL,
            stroke_width=4,
            corner_radius=0.2
        ), num_dashes=80)
        explanatory_text = Text("<-Stack", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(surrRect, RIGHT, buff=0.1)

        self.play(Create(surrRect), run_time=0.5)
        self.wait(0.2)
        self.play(Write(explanatory_text), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(surrRect), FadeOut(explanatory_text), run_time=0.5)
        self.wait(0.7)

        stackElements, pos = [], -1

        element = StackElement(1).get_element().next_to(stackContainer, UP, buff=0.1)
        stackElements.append(element)
        pos += 1

        self.play(Create(stackElements[pos]))
        surrRect = DashedVMobject(SurroundingRectangle(
            element,
            buff=0.2,
            stroke_color=TEXTCOL,
            stroke_width=4,
            corner_radius=0.2
        ), num_dashes=80)
        explanatory_text = Text("<-Data Element", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(surrRect, RIGHT, buff=0.1)
        
        self.play(Create(surrRect), run_time=0.5)
        self.wait(0.2)
        self.play(Write(explanatory_text), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(surrRect), FadeOut(explanatory_text), run_time=0.5)
        self.wait(0.4)
        
        operation_text = Text("PUSH", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(stackContainer, RIGHT, buff=1)
        self.play(Write(operation_text), run_time=0.5)
        self.wait(0.5)
        
        self.play(stackElements[pos].animate.move_to(BOTTOM_STACK_POS + UP * (pos * 1.1)))

        self.wait(0.5)
        top_arrow = Text("TOP ->", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(stackElements[pos], LEFT, buff=0.18)
        self.play(Create(top_arrow), run_time=0.5)

        self.wait(0.8)

        element = StackElement(2).get_element().next_to(stackContainer, UP, buff=0.1)
        stackElements.append(element)
        pos += 1

        self.play(Create(stackElements[pos]))
        self.wait(0.5)
        self.play(stackElements[pos].animate.move_to(BOTTOM_STACK_POS + UP * (pos * 1.1)))
        self.wait(0.2)
        self.play(top_arrow.animate.next_to(stackElements[pos], LEFT, buff=0.18),run_time=0.5)
        self.wait(0.2)

        for i in range(3):
            element = StackElement(random.randint(3, 10)).get_element().next_to(stackContainer, UP, buff=0.1)
            stackElements.append(element)
            pos += 1

            self.play(Create(stackElements[pos]))
            self.wait(0.5)
            self.play(stackElements[pos].animate.move_to(BOTTOM_STACK_POS + UP * (pos * 1.1)))
            self.wait(0.2)
            self.play(top_arrow.animate.next_to(stackElements[pos], LEFT, buff=0.18), run_time=0.5)

        element = StackElement(7).get_element().next_to(stackContainer, UP, buff=0.1)
        pos += 1

        self.play(Create(element))
        self.wait(0.5)
        self.play(element.animate.move_to(BOTTOM_STACK_POS + UP * (pos * 1.1)))
        self.wait(0.2)
        cross = Cross(element, color=RED_A, stroke_width=6)
        surrRect = DashedVMobject(SurroundingRectangle(
            element,
            buff=0.15,
            stroke_color=TEXTCOL,
            stroke_width=4,
            corner_radius=0.2
        ), num_dashes=80)
        explanatory_text = Text("<-Overflow", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(surrRect, RIGHT, buff=0.1)
        self.play(Create(surrRect), run_time=0.5)
        self.wait(0.2)
        self.play(Write(explanatory_text), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(surrRect), FadeOut(explanatory_text), run_time=0.5)
        self.wait(0.4)

        self.play(Create(cross), run_time=0.5)
        self.wait(0.1)
        self.play(FadeOut(cross, element), run_time=0.5)

        pos -= 1

        self.wait(0.6)
        self.play(FadeOut(operation_text))

        self.wait(0.3)

        operation_text = Text("POP", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(stackContainer, RIGHT, buff=1)
        self.play(Write(operation_text), run_time=0.5)
        self.wait(0.5)

        for i in range(5):
            self.play(stackElements[pos].animate.move_to(stackContainer.get_top() + UP * 0.7))
            self.play(FadeOut(stackElements[pos]), run_time=0.5)
            self.wait(0.2)

            stackElements.pop(pos)
            pos -= 1

            if pos < 0:
                break
            
            self.play(top_arrow.animate.next_to(stackElements[pos], LEFT, buff=0.18), run_time=0.5)

            self.wait(0.3)

        self.play(top_arrow.animate.shift(DOWN * 0.8), run_time=0.5)
        self.wait(0.5)

        explanatory_text = Text("Stack Underflow", font_size=EXPLANATORY_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(operation_text, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(explanatory_text), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(explanatory_text), run_time=0.5)
        self.play(top_arrow.animate.shift(UP * 0.8), run_time=0.5)

        self.wait(0.5)
        self.play(FadeOut(operation_text), run_time=0.5)

        self.wait(3)


class Queue(Scene):
    def construct(self):
        from collections import deque

        queueContainer = VGroup(
            Line(
                start=LEFT * 3 + UP * 2.2,
                end=RIGHT * 3 + UP * 2.2,
                stroke_color=TEXTCOL,
                stroke_width=6
            ),
            Line(
                start=LEFT * 3 + DOWN * 2.2,
                end=RIGHT * 3 + DOWN * 2.2,
                stroke_color=TEXTCOL,
                stroke_width=6
            ),
        )

        self.add(queueContainer)

        surrRect = DashedVMobject(RoundedRectangle(
            width= 6.5,
            height= 5,
            stroke_color=TEXTCOL,
            stroke_width=4,
            corner_radius=0.2
        ), num_dashes=80)
        explanatory_text = Text("<-Queue", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(surrRect, RIGHT, buff=0.1)
        # self.play(Create(surrRect), run_time=0.5)
        # self.wait(0.2)
        # self.play(Write(explanatory_text), run_time=0.5)
        # self.wait(0.6)
        # self.play(FadeOut(surrRect), FadeOut(explanatory_text), run_time=0.5)
        # self.wait(0.7)

        queueElements = deque()

        operation_text = Text("Enqueue", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(queueContainer, UP, buff=1)
        self.play(Write(operation_text), run_time=0.5)
        self.wait(0.5)
        
        for i in range(5):
            element = QueueElement(random.randint(1, 10)).get_element().next_to(queueContainer, LEFT, buff=0.1)
            queueElements.append(element)
            self.play(Create(element))
            self.wait(0.5)
            self.play(element.animate.move_to(RIGHT_QUEUE_POS + LEFT * (i * 1.1)))
            self.wait(0.2)

        element = QueueElement(random.randint(1, 10)).get_element().next_to(queueContainer, LEFT, buff=0.1)
        self.play(Create(element))
        self.wait(0.5)
        self.play(element.animate.move_to(RIGHT_QUEUE_POS + LEFT * (5 * 1.1)))
        self.wait(0.2)
        cross = Cross(element, color=RED_A, stroke_width=6)
        surrRect = DashedVMobject(SurroundingRectangle(
            element,
            buff=0.15,
            stroke_color=TEXTCOL,
            stroke_width=4,
            corner_radius=0.2
        ), num_dashes=80)
        explanatory_text = Text("Overflow->", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(surrRect, LEFT, buff=0.1)
        self.play(Create(surrRect), run_time=0.5)
        self.wait(0.2)
        self.play(Write(explanatory_text), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(surrRect), FadeOut(explanatory_text), run_time=0.5)
        self.wait(0.4)
        self.play(Create(cross), run_time=0.5)
        self.wait(0.1)
        self.play(FadeOut(cross, element), run_time=0.5)

        self.wait(0.4)
        self.play(FadeOut(operation_text))
        self.wait(0.3)

        operation_text = Text("Dequeue", font_size=FSIZE, font=FONT, color=TEXTCOL).next_to(queueContainer, UP, buff=1)
        self.play(Write(operation_text), run_time=0.5)

        self.wait(0.5)

        for i in range(5):
            element = queueElements.popleft()

            self.play(element.animate.move_to(queueContainer.get_right() + RIGHT * 0.7))
            self.play(FadeOut(element), run_time=0.5)
            self.wait(0.1)

            for j in range(len(queueElements)):
                self.play(queueElements[j].animate.shift(RIGHT * 1.15), run_time=0.5)

            self.wait(0.2)