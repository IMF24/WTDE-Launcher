# ================================================================================================================= #
#                                                                                                                   #
#  __          _________ _____  ______     _              _    _ _   _  _____ _    _ ______ _____                   #
#  \ \        / /__   __|  __ \|  ____|   | |        /\  | |  | | \ | |/ ____| |  | |  ____|  __ \  _     _         #
#   \ \  /\  / /   | |  | |  | | |__      | |       /  \ | |  | |  \| | |    | |__| | |__  | |__) || |_ _| |_       #
#    \ \/  \/ /    | |  | |  | |  __|     | |      / /\ \| |  | | . ` | |    |  __  |  __| |  _  /_   _|_   _|      #
#     \  /\  /     | |  | |__| | |____    | |____ / ____ \ |__| | |\  | |____| |  | | |____| | \ \ |_|   |_|        #
#      \/  \/      |_|  |_____/|______|   |______/_/    \_\____/|_| \_|\_____|_|  |_|______|_|  \_\                 #
#                                                                                                                   #
#          Coded by IMF24                Guitar Hero World Tour: Definitive Edition by Fretworks EST. 2021          #
#                                                                                                                   #
#                                    Updater Coded by Zedek the Plague Doctor ™                                     #
# ================================================================================================================= #
# Import required modules.
from tkinter import *
from tkinter import ttk as TTK, messagebox as MSG, filedialog as FD
from tkinter.font import *
from tktooltip import ToolTip
from launcher_functions import *
from launcher_constants import *
from PIL import Image, ImageTk
import webbrowser as WEB
import os as OS
import sys as SYS

debug_add_entry("[init] All modules imported!")

# ===========================================================================================================
# Save & Load Config Settings
# 
# The functions for handling the saving and loading of configuration settings.
# ===========================================================================================================
# Save and Load Configuration
# ===========================================================================================================
# Load WTDE config settings.
def wtde_load_config() -> None:
    """ Loads all configuration settings from GHWTDE.ini and AspyrConfig.xml. """
    # ====================================================================
    # GHWTDE.ini Settings
    # ====================================================================
    # Read our GHWTDE.ini file.
    OS.chdir(wtde_find_config())
    config.read("GHWTDE.ini")

    # ==================================
    # General Settings
    # ==================================
    GeneralSettings.richPresence.set(config.get("Config", "RichPresence"))
    GeneralSettings.allowHolidays.set(config.get("Config", "AllowHolidays"))
    GeneralSettings.whammyPitchShift.set(config.get("Audio", "WhammyPitchShift"))

    GeneralSettings.useCareerOption.set(config.get("Config", "UseCareerOption"))
    GeneralSettings.useQuickplayOption.set(config.get("Config", "UseQuickplayOption"))
    GeneralSettings.useHeadToHeadOption.set(config.get("Config", "UseHeadToHeadOption"))
    GeneralSettings.useOnlineOption.set(config.get("Config", "UseOnlineOption"))
    GeneralSettings.useMusicStudioOption.set(config.get("Config", "UseMusicStudioOption"))
    GeneralSettings.useCAROption.set(config.get("Config", "UseCAROption"))
    GeneralSettings.useOptionsOption.set(config.get("Config", "UseOptionsOption"))
    GeneralSettings.useQuitOption.set(config.get("Config", "UseQuitOption"))

    # ==================================
    # Input Settings
    # ==================================
    InputSettings.inputMicSettingsADelayEntry.insert(0, config.get('Audio', 'VocalAdjustment'))

    # ==================================
    # Graphics Settings
    # ==================================
    GraphicsSettings.useNativeRes.set(config.get('Graphics', 'UseNativeRes'))

    GraphicsSettings.disableVSync.set(config.get('Graphics', 'DisableVSync'))
    fps_limit_update()

    # ==================================
    # Auto Launch Settings
    # ==================================
    autoLaunchEnabled.set(config.get('AutoLaunch', 'Enabled'))
    AutoLaunch.auto_update_status()

    AutoLaunch.AutoLaunch_General.autoVenue.set(auto_get_venue(config.get('AutoLaunch', 'Venue')))

    AutoLaunch.AutoLaunch_General.autoSongID.set(config.get('AutoLaunch', 'Song'))

    # ====================================================================
    # AspyrConfig Settings
    # ====================================================================
    # Now we'll read settings that are stored in AspyrConfig.

    # ==================================
    # Input Settings
    # ==================================
    # Mic Video Delay
    InputSettings.inputMicSettingsVDelayEntry.insert(0, aspyr_get_string("Options.VocalsVisualLag"))

    # ==================================
    # Graphics Settings
    # ==================================
    # Resolution
    GraphicsSettings.graphicsResHEntry.insert(0, aspyr_get_string("Video.Height"))
    GraphicsSettings.graphicsResWEntry.insert(0, aspyr_get_string("Video.Width"))
    native_res_update()

# ===========================================================================================================
# Script-Specific Functions
# 
# These are functions that would otherwise not work in the scope of the launcher_functions module.
# ===========================================================================================================
# Update Resolution when Use Native Res is checked.
def native_res_update() -> None:
    """ Update the Resolution widgets when the Use Native Res Checkbutton is turned ON or OFF. """
    # Update the widgets.
    if (GraphicsSettings.useNativeRes.get() == '1'): status = 'disabled'
    else: status = 'normal'
    widgetList = [GraphicsSettings.graphicsResLabel, GraphicsSettings.graphicsResXLabel, GraphicsSettings.graphicsResWEntry, GraphicsSettings.graphicsResHEntry]
    for (widget) in (widgetList): widget.config(state = status)

# Update FPS Limit when Use Vertical Sync is checked.
def fps_limit_update() -> None:
    """ Update the FPS Limit widgets when the Use Vertical Sync Checkbutton is turned ON or OFF. """
    # Update the widgets.
    if (GraphicsSettings.disableVSync.get() == '1'): status = 'normal'
    else: status = 'disabled'
    widgetList = [GraphicsSettings.graphicsFPSLabel, GraphicsSettings.graphicsFPSOptions]
    for (widget) in (widgetList): widget.config(state = status)

# ===========================================================================================================
# Root Window Setup
# 
# Sets up the root window of the GHWT: DE Launcher++.
# ===========================================================================================================
# Set up root window.
debug_add_entry("[init] Setting up Tk widget root...")

root = Tk()
root.title(TITLE)
root.iconbitmap(resource_path("res/icon.ico"))
root.geometry(f"1080x720+{get_screen_resolution()[0] // 5}+{get_screen_resolution()[1] // 8}")
root.resizable(False, False)

debug_add_entry("[init] Tk widget root set up!")
debug_add_entry("!!!--- ENTERING TK SETUP ---!!!")

# Image constants.
debug_add_entry("Adding image constants...", 1)

# img = Image.open(resource_path("res/bg.png"))
# resizedImage = img.resize((2048, 1120), Image.ADAPTIVE)
# IMAGE_BG = ImageTk.PhotoImage(resizedImage)
class ImageConst():
    """
    Image constants class.
    """
    IMAGE_BG = ImageTk.PhotoImage(Image.open(resource_path("res/bg.png")))
    debug_add_entry(f"(const) IMAGE_BG has relative path {resource_path('res/bg.png')}", 1)

    WTDE_LOGO = ImageTk.PhotoImage(Image.open(resource_path("res/logo.png")))
    debug_add_entry(f"(const) WTDE_LOGO has relative path {resource_path('res/logo.png')}", 1)

    WTDE_LOGO_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icon_192.png")))
    debug_add_entry(f"(const) WTDE_LOGO_ICON has relative path {resource_path('res/icon_192.png')}", 1)

    WTDE_LOGO_SMALLER = ImageTk.PhotoImage(Image.open(resource_path("res/logo_smaller.png")))
    debug_add_entry(f"(const) WTDE_LOGO_SMALLER has relative path {resource_path('res/logo_smaller.png')}", 1)

    NEWS_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/news_icon.png")))
    debug_add_entry(f"(const) NEWS_ICON has relative path {resource_path('res/icons/news_icon.png')}", 1)

    MODS_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/mods_icon.png")))
    debug_add_entry(f"(const) MODS_ICON has relative path {resource_path('res/icons/mods_icon.png')}", 1)

    GENERAL_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/general_icon.png")))
    debug_add_entry(f"(const) GENERAL_ICON has relative path {resource_path('res/icons/general_icon.png')}", 1)

    INPUT_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/input_icon.png")))
    debug_add_entry(f"(const) INPUT_ICON has relative path {resource_path('res/icons/input_icon.png')}", 1)

    GRAPHICS_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/graphics_icon.png")))
    debug_add_entry(f"(const) GRAPHICS_ICON has relative path {resource_path('res/icons/graphics_icon.png')}", 1)

    AUTO_LAUNCH_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/auto_launch_icon.png")))
    debug_add_entry(f"(const) AUTO_LAUNCH_ICON has relative path {resource_path('res/icons/auto_launch_icon.png')}", 1)

    BAND_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/band_icon.png")))
    debug_add_entry(f"(const) BAND_ICON has relative path {resource_path('res/icons/band_icon.png')}", 1)

    DEBUG_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/debug_icon.png")))
    debug_add_entry(f"(const) DEBUG_ICON has relative path {resource_path('res/icons/debug_icon.png')}", 1)

    CREDITS_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/credits_icon.png")))
    debug_add_entry(f"(const) CREDITS_ICON has relative path {resource_path('res/icons/credits_icon.png')}", 1)

    CREDITS_TABLE_IMAGE = ImageTk.PhotoImage(Image.open(resource_path("res/credits_table.png")))
    debug_add_entry(f"(const) CREDITS_TABLE_IMAGE has relative path {resource_path('res/icons/credits_table.png')}", 1)

    INPUT_GUITAR_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/guitar_bass.png")))
    debug_add_entry(f"(const) INPUT_GUITAR_ICON has relative path {resource_path('res/icons/guitar_bass.png')}", 1)

    INPUT_DRUMS_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/drums.png")))
    debug_add_entry(f"(const) INPUT_DRUMS_ICON has relative path {resource_path('res/icons/drums.png')}", 1)

    INPUT_MIC_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/vocals.png")))
    debug_add_entry(f"(const) INPUT_MIC_ICON has relative path {resource_path('res/icons/vocals.png')}", 1)

    INPUT_MENU_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/keys.png")))
    debug_add_entry(f"(const) INPUT_MENU_ICON has relative path {resource_path('res/icons/keys.png')}", 1)

# Widget canvas.
debug_add_entry("Adding Canvas widget widgetCanvas...", 1)

widgetCanvas = Canvas(root, width = 2048, height = 1120)
widgetCanvas.place(x = -10, y = -10)
widgetCanvas.create_image(0, 0, image = ImageConst.IMAGE_BG, anchor = 'nw')

# Top panel: WTDE logo and run button.
widgetCanvas.create_image(4, 4, image = ImageConst.WTDE_LOGO_ICON, anchor = 'nw')

# Credits text and latest WTDE version information.
CREDITS_TEXT = "Made by IMF24, WTDE by Fretworks, Updater by Zedek the Plague Doctor \u2122"
VERSION_TEXT = f"Version {VERSION} || WTDE Latest Version: {wtde_latest_version()}"

# Add these strings as text onto the canvas.
widgetCanvas.create_text(18, 724, text = CREDITS_TEXT, fill = FG_COLOR, font = FONT_INFO_FOOTER, justify = 'left', anchor = 'sw')
widgetCanvas.create_text(1080, 724, text = VERSION_TEXT, fill = FG_COLOR, font = FONT_INFO_FOOTER, justify = 'right', anchor = 'se')

debug_add_entry("Canvas widget widgetCanvas created; text and images applied", 1)

# Main tabbed options through TTK's Notebook widget.
debug_add_entry("Setting up ttk.Notebook widget wtdeOptionsRoot...", 1)

wtdeOptionsRoot = TTK.Notebook(root)
wtdeOptionsRoot.place(x = 186, y = 0)

