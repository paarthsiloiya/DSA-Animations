from manim import *
from manim.utils.unit import Percent, Pixels
import random
import networkx as nx

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
EXPLANATORY_FONT_SIZE = 50  # For step-by-step explanations
POINTER_FONT_SIZE = 28      # For pointer labels (if any)

NODE_COL = BASECOL
EDGE_COL = SELCOL


class NodeVisual(VGroup):
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

class AVLNode(VGroup):
    def __init__(self, value):
        super().__init__()
        self.value: int = value
        self.tree_height: int = 1
        self.left : AVLNode | None = None
        self.right : AVLNode | None = None

        self.balanceFactor = ValueTracker(0)
        self.balanceFactorText = DecimalNumber(
            self.balanceFactor.get_value(), 
            num_decimal_places=0, 
            font_size=POINTER_FONT_SIZE, 
            fill_color=TEXTCOL,
            # stroke_width=0,
        ).set_z_index(3).next_to(UP, buff=0.2)
        
        self.node = NodeVisual(value).set_z_index(2)

        self.balanceFactorText.add_updater(
            lambda m: m.set_value(self.balanceFactor.get_value())
        )
        self.balanceFactorText.add_updater(
            lambda m: m.next_to(self.node, UP, buff=0.2)
        )

        # Add updater for automatic tree height calculation
        def update_tree_height():
            left_height = self.left.tree_height if self.left is not None else 0
            right_height = self.right.tree_height if self.right is not None else 0
            self.tree_height = 1 + max(left_height, right_height)
        
        # Store the updater function so we can reference it later if needed
        self._height_updater = update_tree_height
        self.add_updater(lambda m: update_tree_height())

        self.leftPos = Dot(self.node.get_center() + DOWN + (LEFT * (self.tree_height - 1)), color=BLUE, fill_opacity=0)
        self.rightPos = Dot(self.node.get_center() + DOWN + (RIGHT * (self.tree_height - 1)), color=RED, fill_opacity=0)

        self.left_edge = Line(
            self.node.get_center(),
            self.node.get_center(),
            color=EDGE_COL,
            stroke_width=6
        )

        self.right_edge = Line(
            self.node.get_center(),
            self.node.get_center(),
            color=EDGE_COL,
            stroke_width=6
        )

        self.leftPos.add_updater(
            lambda m : m.move_to(
                    self.node.get_center() + DOWN + (LEFT * (self.tree_height - 1))
            )
        )

        self.rightPos.add_updater(
            lambda m : m.move_to(
                    self.node.get_center() + DOWN + (RIGHT * (self.tree_height - 1))
            )
        )

        def left_edge_updater(m):
            if self.left is not None:
                m.put_start_and_end_on(
                    self.node.get_center(), 
                    self.leftPos.get_center()
                )
            else:
                m.put_start_and_end_on(
                    self.node.get_center(), 
                    self.node.get_center() + (DOWN * 0.1)
                )

        def right_edge_updater(m):
            if self.right is not None:
                m.put_start_and_end_on(
                    self.node.get_center(), 
                    self.rightPos.get_center()
                )
            else:
                m.put_start_and_end_on(
                    self.node.get_center(), 
                    self.node.get_center() + (DOWN * 0.1)
                )

        self.left_edge.add_updater(left_edge_updater)
        self.right_edge.add_updater(right_edge_updater)

        self.add(
            self.node, 
            self.balanceFactorText, 
            self.leftPos, 
            self.rightPos, 
            self.left_edge, 
            self.right_edge
        )

    def set_left(self):
        if self.left is None:
            return

        # Clear any existing updaters and add the new one
        self.left.node.clear_updaters()
        self.left.node.add_updater(
            lambda m: m.move_to(self.leftPos.get_center())
        )

    def set_right(self):
        if self.right is None:
            return

        # Clear any existing updaters and add the new one
        self.right.node.clear_updaters()
        self.right.node.add_updater(
            lambda m: m.move_to(self.rightPos.get_center())
        )


