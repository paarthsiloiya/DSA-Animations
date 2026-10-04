import logging

from env_config import *
from manim import *

logger = logging.getLogger(__name__)


class BTreeElement(VGroup):
    def __init__(self, t: int, leaf: bool):
        super().__init__()
        self.keys: list[int | None] = [None] * (2 * t - 1)
        self.C: list[BTreeElement | None] = [None] * (2 * t)
        self.t: int = t
        self.n: int = 0
        self.leaf: bool = leaf

        self.key_vgroup = VGroup()
        self.SurrNode = SurroundingRectangle(self.key_vgroup, color=TEXTCOL, buff=0.3, stroke_width=2)
        self.children_vgroup = VGroup()

        self.childHooks = VGroup()
        self.parentHook: Dot|None = None

        self.connection_lines = VGroup()

        self.add(
            self.key_vgroup,
            self.SurrNode,
            self.children_vgroup,
            self.childHooks,
            self.connection_lines
        )

    def add_key(self, k: int, index: int):
        """Add a key at the specified index and update visual representation"""
        
        if self.n < (2 * self.t - 1):
            self.keys[index] = k
            self.n += 1
            self.rebuild_visual()
        else:
            error_msg = f"Cannot add key {k}, node is full (n={self.n}, max={2 * self.t - 1})"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
    def remove_key(self, index: int):
        """Remove a key at the specified index and update visual representation"""
        
        if 0 <= index < self.n:
            self.keys[index] = None
            self.n -= 1
            
            # Shift keys to fill the gap
            for i in range(index, self.n):
                self.keys[i] = self.keys[i + 1]
                self.keys[i + 1] = None
            
            self.rebuild_visual()
        else:
            error_msg = f"Index {index} out of bounds for key removal (n={self.n})"
            logger.error(error_msg)
            raise IndexError(error_msg)
    
    def rebuild_visual(self):
        """Rebuild the visual representation based on current keys"""
        logger.debug("=== REBUILD_VISUAL OPERATION ===")
        logger.debug(f"Rebuilding visual for node with keys: {[k for k in self.keys if k is not None]}")
        logger.debug(f"Node details: n={self.n}, leaf={self.leaf}")
        
        prev_pos = self.key_vgroup.get_center()
        # Clear existing visual elements
        self.key_vgroup.remove(*self.key_vgroup.submobjects)
        
        # Add visual elements for all current keys
        for i in range(self.n):
            if self.keys[i] is not None:
                key_text = Text(str(self.keys[i]), font=FONT, font_size=FSIZE, color=TEXTCOL)
                self.key_vgroup.add(key_text)
                logger.debug(f"Added visual element for key {self.keys[i]} at position {i}")
        
        # Arrange and update rectangle
        self.key_vgroup.arrange(RIGHT, buff=0.6).move_to(prev_pos)
        self.SurrNode.become(SurroundingRectangle(self.key_vgroup, color=TEXTCOL, buff=0.3, stroke_width=2))

        start = self.SurrNode.get_corner(DL)

        # Ensure we have n+1 child hooks (for n keys, we need n+1 children)
        required_hooks = self.n + 1
        current_hooks = len(self.childHooks)
        
        logger.debug(f"Child hooks: required={required_hooks}, current={current_hooks}")
        
        if current_hooks < required_hooks:
            # Add missing hooks
            for i in range(required_hooks - current_hooks):
                dot = Dot(start, radius=0.1, color=LIGHT_PINK, fill_opacity=0)
                self.childHooks.add(dot)
            logger.debug(f"Added {required_hooks - current_hooks} child hooks")
        elif current_hooks > required_hooks:
            # Remove extra hooks
            for i in range(current_hooks - required_hooks):
                if self.childHooks.submobjects:
                    self.childHooks.remove(self.childHooks.submobjects[-1])
            logger.debug(f"Removed {current_hooks - required_hooks} child hooks")

        # Arrange hooks evenly across the bottom of the node
        if self.childHooks.submobjects:
            self.childHooks.arrange(RIGHT, buff=0.65).move_to(self.SurrNode.get_bottom())

        if self.parentHook is None:
            self.parentHook = Dot(self.SurrNode.get_top(), radius=0.1, color=BLUE, fill_opacity=0)
            self.add(self.parentHook)
            logger.debug("Created parent hook")
        else:
            self.parentHook.move_to(self.SurrNode.get_top())
            logger.debug("Updated parent hook position")

        if not self.leaf:
            # Only arrange children that actually exist in the C array
            existing_children = []
            for i in range(self.n + 1):
                if self.C[i] is not None:
                    existing_children.append(self.C[i])
                    logger.debug(f"Found child at index {i} with keys: {[k for k in self.C[i].keys if k is not None]}")
            
            logger.debug(f"Total existing children: {len(existing_children)}")
            
            # Clear children_vgroup and add only the actual children
            self.children_vgroup.remove(*self.children_vgroup.submobjects)
            for child in existing_children:
                if child not in self.children_vgroup.submobjects:
                    self.children_vgroup.add(child)
            
            self.children_vgroup.arrange(RIGHT, buff=2)
            self.children_vgroup.next_to(self.SurrNode.get_bottom(), DOWN, buff=0.6)

            # Clear existing connection lines
            self.connection_lines.remove(*self.connection_lines.submobjects)

            # Create connection lines to child nodes
            for i, child in enumerate(existing_children):
                if i < len(self.childHooks):
                    line = Line(
                        self.childHooks[i].get_center(), 
                        child.parentHook.get_center(), 
                        color=TEXTCOL,
                        stroke_width=2
                    )
                    self.connection_lines.add(line)
                    logger.debug(f"Created connection line to child {i}")
        
        logger.debug(f"Visual rebuild completed for node with {self.n} keys")


    def insert_non_full(self, k: int):
        i = self.n - 1
        if self.leaf:
            while i >= 0 and self.keys[i] > k:
                logger.debug(f"Shifting key {self.keys[i]} from position {i} to {i+1}")
                self.keys[i + 1] = self.keys[i]
                i -= 1
            
            target_index = i + 1
            self.add_key(k, target_index)
        else:
            while i >= 0 and self.keys[i] > k:
                i -= 1
            i += 1

            if self.C[i].n == (2 * self.t - 1):
                logger.warning(f"Child at index {i} is full (n={self.C[i].n}), splitting required")
                self.splitChild(i, self.C[i])
                if self.keys[i] < k:
                    i += 1

            self.C[i].insert_non_full(k)
            # Only rebuild this node's visual, don't rebuild children
            # The child will rebuild itself when the key is added

    def splitChild(self, i:int, y:'BTreeElement'):
        z = BTreeElement(y.t, y.leaf)
        z.n = self.t - 1
        
        # Store the middle key that will be promoted BEFORE we modify y
        promoted_key = y.keys[self.t - 1]
        
        # Copy keys from y to z
        for j in range(z.n):
            z.keys[j] = y.keys[j + self.t]
            logger.debug(f"  Copied key {z.keys[j]} from y[{j + self.t}] to z[{j}]")

        # Copy children if not leaf
        if not y.leaf:
            for j in range(self.t):
                z.C[j] = y.C[j + self.t]
                if z.C[j] is not None:
                    z_child_keys = [key for key in z.C[j].keys if key is not None]
                    logger.debug(f"  Copied child with keys {z_child_keys} from y.C[{j + self.t}] to z.C[{j}]")
                # Clear the child pointers that were moved to z from y
                y.C[j + self.t] = None
        
        # Clear the keys that were moved to z from y (including the promoted key)
        for j in range(self.t - 1, 2 * self.t - 1):
            if y.keys[j] is not None:
                logger.debug(f"  Clearing key {y.keys[j]} from y[{j}]")
            y.keys[j] = None
            
        y.n = self.t - 1
        
        # Shift children in parent to make room for z
        for j in range(self.n, i, -1):
            self.C[j + 1] = self.C[j]
            if self.C[j + 1] is not None:
                child_keys = [key for key in self.C[j + 1].keys if key is not None]
                logger.debug(f"  Moved child with keys {child_keys} from position {j} to {j + 1}")
        
        self.C[i + 1] = z

        # Shift keys in parent to make room for promoted key
        for j in range(self.n - 1, i - 1, -1):
            self.keys[j + 1] = self.keys[j]
            logger.debug(f"  Moved key {self.keys[j + 1]} from position {j} to {j + 1}")
        
        # Use the stored promoted key instead of accessing y.keys[self.t - 1]
        self.keys[i] = promoted_key

        self.n += 1

        
        # Rebuild visuals for all affected nodes
        y.rebuild_visual()
        z.rebuild_visual()
        
        # Add both children to the children_vgroup if they're not already there
        if y not in self.children_vgroup.submobjects:
            self.children_vgroup.add(y)
        if z not in self.children_vgroup.submobjects:
            self.children_vgroup.add(z)
        
        # Rebuild this node's visual to update the promoted key and connections
        self.rebuild_visual()
        

