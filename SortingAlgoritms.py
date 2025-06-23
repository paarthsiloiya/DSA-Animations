from manim import *
from manim.utils.unit import Percent, Pixels
from manim import CurvedArrow

# manim -ql -p SortingAlgoritms.py SelectionSort
config.frame_width = 16
config.frame_height = 9


BASECOL = ManimColor.from_hex("#ebe7f3")
TEXTCOL = ManimColor.from_hex("#000000")
SELCOL = ManimColor.from_hex("#7a5bae")
SORTCOL = ManimColor.from_hex("#4a2a90")

FSIZE = 40
FONT = 'JetBrains Mono'

class ListElement():
    def __init__(self, value : str):
        self.size = 0.8
        self.value = int(value)
        self.isSorted = False
        self.elementValue = Text(value, font_size=(100*self.size), color=TEXTCOL, font=FONT)
        self.circle = Circle(radius=self.size, color=BASECOL, fill_opacity=1)
        self.elementValue.move_to(self.circle.get_center())
        self.elementGroup = VGroup(self.circle, self.elementValue)

    def getListElement(self):
        return self.elementGroup

    def SelectElement(self):
        return self.circle.animate.set_stroke(color=SELCOL, width=10)
    
    def ClearSelection(self):
        if not self.isSorted:
            return self.circle.animate.set_stroke(color=BASECOL)
        else:
            return self.circle.animate.set_stroke(color=SORTCOL)
    
    def MarkSorted(self):
        self.isSorted = True
        return self.circle.animate.set_fill(color=SORTCOL).set_stroke(width=0), self.elementValue.animate.set_color(color=WHITE)


class BubbleSort(Scene):
    def construct(self):
        values = [5, 2, 4, 6, 3, 1]
        list_elements = [ListElement(str(i)) for i in values]
        visuals = VGroup(*[el.getListElement() for el in list_elements])
        visuals.arrange(RIGHT, buff=0.5)
        # visuals.shift(DOWN)
        # itext = Text("i = 0", font="Courier New", font_size=FSIZE)
        # jtext = Text("j = 0", font="Courier New", font_size=FSIZE)

        # itext.to_corner(UR)
        # jtext.next_to(itext, DOWN, buff=0.3)

        # code_lines = [
        #     "| for i in range(n):",
        #     "|    for j in range(n - i - 1):",
        #     "|        if arr[j] > arr[j+1]:",
        #     "|            swap(arr[j], arr[j+1])"
        # ]
        # code_text = VGroup(*[Text(line, font="Courier New", font_size=FSIZE) for line in code_lines])
        # code_text.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UL)

        # highlight_box = SurroundingRectangle(code_text[3], color=YELLOW, buff=0.2)
        # highlight_box.move_to(code_text[0], aligned_edge=LEFT)
        self.add(visuals)#, itext, jtext, code_text, highlight_box)
        
        n = len(list_elements)

        for i in range(n):
            # new_text_i = Text(f"i = {i}", font="Courier New", font_size=FSIZE).to_corner(UR)
            # self.play(highlight_box.animate.move_to(code_text[0], aligned_edge=LEFT), run_time=0.2)
            # self.play(Transform(itext, new_text_i), run_time=0.2)
            # self.wait(0.3)
            for j in range(n - i - 1):
                # self.play(highlight_box.animate.move_to(code_text[1], aligned_edge=LEFT), run_time=0.2)
                # new_text_j = Text(f"j = {j}", font="Courier New", font_size=FSIZE).next_to(itext, DOWN, buff=0.3)
                # self.play(Transform(jtext, new_text_j), run_time=0.2)
                # # Select both elements
                # self.wait(0.3)
                # self.play(highlight_box.animate.move_to(code_text[2], aligned_edge=LEFT), run_time=0.2)

                self.play(
                    list_elements[j].SelectElement(),
                    list_elements[j + 1].SelectElement(),
                    run_time=0.2
                )

                # Compare values
                val1 = list_elements[j].value
                val2 = list_elements[j + 1].value

                if val1 > val2:
                    # self.wait(0.2)
                    # self.play(highlight_box.animate.move_to(code_text[3], aligned_edge=LEFT), run_time=0.2)
                    self.wait(0.2)
                    # Swap visuals
                    pos1 = list_elements[j].getListElement().get_center() + DOWN
                    pos2 = list_elements[j + 1].getListElement().get_center() + DOWN
                    
                    arrow1 = CurvedArrow(pos1, pos2, angle=PI / 2, color=SORTCOL)
                    arrow2 = CurvedArrow(pos2, pos1, angle=-PI / 2, color=SORTCOL)
                    swapText = Text("Swap!", color=SORTCOL, font=FONT).next_to(arrow1, DOWN)

                    self.play(Create(arrow1), Create(arrow2), run_time=0.3)
                    self.play(Write(swapText), run_time=0.4)

                    self.play(
                        list_elements[j].getListElement().animate.move_to(list_elements[j + 1].getListElement().get_center()),
                        list_elements[j + 1].getListElement().animate.move_to(list_elements[j].getListElement().get_center()),
                        run_time=0.3
                    )
                    # Swap data in the list
                    list_elements[j], list_elements[j + 1] = list_elements[j + 1], list_elements[j]
                    self.play(FadeOut(arrow1), FadeOut(arrow2), FadeOut(swapText), run_time=0.2)
                else:
                    self.wait(0.2)
                # Deselect both elements
                self.play(
                    list_elements[j].ClearSelection(),
                    list_elements[j + 1].ClearSelection(),
                    run_time=0.2
                )
                self.wait(0.3)

            self.play(*(list_elements[n - i - 1].MarkSorted()), run_time=0.3)

        # self.wait(0.2)
        # self.play(FadeOut(highlight_box), run_time=0.2)
        self.wait(1)


