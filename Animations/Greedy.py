import random

import networkx as nx
from common import WeightedLine
from env_config import *
from manim import *

random.seed(32)


class IntervalScheduling(Scene):
    def intervalschedule(self, L, intervals):
        sortedL = sorted(L, key=lambda x: x[2])
        accepted = [0]
        # Explanatory text: First interval always accepted
        first_text = Text(f"Processing interval {sortedL[0][0]}: Always accept first interval", font=FONT, font_size=EXPLANATORY_FONT_SIZE-4, color=TEXTCOL).to_edge(UP, buff=0.2)
        self.play(Write(first_text), run_time=0.7)
        self.play(
            intervals[0][0].animate.set_fill(color=SELCOL),
            intervals[0][1].animate.set_color(BASECOL),
        )
        self.wait(0.5)
        self.play(FadeOut(first_text), run_time=0.5)
        for idx, (i, s, f) in enumerate(sortedL[1:], 1):
            # Explanatory text: Processing interval
            proc_text = Text(f"Processing interval {i}", font=FONT, font_size=EXPLANATORY_FONT_SIZE-4, color=TEXTCOL).to_edge(UP, buff=0.2)
            self.play(Write(proc_text), run_time=0.5)
            self.play(
                intervals[idx][0].animate.set_stroke(color=SORTCOL, width=2)
            )
            # Overlap check
            if s >= sortedL[accepted[-1]][2]:
                overlap_text = Text(f"No overlap with last accepted ({sortedL[accepted[-1]][0]})", font=FONT, font_size=EXPLANATORY_FONT_SIZE-10, color=BLACK).next_to(proc_text, DOWN, 0.3)
                self.play(Write(overlap_text), run_time=0.4)
                accepted.append(idx)
                self.play(
                    intervals[idx][0].animate.set_fill(color=SELCOL),
                    intervals[idx][1].animate.set_color(BASECOL),
                )
                self.wait(0.3)
                self.play(FadeOut(overlap_text), run_time=0.3)
            else:
                overlap_text = Text(f"Overlaps with last accepted ({sortedL[accepted[-1]][0]})", font=FONT, font_size=EXPLANATORY_FONT_SIZE-10, color=BLACK).next_to(proc_text, DOWN, 0.3)
                self.play(Write(overlap_text), run_time=0.4)
                self.play(
                    Indicate(intervals[accepted[-1]], color=SORTCOL, scale_factor=1.1)
                )
                self.wait(0.3)
                self.play(FadeOut(overlap_text), run_time=0.3)
            self.play(FadeOut(proc_text), run_time=0.3)
            self.play(
                intervals[idx][0].animate.set_stroke(color=SORTCOL, width=0)
            )
        return accepted
    
    def construct(self):
        L = [(0, 1, 2),(1, 3, 6),(2, 1, 5),(3, 4, 7),(4, 2, 5),(5, 5, 8),(6, 7, 10),(7, 10, 13),(8, 9, 12)]
        intervals = VGroup()
        for i, s, f in L:
            interval = RoundedRectangle(corner_radius=0.2, width=f-s, height=0.7, fill_color=NODE_COL, fill_opacity=1, stroke_width=0)
            index = Text(str(i), font=FONT, font_size=INTERVAL_FSIZE, color=TEXTCOL)
            index.move_to(interval.get_center())
            interval_visual = VGroup(interval, index)
            interval_visual.to_corner(UL)
            interval_visual.shift(DOWN * (i * 0.7))
            interval_visual.shift(RIGHT * s)
            intervals.add(interval_visual)

        intervals.set_z_index(2)
        intervals.shift(DOWN * 1.6)
        self.add(intervals)

        interval_time = VGroup()

        for i in range(13):
            line = Line(start=(ORIGIN + UP * 3.4) + (RIGHT * i), end=(ORIGIN + DOWN * 3.5) + (RIGHT * i), color=TEXTCOL, stroke_width=1)
            time = Text(str(i), font=FONT, font_size=20, color=TEXTCOL).shift(UP * 3.6 + RIGHT * i)
            interval_time.add(VGroup(line, time))

        interval_time.to_edge(LEFT)
        interval_time.shift(RIGHT * 0.94)
        interval_time.shift(DOWN * 0.8)
        self.add(interval_time)

        L_sorted = sorted(L, key=lambda x: x[2])
        intervals_sorted = VGroup()
        for c, (i, s, f) in enumerate(L_sorted):
            interval = RoundedRectangle(corner_radius=0.2, width=f-s, height=0.7, fill_color=NODE_COL, fill_opacity=1, stroke_width=0)
            index = Text(str(i), font=FONT, font_size=INTERVAL_FSIZE, color=TEXTCOL)
            index.move_to(interval.get_center())
            interval_visual = VGroup(interval, index)
            interval_visual.to_corner(UL)
            interval_visual.shift(DOWN * (c * 0.7))
            interval_visual.shift(RIGHT * s)
            intervals_sorted.add(interval_visual)

        intervals_sorted.set_z_index(2)
        intervals_sorted.shift(DOWN * 1.6)
        
        # Explanatory text: Sorting
        sort_text = Text("Sort intervals by finish time", font=FONT, font_size=EXPLANATORY_FONT_SIZE, color=TEXTCOL).to_edge(UP, buff=0.2)
        self.play(Write(sort_text), run_time=0.8)
        self.wait(0.7)
        self.play(intervals.animate.become(intervals_sorted))
        self.play(FadeOut(sort_text), run_time=0.5)
        self.wait(1)
        accepted_indices = self.intervalschedule(L, intervals)
        self.wait(1)
        
        # Fade out non-accepted intervals
        non_accepted_intervals = []
        for i in range(len(intervals)):
            if i not in accepted_indices:
                non_accepted_intervals.append(intervals[i])
        
        if non_accepted_intervals:
            self.play(
                *[FadeOut(interval) for interval in non_accepted_intervals]
            )
        self.wait(1)
        
        # Shift accepted intervals to center on y-axis
        accepted_intervals = [intervals[i] for i in accepted_indices]
        self.play(
            *[interval.animate.shift(UP * (0 - interval.get_center()[1])) for interval in accepted_intervals]
        )
        self.wait(1)
        