class AVLTreeInsertion(Scene):
    def height(self, node: AVLNode):
        if node is None:
            return 0
        return node.tree_height
    
    def right_rotate(self, y : AVLNode):
        x = y.left

        self.play(
            y.node.Select(),
            x.node.Select()
        )

        T2 = x.right

        # Clear updaters and update tree structure
        if y.left is not None:
            y.left.node.clear_updaters()
        if x.right is not None:
            x.right.node.clear_updaters()
            
        y.node.clear_updaters()
        x.node.clear_updaters()

        # Update the tree structure
        y.left = T2
        x.right = y

        # Move nodes to their new positions
        self.play(
            y.node.animate.move_to(x.rightPos.get_center()),
            run_time=0.8
        )

        # Set up the new parent-child relationships with updaters
        x.set_right()
        if T2 is not None:
            y.set_left()

        self.play(
            y.node.Clear(),
            x.node.Clear()
        )

        self.recalculate_balance_factors([y, x])

        return x
    
    def left_rotate(self, x : AVLNode):
        y = x.right

        self.play(
            x.node.Select(),
            y.node.Select()
        )

        T2 = y.left

        # Clear updaters and update tree structure
        if x.right is not None:
            x.right.node.clear_updaters()
        if y.left is not None:
            y.left.node.clear_updaters()
            
        x.node.clear_updaters()
        y.node.clear_updaters()

        # Update the tree structure
        x.right = T2
        y.left = x

        # Move nodes to their new positions
        self.play(
            x.node.animate.move_to(y.leftPos.get_center()),
            run_time=0.8
        )

        # Set up the new parent-child relationships with updaters
        y.set_left()
        if T2 is not None:
            x.set_right()

        self.play(
            y.node.Clear(),
            x.node.Clear()
        )

        self.recalculate_balance_factors([x, y])

        return y
    
    def get_balance(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)
    
    def insert(self, node : AVLNode, value, is_left=False, parent_node : AVLNode = None):
        if node is None:
            avlnode = AVLNode(value)
            if parent_node is not None:
                if is_left:
                    avlnode.move_to(parent_node.leftPos.get_center() + LEFT)
                else:
                    avlnode.move_to(parent_node.rightPos.get_center() + RIGHT)
            
            self.play(Create(avlnode), run_time=0.5)
            self.nodeGroup.add(avlnode.node)
            self.AVLnodeGroup.append(avlnode)
            self.wait(0.52)
            return avlnode

        if value < node.value:
            node.left = self.insert(node.left, value, True, node)
            node.set_left()
            self.wait(0.52)
        elif value > node.value:
            node.right = self.insert(node.right, value, False, node)
            node.set_right()
            self.wait(0.52)
        else:
            return node
        
        balance = self.get_balance(node)

        old_balance = node.balanceFactor.get_value()
        new_balance = self.get_balance(node)
        if abs(old_balance - new_balance) > 0.001:
            self.play(Indicate(node.balanceFactorText, color=SELCOL), run_time=0.3)
            self.wait(0.1)
            node.balanceFactor.set_value(new_balance)
            self.wait(0.2)

        if balance > 1 and value < node.left.value:
            print("Left Left Case")
            return self.right_rotate(node)
        
        if balance < -1 and value > node.right.value:
            print("Right Right Case")
            return self.left_rotate(node)
        
        if balance > 1 and value > node.left.value:
            print("Left Right Case")
            node.left = self.left_rotate(node.left)
            self.wait(1)
            return self.right_rotate(node)
        
        if balance < -1 and value < node.right.value:
            print("Right Left Case")
            node.right = self.right_rotate(node.right)
            self.wait(1)
            return self.left_rotate(node)
        
        return node
    
    def recalculate_balance_factors(self, nodes_to_update=None):
        if nodes_to_update is None:
            nodes_to_update = self.AVLnodeGroup
        
        for avl_node in nodes_to_update:
            old_balance = avl_node.balanceFactor.get_value()
            new_balance = self.get_balance(avl_node)
            
            if abs(old_balance - new_balance) > 0.001:  # Use abs for better floating point comparison
                self.play(Indicate(avl_node.balanceFactorText, color=SELCOL), run_time=0.5)
                self.wait(0.1)
                avl_node.balanceFactor.set_value(new_balance)
                self.wait(0.2)
    
    def collect_path_to_node(self, root, value, path=None):
        if path is None:
            path = []
        
        if root is None:
            return path
        
        path.append(root)
        
        if value < root.value:
            return self.collect_path_to_node(root.left, value, path)
        elif value > root.value:
            return self.collect_path_to_node(root.right, value, path)
        else:
            return path

    def insert_into_AVLTree(self, root, value):
        path_nodes = []
        if root is not None:
            path_nodes = self.collect_path_to_node(root, value)
        
        root = self.insert(root, value)
        self.wait(0.2)
        self.play(self.nodeGroup.animate.center().shift(UP * 0.3))
        self.wait(0.2)
        
        affected_nodes = []
        
        for node in path_nodes:
            old_displayed = node.balanceFactorText.get_value() 
            actual_balance = self.get_balance(node)
            if abs(old_displayed - actual_balance) > 0.001:
                affected_nodes.append(node)
        
        if self.AVLnodeGroup:
            new_node = self.AVLnodeGroup[-1]
            if new_node not in path_nodes:
                affected_nodes.append(new_node)
        
        if affected_nodes:
            self.recalculate_balance_factors(affected_nodes)
        
        return root


    def construct(self):
        self.nodeGroup = VGroup()
        self.AVLnodeGroup : list[AVLNode] = []
        root = None

        values = [3, 4, 5, 6, 7, 2, 1, 9, 8, 10, 11]

        for value in values:
            print(f"Inserting {value} into AVL Tree")
            root = self.insert_into_AVLTree(root, value)

        self.wait(2)


