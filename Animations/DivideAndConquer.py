from manim import *
import random
from env_config import *
import numpy as np

# Override specific font sizes for DivideAndConquer
POINTER_FONT_SIZE = 28      # For "i", "j", "Min", etc. above arrows

class ListElement(VGroup):
    def __init__(self, value : str):
        super().__init__()
        self.size = 0.8
        self.value = value if value.isalpha() else int(value)
        self.isSorted = False
        self.elementValue = Text(value, font_size=(100*self.size), color=TEXTCOL, font=FONT)
        self.circle = Circle(radius=self.size, color=BASECOL, fill_opacity=1)
        self.elementValue.move_to(self.circle.get_center())
        self.add(self.circle, self.elementValue)

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


class CountInversions(Scene):
    def construct(self):
        # Create scrambled alphabet sequences
        top_alphabets = ['E', 'B', 'D', 'F', 'C', 'A']  # This defines the mapping: E=1, B=2, D=3, F=4, C=5, A=6
        bottom_alphabets = ['F', 'B', 'E', 'A', 'D', 'C']  # Different scrambled order: [4, 2, 1, 6, 3, 5]
        
        # Create alphabet visual elements
        top_elements = [ListElement(letter) for letter in top_alphabets]
        bottom_elements = [ListElement(letter) for letter in bottom_alphabets]
        
        # Arrange visuals
        top_visuals = VGroup(*top_elements).set_z_index(10)
        bottom_visuals = VGroup(*bottom_elements).set_z_index(10)
        
        top_visuals.arrange(RIGHT, buff=0.6).shift(UP * 1.5)
        bottom_visuals.arrange(RIGHT, buff=0.6).shift(DOWN * 1.5)
        
        # Add title
        title = Text("Alphabet to Number Mapping", font_size=50, color=TEXTCOL, font=FONT).to_edge(UP)
        self.add(title, top_visuals, bottom_visuals)
        self.wait(1)
        
        # Create mapping based on top visual
        alphabet_to_number = {letter: i + 1 for i, letter in enumerate(top_alphabets)}
        
        # Show mapping explanation
        mapping_text = Text("Top row defines the mapping:", font_size=35, color=TEXTCOL, font=FONT).shift(DOWN * 3.5)
        self.play(Write(mapping_text), run_time=1)
        
        # Show individual mappings
        mapping_lines = []
        for i, (letter, number) in enumerate(alphabet_to_number.items()):
            map_text = Text(f"{letter} → {number}", font_size=30, color=SORTCOL, font=FONT)
            map_text.shift(DOWN * 4.2 + RIGHT * (i - 2.5) * 1.5)
            mapping_lines.append(map_text)
            self.play(Write(map_text), run_time=0.3)
        
        self.wait(2)
        
        # Transform alphabets to numbers one by one
        transform_title = Text("Converting to Numbers", font_size=50, color=TEXTCOL, font=FONT).to_edge(UP)
        self.play(Transform(title, transform_title), run_time=0.5)
        
        # Transform both rows simultaneously, letter by letter
        unique_letters = list(set(top_alphabets + bottom_alphabets))  # Get all unique letters
        for letter in sorted(unique_letters):  # Process in alphabetical order
            number = alphabet_to_number[letter]
            
            # Find all positions of this letter in both rows
            top_positions = [i for i, l in enumerate(top_alphabets) if l == letter]
            bottom_positions = [i for i, l in enumerate(bottom_alphabets) if l == letter]
            
            # Create simultaneous transformations for all instances of this letter
            animations = []
            
            # Transform in top row
            for pos in top_positions:
                old_element = top_elements[pos]
                new_element = ListElement(str(number))
                new_element.move_to(old_element.get_center())
                animations.append(Transform(old_element, new_element))
            
            # Transform in bottom row
            for pos in bottom_positions:
                old_element = bottom_elements[pos]
                new_element = ListElement(str(number))
                new_element.move_to(old_element.get_center())
                animations.append(Transform(old_element, new_element))
            
            # Play all transformations for this letter simultaneously
            if animations:
                self.play(*animations, run_time=0.6)
                self.wait(0.2)
        
        self.wait(0.5)
        
        # Remove mapping explanation
        self.play(*[FadeOut(text) for text in mapping_lines], FadeOut(mapping_text), run_time=0.5)
        
        self.wait(0.5)
        
        # Fade out top visual and move bottom to center
        self.play(FadeOut(top_visuals), run_time=0.8)
        
        # Update title for inversion counting
        inversion_title = Text("Counting Inversions", font_size=50, color=TEXTCOL, font=FONT).to_edge(UP)
        self.inversion_counter = Text("Inversions: 0", font_size=40, color=SORTCOL, font=FONT).next_to(inversion_title, DOWN)
        
        self.play(Transform(title, inversion_title), Write(self.inversion_counter), run_time=0.8)
        self.title = title  # Keep reference for later use
        
        # Extract numerical values for inversion counting
        values = [alphabet_to_number[letter] for letter in bottom_alphabets]
        list_elements = bottom_elements  # Use the original transformed elements
        
        # Update the value attribute of each element to be the numeric value
        for i, element in enumerate(list_elements):
            element.value = values[i]
        
        self.total_inversions = 0
        self.wait(0.5)

        self.recursive_merge_sort(list_elements, 0, len(values) - 1, 0.55)

        self.wait(0.5)

        # Center the elements
        self.play(VGroup(*list_elements).animate.center())
        self.wait(1)

    def recursive_merge_sort(self, arr : list[ListElement], left : int, right : int, buff_adjust):
        if left >= right:
            self.wait(0.2)
            return 0

        mid = (left + right) // 2

        # Highlight current subarray
        rect = SurroundingRectangle(VGroup(*[arr[i] for i in range(left, right + 1)]), color=SORTCOL, buff=buff_adjust, corner_radius=0.3, stroke_width=0.5)
        self.play(Create(rect), run_time=0.3)

        left_inv = self.recursive_merge_sort(arr, left, mid, buff_adjust-0.12)
        self.wait(0.1)
        right_inv = self.recursive_merge_sort(arr, mid + 1, right, buff_adjust-0.12)
        self.wait(0.1)
        split_inv = self.merge(arr, left, mid, right)
        
        self.play(FadeOut(rect), run_time=0.2)
        
        return left_inv + right_inv + split_inv


    def merge(self, arr : list[ListElement], left:int, mid:int, right:int):
        target_positions = [arr[i].get_center() + (UP * 2.6) for i in range(left, right + 1)]
        left_group = arr[left:mid + 1]
        right_group = arr[mid + 1:right + 1]
        
        left_rect = SurroundingRectangle(VGroup(*[left_group[i] for i in range(len(left_group))]), color=SORTCOL, buff=0.14, corner_radius=0.3)
        right_rect = SurroundingRectangle(VGroup(*[right_group[i] for i in range(len(right_group))]), color=SORTCOL, buff=0.14, corner_radius=0.3)
        self.play(Create(left_rect), Create(right_rect), run_time=0.3)
        self.wait(0.2)

        left_vals = [int(el.value) for el in left_group]
        right_vals = [int(el.value) for el in right_group]

        merged : list[tuple[ListElement, int]] = []
        i = j = 0
        k = 0
        count = 0

        while i < len(left_vals) and j < len(right_vals):
            eli, elj = left_group[i], right_group[j]
            self.play(eli.SelectElement(), elj.SelectElement(), run_time=0.2)
            self.wait(0.2)
            if left_vals[i] <= right_vals[j]:
                merged.append((left_group[i], left_vals[i]))
                explanatoryText = Text(f"{left_vals[i]} <= {right_vals[j]}", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).to_edge(DOWN)
                self.play(Write(explanatoryText), run_time=0.3)
                self.wait(0.6)
                self.play(FadeOut(explanatoryText), run_time=0.2)
                i += 1
            else:
                # Count inversions: all remaining elements in left array form inversions with current right element
                inversions_count = len(left_vals) - i
                count += inversions_count
                self.total_inversions += inversions_count
                
                merged.append((right_group[j], right_vals[j]))
                explanatoryText = Text(f"{left_vals[i]} > {right_vals[j]} (+{inversions_count} inversions)", color=EXPLANATORY_FONT_COLOR, font=FONT, font_size=EXPLANATORY_FONT_SIZE).to_edge(DOWN)
                self.play(Write(explanatoryText), run_time=0.3)
                
                # Update counter
                new_counter = Text(f"Inversions: {self.total_inversions}", font_size=40, color=SORTCOL, font=FONT).next_to(self.title, DOWN)
                self.play(Transform(self.inversion_counter, new_counter), run_time=0.3)
                
                self.wait(0.6)
                self.play(FadeOut(explanatoryText), run_time=0.2)
                j += 1

            animations = []
            for index, (el, val) in enumerate(merged):
                animations.append(el.animate.move_to(target_positions[index]))
            self.play(*animations, run_time=1)

            self.play(eli.ClearSelection(), elj.ClearSelection(), run_time=0.2)


        while i < len(left_vals):
            self.play(left_group[i].SelectElement(), run_time=0.2)
            self.wait(0.2)
            merged.append((left_group[i], left_vals[i]))
            i += 1
        
            animations = []
            for index, (el, val) in enumerate(merged):
                animations.append(el.animate.move_to(target_positions[index]))
            self.play(*animations, run_time=1)

            self.play(left_group[i-1].ClearSelection(), run_time=0.2)


        while j < len(right_vals):
            self.play(right_group[j].SelectElement(), run_time=0.2)
            self.wait(0.2)
            merged.append((right_group[j], right_vals[j]))
            j += 1

            animations = []
            for index, (el, val) in enumerate(merged):
                animations.append(el.animate.move_to(target_positions[index]))
            self.play(*animations, run_time=1)

            self.play(right_group[j-1].ClearSelection(), run_time=0.2)


        self.play(FadeOut(left_rect), FadeOut(right_rect), run_time=0.2)
        self.wait(0.2)

        animations = []
        for index, (el, val) in enumerate(merged):
            animations.append(el.animate.shift(DOWN * 2.6))
        self.play(*animations, run_time=1)


        # Update the array reference to new order
        for i, (el, val) in enumerate(merged):
            arr[left + i] = el
            
        return count
    