class InsertionSort(Scene):
    def construct(self):
        values = [5, 2, 4, 6, 3, 1]
        list_elements = [ListElement(str(v)) for v in values]
        visuals = VGroup(*[el.getListElement() for el in list_elements]).arrange(RIGHT, buff=0.5)#.move_to(DOWN * 1.5)
        # itext = Text("i = 0", font="Courier New", font_size=FSIZE)
        # jtext = Text("j = 0", font="Courier New", font_size=FSIZE)

        # itext.to_corner(UR)
        # jtext.next_to(itext, DOWN, buff=0.3)

        # code_lines = [
        #     "| for i in range(1, n):",
        #     "| insert_index = i",
        #     "| current_value = my_array[i]",
        #     "| for j in range(i - 1, -1, -1):",
        #     "|     if my_array[j] > current_value:",
        #     "|         my_array[j + 1] = my_array[j]",
        #     "|         insert_index = j",
        #     "|     else:",
        #     "|         break",
        #     "| my_array[insert_index] = current_value"
        # ]

        # code_text = VGroup(*[Text(line, font="Courier New", font_size=FSIZE-17) for line in code_lines])
        # code_text.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL)

        # highlight_box = SurroundingRectangle(code_text[5], color=YELLOW, buff=0.05)
        # highlight_box.move_to(code_text[0], aligned_edge=LEFT)

        self.add(visuals)#, itext, jtext, code_text, highlight_box)

        self.play(*(list_elements[0].MarkSorted()))

        for i in range(1, len(list_elements)):
            # new_text_i = Text(f"i = {i}", font="Courier New", font_size=FSIZE).to_corner(UR)
            # self.play(highlight_box.animate.move_to(code_text[0], aligned_edge=LEFT), run_time=0.2)
            # self.play(Transform(itext, new_text_i), run_time=0.2)
            # self.wait(0.3)
            current = list_elements[i]
            current_value = current.value
            current_pos = current.getListElement().get_center()
            
            self.play(current.elementGroup.animate.shift(UP * 2), run_time=0.4)

            j = i - 1
            insert_index = i

            backToPos = True

            while j >= 0 and list_elements[j].value > current_value:
                # self.play(highlight_box.animate.move_to(code_text[1], aligned_edge=LEFT), run_time=0.2)
                # new_text_j = Text(f"j = {j}", font="Courier New", font_size=FSIZE).next_to(itext, DOWN, buff=0.3)
                # self.play(Transform(jtext, new_text_j), run_time=0.2)
                # Select both elements
                # self.play(highlight_box.animate.move_to(code_text[2], aligned_edge=LEFT), run_time=0.2)
                self.wait(0.3)

                backToPos = False
                self.play(list_elements[j].SelectElement(), run_time=0.2)

                shiftArrow = CurvedArrow(list_elements[j].getListElement().get_center() + DOWN, list_elements[j].getListElement().get_center() + DOWN + (RIGHT * 1.3), angle=PI / 2, color=SORTCOL)
                shiftText = Text("Shift", color=SORTCOL, font=FONT).next_to(shiftArrow, DOWN)
                self.play(Create(shiftArrow), run_time=0.3)
                self.play(Write(shiftText), run_time=0.2)

                # Move element to the right
                self.play(list_elements[j].getListElement().animate.shift(RIGHT * 2.1), run_time=0.3)

                self.play(FadeOut(shiftArrow), FadeOut(shiftText), run_time=0.2)

                self.play(list_elements[j].ClearSelection(), run_time=0.2)
                # Shift in list
                list_elements[j + 1] = list_elements[j]
                insert_index = j
                j -= 1

            if not backToPos:
                target_pos = list_elements[insert_index].getListElement().get_center()
                target_pos = target_pos + (LEFT * 2.1)  # back to row level
            else:
                target_pos = current_pos
                self.wait(0.5)

            
            self.play(current.elementGroup.animate.move_to(target_pos), run_time=0.4)
            list_elements[insert_index] = current

            self.play(*(current.MarkSorted()), run_time=0.15)
            self.wait(0.2)

        self.wait(1)