class RightRightCase(Scene):
    """Right-Right case: balance factor < -1, needs left rotation"""
    def construct(self):
        # Create nodes step by step to show the problem
        explanation = Text("Insert 3", font_size=EXPLANATORY_FONT_SIZE, color=TEXTCOL)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))

        node3 = AVLNode(3)
        node3.move_to(ORIGIN + UP)
        node3.balanceFactor.set_value(0)
        self.play(Create(node3))
        self.wait(0.5)
        self.play(FadeOut(explanation))
        self.wait(1)


        # Insert left Subtree of Node 3
        nodex = AVLNode("X")
        nodex.move_to(node3.leftPos.get_center())
        self.play(nodex.node.Highlight())
        self.play(Create(nodex))
        self.remove(nodex.balanceFactorText)
        node3.left = nodex
        self.wait(0.5)
        node3.set_left()
        self.wait(1)

        # Insert 4
        explanation = Text("Insert 4", font_size=EXPLANATORY_FONT_SIZE, color=TEXTCOL)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))

        node4 = AVLNode(4)
        node4.move_to(node3.rightPos.get_center())
        self.play(Create(node4))
        node3.right = node4
        self.wait(0.5)
        node3.set_right()
        self.wait(0.5)
        self.play(Indicate(node3.balanceFactorText, color=SELCOL), run_time=0.5)
        node3.balanceFactor.set_value(-1)
        self.wait(0.5)
        self.play(FadeOut(explanation))
        self.wait(1)

        # Insert left Subtree of Node 4
        nodey = AVLNode("Y")
        nodey.move_to(node4.leftPos.get_center())
        self.play(nodey.node.Highlight())
        self.play(Create(nodey))
        self.remove(nodey.balanceFactorText)
        node4.left = nodey
        self.wait(0.5)
        node4.set_left()
        self.wait(1)

        # Insert 5 - causes imbalance
        explanation = Text("Insert 5", font_size=EXPLANATORY_FONT_SIZE, color=TEXTCOL)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))

        node5 = AVLNode(5)
        node5.move_to(node4.rightPos.get_center())
        self.play(Create(node5))
        node4.right = node5
        self.wait(0.5)
        node4.set_right()
        self.wait(0.5)
        self.play(Indicate(node4.balanceFactorText, color=SELCOL), run_time=0.5)
        node4.balanceFactor.set_value(-1)
        self.play(Indicate(node3.balanceFactorText, color=SELCOL), run_time=0.5)
        node3.balanceFactor.set_value(-2)
        self.wait(0.5)
        self.play(FadeOut(explanation))
        self.wait(1)


        # Inserting left and right Subtree of Node 5
        nodez = AVLNode("Z")
        nodew = AVLNode("W")
        nodez.move_to(node5.leftPos.get_center() + LEFT)
        nodew.move_to(node5.rightPos.get_center() + RIGHT)
        self.play(nodez.node.Highlight(), nodew.node.Highlight())
        self.play(Create(nodez), Create(nodew))
        self.remove(nodez.balanceFactorText, nodew.balanceFactorText)
        node5.left = nodez
        node5.right = nodew
        node5.set_left()
        node5.set_right()
        self.wait(1)

        # Highlight imbalance
        explanation = Text("Balance factor = -2 (IMBALANCED!)", font_size=EXPLANATORY_FONT_SIZE, color=RED)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))
        self.play(Indicate(node3.balanceFactorText, color=RED, scale_factor=1.5))
        self.wait(2)
        
        # Show curved arrow for rotation
        arrow = CurvedArrow(
            start_point=node3.node.get_center(),
            end_point=node4.node.get_left(),
            color=RED,
            stroke_width=3,
        )
        arrow_label = Text("Left Rotation", font_size=SWAP_FONT_SIZE, color=RED)
        arrow_label.next_to(explanation, DOWN, buff=0.2)
        
        self.play(Create(arrow), Write(arrow_label))
        self.wait(1)
        self.play(FadeOut(arrow))

        self.wait(0.5)

        # Perform left rotation
        node3.right = None
        node3.set_right()
        node4.node.clear_updaters()
        node4.left = None
        node4.set_left()
        nodey.node.clear_updaters()
        
        # Animate the rotation
        self.play(
            node3.node.animate.move_to(node4.leftPos.get_center()),
            nodey.node.animate.shift(DR),
            run_time=0.5
        )

        # Update tree structure
        node3.right = nodey
        node4.left = node3
        
        # Set up new relationships
        node3.set_right()
        node4.set_left()
        
        # Update balance factors
        node3.balanceFactor.set_value(0)
        node4.balanceFactor.set_value(0)
        node5.balanceFactor.set_value(0)

        self.play(FadeOut(explanation), FadeOut(arrow_label))

        self.play(node4.animate.move_to(ORIGIN + UP), run_time=0.5)
        
        result_text = Text("Tree is now balanced!", font_size=EXPLANATORY_FONT_SIZE, color=GREEN)
        result_text.to_edge(UP, buff=0.5)
        self.play(Write(result_text))
        self.wait(2)


