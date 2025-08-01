from manim import *
from env_config import *

# Override specific font sizes for SortingAlgoritms
POINTER_FONT_SIZE = 28      # For "i", "j", "Min", etc. above arrows

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
        self.add(visuals)
        
        n = len(list_elements)

        self.wait(1)

        for i in range(n):
            for j in range(n - i - 1):
                self.play(
                    list_elements[j].SelectElement(),
                    list_elements[j + 1].SelectElement(),
                    run_time=0.2
                )

                # Compare values
                val1 = list_elements[j].value
                val2 = list_elements[j + 1].value

                # Show comparison text
                compare_text = Text(f"{val1} {'>' if val1 > val2 else '<='} {val2}", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).scale(1.3).next_to(visuals, DOWN, buff=1.9)
                self.play(Write(compare_text), run_time=0.2)

                if val1 > val2:
                    self.wait(0.2)
                    # Swap visuals
                    pos1 = list_elements[j].getListElement().get_center() + DOWN
                    pos2 = list_elements[j + 1].getListElement().get_center() + DOWN
                    
                    arrow = CurvedDoubleArrow(pos1, pos2, angle=PI / 2, color=SORTCOL)
                    swapText = Text("Swap!", color=SWAP_FONT_COLOR, font=FONT, font_size=SWAP_FONT_SIZE).next_to(arrow, DOWN)

                    self.play(Create(arrow), run_time=0.3)
                    self.play(Write(swapText), run_time=0.4)

                    self.play(
                        list_elements[j].getListElement().animate.move_to(list_elements[j + 1].getListElement().get_center()),
                        list_elements[j + 1].getListElement().animate.move_to(list_elements[j].getListElement().get_center()),
                        run_time=0.3
                    )
                    # Swap data in the list
                    list_elements[j], list_elements[j + 1] = list_elements[j + 1], list_elements[j]
                    self.play(FadeOut(arrow), FadeOut(swapText), run_time=0.2)
                else:
                    self.wait(0.2)

                # Fade out comparison text
                self.play(FadeOut(compare_text), run_time=0.2)

                # Deselect both elements
                self.play(
                    list_elements[j].ClearSelection(),
                    list_elements[j + 1].ClearSelection(),
                    run_time=0.2
                )
                self.wait(0.3)

            self.play(*(list_elements[n - i - 1].MarkSorted()), run_time=0.3)

        self.wait(1)