class BTree(VGroup):
    def __init__(self, t: int):
        super().__init__()
        self.root: None | BTreeElement = None
        self.t: int = t


    def insert(self, k: int):
        if self.root is None:
            self.root = BTreeElement(self.t, True)
            self.root.add_key(k, 0)
            self.add(self.root)
        else:
            # If root is full, we need to check if we actually need to split
            if self.root.n == 2 * self.t - 1:
                if self.root.leaf:
                    # Root is a full leaf - must split
                    logger.warning("Root is full leaf, must create new root and split")
                    s = BTreeElement(self.t, False)
                    old_root = self.root
                    
                    self.remove(old_root)
                    
                    s.C[0] = old_root
                    s.children_vgroup.add(old_root)
                    
                    s.splitChild(0, old_root)
                    
                    i = 0
                    if s.keys[0] < k:
                        i += 1

                    s.C[i].insert_non_full(k)
                    
                    self.root = s
                    self.add(s)
                else:
                    # Root is full internal node - check if target child would need splitting
                    
                    # Find which child the key would go to
                    i = self.root.n - 1
                    while i >= 0 and self.root.keys[i] > k:
                        i -= 1
                    i += 1
                    
                    target_child = self.root.C[i]
                    
                    if target_child.n == (2 * self.t - 1):
                        # Target child is full, so we need to split it, but root has no space
                        # Therefore we must split root first
                        logger.warning("Target child is full and root has no space, must split root first")
                        s = BTreeElement(self.t, False)
                        old_root = self.root
                        
                        self.remove(old_root)
                        
                        s.C[0] = old_root
                        s.children_vgroup.add(old_root)
                        
                        s.splitChild(0, old_root)
                        
                        # Now find the correct child in the new structure
                        i = 0
                        if s.keys[0] < k:
                            i += 1

                        s.C[i].insert_non_full(k)
                        
                        self.root = s
                        self.add(s)
                    else:
                        # Target child has space, so we can insert without splitting root
                        self.root.insert_non_full(k)
            else:
                self.root.insert_non_full(k)
        

class BTreeScene(Scene):
    def construct(self):
        t = 2  # Minimum degree
        btree = BTree(t)

        self.add(btree)

        keys = range(1, 11) # Example keys to insert
        
        for key in keys:
            btree.insert(key)
            self.wait(2)
        