class LeftLeftCase(Scene):
    """Left-Left case: balance factor > 1, needs right rotation"""
    
    def construct(self):
        # Create nodes step by step to show the problem
        explanation = Text("Insert 5", font_size=EXPLANATORY_FONT_SIZE, color=TEXTCOL)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))

        node5 = AVLNode(5)
        node5.move_to(ORIGIN + UP)
        node5.balanceFactor.set_value(0)
        self.play(Create(node5))
        self.wait(0.5)
        self.play(FadeOut(explanation))
        self.wait(1)

        # Insert right Subtree of Node 5
        nodex = AVLNode("X")
        nodex.move_to(node5.rightPos.get_center())
        self.play(nodex.node.Highlight())
        self.play(Create(nodex))
        self.remove(nodex.balanceFactorText)
        node5.right = nodex
        self.wait(0.5)
        node5.set_right()
        self.wait(1)

        # Insert 4
        explanation = Text("Insert 4", font_size=EXPLANATORY_FONT_SIZE, color=TEXTCOL)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))

        node4 = AVLNode(4)
        node4.move_to(node5.leftPos.get_center())
        self.play(Create(node4))
        node5.left = node4
        self.wait(0.5)
        node5.set_left()
        self.wait(0.5)
        self.play(Indicate(node5.balanceFactorText, color=SELCOL), run_time=0.5)
        node5.balanceFactor.set_value(1)
        self.wait(0.5)
        self.play(FadeOut(explanation))
        self.wait(1)

        # Insert right Subtree of Node 4
        nodey = AVLNode("Y")
        nodey.move_to(node4.rightPos.get_center())
        self.play(nodey.node.Highlight())
        self.play(Create(nodey))
        self.remove(nodey.balanceFactorText)
        node4.right = nodey
        self.wait(0.5)
        node4.set_right()
        self.wait(1)

        # Insert 3 - causes imbalance
        explanation = Text("Insert 3", font_size=EXPLANATORY_FONT_SIZE, color=TEXTCOL)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))

        node3 = AVLNode(3)
        node3.move_to(node4.leftPos.get_center())
        self.play(Create(node3))
        node4.left = node3
        self.wait(0.5)
        node4.set_left()
        self.wait(0.5)
        self.play(Indicate(node4.balanceFactorText, color=SELCOL), run_time=0.5)
        node4.balanceFactor.set_value(1)
        self.play(Indicate(node5.balanceFactorText, color=SELCOL), run_time=0.5)
        node5.balanceFactor.set_value(2)
        self.wait(0.5)
        self.play(FadeOut(explanation))
        self.wait(1)

        # Inserting left and right Subtree of Node 3
        nodez = AVLNode("Z")
        nodew = AVLNode("W")
        nodez.move_to(node3.leftPos.get_center() + LEFT)
        nodew.move_to(node3.rightPos.get_center() + RIGHT)
        self.play(nodez.node.Highlight(), nodew.node.Highlight())
        self.play(Create(nodez), Create(nodew))
        self.remove(nodez.balanceFactorText, nodew.balanceFactorText)
        node3.left = nodez
        node3.right = nodew
        node3.set_left()
        node3.set_right()
        self.wait(1)

        # Highlight imbalance
        explanation = Text("Balance factor = 2 (IMBALANCED!)", font_size=EXPLANATORY_FONT_SIZE, color=RED)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))
        self.play(Indicate(node5.balanceFactorText, color=RED, scale_factor=1.5))
        self.wait(2)
        
        # Show curved arrow for rotation
        arrow = CurvedArrow(
            start_point=node5.node.get_center(),
            end_point=node4.node.get_right(),
            color=RED,
            stroke_width=3,
            angle=-PI/2
        )
        arrow_label = Text("Left Rotation", font_size=SWAP_FONT_SIZE, color=RED)
        arrow_label.next_to(explanation, DOWN, buff=0.2)
        
        self.play(Create(arrow), Write(arrow_label))
        self.wait(1)
        self.play(FadeOut(arrow))

        self.wait(0.5)

        # Perform right rotation
        node5.left = None
        node5.set_left()
        node4.node.clear_updaters()
        node4.right = None
        node4.set_right()
        nodey.node.clear_updaters()
        
        # Animate the rotation
        self.play(
            node5.node.animate.move_to(node4.rightPos.get_center()),
            nodey.node.animate.shift(DL),
            run_time=0.5
        )

        # Update tree structure
        node5.left = nodey
        node4.right = node5
        
        # Set up new relationships
        node5.set_left()
        node4.set_right()
        
        # Update balance factors
        node5.balanceFactor.set_value(0)
        node4.balanceFactor.set_value(0)
        node3.balanceFactor.set_value(0)

        self.play(FadeOut(explanation), FadeOut(arrow_label))

        self.play(node4.animate.move_to(ORIGIN + UP), run_time=0.5)
        
        result_text = Text("Tree is now balanced!", font_size=EXPLANATORY_FONT_SIZE, color=GREEN)
        result_text.to_edge(UP, buff=0.5)
        self.play(Write(result_text))
        self.wait(2)