class Node:
    def __init__(self, frequency: int, symbol: str | None = None, left: 'Node' = None, right: 'Node' = None):
        self.frequency = frequency
        self.symbol = symbol
        self.left = left
        self.right = right

class HuffmanNode(VGroup):
    def __init__(self, symbol: str, frequency: int):
        super().__init__()
        self.circle = Circle(radius=0.5, color=NODE_COL, fill_color=NODE_COL, fill_opacity=1, stroke_width=0)
        
        # Create text for frequency (larger, on top)
        self.freq_text = Text(str(frequency), font=FONT, color=TEXTCOL, font_size=30)
        
        # Create text for symbol (smaller, below frequency)
        if symbol and len(symbol) == 1:  # Single character
            self.symbol_text = Text(symbol, font=FONT, color=TEXTCOL, font_size=24)
        else:  # Internal node or multi-character symbol
            self.symbol_text = Text("", font=FONT, color=TEXTCOL, font_size=24)
        
        # Position texts within circle
        if symbol and len(symbol) == 1:
            self.freq_text.move_to(self.circle.get_center() + UP * 0.15)
            self.symbol_text.move_to(self.circle.get_center() + DOWN * 0.2)
        else:
            self.freq_text.move_to(self.circle.get_center())
        
        # Add all elements to the VGroup
        self.add(self.circle, self.freq_text)
        if symbol and len(symbol) == 1:
            self.add(self.symbol_text)

    def Select(self):
        return self.circle.animate.set_stroke(color=SORTCOL, width=10)
    
    def Clear(self):
        return self.circle.animate.set_stroke(color=NODE_COL, width=0)
        
    def Highlight(self):
        return self.circle.animate.set_fill(color=SELCOL)
    
    def SelectHighlight(self):
        return self.circle.animate.set_stroke(color=SELCOL, width=10)
    
    def Reset(self):
        return self.circle.animate.set_fill(color=NODE_COL).set_stroke(color=NODE_COL, width=0)