# Various WTDE commands.
# Edit the background color on the buttons and notebook.
TTK.Style().configure("TButton", background = BG_COLOR)
TTK.Style().configure("TNotebook", background = '#0B101F', tabposition = 'nw')
TTK.Style().configure("TCheckbutton", background = BG_COLOR, foreground = FG_COLOR)
TTK.Style().configure("TMenubutton", width = 20)
TTK.Style().configure("TCombobox", background = BG_COLOR)

# Save configuration and start WTDE.
wtdeStartGame = TTK.Button(root, text = "Save & Run WTDE", width = 25, padding = 10)
wtdeStartGame.place(x = 4, y = 185)

wtdeSaveConfig = TTK.Button(root, text = "Save Configuration", width = 25, padding = 10)
wtdeSaveConfig.place(x = 4, y = 235)

# Are we connected to the internet?
if (is_connected("https://cdn.discordapp.com/attachments/872794777060515890/1044075617307590666/Updater_Main_1_0_3.zip")):
    wtdeUpdateButtonTipText = "Update WTDE to the latest version and verify your installation's integrity."
    stateToUpdateTo = 'normal'
else:
    wtdeUpdateButtonTipText = "Can't update WTDE! No internet connection was found."
    stateToUpdateTo = 'disabled'

wtdeUpdateGame = TTK.Button(root, text = "Update WTDE", width = 25, padding = 10, command = wtde_run_updater, state = stateToUpdateTo)
wtdeUpdateGame.place(x = 4, y = 285)

wtdeOpenMods = TTK.Button(root, text = "Open Mods Folder", width = 25, padding = 10, command = open_mods_folder)
wtdeOpenMods.place(x = 4, y = 335)

wtdeMakeShortcut = TTK.Button(root, text = "Make Desktop Shortcut", width = 25, padding = 10, command = wtde_create_lnk)
wtdeMakeShortcut.place(x = 4, y = 385)

wtdeBackUpSave = TTK.Button(root, text = "Back Up Save", width = 25, padding = 10, command = wtde_backup_save)
wtdeBackUpSave.place(x = 4, y = 435)