class LeftRightCase(Scene):
    """Left-Right case: balance factor > 1, needs left-right rotation"""
    
    def construct(self):
        # Create nodes step by step to show the problem
        explanation = Text("Insert 5", font_size=EXPLANATORY_FONT_SIZE, color=TEXTCOL)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))

        node5 = AVLNode(5)
        node5.move_to(ORIGIN + UP)
        node5.balanceFactor.set_value(0)
        self.play(Create(node5))
        self.wait(0.5)
        self.play(FadeOut(explanation))
        self.wait(1)

        # Insert right Subtree of Node 5
        nodex = AVLNode("X")
        nodex.move_to(node5.rightPos.get_center())
        self.play(nodex.node.Highlight())
        self.play(Create(nodex))
        self.remove(nodex.balanceFactorText)
        node5.right = nodex
        self.wait(0.5)
        node5.set_right()
        self.wait(1)

        # Insert 3
        explanation = Text("Insert 3", font_size=EXPLANATORY_FONT_SIZE, color=TEXTCOL)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))

        node3 = AVLNode(3)
        node3.move_to(node5.leftPos.get_center())
        self.play(Create(node3))
        node5.left = node3
        self.wait(0.5)
        node5.set_left()
        self.wait(0.5)
        self.play(Indicate(node5.balanceFactorText, color=SELCOL), run_time=0.5)
        node5.balanceFactor.set_value(1)
        self.wait(0.5)
        self.play(FadeOut(explanation))
        self.wait(1)

        # Insert left Subtree of Node 3
        nodey = AVLNode("Y")
        nodey.move_to(node3.leftPos.get_center())
        self.play(nodey.node.Highlight())
        self.play(Create(nodey))
        self.remove(nodey.balanceFactorText)
        node3.left = nodey
        self.wait(0.5)
        node3.set_left()
        self.wait(1)

        # Insert 4 - causes imbalance
        explanation = Text("Insert 4", font_size=EXPLANATORY_FONT_SIZE, color=TEXTCOL)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))

        node4 = AVLNode(4)
        node4.move_to(node3.rightPos.get_center())
        self.play(Create(node4))
        node3.right = node4
        self.wait(0.5)
        node3.set_right()
        self.wait(0.5)
        self.play(Indicate(node3.balanceFactorText, color=SELCOL), run_time=0.5)
        node3.balanceFactor.set_value(-1)
        self.play(Indicate(node5.balanceFactorText, color=SELCOL), run_time=0.5)
        node5.balanceFactor.set_value(2)
        self.wait(0.5)
        self.play(FadeOut(explanation))
        self.wait(1)

        # Inserting left and right Subtree of Node 4
        nodez = AVLNode("Z")
        nodew = AVLNode("W")
        nodez.move_to(node4.leftPos.get_center() + LEFT)
        nodew.move_to(node4.rightPos.get_center() + RIGHT)
        self.play(nodez.node.Highlight(), nodew.node.Highlight())
        self.play(Create(nodez), Create(nodew))
        self.remove(nodez.balanceFactorText, nodew.balanceFactorText)
        node4.left = nodez
        node4.right = nodew
        node4.set_left()
        node4.set_right()
        self.wait(1)

        # Highlight imbalance
        explanation = Text("Balance factor = 2 (IMBALANCED!)", font_size=EXPLANATORY_FONT_SIZE, color=RED)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))
        self.play(Indicate(node5.balanceFactorText, color=RED, scale_factor=1.5))
        self.wait(2)
        
        # Step 1: Left rotation on left subtree
        step1_label = Text("Step 1: Left rotation (3-4)", font_size=SWAP_FONT_SIZE, color=RED)
        step1_label.next_to(explanation, DOWN, buff=0.2)
        self.play(Write(step1_label))
        
        # Show curved arrow for first rotation
        arrow1 = CurvedArrow(
            start_point=node3.node.get_center(),
            end_point=node4.node.get_left(),
            color=RED,
            stroke_width=3,
        )
        self.play(Create(arrow1))
        self.wait(1)
        self.play(FadeOut(arrow1))

        # Perform first rotation
        node5.left = None
        node5.set_left()
        node3.node.clear_updaters()
        node3.right = None
        node3.set_right()
        node4.node.clear_updaters()
        node4.left = None
        node4.set_left()
        nodez.node.clear_updaters()
        
        # Animate the first rotation
        self.play(
            node4.node.animate.move_to(node3.node.get_center()),
            node3.node.animate.move_to(nodey.node.get_center()),
            nodez.node.animate.shift(LEFT * 2),
            run_time=0.5
        )

        # Update tree structure after first rotation
        node3.right = nodez
        node4.left = node3
        node5.left = node4
        
        # Set up new relationships
        node3.set_right()
        node4.set_left()
        node5.set_left()
        
        self.wait(1)

        # Step 2: Right rotation on root
        step2_label = Text("Step 2: Right rotation (5-4)", font_size=SWAP_FONT_SIZE, color=RED)
        step2_label.next_to(step1_label, DOWN, buff=0.2)
        self.play(Write(step2_label))
        
        # Show curved arrow for second rotation
        arrow2 = CurvedArrow(
            start_point=node5.node.get_center(),
            end_point=node4.node.get_right(),
            color=RED,
            stroke_width=3,
            angle=-PI/2
        )
        self.play(Create(arrow2))
        self.wait(1)
        self.play(FadeOut(arrow2))

        # Perform second rotation
        node5.left = None
        node5.set_left()
        node4.node.clear_updaters()
        node4.right = None
        node4.set_right()
        nodew.node.clear_updaters()
        
        # Animate the second rotation
        self.play(
            node5.node.animate.move_to(node4.rightPos.get_center()),
            nodew.node.animate.shift(DL),
            run_time=0.5
        )

        # Update tree structure after second rotation
        node5.left = nodew
        node4.right = node5
        
        # Set up new relationships
        node5.set_left()
        node4.set_right()
        
        # Update balance factors
        node3.balanceFactor.set_value(0)
        node4.balanceFactor.set_value(0)
        node5.balanceFactor.set_value(0)

        self.play(FadeOut(explanation), FadeOut(step1_label), FadeOut(step2_label))

        self.play(node4.animate.move_to(ORIGIN + UP), run_time=0.5)
        
        result_text = Text("Tree is now balanced!", font_size=EXPLANATORY_FONT_SIZE, color=GREEN)
        result_text.to_edge(UP, buff=0.5)
        self.play(Write(result_text))
        self.wait(2)