class InsertionSort(Scene):
    def construct(self):
        values = [5, 2, 4, 6, 3, 1]
        list_elements = [ListElement(str(v)) for v in values]
        visuals = VGroup(*[el.getListElement() for el in list_elements]).arrange(RIGHT, buff=0.5)
        self.add(visuals)

        self.play(*(list_elements[0].MarkSorted()))

        for i in range(1, len(list_elements)):
            current = list_elements[i]
            current_value = current.value
            current_pos = current.getListElement().get_center()
            
            self.play(current.elementGroup.animate.shift(UP * 2), run_time=0.4)

            j = i - 1
            insert_index = i

            backToPos = True

            while j >= 0 and list_elements[j].value > current_value:
                # Show comparison text
                val1 = list_elements[j].value
                val2 = current_value

                backToPos = False
                self.play(list_elements[j].SelectElement(), run_time=0.2)

                self.wait(0.3)
                compare_text = Text(f"{val1} > {val2}", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(visuals, DOWN, buff=1.7)
                self.play(Write(compare_text), run_time=0.2)
                self.wait(0.3)
                
                shiftArrow = CurvedArrow(list_elements[j].getListElement().get_center() + DOWN, list_elements[j].getListElement().get_center() + DOWN + (RIGHT * 1.3), angle=PI / 2, color=SORTCOL)
                shiftText = Text("Shift", color=SWAP_FONT_COLOR, font=FONT, font_size=SWAP_FONT_SIZE).next_to(shiftArrow, DOWN)
                self.play(Create(shiftArrow), run_time=0.3)
                self.play(Write(shiftText), run_time=0.2)

                # Move element to the right
                self.play(list_elements[j].getListElement().animate.shift(RIGHT * 2.1), run_time=0.3)

                self.play(FadeOut(shiftArrow), FadeOut(shiftText), FadeOut(compare_text), run_time=0.2)

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

        def get_arrow_position(idx, label, i_idx, min_idx):
            base = list_elements[idx].getListElement().get_center() + (UP * 1.7)
            if i_idx == min_idx:
                if label == "i":
                    return base + LEFT * 0.3
                elif label == "Min":
                    return base + RIGHT * 0.3
            return base

        self.wait(1)
        for i in range(len(values)):
            min_index = i
            i_index_group = make_arrow(i, "i").move_to(get_arrow_position(i, "i", i, min_index))
            min_index_group = make_arrow(min_index, "Min").move_to(get_arrow_position(min_index, "Min", i, min_index))
            self.play(Create(min_index_group), Create(i_index_group), run_time=0.3)           
            for j in range(i + 1, len(values)):
                self.play(list_elements[j].SelectElement(), run_time=0.2)
                if values[j] < values[min_index]:
                    self.wait(0.3)
                    compare_text = Text(f"{values[j]} < {values[min_index]}", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).next_to(visuals, DOWN, buff=1.5)
                    self.play(Write(compare_text), run_time=0.2)
                    min_index = j
                    self.wait(0.3)
                    # Move "Min" arrow, check for overlap with "i"
                    self.play(min_index_group.animate.move_to(get_arrow_position(min_index, "Min", i, min_index)), i_index_group.animate.move_to(get_arrow_position(i, "i", i, min_index)), run_time=0.3)
                    self.play(FadeOut(compare_text), run_time=0.2)
                self.wait(0.2)
                self.play(list_elements[j].ClearSelection(), run_time=0.2)
                self.wait(0.1)

            self.play(FadeOut(min_index_group), FadeOut(i_index_group), run_time=0.2)

            if min_index != i:
                pos1 = list_elements[i].getListElement().get_center() + DOWN
                pos2 = list_elements[min_index].getListElement().get_center() + DOWN
                
                arrow = CurvedDoubleArrow(pos1, pos2, angle=PI / 2, color=SORTCOL)
                swapText = Text("Swap!", color=SWAP_FONT_COLOR, font=FONT, font_size=SWAP_FONT_SIZE).next_to(arrow, DOWN)

                self.play(Create(arrow), run_time=0.3)
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
                self.play(FadeOut(arrow), FadeOut(swapText), run_time=0.2)

                values[i], values[min_index] = values[min_index], values[i]
            else:
                pos1 = list_elements[i].getListElement().get_center() + DOWN + (LEFT * 0.3)
                pos2 = list_elements[i].getListElement().get_center() + DOWN + (RIGHT * 0.3)
            
                arrow = CurvedDoubleArrow(pos1, pos2, angle=PI, color=SORTCOL)

                swapText = Text("Swap!", color=SWAP_FONT_COLOR, font=FONT, font_size=SWAP_FONT_SIZE).next_to(arrow, DOWN)

                self.play(Create(arrow), run_time=0.3)
                self.play(Write(swapText), run_time=0.4)
                self.wait(0.2)
                self.play(FadeOut(arrow), FadeOut(swapText), run_time=0.2)

            self.play(*(list_elements[i].MarkSorted()), run_time=0.2)
            self.wait(0.3)

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
            self.wait(0.2)
            return

        mid = (left + right) // 2

        # Highlight current subarray
        rect = SurroundingRectangle(VGroup(*[arr[i].getListElement() for i in range(left, right + 1)]), color=SORTCOL, buff=buff_adjust, corner_radius=0.3, stroke_width=0.5)
        self.play(Create(rect), run_time=0.3)

        self.recursive_merge_sort(arr, left, mid, buff_adjust-0.12)
        self.wait(0.1)
        self.recursive_merge_sort(arr, mid + 1, right, buff_adjust-0.12)
        self.wait(0.1)
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
                explanatoryText = Text(f"{left_vals[i]} <= {right_vals[j]}", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).shift(DOWN * 2.5)
                self.play(Write(explanatoryText), run_time=0.3)
                self.wait(0.6)
                self.play(FadeOut(explanatoryText), run_time=0.2)
                i += 1
            else:
                merged.append((right_group[j], right_vals[j]))
                explanatoryText = Text(f"{left_vals[i]} > {right_vals[j]}", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).shift(DOWN * 2.5)
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
        self.wait(1)
        self.quickSort(list_elements, 0, len(values) - 1, 0.35)
        self.wait(1)
    

    def quickSort(self, arr : list[ListElement], low : int, high : int, buff_adj : int):
        self.wait(0.3)
        if low < high:
            pi = self.partition(arr, low, high)

            if pi != low:
                surr = [arr[i].getListElement() for i in range(low, pi)]
            else:
                surr = [arr[low].getListElement()]
            rect = SurroundingRectangle(VGroup(*surr), color=SORTCOL, buff=buff_adj, corner_radius=0.3, stroke_width=0.5)
            self.play(Create(rect), run_time=0.3)
            self.quickSort(arr, low, pi - 1, buff_adj-0.12)
            self.play(FadeOut(rect), run_time=0.3)
            self.wait(0.2)
            if pi + 1 != high:
                surr = [arr[i].getListElement() for i in range(min(pi+1, high), high+1)]
            else:
                surr = [arr[pi + 1].getListElement()]
            rect = SurroundingRectangle(VGroup(*surr), color=SORTCOL, buff=buff_adj, corner_radius=0.3, stroke_width=0.5)
            self.play(Create(rect), run_time=0.3)
            self.quickSort(arr, pi + 1, high, buff_adj-0.12)
            self.play(FadeOut(rect), run_time=0.3)
           
        else:
            self.wait(0.4)
            self.play(*(arr[low].MarkSorted()), run_time=0.2)
            self.wait(0.4)

    def partition(self, arr : list[ListElement], low : int, high : int):
        def make_arrow(idx:int, label:str):
            arrow = Arrow(
                start=arr[idx].getListElement().get_center() + (UP * 2),
                end=arr[idx].getListElement().get_center() + UP,
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
                explanatoryText1 = Text(f"{array[j]} < {pivot} :", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE)
                explanatoryText2 = Text("i++ => Swap i and j", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE)
                explanatoryText = VGroup(explanatoryText1, explanatoryText2).arrange(DOWN, buff=0.3).shift(DOWN * 3)
                self.play(Write(explanatoryText), run_time=0.3)
                self.wait(0.6)
                self.play(FadeOut(explanatoryText), run_time=0.2)
                self.wait(0.2)

                i += 1
                if i == j:
                    self.play(j_group.animate.shift(RIGHT * 0.3), i_group.animate.move_to(arr[i].getListElement().get_center() + (UP * 1.7) + (LEFT * 0.3)), run_time=0.3)
                else:
                    self.play(i_group.animate.move_to(arr[i].getListElement().get_center() + (UP * 1.7)), run_time=0.3)
                
                self.swap(arr, i, j, "Swap")
                array[i], array[j] = array[j], array[i]
                self.wait(0.1)
            else:
                explanatoryText1 = Text(f"{array[j]} > {pivot} :", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE)
                explanatoryText2 = Text("No Swap", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE)
                explanatoryText = VGroup(explanatoryText1, explanatoryText2).arrange(DOWN, buff=0.3).shift(DOWN * 3)
                self.play(Write(explanatoryText), run_time=0.3)
                self.wait(0.6)
                self.play(FadeOut(explanatoryText), run_time=0.2)
                self.wait(0.3)
        
        self.play(FadeOut(j_group), run_time=0.2)

        explanatoryText = Text("Increment i", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).shift(DOWN * 3)
        self.play(Write(explanatoryText), run_time=0.3)
        self.wait(0.6)
        self.play(FadeOut(explanatoryText), run_time=0.2)
        self.wait(0.1)

        self.play(i_group.animate.move_to(arr[i + 1].getListElement().get_center() + (UP * 1.7)), run_time=0.3)
        self.swap(arr, i + 1, high, "Swap i with pivot")
        array[i + 1], array[high] = array[high], array[i + 1]
        self.wait(0.2)

        self.play(*(arr[i+1].MarkSorted()), run_time=0.2)
        self.wait(0.2)

        self.play(FadeOut(i_group), run_time=0.2)
        self.play(pivot_element.ClearSelection(), run_time=0.2)
        self.wait(0.3)

        return i + 1

    def swap(self, arr : list[ListElement], i : int, j : int, text_for_swap : str):
        if i != j:
            pos1 = arr[i].getListElement().get_center() + DOWN
            pos2 = arr[j].getListElement().get_center() + DOWN
            angle = PI/2
        else:
            pos1 = arr[i].getListElement().get_center() + DOWN + (LEFT * 0.3)
            pos2 = arr[i].getListElement().get_center() + DOWN + (RIGHT * 0.3)
            angle = PI
        
        arrow = CurvedDoubleArrow(pos1, pos2, angle=angle, color=SORTCOL)
        swapText = Text(text_for_swap, color=SWAP_FONT_COLOR, font=FONT, font_size=SWAP_FONT_SIZE).next_to(arrow, DOWN)

        self.play(Create(arrow), run_time=0.3)
        self.play(Write(swapText), run_time=0.4)

        self.play(
            arr[i].getListElement().animate.move_to(arr[j].getListElement().get_center()),
            arr[j].getListElement().animate.move_to(arr[i].getListElement().get_center()),
            run_time=0.3
        )

        self.wait(0.1)
        self.play(FadeOut(arrow), FadeOut(swapText), run_time=0.2)

        arr[i], arr[j] = arr[j], arr[i]


import networkx as nx

EDGE_COL = SELCOL
NODE_COL = BASECOL

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
    
    def SelectHighlight(self):
        return self.circle.animate.set_stroke(color=SELCOL, width=10)
    
    def Reset(self):
        return self.circle.animate.set_stroke(color=NODE_COL, width=0).set_fill(color=NODE_COL), self.text.animate.set_color(color=TEXTCOL)


class HeapSort(Scene):
    def construct(self):
        def max_heapify(A : list[int], size : int, k : int, buff=1.4):
            l = 2 * k + 1
            r = 2 * k + 2
            largest = k

            if l < size and A[l] > A[largest]:
                largest = l
            
            if r < size and A[r] > A[largest]:
                largest = r

            largestSurrL = DashedVMobject(SurroundingRectangle(list_elements[largest], color=TEXTCOL, buff=0, corner_radius=0.52))
            largestSurrT = DashedVMobject(SurroundingRectangle(tree.vertices[A[largest]], color=TEXTCOL, buff=0, corner_radius=0.52))    

            explanatory_text = Text(f"Largest Child of Node {A[k]} : {A[largest]}", font=FONT, color=EXPLANATORY_FONT_COLOR, font_size=30).to_edge(UP, buff=buff)
            self.play(Write(explanatory_text), Create(largestSurrL), Create(largestSurrT), run_time=0.3)
            self.wait(1.5)
            self.play(FadeOut(explanatory_text), Uncreate(largestSurrL), Uncreate(largestSurrT), run_time=0.2)
            self.wait(0.2)
            
            if largest != k:
                (A[k], A[largest]) = (A[largest], A[k])

                explanatory_text = Text(f"Swapping {A[k]} and {A[largest]}", font=FONT, color=EXPLANATORY_FONT_COLOR, font_size=30).to_edge(UP, buff=buff)
                self.play(Write(explanatory_text), run_time=0.3)
                self.wait(0.3)

                self.play(
                    list_elements[k].animate.move_to(list_elements[largest].get_center()),
                    list_elements[largest].animate.move_to(list_elements[k].get_center()),
                    tree.vertices[A[k]].animate.move_to(tree.vertices[A[largest]].get_center()),
                    tree.vertices[A[largest]].animate.move_to(tree.vertices[A[k]].get_center()),
                    run_time=0.6
                )
                list_elements[k], list_elements[largest] = list_elements[largest], list_elements[k]

                self.play(FadeOut(explanatory_text), run_time=0.2)
                self.wait(0.2)

                max_heapify(A,size,largest, buff)

            self.wait(0.2)

        def build_max_heap(A):
            operationText = Text("Building Max Heap", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.5)
            self.play(Write(operationText), run_time=0.5)
            self.wait(0.5)

            n = (len(A)//2)-1
            for i in range(n, -1, -1):
                lnode = list_elements[i]
                tnode = tree.vertices[A[i]]
                self.play(
                    lnode.Select(),
                    tnode.Select(),
                    run_time=0.3
                )

                self.wait(0.3)

                max_heapify(A,len(A),i)
                
                self.wait(0.1)
                self.play(
                    lnode.Clear(),
                    tnode.Clear(),
                    run_time=0.3
                )
                self.wait(0.3)

            self.wait(0.2)
            self.play(FadeOut(operationText), run_time=0.5)


        def heap_sort(A):
            build_max_heap(A)
            
            self.wait(0.5)

            operationText = Text("Performing Heap Sort", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(UP, buff=0.5)
            self.play(Write(operationText), run_time=0.5)
            self.wait(0.5)

            n = len(A)
            for i in range(n - 1, 0, -1):
                explanatory_text = Text(f"Swapping First and Largest Element\n              {A[0]} and {A[i]}", font=FONT, color=EXPLANATORY_FONT_COLOR, font_size=30).to_edge(UP, buff=1.4)
                self.play(Write(explanatory_text), run_time=0.3)
                self.wait(0.3)

                A[0], A[i] = A[i], A[0]

                self.play(
                    list_elements[0].animate.move_to(list_elements[i].get_center()),
                    list_elements[i].animate.move_to(list_elements[0].get_center()),
                    tree.vertices[A[0]].animate.move_to(tree.vertices[A[i]].get_center()),
                    tree.vertices[A[i]].animate.move_to(tree.vertices[A[0]].get_center()),
                    run_time=0.6
                )
                list_elements[0], list_elements[i] = list_elements[i], list_elements[0]

                self.wait(0.2)
                self.play(FadeOut(explanatory_text), run_time=0.2)
                self.play(
                    list_elements[i].Highlight(),
                    tree.vertices[A[i]].Highlight(),
                    run_time=0.3
                )
                self.wait(0.3)

                explanatory_text = Text(f"Building Max Heap on the Remaining Elements", font=FONT, color=EXPLANATORY_FONT_COLOR, font_size=30).to_edge(UP, buff=1.4)
                self.play(Write(explanatory_text), run_time=0.3)
                self.wait(0.2)

                max_heapify(A, i, 0, 2.2)

                self.wait(0.1)
                self.play(Unwrite(explanatory_text), run_time=0.2)

                self.wait(0.2)

            self.wait(0.2)

            self.play(
                list_elements[0].Highlight(),
                tree.vertices[A[0]].Highlight(),
                run_time=0.3
            )

            self.wait(0.2)
            self.play(FadeOut(operationText), run_time=0.5)

        values = [5, 2, 4, 6, 3, 1]
        list_elements = [Node(str(i)) for i in values]
        visuals = VGroup(*list_elements)

        edges = []

        for i in range(len(values)):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < len(values):
                edges.append((values[i], values[left]))
            if right < len(values):
                edges.append((values[i], values[right]))

        G = nx.Graph()
        G.add_nodes_from(values)
        G.add_edges_from(edges)

        tree = Graph(
            vertices=list(G.nodes), 
            edges=list(G.edges)[::-1], 
            vertex_mobjects={v : Node(v) for v in list(G.nodes)},
            edge_config={"stroke_color": EDGE_COL, "stroke_width": 6},
            layout="tree", 
            layout_scale=2,
            root_vertex=5    
        )

        tree.clear_updaters()


        visuals.arrange(RIGHT, buff=0.4)
        self.add(VGroup(visuals, tree).arrange(RIGHT, buff=1))
        self.wait(0.5)


        nodeSurr = DashedVMobject(SurroundingRectangle(visuals, color=TEXTCOL, buff=0.15, corner_radius=0.6), num_dashes=40)
        nodeText = Text("List", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, UP, buff=0.2)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)
        
        self.wait(1)

        nodeSurr = DashedVMobject(SurroundingRectangle(tree, color=TEXTCOL, buff=0.15, corner_radius=0.6), num_dashes=40)
        nodeText = Text("Tree Representation\n      of List", font=FONT, color=TEXTCOL, font_size=FSIZE).next_to(nodeSurr, UP, buff=0.2)
        self.play(Create(nodeSurr), run_time=0.5)
        self.wait(0.2)
        self.play(Write(nodeText), run_time=0.5)
        self.wait(1.5)
        self.play(Uncreate(nodeSurr), Unwrite(nodeText), run_time=0.5, lag_ratio=0.1)

        self.wait(0.5)

        heap_sort(values)

        self.wait(0.5)
        self.play(FadeOut(tree), run_time=0.5)
        self.wait(0.3)
        self.play(visuals.animate.center(), run_time=0.5)

        self.wait(1)