class SelectionSort(Scene):
    def construct(self):
        values = [5, 2, 4, 6, 3, 1]
        list_elements = [ListElement(str(v)) for v in values]
        visuals = VGroup(*[el.getListElement() for el in list_elements]).arrange(RIGHT, buff=0.5)
        self.add(visuals)

        def make_arrow(idx, label):
            arrow = Arrow(start=list_elements[idx].getListElement().get_center() + (UP * 2),
                          end=list_elements[idx].getListElement().get_center() + UP,
                          max_stroke_width_to_length_ratio=5,
                          color=SORTCOL)
            text = Text(label, color=SORTCOL, font=FONT).scale(0.5).next_to(arrow, UP, buff=0.1)
            return VGroup(arrow, text)

        for i in range(len(values)):
            min_index = i
            min_index_group = make_arrow(min_index, "Min Value")
            self.play(Create(min_index_group))            
            for j in range(i + 1, len(values)):
                self.play(list_elements[j].SelectElement(), run_time=0.2)
                if values[j] < values[min_index]:
                    min_index = j
                    self.wait(0.3)
                    self.play(min_index_group.animate.move_to(list_elements[min_index].getListElement().get_center() + (UP * 1.7)), run_time=0.3)
                self.wait(0.2)
                self.play(list_elements[j].ClearSelection(), run_time=0.2)
                self.wait(0.1)
            self.play(FadeOut(min_index_group), run_time=0.2)


            pos1 = list_elements[i].getListElement().get_center() + DOWN
            pos2 = list_elements[min_index].getListElement().get_center() + DOWN
            
            arrow1 = CurvedArrow(pos1, pos2, angle=PI / 2, color=SORTCOL)
            arrow2 = CurvedArrow(pos2, pos1, angle=-PI / 2, color=SORTCOL)
            swapText = Text("Swap!", color=SORTCOL, font=FONT).next_to(arrow1, DOWN)

            self.play(Create(arrow1), Create(arrow2), run_time=0.3)
            self.play(Write(swapText), run_time=0.4)
            self.wait(0.2)
            self.play(
                list_elements[i].getListElement().animate.move_to(list_elements[min_index].getListElement().get_center()),
                list_elements[min_index].getListElement().animate.move_to(list_elements[i].getListElement().get_center()),
                run_time=0.3
            )
            # Swap data in the list
            list_elements[i], list_elements[min_index] = list_elements[min_index], list_elements[i]

            self.wait(0.1)
            self.play(FadeOut(arrow1), FadeOut(arrow2), FadeOut(swapText), run_time=0.2)

            self.play(*(list_elements[i].MarkSorted()), run_time=0.2)

            values[i], values[min_index] = values[min_index], values[i]

        self.wait(1)


