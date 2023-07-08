# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#     W T D E     L A U N C H E R + +     C O N S T A N T S 
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
""" All constants used for the GHWT: DE Launcher++. """
# Import required modules.
import os as OS

# Version of the program.
VERSION = "2.2"
""" Version of the program. """

# Hash list page.
HASH_LIST = "https://gitgud.io/fretworks/ghwt-de-volatile/-/raw/master/GHWTDE/hashlist.dat"
""" The hash list for GHWT: DE. Used by the launcher to check for updates. """

# Original working directory.
OWD = OS.getcwd()
""" Original working directory. """

# Window title.
TITLE = f"GHWT: Definitive Edition Launcher++ - V{VERSION}"
""" Title of the launcher window. """

# Frame width and height defaults.
FRAME_WIDTH = 886
FRAME_HEIGHT = 650

# Default program variables.
BG_COLOR = "#181B25"
""" The global background color. """
MENU_HOVER = "#A5C9CA"
""" The color of the hover when mousing over the commands in the top menu bar. """
# MENU_HOVER = "#E7F6F2"
FG_COLOR = "#FFFFFF"
""" Text color. """
FONT = "Segoe UI"
""" The main text font everything. """
FONT_SIZE = 9
""" The main font size. """
FONT_INFO = (FONT, FONT_SIZE)
""" Tuple containing the various font information for the program. """
FONT_INFO_BOLD = (FONT, FONT_SIZE, 'bold')
""" Same info tuple as `FONT_INFO`, but for bold text. """
FONT_INFO_CODE = ("Consolas", 11)
""" Tuple contining font information for the INI Editor or any other code editor. """
FONT_INFO_HEADER = (FONT, 10)
""" Font information for headers (meant for more important/pronounced text). """
FONT_INFO_FOOTER = (FONT, 11)
""" Font information for the footer (text along the bottom of the program). """
TAB_WINDOW_WIDTH = FRAME_WIDTH
""" The width of the windows on the tabs. """
TAB_WINDOW_HEIGHT = FRAME_HEIGHT
""" The height of the windows on the tabs. """
HOVER_DELAY = 0.35
""" Time delay before tooltips appear, in seconds. """
TOOLTIP_WIDTH = 500
""" In pixels, the width of tooltips when hovering over the various options. """

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

# Backup strings for AspyrConfig.
ASPYR_INPUT_GUITAR_BACKUP = "GREEN 328 308 RED 221 YELLOW 340 BLUE 343 ORANGE 267 STAR 402 318 CANCEL 999 START 219 BACK 999 DOWN 231 400 UP 327 401 WHAMMY 310 LEFT 265 RIGHT 309 "
""" The default mapping string for `Keyboard_Guitar` in AspyrConfig.xml. """

ASPYR_INPUT_DRUMS_BACKUP = "GREEN 308 262 259 258 254 RED 252 236 227 313 YELLOW 322 305 232 331 BLUE 295 256 324 341 ORANGE 999 KICK 318 CANCEL 999 START 219 BACK 999 DOWN 231 UP 327 WHAMMY 999 "
""" The default mapping string for `Keyboard_Drum` in AspyrConfig.xml. """

ASPYR_INPUT_MIC_BACKUP = "GREEN 328 308 402 318 RED 221 YELLOW 340 BLUE 343 ORANGE 267 234 218 CANCEL 999 START 219 BACK 999 DOWN 400 231 UP 401 327 MIC_VOL_DOWN 273 "
""" The default mapping string for `Keyboard_Mic` in AspyrConfig.xml. """

ASPYR_INPUT_MENU_BACKUP = "GREEN 308 328 RED 221 YELLOW 340 BLUE 343 ORANGE 267 CANCEL 999 START 219 BACK 402 311 DOWN 400 231 UP 401 327 WHAMMY 310 KICK 318 LEFT 265 RIGHT 309 "
""" The default mapping string for `Keyboard_Menu` in AspyrConfig.xml. """