from math import sqrt, pow
class ClosestPairPoint(Scene):
    # Returns eucledian disatnce between points p and q
    def distance(self, p, q):
        return sqrt(pow(p[0] - q[0],2) + pow(p[1] - q[1],2))

    def minDistanceRec(self, Px: list[tuple[float, float]], Py: list[tuple[float, float]], depth: int = 0):
        s = len(Px)
        # Given number of points cannot be less than 2.
        # If only 2 or 3 points are left return the minimum distance accordingly.
        if (s == 2):
            base_text = Text("Base case: 2 points", font_size=35, color=EXPLANATORY_FONT_COLOR, font=FONT)
            base_text.to_edge(UP, buff=0.5)
            dist_line = Line((Px[0][0], Px[0][1], 0), (Px[1][0], Px[1][1], 0), color=SORTCOL, stroke_width=3)
            distance_val = self.distance(Px[0], Px[1])
            dist_text = Text(f"Distance: {distance_val:.2f}", font_size=32, color=SORTCOL, font=FONT)
            dist_text.next_to(base_text, DOWN, buff=0.1)
            
            self.play(FadeIn(dist_line), Write(base_text), Write(dist_text), run_time=0.5)
            self.wait(0.5)
            
            # Update current best if this is the first or better
            if self.current_best is None or distance_val < self.current_best[2]:
                if self.current_best is not None:
                    # Remove old highlighting
                    self.play(
                        self.dot_to_mob[self.current_best[0]].animate.set_fill(TEXTCOL),
                        self.dot_to_mob[self.current_best[1]].animate.set_fill(TEXTCOL),
                        run_time=0.3
                    )
                self.current_best = (Px[0], Px[1], distance_val)
                # Highlight new best
                self.play(
                    self.dot_to_mob[Px[0]].animate.set_fill(PINK),
                    self.dot_to_mob[Px[1]].animate.set_fill(PINK),
                    run_time=0.3
                )
            
            self.play(FadeOut(dist_line), FadeOut(base_text), FadeOut(dist_text), run_time=0.3)
            return distance_val
        elif (s == 3):
            base_text = Text("Base case: 3 points", font_size=35, color=EXPLANATORY_FONT_COLOR, font=FONT)
            base_text.to_edge(UP, buff=0.5)
            dist_lines = [
                Line((Px[0][0], Px[0][1], 0), (Px[1][0], Px[1][1], 0), color=SORTCOL, stroke_width=3),
                Line((Px[1][0], Px[1][1], 0), (Px[2][0], Px[2][1], 0), color=SORTCOL, stroke_width=3),
                Line((Px[2][0], Px[2][1], 0), (Px[0][0], Px[0][1], 0), color=SORTCOL, stroke_width=3)
            ]
            
            # Find minimum distance and corresponding pair
            distances = [
                (self.distance(Px[0], Px[1]), Px[0], Px[1]),
                (self.distance(Px[1], Px[2]), Px[1], Px[2]),
                (self.distance(Px[2], Px[0]), Px[2], Px[0])
            ]
            min_dist, p1, p2 = min(distances)
            
            dist_text = Text(f"Min Distance: {min_dist:.2f}", font_size=32, color=SORTCOL, font=FONT)
            dist_text.next_to(base_text, DOWN, buff=0.1)
            
            self.play(*[FadeIn(line) for line in dist_lines], Write(base_text), Write(dist_text), run_time=0.5)
            self.wait(0.5)
            
            # Update current best if this is the first or better
            if self.current_best is None or min_dist < self.current_best[2]:
                if self.current_best is not None:
                    # Remove old highlighting
                    self.play(
                        self.dot_to_mob[self.current_best[0]].animate.set_fill(TEXTCOL),
                        self.dot_to_mob[self.current_best[1]].animate.set_fill(TEXTCOL),
                        run_time=0.3
                    )
                self.current_best = (p1, p2, min_dist)
                # Highlight new best
                self.play(
                    self.dot_to_mob[p1].animate.set_fill(PINK),
                    self.dot_to_mob[p2].animate.set_fill(PINK),
                    run_time=0.3
                )
            
            self.play(*[FadeOut(line) for line in dist_lines], FadeOut(base_text), FadeOut(dist_text), run_time=0.3)
            return min_dist

        # For more than 3 points divide the points by point around median of x coordinates
        m = s//2
        Qx = Px[:m]
        Rx = Px[m:]
        xQ = Qx[-1][0]  # maximum x value in Qx
        xR = Rx[0][0]    # minimum x value in Rx
        
        # Construct Qy and Ry in O(n) rather from Py
        Qy: list[tuple[float, float]] = []
        Ry: list[tuple[float, float]] = []
        for p in Py:
            if(p[0] < xR):
                Qy.append(p)
            else:
                Ry.append(p)

        line_x = (xR + xQ)/2
        split_line = DashedVMobject(Line((line_x, 2.5, 0), (line_x, -4, 0), color=RED, stroke_width=3))
        
        # Add explanation for divide step
        divide_text = Text("Dividing points by median x-coordinate", font_size=35, color=EXPLANATORY_FONT_COLOR, font=FONT)
        divide_text.to_edge(UP, buff=0.5)
        self.play(Create(split_line), Write(divide_text), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(divide_text), run_time=0.3)

        # Extract Sy using delta
        # Calculate opacity reduction based on depth (more reduction at deeper levels)
        opacity_factor = 0.1 + (depth * 0.2)  # Starts at 0.1, increases with depth

        # Decrease opacity of points not in left call (Qx, Qy)
        points_to_dim = [self.dot_to_mob[pt] for pt in Px if pt not in Qx]
        if points_to_dim:
            left_text = Text("Processing left half", font_size=35, color=EXPLANATORY_FONT_COLOR, font=FONT)
            left_text.to_edge(UP, buff=0.5)
            self.play(*[dot.animate.set_opacity(max(0.05, dot.fill_opacity * opacity_factor)) for dot in points_to_dim], 
                     Write(left_text), run_time=0.5)
            self.wait(0.3)
            self.play(FadeOut(left_text), run_time=0.2)
        
        left = self.minDistanceRec(Qx, Qy, depth + 1)
        
        # Restore opacity of dimmed points
        if points_to_dim:
            fade_in = AnimationGroup(*[dot.animate.set_opacity(min(1.0, dot.fill_opacity / opacity_factor)) for dot in points_to_dim])
        
        # Decrease opacity of points not in right call (Rx, Ry)
        points_to_dim_right = [self.dot_to_mob[pt] for pt in Px if pt not in Rx]
        if points_to_dim_right:
            fade_out = AnimationGroup(*[dot.animate.set_opacity(max(0.05, dot.fill_opacity * opacity_factor)) for dot in points_to_dim_right])
            right_text = Text("Processing right half", font_size=35, color=EXPLANATORY_FONT_COLOR, font=FONT)
            right_text.to_edge(UP, buff=0.5)

        self.play(fade_in, fade_out, Write(right_text) if points_to_dim_right else fade_in, run_time=0.5)
        if points_to_dim_right:
            self.wait(0.3)
            self.play(FadeOut(right_text), run_time=0.2)
        right = self.minDistanceRec(Rx, Ry, depth + 1)
        
        # Restore opacity of dimmed points
        if points_to_dim_right:
            self.play(*[dot.animate.set_opacity(min(1.0, dot.fill_opacity / opacity_factor)) for dot in points_to_dim_right], run_time=0.5)
        
        # Show comparison of left and right results
        # Determine which half had the better result
        if left <= right:
            comparison_text = Text(f"Left half wins: {left:.2f} ≤ {right:.2f}", font_size=30, color=EXPLANATORY_FONT_COLOR, font=FONT)
        else:
            comparison_text = Text(f"Right half wins: {left:.2f} > {right:.2f}", font_size=30, color=EXPLANATORY_FONT_COLOR, font=FONT)
        
        comparison_text.to_edge(UP, buff=0.5)
        self.play(Write(comparison_text), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(comparison_text), run_time=0.3)
        

        delta = min(left, right)
        # Create delta strip as a rectangle instead of two lines
        delta_rect = Rectangle(
            width=2*delta, 
            height=6.5,  # From y=2.5 to y=-4
            color=GREEN, 
            fill_color=GREEN, 
            fill_opacity=0.15,
            stroke_width=0,
            # grid_xstep=delta/2, 
            # grid_ystep=delta/2,
        )
        delta_rect.move_to([line_x, -0.75, 0])  # Center between y=2.5 and y=-4
        # delta_rect.grid_lines.set_stroke(width=1)

        # Add explanation for strip checking
        strip_text = Text(f"Checking strip within δ = {delta:.2f} of dividing line", font_size=35, color=EXPLANATORY_FONT_COLOR, font=FONT)
        strip_text.to_edge(UP, buff=0.5)
        self.play(FadeIn(delta_rect), Write(strip_text), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(strip_text), run_time=0.3)

        Sy: list[tuple[float, float]] = []
        for p in Py:
            if abs(p[0] - line_x) <= delta:
                Sy.append(p)

        sizeS = len(Sy)
        if sizeS > 1:
            sy_points_to_dim = [self.dot_to_mob[pt] for pt in Sy]
            
            # Add explanation for strip points
            strip_points_text = Text(f"Found {sizeS} points in strip - checking distances", font_size=35, color=EXPLANATORY_FONT_COLOR, font=FONT)
            strip_points_text.to_edge(UP, buff=0.5)
            self.play(*[dot.animate.set_fill(BLUE) for dot in sy_points_to_dim], Write(strip_points_text), run_time=0.5)
            self.wait(0.8)
            self.play(FadeOut(strip_points_text), run_time=0.3)
            
            minS = self.distance(Sy[0], Sy[1])
            
            for i in range(1, sizeS-1):
                for j in range(i, min(i+15, sizeS-1)):
                    sy_dist_line = Line((Sy[i][0], Sy[i][1], 0), (Sy[j+1][0], Sy[j+1][1], 0), color=SORTCOL, stroke_width=3)
                    
                    # Add distance comparison text
                    dist_value = self.distance(Sy[i], Sy[j+1])
                    comparison_text = Text(f"Distance: {dist_value:.2f}", font_size=32, color=EXPLANATORY_FONT_COLOR, font=FONT)
                    comparison_text.to_edge(UP, buff=0.5)
                    
                    self.play(FadeIn(sy_dist_line), Write(comparison_text), run_time=0.3)
                    
                    # Check if this is a new best
                    if dist_value < minS:
                        minS = dist_value
                        # Update global current best if this is better
                        if self.current_best is None or dist_value < self.current_best[2]:
                            if self.current_best is not None:
                                # Remove old highlighting
                                self.play(
                                    self.dot_to_mob[self.current_best[0]].animate.set_fill(TEXTCOL),
                                    self.dot_to_mob[self.current_best[1]].animate.set_fill(TEXTCOL),
                                    run_time=0.3
                                )
                            self.current_best = (Sy[i], Sy[j+1], dist_value)
                            # Highlight new best
                            self.play(
                                self.dot_to_mob[Sy[i]].animate.set_fill(PINK),
                                self.dot_to_mob[Sy[j+1]].animate.set_fill(PINK),
                                run_time=0.3
                            )
                    
                    self.wait(0.2)
                    self.play(FadeOut(sy_dist_line), FadeOut(comparison_text), run_time=0.2)

            # Clean up strip highlighting (but keep current best highlighted)
            non_best_dots = []
            for dot in sy_points_to_dim:
                point = next((pt for pt, mob in self.dot_to_mob.items() if mob == dot), None)
                if self.current_best is None or (point != self.current_best[0] and point != self.current_best[1]):
                    non_best_dots.append(dot)
            
            if non_best_dots:
                self.play(*[dot.animate.set_fill(TEXTCOL) for dot in non_best_dots], run_time=0.5)
            
            self.play(FadeOut(split_line), FadeOut(delta_rect), run_time=0.2)
            return min(delta, minS)
        else:
            self.play(FadeOut(split_line), FadeOut(delta_rect), run_time=0.2)
            return delta


    def minDistance(self, Points: list[tuple[float, float]]):
        Px = sorted(Points)
        Py = Points
        Py.sort(key=lambda x: x[-1])
        #print(Px,Py)
        return round(self.minDistanceRec(Px, Py), 2)


    def construct(self):
        # Initialize current best tracking
        self.current_best = None
        
        # Generate 25 random points within x: [-8,8], y: [-4.5,4.5] using a fixed seed
        random.seed(31)
        pts = [(random.uniform(-7, 7), random.uniform(-3.2, 2)) for _ in range(35)]
        dots = [Dot(point=(x, y, 0), color=TEXTCOL, radius=0.1).set_z_index(2) for x, y in pts]
        self.dot_to_mob = {pt: dot for pt, dot in zip(pts, dots)}
        self.add(*dots)
        
        result = self.minDistance(pts)
        
        # Final result text
        final_text = Text(f"Closest Distance: {result}", font_size=45, color=SORTCOL, font=FONT)
        final_text.to_edge(UP, buff=0.3)
        self.play(Write(final_text), run_time=1)
        self.wait(2)