class MergeSort(Scene):
    def construct(self):
        values = [5, 2, 4, 6, 3, 1]
        list_elements = [ListElement(str(i)) for i in values]
        visuals = VGroup(*[el.getListElement() for el in list_elements]).set_z_index(10)
        visuals.arrange(RIGHT, buff=0.6)
        self.add(visuals)
        self.wait(0.5)

        self.recursive_merge_sort(list_elements, 0, len(values) - 1, 0.55)

        self.wait(0.7)

    def recursive_merge_sort(self, arr : list[ListElement], left : int, right : int, buff_adjust):
        if left >= right:
            return

        mid = (left + right) // 2

        # Highlight current subarray
        rect = SurroundingRectangle(VGroup(*[arr[i].getListElement() for i in range(left, right + 1)]), color=SORTCOL, buff=buff_adjust, corner_radius=0.3, stroke_width=0.5)
        self.play(Create(rect), run_time=0.3)

        self.recursive_merge_sort(arr, left, mid, buff_adjust-0.12)
        self.recursive_merge_sort(arr, mid + 1, right, buff_adjust-0.12)

        self.merge(arr, left, mid, right)
        self.play(FadeOut(rect), run_time=0.2)


    def merge(self, arr : list[ListElement], left:int, mid:int, right:int):
        target_positions = [arr[i].getListElement().get_center() + (UP * 2.6) for i in range(left, right + 1)]
        left_group = arr[left:mid + 1]
        right_group = arr[mid + 1:right + 1]
        
        left_rect = SurroundingRectangle(VGroup(*[left_group[i].getListElement() for i in range(len(left_group))]), color=SORTCOL, buff=0.14, corner_radius=0.3)
        right_rect = SurroundingRectangle(VGroup(*[right_group[i].getListElement() for i in range(len(right_group))]), color=SORTCOL, buff=0.14, corner_radius=0.3)
        self.play(Create(left_rect), Create(right_rect), run_time=0.3)
        self.wait(0.2)

        left_vals = [int(el.value) for el in left_group]
        right_vals = [int(el.value) for el in right_group]

        merged : list[tuple[ListElement, int]] = []
        i = j = 0
        k = left

        while i < len(left_vals) and j < len(right_vals):
            eli, elj = left_group[i], right_group[j]
            self.play(eli.SelectElement(), elj.SelectElement(), run_time=0.2)
            self.wait(0.2)
            if left_vals[i] <= right_vals[j]:
                merged.append((left_group[i], left_vals[i]))
                explanatoryText = Text(f"{left_vals[i]} <= {right_vals[j]}", color=SORTCOL, font_size=60, font=FONT).shift(DOWN * 2.5)
                self.play(Write(explanatoryText), run_time=0.3)
                self.wait(0.6)
                self.play(FadeOut(explanatoryText), run_time=0.2)
                i += 1
            else:
                merged.append((right_group[j], right_vals[j]))
                explanatoryText = Text(f"{left_vals[i]} >= {right_vals[j]}", color=SORTCOL, font_size=60, font=FONT).shift(DOWN * 2.5)
                self.play(Write(explanatoryText), run_time=0.3)
                self.wait(0.6)
                self.play(FadeOut(explanatoryText), run_time=0.2)
                j += 1

            animations = []
            for index, (el, val) in enumerate(merged):
                animations.append(el.getListElement().animate.move_to(target_positions[index]))
            self.play(*animations, run_time=1)

            self.play(eli.ClearSelection(), elj.ClearSelection(), run_time=0.2)


        while i < len(left_vals):
            self.play(left_group[i].SelectElement(), run_time=0.2)
            self.wait(0.2)
            merged.append((left_group[i], left_vals[i]))
            i += 1
        
            animations = []
            for index, (el, val) in enumerate(merged):
                animations.append(el.getListElement().animate.move_to(target_positions[index]))
            self.play(*animations, run_time=1)

            self.play(left_group[i-1].ClearSelection(), run_time=0.2)


        while j < len(right_vals):
            self.play(right_group[j].SelectElement(), run_time=0.2)
            self.wait(0.2)
            merged.append((right_group[j], right_vals[j]))
            j += 1

            animations = []
            for index, (el, val) in enumerate(merged):
                animations.append(el.getListElement().animate.move_to(target_positions[index]))
            self.play(*animations, run_time=1)

            self.play(right_group[j-1].ClearSelection(), run_time=0.2)


        self.play(FadeOut(left_rect), FadeOut(right_rect), run_time=0.2)
        self.wait(0.2)

        animations = []
        for index, (el, val) in enumerate(merged):
            animations.append(el.getListElement().animate.shift(DOWN * 2.6))
        self.play(*animations, run_time=1)


        # Update the array reference to new order
        for i, (el, val) in enumerate(merged):
            arr[left + i] = el