class HuffmanEncoding(Scene):
    def huffman_steps(self, s):
        """Compute the Huffman merge sequence once: the single source of truth
        consumed by both the graph pre-pass and the animation replay."""
        char = list(s)
        freqlist: list[tuple[int, str]] = []
        unique_char = set(char)
        for c in unique_char:
            freqlist.append((char.count(c), c))
        freqlist.sort()

        items = [(freq, symbol, symbol) for freq, symbol in freqlist]
        steps = []
        counter = 0
        root_key = None
        while len(items) > 1:
            items.sort()
            left_freq, left_symbol, left_key = items.pop(0)
            right_freq, right_symbol, right_key = items.pop(0)
            merged_freq = left_freq + right_freq
            merged_symbol = left_symbol + right_symbol
            internal_key = f"internal_{counter}"
            steps.append((left_freq, left_symbol, left_key, right_freq, right_symbol, right_key, merged_freq, merged_symbol, internal_key))
            items.append((merged_freq, merged_symbol, internal_key))
            root_key = internal_key
            counter += 1
        return steps, freqlist, root_key

    def build_huffman_graph(self, s):
        steps, freqlist, root_key = self.huffman_steps(s)

        # Build NetworkX graph
        G = nx.Graph()
        node_labels = {}
        edge_weights = {}  # Track edge weights (0 for left, 1 for right)

        # Create initial mapping for leaf nodes
        for freq, symbol in freqlist:
            node_id = f"{symbol}"
            G.add_node(node_id)
            node_labels[node_id] = f"{freq}\n{symbol}"

        # Build tree bottom-up
        for _, _, left_id, _, _, right_id, combined_freq, _, internal_node_id in steps:
            G.add_node(internal_node_id)
            node_labels[internal_node_id] = str(combined_freq)

            # Add edges to children with weights (0 for left, 1 for right)
            G.add_edge(internal_node_id, left_id)
            G.add_edge(internal_node_id, right_id)
            edge_weights[(internal_node_id, left_id)] = 0
            edge_weights[(left_id, internal_node_id)] = 0  # Both directions
            edge_weights[(internal_node_id, right_id)] = 1
            edge_weights[(right_id, internal_node_id)] = 1  # Both directions

        return G, node_labels, edge_weights, root_key  # Return edge weights too

    def construct(self):
        s = 'abbcaaaabbcdddeee'
        
        # Build Huffman tree graph
        G, node_labels, edge_weights, root_id = self.build_huffman_graph(s)
        
        # Create vertex mobjects using HuffmanNode
        vertex_mobjects = {}
        for node_id in G.nodes:
            if node_id.startswith('internal_'):
                # Internal node - only frequency
                frequency = int(node_labels[node_id])
                vertex_mobjects[node_id] = HuffmanNode("", frequency)
            else:
                # Leaf node - has both symbol and frequency
                symbol = node_id
                frequency_text = node_labels[node_id].split('\n')[0]
                frequency = int(frequency_text)
                vertex_mobjects[node_id] = HuffmanNode(symbol, frequency)
        
        # Create edge config with weights
        edge_config = {}
        for edge in G.edges:
            weight = edge_weights.get(edge, edge_weights.get((edge[1], edge[0]), ""))
            edge_config[edge] = {
                'weight': weight,
                "stroke_color": EDGE_COL,
                "stroke_width": 4,
                "weight_font": FONT,
                "standalone_bg": True
            }
        
        # Create Manim graph
        huffman_tree = Graph(
            vertices=list(G.nodes),
            edges=list(G.edges)[::-1],
            vertex_mobjects=vertex_mobjects,
            edge_type=WeightedLine,
            edge_config=edge_config,
            layout="tree",
            layout_scale=3.5,
            root_vertex=root_id
        )
        
        # Move tree to left edge
        huffman_tree.to_edge(LEFT, buff=0.4)
        
        # Animate the Huffman tree construction
        self.animate_huffman_construction(s, huffman_tree)

    def animate_huffman_construction(self, s, huffman_tree):
        steps, freqlist, _ = self.huffman_steps(s)

        # Step 1: Show initial frequency counting
        freq_text = Text(f"Character frequencies in\n  '{s}':", font=FONT, font_size=EXPLANATORY_FONT_SIZE-7, color=TEXTCOL).next_to(huffman_tree, RIGHT, buff=0, aligned_edge=UP)
        self.play(Write(freq_text), run_time=1)
        self.wait(0.5)
        
        # Step 2: Fade in all leaf nodes
        leaf_nodes = []
        for freq, symbol in freqlist:
            leaf_nodes.append(huffman_tree.vertices[symbol])
        
        create_text = Text("Create leaf nodes\n with frequencies", font=FONT, font_size=EXPLANATORY_FONT_SIZE-10, color=BLACK).next_to(freq_text, DOWN, buff=0.6)
        self.play(Write(create_text), run_time=0.8)
        
        self.play(
            *[FadeIn(node) for node in leaf_nodes],
            run_time=2
        )
        self.wait(1)
        
        self.play(FadeOut(freq_text), FadeOut(create_text), run_time=0.5)

        # Step 3: Replay the recorded merge sequence
        for l_freq, l_sym, left_id, r_freq, r_sym, right_id, combined_freq, _, internal_node_id in steps:
            # Explanatory text for selecting nodes
            left_symbol = l_sym if len(l_sym) == 1 else f"({l_sym})"
            right_symbol = r_sym if len(r_sym) == 1 else f"({r_sym})"
            comb_text = f"{left_symbol}({l_freq}) + {right_symbol}({r_freq})"
            spaces = " " * (max(0, len(comb_text) - 9)//2)
            select_text = Text("Select two nodes with\nsmallest frequencies", font=FONT, font_size=EXPLANATORY_FONT_SIZE-7, color=TEXTCOL).next_to(huffman_tree, RIGHT, buff=0.5, aligned_edge=UP)
            detail_text = Text(f"{spaces}Combining\n{comb_text}", font=FONT, font_size=EXPLANATORY_FONT_SIZE-10, color=BLACK).next_to(select_text, DOWN, buff=0.6)

            self.play(Write(select_text), run_time=0.8)
            self.play(Write(detail_text), run_time=0.6)
            
            # Highlight the two smallest frequency nodes
            left_visual = huffman_tree.vertices[left_id]
            right_visual = huffman_tree.vertices[right_id]
            
            self.play(
                left_visual.Select(),
                right_visual.Select(),
                run_time=0.8
            )
            self.wait(0.5)
            
            # Create and show parent node
            parent_node = huffman_tree.vertices[internal_node_id]
            
            parent_text = Text(f"Create parent node\nwith frequency {combined_freq}", font=FONT, font_size=EXPLANATORY_FONT_SIZE-10, color=BLACK).next_to(detail_text, DOWN, buff=0.5)
            self.play(Write(parent_text), run_time=0.6)
            
            self.play(FadeIn(parent_node), run_time=1)
            self.wait(0.5)
            
            # Show edges connecting parent to children
            left_edge = None
            right_edge = None
            
            for edge_key, edge_mob in huffman_tree.edges.items():
                if set(edge_key) == {internal_node_id, left_id}:
                    left_edge = edge_mob
                elif set(edge_key) == {internal_node_id, right_id}:
                    right_edge = edge_mob
            
            edges_to_show = [e for e in [left_edge, right_edge] if e is not None]
            
            edge_text = Text("Connect with weighted\nedges (0=left, 1=right)", font=FONT, font_size=EXPLANATORY_FONT_SIZE-13, color=BLACK).next_to(parent_text, DOWN, buff=0.6)
            self.play(Write(edge_text), run_time=0.5)
            
            if edges_to_show:
                self.play(
                    *[Create(edge) for edge in edges_to_show],
                    run_time=1
                )
            
            # Clear highlighting and text
            self.play(
                left_visual.Clear(),
                right_visual.Clear(),
                run_time=0.5
            )
            
            self.play(FadeOut(select_text), FadeOut(detail_text), FadeOut(parent_text), FadeOut(edge_text), run_time=0.5)
            self.wait(0.5)

        self.wait(1)