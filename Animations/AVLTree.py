from manim import *
from manim.utils.unit import Percent, Pixels
import random
import networkx as nx
from env_config import *

random.seed(32)

# Override specific font sizes for AVLTree
EXPLANATORY_FONT_SIZE = 50  # For step-by-step explanations
POINTER_FONT_SIZE = 28      # For pointer labels (if any)


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


class AVLTreeDeletion(Scene):
    def construct(self):
        self.nodeGroup = VGroup()
        self.AVLnodeGroup: list[AVLNode] = []
        self.root = None

        # Build initial AVL tree silently (without animations)
        values = [26, 7, 2, 25, 19, 47, 1, 90, 36, 3, 34]
        
        for value in values:
            self.root = self.build_tree_silently(self.root, value)

        # Center the tree and fade it in
        self.nodeGroup.center().shift(UP * 0.3)
        self.play(FadeIn(self.nodeGroup), run_time=1)
        self.wait(1)

        # Perform deletions
        self.root = self.delete_avl(self.root, 1)
        self.wait(0.5)
        self.root = self.delete_avl(self.root, 25)
        self.wait(0.5)
        self.root = self.delete_avl(self.root, 26)
        self.wait(0.5)
        self.root = self.delete_avl(self.root, 19)

        self.wait(1)
        self.play(self.nodeGroup.animate.center().shift(UP * 0.3))
        self.wait(2)


    def height(self, node: AVLNode):
        if node is None:
            return 0
        return node.tree_height
    
    def right_rotate(self, y: AVLNode):
        x = y.left
        
        # Show rotation explanation
        rotation_text = Text("Right Rotation Required", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).to_edge(UP, buff=0.2)
        self.play(Write(rotation_text), run_time=0.5)
        
        # Highlight the nodes being rotated
        self.play(
            y.node.Select(),
            x.node.Select(),
            run_time=0.5
        )
        
        # Perform rotation
        T2 = x.right
        
        # Clear updaters
        if y.left is not None:
            y.left.node.clear_updaters()
        if x.right is not None:
            x.right.node.clear_updaters()
            
        y.node.clear_updaters()
        x.node.clear_updaters()

        # Update tree structure
        y.left = T2
        x.right = y

        # Animate rotation with smooth movement
        self.play(
            y.node.animate.move_to(x.rightPos.get_center()),
            run_time=0.8
        )

        # Set up new relationships
        x.set_right()
        if T2 is not None:
            y.set_left()
        
        # Clean up rotation text
        self.play(Unwrite(rotation_text), run_time=0.3)

        self.recalculate_balance_factors([y, x])
        
        # Ensure the rotated subtree root (x) gets reconnected to its parent
        # by clearing its updater and forcing parent to reset connection
        x.node.clear_updaters()
        
        # Clear selection highlighting first, then recenter
        self.play(
            y.node.Clear(),
            x.node.Clear(),
            run_time=0.3
        )

        return x
    
    def left_rotate(self, x: AVLNode):
        y = x.right
        
        # Show rotation explanation
        rotation_text = Text("Left Rotation Required", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).to_edge(UP, buff=0.2)
        self.play(Write(rotation_text), run_time=0.5)
        
        # Highlight the nodes being rotated
        self.play(
            x.node.Select(),
            y.node.Select(),
            run_time=0.5
        )
        
        # Perform rotation
        T2 = y.left
        
        # Clear updaters
        if x.right is not None:
            x.right.node.clear_updaters()
        if y.left is not None:
            y.left.node.clear_updaters()
            
        x.node.clear_updaters()
        y.node.clear_updaters()

        # Update tree structure
        x.right = T2
        y.left = x

        # Animate rotation with smooth movement
        self.play(
            x.node.animate.move_to(y.leftPos.get_center()),
            run_time=0.8
        )

        # Set up new relationships
        y.set_left()
        if T2 is not None:
            x.set_right()
        
        # Clean up rotation text
        self.play(Unwrite(rotation_text), run_time=0.3)

        self.recalculate_balance_factors([x, y])
        
        # Ensure the rotated subtree root (y) gets reconnected to its parent
        # by clearing its updater and forcing parent to reset connection
        y.node.clear_updaters()
        
        # Clear selection highlighting first, then recenter
        self.play(
            x.node.Clear(),
            y.node.Clear(),
            run_time=0.3
        )
        
        return y
    
    def get_balance(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)
    
    def find_successor(self, node: AVLNode):
        """Find the inorder successor (smallest value in right subtree)"""
        if node.right is None:
            return None
            
        current = node.right
        
        # Create a successor search indicator
        successor_search_surr = DashedVMobject(SurroundingRectangle(current.node, color=BLUE, buff=0, corner_radius=0.52))
        successor_search_surr.set_z_index(3)
        
        sub_explanatory_text = Text(f"Finding successor: go right to {current.value}", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).to_edge(DOWN, buff=1.3)
        self.play(Create(successor_search_surr), Write(sub_explanatory_text), run_time=0.5)
        self.wait(0.3)
        
        # Go to right subtree and find leftmost node
        while current.left is not None:
            # Move to left child
            left_node = current.left
            
            self.play(Unwrite(sub_explanatory_text), run_time=0.3)
            sub_explanatory_text = Text(f"Go left to {left_node.value}", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).to_edge(DOWN, buff=1.3)
            self.play(
                successor_search_surr.animate.move_to(left_node.node.get_center()),
                Write(sub_explanatory_text),
                run_time=0.5
            )
            self.wait(0.3)
            current = left_node
        
        # Found the successor
        self.play(Unwrite(sub_explanatory_text), run_time=0.3)
        sub_explanatory_text = Text(f"Successor found: {current.value}", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).to_edge(DOWN, buff=1.3)
        self.play(Write(sub_explanatory_text), run_time=0.5)
        self.wait(0.5)
        
        # Clean up the search indicator
        self.play(Uncreate(successor_search_surr), Unwrite(sub_explanatory_text), run_time=0.5)
        
        return current

    def delete_avl(self, root: AVLNode, value):
        explanatory_text = Text(f"Deleting {value}", font=FONT, color=TEXTCOL, font_size=FSIZE).to_edge(DOWN, buff=1.9)
        self.play(Write(explanatory_text), run_time=0.5)
        self.wait(0.3)

        # Step 1: Standard BST deletion
        if root is None:
            sub_explanatory_text = Text(f"Value {value} not found in tree", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
            self.play(Write(sub_explanatory_text), run_time=0.5)
            self.wait(1)
            self.play(Unwrite(sub_explanatory_text), Unwrite(explanatory_text), run_time=0.5)
            return root

        # Search for the node to delete with animation
        current = root
        search_surr = DashedVMobject(SurroundingRectangle(current.node, color=ORANGE, buff=0, corner_radius=0.52))
        search_surr.set_z_index(3)
        
        search_explanatory_text = Text(f"Searching for {value}", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
        self.play(Create(search_surr), Write(search_explanatory_text), run_time=0.5)
        self.wait(0.3)
        
        # Perform the search animation
        while current.value != value:
            if value < current.value:
                direction_text = f"{value} < {current.value}, go left"
                next_node = current.left
            else:
                direction_text = f"{value} >= {current.value}, go right"
                next_node = current.right
            
            if next_node is None:
                break
                
            # Show direction and move search indicator
            self.play(Unwrite(search_explanatory_text), run_time=0.3)
            search_explanatory_text = Text(direction_text, font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
            self.play(
                search_surr.animate.move_to(next_node.node.get_center()),
                Write(search_explanatory_text),
                run_time=0.5
            )
            self.wait(0.3)
            
            current = next_node
        
        if current.value != value:
            # Node not found
            self.play(Unwrite(search_explanatory_text), run_time=0.3)
            search_explanatory_text = Text(f"Value {value} not found", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
            self.play(Write(search_explanatory_text), run_time=0.5)
            self.wait(1)
            self.play(Uncreate(search_surr), Unwrite(search_explanatory_text), Unwrite(explanatory_text), run_time=0.5)
            return root

        # Found the node
        self.play(Unwrite(search_explanatory_text), run_time=0.3)
        search_explanatory_text = Text(f"Found {value}!", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).next_to(explanatory_text, DOWN, buff=0.2)
        self.play(Write(search_explanatory_text), run_time=0.5)
        self.wait(0.5)
        
        # Clean up search animation
        self.play(Uncreate(search_surr), Unwrite(search_explanatory_text), run_time=0.5)

        # Now perform the actual deletion
        root = self._delete_node_recursive(root, value)
        
        self.wait(0.4)
        self.play(Unwrite(explanatory_text), run_time=0.5)
        
        return root

    def _delete_node_recursive(self, root: AVLNode, value):
        # Base case
        if root is None:
            return root

        # Recursive cases - find the node
        if value < root.value:
            root.left = self._delete_node_recursive(root.left, value)
            # Ensure left child is properly connected after potential rotation
            if root.left is not None:
                root.set_left()
        elif value > root.value:
            root.right = self._delete_node_recursive(root.right, value)
            # Ensure right child is properly connected after potential rotation
            if root.right is not None:
                root.set_right()
        else:
            # This is the node to delete
            has_left = root.left is not None
            has_right = root.right is not None
            
            # Highlight the node to be deleted
            nodeSurr = DashedVMobject(SurroundingRectangle(root.node, color=TEXTCOL, buff=0, corner_radius=0.52))
            nodeSurr.set_z_index(3)
            self.play(Create(nodeSurr), run_time=0.5)
            self.wait(0.2)
            
            if not has_left and not has_right:
                # Case 1: Leaf node
                sub_explanatory_text = Text(f"{value} is a leaf node - simply remove it", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).to_edge(UP, buff=0.2)
                self.play(Write(sub_explanatory_text), run_time=0.5)
                self.wait(1)
                
                # Remove the node from visual group
                if root in self.AVLnodeGroup:
                    self.AVLnodeGroup.remove(root)
                    self.nodeGroup.remove(root)
                
                self.play(FadeOut(root), FadeOut(nodeSurr), run_time=0.5)
                self.play(Unwrite(sub_explanatory_text), run_time=0.5)
                
                return None
                
            elif has_left and not has_right:
                # Case 2: Only left child
                left_child = root.left
                
                sub_explanatory_text = Text(f"{value} has only left child - replace with {left_child.value}", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).to_edge(UP, buff=0.2)
                self.play(Write(sub_explanatory_text), run_time=0.5)
                self.wait(1)
                
                # Move left child to parent's position
                left_child.node.clear_updaters()
                self.play(left_child.node.animate.move_to(root.node.get_center()), run_time=0.5)
                
                # Remove the node from visual group
                if root in self.AVLnodeGroup:
                    self.AVLnodeGroup.remove(root)
                    self.nodeGroup.remove(root)
                
                self.play(FadeOut(root.node), FadeOut(nodeSurr), run_time=0.5)
                self.play(Unwrite(sub_explanatory_text), run_time=0.5)
                
                return left_child
                
            elif not has_left and has_right:
                # Case 3: Only right child
                right_child = root.right
                
                sub_explanatory_text = Text(f"{value} has only right child - replace with {right_child.value}", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).to_edge(UP, buff=0.2)
                self.play(Write(sub_explanatory_text), run_time=0.5)
                self.wait(1)
                
                # Move right child to parent's position
                right_child.node.clear_updaters()
                self.play(right_child.node.animate.move_to(root.node.get_center()), run_time=0.5)
                
                # Remove the node from visual group
                if root in self.AVLnodeGroup:
                    self.AVLnodeGroup.remove(root)
                    self.nodeGroup.remove(root)
                
                self.play(FadeOut(root.node), FadeOut(nodeSurr), run_time=0.5)
                self.play(Unwrite(sub_explanatory_text), run_time=0.5)
                
                return right_child
                
            else:
                # Case 4: Two children - replace with successor
                successor = self.find_successor(root)
                
                if successor is None:
                    sub_explanatory_text = Text(f"Error: No successor found for {value}", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).to_edge(UP, buff=0.2)
                    self.play(Write(sub_explanatory_text), run_time=0.5)
                    self.wait(1)
                    self.play(Unwrite(sub_explanatory_text), FadeOut(nodeSurr), run_time=0.5)
                    return root
                
                sub_explanatory_text1 = Text(f"{value} has two children", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).to_edge(UP, buff=0.2)
                sub_explanatory_text2 = Text(f"Replace with successor {successor.value}", font=FONT, color=TEXTCOL, font_size=SWAP_FONT_SIZE).next_to(sub_explanatory_text1, DOWN, buff=0.2)
                
                self.play(Write(sub_explanatory_text1), Write(sub_explanatory_text2), run_time=0.5)
                
                # Highlight successor
                successor_surr = DashedVMobject(SurroundingRectangle(successor.node, color=GREEN, buff=0, corner_radius=0.52))
                successor_surr.set_z_index(3)
                self.play(Create(successor_surr), run_time=0.5)
                self.wait(1)
                
                # Create temporary text to show the replacement
                replacement_text = Text(str(successor.value), font=FONT, color=TEXTCOL, font_size=FSIZE)
                replacement_text.move_to(root.node.text.get_center())
                
                # Animate the value replacement
                self.play(
                    Transform(root.node.text, replacement_text),
                    run_time=0.5
                )
                
                # Replace the value in the node
                root.value = successor.value
                
                self.play(FadeOut(nodeSurr), run_time=0.5)
                
                # Clear the explanatory text before recursive call to avoid overlap
                self.play(Unwrite(sub_explanatory_text1), Unwrite(sub_explanatory_text2), run_time=0.3)
                
                # Delete the successor
                root.right = self._delete_node_recursive(root.right, successor.value)
                
                self.play(FadeOut(successor_surr), run_time=0.5)

        # Step 2: Update height and balance factor
        self.recalculate_balance_factors([root])
        
        # Step 3: Get balance factor
        balance = self.get_balance(root)
        
        # Step 4: Rebalance if needed
        if balance > 1:
            # Left heavy
            if self.get_balance(root.left) >= 0:
                # Left-Left case
                new_root = self.right_rotate(root)
                # Ensure proper reconnection
                self.reconnect_after_rotation(new_root)
                return new_root
            else:
                # Left-Right case
                root.left = self.left_rotate(root.left)
                # Reconnect left child after first rotation
                if root.left is not None:
                    root.set_left()
                new_root = self.right_rotate(root)
                # Ensure proper reconnection
                self.reconnect_after_rotation(new_root)
                return new_root
        
        if balance < -1:
            # Right heavy
            if self.get_balance(root.right) <= 0:
                # Right-Right case
                new_root = self.left_rotate(root)
                # Ensure proper reconnection
                self.reconnect_after_rotation(new_root)
                return new_root
            else:
                # Right-Left case
                root.right = self.right_rotate(root.right)
                # Reconnect right child after first rotation
                if root.right is not None:
                    root.set_right()
                new_root = self.left_rotate(root)
                # Ensure proper reconnection
                self.reconnect_after_rotation(new_root)
                return new_root
        
        return root

    def reconnect_after_rotation(self, node):
        """Ensure a node is properly connected after rotation"""
        if node is not None:
            node.node.clear_updaters()
            # The parent will call set_left() or set_right() when this method returns

    def insert_into_AVLTree(self, root, value):
        # Simplified insert for building initial tree
        new_node = AVLNode(value)
        new_node.move_to(ORIGIN)
        
        if root is None:
            self.nodeGroup.add(new_node)
            self.AVLnodeGroup.append(new_node)
            self.play(Create(new_node), run_time=0.1)
            return new_node
        
        root = self.insert(root, value)
        self.wait(0.05)
        self.play(self.nodeGroup.animate.center().shift(UP * 0.3), run_time=0.1)
        self.wait(0.05)
        
        return root

    def insert(self, node: AVLNode, value, is_left=False, parent_node: AVLNode = None):
        if node is None:
            new_node = AVLNode(value)
            if parent_node is not None:
                if is_left:
                    new_node.move_to(parent_node.leftPos.get_center())
                    parent_node.left = new_node
                    parent_node.set_left()
                else:
                    new_node.move_to(parent_node.rightPos.get_center())
                    parent_node.right = new_node
                    parent_node.set_right()
            
            self.nodeGroup.add(new_node)
            self.AVLnodeGroup.append(new_node)
            self.play(Create(new_node), run_time=0.1)
            return new_node

        if value < node.value:
            node.left = self.insert(node.left, value, is_left=True, parent_node=node)
        elif value > node.value:
            node.right = self.insert(node.right, value, is_left=False, parent_node=node)
        else:
            return node
        
        balance = self.get_balance(node)

        # Rebalancing
        if balance > 1 and value < node.left.value:
            return self.right_rotate(node)
        
        if balance < -1 and value > node.right.value:
            return self.left_rotate(node)
        
        if balance > 1 and value > node.left.value:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        
        if balance < -1 and value < node.right.value:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        
        return node
    
    def recalculate_balance_factors(self, nodes_to_update=None):
        if nodes_to_update is None:
            nodes_to_update = self.AVLnodeGroup
        
        for avl_node in nodes_to_update:
            old_balance = avl_node.balanceFactor.get_value()
            new_balance = self.get_balance(avl_node)
            if abs(old_balance - new_balance) > 0.001:
                avl_node.balanceFactor.set_value(new_balance)

    def build_tree_silently(self, root, value):
        """Build AVL tree without animations for initial setup"""
        if root is None:
            new_node = AVLNode(value)
            new_node.move_to(ORIGIN)
            self.nodeGroup.add(new_node)
            self.AVLnodeGroup.append(new_node)
            return new_node
        
        root = self.insert_silently(root, value)
        
        # Update balance factors without animation
        for avl_node in self.AVLnodeGroup:
            new_balance = self.get_balance(avl_node)
            avl_node.balanceFactor.set_value(new_balance)
        
        return root
    
    def insert_silently(self, node: AVLNode, value, is_left=False, parent_node: AVLNode = None):
        """Insert node without animations"""
        if node is None:
            new_node = AVLNode(value)
            if parent_node is not None:
                if is_left:
                    new_node.move_to(parent_node.leftPos.get_center())
                    parent_node.left = new_node
                    parent_node.set_left()
                else:
                    new_node.move_to(parent_node.rightPos.get_center())
                    parent_node.right = new_node
                    parent_node.set_right()
            
            self.nodeGroup.add(new_node)
            self.AVLnodeGroup.append(new_node)
            return new_node

        if value < node.value:
            node.left = self.insert_silently(node.left, value, is_left=True, parent_node=node)
        elif value > node.value:
            node.right = self.insert_silently(node.right, value, is_left=False, parent_node=node)
        else:
            return node
        
        balance = self.get_balance(node)

        # Rebalancing without animations
        if balance > 1 and value < node.left.value:
            return self.right_rotate_silent(node)
        
        if balance < -1 and value > node.right.value:
            return self.left_rotate_silent(node)
        
        if balance > 1 and value > node.left.value:
            node.left = self.left_rotate_silent(node.left)
            return self.right_rotate_silent(node)
        
        if balance < -1 and value < node.right.value:
            node.right = self.right_rotate_silent(node.right)
            return self.left_rotate_silent(node)
        
        return node
    
    def right_rotate_silent(self, y: AVLNode):
        """Right rotation without animation"""
        x = y.left
        T2 = x.right
        
        # Clear updaters
        if y.left is not None:
            y.left.node.clear_updaters()
        if x.right is not None:
            x.right.node.clear_updaters()
            
        y.node.clear_updaters()
        x.node.clear_updaters()

        # Update tree structure
        y.left = T2
        x.right = y

        # Move node to new position without animation
        y.node.move_to(x.rightPos.get_center())

        # Set up new relationships
        x.set_right()
        if T2 is not None:
            y.set_left()

        return x
    
    def left_rotate_silent(self, x: AVLNode):
        """Left rotation without animation"""
        y = x.right
        T2 = y.left
        
        # Clear updaters
        if x.right is not None:
            x.right.node.clear_updaters()
        if y.left is not None:
            y.left.node.clear_updaters()
            
        x.node.clear_updaters()
        y.node.clear_updaters()

        # Update tree structure
        x.right = T2
        y.left = x

        # Move node to new position without animation
        x.node.move_to(y.leftPos.get_center())

        # Set up new relationships
        y.set_left()
        if T2 is not None:
            x.set_right()

        return y