class QuickSort(Scene):
    def construct(self):
        values = [5, 2, 4, 6, 3, 1]
        list_elements = [ListElement(str(i)) for i in values]
        visuals = VGroup(*[el.getListElement() for el in list_elements]).set_z_index(10)
        visuals.arrange(RIGHT, buff=0.6)
        self.add(visuals)
        self.wait(0.5)
        self.quickSort(list_elements, 0, len(values) - 1)
        self.wait(1)
    

    def quickSort(self, arr : list[ListElement], low : int, high : int):
        if low < high:
            pi = self.partition(arr, low, high)
            self.quickSort(arr, low, pi - 1)
            self.quickSort(arr, pi + 1, high)
        else:
            self.play(*(arr[low].MarkSorted()), run_time=0.2)
            self.wait(0.4)

    def partition(self, arr : list[ListElement], low : int, high : int):
        def make_arrow(idx:int, label:str):
            arrow = Arrow(start=arr[idx].getListElement().get_center() + (UP * 2),
                          end=arr[idx].getListElement().get_center() + UP,
                          max_stroke_width_to_length_ratio=5,
                          color=SORTCOL)
            text = Text(label, color=SORTCOL, font=FONT).scale(0.5).next_to(arrow, UP, buff=0.1)
            return VGroup(arrow, text)
        
        array = [(el.value) for el in arr]
        pivot = array[high]
        pivot_element = arr[high]
        self.play(pivot_element.SelectElement(), run_time=0.2)
        self.wait(0.2)

        i = low - 1
        i_group = make_arrow(i, "i")
        if i < 0:
            i_group.move_to(arr[0].getListElement().get_center() + (UP * 1.7)).shift(LEFT * 1.8)
        
        self.play(Create(i_group), run_time=0.2)
        
        j_group = make_arrow(low, "j")
        self.play(Create(j_group), run_time=0.2)
        for j in range(low, high):
            if i >= 0:
                self.play(j_group.animate.move_to(arr[j].getListElement().get_center() + (UP * 1.7)), i_group.animate.move_to(arr[i].getListElement().get_center() + (UP * 1.7)), run_time=0.3)
            else:
                self.play(j_group.animate.move_to(arr[j].getListElement().get_center() + (UP * 1.7)), run_time=0.3)
            self.wait(0.2)
            if array[j] < pivot:
                explanatoryText = Text(f"{array[j]}<={pivot} : i++", color=SORTCOL, font_size=60, font=FONT).shift(DOWN * 3)
                self.play(Write(explanatoryText), run_time=0.3)
                self.wait(0.6)
                self.play(FadeOut(explanatoryText), run_time=0.2)
                self.wait(0.2)

                i += 1
                if i == j:
                    self.play(j_group.animate.shift(RIGHT * 0.3), i_group.animate.move_to(arr[i].getListElement().get_center() + (UP * 1.7) + (LEFT * 0.3)), run_time=0.3)
                else:
                    self.play(i_group.animate.move_to(arr[i].getListElement().get_center() + (UP * 1.7)), run_time=0.3)
                
                self.swap(arr, i, j, "Swap i and j")
                self.wait(0.1)
            else:
                explanatoryText = Text(f"{array[j]}>={pivot}", color=SORTCOL, font_size=60, font=FONT).shift(DOWN * 3)
                self.play(Write(explanatoryText), run_time=0.3)
                self.wait(0.6)
                self.play(FadeOut(explanatoryText), run_time=0.2)
                self.wait(0.3)
        
        self.play(FadeOut(j_group), run_time=0.2)

        explanatoryText = Text("Increment i", color=SORTCOL, font_size=40, font=FONT).shift(DOWN * 3)
        self.play(Write(explanatoryText), run_time=0.3)
        self.wait(0.6)
        self.play(FadeOut(explanatoryText), run_time=0.2)
        self.wait(0.1)

        self.play(i_group.animate.move_to(arr[i + 1].getListElement().get_center() + (UP * 1.7)), run_time=0.3)
        self.swap(arr, i + 1, high, "Swap i and pivot")
        self.wait(0.2)

        self.play(*(arr[i+1].MarkSorted()))
        self.wait(0.2)

        self.play(FadeOut(i_group), run_time=0.2)
        self.play(pivot_element.ClearSelection(), run_time=0.2)
        self.wait(0.3)

        return i + 1

    def swap(self, arr : list[ListElement], i : int, j : int, text_for_swap : str):
        pos1 = arr[i].getListElement().get_center() + DOWN
        pos2 = arr[j].getListElement().get_center() + DOWN
        
        arrow1 = CurvedArrow(pos1, pos2, angle=PI / 2, color=SORTCOL)
        arrow2 = CurvedArrow(pos2, pos1, angle=-PI / 2, color=SORTCOL)
        swapText = Text(text_for_swap, color=SORTCOL, font=FONT).next_to(arrow1, DOWN)

        self.play(Create(arrow1), Create(arrow2), run_time=0.3)
        self.play(Write(swapText), run_time=0.4)

        self.play(
            arr[i].getListElement().animate.move_to(arr[j].getListElement().get_center()),
            arr[j].getListElement().animate.move_to(arr[i].getListElement().get_center()),
            run_time=0.3
        )

        self.wait(0.1)
        self.play(FadeOut(arrow1), FadeOut(arrow2), FadeOut(swapText), run_time=0.2)

        arr[i], arr[j] = arr[j], arr[i]
    