class LongestCommonSubsequence(Scene):
    def construct(self):
        u, v = "bisect", "secret"
        self.m, self.n = len(u), len(v)

        self.lcs = np.zeros((self.m + 1, self.n + 1), dtype=int)

        table_for_Table = np.hstack((np.array(list(range(self.n + 1))).reshape(-1, 1), self.lcs))
        table_for_Table = np.vstack((np.array([0] + list(range(self.m + 1))).reshape(1, -1), table_for_Table))

        # print(table_for_Table)
        self.lcs_table = IntegerTable(
            table_for_Table,
            row_labels=[Text(str(x), font=FONT, color=TEXTCOL, font_size=FSIZE) for x in [" "] + list(u) + [" "]],
            col_labels=[Text(str(x), font=FONT, color=TEXTCOL, font_size=FSIZE) for x in [" "] + list(v) + [" "]],
            include_outer_lines=True,
            v_buff=0.5,
            h_buff=0.7,
        ).to_edge(LEFT, buff=0.6)

        self.lcs_table.get_entries().set_color(WHITE)

        for i in range(2, self.m + 3):
            self.lcs_table.get_entries_without_labels((0, i)).set_color(TEXTCOL)
            self.lcs_table.get_entries_without_labels((1, i)).set_color(TEXTCOL)
            self.lcs_table.add_to_back(self.lcs_table.get_highlighted_cell((1, i + 1), color=SELCOL, fill_opacity=0.2))
            self.lcs_table.add_to_back(self.lcs_table.get_highlighted_cell((2, i + 1), color=SELCOL, fill_opacity=0.2))

        for j in range(2, self.n + 3):
            self.lcs_table.get_entries_without_labels((j, 0)).set_color(TEXTCOL)
            self.lcs_table.get_entries_without_labels((j, 1)).set_color(TEXTCOL)
            self.lcs_table.add_to_back(self.lcs_table.get_highlighted_cell((j + 1, 1), color=SELCOL, fill_opacity=0.2))
            self.lcs_table.add_to_back(self.lcs_table.get_highlighted_cell((j + 1, 2), color=SELCOL, fill_opacity=0.2))

        self.lcs_table.get_labels().set_color(TEXTCOL)
        self.lcs_table.get_entries_without_labels((1, 1)).set_color(WHITE)

        for line in self.lcs_table.get_horizontal_lines() + self.lcs_table.get_vertical_lines():
            line.set_stroke(color=EDGE_COL, width=3.5)

        self.add(self.lcs_table)

        lcs_ans, path_cells = self.LCS(u, v)

        path = VGroup()
        for i in range(len(path_cells) - 1):
            path.add(
                Line(
                    start=self.lcs_table.get_cell((path_cells[i])).get_center(),
                    end=self.lcs_table.get_cell((path_cells[i + 1])).get_center(),
                    color=SORTCOL,
                    stroke_width=DEGREE_FONT_SIZE,
                    stroke_opacity=0.3,
                )
            )

        self.wait(1)
        self.play(
            Create(path),
            run_time=1,
        )
        self.wait(0.2)

        # Highlight the LCS characters in the table
        self.highlight_lcs_characters(u, v, path_cells)

        # Calculate the actual LCS string
        lcs_string = ""
        i, j = self.m, self.n
        while i > 0 and j > 0:
            if u[i-1] == v[j-1]:
                lcs_string = u[i-1] + lcs_string
                i -= 1
                j -= 1
            elif self.lcs[i-1][j] > self.lcs[i][j-1]:
                i -= 1
            else:
                j -= 1

        # Add final result heading and LCS text
        result_heading = Text("Result:", font_size=40, color=TEXTCOL, font=FONT)
        result_heading.to_edge(RIGHT, buff=2.5).shift(UP * 1)
        
        lcs_result_text = Text(f"LCS: \"{lcs_string}\" (Length: {lcs_ans})", font_size=28, color=TEXTCOL, font=FONT)
        lcs_result_text.next_to(result_heading, DOWN, buff=0.5)
        
        self.play(Write(result_heading), run_time=0.5)
        self.play(Write(lcs_result_text), run_time=0.5)

        self.wait(1)


    def LCS(self, X: str, Y: str) -> tuple[int, list[tuple[int, int]]]:
        path_cells = []
        
        # First, fill the DP table
        for i in range(self.n-1, -1, -1):
            for j in range(self.m-1, -1, -1):
                # Show current cell info
                cell_info = Text(f"Processing cell ({j+1}, {i+1})", font_size=28, color=EXPLANATORY_FONT_COLOR, font=FONT)
                cell_info.to_edge(RIGHT, buff=1).shift(UP * 1)
                self.play(Write(cell_info), run_time=0.3)
                
                char_highlight_h = self.lcs_table.get_highlighted_cell((1, i + 3), color=SELCOL, fill_opacity=0.3)
                index_highlight_h = self.lcs_table.get_highlighted_cell((2, i + 3), color=SELCOL, fill_opacity=0.3)
                char_highlight_v = self.lcs_table.get_highlighted_cell((j + 3, 1), color=SELCOL, fill_opacity=0.3)
                index_highlight_v = self.lcs_table.get_highlighted_cell((j + 3, 2), color=SELCOL, fill_opacity=0.3)
                current_highlight = self.lcs_table.get_cell((j + 3, i + 3), color=TEXTCOL) 

                self.lcs_table.add_to_back(char_highlight_h, index_highlight_h, char_highlight_v, index_highlight_v),
                self.lcs_table.add(current_highlight)

                self.wait(0.2)

                if X[j] == Y[i]:
                    # Show comparison text for match
                    comparison_text = Text(f"'{X[j]}' == '{Y[i]}' ✓", font_size=32, color=GREEN_C, font=FONT)
                    comparison_text.next_to(cell_info, DOWN, buff=0.5)
                    self.play(Write(comparison_text), run_time=0.3)
                    
                    arrow = Arrow(
                        start=self.lcs_table.get_entries((j + 4, i + 4)).get_center(),
                        end=self.lcs_table.get_entries((j + 3, i + 3)).get_center(),
                        color=SORTCOL,
                        stroke_width=POINTER_FONT_SIZE,
                    )
                    self.play(Create(arrow), run_time=0.2)
                    self.lcs[j][i] = self.lcs[j + 1][i + 1] + 1
                    
                    # Show the calculation - split into two lines
                    calc_line1 = Text(f"LCS[{j}][{i}] = LCS[{j+1}][{i+1}] + 1", 
                                   font_size=24, color=EXPLANATORY_FONT_COLOR, font=FONT)
                    calc_line2 = Text(f"= {self.lcs[j+1][i+1]} + 1 = {self.lcs[j][i]}", 
                                   font_size=24, color=EXPLANATORY_FONT_COLOR, font=FONT)
                    calc_line1.next_to(comparison_text, DOWN, buff=0.3)
                    calc_line2.next_to(calc_line1, DOWN, buff=0.2)
                    self.play(Write(calc_line1), run_time=0.3)
                    self.play(Write(calc_line2), run_time=0.3)
                    self.wait(0.4)
                    
                else:
                    # Show comparison text for mismatch
                    comparison_text = Text(f"'{X[j]}' != '{Y[i]}' ✗", font_size=32, color=RED_C, font=FONT)
                    comparison_text.next_to(cell_info, DOWN, buff=0.5)
                    self.play(Write(comparison_text), run_time=0.3)
                    
                    if self.lcs[j + 1][i] >= self.lcs[j][i + 1]:
                        arrow = Arrow(
                            start=self.lcs_table.get_entries((j + 4, i + 3)).get_center(),
                            end=self.lcs_table.get_entries((j + 3, i + 3)).get_center(),
                            color=SORTCOL,
                            stroke_width=POINTER_FONT_SIZE,
                        )
                    else:
                        arrow = Arrow(
                            start=self.lcs_table.get_entries((j + 3, i + 4)).get_center(),
                            end=self.lcs_table.get_entries((j + 3, i + 3)).get_center(),
                            color=SORTCOL,
                            stroke_width=POINTER_FONT_SIZE,
                        )
                        
                    self.play(Create(arrow), run_time=0.2)
                    self.lcs[j][i] = max(self.lcs[j + 1][i], self.lcs[j][i + 1])
                    
                    # Show the calculation
                    calc_text = Text(f"LCS[{j}][{i}] = max({self.lcs[j+1][i]}, {self.lcs[j][i+1]}) = {self.lcs[j][i]}", 
                                   font_size=24, color=EXPLANATORY_FONT_COLOR, font=FONT)
                    calc_text.next_to(comparison_text, DOWN, buff=0.3)
                    self.play(Write(calc_text), run_time=0.4)
                    self.wait(0.4)
                
                # Update the table value
                self.play(self.lcs_table.get_entries_without_labels((j + 2, i + 2)).animate.become(
                    Integer(self.lcs[j][i], font_size=FSIZE + 8).set_color(TEXTCOL).move_to(self.lcs_table.get_entries_without_labels((j + 2, i + 2)).get_center())
                    ),
                    run_time=0.3
                )
                
                # Clean up - unwrite all the text and remove highlights
                if X[j] == Y[i]:
                    # For diagonal case, we have two calculation lines
                    self.play(
                        FadeOut(arrow),
                        Unwrite(cell_info),
                        Unwrite(comparison_text),
                        Unwrite(calc_line1),
                        Unwrite(calc_line2),
                        run_time=0.3
                    )
                else:
                    # For max case, we have one calculation line
                    self.play(
                        FadeOut(arrow),
                        Unwrite(cell_info),
                        Unwrite(comparison_text),
                        Unwrite(calc_text),
                        run_time=0.3
                    )
                self.lcs_table.remove(current_highlight, char_highlight_h, index_highlight_h, char_highlight_v, index_highlight_v)
                self.wait(0.1)

        # Now backtrack to find the actual LCS path
        i, j = self.m, self.n
        path_cells.append((i + 3, j + 3))  # Start from bottom-right corner (row, col format)
        
        while i > 0 and j > 0:
            if X[i-1] == Y[j-1]:
                # Characters match - came from diagonal
                i -= 1
                j -= 1
                path_cells.append((i + 3, j + 3))
            elif self.lcs[i-1][j] > self.lcs[i][j-1]:
                # Came from above (move up in table)
                i -= 1
                path_cells.append((i + 3, j + 3))
            else:
                # Came from left (move left in table)
                j -= 1
                path_cells.append((i + 3, j + 3))
        
        # Add remaining path to (0,0)
        while i > 0:
            i -= 1
            path_cells.append((i + 3, j + 3))
        while j > 0:
            j -= 1
            path_cells.append((i + 3, j + 3))

        return self.lcs[0][0], path_cells
    
    def highlight_lcs_characters(self, X: str, Y: str, path_cells: list):
        """Highlight the LCS characters in the row and column headers"""
        # First, find the LCS sequence by following the path
        lcs_chars = []
        lcs_x_indices = []
        lcs_y_indices = []
        
        # Go through path_cells in reverse (from start to end of path)
        for k in range(len(path_cells) - 1, 0, -1):
            curr_cell = path_cells[k]
            prev_cell = path_cells[k-1]
            
            curr_i, curr_j = curr_cell[0] - 3, curr_cell[1] - 3
            prev_i, prev_j = prev_cell[0] - 3, prev_cell[1] - 3
            
            # Check if this was a diagonal move (character match)
            if prev_i == curr_i + 1 and prev_j == curr_j + 1:
                if curr_i >= 0 and curr_j >= 0 and curr_i < self.m and curr_j < self.n:
                    lcs_chars.append(X[curr_i])
                    lcs_x_indices.append(curr_i)
                    lcs_y_indices.append(curr_j)
        
        # Highlight the LCS characters in X and Y simultaneously
        highlight_animations = []
        char_cells = []
        
        for i, (x_idx, y_idx) in enumerate(zip(lcs_x_indices, lcs_y_indices)):
            # Create highlight for X (row header)
            x_char_cell = self.lcs_table.get_highlighted_cell((x_idx + 3, 1), color=SORTCOL, fill_opacity=0.5)
            self.lcs_table.add_to_back(x_char_cell)
            
            # Create highlight for Y (column header) 
            y_char_cell = self.lcs_table.get_highlighted_cell((1, y_idx + 3), color=SORTCOL, fill_opacity=0.5)
            self.lcs_table.add_to_back(y_char_cell)
            
            char_cells.extend([x_char_cell, y_char_cell])
            
            # Animate both highlights simultaneously
            self.play(FadeIn(x_char_cell), FadeIn(y_char_cell), run_time=0.5)
            self.wait(0.2)
        