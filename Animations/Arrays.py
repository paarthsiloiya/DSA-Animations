from manim import *
from manim.utils.unit import Percent, Pixels
from manim import CurvedArrow
import random
from env_config import *

random.seed(30)

# Override specific font sizes for Arrays
POINTER_FONT_SIZE = 32      # For "Low", "High", "Mid", etc.


class ListElement(VGroup):
    def __init__(self, value : int, size:int=0.8, mult:int=100):
        super().__init__()
        self.size = size
        self.value = value
        self.isFound = False
        self.elementValue = Text(str(self.value), font_size=(mult*self.size), color=TEXTCOL, font=FONT)
        self.circle = Circle(radius=self.size, color=BASECOL, fill_opacity=1)
        self.elementValue.move_to(self.circle.get_center())
        self.add(self.circle, self.elementValue)

    def Select(self):
        return self.circle.animate.set_stroke(color=SELCOL, width=10)
    
    def Clear(self):
        if not self.isFound:
            return self.circle.animate.set_stroke(color=BASECOL)
        else:
            return self.circle.animate.set_stroke(color=SORTCOL)

class Node(VGroup):
    def __init__(self, value):
        super().__init__()
        self.text = Text(str(value), font=FONT, color=TEXTCOL, font_size=2*FSIZE)
        self.circle = Circle(radius=0.8, color=NODE_COL, fill_color=NODE_COL, fill_opacity=1, stroke_width=0)
        self.text.move_to(self.circle.get_center())
        self.add(self.circle, self.text)

    def Select(self):
        return self.circle.animate.set_stroke(color=SORTCOL, width=10)
    
    def Clear(self):
            return self.circle.animate.set_stroke(color=NODE_COL, width=0)
        
    def Highlight(self):
        return self.circle.animate.set_fill(color=SORTCOL), self.text.animate.set_color(color=BASECOL)