ToolTip(wtdeStartGame, msg = "Save your configuration settings and launch GHWT: DE.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(wtdeSaveConfig, msg = "Save your configuration settings.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(wtdeUpdateGame, msg = wtdeUpdateButtonTipText, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(wtdeOpenMods, msg = "Open your Mods folder.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(wtdeMakeShortcut, msg = "Makes a shortcut to GHWT: DE on the desktop.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(wtdeBackUpSave, msg = "Makes a backup of your GHWT: DE save file, with the date and time of backup in the file name.\n\nAll save data backups can be found in the Save Backups folder in your save & config file folder.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

# ===========================================================================================================
# Tab Frame Setup
# 
# These are the frames used in the window that contain the things shown in the tabs.
# ===========================================================================================================
# Set up tab frames.
debug_add_entry("Creating tab frames and packing them (fill = 'both', expand = 1)...", 1)

wtdeOptionsNews = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsMods = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsGeneral = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsInput = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsGraphics = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsBand = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsAutoLaunch = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsDebug = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsCredits = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)

# Pack tab frames into the notebook.
wtdeOptionsNews.pack(fill = 'both', expand = 1)
wtdeOptionsMods.pack(fill = 'both', expand = 1)
wtdeOptionsGeneral.pack(fill = 'both', expand = 1)
wtdeOptionsInput.pack(fill = 'both', expand = 1)
wtdeOptionsGraphics.pack(fill = 'both', expand = 1)
wtdeOptionsBand.pack(fill = 'both', expand = 1)
wtdeOptionsAutoLaunch.pack(fill = 'both', expand = 1)
wtdeOptionsDebug.pack(fill = 'both', expand = 1)
wtdeOptionsCredits.pack(fill = 'both', expand = 1)

debug_add_entry("Adding frames as tabs...", 1)

# Add the tabs into the notebook.
wtdeOptionsRoot.add(wtdeOptionsNews, text = " GHWT: DE News", image = ImageConst.NEWS_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsMods, text = " Mods", image = ImageConst.MODS_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsGeneral, text = " General", image = ImageConst.GENERAL_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsInput, text = " Input", image = ImageConst.INPUT_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsGraphics, text = " Graphics", image = ImageConst.GRAPHICS_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsBand, text = " Band", image = ImageConst.BAND_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsAutoLaunch, text = " Auto Launch", image = ImageConst.AUTO_LAUNCH_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsDebug, text = " Debug", image = ImageConst.DEBUG_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsCredits, text = " Credits", image = ImageConst.CREDITS_ICON, compound = 'left')

debug_add_entry("ttk.Notebook widget wtdeOptionsRoot created and 9 child tabs were added!", 1)

# ===========================================================================================================
# GHWT: DE News
# 
# Used to inform the user about any and all news about GHWT: DE.
# ===========================================================================================================
# Main NewsTab class.
class NewsTab():
    """
    News tab class.
    \n
    This class is responsible for adding the widgets to the GHWT: DE News tab.
    """
    # Title text with the WTDE logo and purpose of the tab.
    WTDE_NEWS_TITLE_TEXT = "    Want some of the latest news for GHWT: DE? Have a look for yourself here!\n\n    This page attempts to be as up-to-date as possible. Stay tuned for more!"
    newsTitleLabel = Label(wtdeOptionsNews, text = WTDE_NEWS_TITLE_TEXT, image = ImageConst.WTDE_LOGO_SMALLER, compound = 'left', bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO_HEADER, justify = 'left')
    newsTitleLabel.pack(fill = 'x', anchor = 'n')

    # Add a white line (TTK Separator widget).
    newsSeparator = TTK.Separator(wtdeOptionsNews, orient = 'horizontal')
    newsSeparator.pack(fill = 'x')

    # This "label" is actually a Text widget, using
    newsLabel = Text(wtdeOptionsNews, bg = BG_COLOR, fg = FG_COLOR, relief = 'flat', font = FONT_INFO_HEADER, wrap = 'word')
    newsLabel.pack(side = 'left', fill = 'both', expand = 1)
    newsLabel.insert(END, wtde_get_news())
    newsLabel.configure(state = 'disabled')

    # Add a scrollbar to the text box.
    newsScroll = TTK.Scrollbar(wtdeOptionsNews, orient = 'vertical', command = newsLabel.yview)
    newsScroll.pack(side = 'right', fill = 'y')
    newsLabel.config(yscrollcommand = newsScroll.set)

# Execute tab code.
NewsTab()

# ===========================================================================================================
# Mods Settings
# 
# Allows the user to manage and install mods for GHWT: DE.
# ===========================================================================================================
# Main ModsSettings class.
class ModsSettings():
    """
    Mods settings class.
    \n
    This is the class responsible for the mod manager and other widgets.
    """
    # Title text with the purpose of the tab.
    MODS_SETTINGS_TITLE_TEXT = "Mods Settings: Install and manage mods for GHWT: DE.\nHover over any option to see what it does!"
    modsTitleLabel = Label(wtdeOptionsMods, text = MODS_SETTINGS_TITLE_TEXT, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO_HEADER, justify = 'left', anchor = 'w')
    modsTitleLabel.pack(fill = 'x', anchor = 'nw')

    # TODO (maybe): Might add pages to where people can get mods for GHWT: DE.
    # WTDE_SITE_TIP = "Open the GHWT: DE website."
    # NEXUS_SITE_TIP = "Open the Nexus Mods page for GHWT."
    # DRIVE_SITE_TIP = "Open the Google Drive repository for GHWT: DE."

    # WEB_TIP_DISALLOWED = "No internet connection detected! Is the internet/Wi-Fi on?"

    # Mod Manager
    modsManagerLabel = Label(wtdeOptionsMods, text = "Mod Manager:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO_HEADER, justify = 'left', anchor = 'w')
    modsManagerLabel.pack(anchor = 'nw', pady = 5)

    # Command Frame
    modManagerCommandsFrame = Frame(wtdeOptionsMods, bg = BG_COLOR, relief = 'flat')
    modManagerCommandsFrame.pack(fill = 'x')

    # Install Mod
    modManagerInstallMod = TTK.Button(modManagerCommandsFrame, text = "Install Mods", width = 20, takefocus = False, command = wtde_ask_install_mods)
    modManagerInstallMod.grid(row = 0, column = 0, padx = 5)
    ToolTip(modManagerInstallMod, msg = "Install mods into GHWT: DE.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Refresh Mods List
    modManagerRefresh = TTK.Button(modManagerCommandsFrame, text = "Refresh List", width = 20, takefocus = False, command = lambda: wtde_get_mods(ModsSettings.modTree, ModsSettings.modManagerStatus))
    modManagerRefresh.grid(row = 0, column = 1, padx = 5)
    ToolTip(modManagerRefresh, msg = "Refresh the list of installed mods.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Mod Manager Setup
    modManagerFrame = Frame(wtdeOptionsMods, bg = BG_COLOR, relief = 'flat')
    modManagerFrame.pack(fill = 'both', expand = 1, pady = 5)

    # Create our table of information.
    modTree = TTK.Treeview(modManagerFrame)

    # Add columns to the tree view.
    modTree['columns'] = ("Mod Name", "Author", "Type", "Version", "Description")
    modTree.column("#0", width = 0, minwidth = 0, stretch = 'no')
    modTree.column("Mod Name", anchor = 'w', width = 180, minwidth = 25)
    modTree.column("Author", anchor = 'w', width = 120, minwidth = 25)
    modTree.column("Type", anchor = 'w', width = 90, minwidth = 25)
    modTree.column("Version", anchor = 'w', width = 36, minwidth = 25)
    modTree.column("Description", anchor = 'w', width = 360, minwidth = 120)

    # Create the headings.
    modTree.heading("#0")
    modTree.heading("Mod Name", text = "Mod Name", anchor = 'w', )
    modTree.heading("Author", text = "Author", anchor = 'w')
    modTree.heading("Type", text = "Type", anchor = 'w')
    modTree.heading("Version", text = "Version", anchor = 'w')
    modTree.heading("Description", text = "Description", anchor = 'w')

    # Add the info.
    modTree.pack(side = 'left', fill = 'both', expand = 1)

    # Add scrollbars.
    modTreeYBar = TTK.Scrollbar(modManagerFrame, orient = 'vertical', command = modTree.yview)
    modTreeYBar.pack(side = 'right', fill = 'y')

    modTree.config(yscrollcommand = modTreeYBar.set)
    modTree.bind('<Configure>')

    # Status label.
    modManagerStatus = Label(wtdeOptionsMods, text = "Mods loaded", relief = 'sunken', anchor = 'w', bd = 1)
    modManagerStatus.pack(fill = 'x', anchor = 's')

    # Load all mod data into the tree.
    wtde_get_mods(modTree, modManagerStatus)

# Execute tab code.
ModsSettings()

# ===========================================================================================================
# General Settings
# 
# Used to adjust general settings about GHWT: DE.
# ===========================================================================================================
# Main GeneralSettings class.
class GeneralSettings():
    """
    General settings tab.
    \n
    This class is responsible for creating the widgets for the General Settings tab.
    """
    # Title text with the purpose of the tab.
    GENERAL_SETTINGS_TITLE_TEXT = "General Settings: Adjust general settings about WTDE.\nHover over any option to see what it does!"
    generalTitleLabel = Label(wtdeOptionsGeneral, text = GENERAL_SETTINGS_TITLE_TEXT, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO_HEADER, justify = 'left')
    generalTitleLabel.grid(row = 0, column = 0, columnspan = 999, sticky = 'nw')

    # Use Discord Rich Presence
    richPresence = StringVar()
    RICH_PRESENCE_TIP = "Use Discord Rich Presence.\n\n" \
                        "If Discord is installed on this device, when this is enabled,\n" \
                        "it will show a detailed summary about what\n" \
                        "you are currently doing in-game, such as what mode\n" \
                        "you're playing, your instrument, what song you are\n" \
                        "currently in, time until it's over, and more!"
    generalUseRichPresence = TTK.Checkbutton(wtdeOptionsGeneral, text = "Use Discord Rich Presence", variable = richPresence, onvalue = '1', offvalue = '0')
    generalUseRichPresence.grid(row = 1, column = 0, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalUseRichPresence, msg = RICH_PRESENCE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Use Holiday Themes
    allowHolidays = StringVar()
    ALLOW_HOLIDAYS_TIP = "Use holiday themes in WTDE.\n\n" \
                        "These are themes that will be shown during certain times of the year!\n" \
                        "Currently, there are the following themes:\n" \
                        "  •  WTDE Default Theme\n" \
                        "  •  Valentine's Day Theme\n" \
                        "  •  Halloween Theme\n" \
                        "  •  Christmas Theme"
    generalAllowHolidays = TTK.Checkbutton(wtdeOptionsGeneral, text = "Use Holiday Themes", variable = allowHolidays, onvalue = '1', offvalue = '0')
    generalAllowHolidays.grid(row = 2, column = 0, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalAllowHolidays, msg = ALLOW_HOLIDAYS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Whammy Pitch Shift
    whammyPitchShift = StringVar()
    WHAMMY_PITCH_SHIFT_TIP = "Turn ON or OFF whammy effects. If this is OFF, audio distortion by whammy will be disabled."
    generalWhammyPitchShift = TTK.Checkbutton(wtdeOptionsGeneral, text = "Whammy Pitch Shift", variable = whammyPitchShift, onvalue = '1', offvalue = '0')
    generalWhammyPitchShift.grid(row = 3, column = 0, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalWhammyPitchShift, msg = WHAMMY_PITCH_SHIFT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Language
    language = StringVar()
    LANGUAGE_SELECT_TIP = "Set the language to be used in-game."

    generalLanguageSelectLabel = Label(wtdeOptionsGeneral, text = "Language:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    generalLanguageSelectLabel.grid(row = 4, column = 0, padx = 20, pady = 5)
    ToolTip(generalLanguageSelectLabel, msg = LANGUAGE_SELECT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    generalLanguageSelect = TTK.OptionMenu(wtdeOptionsGeneral, language, *languages)
    generalLanguageSelect.grid(row = 4, column = 1, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalLanguageSelect, msg = LANGUAGE_SELECT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Audio Buffer Length
    audioBuffLen = StringVar()
    AUDIO_BUFF_LEN_TIP = "The length, in bytes, of the audio buffer used when decoding FMOD Sound Bank streams. Higher is usually better.\n\n" \
                        "Modifying this and/or changing your sound output to 44.1 kHz can cause bad audio output in-game."

    generalAudioBuffLenLabel = Label(wtdeOptionsGeneral, text = "Audio Buffer Length:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    generalAudioBuffLenLabel.grid(row = 5, column = 0, padx = 20, pady = 5)
    ToolTip(generalAudioBuffLenLabel, msg = AUDIO_BUFF_LEN_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    generalAudioBuffLen = TTK.OptionMenu(wtdeOptionsGeneral, audioBuffLen, *AUDIO_BUFFLENS)
    generalAudioBuffLen.grid(row = 5, column = 1, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalAudioBuffLen, msg = AUDIO_BUFF_LEN_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Audio Buffer Length
    autoLogin = StringVar()
    AUTO_LOGIN_TIP = "Set if you want the game to automatically log you in to the online servers upon startup."

    generalAutoLoginLabel = Label(wtdeOptionsGeneral, text = "Auto Login:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    generalAutoLoginLabel.grid(row = 6, column = 0, padx = 20, pady = 5)
    ToolTip(generalAutoLoginLabel, msg = AUTO_LOGIN_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    generalAutoLogin = TTK.OptionMenu(wtdeOptionsGeneral, autoLogin, *AUTO_LOGIN_OPTIONS)
    generalAutoLogin.grid(row = 6, column = 1, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalAutoLogin, msg = AUTO_LOGIN_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # ===========================================================================================================
    # Main Menu Toggles
    # ===========================================================================================================
    # Main Menu Toggles Header
    MENU_TOGGLES_TIP = "Turn ON or OFF various different commands on the main menu."
    generalMainMenuOptionsLabel = Label(wtdeOptionsGeneral, text = "Main Menu Options:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    generalMainMenuOptionsLabel.grid(row = 1, column = 2, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalMainMenuOptionsLabel, msg = MENU_TOGGLES_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Career Option
    useCareerOption = StringVar()
    USE_CAREER_TIP = "Show or hide the Career option."
    generalMMOCareer = TTK.Checkbutton(wtdeOptionsGeneral, text = "Career", variable = useCareerOption, onvalue = '1', offvalue = '0')
    generalMMOCareer.grid(row = 2, column = 2, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalMMOCareer, msg = USE_CAREER_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Quickplay Option
    useQuickplayOption = StringVar()
    USE_QUICKPLAY_TIP = "Show or hide the Quickplay option."
    generalMMOQuickplay = TTK.Checkbutton(wtdeOptionsGeneral, text = "Quickplay", variable = useQuickplayOption, onvalue = '1', offvalue = '0')
    generalMMOQuickplay.grid(row = 3, column = 2, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalMMOQuickplay, msg = USE_QUICKPLAY_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Head to Head Option
    useHeadToHeadOption = StringVar()
    USE_HTH_TIP = "Show or hide the Head to Head option."
    generalMMOHeadToHead = TTK.Checkbutton(wtdeOptionsGeneral, text = "Head to Head", variable = useHeadToHeadOption, onvalue = '1', offvalue = '0')
    generalMMOHeadToHead.grid(row = 4, column = 2, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalMMOHeadToHead, msg = USE_HTH_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Online Option
    useOnlineOption = StringVar()
    USE_ONLINE_TIP = "Show or hide the Online option."
    generalMMOOnline = TTK.Checkbutton(wtdeOptionsGeneral, text = "Online", variable = useOnlineOption, onvalue = '1', offvalue = '0')
    generalMMOOnline.grid(row = 5, column = 2, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalMMOOnline, msg = USE_ONLINE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Music Studio Option
    useMusicStudioOption = StringVar()
    USE_MUSIC_STUDIO_TIP = "Show or hide the Music Studio option."
    generalMMOMusicStudio = TTK.Checkbutton(wtdeOptionsGeneral, text = "Music Studio", variable = useMusicStudioOption, onvalue = '1', offvalue = '0')
    generalMMOMusicStudio.grid(row = 6, column = 2, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalMMOMusicStudio, msg = USE_MUSIC_STUDIO_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Rock Star Creator Option
    useCAROption = StringVar()
    USE_CAR_TIP = "Show or hide the Rock Star Creator option."
    generalMMOCreateRocker = TTK.Checkbutton(wtdeOptionsGeneral, text = "Rock Star Creator", variable = useCAROption, onvalue = '1', offvalue = '0')
    generalMMOCreateRocker.grid(row = 7, column = 2, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalMMOCreateRocker, msg = USE_CAR_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Options Option
    useOptionsOption = StringVar()
    USE_OPTIONS_TIP = "Show or hide the Options option."
    generalMMOOptions = TTK.Checkbutton(wtdeOptionsGeneral, text = "Options", variable = useOptionsOption, onvalue = '1', offvalue = '0')
    generalMMOOptions.grid(row = 8, column = 2, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalMMOOptions, msg = USE_OPTIONS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Exit Option
    useQuitOption = StringVar()
    USE_QUIT_TIP = "Show or hide the Exit option."
    generalMMOExit = TTK.Checkbutton(wtdeOptionsGeneral, text = "Exit", variable = useQuitOption, onvalue = '1', offvalue = '0')
    generalMMOExit.grid(row = 9, column = 2, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalMMOExit, msg = USE_QUIT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

# Execute tab code.
GeneralSettings()

# ===========================================================================================================
# Input Settings
# 
# Used for the user's keyboard controls, microphone, and more.
# ===========================================================================================================
# Main InputSettings class.
class InputSettings():
    """
    Input settings class.
    \n
    This class is responsible for setting up the Input Settings tab.
    """
    # Title text with the purpose of the tab.
    INPUT_SETTINGS_TITLE_TEXT = "Input Settings: Modify your keyboard controls and microphone settings.\nHover over any option to see what it does!"
    inputTitleLabel = Label(wtdeOptionsInput, text = INPUT_SETTINGS_TITLE_TEXT, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO_HEADER, justify = 'left', anchor = 'w')
    inputTitleLabel.pack(fill = 'x', anchor = 'nw')

    # Add divider.
    # TTK.Separator(wtdeOptionsInput).pack(fill = 'x')

    # Add and Clear tooltips.
    INPUT_LIST_TIP = "List of all inputs assigned to this binding."
    ADD_INPUT_TIP = "Record a key to add to this binding."
    CLEAR_INPUTS_TIP = "Clear all bindings for this input."

    # Input root frame setup.
    inputRootFrame = Frame(wtdeOptionsInput, bg = BG_COLOR, relief = 'flat')
    inputRootFrame.pack(fill = 'both', expand = 1)

    # Input canvas.
    inputFrameCanvas = Canvas(inputRootFrame, bg = BG_COLOR, relief = 'flat')
    inputFrameCanvas.pack(side = 'left', fill = 'both', expand = 1)

    # Add the scroll bar.
    inputFrameScrollbar = TTK.Scrollbar(inputRootFrame, orient = 'vertical', command = inputFrameCanvas.yview)
    inputFrameScrollbar.pack(side = 'right', fill = 'y')

    # Configure the canvas.
    inputFrameCanvas.config(yscrollcommand = inputFrameScrollbar.set)
    inputFrameCanvas.bind('<Configure>', lambda e: InputSettings.inputFrameCanvas.config(scrollregion = InputSettings.inputFrameCanvas.bbox('all')))

    # The actual frame everything will go into.
    inputFrameWidgets = Frame(inputFrameCanvas, bg = BG_COLOR, relief = 'flat')

    # Add the frame in as a window.
    inputFrameCanvas.create_window((0, 0), window = inputFrameWidgets, anchor = 'nw') 

    # ===========================================================================================================
    # Guitar & Bass Inputs
    # ===========================================================================================================
    
    inputGuitarHeaderLabel = Label(inputFrameWidgets, text = "  Guitar & Bass Keyboard Controls:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', image = ImageConst.INPUT_GUITAR_ICON, compound = 'left')
    inputGuitarHeaderLabel.grid(row = 0, column = 0, columnspan = 4, pady = 5, sticky = 'w')

    # ===========================================================================================================
    # Guitar Inputs Label Widgets
    # ===========================================================================================================

    inputKeyGuitarGreenLabel = Label(inputFrameWidgets, text = "Green: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyGuitarGreenLabel.grid(row = 1, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyGuitarRedLabel = Label(inputFrameWidgets, text = "Red: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyGuitarRedLabel.grid(row = 2, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyGuitarYellowLabel = Label(inputFrameWidgets, text = "Yellow: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyGuitarYellowLabel.grid(row = 3, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyGuitarBlueLabel = Label(inputFrameWidgets, text = "Blue: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyGuitarBlueLabel.grid(row = 4, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyGuitarOrangeLabel = Label(inputFrameWidgets, text = "Orange: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyGuitarOrangeLabel.grid(row = 5, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyGuitarSPLabel = Label(inputFrameWidgets, text = "Star Power: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyGuitarSPLabel.grid(row = 6, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyGuitarStartLabel = Label(inputFrameWidgets, text = "Start: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyGuitarStartLabel.grid(row = 7, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyGuitarSelectLabel = Label(inputFrameWidgets, text = "Back/Select: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyGuitarSelectLabel.grid(row = 8, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyGuitarCancelLabel = Label(inputFrameWidgets, text = "Cancel: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyGuitarCancelLabel.grid(row = 9, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyGuitarWhammyLabel = Label(inputFrameWidgets, text = "Whammy: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyGuitarWhammyLabel.grid(row = 10, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyGuitarUpLabel = Label(inputFrameWidgets, text = "Up: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyGuitarUpLabel.grid(row = 11, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyGuitarDownLabel = Label(inputFrameWidgets, text = "Down: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyGuitarDownLabel.grid(row = 12, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyGuitarLeftLabel = Label(inputFrameWidgets, text = "Left: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyGuitarLeftLabel.grid(row = 13, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyGuitarRightLabel = Label(inputFrameWidgets, text = "Right: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyGuitarRightLabel.grid(row = 14, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    # ===========================================================================================================
    # Guitar Inputs Entry Widgets
    # ===========================================================================================================

    inputKeyGuitarGreenEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyGuitarGreenEntry.grid(row = 1, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyGuitarGreenEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarRedEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyGuitarRedEntry.grid(row = 2, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyGuitarRedEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarYellowEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyGuitarYellowEntry.grid(row = 3, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyGuitarYellowEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarBlueEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyGuitarBlueEntry.grid(row = 4, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyGuitarBlueEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarOrangeEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyGuitarOrangeEntry.grid(row = 5, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyGuitarOrangeEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarSPEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyGuitarSPEntry.grid(row = 6, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyGuitarSPEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarStartEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyGuitarStartEntry.grid(row = 7, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyGuitarStartEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarSelectEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyGuitarSelectEntry.grid(row = 8, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyGuitarSelectEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarCancelEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyGuitarCancelEntry.grid(row = 9, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyGuitarCancelEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarWhammyEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyGuitarWhammyEntry.grid(row = 10, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyGuitarWhammyEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarUpEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyGuitarUpEntry.grid(row = 11, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyGuitarUpEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarDownEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyGuitarDownEntry.grid(row = 12, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyGuitarDownEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarLeftEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyGuitarLeftEntry.grid(row = 13, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyGuitarLeftEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarRightEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyGuitarRightEntry.grid(row = 14, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyGuitarRightEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # ===========================================================================================================
    # Guitar Inputs Add Button Widgets
    # ===========================================================================================================

    inputKeyGuitarGreenAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyGuitarGreenEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyGuitarGreenAdd.grid(row = 1, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarGreenAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarRedAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyGuitarRedEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyGuitarRedAdd.grid(row = 2, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarRedAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarYellowAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyGuitarYellowEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyGuitarYellowAdd.grid(row = 3, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarYellowAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarBlueAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyGuitarBlueEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyGuitarBlueAdd.grid(row = 4, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarBlueAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarOrangeAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyGuitarOrangeEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyGuitarOrangeAdd.grid(row = 5, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarOrangeAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarSPAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyGuitarSPEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyGuitarSPAdd.grid(row = 6, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarSPAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarStartAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyGuitarStartEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyGuitarStartAdd.grid(row = 7, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarStartAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarSelectAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyGuitarSelectEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyGuitarSelectAdd.grid(row = 8, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarSelectAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarCancelAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyGuitarCancelEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyGuitarCancelAdd.grid(row = 9, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarCancelAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarWhammyAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyGuitarWhammyEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyGuitarWhammyAdd.grid(row = 10, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarWhammyAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarUpAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyGuitarUpEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyGuitarUpAdd.grid(row = 11, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarUpAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarDownAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyGuitarDownEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyGuitarDownAdd.grid(row = 12, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarDownAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarLeftAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyGuitarLeftEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyGuitarLeftAdd.grid(row = 13, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarLeftAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarRightAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyGuitarRightEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyGuitarRightAdd.grid(row = 14, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarRightAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # ===========================================================================================================
    # Guitar Inputs Clear Button Widgets
    # ===========================================================================================================

    inputKeyGuitarGreenDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyGuitarGreenEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyGuitarGreenDelete.grid(row = 1, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarGreenDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarRedDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyGuitarRedEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyGuitarRedDelete.grid(row = 2, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarRedDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarYellowDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyGuitarYellowEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyGuitarYellowDelete.grid(row = 3, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarYellowDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarBlueDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyGuitarBlueEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyGuitarBlueDelete.grid(row = 4, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarBlueDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarOrangeDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyGuitarOrangeEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyGuitarOrangeDelete.grid(row = 5, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarOrangeDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarSPDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyGuitarSPEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyGuitarSPDelete.grid(row = 6, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarSPDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarStartDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyGuitarStartEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyGuitarStartDelete.grid(row = 7, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarStartDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarSelectDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyGuitarSelectEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyGuitarSelectDelete.grid(row = 8, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarSelectDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarCancelDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyGuitarCancelEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyGuitarCancelDelete.grid(row = 9, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarCancelDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarWhammyDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyGuitarWhammyEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyGuitarWhammyDelete.grid(row = 10, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarWhammyDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarUpDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyGuitarUpEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyGuitarUpDelete.grid(row = 11, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarUpDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarDownDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyGuitarDownEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyGuitarDownDelete.grid(row = 12, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarDownDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarLeftDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyGuitarLeftEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyGuitarLeftDelete.grid(row = 13, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarLeftDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyGuitarRightDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyGuitarRightEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyGuitarRightDelete.grid(row = 14, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyGuitarRightDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # ================== SPACER ================== #
    inputKeySpacer = Label(inputFrameWidgets, bg = BG_COLOR, text = "  ")
    inputKeySpacer.grid(row = 0, column = 4)

    # ===========================================================================================================
    # Drum Inputs
    # ===========================================================================================================

    inputDrumsHeaderLabel = Label(inputFrameWidgets, text = "  Drum Keyboard Controls:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', image = ImageConst.INPUT_DRUMS_ICON, compound = 'left')
    inputDrumsHeaderLabel.grid(row = 0, column = 5, columnspan = 4, pady = 5, sticky = 'w')

    # ===========================================================================================================
    # Drum Inputs Label Widgets
    # ===========================================================================================================

    inputKeyDrumsRedLabel = Label(inputFrameWidgets, text = "Red: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyDrumsRedLabel.grid(row = 1, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyDrumsYellowLabel = Label(inputFrameWidgets, text = "Yellow: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyDrumsYellowLabel.grid(row = 2, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyDrumsBlueLabel = Label(inputFrameWidgets, text = "Blue: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyDrumsBlueLabel.grid(row = 3, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyDrumsOrangeLabel = Label(inputFrameWidgets, text = "Orange: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyDrumsOrangeLabel.grid(row = 4, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyDrumsGreenLabel = Label(inputFrameWidgets, text = "Green: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyDrumsGreenLabel.grid(row = 5, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyDrumsKickLabel = Label(inputFrameWidgets, text = "Kick Drum: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyDrumsKickLabel.grid(row = 6, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyDrumsStartLabel = Label(inputFrameWidgets, text = "Start: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyDrumsStartLabel.grid(row = 7, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyDrumsSelectLabel = Label(inputFrameWidgets, text = "Back/Select: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyDrumsSelectLabel.grid(row = 8, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyDrumsCancelLabel = Label(inputFrameWidgets, text = "Cancel: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyDrumsCancelLabel.grid(row = 9, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyDrumsUpLabel = Label(inputFrameWidgets, text = "Up: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyDrumsUpLabel.grid(row = 10, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyDrumsDownLabel = Label(inputFrameWidgets, text = "Down: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyDrumsDownLabel.grid(row = 11, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    # ===========================================================================================================
    # Drum Inputs Entry Widgets
    # ===========================================================================================================

    inputKeyDrumsRedEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyDrumsRedEntry.grid(row = 1, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyDrumsRedEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsYellowEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyDrumsYellowEntry.grid(row = 2, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyDrumsYellowEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsBlueEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyDrumsBlueEntry.grid(row = 3, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyDrumsBlueEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsOrangeEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyDrumsOrangeEntry.grid(row = 4, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyDrumsOrangeEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsGreenEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyDrumsGreenEntry.grid(row = 5, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyDrumsGreenEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsKickEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyDrumsKickEntry.grid(row = 6, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyDrumsKickEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsStartEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyDrumsStartEntry.grid(row = 7, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyDrumsStartEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsSelectEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyDrumsSelectEntry.grid(row = 8, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyDrumsSelectEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsCancelEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyDrumsCancelEntry.grid(row = 9, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyDrumsCancelEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsUpEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyDrumsUpEntry.grid(row = 10, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyDrumsUpEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsDownEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyDrumsDownEntry.grid(row = 11, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyDrumsDownEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # ===========================================================================================================
    # Drum Inputs Add Button Widgets
    # ===========================================================================================================

    inputKeyDrumsRedAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyDrumsRedEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyDrumsRedAdd.grid(row = 1, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsRedAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsYellowAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyDrumsYellowEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyDrumsYellowAdd.grid(row = 2, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsYellowAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsBlueAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyDrumsBlueEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyDrumsBlueAdd.grid(row = 3, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsBlueAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsOrangeAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyDrumsOrangeEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyDrumsOrangeAdd.grid(row = 4, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsOrangeAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsGreenAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyDrumsGreenEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyDrumsGreenAdd.grid(row = 5, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsGreenAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsKickAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyDrumsKickEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyDrumsKickAdd.grid(row = 6, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsKickAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsStartAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyDrumsStartEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyDrumsStartAdd.grid(row = 7, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsStartAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsSelectAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyDrumsSelectEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyDrumsSelectAdd.grid(row = 8, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsSelectAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsCancelAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyDrumsCancelEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyDrumsCancelAdd.grid(row = 9, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsCancelAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsUpAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyDrumsUpEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyDrumsUpAdd.grid(row = 10, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsUpAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsDownAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyDrumsDownEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyDrumsDownAdd.grid(row = 11, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsDownAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # ===========================================================================================================
    # Drum Inputs Clear Button Widgets
    # ===========================================================================================================

    inputKeyDrumsRedDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyDrumsRedEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyDrumsRedDelete.grid(row = 1, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsRedDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsYellowDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT,command = lambda: InputSettings.inputKeyDrumsYellowEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyDrumsYellowDelete.grid(row = 2, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsYellowDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsBlueDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT,command = lambda: InputSettings.inputKeyDrumsBlueEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyDrumsBlueDelete.grid(row = 3, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsBlueDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsOrangeDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT,command = lambda: InputSettings.inputKeyDrumsOrangeEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyDrumsOrangeDelete.grid(row = 4, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsOrangeDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsGreenDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT,command = lambda: InputSettings.inputKeyDrumsGreenEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyDrumsGreenDelete.grid(row = 5, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsGreenDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsKickDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT,command = lambda: InputSettings.inputKeyDrumsKickEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyDrumsKickDelete.grid(row = 6, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsKickDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsStartDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT,command = lambda: InputSettings.inputKeyDrumsStartEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyDrumsStartDelete.grid(row = 7, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsStartDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsSelectDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT,command = lambda: InputSettings.inputKeyDrumsSelectEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyDrumsSelectDelete.grid(row = 8, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsSelectDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsCancelDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT,command = lambda: InputSettings.inputKeyDrumsCancelEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyDrumsCancelDelete.grid(row = 9, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsCancelDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsUpDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT,command = lambda: InputSettings.inputKeyDrumsUpEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyDrumsUpDelete.grid(row = 10, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsUpDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyDrumsDownDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT,command = lambda: InputSettings.inputKeyDrumsDownEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyDrumsDownDelete.grid(row = 11, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyDrumsDownDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # ================== SPACER ================== #
    inputKeySpacer1 = Label(inputFrameWidgets, bg = BG_COLOR, text = " ")
    inputKeySpacer1.grid(row = 15, column = 0, columnspan = 999, pady = 10)

    # ===========================================================================================================
    # Mic Inputs
    # ===========================================================================================================

    inputMicHeaderLabel = Label(inputFrameWidgets, text = "  Mic Keyboard Controls:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', image = ImageConst.INPUT_MIC_ICON, compound = 'left')
    inputMicHeaderLabel.grid(row = 16, column = 0, columnspan = 4, pady = 5, sticky = 'w')

    # ===========================================================================================================
    # Mic Inputs Label Widgets
    # ===========================================================================================================

    inputKeyMicGreenLabel = Label(inputFrameWidgets, text = "Green: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMicGreenLabel.grid(row = 17, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMicRedLabel = Label(inputFrameWidgets, text = "Red: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMicRedLabel.grid(row = 18, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMicYellowLabel = Label(inputFrameWidgets, text = "Yellow: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMicYellowLabel.grid(row = 19, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMicBlueLabel = Label(inputFrameWidgets, text = "Blue: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMicBlueLabel.grid(row = 20, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMicOrangeLabel = Label(inputFrameWidgets, text = "Orange: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMicOrangeLabel.grid(row = 21, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMicStartLabel = Label(inputFrameWidgets, text = "Start: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMicStartLabel.grid(row = 22, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMicSelectLabel = Label(inputFrameWidgets, text = "Back/Select: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMicSelectLabel.grid(row = 23, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMicCancelLabel = Label(inputFrameWidgets, text = "Cancel: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMicCancelLabel.grid(row = 24, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMicUpLabel = Label(inputFrameWidgets, text = "Up: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMicUpLabel.grid(row = 25, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMicDownLabel = Label(inputFrameWidgets, text = "Down: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMicDownLabel.grid(row = 26, column = 0, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    # ===========================================================================================================
    # Mic Inputs Entry Widgets
    # ===========================================================================================================

    inputKeyMicGreenEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMicGreenEntry.grid(row = 17, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMicGreenEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicRedEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMicRedEntry.grid(row = 18, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMicRedEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicYellowEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMicYellowEntry.grid(row = 19, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMicYellowEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicBlueEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMicBlueEntry.grid(row = 20, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMicBlueEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicOrangeEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMicOrangeEntry.grid(row = 21, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMicOrangeEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicStartEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMicStartEntry.grid(row = 22, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMicStartEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicSelectEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMicSelectEntry.grid(row = 23, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMicSelectEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicCancelEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMicCancelEntry.grid(row = 24, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMicCancelEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicUpEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMicUpEntry.grid(row = 25, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMicUpEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicDownEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMicDownEntry.grid(row = 26, column = 1, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMicDownEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # ===========================================================================================================
    # Mic Inputs Add Button Widgets
    # ===========================================================================================================

    inputKeyMicGreenAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMicGreenEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMicGreenAdd.grid(row = 17, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicGreenAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicRedAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMicRedEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMicRedAdd.grid(row = 18, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicRedAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicYellowAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMicYellowEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMicYellowAdd.grid(row = 19, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicYellowAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicBlueAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMicBlueEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMicBlueAdd.grid(row = 20, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicBlueAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicOrangeAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMicOrangeEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMicOrangeAdd.grid(row = 21, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicOrangeAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicStartAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMicStartEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMicStartAdd.grid(row = 22, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicStartAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicSelectAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMicSelectEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMicSelectAdd.grid(row = 23, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicSelectAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicCancelAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMicCancelEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMicCancelAdd.grid(row = 24, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicCancelAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicUpAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMicUpEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMicUpAdd.grid(row = 25, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicUpAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicDownAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMicDownEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMicDownAdd.grid(row = 26, column = 2, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicDownAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # ===========================================================================================================
    # Mic Inputs Clear Button Widgets
    # ===========================================================================================================

    inputKeyMicGreenDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMicGreenEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMicGreenDelete.grid(row = 17, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicGreenDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicRedDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMicRedEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMicRedDelete.grid(row = 18, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicRedDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicYellowDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMicYellowEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMicYellowDelete.grid(row = 19, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicYellowDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicBlueDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMicBlueEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMicBlueDelete.grid(row = 20, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicBlueDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicOrangeDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMicOrangeEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMicOrangeDelete.grid(row = 21, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicOrangeDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicStartDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMicOrangeEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMicStartDelete.grid(row = 22, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicStartDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicSelectDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMicSelectEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMicSelectDelete.grid(row = 23, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicSelectDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicCancelDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMicCancelEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMicCancelDelete.grid(row = 24, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicCancelDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicUpDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMicUpEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMicUpDelete.grid(row = 25, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicUpDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMicDownDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMicDownEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMicDownDelete.grid(row = 26, column = 3, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMicDownDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # ===========================================================================================================
    # Menu Inputs
    # ===========================================================================================================

    inputMenuHeaderLabel = Label(inputFrameWidgets, text = "  Menu Keyboard Controls:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', image = ImageConst.INPUT_MENU_ICON, compound = 'left')
    inputMenuHeaderLabel.grid(row = 16, column = 5, columnspan = 4, pady = 5, sticky = 'w')

    # ===========================================================================================================
    # Menu Inputs Label Widgets
    # ===========================================================================================================

    inputKeyMenuGreenLabel = Label(inputFrameWidgets, text = "Green: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMenuGreenLabel.grid(row = 17, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMenuRedLabel = Label(inputFrameWidgets, text = "Red: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMenuRedLabel.grid(row = 18, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMenuYellowLabel = Label(inputFrameWidgets, text = "Yellow: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMenuYellowLabel.grid(row = 19, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMenuBlueLabel = Label(inputFrameWidgets, text = "Blue: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMenuBlueLabel.grid(row = 20, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMenuOrangeLabel = Label(inputFrameWidgets, text = "Orange: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMenuOrangeLabel.grid(row = 21, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMenuStartLabel = Label(inputFrameWidgets, text = "Start: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMenuStartLabel.grid(row = 22, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMenuSelectLabel = Label(inputFrameWidgets, text = "Back/Select: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMenuSelectLabel.grid(row = 23, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMenuCancelLabel = Label(inputFrameWidgets, text = "Cancel: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMenuCancelLabel.grid(row = 24, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMenuWhammyLabel = Label(inputFrameWidgets, text = "Whammy: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMenuWhammyLabel.grid(row = 25, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMenuKickLabel = Label(inputFrameWidgets, text = "Kick Drum: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMenuKickLabel.grid(row = 26, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMenuUpLabel = Label(inputFrameWidgets, text = "Up: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMenuUpLabel.grid(row = 27, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMenuDownLabel = Label(inputFrameWidgets, text = "Down: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMenuDownLabel.grid(row = 28, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMenuLeftLabel = Label(inputFrameWidgets, text = "Left: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMenuLeftLabel.grid(row = 29, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    inputKeyMenuRightLabel = Label(inputFrameWidgets, text = "Right: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputKeyMenuRightLabel.grid(row = 30, column = 6, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'e')

    # ===========================================================================================================
    # Menu Inputs Entry Widgets
    # ===========================================================================================================

    inputKeyMenuGreenEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMenuGreenEntry.grid(row = 17, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMenuGreenEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuRedEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMenuRedEntry.grid(row = 18, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMenuRedEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuYellowEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMenuYellowEntry.grid(row = 19, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMenuYellowEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuBlueEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMenuBlueEntry.grid(row = 20, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMenuBlueEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuOrangeEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMenuOrangeEntry.grid(row = 21, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMenuOrangeEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuStartEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMenuStartEntry.grid(row = 22, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMenuStartEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuSelectEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMenuSelectEntry.grid(row = 23, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMenuSelectEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuCancelEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMenuCancelEntry.grid(row = 24, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMenuCancelEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuWhammyEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMenuWhammyEntry.grid(row = 25, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMenuWhammyEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuKickEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMenuKickEntry.grid(row = 26, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMenuKickEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuUpEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMenuUpEntry.grid(row = 27, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMenuUpEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuDownEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMenuDownEntry.grid(row = 28, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMenuDownEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuLeftEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMenuLeftEntry.grid(row = 29, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMenuLeftEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuRightEntry = TTK.Entry(inputFrameWidgets, width = INPUT_ENTRY_WIDTH, takefocus = ALLOW_INPUT_ENTRY_FOCUS)
    inputKeyMenuRightEntry.grid(row = 30, column = 7, padx = 5, pady = INPUT_Y_OFFSET, sticky = 'w')
    ToolTip(inputKeyMenuRightEntry, msg = INPUT_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # ===========================================================================================================
    # Menu Inputs Add Button Widgets
    # ===========================================================================================================

    inputKeyMenuGreenAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMenuGreenEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMenuGreenAdd.grid(row = 17, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuGreenAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuRedAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMenuRedEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMenuRedAdd.grid(row = 18, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuRedAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuYellowAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMenuYellowEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMenuYellowAdd.grid(row = 19, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuYellowAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuBlueAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMenuBlueEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMenuBlueAdd.grid(row = 20, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuBlueAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuOrangeAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMenuOrangeEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMenuOrangeAdd.grid(row = 21, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuOrangeAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuStartAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMenuStartEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMenuStartAdd.grid(row = 22, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuStartAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuSelectAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMenuSelectEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMenuSelectAdd.grid(row = 23, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuSelectAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuCancelAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMenuCancelEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMenuCancelAdd.grid(row = 24, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuCancelAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuWhammyAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMenuWhammyEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMenuWhammyAdd.grid(row = 25, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuWhammyAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuKickAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMenuKickEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMenuKickAdd.grid(row = 26, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuKickAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuUpAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMenuUpEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMenuUpAdd.grid(row = 27, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuUpAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuDownAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMenuDownEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMenuDownAdd.grid(row = 28, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuDownAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuLeftAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMenuLeftEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMenuLeftAdd.grid(row = 29, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuLeftAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuRightAdd = TTK.Button(inputFrameWidgets, text = ADD_BUTTON_TEXT, command = lambda: listen_key(InputSettings.inputKeyMenuRightEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputKeyMenuRightAdd.grid(row = 30, column = 8, padx = 5, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuRightAdd, msg = ADD_INPUT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # ===========================================================================================================
    # Menu Inputs Clear Button Widgets
    # ===========================================================================================================

    inputKeyMenuGreenDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMenuGreenEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMenuGreenDelete.grid(row = 17, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuGreenDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuRedDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMenuRedEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMenuRedDelete.grid(row = 18, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuRedDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuYellowDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMenuYellowEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMenuYellowDelete.grid(row = 19, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuYellowDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuBlueDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMenuBlueEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMenuBlueDelete.grid(row = 20, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuBlueDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuOrangeDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMenuOrangeEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMenuOrangeDelete.grid(row = 21, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuOrangeDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuStartDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMenuStartEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMenuStartDelete.grid(row = 22, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuStartDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuSelectDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMenuSelectEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMenuSelectDelete.grid(row = 23, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuSelectDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuCancelDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMenuCancelEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMenuCancelDelete.grid(row = 24, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuCancelDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuWhammyDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMenuWhammyEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMenuWhammyDelete.grid(row = 25, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuWhammyDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuKickDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMenuKickEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMenuKickDelete.grid(row = 26, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuKickDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuUpDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMenuUpEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMenuUpDelete.grid(row = 27, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuUpDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuDownDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMenuDownEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMenuDownDelete.grid(row = 28, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuDownDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuLeftDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMenuLeftEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMenuLeftDelete.grid(row = 29, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuLeftDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputKeyMenuRightDelete = TTK.Button(inputFrameWidgets, text = CLEAR_BUTTON_TEXT, command = lambda: InputSettings.inputKeyMenuRightEntry.delete(0, END), takefocus = ALLOW_CLEAR_BUTTON_FOCUS)
    inputKeyMenuRightDelete.grid(row = 30, column = 9, pady = INPUT_Y_OFFSET)
    ToolTip(inputKeyMenuRightDelete, msg = CLEAR_INPUTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # ================== SPACER ================== #
    inputKeySpacer2 = Label(inputFrameWidgets, bg = BG_COLOR, text = " ")
    inputKeySpacer2.grid(row = 31, column = 0, columnspan = 999, pady = 10)

    # ===========================================================================================================
    # Mic Settings
    # ===========================================================================================================

    inputMicSettingsHeaderLabel = Label(inputFrameWidgets, text = "  Mic Settings:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', image = ImageConst.INPUT_MIC_ICON, compound = 'left')
    inputMicSettingsHeaderLabel.grid(row = 32, column = 0, columnspan = 10, pady = 5, sticky = 'w')

    # Select Microphone
    micDevice = StringVar()
    MIC_SELECT_TIP = "Select the microphone you want to use for vocal play in-game.\n\n" \
                    "A list of all supported devices will be shown. To disable, select None.\n" \
                    "If your microphone has non-ASCII characters in its name, it might be best\n" \
                    "to rename it in the Sound settings in Windows."

    inputMicSettingsDeviceLabel = Label(inputFrameWidgets, text = "Microphone: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputMicSettingsDeviceLabel.grid(row = 33, column = 0, padx = 5, pady = 5, sticky = 'e')
    ToolTip(inputMicSettingsDeviceLabel, msg = MIC_SELECT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputMicSettingsDeviceMenu = TTK.OptionMenu(inputFrameWidgets, micDevice, *MIC_LIST)
    inputMicSettingsDeviceMenu.grid(row = 33, column = 1, columnspan = 3, padx = 5, pady = 5, sticky = 'w')
    inputMicSettingsDeviceMenu.config(width = 48)
    ToolTip(inputMicSettingsDeviceMenu, msg = MIC_SELECT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Use Input Hack
    disableInputHack = StringVar()
    INPUT_HACK_TIP = "Enable or disable the input hack."
    inputUseInputHack = TTK.Checkbutton(inputFrameWidgets, text = "Use Input Hack", variable = disableInputHack, onvalue = '0', offvalue = '1')
    inputUseInputHack.grid(row = 33, column = 6, pady = 5, sticky = 'w')
    ToolTip(inputUseInputHack, msg = INPUT_HACK_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Mic Audio Delay
    micAudioDelay = StringVar()
    MIC_AUDIO_DELAY = "Audio offset, in milliseconds, of the song audio while playing vocals."

    inputMicSettingsADelayLabel = Label(inputFrameWidgets, text = "Mic Audio Delay: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputMicSettingsADelayLabel.grid(row = 33, column = 7, padx = 5, pady = 5, sticky = 'e')
    ToolTip(inputMicSettingsADelayLabel, msg = MIC_AUDIO_DELAY, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputMicSettingsADelayEntry = TTK.Entry(inputFrameWidgets, width = 11, takefocus = ALLOW_INPUT_ENTRY_FOCUS, textvariable = micAudioDelay)
    inputMicSettingsADelayEntry.grid(row = 33, column = 8, padx = 5, pady = 5, sticky = 'w')
    ToolTip(inputMicSettingsADelayEntry, msg = MIC_AUDIO_DELAY, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Mic Video Delay
    micVideoDelay = StringVar()
    MIC_VIDEO_DELAY = "Video offset, in milliseconds, of the notes while playing vocals."

    inputMicSettingsVDelayLabel = Label(inputFrameWidgets, text = "Mic Video Delay: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
    inputMicSettingsVDelayLabel.grid(row = 34, column = 7, padx = 5, pady = 5, sticky = 'e')
    ToolTip(inputMicSettingsVDelayLabel, msg = MIC_VIDEO_DELAY, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    inputMicSettingsVDelayEntry = TTK.Entry(inputFrameWidgets, width = 11, takefocus = ALLOW_INPUT_ENTRY_FOCUS, textvariable = micVideoDelay)
    inputMicSettingsVDelayEntry.grid(row = 34, column = 8, padx = 5, pady = 5, sticky = 'w')
    ToolTip(inputMicSettingsVDelayEntry, msg = MIC_VIDEO_DELAY, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Use Recommended Values
    USE_RECOMMENDED_TIP = "Set your Mic calibration to the recommended values."
    inputMicUseRecommended = TTK.Button(inputFrameWidgets, text = "Use Recommended Calibration", width = 30, command = lambda: mic_set_calibration(-80, -315, InputSettings.inputMicSettingsADelayEntry, InputSettings.inputMicSettingsVDelayEntry), takefocus = ALLOW_ADD_BUTTON_FOCUS)
    inputMicUseRecommended.grid(row = 35, column = 7, columnspan = 2, pady = 5, sticky = 'e')
    ToolTip(inputMicUseRecommended, msg = USE_RECOMMENDED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

# Execute tab code.
InputSettings()

# ===========================================================================================================
# Graphics Settings
# 
# Used for the user's graphics controls, such as note theme, interface options, and more.
# ===========================================================================================================
# Main GraphicsSettings class.
class GraphicsSettings():
    """
    Graphics settings tab.
    \n
    This class is responsible for populating the Graphics Settings tab with the necessary widgets.
    """
    # Title text with the purpose of the tab.
    GRAPHICS_SETTINGS_TITLE_TEXT = "Graphics Settings: Set your preferences for graphics in WTDE.\nHover over any option to see what it does!"
    graphicsTitleLabel = Label(wtdeOptionsGraphics, text = GRAPHICS_SETTINGS_TITLE_TEXT, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO_HEADER, justify = 'left', anchor = 'w')
    graphicsTitleLabel.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

    # Resolution Width & Height
    RESOLUTION_TIP = "Set the resolution for the game window."
    RESOLUTION_W_TIP = "Set the width (in pixels) for the game window."
    RESOLUTION_H_TIP = "Set the height (in pixels) for the game window."

    graphicsResLabel = Label(wtdeOptionsGraphics, text = "Resolution:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    graphicsResLabel.grid(row = 1, column = 0, padx = 20, pady = 5)
    ToolTip(graphicsResLabel, msg = RESOLUTION_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    graphicsResWEntry = TTK.Entry(wtdeOptionsGraphics, width = 10, takefocus = False)
    graphicsResWEntry.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'w')
    ToolTip(graphicsResWEntry, msg = RESOLUTION_W_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    graphicsResXLabel = Label(wtdeOptionsGraphics, text = "X", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'center')
    graphicsResXLabel.grid(row = 1, column = 2, pady = 5)
    ToolTip(graphicsResXLabel, msg = RESOLUTION_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    graphicsResHEntry = TTK.Entry(wtdeOptionsGraphics, width = 10, takefocus = False)
    graphicsResHEntry.grid(row = 1, column = 3, padx = 5, pady = 5, sticky = 'w')
    ToolTip(graphicsResHEntry, msg = RESOLUTION_H_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Use Native Resolution
    useNativeRes = StringVar()
    NATIVE_RESOLUTION_TIP = "Use the native resolution of your primary monitor as the resolution the game will run at.\n" \
                            "If this is ON, the resolution entered in the width and height boxes will be ignored."
    graphicsUseNativeRes = TTK.Checkbutton(wtdeOptionsGraphics, text = f"Native Monitor Resolution ({get_screen_resolution()[0]} X {get_screen_resolution()[1]})", variable = useNativeRes, onvalue = '1', offvalue = '0', command = native_res_update)
    graphicsUseNativeRes.grid(row = 2, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsUseNativeRes, msg = NATIVE_RESOLUTION_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # FPS Limit
    fpsLimit = StringVar()
    FPS_LIMIT_TIP = "Set the limit for the game's frame rate.\n\n" \
                    "Setting this value will set the target frame rate that the game will try\n" \
                    "to run at. Remember that if Vertical Sync (VSync) is turned ON,\n" \
                    "it will override this and lock the framerate at 60 FPS!"
    graphicsFPSLabel = Label(wtdeOptionsGraphics, text = "FPS Limit:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    graphicsFPSLabel.grid(row = 3, column = 0, padx = 20, pady = 5)
    ToolTip(graphicsFPSLabel, msg = FPS_LIMIT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    graphicsFPSOptions = TTK.OptionMenu(wtdeOptionsGraphics, fpsLimit, *FPS_LIMITS)
    graphicsFPSOptions.config(width = 10)
    graphicsFPSOptions.grid(row = 3, column = 1, columnspan = 3, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsFPSOptions, msg = FPS_LIMIT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Use Vertical Sync
    disableVSync = StringVar()
    VSYNC_LIMIT_TIP = "Turn ON or OFF vertical sync. If this is ON, it will cap the game at\n" \
                    "60 FPS, regardless of the set FPS limit. Helps aid screen tearing!"
    graphicsUseVSync = TTK.Checkbutton(wtdeOptionsGraphics, text = f"Use Vertical Sync", variable = disableVSync, onvalue = '0', offvalue = '1', command = fps_limit_update)
    graphicsUseVSync.grid(row = 4, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsUseVSync, msg = VSYNC_LIMIT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

# ===========================================================================================================
# Auto Launch Tab
# 
# Used to make GHWT: DE automatically load into a song of the user's choice.
# ===========================================================================================================
# Main AutoLaunch class.
class AutoLaunch():
    """
    Auto launch settings tab.
    \n
    This class is responsible for creating the widgets on the screen for the Auto Launch tab.
    """
    # Handle enabled or disabled states of all widgets when Enable Auto Launch is ON or OFF.
    def auto_update_status() -> None:
        """ Handle enabled or disabled states of all widgets when Enable Auto Launch is ON or OFF. """
        if (autoLaunchEnabled.get() == '1'): updateState = 'normal'
        else: updateState = 'disabled'

        for (widget) in (AutoLaunch.AutoLaunch_General.autoSettingsFrame.grid_slaves()): widget.configure(state = updateState)
        AutoLaunch.AutoLaunch_General.autoPlayerSettingsHeader.config(state = updateState)
        for (widget) in (AutoLaunch.AutoLaunch_Advanced.autoAdvancedSettingsFrame.grid_slaves()): widget.configure(state = updateState)

        if (autoLaunchEnabled.get() == '1'):
            AutoLaunch.AutoLaunch_General.auto_update_players(autoPlayerCount.get())
        else:
            for (widget) in (autoP1SettingsFrame.grid_slaves()): widget.configure(state = 'disabled')
            for (widget) in (autoP2SettingsFrame.grid_slaves()): widget.configure(state = 'disabled')
            for (widget) in (autoP3SettingsFrame.grid_slaves()): widget.configure(state = 'disabled')
            for (widget) in (autoP4SettingsFrame.grid_slaves()): widget.configure(state = 'disabled')
            
    # Title text with the purpose of the tab.
    AUTO_SETTINGS_TITLE_TEXT = "Auto Launch Settings: Set up the game to automatically load into a song of your choice.\nHover over any option to see what it does!"
    autoTitleLabel = Label(wtdeOptionsAutoLaunch, text = AUTO_SETTINGS_TITLE_TEXT, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO_HEADER, justify = 'left', anchor = 'w')
    autoTitleLabel.pack(fill = 'x', anchor = 'nw')

    # Save file corruption warning.
    autoInfoWarnLabel = Label(wtdeOptionsAutoLaunch, text = "Warning: This may erase your save data, so make sure to back it up first!", bg = BG_COLOR, fg = '#FF0000', font = FONT_INFO_HEADER, justify = 'left', anchor = 'w')
    autoInfoWarnLabel.pack(fill = 'x', anchor = 'nw')

    # Enable Auto Launch
    global autoLaunchEnabled
    autoLaunchEnabled = StringVar()
    ENABLE_AUTO_LAUNCH_TIP = "Enable or disable auto launch.\n\n" \
                             "Using this, you can set up WTDE to automatically load into a song of your choosing.\n" \
                             "You can even set it up to autoplay, too!\n\n" \
                             "Be warned! This may erase your save data, so make sure to back it up first!"
    autoEnableAL = TTK.Checkbutton(wtdeOptionsAutoLaunch, text = "Enable Auto Launch", variable = autoLaunchEnabled, onvalue = '1', offvalue = '0', command = auto_update_status)
    autoEnableAL.pack(anchor = 'w', pady = 5, padx = 20)
    ToolTip(autoEnableAL, msg = ENABLE_AUTO_LAUNCH_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Add settings into the general Auto Launch Settings.
    class AutoLaunch_General():
        """ General settings for the Auto Launch tab. """
        # Update player settings based on desired player count.
        def auto_update_players(amount: int | str) -> None:
            """ Update player settings based on desired player count. """
            if (autoLaunchEnabled.get() == '1'):
                match (amount):
                    case 1 | "1":
                        for (widget) in (autoP1SettingsFrame.grid_slaves()): widget.configure(state = 'normal')
                        for (widget) in (autoP2SettingsFrame.grid_slaves()): widget.configure(state = 'disabled')
                        for (widget) in (autoP3SettingsFrame.grid_slaves()): widget.configure(state = 'disabled')
                        for (widget) in (autoP4SettingsFrame.grid_slaves()): widget.configure(state = 'disabled')

                    case 2 | "2":
                        for (widget) in (autoP1SettingsFrame.grid_slaves()): widget.configure(state = 'normal')
                        for (widget) in (autoP2SettingsFrame.grid_slaves()): widget.configure(state = 'normal')
                        for (widget) in (autoP3SettingsFrame.grid_slaves()): widget.configure(state = 'disabled')
                        for (widget) in (autoP4SettingsFrame.grid_slaves()): widget.configure(state = 'disabled')

                    case 3 | "3":
                        for (widget) in (autoP1SettingsFrame.grid_slaves()): widget.configure(state = 'normal')
                        for (widget) in (autoP2SettingsFrame.grid_slaves()): widget.configure(state = 'normal')
                        for (widget) in (autoP3SettingsFrame.grid_slaves()): widget.configure(state = 'normal')
                        for (widget) in (autoP4SettingsFrame.grid_slaves()): widget.configure(state = 'disabled')

                    case 4 | "4":
                        for (widget) in (autoP1SettingsFrame.grid_slaves()): widget.configure(state = 'normal')
                        for (widget) in (autoP2SettingsFrame.grid_slaves()): widget.configure(state = 'normal')
                        for (widget) in (autoP3SettingsFrame.grid_slaves()): widget.configure(state = 'normal')
                        for (widget) in (autoP4SettingsFrame.grid_slaves()): widget.configure(state = 'normal')
            else:
                for (widget) in (autoP1SettingsFrame.grid_slaves()): widget.configure(state = 'disabled')
                for (widget) in (autoP2SettingsFrame.grid_slaves()): widget.configure(state = 'disabled')
                for (widget) in (autoP3SettingsFrame.grid_slaves()): widget.configure(state = 'disabled')
                for (widget) in (autoP4SettingsFrame.grid_slaves()): widget.configure(state = 'disabled')

        # Auto Launch Settings frame.
        autoSettingsFrame = Frame(wtdeOptionsAutoLaunch, bg = BG_COLOR)
        autoSettingsFrame.pack(fill = 'x', anchor = 'n', pady = 5)

        # Title label.
        autoSettingsTitle = Label(autoSettingsFrame, text = "Auto Launch Settings:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO_HEADER, justify = 'left', anchor = 'w')
        autoSettingsTitle.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

        # Hide HUD
        autoHideHUD = StringVar()
        HIDE_HUD_TIP = "When auto launch is enabled, do you want the interface hidden?"
        autoSettingsHideHUD = TTK.Checkbutton(autoSettingsFrame, text = "Hide HUD", variable = autoHideHUD, onvalue = '1', offvalue = '0')
        autoSettingsHideHUD.grid(row = 1, column = 0, padx = 20, pady = 5)
        ToolTip(autoSettingsHideHUD, msg = HIDE_HUD_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ================== SPACER ================== #
        autoSettingsSpacer1 = Label(autoSettingsFrame, bg = BG_COLOR, text = "")
        autoSettingsSpacer1.grid(row = 1, column = 1, padx = 30)

        # Number of Players
        global autoPlayerCount
        autoPlayerCount = StringVar()
        PLAYERS_COUNT_TIP = "How many players do you want?"

        autoSettingsPlayersLabel = Label(autoSettingsFrame, text = "Players:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoSettingsPlayersLabel.grid(row = 1, column = 2, pady = 5, sticky = 'e')
        ToolTip(autoSettingsPlayersLabel, msg = PLAYERS_COUNT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        autoSettingsPlayers = TTK.OptionMenu(autoSettingsFrame, autoPlayerCount, *PLAYERS_OPTIONS, command = lambda e: AutoLaunch.AutoLaunch_General.auto_update_players(autoPlayerCount.get()))
        autoSettingsPlayers.config(width = 5)
        autoSettingsPlayers.grid(row = 1, column = 3, padx = 10, pady = 5, sticky = 'w')
        ToolTip(autoSettingsPlayers, msg = PLAYERS_COUNT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ================== SPACER ================== #
        autoSettingsSpacer2 = Label(autoSettingsFrame, bg = BG_COLOR, text = "")
        autoSettingsSpacer2.grid(row = 1, column = 4, padx = 30)

        # Venue Selector
        VENUE_SELECTION_TIP = "Select the venue you want to use."

        autoVenueSelectLabel = Label(autoSettingsFrame, text = "Venue:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoVenueSelectLabel.grid(row = 1, column = 5, pady = 5, sticky = 'e')
        ToolTip(autoVenueSelectLabel, msg = VENUE_SELECTION_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        autoVenue = StringVar()
        autoVenueSelect = TTK.Combobox(autoSettingsFrame, width = 25,values = VENUES, textvariable = autoVenue)
        autoVenueSelect.grid(row = 1, column = 6, padx = 10, pady = 5)
        ToolTip(autoVenueSelect, msg = VENUE_SELECTION_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ================== SPACER ================== #
        autoSettingsSpacer3 = Label(autoSettingsFrame, bg = BG_COLOR, text = "")
        autoSettingsSpacer3.grid(row = 1, column = 7, padx = 20)

        # Song Checksum
        SONG_ID_TIP = "The checksum of the song to boot into."
        autoSongIDLabel = Label(autoSettingsFrame, text = "Song:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoSongIDLabel.grid(row = 1, column = 8, pady = 5, sticky = 'e')
        ToolTip(autoSongIDLabel, msg = SONG_ID_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        autoSongID = StringVar()
        autoSongIDEntry = TTK.Entry(autoSettingsFrame, width = 25, takefocus = False, textvariable = autoSongID)
        autoSongIDEntry.grid(row = 1, column = 9, padx = 10, pady = 5, sticky = 'w')
        ToolTip(autoSongIDEntry, msg = SONG_ID_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ===========================================================================================================
        # Auto Launch Player Settings
        # ===========================================================================================================
        # Player Settings Frame
        autoPlayerSettingsFrame = Frame(wtdeOptionsAutoLaunch, bg = BG_COLOR)
        autoPlayerSettingsFrame.pack(fill = 'x', anchor = 'n', pady = 5)
     
        # Section Header
        autoPlayerSettingsHeader = Label(autoPlayerSettingsFrame, text = "Player Settings:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO_HEADER, justify = 'left', anchor = 'w')
        autoPlayerSettingsHeader.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

        # Hover tool tips for the various settings for the players.
        P1_SETTINGS_INFO = "Edit the settings for Player 1."
        P2_SETTINGS_INFO = "Edit the settings for Player 2."
        P3_SETTINGS_INFO = "Edit the settings for Player 3."
        P4_SETTINGS_INFO = "Edit the settings for Player 4."
        AUTO_INSTRUMENT_TIP = "Set the instrument to use for this player in auto launch."
        AUTO_DIFFICULTY_TIP = "Set the difficulty this player will use in auto launch."
        AUTO_USE_BOT_TIP = "Should this player have the bot enabled?"

        # ===========================================================================================================
        # Player 1 Settings
        # ===========================================================================================================
        global autoP1SettingsFrame
        autoP1SettingsFrame = Frame(autoPlayerSettingsFrame, bg = BG_COLOR)
        autoP1SettingsFrame.grid(row = 1, column = 0, columnspan = 999, sticky = 'w')

        autoP1SectionLabel = Label(autoP1SettingsFrame, text = "Player 1:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoP1SectionLabel.grid(row = 0, column = 0, padx = 70, pady = 10)
        ToolTip(autoP1SectionLabel, msg = P1_SETTINGS_INFO, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ================== SPACER ================== #
        autoP1SettingsFrameSpacer1 = Label(autoP1SettingsFrame, bg = BG_COLOR, text = "")
        autoP1SettingsFrameSpacer1.grid(row = 0, column = 1)

        # Player 1 Instrument
        autoP1InstrumentLabel = Label(autoP1SettingsFrame, text = "P1 Instrument:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoP1InstrumentLabel.grid(row = 0, column = 2, pady = 5, sticky = 'e')
        ToolTip(autoP1InstrumentLabel, msg = AUTO_INSTRUMENT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        
        autoP1Instrument = StringVar()
        autoP1InstrumentOption = TTK.OptionMenu(autoP1SettingsFrame, autoP1Instrument, *P1_INSTRUMENTS)
        autoP1InstrumentOption.config(width = 25)
        autoP1InstrumentOption.grid(row = 0, column = 3, padx = 10, pady = 5, sticky = 'w')
        ToolTip(autoP1InstrumentOption, msg = AUTO_INSTRUMENT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ================== SPACER ================== #
        autoP1SettingsFrameSpacer2 = Label(autoP1SettingsFrame, bg = BG_COLOR, text = "")
        autoP1SettingsFrameSpacer2.grid(row = 0, column = 4)

        # Player 1 Difficulty
        autoP1DifficultyLabel = Label(autoP1SettingsFrame, text = "P1 Difficulty:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoP1DifficultyLabel.grid(row = 0, column = 5, pady = 5, sticky = 'e')
        ToolTip(autoP1DifficultyLabel, msg = AUTO_DIFFICULTY_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        
        autoP1Difficulty = StringVar()
        autoP1DifficultyOption = TTK.OptionMenu(autoP1SettingsFrame, autoP1Difficulty, *P1_DIFFICULTIES)
        autoP1DifficultyOption.config(width = 10)
        autoP1DifficultyOption.grid(row = 0, column = 6, padx = 10, pady = 5, sticky = 'w')
        ToolTip(autoP1DifficultyOption, msg = AUTO_DIFFICULTY_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # Player 1 Use Bot
        autoP1Bot = StringVar()
        autoP1BotOption = TTK.Checkbutton(autoP1SettingsFrame, text = "Use Bot?", variable = autoP1Bot, onvalue = '1', offvalue = '0')
        autoP1BotOption.grid(row = 0, column = 7, padx = 20, pady = 5)
        ToolTip(autoP1BotOption, msg = AUTO_USE_BOT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ===========================================================================================================
        # Player 2 Settings
        # ===========================================================================================================
        global autoP2SettingsFrame
        autoP2SettingsFrame = Frame(autoPlayerSettingsFrame, bg = BG_COLOR)
        autoP2SettingsFrame.grid(row = 2, column = 0, columnspan = 999, sticky = 'w')

        autoP2SectionLabel = Label(autoP2SettingsFrame, text = "Player 2:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoP2SectionLabel.grid(row = 0, column = 0, padx = 70, pady = 10)
        ToolTip(autoP2SectionLabel, msg = P2_SETTINGS_INFO, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ================== SPACER ================== #
        autoP2SettingsFrameSpacer1 = Label(autoP2SettingsFrame, bg = BG_COLOR, text = "")
        autoP2SettingsFrameSpacer1.grid(row = 0, column = 1)

        # Player 2 Instrument
        autoP2InstrumentLabel = Label(autoP2SettingsFrame, text = "P2 Instrument:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoP2InstrumentLabel.grid(row = 0, column = 2, pady = 5, sticky = 'e')
        ToolTip(autoP2InstrumentLabel, msg = AUTO_INSTRUMENT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        
        autoP2Instrument = StringVar()
        autoP2InstrumentOption = TTK.OptionMenu(autoP2SettingsFrame, autoP2Instrument, *P2_INSTRUMENTS)
        autoP2InstrumentOption.config(width = 25)
        autoP2InstrumentOption.grid(row = 0, column = 3, padx = 10, pady = 5, sticky = 'w')
        ToolTip(autoP2InstrumentOption, msg = AUTO_INSTRUMENT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ================== SPACER ================== #
        autoP2SettingsFrameSpacer2 = Label(autoP2SettingsFrame, bg = BG_COLOR, text = "")
        autoP2SettingsFrameSpacer2.grid(row = 0, column = 4)

        # Player 2 Difficulty
        autoP2DifficultyLabel = Label(autoP2SettingsFrame, text = "P2 Difficulty:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoP2DifficultyLabel.grid(row = 0, column = 5, pady = 5, sticky = 'e')
        ToolTip(autoP2DifficultyLabel, msg = AUTO_DIFFICULTY_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        
        autoP2Difficulty = StringVar()
        autoP2DifficultyOption = TTK.OptionMenu(autoP2SettingsFrame, autoP2Difficulty, *P2_DIFFICULTIES)
        autoP2DifficultyOption.config(width = 10)
        autoP2DifficultyOption.grid(row = 0, column = 6, padx = 10, pady = 5, sticky = 'w')
        ToolTip(autoP2DifficultyOption, msg = AUTO_DIFFICULTY_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # Player 2 Use Bot
        autoP2Bot = StringVar()
        autoP2BotOption = TTK.Checkbutton(autoP2SettingsFrame, text = "Use Bot?", variable = autoP2Bot, onvalue = '1', offvalue = '0')
        autoP2BotOption.grid(row = 0, column = 7, padx = 20, pady = 5)
        ToolTip(autoP2BotOption, msg = AUTO_USE_BOT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ===========================================================================================================
        # Player 3 Settings
        # ===========================================================================================================
        global autoP3SettingsFrame
        autoP3SettingsFrame = Frame(autoPlayerSettingsFrame, bg = BG_COLOR)
        autoP3SettingsFrame.grid(row = 3, column = 0, columnspan = 999, sticky = 'w')

        autoP3SectionLabel = Label(autoP3SettingsFrame, text = "Player 3:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoP3SectionLabel.grid(row = 0, column = 0, padx = 70, pady = 10)
        ToolTip(autoP3SectionLabel, msg = P3_SETTINGS_INFO, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ================== SPACER ================== #
        autoP3SettingsFrameSpacer1 = Label(autoP3SettingsFrame, bg = BG_COLOR, text = "")
        autoP3SettingsFrameSpacer1.grid(row = 0, column = 1)

        # Player 3 Instrument
        autoP3InstrumentLabel = Label(autoP3SettingsFrame, text = "P3 Instrument:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoP3InstrumentLabel.grid(row = 0, column = 2, pady = 5, sticky = 'e')
        ToolTip(autoP3InstrumentLabel, msg = AUTO_INSTRUMENT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        
        autoP3Instrument = StringVar()
        autoP3InstrumentOption = TTK.OptionMenu(autoP3SettingsFrame, autoP3Instrument, *P3_INSTRUMENTS)
        autoP3InstrumentOption.config(width = 25)
        autoP3InstrumentOption.grid(row = 0, column = 3, padx = 10, pady = 5, sticky = 'w')
        ToolTip(autoP3InstrumentOption, msg = AUTO_INSTRUMENT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ================== SPACER ================== #
        autoP3SettingsFrameSpacer2 = Label(autoP3SettingsFrame, bg = BG_COLOR, text = "")
        autoP3SettingsFrameSpacer2.grid(row = 0, column = 4)

        # Player 2 Difficulty
        autoP3DifficultyLabel = Label(autoP3SettingsFrame, text = "P3 Difficulty:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoP3DifficultyLabel.grid(row = 0, column = 5, pady = 5, sticky = 'e')
        ToolTip(autoP3DifficultyLabel, msg = AUTO_DIFFICULTY_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        
        autoP3Difficulty = StringVar()
        autoP3DifficultyOption = TTK.OptionMenu(autoP3SettingsFrame, autoP3Difficulty, *P3_DIFFICULTIES)
        autoP3DifficultyOption.grid(row = 0, column = 6, padx = 10, pady = 5, sticky = 'w')
        autoP3DifficultyOption.config(width = 10)
        ToolTip(autoP3DifficultyOption, msg = AUTO_DIFFICULTY_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # Player 3 Use Bot
        autoP3Bot = StringVar()
        autoP3BotOption = TTK.Checkbutton(autoP3SettingsFrame, text = "Use Bot?", variable = autoP3Bot, onvalue = '1', offvalue = '0')
        autoP3BotOption.grid(row = 0, column = 7, padx = 20, pady = 5)
        ToolTip(autoP3BotOption, msg = AUTO_USE_BOT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ===========================================================================================================
        # Player 4 Settings
        # ===========================================================================================================
        global autoP4SettingsFrame
        autoP4SettingsFrame = Frame(autoPlayerSettingsFrame, bg = BG_COLOR)
        autoP4SettingsFrame.grid(row = 4, column = 0, columnspan = 999, sticky = 'w')

        autoP4SectionLabel = Label(autoP4SettingsFrame, text = "Player 4:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoP4SectionLabel.grid(row = 0, column = 0, padx = 70, pady = 10)
        ToolTip(autoP4SectionLabel, msg = P4_SETTINGS_INFO, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ================== SPACER ================== #
        autoP4SettingsFrameSpacer1 = Label(autoP4SettingsFrame, bg = BG_COLOR, text = "")
        autoP4SettingsFrameSpacer1.grid(row = 0, column = 1)

        # Player 4 Instrument
        autoP4InstrumentLabel = Label(autoP4SettingsFrame, text = "P4 Instrument:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoP4InstrumentLabel.grid(row = 0, column = 2, pady = 5, sticky = 'e')
        ToolTip(autoP4InstrumentLabel, msg = AUTO_INSTRUMENT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        
        autoP4Instrument = StringVar()
        autoP4InstrumentOption = TTK.OptionMenu(autoP4SettingsFrame, autoP4Instrument, *P4_INSTRUMENTS)
        autoP4InstrumentOption.config(width = 25)
        autoP4InstrumentOption.grid(row = 0, column = 3, padx = 10, pady = 5, sticky = 'w')
        ToolTip(autoP4InstrumentOption, msg = AUTO_INSTRUMENT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # ================== SPACER ================== #
        autoP4SettingsFrameSpacer2 = Label(autoP4SettingsFrame, bg = BG_COLOR, text = "")
        autoP4SettingsFrameSpacer2.grid(row = 0, column = 4)

        # Player 4 Difficulty
        autoP4DifficultyLabel = Label(autoP4SettingsFrame, text = "P4 Difficulty:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        autoP4DifficultyLabel.grid(row = 0, column = 5, pady = 5, sticky = 'e')
        ToolTip(autoP4DifficultyLabel, msg = AUTO_DIFFICULTY_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        
        autoP4Difficulty = StringVar()
        autoP4DifficultyOption = TTK.OptionMenu(autoP4SettingsFrame, autoP4Difficulty, *P4_DIFFICULTIES)
        autoP4DifficultyOption.grid(row = 0, column = 6, padx = 10, pady = 5, sticky = 'w')
        autoP4DifficultyOption.config(width = 10)
        ToolTip(autoP4DifficultyOption, msg = AUTO_DIFFICULTY_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # Player 4 Use Bot
        autoP4Bot = StringVar()
        autoP4BotOption = TTK.Checkbutton(autoP4SettingsFrame, text = "Use Bot?", variable = autoP4Bot, onvalue = '1', offvalue = '0')
        autoP4BotOption.grid(row = 0, column = 7, padx = 20, pady = 5)
        ToolTip(autoP4BotOption, msg = AUTO_USE_BOT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        auto_update_players(autoPlayerCount.get())

    # Add settings into the advanced Auto Launch Settings.
    class AutoLaunch_Advanced():
        """ Advanced settings for the Auto Launch tab. """
        autoAdvancedSettingsFrame = Frame(wtdeOptionsAutoLaunch, bg = BG_COLOR)
        autoAdvancedSettingsFrame.pack(fill = 'x', pady = 5, anchor = 'n')
        
        # Title label.
        autoAdvancedSettingsTitle = Label(autoAdvancedSettingsFrame, text = "Advanced Settings:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO_HEADER, justify = 'left', anchor = 'w')
        autoAdvancedSettingsTitle.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

        # Use Raw PAK Loading
        autoRawLoad = StringVar()
        RAW_LOAD_TIP = "Turn ON or OFF raw loading of the venue.\n\n" \
                       "In its essence, this will load the zone PAK, but will not try and set it up\n" \
                       "as a song or load into a game mode. Good for creating custom venues and\n" \
                       "testing if the SCN and TEX files are working properly!"
        autoUseRawLoad = TTK.Checkbutton(autoAdvancedSettingsFrame, text = "Use Raw PAK Loading", variable = autoRawLoad, onvalue = '1', offvalue = '0')
        autoUseRawLoad.grid(row = 1, column = 0, padx = 20, pady = 5)
        ToolTip(autoUseRawLoad, msg = RAW_LOAD_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        # Song Time
        autoSongTime = StringVar()
        SONG_TIME_TIP = "Show the song time on-screen. The time is shown in seconds."
        autoShowSongTime = TTK.Checkbutton(autoAdvancedSettingsFrame, text = "Show Song Time", variable = autoSongTime, onvalue = '1', offvalue = '0')
        autoShowSongTime.grid(row = 1, column = 1, padx = 20, pady = 5)
        ToolTip(autoShowSongTime, msg = SONG_TIME_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Add general and advanced settings tab.
    AutoLaunch_General()
    AutoLaunch_Advanced()

# Execute tab code.
AutoLaunch()

# ===========================================================================================================
# Credits Tab
# 
# Used for the credits for GHWT: DE and the launcher.
# ===========================================================================================================
# Main CreditsTab class.
class CreditsTab():
    """
    Credits tab class.
    \n
    The class responsible for displaying the GHWT: DE credits information.
    """
    # Show the WTDE logo.
    creditsWTDELogo = Label(wtdeOptionsCredits, bg = BG_COLOR, image = ImageConst.WTDE_LOGO, compound = 'center', anchor = 'center')
    creditsWTDELogo.pack(fill = 'x')

    # First line of credits text.
    TAB_CREDITS_TEXT1 = f"GH World Tour: Definitive Edition Launcher++ by IMF24 - Version {VERSION}\n\n" \
                        "GHWT: DE Developed by Fretworks, EST. 2021\n\n" \
                        "🧪 ✨ WTDE Developers ✨ 🧪"
    creditsTextLine1 = Label(wtdeOptionsCredits, bg = BG_COLOR, fg = FG_COLOR, text = TAB_CREDITS_TEXT1, font = FONT_INFO, justify = 'center')
    creditsTextLine1.pack(fill = 'x', pady = 10)

    # Credits members frame.
    creditsMembersFrame = Frame(wtdeOptionsCredits, bg = BG_COLOR)
    creditsMembersFrame.pack(fill = 'x', anchor = 'center', padx = 40)

    # Add the names of the members of the WTDE team into the frame.
    wtde_add_credits(creditsMembersFrame, 'WTDECreditsNames.csv')

    # Second line of credits text.
    TAB_CREDITS_TEXT2 = "A special thanks to our development testers and of course, all of you, the players, modders, content creators, and everything in between!\n\n" \
                        "Making your Guitar Hero World Tour experience better, one update at a time!\n\n" \
                        "GHWT: DE and Fretworks are not associated with Activision, Neversoft, or RedOctane in any way, shape, or form.\n" \
                        "GHWT: DE is and always will be a non-profit fan-made project."
    creditsTextLine2 = Label(wtdeOptionsCredits, bg = BG_COLOR, fg = FG_COLOR, text = TAB_CREDITS_TEXT2, font = FONT_INFO, justify = 'center')
    creditsTextLine2.pack(fill = 'x', pady = 10)

# Execute tab code.
CreditsTab()

# ===========================================================================================================
# Start Program
# 
# Start the execution of the program (mainloop of Tk).
# ===========================================================================================================
# Load config data.
debug_add_entry("[BS4, ConfigParser] Importing GHWT: DE settings...")
wtde_load_config()

# Enter main loop.
debug_add_entry("[Tk] Entering main loop.")
root.mainloop()

debug_add_entry("[Tk] Exited main loop of Tk; program was closed!")

# Save debug log.
debug_add_entry("[exit] Saving debug log in working directory as dbg_launcher.txt")
save_debug()