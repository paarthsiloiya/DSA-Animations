from manim import *
from manim.utils.unit import Percent, Pixels
from manim import CurvedArrow

# manim -ql -p SearchingAlgorithms.py BinarySearch
config.frame_width = 16
config.frame_height = 9

BASECOL = ManimColor.from_hex("#ebe7f3")
TEXTCOL = ManimColor.from_hex("#000000")
SELCOL = ManimColor.from_hex("#7a5bae")
SORTCOL = ManimColor.from_hex("#4a2a90")

FSIZE = 40
FONT = 'JetBrains Mono'

SWAP_FONT_SIZE = 38         # For "Found!", "SORT!", etc.
EXPLANATORY_FONT_SIZE = 40  # For step-by-step explanations
POINTER_FONT_SIZE = 28      # For "Low", "High", "Mid", etc.

SWAP_FONT_COLOR = SORTCOL
EXPLANATORY_FONT_COLOR = TEXTCOL
POINTER_FONT_COLOR = SORTCOL

class ListElement():
    def __init__(self, value : str):
        self.size = 0.8
        self.value = int(value)
        self.isFound = False
        self.elementValue = Text(value, font_size=(100*self.size), color=TEXTCOL, font=FONT)
        self.circle = Circle(radius=self.size, color=BASECOL, fill_opacity=1)
        self.elementValue.move_to(self.circle.get_center())
        self.elementGroup = VGroup(self.circle, self.elementValue)

    def getListElement(self):
        return self.elementGroup

    def SelectElement(self):
        return self.circle.animate.set_stroke(color=SELCOL, width=10)
    
    def ClearSelection(self):
        if not self.isFound:
            return self.circle.animate.set_stroke(color=BASECOL)
        else:
            return self.circle.animate.set_stroke(color=SORTCOL)
    
    def MarkFound(self):
        self.isFound = True
        return self.circle.animate.set_fill(color=SORTCOL).set_stroke(width=0), self.elementValue.animate.set_color(color=WHITE)


class LinearSearch(Scene):
    def construct(self):
        target = 6
        array = [5, 2, 4, 6, 3, 1]
        list_elements = [ListElement(str(i)) for i in array]
        visuals = VGroup(*[el.getListElement() for el in list_elements])
        visuals.arrange(RIGHT, buff=0.5)
        self.add(visuals)

        # Show the key visually
        target_text = Text(f"Target = {target}", color=SELCOL, font=FONT).scale(1.2).next_to(visuals, UP, buff=1.6)
        self.play(Write(target_text), run_time=0.4)

        n = len(list_elements)

        for i in range(n):
            # Step label
            step_text = Text(f"Checking index {i}", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(visuals, DOWN, buff=1)
            self.play(Write(step_text), run_time=0.2)

            self.play(list_elements[i].SelectElement(), run_time=0.2)
            self.wait(0.5)
            if array[i] == target:
                self.play(*(list_elements[i].MarkFound()), run_time=0.2)
                found_text = Text("Found!", color=SWAP_FONT_COLOR, font=FONT, font_size=SWAP_FONT_SIZE).next_to(visuals, DOWN, buff=1.8)
                self.play(Write(found_text), run_time=0.4)
                self.wait(1)
                self.play(FadeOut(step_text), FadeOut(found_text))
                break
            self.play(list_elements[i].ClearSelection(), run_time=0.2)
            self.play(FadeOut(step_text), run_time=0.1)

        self.wait(1)

            
class BinarySearch(Scene):
    def construct(self):
        target = 4
        array = [5, 2, 4, 6, 3, 1]
        list_elements = [ListElement(str(i)) for i in array]

        visuals = VGroup(*[el.getListElement() for el in list_elements])
        visuals.arrange(RIGHT, buff=0.5)
        self.add(visuals)

        sorted_elements = sorted(list_elements, key=lambda el: int(el.value))
        dummy_group = VGroup(*[el.getListElement().copy() for el in sorted_elements])
        dummy_group.arrange(RIGHT, buff=0.5)
        target_positions = [el.get_center() for el in dummy_group]

        sortText = Text("SORT!", color=SWAP_FONT_COLOR, font=FONT, font_size=SWAP_FONT_SIZE+5).shift(UP*2.5)
        self.play(Write(sortText), run_time=0.4)

        animations = [
            el.getListElement().animate.move_to(pos)
            for el, pos in zip(sorted_elements, target_positions)
        ]
        self.play(*animations, run_time=2)
        self.play(FadeOut(sortText), run_time=0.2)
        self.wait(0.4)
        
        target_text = Text(f"Target = {target}", color=SELCOL, font=FONT, font_size=SWAP_FONT_SIZE).next_to(visuals, UP, buff=1.6)
        self.play(Write(target_text), run_time=0.4)
        self.wait(0.4)

        list_elements = sorted_elements
        array = sorted(array)

        low, high = 0, len(array) - 1

        def make_arrow(idx, label):
            arrow = Arrow(
                start=list_elements[idx].getListElement().get_center() + (UP * 2),
                end=list_elements[idx].getListElement().get_center() + UP,
                max_stroke_width_to_length_ratio=5,
                color=SORTCOL
            )
            text = Text(
                label,
                color=POINTER_FONT_COLOR,
                font=FONT,
                font_size=POINTER_FONT_SIZE
            ).next_to(arrow, UP, buff=0.1)
            return VGroup(arrow, text)

        lowGroup = make_arrow(low, "Low")
        highGroup = make_arrow(high, "High")
        mid = (low + high) // 2
        midGroup = make_arrow(mid, "Mid")

        midSmallerText = Text("Mid < Target : Low = Mid + 1", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).shift(DOWN * 2.5)
        midGreaterText = Text("Mid > Target : High = Mid - 1", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).shift(DOWN * 2.5)

        self.play(Create(lowGroup), Create(highGroup), Create(midGroup), run_time=0.6)

        while low <= high:
            self.play(list_elements[mid].ClearSelection(), run_time=0.2)
            mid = (low + high) // 2
            mid_pos = list_elements[mid].getListElement().get_center()
            self.play(midGroup.animate.move_to(mid_pos + 1.7 * UP), run_time=0.4)
            self.play(list_elements[mid].SelectElement(), run_time=0.2)

            self.wait(0.4)

            if array[mid] == target:
                self.play(FadeOut(lowGroup), FadeOut(highGroup))
                break
            elif array[mid] < target:
                low = mid + 1
                self.play(Write(midSmallerText), run_time=0.2)
                self.wait(1)
                self.play(FadeOut(midSmallerText), run_time=0.2)
            else:
                high = mid - 1
                self.play(Write(midGreaterText), run_time=0.2)
                self.wait(1)
                self.play(FadeOut(midGreaterText), run_time=0.2)

            if low == high:
                deviation = 0.8
            else:
                deviation = 0
            
            self.play(
                lowGroup.animate.move_to(list_elements[low].getListElement().get_center() + (1.7 * UP) + (deviation * LEFT)),
                highGroup.animate.move_to(list_elements[high].getListElement().get_center() + (1.7 * UP) + (deviation * RIGHT)),
                run_time=0.4
            )
            
            self.wait(0.4)

        self.play(FadeOut(midGroup))
        self.wait(1)
