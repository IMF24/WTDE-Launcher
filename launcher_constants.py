""" All constants used for the GHWT: DE Launcher++. """
# Import required modules.
import os as OS

# Version of the program.
VERSION = "2.0 Alpha Version 1"

# Original working directory.
OWD = OS.getcwd()

# Window title.
TITLE = f"GHWT: Definitive Edition Launcher++ - V{VERSION}"

# Frame width and height defaults.
FRAME_WIDTH = 886
FRAME_HEIGHT = 650

# Default program variables.
BG_COLOR = "#181B25"
BUTTON_BG = "#A5C9CA"
BUTTON_FG = "#000000"
BUTTON_ACTIVE_BG = "#E7F6F2"
BUTTON_ACTIVE_FG = "#000000"
FG_COLOR = "#FFFFFF"
FONT = "Segoe UI"
FONT_SIZE = 9
FONT_INFO = (FONT, FONT_SIZE)
FONT_INFO_HEADER = (FONT, 10)
FONT_INFO_FOOTER = (FONT, 11)
TAB_WINDOW_WIDTH = FRAME_WIDTH
TAB_WINDOW_HEIGHT = FRAME_HEIGHT
HOVER_DELAY = 0.35
TOOLTIP_WIDTH = 500

# Input field constants.
INPUT_Y_OFFSET = 3
INPUT_ENTRY_WIDTH = 25

# Allow entry & button focus for the Input Settings.
ALLOW_INPUT_ENTRY_FOCUS = False
ALLOW_ADD_BUTTON_FOCUS = False
ALLOW_CLEAR_BUTTON_FOCUS = False

# Add & Clear button text.
ADD_BUTTON_TEXT = "Add"
CLEAR_BUTTON_TEXT = "Clear"