class MemoryAllocation(Scene):
    def construct(self):
        array = [5, 2, 4, 6, 3, 1]
        list_elements = [ListElement(i) for i in array]
        visuals = VGroup(*list_elements)
        visuals.arrange(RIGHT, buff=0.5)
        self.add(visuals)

        self.wait(0.5)

        nodeSurr = DashedVMobject(SurroundingRectangle(visuals[0], color=TEXTCOL, buff=0.15, corner_radius=0.9))
        nodeText = Text("List Element", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, UP, buff=0.1)
        self.play(
            Create(nodeSurr),
            Write(nodeText),
            run_time=0.5
        )
        self.wait(0.5)
        self.play(FadeOut(nodeSurr), FadeOut(nodeText), run_time=0.2)

        head_address = random.randint(1000, 9999)
        addresses = [head_address + i for i in range(len(array))]
        address_labels = VGroup(
            *[Text('0x' + str(addr), font_size=ADDRESS_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(el, UP) for el, addr in zip(visuals, addresses)]
        )

        self.play(Write(address_labels), run_time=0.5)

        self.wait(0.5)
        nodeSurr = DashedVMobject(SurroundingRectangle(address_labels[0], color=TEXTCOL, buff=0.15, corner_radius=0.1), num_dashes=18)
        nodeText = Text("Memory Location", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, UP, buff=0.1)
        self.play(
            Create(nodeSurr),
            Write(nodeText),
            run_time=0.5
        )
        self.wait(0.5)
        self.play(FadeOut(nodeSurr), FadeOut(nodeText), run_time=0.2)

        self.wait(1)
        

class Indexing(Scene):
    def construct(self):
        array = [5, 2, 4, 6, 3, 1]
        list_elements = [ListElement(i) for i in array]
        visuals = VGroup(*list_elements)
        visuals.arrange(RIGHT, buff=0.5)
        self.add(visuals)

        self.wait(0.5)

        operationText = Text("Forward Indexing", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE)
        operationText.to_edge(UP, buff=0.5)
        self.play(Write(operationText), run_time=0.5)
        self.wait(0.2)

        index_labels = VGroup(
            *[Text(str(i), font_size=ADDRESS_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(el.circle, DOWN) for i, el in enumerate(list_elements)]
        )
        self.play(Write(index_labels), run_time=0.5)

        self.wait(0.5)
        nodeSurr = DashedVMobject(SurroundingRectangle(index_labels[0], color=TEXTCOL, buff=0.15, corner_radius=0.1), num_dashes=18)
        nodeText = Text("Index", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, DOWN, buff=0.1)
        self.play(
            Create(nodeSurr),
            Write(nodeText),
            run_time=0.5
        )
        self.wait(0.5)
        self.play(FadeOut(nodeSurr), FadeOut(nodeText), run_time=0.2)
        self.play(FadeOut(operationText), FadeOut(index_labels), run_time=0.5)

        self.wait(1)

        operationText = Text("Reverse Indexing", font=FONT, color=TEXTCOL, font_size=EXPLANATORY_FONT_SIZE)
        operationText.to_edge(UP, buff=0.5)
        self.play(Write(operationText), run_time=0.5)

        reverse_index_labels = VGroup(
            *[Text(str(i - len(array)), font_size=ADDRESS_FONT_SIZE, font=FONT, color=TEXTCOL).next_to(el.circle, DOWN) for i, el in enumerate(list_elements)]
        )

        self.play(Write(reverse_index_labels), run_time=0.5)
        self.wait(0.5)
        nodeSurr = DashedVMobject(SurroundingRectangle(reverse_index_labels[0], color=TEXTCOL, buff=0.15, corner_radius=0.1), num_dashes=18)
        nodeText = Text("Index", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, DOWN, buff=0.1)
        self.play(
            Create(nodeSurr),
            Write(nodeText),
            run_time=0.5
        )

        self.wait(0.5)
        self.play(FadeOut(nodeSurr), FadeOut(nodeText), run_time=0.2)
        self.play(FadeOut(operationText), FadeOut(reverse_index_labels), run_time=0.5)

        self.wait(1)

class TwoDArraysAsMatrix(Scene):
    def construct(self):
        array = [
            [5, 2, 8],
            [6, 3, 1],
            [4, 7, 9]
        ]

        matrix = Matrix(array, h_buff=0.8, v_buff=0.8,
                        element_to_mobject_config={"font_size": 50, "color": TEXTCOL},
                        bracket_config={"color": TEXTCOL})

        self.play(Create(matrix), run_time=0.5)
        self.wait(0.5)
        self.play(matrix.animate.to_edge(UL), run_time=0.3)
        self.wait(0.5)

        mobject_matrix = Matrix(array, h_buff=1.8, v_buff=1.8,
                                element_to_mobject=Node)

        self.play(Create(mobject_matrix), run_time=1)
        self.wait(1)

        i = ValueTracker(0)
        j = ValueTracker(0)

        i_pointer = Text("i ->", font_size=POINTER_FONT_SIZE, font=FONT, color=POINTER_FONT_COLOR)
        j_pointer = VGroup(
            Text("j", font_size=POINTER_FONT_SIZE, font=FONT, color=POINTER_FONT_COLOR),
            Text("->", font_size=POINTER_FONT_SIZE, font=FONT, color=POINTER_FONT_COLOR).rotate(-PI/2)
        ).arrange(DOWN)

        def update_i_pointer(m):
            current_i = i.get_value()
            # Get the fractional part for interpolation
            frac = current_i - int(current_i)
            current_row = int(current_i)
            next_row = min(current_row + 1, len(mobject_matrix.get_rows()) - 1)
            
            # Get positions of current and next rows
            current_pos = mobject_matrix.get_rows()[current_row].get_center()
            next_pos = mobject_matrix.get_rows()[next_row].get_center()
            
            # Interpolate between positions
            interpolated_pos = current_pos + frac * (next_pos - current_pos)
            target_point = interpolated_pos + LEFT * (mobject_matrix.get_rows()[current_row].get_width()/2 + 0.1)
            m.move_to(target_point + LEFT * m.get_width()/2)

        def update_j_pointer(m):
            current_j = j.get_value()
            # Get the fractional part for interpolation
            frac = current_j - int(current_j)
            current_col = int(current_j)
            next_col = min(current_col + 1, len(mobject_matrix.get_columns()) - 1)
            
            # Get positions of current and next columns
            current_pos = mobject_matrix.get_columns()[current_col].get_center()
            next_pos = mobject_matrix.get_columns()[next_col].get_center()
            
            # Interpolate between positions
            interpolated_pos = current_pos + frac * (next_pos - current_pos)
            target_point = interpolated_pos + UP * (mobject_matrix.get_columns()[current_col].get_height()/2 + 0.1)
            m.move_to(target_point + UP * m.get_height()/2)

        i_pointer.add_updater(update_i_pointer)
        j_pointer.add_updater(update_j_pointer)

        i_text = DecimalNumber(i.get_value(), font_size=FSIZE, color=TEXTCOL, num_decimal_places=0)
        j_text = DecimalNumber(j.get_value(), font_size=FSIZE, color=TEXTCOL, num_decimal_places=0)

        i_text.add_updater(lambda m: m.set_value(i.get_value()))
        j_text.add_updater(lambda m: m.set_value(j.get_value()))

        i_text_group = VGroup(Text("i = ", font_size=FSIZE, color=TEXTCOL), i_text).arrange(RIGHT, buff=0.1).to_edge(RIGHT, buff=0.8)
        j_text_group = VGroup(Text("j = ", font_size=FSIZE, color=TEXTCOL), j_text).arrange(RIGHT, buff=0.1).to_edge(RIGHT, buff=0.8).next_to(i_text_group, DOWN, buff=0.5)

        self.play(Write(i_pointer), Write(j_pointer), Write(i_text_group), Write(j_text_group), run_time=0.5)
        self.wait(1)

        # self.play(
        #     i.animate.set_value(1),
        #     j.animate.set_value(2),
        #     run_time=1
        # )

        for x in range(3):
            for y in range(3):
                self.play(
                    i.animate.set_value(x),
                    j.animate.set_value(y),
                    run_time=0.3
                )
                self.play(
                    mobject_matrix.get_entries()[x * 3 + y].Select(), 
                    matrix.get_entries()[x * 3 + y].animate.set_color(SELCOL),
                    run_time=0.3
                )
                self.wait(0.4)
                self.play(
                    mobject_matrix.get_entries()[x * 3 + y].Clear(), 
                    matrix.get_entries()[x * 3 + y].animate.set_color(TEXTCOL),
                    run_time=0.2
                )
                self.wait(0.1)

        self.wait(1)

        self.play(
            FadeOut(i_pointer), 
            FadeOut(j_pointer), 
            FadeOut(i_text_group), 
            FadeOut(j_text_group),
            run_time=0.5
        )

        self.wait(1)


class TwoDArraysMultiplication(Scene):
    def construct(self):
        arrayA = [
            [5, 2, 8],
            [6, 3, 1],
            [4, 7, 9]
        ]

        arrayB = [
            [1, 9, 2],
            [3, 4, 5],
            [6, 7, 8]
        ]

        matrixA = Matrix(arrayA, h_buff=0.5, v_buff=0.5, bracket_h_buff=0.2, bracket_v_buff=0.2,
                        element_to_mobject_config={"font_size": 40, "color": TEXTCOL},
                        bracket_config={"color": TEXTCOL}
                )
        matrixB = Matrix(arrayB, h_buff=0.5, v_buff=0.5, bracket_h_buff=0.2, bracket_v_buff=0.2,
                        element_to_mobject_config={"font_size": 40, "color": TEXTCOL},
                        bracket_config={"color": TEXTCOL}
                )

        self.play(Create(matrixA), run_time=0.5)
        self.wait(0.5)
        self.play(matrixA.animate.to_edge(UL), run_time=0.3)
        self.wait(0.5)
        self.play(Create(matrixB), run_time=0.5)
        self.wait(0.5)
        self.play(matrixB.animate.next_to(matrixA, RIGHT, buff=0.5), run_time=0.3)

        mobject_matrixA = Matrix(arrayA, h_buff=1.3, v_buff=1.3,
                                element_to_mobject=ListElement,
                                element_to_mobject_config={"size": 0.5})
        mobject_matrixB = Matrix(arrayB, h_buff=1.3, v_buff=1.3,
                                element_to_mobject=ListElement,
                                element_to_mobject_config={"size": 0.5}).shift(RIGHT * 2.5)

        self.play(Create(mobject_matrixA), run_time=1)
        self.play(mobject_matrixA.animate.shift(LEFT * 2.5), run_time=0.3)
        self.play(Create(mobject_matrixB), run_time=1)

        self.play(VGroup(mobject_matrixA, mobject_matrixB).animate.to_edge(LEFT, buff=0.2).shift(DOWN * 0.5), run_time=0.3)
        self.wait(1)

        self.play(
            Write(MathTex(r"\times", font_size=FSIZE, color=TEXTCOL).next_to(matrixA, RIGHT, buff=0.15)), 
            Write(MathTex(r"\times", font_size=2*FSIZE, color=TEXTCOL).next_to(mobject_matrixA, RIGHT, buff=0.1)),
            run_time=0.5
        )

        self.play(
            Write(MathTex(r"=", font_size=FSIZE, color=TEXTCOL).next_to(matrixB, RIGHT, buff=0.15)), 
            Write(MathTex(r"=", font_size=2*FSIZE, color=TEXTCOL).next_to(mobject_matrixB, RIGHT, buff=0.2)),
            run_time=0.5
        )

        self.wait(1)

        result_matrix = Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]], h_buff=2.8, v_buff=0.5,
                                bracket_h_buff=2.2, 
                                element_to_mobject_config={"font_size": 40, "color": TEXTCOL},
                                bracket_config={"color": TEXTCOL}
                ).next_to(matrixB, RIGHT, buff=0.5)
        self.play(Create(result_matrix), run_time=0.5)
        result_array = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        for i in range(len(arrayA)):
            for j in range(len(arrayB[0])):
                surrRecti = SurroundingRectangle(matrixA.get_rows()[i], color=SORTCOL, buff=0.15, corner_radius=0.1)
                surrRectj = SurroundingRectangle(matrixB.get_columns()[j], color=SORTCOL, buff=0.15, corner_radius=0.1)
                self.play(
                    Create(surrRecti),
                    Create(surrRectj),
                    run_time=0.3
                )
                sum = 0
                terms = []
                for k in range(len(arrayB)):
                    sum += arrayA[i][k] * arrayB[k][j]
                    result_array[i][j] += arrayA[i][k] * arrayB[k][j]
                    terms.append(f"({arrayA[i][k]} \\times {arrayB[k][j]})")
                    self.play(
                        mobject_matrixA.get_entries()[i * len(arrayA[0]) + k].Select(),
                        mobject_matrixB.get_entries()[k * len(arrayB[0]) + j].Select(),
                        matrixA.get_entries()[i * len(arrayA[0]) + k].animate.set_color(SELCOL),
                        matrixB.get_entries()[k * len(arrayB[0]) + j].animate.set_color(SELCOL),
                        run_time=0.3
                    )
                    self.wait(0.5)
                    new_tex = MathTex(" + ".join(terms), font_size=40, color=TEXTCOL).move_to(result_matrix.get_entries()[i * len(arrayB[0]) + j].get_center())
                    self.play(
                        result_matrix.get_entries()[i * len(arrayB[0]) + j].animate.become(new_tex),
                        run_time=0.2
                    )
                    self.play(
                        mobject_matrixA.get_entries()[i * len(arrayA[0]) + k].Clear(),
                        mobject_matrixB.get_entries()[k * len(arrayB[0]) + j].Clear(),
                        matrixA.get_entries()[i * len(arrayA[0]) + k].animate.set_color(TEXTCOL),
                        matrixB.get_entries()[k * len(arrayB[0]) + j].animate.set_color(TEXTCOL),
                        run_time=0.2
                    )


                self.wait(0.5)
                self.play(
                    result_matrix.get_entries()[i * len(arrayB[0]) + j].animate.become(
                        MathTex(str(sum), font_size=40, color=TEXTCOL).move_to(result_matrix.get_entries()[i * len(arrayB[0]) + j].get_center())
                    ),
                    run_time=0.2
                )
                self.play(
                    FadeOut(surrRecti),
                    FadeOut(surrRectj),
                    run_time=0.2
                )

        self.play(
            result_matrix.animate.become(
                Matrix(result_array, h_buff=0.7, v_buff=0.5, bracket_h_buff=0.2, bracket_v_buff=0.2,
                        element_to_mobject_config={"font_size": 40, "color": TEXTCOL},
                        bracket_config={"color": TEXTCOL}
                ).next_to(matrixB, RIGHT, buff=0.5)
            )
        )

        mobject_matrixR = Matrix(result_array, h_buff=1.4, v_buff=1.4,
                                element_to_mobject=ListElement,
                                element_to_mobject_config={"size": 0.5, "mult": 70}).next_to(mobject_matrixB, RIGHT, buff=1.7)
        self.play(Create(mobject_matrixR), run_time=0.5)
        self.wait(1)