class RightLeftCase(Scene):
    """Right-Left case: balance factor < -1, needs right-left rotation"""
    
    def construct(self):
        # Create nodes step by step to show the problem
        explanation = Text("Insert 3", font_size=EXPLANATORY_FONT_SIZE, color=TEXTCOL)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))

        node3 = AVLNode(3)
        node3.move_to(ORIGIN + UP)
        node3.balanceFactor.set_value(0)
        self.play(Create(node3))
        self.wait(0.5)
        self.play(FadeOut(explanation))
        self.wait(1)

        # Insert left Subtree of Node 3
        nodex = AVLNode("X")
        nodex.move_to(node3.leftPos.get_center())
        self.play(nodex.node.Highlight())
        self.play(Create(nodex))
        self.remove(nodex.balanceFactorText)
        node3.left = nodex
        self.wait(0.5)
        node3.set_left()
        self.wait(1)

        # Insert 5
        explanation = Text("Insert 5", font_size=EXPLANATORY_FONT_SIZE, color=TEXTCOL)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))

        node5 = AVLNode(5)
        node5.move_to(node3.rightPos.get_center())
        self.play(Create(node5))
        node3.right = node5
        self.wait(0.5)
        node3.set_right()
        self.wait(0.5)
        self.play(Indicate(node3.balanceFactorText, color=SELCOL), run_time=0.5)
        node3.balanceFactor.set_value(-1)
        self.wait(0.5)
        self.play(FadeOut(explanation))
        self.wait(1)

        # Insert right Subtree of Node 5
        nodey = AVLNode("Y")
        nodey.move_to(node5.rightPos.get_center())
        self.play(nodey.node.Highlight())
        self.play(Create(nodey))
        self.remove(nodey.balanceFactorText)
        node5.right = nodey
        self.wait(0.5)
        node5.set_right()
        self.wait(1)

        # Insert 4 - causes imbalance
        explanation = Text("Insert 4", font_size=EXPLANATORY_FONT_SIZE, color=TEXTCOL)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))

        node4 = AVLNode(4)
        node4.move_to(node5.leftPos.get_center())
        self.play(Create(node4))
        node5.left = node4
        self.wait(0.5)
        node5.set_left()
        self.wait(0.5)
        self.play(Indicate(node5.balanceFactorText, color=SELCOL), run_time=0.5)
        node5.balanceFactor.set_value(1)
        self.play(Indicate(node3.balanceFactorText, color=SELCOL), run_time=0.5)
        node3.balanceFactor.set_value(-2)
        self.wait(0.5)
        self.play(FadeOut(explanation))
        self.wait(1)

        # Inserting left and right Subtree of Node 4
        nodez = AVLNode("Z")
        nodew = AVLNode("W")
        nodez.move_to(node4.leftPos.get_center() + LEFT)
        nodew.move_to(node4.rightPos.get_center() + RIGHT)
        self.play(nodez.node.Highlight(), nodew.node.Highlight())
        self.play(Create(nodez), Create(nodew))
        self.remove(nodez.balanceFactorText, nodew.balanceFactorText)
        node4.left = nodez
        node4.right = nodew
        node4.set_left()
        node4.set_right()
        self.wait(1)

        # Highlight imbalance
        explanation = Text("Balance factor = -2 (IMBALANCED!)", font_size=EXPLANATORY_FONT_SIZE, color=RED)
        explanation.to_edge(UP, buff=0.5)
        self.play(Write(explanation))
        self.play(Indicate(node3.balanceFactorText, color=RED, scale_factor=1.5))
        self.wait(2)
        
        # Step 1: Right rotation on right subtree
        step1_label = Text("Step 1: Right rotation (5-4)", font_size=SWAP_FONT_SIZE, color=RED)
        step1_label.next_to(explanation, DOWN, buff=0.2)
        self.play(Write(step1_label))
        
        # Show curved arrow for first rotation
        arrow1 = CurvedArrow(
            start_point=node5.node.get_center(),
            end_point=node4.node.get_right(),
            color=RED,
            stroke_width=3,
            angle=-PI/2
        )
        self.play(Create(arrow1))
        self.wait(1)
        self.play(FadeOut(arrow1))

        # Perform first rotation
        node3.right = None
        node3.set_right()
        node5.node.clear_updaters()
        node5.left = None
        node5.set_left()
        node4.node.clear_updaters()
        node4.right = None
        node4.set_right()
        nodew.node.clear_updaters()
        
        # Animate the first rotation
        self.play(
            node4.node.animate.move_to(node5.node.get_center()),
            node5.node.animate.move_to(nodey.node.get_center()),
            nodew.node.animate.shift(RIGHT * 2),
            run_time=0.5
        )

        # Update tree structure after first rotation
        node5.left = nodew
        node4.right = node5
        node3.right = node4
        
        # Set up new relationships
        node5.set_left()
        node4.set_right()
        node3.set_right()
        
        self.wait(1)

        # Step 2: Left rotation on root
        step2_label = Text("Step 2: Left rotation (3-4)", font_size=SWAP_FONT_SIZE, color=RED)
        step2_label.next_to(step1_label, DOWN, buff=0.2)
        self.play(Write(step2_label))
        
        # Show curved arrow for second rotation
        arrow2 = CurvedArrow(
            start_point=node3.node.get_center(),
            end_point=node4.node.get_left(),
            color=RED,
            stroke_width=3,
            angle=PI/2
        )
        self.play(Create(arrow2))
        self.wait(1)
        self.play(FadeOut(arrow2))

        # Perform second rotation
        node3.right = None
        node3.set_right()
        node4.node.clear_updaters()
        node4.left = None
        node4.set_left()
        nodez.node.clear_updaters()
        
        # Animate the second rotation
        self.play(
            node3.node.animate.move_to(node4.leftPos.get_center()),
            nodez.node.animate.shift(DR),
            run_time=0.5
        )

        # Update tree structure after second rotation
        node3.right = nodez
        node4.left = node3
        
        # Set up new relationships
        node3.set_right()
        node4.set_left()
        
        # Update balance factors
        node3.balanceFactor.set_value(0)
        node4.balanceFactor.set_value(0)
        node5.balanceFactor.set_value(0)

        self.play(FadeOut(explanation), FadeOut(step1_label), FadeOut(step2_label))

        self.play(node4.animate.move_to(ORIGIN + UP), run_time=0.5)
        
        result_text = Text("Tree is now balanced!", font_size=EXPLANATORY_FONT_SIZE, color=GREEN)
        result_text.to_edge(UP, buff=0.5)
        self.play(Write(result_text))
        self.wait(2)