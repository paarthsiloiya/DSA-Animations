# Environment Configuration for DSA Animations
# This file contains all color and font configurations used across the animation files

from manim import *

# Frame Configuration
config.frame_width = 16
config.frame_height = 9

# Base Colors
BASECOL = ManimColor.from_hex("#ebe7f3")  # Light background color
TEXTCOL = ManimColor.from_hex("#000000")  # Black text color
SELCOL = ManimColor.from_hex("#7a5bae")   # Selection/highlight color
SORTCOL = ManimColor.from_hex("#4a2a90")  # Sort/action color

# Font Configuration
FONT = 'JetBrains Mono'

# Font Sizes
FSIZE = 40                      # Base font size
SWAP_FONT_SIZE = 38             # For "Insert!", "Delete!", "Swap!" etc.
EXPLANATORY_FONT_SIZE = 40      # For step-by-step explanations (standardized to 40)
POINTER_FONT_SIZE = 28          # For pointer labels, "i", "j", "Min", etc.

# Specialized Font Sizes
ADDRESS_FONT_SIZE = 25          # For address displays in Arrays
SELF_ADDRESS_FONT_SIZE = 21     # For self address in LinkedList
NEXT_ADDRESS_FONT_SIZE = 25     # For next address in LinkedList
VALUE_FONT_SIZE = 90            # For large value displays in LinkedList
WEIGHT_FONT_SIZE = 25           # For weight displays in Graphs
DEGREE_FONT_SIZE = 17           # For degree displays in Graphs
INTERVAL_FSIZE = 40             # For interval scheduling in Greedy

# Font Colors
SWAP_FONT_COLOR = SORTCOL           # For swap/action text color
EXPLANATORY_FONT_COLOR = TEXTCOL    # For explanatory text color
POINTER_FONT_COLOR = SORTCOL        # For pointer text color

# Node and Edge Colors
NODE_COL = BASECOL              # Node background color
EDGE_COL = SELCOL               # Edge color

# Element Colors
ELEMENT_BG = BASECOL            # Element background (Stack-Queue)

# Layout and Positioning
LAYOT_SCALE = 2.4               # Layout scale for graphs
NODE_WIDTH = 1.6                # Node width for LinkedList

# Positioning Constants
BOTTOM_STACK_POS = (0, -2.4, 0)    # Bottom stack position
RIGHT_QUEUE_POS = (2.3, 0, 0)      # Right queue position

# Random Seed Settings (commented out - set individually in files if needed)
# random.seed(30)   # Used in Arrays.py
# random.seed(32)   # Used in Trees.py, LinkedList.py, Stack-Queue.py, AVLTree.py, Greedy.py
