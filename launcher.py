# ================================================================================================================= #
#                                                                                                                   #
#  __          _________ _____  ______     _              _    _ _   _  _____ _    _ ______ _____                   #
#  \ \        / /__   __|  __ \|  ____|   | |        /\  | |  | | \ | |/ ____| |  | |  ____|  __ \  _     _         #
#   \ \  /\  / /   | |  | |  | | |__      | |       /  \ | |  | |  \| | |    | |__| | |__  | |__) || |_ _| |_       #
#    \ \/  \/ /    | |  | |  | |  __|     | |      / /\ \| |  | | . ` | |    |  __  |  __| |  _  /_   _|_   _|      #
#     \  /\  /     | |  | |__| | |____    | |____ / ____ \ |__| | |\  | |____| |  | | |____| | \ \ |_|   |_|        #
#      \/  \/      |_|  |_____/|______|   |______/_/    \_\____/|_| \_|\_____|_|  |_|______|_|  \_\                 #
#                                                                                                                   #
#         Coded by IMF24               Guitar Hero World Tour: Definitive Edition by Fretworks EST. 2021            #
#                                                                                                                   #
#                                      Updater Coded by Zedek the Plague Doctor™                                    #
# ================================================================================================================= #
# Import required modules.
from tkinter import *
from tkinter.font import *
from tkinter import ttk, filedialog, messagebox
from tkinterweb import *
from idlelib.tooltip import Hovertip
from PIL import Image, ImageTk
import os as OS
import sys as SYS
import subprocess as SP
import winshell as WS
from win32com.client import Dispatch
from win32api import GetSystemMetrics
import requests as REQ
import zipfile as ZIP
import configparser as CF
from bs4 import BeautifulSoup
import pyaudio as PA
from screeninfo import get_monitors

# Version of the program.
VERSION = "1.0 Beta"

# Original working directory.
OWD = OS.getcwd()

# Set up ConfigParser.
config = CF.ConfigParser(comment_prefixes = ('#', ';'), allow_no_value = True)
config.optionxform = str

# Argument parser at the command line.
def arg_cmd_parse() -> None:
    args = SYS.argv

    # Set up console colors.
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

    # Help message.
    HELP_INFO = "-=-=-=-=-=-=- GHWT: Definitive Edition Launcher++ -=-=-=-=-=-=-\n" \
                "You've entered the debug mode for the GHWT: DE Launcher++!\n" \
                "List of command line arguments:\n" \
                "[-h] [--help]          - Print this message.\n" \
                "[-i] [--ini]           - Update a setting in GHWTDE.ini.\n" \
                "[-u] [--update]        - Update WTDE to the latest version.\n" \
                "[-d] [--dir]           - Edit your defined install path to WTDE.\n" \
                "[-r] [--normal]        - Run normally."
    
    if (len(args) > 1):
        def print_help() -> None:
            """ Print command line help information. """
            print(HELP_INFO)
            SYS.exit(0)

        def ini_edit_cmd() -> None:
            """ Update a setting in GHWTDE.ini at the command line. """
            match (len(args)):
                case 2: print(f"{YELLOW}Usage: --ini <section> <option> <value>{WHITE}")

                case 3: print(f"{RED}Invalid argument count! Usage: --ini <section> <option> <value>{WHITE}")

                case 4: print(f"{RED}Invalid argument count! Usage: --ini <section> <option> <value>{WHITE}")

                case 5:
                    print(f"{YELLOW}Attempting to edit option {args[3]} in section {args[2]}...{WHITE}")
                    
                    OS.chdir(wtde_find_config())

                    config.read("GHWTDE.ini")

                    if (not config.has_section(args[2])):
                        print(f"{RED}Error: Section does not exist!{WHITE}")
                        SYS.exit(0)

                    if (not config.has_option(args[2], args[3])):
                        print(f"{RED}Error: Option does not exist!{WHITE}")
                        SYS.exit(0)

                    print("Value found! Modifying...")

                    config.set(args[2], args[3], args[4])

                    print(f"Changed option {args[3]} with value {args[4]}")
                    print("Writing new data...")

                    with (open("GHWTDE.ini", 'w')) as cnf: config.write(cnf)

                    print(f"{GREEN}Update complete! The option {args[3]} should be updated.{WHITE}")

                    SYS.exit(0)


            SYS.exit(0)

        match (args[1]):
            case "-h" | "--help": print_help()

            case "-i" | "--ini": ini_edit_cmd()

            case "-u" | "--update":
                wtde_run_updater()
                SYS.exit(0)

            case "-r" | "--normal": pass

            case _:
                print(f"Unknown argument: {args[1]}. Type -h or --help for a list of parameters.")
                SYS.exit(0)

# Relative path function.
def resource_path(relative_path: str) -> str:
    """ Get the absolute path to a given resource. """
    try:
        base_path = SYS._MEIPASS
    except Exception:
        base_path = OS.path.abspath(".")

    return OS.path.join(base_path, relative_path)

# Verify file presence.
def verify_files() -> None:
    """ Runs file verification. """
    # Is there an Updater.ini file already present?
    if (OS.path.exists("Updater.ini")): pass # print("Config file exists!")

    # If not, create a new, unconfigured INI file.
    else:
        print("No config file exists! Writing new config...")

        config.write(open('Updater.ini', 'w'))

        config["Updater"] = {
            "GameDirectory" : ""
        }

        with open("Updater.ini", 'w') as cnf:
            config.write(cnf)

        print("New config file successfully created!")

    # Has the installation path to WTDE been defined?
    config.read("Updater.ini")

    wtdePathGet = ""

    if (config.has_option("Updater", "GameDirectory")): wtdePathGet = config.get("Updater", "GameDirectory")
    else:
        config["Updater"] = { "GameDirectory" : "" }

    if (wtdePathGet == ""):
        # Try and auto detect the path.
        if (not OS.path.exists("GHWT.exe")):
            messagebox.showerror("GHWT Path Not Defined", "You have not specified your Guitar Hero World Tour installation path!\n\nNavigate to the folder that contains GHWT.exe.")

            wtdeDir = filedialog.askdirectory()

            while (not OS.path.exists(f"{wtdeDir}/GHWT.exe")):
                messagebox.showerror("GHWT.exe Not Detected", "This folder does not contain GHWT.exe.\n\nNavigate to the folder that contains GHWT.exe.")
                wtdeDir = filedialog.askdirectory()
            else:
                messagebox.showinfo("GHWT.exe Detected", "GHWT.exe was successfully found!")

            config.set("Updater", "GameDirectory", wtdeDir)

        else:
            config.set("Updater", "GameDirectory", OS.getcwd())

        with open("Updater.ini", 'w') as updaterConfig:
            config.write(updaterConfig)

# Create WTDE shortcut on desktop.
def wtde_create_lnk() -> bool:
    """ Makes a shortcut to WTDE on the desktop. """
    oldDir = OS.getcwd()
    OS.chdir(OWD)
    config.read("Updater.ini")

    wtdeDir = config.get("Updater", "GameDirectory")
    wtdeExeDir = wtdeDir + "/GHWT_Definitive.exe"

    if (not OS.path.exists(wtdeExeDir)):
        messagebox.showerror("GHWT_Definitive.exe Not Found", "GHWT_Definitive.exe was not found. Either WTDE is not installed or the executable for WTDE was moved or deleted.")
        
        OS.chdir(oldDir)
        
        return False
    else:
        desktop = WS.desktop()
        shortcutPath = OS.path.join(desktop, "Guitar Hero World Tour Definitive Edition.lnk")
        targetPath = wtdeExeDir
        workingDir = wtdeDir
        iconDir = wtdeExeDir

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcutPath)
        shortcut.TargetPath = targetPath
        shortcut.WorkingDirectory = workingDir
        shortcut.IconLocation = iconDir
        shortcut.save()

        OS.chdir(oldDir)

        return True

# Save configuration settings and run WTDE.
def wtde_run_save() -> None:
    """ Save the current configuration settings and run WTDE. """
    oldDir = OS.getcwd()

    wtde_save_config()

    root.destroy()

    OS.chdir(OWD)

    config.read("Updater.ini")

    wtdeDir = config.get("Updater", "GameDirectory")

    OS.chdir(wtdeDir)

    OS.system(".\\GHWT_Definitive.exe")

# Save configuration settings.
def wtde_save_config() -> None:
    """ Save the current configuration settings, including keyboard mappings. """
    # Change working directory to our INI directory.
    OS.chdir(wtde_find_config())
    config.read("GHWTDE.ini")

    # Used on options where the inverse may be given.
    valueToSet = "0"

    # ===================== SAVE GENERAL SETTINGS ===================== #
    config.set("Config", "RichPresence", richPresence.get())

    config.set("Config", "AllowHolidays", allowHolidays.get())

    config.set("Audio", "WhammyPitchShift", whammyPitchShift.get())

    config.set("Config", "Language", wtde_convert_language(language.get()))

    config.set("Config", "UseCareerOption", useCareerOption.get())

    config.set("Config", "UseQuickplayOption", useQuickplayOption.get())

    config.set("Config", "UseHeadToHeadOption", useHeadToHeadOption.get())

    config.set("Config", "UseOnlineOption", useOnlineOption.get())

    config.set("Config", "UseMusicStudioOption", useMusicStudioOption.get())

    config.set("Config", "UseCAROption", useCAROption.get())

    config.set("Config", "UseOptionsOption", useOptionsOption.get())

    config.set("Config", "UseQuitOption", useQuitOption.get())

    # ===================== SAVE GRAPHICS SETTINGS ===================== #
    config.set("Graphics", "UseNativeRes", useNativeResolution.get())

    config.set("Graphics", "FPSLimit", wtde_get_fps_limit())

    if (disableVSync.get() == "0"): valueToSet = "1"
    else: valueToSet = "0"
    config.set("Graphics", "DisableVSync", valueToSet)

    config.set("Graphics", "HitSparks", hitSparks.get())

    if (disableDOF.get() == "0"): valueToSet = "1"
    else: valueToSet = "0"
    config.set("Graphics", "DisableDOF", valueToSet)

    config.set("Graphics", "WindowedMode", windowedMode.get())

    config.set("Graphics", "Borderless", borderlessMode.get())

    if (bloomFX.get() == "0"): valueToSet = "1"
    else: valueToSet = "0"
    config.set("Graphics", "DisableBloom", valueToSet)

    config.set("Graphics", "ColorFilters", colorFilters.get())

    config.set("Graphics", "AntiAliasing", antiAliasing.get())

    config.set("Graphics", "RenderParticles", renderParticles.get())

    config.set("Graphics", "RenderGeoms", renderGeoms.get())

    config.set("Graphics", "RenderInstances", renderInstances.get())

    config.set("Graphics", "DrawProjectors", drawProjectors.get())

    config.set("Graphics", "Render2D", render2D.get())

    config.set("Graphics", "RenderScreenFX", renderScreenFX.get())

    config.set("Graphics", "BlackStage", blackStage.get())

    config.set("Graphics", "HideBand", hideBand.get())

    config.set("Graphics", "HideInstruments", hideInstruments.get())

    config.set("Graphics", "GemTheme", wtde_save_note_info('style'))

    config.set("Graphics", "GemColors", wtde_save_note_info('color'))

    # ===================== SAVE BAND SETTINGS ===================== #
    config.set("Band", "PreferredGuitarist", bandPreferredGuitaristEntry.get())

    config.set("Band", "PreferredBassist", bandPreferredBassistEntry.get())

    config.set("Band", "PreferredDrummer", bandPreferredDrummerEntry.get())

    config.set("Band", "PreferredSinger", bandPreferredVocalistEntry.get())

    config.set("Band", "PreferredStage", auto_save_venue(preferredVenue.get()))

    config.set("Band", "PreferredGuitaristHighway", bandPreferredGuitaristHighwayEntry.get())

    config.set("Band", "PreferredBassistHighway", bandPreferredBassistHighwayEntry.get())

    config.set("Band", "PreferredDrummerHighway", bandPreferredDrummerHighwayEntry.get())

    # ===================== SAVE AUTO LAUNCH SETTINGS ===================== #
    config.set("AutoLaunch", "Enabled", enableAutoLaunch.get())
    
    config.set("AutoLaunch", "HideHUD", hideHUDAuto.get())

    config.set("AutoLaunch", "SongTime", songTime.get())

    config.set("AutoLaunch", "RawLoad", rawLoad.get())

    config.set("AutoLaunch", "Players", playerCount.get())

    config.set("AutoLaunch", "Venue", auto_save_venue(venueSelection.get()))

    config.set("AutoLaunch", "Song", autoSongEntry.get())

    config.set("AutoLaunch", "Difficulty", auto_get_diff(autoDifficulty1.get()))
    config.set("AutoLaunch", "Difficulty2", auto_get_diff(autoDifficulty2.get()))
    config.set("AutoLaunch", "Difficulty3", auto_get_diff(autoDifficulty3.get()))
    config.set("AutoLaunch", "Difficulty4", auto_get_diff(autoDifficulty4.get()))

    config.set("AutoLaunch", "Part", auto_get_part(autoInstrument1.get()))
    config.set("AutoLaunch", "Part2", auto_get_part(autoInstrument2.get()))
    config.set("AutoLaunch", "Part3", auto_get_part(autoInstrument3.get()))
    config.set("AutoLaunch", "Part4", auto_get_part(autoInstrument4.get()))

    config.set("AutoLaunch", "Bot", autoBot1.get())
    config.set("AutoLaunch", "Bot2", autoBot2.get())
    config.set("AutoLaunch", "Bot3", autoBot3.get())
    config.set("AutoLaunch", "Bot4", autoBot4.get())

    # ===================== SAVE DEBUG SETTINGS ===================== #
    config.set("Debug", "FixNoteLimit", fixNoteLimit.get())

    config.set("Debug", "FixMemoryHandler", fixMemoryHandler.get())

    config.set("Logger", "Console", loggerConsole.get())

    config.set("Logger", "WriteFile", writeFile.get())

    config.set("Logger", "DisableSongLogging", disableSongLogging.get())

    config.set("Logger", "DebugDLCSync", debugDLCSync.get())

    config.set("Debug", "FixFSBObjects", fixFSBObjects.get())
    
    # ===================== SAVE INPUT AND OTHER SETTINGS ===================== #
    # Last, we'll save our input & other graphics settings.
    config.set("Audio", "MicDevice", micDevice.get())

    config.set("Audio", "VocalAdjustment", input_filter_numeric(inputMicDelayEntry.get()))

    if (inputHack.get() == "1"): config.set("Debug", "DisableInputHack", "0")
    else: config.set("Debug", "DisableInputHack", "1")

    with (open("GHWTDE.ini", 'w')) as cnf: config.write(cnf)

    # ========== READ XML DATA ========== #
    # Open the XML file and read its data.
    with (open(f"{wtde_find_appdata()}\\AspyrConfig.xml", 'rb')) as xml: aspyrConfigData = xml.read()

    # Run BS4 on this data.
    aspyrConfigDataBS = BeautifulSoup(aspyrConfigData, 'xml')

    # ========== SAVE RESOLUTION ========== #
    resWidthXML = aspyrConfigDataBS.find('s', {"id": "Video.Width"})
    resHeightXML = aspyrConfigDataBS.find('s', {"id": "Video.Height"})
    audioBuffLenXML = aspyrConfigDataBS.find('s', {"id": "Audio.BuffLen"})
    if (useNativeResolution.get() == "0"):
        resWidthXML.string = graphicsResolutionWidth.get()
        resHeightXML.string = graphicsResolutionHeight.get()
    else:
        resWidthXML.string = str(get_screen_resolution()[0])
        resHeightXML.string = str(get_screen_resolution()[1])

    audioBuffLenXML.string = audioBuffLenOption.get()

    # ========== GUITAR INPUTS ========== #
    guitarInputString = ""

    # GREEN
    guitarInputString += "GREEN " + wtde_encode_input(inputKeyGuitarGreenEntry.get()) + " "
    # RED
    guitarInputString += "RED " + wtde_encode_input(inputKeyGuitarRedEntry.get()) + " "
    # YELLOW
    guitarInputString += "YELLOW " + wtde_encode_input(inputKeyGuitarYellowEntry.get()) + " "
    # BLUE
    guitarInputString += "BLUE " + wtde_encode_input(inputKeyGuitarBlueEntry.get()) + " "
    # ORANGE
    guitarInputString += "ORANGE " + wtde_encode_input(inputKeyGuitarOrangeEntry.get()) + " "
    # STAR
    guitarInputString += "STAR " + wtde_encode_input(inputKeyGuitarSPEntry.get()) + " "
    # CANCEL
    guitarInputString += "CANCEL " + wtde_encode_input(inputKeyGuitarCancelEntry.get()) + " "
    # START
    guitarInputString += "START " + wtde_encode_input(inputKeyGuitarStartEntry.get()) + " "
    # BACK
    guitarInputString += "BACK " + wtde_encode_input(inputKeyGuitarBackEntry.get()) + " "
    # DOWN
    guitarInputString += "DOWN " + wtde_encode_input(inputKeyGuitarDownEntry.get()) + " "
    # UP
    guitarInputString += "UP " + wtde_encode_input(inputKeyGuitarUpEntry.get()) + " "
    # WHAMMY
    guitarInputString += "WHAMMY " + wtde_encode_input(inputKeyGuitarWhammyEntry.get()) + " "
    # LEFT
    guitarInputString += "LEFT " + wtde_encode_input(inputKeyGuitarLeftEntry.get()) + " "
    # RIGHT
    guitarInputString += "RIGHT " + wtde_encode_input(inputKeyGuitarRightEntry.get()) + " "

    # Modify the string in the AspyrConfig.xml file to the newly created one that will be assigned to Keyboard_Guitar.
    keyGuitarStringXML = aspyrConfigDataBS.find('s', {"id": "Keyboard_Guitar"})
    keyGuitarStringXML.string = guitarInputString

    # ========== DRUM INPUTS ========== #
    drumInputString = ""

    # RED
    drumInputString += "RED " + wtde_encode_input(inputKeyDrumsRedEntry.get()) + " "
    # YELLOW
    drumInputString += "YELLOW " + wtde_encode_input(inputKeyDrumsYellowEntry.get()) + " "
    # BLUE
    drumInputString += "BLUE " + wtde_encode_input(inputKeyDrumsBlueEntry.get()) + " "
    # ORANGE
    drumInputString += "ORANGE " + wtde_encode_input(inputKeyDrumsOrangeEntry.get()) + " "
    # GREEN
    drumInputString += "GREEN " + wtde_encode_input(inputKeyDrumsGreenEntry.get()) + " "
    # CANCEL
    drumInputString += "CANCEL " + wtde_encode_input(inputKeyDrumsCancelEntry.get()) + " "
    # START
    drumInputString += "START " + wtde_encode_input(inputKeyDrumsStartEntry.get()) + " "
    # BACK
    drumInputString += "BACK " + wtde_encode_input(inputKeyDrumsBackEntry.get()) + " "
    # DOWN
    drumInputString += "DOWN " + wtde_encode_input(inputKeyDrumsDownEntry.get()) + " "
    # UP
    drumInputString += "UP " + wtde_encode_input(inputKeyDrumsUpEntry.get()) + " "
    # WHAMMY (unused)
    drumInputString += "WHAMMY 999 "
    # KICK
    drumInputString += "KICK " + wtde_encode_input(inputKeyDrumsKickEntry.get()) + " "

    # Modify the string in the AspyrConfig.xml file to the newly created one that will be assigned to Keyboard_Drum.
    keyDrumStringXML = aspyrConfigDataBS.find('s', {"id": "Keyboard_Drum"})
    keyDrumStringXML.string = drumInputString

    # ========== MIC INPUTS ========== #
    micInputString = ""

    # GREEN
    micInputString += "GREEN " + wtde_encode_input(inputKeyMicGreenEntry.get()) + " "
    # RED
    micInputString += "RED " + wtde_encode_input(inputKeyMicRedEntry.get()) + " "
    # YELLOW
    micInputString += "YELLOW " + wtde_encode_input(inputKeyMicYellowEntry.get()) + " "
    # BLUE
    micInputString += "BLUE " + wtde_encode_input(inputKeyMicBlueEntry.get()) + " "
    # ORANGE
    micInputString += "ORANGE " + wtde_encode_input(inputKeyMicOrangeEntry.get()) + " "
    # CANCEL
    micInputString += "CANCEL " + wtde_encode_input(inputKeyMicCancelEntry.get()) + " "
    # START
    micInputString += "START " + wtde_encode_input(inputKeyMicStartEntry.get()) + " "
    # BACK
    micInputString += "BACK " + wtde_encode_input(inputKeyMicBackEntry.get()) + " "
    # DOWN
    micInputString += "DOWN " + wtde_encode_input(inputKeyMicDownEntry.get()) + " "
    # UP
    micInputString += "UP " + wtde_encode_input(inputKeyMicUpEntry.get()) + " "
    # MIC_VOL_DOWN
    micInputString += "MIC_VOL_DOWN " + wtde_encode_input(inputKeyMicMVDEntry.get()) + " "

    # Modify the string in the AspyrConfig.xml file to the newly created one that will be assigned to Keyboard_Mic.
    keyMicStringXML = aspyrConfigDataBS.find('s', {"id": "Keyboard_Mic"})
    keyMicStringXML.string = micInputString

    # ========== MENU INPUTS ========== #
    menuInputString = ""

    # GREEN
    menuInputString += "GREEN " + wtde_encode_input(inputKeyMenuGreenEntry.get()) + " "
    # RED
    menuInputString += "RED " + wtde_encode_input(inputKeyMenuRedEntry.get()) + " "
    # YELLOW
    menuInputString += "YELLOW " + wtde_encode_input(inputKeyMenuYellowEntry.get()) + " "
    # BLUE
    menuInputString += "BLUE " + wtde_encode_input(inputKeyMenuBlueEntry.get()) + " "
    # ORANGE
    menuInputString += "ORANGE " + wtde_encode_input(inputKeyMenuOrangeEntry.get()) + " "
    # CANCEL
    menuInputString += "CANCEL " + wtde_encode_input(inputKeyMenuCancelEntry.get()) + " "
    # START
    menuInputString += "START " + wtde_encode_input(inputKeyMenuStartEntry.get()) + " "
    # BACK
    menuInputString += "BACK " + wtde_encode_input(inputKeyMenuBackEntry.get()) + " "
    # DOWN
    menuInputString += "DOWN " + wtde_encode_input(inputKeyMenuDownEntry.get()) + " "
    # UP
    menuInputString += "UP " + wtde_encode_input(inputKeyMenuUpEntry.get()) + " "
    # WHAMMY
    menuInputString += "WHAMMY " + wtde_encode_input(inputKeyMenuWhammyEntry.get()) + " "
    # KICK
    menuInputString += "KICK " + wtde_encode_input(inputKeyMenuKickEntry.get()) + " "
    # LEFT
    menuInputString += "LEFT " + wtde_encode_input(inputKeyMenuLeftEntry.get()) + " "
    # RIGHT
    menuInputString += "RIGHT " + wtde_encode_input(inputKeyMenuRightEntry.get()) + " "

    # Modify the string in the AspyrConfig.xml file to the newly created one that will be assigned to Keyboard_Menu.
    keyMenuStringXML = aspyrConfigDataBS.find('s', {"id": "Keyboard_Menu"})
    keyMenuStringXML.string = menuInputString

    # After all new strings have been created, write it all back in.
    with (open(f"{wtde_find_appdata()}\\AspyrConfig.xml", 'w', encoding = "utf-8")) as xml: xml.write(str(aspyrConfigDataBS))

# Get FPS value from user's settings.
def wtde_get_fps_limit() -> str:
    """ Returns the FPS limit set by the user in the FPS Limit Graphics Settings option. """
    # Get the value from the FPS limit dropdown.
    match (fpsLimit.get()):
        case "15 FPS":          return "15"
        case "24 FPS":          return "24"
        case "30 FPS":          return "30"
        case "60 FPS":          return "60"
        case "120 FPS":         return "120"
        case "240 FPS":         return "240"
        case "Unlimited":       return "0"
        case _:                 return "0"

# Get the instrument checksum from a given part.
def auto_get_part(part: str) -> str:
    """ Take a given instrument and return its part checksum. """
    # Use the variable to match what it's supposed to be.
    match (part):
        case "Lead Guitar - PART GUITAR":       return "guitar"
        case "Bass Guitar - PART BASS":         return "bass"
        case "Drums - PART DRUMS":              return "drum"
        case "Vocals - PART VOCALS":            return "vocals"
        case _:                                 return ""

# Get the difficulty from a given selector.
def auto_get_diff(diff: str) -> str:
    """ Take a given difficulty and return its difficulty checksum. """
    # Use the variable to match what it's supposed to be.
    match (diff):
        case "Beginner":    return "easy_rhythm"
        case "Easy":        return "easy"
        case "Medium":      return "medium"
        case "Hard":        return "hard"
        case "Expert":      return "expert"
        case _:             return ""

# Get the venue from the venue selection.
def auto_save_venue(venue: str) -> str:
    """ Take the variable holding the selected Auto Launch venue and convert it to its zone PAK name. """
    # Return the actual venue name.
    match (venue):
        case "Phi Psi Kappa":       return "z_frathouse"
        case "Wilted Orchid":       return "z_goth"
        case "Bone Church":         return "z_cathedral"
        case "Pang Tang Bay":       return "z_harbor"
        case "Amoeba Records":      return "z_recordstore"
        case "Tool":                return "z_tool"
        case "Swamp Shack":         return "z_bayou"
        case "Rock Brigade":        return "z_military"
        case "Strutter's Farm":     return "z_fairgrounds"
        case "House of Blues":      return "z_hob"
        case "Ted's Tiki Hut":      return "z_hotel"
        case "Will Heilm's Keep":   return "z_castle"
        case "Recording Studio":    return "z_studio2"
        case "AT&T Park":           return "z_ballpark"
        case "Tesla's Coil":        return "z_scifi"
        case "Ozzfest":             return "z_metalfest"
        case "Times Square":        return "z_newyork"
        case "Sunna's Chariot":     return "z_credits"
        case _:
            if (not venue == "") and (not venue == "None"): return venue
            else: return ""

# Load configuration settings.
def wtde_load_config() -> None:
    """
    This loads all configuration data from the GHWTDE.ini and AspyrConfig.xml files.
    \n
    The load order is as follows:
    - Loads all configuration data from GHWTDE.ini first, populating all options that are saved in the INI.
    - Loads all configuration data from AspyrConfig.xml, including keyboard inputs and other settings not saved in the GHWTDE.ini.
    \n
    This doesn't return anything, but will populate all settings boxes with their transferred values.
    """
    # Load general settings.
    oldDir = OS.getcwd()
    OS.chdir(wtde_find_config())

    # Read config file.
    config.read("GHWTDE.ini")

    # ===================== GENERAL ===================== #

    # Load rich presence.
    if (config.get("Config", "RichPresence") == "1"): generalRichPresence.select()
    else: generalRichPresence.deselect()

    # Load allow holidays.
    if (config.get("Config", "AllowHolidays") == "1"): generalAllowHolidays.select()
    else: generalAllowHolidays.deselect()

    # Load whammy pitch shift.
    if (config.get("Audio", "WhammyPitchShift") == "1"): generalWhammyPitchShift.select()
    else: generalWhammyPitchShift.deselect()

    # Load language.
    match (config.get("Config", "Language")):
        case "en":     language.set(languages[0])
        case "es":     language.set(languages[1])
        case "it":     language.set(languages[2])
        case "fr":     language.set(languages[3])
        case "de":     language.set(languages[4])
        case "ja":     language.set(languages[5])
        case "ko":     language.set(languages[6])
        case _:        language.set(languages[0])

    useCareerOption.set(config.get("Config", "UseCareerOption"))

    useQuickplayOption.set(config.get("Config", "UseQuickplayOption"))

    useHeadToHeadOption.set(config.get("Config", "UseHeadToHeadOption"))

    useOnlineOption.set(config.get("Config", "UseOnlineOption"))

    useMusicStudioOption.set(config.get("Config", "UseMusicStudioOption"))

    useCAROption.set(config.get("Config", "UseCAROption"))

    useOptionsOption.set(config.get("Config", "UseOptionsOption"))

    useQuitOption.set(config.get("Config", "UseQuitOption"))

    # ===================== GRAPHICS ===================== #
    useNativeResolution.set(config.get("Graphics", "UseNativeRes"))

    if (config.get("Graphics", "FPSLimit") == "0"): fpsLimit.set("Unlimited")
    else: fpsLimit.set(config.get("Graphics", "FPSLimit") + " FPS")

    if (config.get("Graphics", "DisableVSync") == "1"): graphicsUseVSync.deselect()
    else: graphicsUseVSync.select()

    hitSparks.set(config.get("Graphics", "HitSparks"))

    if (config.get("Graphics", "DisableDOF") == "0"): disableDOF.set("1")

    windowedMode.set(config.get("Graphics", "WindowedMode"))

    borderlessMode.set(config.get("Graphics", "Borderless"))

    if (config.get("Graphics", "DisableBloom") == "0"): bloomFX.set("1")

    colorFilters.set(config.get("Graphics", "ColorFilters"))

    antiAliasing.set(config.get("Graphics", "AntiAliasing"))

    renderParticles.set(config.get("Graphics", "RenderParticles"))

    renderGeoms.set(config.get("Graphics", "RenderGeoms"))

    renderInstances.set(config.get("Graphics", "RenderInstances"))

    drawProjectors.set(config.get("Graphics", "DrawProjectors"))

    render2D.set(config.get("Graphics", "Render2D"))

    renderScreenFX.set(config.get("Graphics", "RenderScreenFX"))

    blackStage.set(config.get("Graphics", "BlackStage"))

    hideBand.set(config.get("Graphics", "HideBand"))

    hideInstruments.set(config.get("Graphics", "HideInstruments"))

    noteStyle.set(wtde_get_note_info('style'))

    noteTheme.set(wtde_get_note_info('color'))

    introStyle.set(wtde_get_intro_load('intro'))

    # ===================== INPUT ===================== #
    inputMicDelayEntry.insert(0, config.get("Audio", "VocalAdjustment"))

    inputMicVideoDelayEntry.insert(0, audioVisualLag)

    if (config.get("Debug", "DisableInputHack") == "1"): inputUseInputHack.deselect()
    else: inputUseInputHack.select()

    # ===================== BAND ===================== #
    guitarStrumAnim.set(wtde_get_game(config.get("Band", "GuitarStrumAnim")))
    
    bassStrumAnim.set(wtde_get_game(config.get("Band", "BassStrumAnim")))

    # ===================== AUTO LAUNCH ===================== #
    enableAutoLaunch.set(config.get("AutoLaunch", "Enabled"))
    auto_launch_status()

    hideHUDAuto.set(config.get("AutoLaunch", "HideHUD"))

    playerCount.set(config.get("AutoLaunch", "Players"))

    venueSelection.set(auto_get_venue(config.get("AutoLaunch", "Venue")))

    autoSongEntry.insert(0, config.get("AutoLaunch", "Song"))

    # Player 1
    autoInstrument1.set(auto_inst_diff("Part"))

    autoDifficulty1.set(auto_inst_diff("Difficulty"))

    autoBot1.set(config.get("AutoLaunch", "Bot"))

    # Player 2
    autoInstrument2.set(auto_inst_diff("Part2"))

    autoDifficulty2.set(auto_inst_diff("Difficulty2"))

    autoBot2.set(config.get("AutoLaunch", "Bot2"))

    # Player 3
    autoInstrument3.set(auto_inst_diff("Part3"))

    autoDifficulty3.set(auto_inst_diff("Difficulty3"))

    autoBot3.set(config.get("AutoLaunch", "Bot3"))

    # Player 4
    autoInstrument4.set(auto_inst_diff("Part4"))

    autoDifficulty4.set(auto_inst_diff("Difficulty4"))

    autoBot4.set(config.get("AutoLaunch", "Bot4"))

    # Advanced Settings
    rawLoad.set(config.get("AutoLaunch", "RawLoad"))

    songTime.set(config.get("AutoLaunch", "RawLoad"))

    # ===================== DEBUG ===================== #
    fixNoteLimit.set(config.get("Debug", "FixNoteLimit"))

    fixMemoryHandler.set(config.get("Debug", "FixMemoryHandler"))

    loggerConsole.set(config.get("Logger", "Console"))

    writeFile.set(config.get("Logger", "WriteFile"))

    disableSongLogging.set(config.get("Logger", "DisableSongLogging"))

    debugDLCSync.set(config.get("Logger", "DebugDLCSync"))

    fixFSBObjects.set(config.get("Debug", "FixFSBObjects"))

    # Revert working directory.
    OS.chdir(oldDir)

# Verify configuration fields.
def wtde_verify_config() -> None:
    """ Verifies if any fields are missing in the GHWTDE.ini file that the launcher uses. Adds them back in if not present. """
    # Change directory to our config folder (and store old working directory).
    oldDir = OS.getcwd()
    OS.chdir(wtde_find_config())

    # Read the config data.
    config.read("GHWTDE.ini")

    # Read and edit config sections if necessary.
    # Value to set.
    valueToSet = ""

    # ================= CONFIG ================= #
    CONFIG_OPTIONS = [
        "Language",
        "RichPresence",
        "AllowHolidays",
        "AttractDelay",
        "SplashScreenDelay",
        "UseCareerOption",
        "UseQuickplayOption",
        "UseHeadToHeadOption",
        "UseOnlineOption",
        "UseMusicStudioOption",
        "UseCAROption",
        "UseOptionsOption",
        "UseQuitOption"
    ]

    # Verify "Config" section.
    if (not config.has_section("Config")): config["Config"] = {}

    for (item) in (CONFIG_OPTIONS):
        if (not config.has_option("Config", item)):
            match (item):
                case "Language":            valueToSet = "en"
                case "AttractDelay":        valueToSet = "110"
                case "SplashScreenDelay":   valueToSet = "0"
                case _:                     valueToSet = "1"
            
            config.set("Config", item, valueToSet)
        else: continue

    # ================= GRAPHICS ================= #
    GRAPHICS_OPTIONS = [
        "WindowedMode",
        "DisableVSync",
        "HelperPillTheme",
        "DisableDOF",
        "HitSparks",
        "Borderless",
        "DisableBloom",
        "TapTrailTheme",
        "SongIntroStyle",
        "SustainFX",
        "HitFlameTheme",
        "GemTheme",
        "GemColors",
        "FPSLimit",
        "ColorFilters",
        "LoadingTheme",
        "HavokFPS",
        "AntiAliasing",
        "SoloMarkers",
        "HitFlames",
        "RenderParticles",
        "RenderGeoms",
        "RenderInstances",
        "DrawProjectors",
        "BlackStage",
        "HideBand",
        "HideInstruments",
        "Render2D",
        "RenderScreenFX",
        "UseNativeRes"
    ]

    # Verify "Graphics" section.
    if (not config.has_section("Graphics")): config["Graphics"] = {}

    for (item) in (GRAPHICS_OPTIONS):
        if (not config.has_option("Graphics", item)):
            match (item):
                case "WindowedMode":                valueToSet = "0"
                case "HelperPillTheme":             valueToSet = "wtde"
                case "DisableDOF":                  valueToSet = "0"
                case "Borderless":                  valueToSet = "0"
                case "TapTrailTheme":               valueToSet = "ghwt"
                case "SongIntroStyle":              valueToSet = "ghwt"
                case "HitFlameTheme":               valueToSet = "ghwt"
                case "GemTheme":                    valueToSet = "ghwt"
                case "GemColors":                   valueToSet = "standard_gems"
                case "FPSLimit":                    valueToSet = "0"
                case "LoadingTheme":                valueToSet = "wtde"
                case "HavokFPS":                    valueToSet = "60"
                case "AntiAliasing":                valueToSet = "0"
                case "BlackStage":                  valueToSet = "0"
                case "HideBand":                    valueToSet = "0"
                case "HideInstruments":             valueToSet = "0"
                case "UseNativeRes":                valueToSet = "0"
                case _:                             valueToSet = "1"
            
            config.set("Graphics", item, valueToSet)
        else: continue

    # ================= BAND ================= #
    BAND_OPTIONS = [
        "PreferredGuitarist",
        "PreferredBassist",
        "PreferredDrummer",
        "PreferredSinger",
        "PreferredStage",
        "PreferredGuitaristHighway",
        "PreferredBassistHighway",
        "PreferredDrummerHighway",
        "GuitarStrumAnim",
        "BassStrumAnim"
    ]
    
    # Verify "Band" section.
    if (not config.has_section("Band")): config["Band"] = {}

    for (item) in (BAND_OPTIONS):
        if (not config.has_option("Band", item)):
            match (item):
                case "GuitarStrumAnim":     valueToSet = "none"
                case "BassStrumAnim":       valueToSet = "none"
                case _:                     valueToSet = ""
            
            config.set("Band", item, valueToSet)
        else: continue

    # ================= AUDIO ================= #
    AUDIO_OPTIONS = [
        "MicDevice",
        "VocalAdjustment",
        "WhammyPitchShift"
    ]

    # Verify "Audio" section.
    if (not config.has_section("Audio")): config["Audio"] = {}
    
    for (item) in (AUDIO_OPTIONS):
        if (not config.has_option("Audio", item)):
            match (item):
                case "MicDevice":           valueToSet = ""
                case "VocalAdjustment":     valueToSet = "0"
                case _:                     valueToSet = "1"
            
            config.set("Audio", item, valueToSet)
        else: continue
    
    # ================= LOGGER ================= #
    LOGGER_OPTIONS = [
        "Console",
        "WriteFile",
        "PrintStructures",
        "ScriptTracing",
        "DisableSongLogging",
        "ExitOnAssert",
        "DebugDLCSync"
    ]

    # Verify "Logger" section.
    if (not config.has_section("Logger")): config["Logger"] = {}

    for (item) in (LOGGER_OPTIONS):
        if (not config.has_option("Logger", item)):
            match (item):
                case "WriteFile":           valueToSet = "1"
                case "ExitOnAssert":        valueToSet = "1"
                case "DebugDLCSync":        valueToSet = "1"
                case _:                     valueToSet = "0"
            
            config.set("Logger", item, valueToSet)
        else: continue

    # ================= AUTO LAUNCH ================= #
    AUTO_LAUNCH_OPTIONS = [
        "Enabled",
        "HideHUD",
        "SongTime",
        "RawLoad",
        "Players",
        "Venue",
        "Song",
        "Difficulty",
        "Difficulty2",
        "Difficulty3",
        "Difficulty4",
        "Part",
        "Part2",
        "Part3",
        "Part4",
        "Bot",
        "Bot2",
        "Bot3",
        "Bot4"
    ]

    # Verify "AutoLaunch" section.
    if (not config.has_section("AutoLaunch")): config["AutoLaunch"] = {}

    for (item) in (AUTO_LAUNCH_OPTIONS):
        if (not config.has_option("AutoLaunch", item)):
            match (item):
                case "Players":             valueToSet = "1"
                case "Venue":               valueToSet = "z_frathouse"
                case "Song":                valueToSet = ""
                case "Difficulty":          valueToSet = "expert"
                case "Difficulty2":         valueToSet = "expert"
                case "Difficulty3":         valueToSet = "expert"
                case "Difficulty4":         valueToSet = "expert"
                case "Part":                valueToSet = "guitar"
                case "Part2":               valueToSet = "bass"
                case "Part3":               valueToSet = "drum"
                case "Part4":               valueToSet = "vocals"
                case "Bot":                 valueToSet = "1"
                case "Bot2":                valueToSet = "1"
                case "Bot3":                valueToSet = "1"
                case "Bot4":                valueToSet = "1"
                case _:                     valueToSet = "0"
            
            config.set("AutoLaunch", item, valueToSet)
        else: continue

    # ================= DEBUG ================= #
    DEBUG_OPTIONS = [
        "MicAttempts",
        "BindWarningShown",
        "FixMemoryHandler",
        "FixFSBObjects",
        "FixNoteLimit",
        "DisableInputHack",
        "SetlistScaler",
        "HeapScaler"
    ]

    # Verify "Debug" section.
    if (not config.has_section("Debug")): config["Debug"] = {}

    for (item) in (DEBUG_OPTIONS):
        if (not config.has_option("Debug", item)):
            match (item):
                case "FixMemoryHandler":    valueToSet = "1"
                case "DisableInputHack":    valueToSet = "1"
                case _:                     valueToSet = "0"
            
            config.set("Debug", item, valueToSet)
        else: continue

    # ================= FINALIZE CONFIG READ ================= #
    # Is there an unneeded Updater section? If so, get rid of it!
    # This is sometimes caused by conflicting INI reads.
    if (config.has_section("Updater")): config.remove_section("Updater")
 
    # Write this data.
    with (open("GHWTDE.ini", 'w')) as cnf: config.write(cnf)

    # ================= VERIFY ASPYRCONFIG ================= #
    # Change to our directory for AspyrConfig.
    OS.chdir(wtde_find_appdata())

    # Open the XML file and read its data.
    with (open("AspyrConfig.xml", 'rb')) as xml: aspyrConfigData = xml.read()

    # Run BS4 on this data.
    aspyrConfigDataBS = BeautifulSoup(aspyrConfigData, 'xml')

    # Do the drum and mic mapping strings exist?
    try:
        aspyrConfigDataBS.find('s', {'id': 'Keyboard_Drum'}).decode_contents()
    except AttributeError:
        originalData = aspyrConfigDataBS.r

        normalDrumString = "GREEN 308 262 259 258 254 RED 252 236 227 313 YELLOW 322 305 232 331 BLUE 295 256 324 341 ORANGE 999 KICK 318 CANCEL 999 START 219 BACK 999 DOWN 231 UP 327 WHAMMY 999 "

        drumStringNewTag = aspyrConfigDataBS.new_tag("s", id="Keyboard_Drum")
        drumStringNewTag.string = normalDrumString
        originalData.append(drumStringNewTag)

    try:
        aspyrConfigDataBS.find('s', {'id': 'Keyboard_Mic'}).decode_contents()
    except AttributeError:
        originalData = aspyrConfigDataBS.r

        normalMicString = "GREEN 328 308 402 318 RED 221 YELLOW 340 BLUE 343 ORANGE 267 234 218 CANCEL 999 START 219 BACK 999 DOWN 400 231 UP 401 327 MIC_VOL_DOWN 273 "

        micStringNewTag = aspyrConfigDataBS.new_tag("s", id="Keyboard_Mic")
        micStringNewTag.string = normalMicString
        originalData.append(micStringNewTag)

    # After all new tags have been created, write it all back in.
    with (open("AspyrConfig.xml", 'w', encoding = "utf-8")) as xml: xml.write(str(aspyrConfigDataBS))

    # Reset working directory.
    OS.chdir(oldDir)

# Save keyboard mappings to the AspyrConfig.xml file.
def wtde_encode_input(inputStr: str) -> str:
    """
    Takes the string from one of the Input Settings Entry widgets, then encodes its contents into data used by GHWT.\n

    - inputStr : str >> The string of raw characters to be encoded into their Aspyr keyboard ID equivalents.
    \n
    The string returned a string of numbers, which is the original string encoded into their Aspyr keyboard input IDs.
    """
    # Split the string at the spaces.
    inputStrings = inputStr.split(" ")

    # Input final string.
    inputFinalString = ""

    # For each item, convert it to its numerical equivalent.
    for (item) in (inputStrings): inputFinalString += str(key_number_encode(item)) + " "

    return inputFinalString.strip()

# Convert string key mappings into their keyboard values for use in GHWT.
def key_number_encode(key: str) -> int:
    """ For the mapping string, encodes a given string as their equivalent numbers for use in GHWT. """
    # Take the key and convert it to all caps. Makes this case-insensitive!
    key = key.upper()

    # Match the input to the ID it belongs to.
    match (key):
        # Escape key.
        case "ESC":         return 999
        
        # Function keys.
        case "F1":          return 237
        case "F2":          return 238
        case "F3":          return 239
        case "F4":          return 240
        case "F5":          return 241
        case "F6":          return 242
        case "F7":          return 243
        case "F8":          return 244
        case "F9":          return 245

        # Print screen, scroll lock, pause break, and tilde (~).
        case "PRSCR":       return 321
        case "SCRLCK":      return 314
        case "PAUSE":       return 298
        case "~":           return 253
        case "`":           return 253

        # Top row number keys 0-9.
        case "0":           return 200
        case "1":           return 201
        case "2":           return 202
        case "3":           return 203
        case "4":           return 204
        case "5":           return 205
        case "6":           return 206
        case "7":           return 207
        case "8":           return 208
        case "9":           return 209

        # Backspace, insert, home, delete, end, page up/down.
        case "BCKSPC":      return 219
        case "INS":         return 257
        case "DEL":         return 229
        case "HOME":        return 255
        case "END":         return 233
        case "PGUP":        return 303
        case "PGDN":        return 278

        # Number lock and number pad keys.
        case "NUMLCK":      return 281
        case "NUM0":        return 282
        case "NUM1":        return 283
        case "NUM2":        return 284
        case "NUM3":        return 285
        case "NUM4":        return 286
        case "NUM5":        return 287
        case "NUM6":        return 288
        case "NUM7":        return 289
        case "NUM8":        return 290
        case "NUM9":        return 291
        case "NUM+":        return 213
        case "NUM-":        return 320
        case "NUM*":        return 274
        case "NUM/":        return 230
        case "NUMENT":      return 293
        case "NUMDEL":      return 228

        # Row 1 keys, QWERTY row (+ - and =).
        case "TAB":         return 323
        case "Q":           return 304
        case "W":           return 331
        case "E":           return 232
        case "R":           return 305
        case "T":           return 322
        case "Y":           return 341
        case "U":           return 324
        case "I":           return 256
        case "O":           return 295
        case "P":           return 297
        case "[":           return 263
        case "{":           return 263
        case "]":           return 306
        case "}":           return 306
        case "\\":          return 220
        case "|":           return 220
        case "-":           return 273
        case "_":           return 273
        case "=":           return 234
        case "+":           return 234

        # Row 2 keys, ASDFGH row.
        case "CAPS":        return 223
        case "A":           return 210
        case "S":           return 313
        case "D":           return 227
        case "F":           return 236
        case "G":           return 252
        case "H":           return 254
        case "J":           return 258
        case "K":           return 259
        case "L":           return 262
        case ":":           return 345
        case ";":           return 345
        case "'":           return 214
        case "\"":          return 214
        case "ENTER":       return 308

        # Row 3 keys, ZXCVBN row.
        case "LSHIFT":      return 267
        case "Z":           return 343
        case "X":           return 340
        case "C":           return 221
        case "V":           return 328
        case "B":           return 218
        case "N":           return 277
        case "M":           return 269
        case "<":           return 225
        case ",":           return 225
        case ">":           return 299
        case ".":           return 299
        case "?":           return 316
        case "/":           return 316
        case "RSHIFT":      return 311

        # Row 4 keys, LCtrl/Alt, Space, RCtrl/Alt, arrow keys.
        case "LCTRL":       return 264
        case "LALT":        return 266
        case "SPACE":       return 318
        case "RALT":        return 310
        case "RCTRL":       return 307
        case "LMB":         return 400
        case "RMB":         return 401
        case "MMB":         return 402

        case "UP":          return 327
        case "DOWN":        return 231
        case "LEFT":        return 265
        case "RIGHT":       return 309

        # If none of the above match, return 0.
        case _:             return 0

# Update to the latest version.
def wtde_run_updater() -> None:
    """ Runs the updater program for WTDE. Aborts execution if the updater is not present. """
    # Is the user connected to the internet?
    if (is_connected("https://cdn.discordapp.com/attachments/872794777060515890/1044075617307590666/Updater_Main_1_0_3.zip")):
        oldDir = OS.getcwd()
        OS.chdir(OWD)

        config.read("Updater.ini")

        wtdeDir = config.get("Updater", "GameDirectory")

        if (OS.path.exists(f"{wtdeDir}/Updater.exe")):
            OS.chdir(wtdeDir)
            OS.startfile("Updater.exe")
            return True
        else:
            print("WTDE Updater not downloaded!")
            
            # If the updater isn't downloaded, ask the user if they want to download it.
            if (messagebox.askyesno("Download Updater?", "The WTDE updater program was not found in your\ngame folder. Do you want to download it?")):
                print("Downloading files and extracting ZIP...")

                # Print GHWT install location.
                print(wtdeDir)

                # Download the updater files.
                updaterDir = "https://cdn.discordapp.com/attachments/872794777060515890/1044075617307590666/Updater_Main_1_0_3.zip"

                saveDir = f"{wtdeDir}/updater_files.zip"

                zipData = REQ.get(updaterDir, allow_redirects = True)

                open(saveDir, 'wb').write(zipData.content)

                # Extract the ZIP file to the local directory.
                with ZIP.ZipFile(saveDir, "r") as zipRef:
                    zipRef.extractall(path = wtdeDir)

                # Delete the ZIP file, we no longer need it.
                OS.remove(saveDir)

                # If it doesn't exist, add the Updater.ini to accompany the updater program.
                updaterINIDir = f"{wtdeDir}/Updater.ini"

                if (not OS.path.exists(updaterINIDir)):
                    config.write(open(updaterINIDir, 'w'))

                    config["Updater"] = {
                        "GameDirectory" : wtdeDir
                    }

                    with open(updaterINIDir, 'w') as cnf:
                        config.write(cnf)

                    print("New Updater configuration file successfully created!")

                messagebox.showinfo("Successfully Downloaded!", "The WTDE updater program was successfully downloaded! Select this button again to update your mod to the latest version.")

                print("WTDE Updater successfully downloaded and set up!")

                OS.chdir(oldDir)

                return True
            
    else:
        messagebox.showerror("No Internet Connection", "We can't update your mod because you are not currently connected to the internet. Please check your internet connection, then try again.")
        return False

# Find the main WTDE configuration file.
def wtde_find_config() -> str:
    """ Tries to locate the main config file for WTDE (GHWTDE.ini). The path is returned if found; an empty string is returned if not. """
    # Normal directory. Any sane computer *SHOULD* hold it here.
    wtdeConfigNormalDir = "~/Documents/My Games/Guitar Hero World Tour Definitive Edition"

    # Some may have the OneDrive folder... thanks Microsoft for the dumb design...
    wtdeConfigBackupDir = "~/OneDrive/Documents/My Games/Guitar Hero World Tour Definitive Edition"

    # Attempt the default location.
    normalDirOutput = OS.path.expanduser(wtdeConfigNormalDir)
    backupDirOutput = OS.path.expanduser(wtdeConfigBackupDir)

    if (OS.path.exists(normalDirOutput)):
        fixedPath = OS.path.expanduser(wtdeConfigNormalDir).replace("/", "\\")
        return fixedPath

    # If the above didn't work, we'll try a different directory.
    elif (OS.path.exists(backupDirOutput)):
        fixedPath = OS.path.expanduser(wtdeConfigBackupDir).replace("/", "\\")
        return fixedPath

    # If neither worked, it's a bad path, so just return nothing.
    else: return ""

# Access the GHWT local AppData folder.
def wtde_find_appdata() -> str:
    """ Access and return the path to the GHWT local AppData folder. """
    # Access our AspyrConfig.xml file.
    localAppData = OS.getenv('LOCALAPPDATA')
    aspyrConfigXMLDir = OS.path.join(localAppData, "Aspyr\\Guitar Hero World Tour")
    return aspyrConfigXMLDir

# Reads keyboard mapping strings and converts them into actual character strings.
def wtde_decode_input(inputString: str, inputTarget: str) -> str:
    """
    Takes an input mapping string used by GHWT, and decodes the numbers into their actual keyboard inputs.

    - inputString : str
    >> A mapping string of inputs used by GHWT. The string doesn't have to be in order by input.\n
    >> An example of these strings: GREEN 001 002 003 RED 004 005 006...

    - inputTarget : str
    >> The input you want to search for; this isn't case-sensitive.

    Returns a string with the numbers in AspyrConfig.xml converted to their keyboard inputs. An empty string is returned if no bindings are found for the given input.
    """
    # Split the given input string at the spaces.
    inputList = inputString.split(" ")

    # Input find list; used to just get the inputs.
    inputFindList = []

    # Input return string.
    inputReturnString = ""

    # Find the given input in the list.
    # Make sure that the given input exists.
    inputMatchString = inputTarget.upper()
    if (inputList.count(inputMatchString) != 1): return ""

    # Find where the first index of the input is, then move the position to the first number so we can start looping through and getting the input mappings.
    beginIndex = inputList.index(inputMatchString) + 1

    # Now loop through until we get to the next input.
    for (item) in (inputList[beginIndex:]):
        # Is this an input or is it a declaration for a new one?
        if (item.isnumeric()): inputFindList.append(int(item))
        else: break

    # Now that we have our list of inputs, we need to convert them to strings.
    for (item) in (inputFindList):
        key = key_number_decode(item)
        inputReturnString += (key + " ")

    # After converting, return our completed string.
    return inputReturnString.strip()

# Key decoder for keyboard inputs as numbers.
def key_number_decode(key: int) -> str:
    """ For the mapping string, decode a given number (as an int) to its keyboard binding. Return an empty string if no match was found. """
    if (not isinstance(key, int)):
        try: key = int(key)
        except ValueError: return ""

    # Match the number to the key it belongs to.
    match (key):
        # Escape key.
        case 999: return "Esc"

        # Function keys.
        case 237: return "F1"
        case 238: return "F2"
        case 239: return "F3"
        case 240: return "F4"
        case 241: return "F5"
        case 242: return "F6"
        case 243: return "F7"
        case 244: return "F8"
        case 245: return "F9"

        # Print screen, scroll lock, pause break, and tilde (~).
        case 321: return "PrScr"
        case 314: return "ScrLck"
        case 298: return "Pause"
        case 253: return "~"

        # Top row number keys 0-9.
        case 200: return "0"
        case 201: return "1"
        case 202: return "2"
        case 203: return "3"
        case 204: return "4"
        case 205: return "5"
        case 206: return "6"
        case 207: return "7"
        case 208: return "8"
        case 209: return "9"
        
        # Backspace, insert, home, delete, end, page up/down.
        case 219: return "BckSpc"
        case 235: return "Accent"
        case 257: return "Ins"
        case 229: return "Del"
        case 255: return "Home"
        case 233: return "End"
        case 303: return "PgUp"
        case 278: return "PgDn"

        # Number lock and number pad keys.
        case 281: return "NumLck"
        case 282: return "Num0"
        case 283: return "Num1"
        case 284: return "Num2"
        case 285: return "Num3"
        case 286: return "Num4"
        case 287: return "Num5"
        case 288: return "Num6"
        case 289: return "Num7"
        case 290: return "Num8"
        case 291: return "Num9"
        case 213: return "Num+"
        case 320: return "Num-"
        case 274: return "Num*"
        case 230: return "Num/"
        case 293: return "NumEnt"
        case 228: return "NumDel"

        # Row 1 keys, QWERTY row (+ - and =).
        case 323: return "Tab"
        case 304: return "Q"
        case 331: return "W"
        case 232: return "E"
        case 305: return "R"
        case 322: return "T"
        case 341: return "Y"
        case 324: return "U"
        case 256: return "I"
        case 295: return "O"
        case 297: return "P"
        case 263: return "["
        case 306: return "]"
        case 220: return "\\"
        case 273: return "-"
        case 234: return "="
    
        # Row 2 keys, ASDFGH row.
        case 223: return "Caps"
        case 210: return "A"
        case 313: return "S"
        case 227: return "D"
        case 236: return "F"
        case 252: return "G"
        case 254: return "H"
        case 258: return "J"
        case 259: return "K"
        case 262: return "L"
        case 345: return ";"
        case 214: return "\""
        case 308: return "Enter"

        # Row 3 keys, ZXCVBN row.
        case 267: return "LShift"
        case 343: return "Z"
        case 340: return "X"
        case 221: return "C"
        case 328: return "V"
        case 218: return "B"
        case 330: return "B"
        case 277: return "N"
        case 269: return "M"
        case 225: return ","
        case 299: return "."
        case 316: return "?"
        case 311: return "RShift"

        # Row 4 keys, LCtrl/Alt, Space, RCtrl/Alt, arrow keys.
        case 264: return "LCtrl"
        case 266: return "LAlt"
        case 318: return "Space"
        case 310: return "RAlt"
        case 307: return "RCtrl"
        case 327: return "Up"
        case 401: return "RMB"
        case 231: return "Down"
        case 400: return "LMB"
        case 402: return "MMB"
        case 265: return "Left"
        case 309: return "Right"

        

        # If none of the above match, return an empty string.
        case _: return ""

# Get list of microphones.
def mic_name_get_list() -> list[str]:
    """ Returns a list of all microphone names. """
    audio = PA.PyAudio()

    info = audio.get_host_api_info_by_index(0)
    deviceCount = info.get('deviceCount')

    micList = []

    for (i) in (range(0, deviceCount)):
        if ((audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0):
            micList.append(audio.get_device_info_by_host_api_device_index(0, i).get('name'))

    return micList

# Input box numerical verifier.
def input_verify_numeric(inStr: str, acttyp: str) -> bool:
    """ Checks if an input box's text is only numbers; forbids anything else. """
    if (acttyp == '1'):
        if (not inStr.isdigit()): return False
    return True

# Reset working directory.
def reset_working_directory() -> None:
    """ Resets our current working directory to the default. """
    OS.chdir(OWD)

# Warn the user about disabling FixMemoryHandler.
def warn_memory_deselect() -> None:
    """ Warn the user about disabling FixMemoryHandler. """
    if (fixMemoryHandler.get() == "0"):
        if (messagebox.askyesno("Are You Sure?", "Do you really wish to disable the memory handler fix? Disabling this may be dangerous and is not recommended.")):
            debugFixMemoryHandler.deselect()
        else: debugFixMemoryHandler.select()

# Enable or disable other widgets in the Auto Launch Settings tab when Enable Auto Launch is turned ON/OFF.
def auto_launch_status() -> None:
    """ When the Enable Auto Launch checkbutton is pressed, this will enable or disable the ability to set up any of the auto launch settings. """    
    if (enableAutoLaunch.get() == "0"):
        # Disable all widgets for auto launch.
        autoHideHUD.config(state = 'disabled')
        autoPlayersLabel.config(state = 'disabled')
        autoPlayers.config(state = 'disabled')
        autoVenueLabel.config(state = 'disabled')
        autoVenueSelect.config(state = 'disabled')
        autoSongLabel.config(state = 'disabled')
        autoSongEntry.config(state = 'disabled')
        autoPlayerSectionLabel.config(state = 'disabled')

        for (x) in (range(5)):
            if (x == 0): continue
            auto_set_player(x, 'disabled')

        autoAdvancedSectionLabel.config(state = 'disabled')
        autoRawLoad.config(state = 'disabled')
        autoSongTime.config(state = 'disabled')

    else:
        # Enable all widgets for auto launch.
        autoHideHUD.config(state = 'active')
        autoPlayersLabel.config(state = 'active')
        autoPlayers.config(state = 'active')
        autoVenueLabel.config(state = 'active')
        autoVenueSelect.config(state = 'active')
        autoSongLabel.config(state = 'active')
        autoSongEntry.config(state = 'normal')
        autoPlayerSectionLabel.config(state = 'active')

        # Update player widgets.
        auto_update_players()

        autoAdvancedSectionLabel.config(state = 'active')
        autoRawLoad.config(state = 'active')
        autoSongTime.config(state = 'active')

# Get venue name.
def auto_get_venue(venueID: str) -> str:
    """ Returns the actual name of the given venue zone ID. """
    # Return the actual venue name.
    match (venueID):
        case "z_frathouse":         return "Phi Psi Kappa"
        case "z_goth":              return "Wilted Orchid"
        case "z_cathedral":         return "Bone Church"
        case "z_harbor":            return "Pang Tang Bay"
        case "z_recordstore":       return "Amoeba Records"
        case "z_tool":              return "Tool"
        case "z_bayou":             return "Swamp Shack"
        case "z_military":          return "Rock Brigade"
        case "z_fairgrounds":       return "Strutter's Farm"
        case "z_hob":               return "House of Blues"
        case "z_hotel":             return "Ted's Tiki Hut"
        case "z_castle":            return "Will Heilm's Keep"
        case "z_studio2":           return "Recording Studio"
        case "z_ballpark":          return "AT&T Park"
        case "z_scifi":             return "Tesla's Coil"
        case "z_metalfest":         return "Ozzfest"
        case "z_newyork":           return "Times Square"
        case "z_credits":           return "Sunna's Chariot"
        case _:
            if (not venueID == ""): return venueID
            else: return "None"

# Enable widgets based on player count.
def auto_update_players() -> None:
    """ Update the player widgets whenever the players OptionMenu widget updates. """
    auto_set_player(1, 'active')
    match (playerCount.get()):
        case "1":
            auto_set_player(2, 'disabled')
            auto_set_player(3, 'disabled')
            auto_set_player(4, 'disabled')
        
        case "2":
            auto_set_player(2, 'active')
            auto_set_player(3, 'disabled')
            auto_set_player(4, 'disabled')

        case "3":
            auto_set_player(2, 'active')
            auto_set_player(3, 'active')
            auto_set_player(4, 'disabled')

        case "4":
            auto_set_player(2, 'active')
            auto_set_player(3, 'active')
            auto_set_player(4, 'active')
            
# Update player settings (for auto launch).
def auto_set_player(id: int | str, status: str) -> None:
    """
    For the given player, set their status as either active or disabled.

    - id : str OR int >> The player to set the widgets' state for. This should be a number from 1 to 4.
    - status: str >> The state of the widgets. Set this to either 'active' or 'disabled'.   
    """
    match (str(id)):
        case "1":
            # Set state for player 1 widgets.
            autoP1SectionLabel.config(state = status)

            autoP1InstrumentLabel.config(state = status)
            autoP1Instrument.config(state = status)

            autoP1DifficultyLabel.config(state = status)
            autoP1Difficulty.config(state = status)

            autoP1UseBot.config(state = status)

        case "2":
            # Set state for player 2 widgets.
            autoP2SectionLabel.config(state = status)

            autoP2InstrumentLabel.config(state = status)
            autoP2Instrument.config(state = status)

            autoP2DifficultyLabel.config(state = status)
            autoP2Difficulty.config(state = status)

            autoP2UseBot.config(state = status)

        case "3":
            # Set state for player 3 widgets.
            autoP3SectionLabel.config(state = status)

            autoP3InstrumentLabel.config(state = status)
            autoP3Instrument.config(state = status)

            autoP3DifficultyLabel.config(state = status)
            autoP3Difficulty.config(state = status)

            autoP3UseBot.config(state = status)
        
        case "4":
            # Set state for player 4 widgets.
            autoP4SectionLabel.config(state = status)

            autoP4InstrumentLabel.config(state = status)
            autoP4Instrument.config(state = status)

            autoP4DifficultyLabel.config(state = status)
            autoP4Difficulty.config(state = status)

            autoP4UseBot.config(state = status)

# Enable widgets based on player count (event version used by OptionMenu).
def auto_update_players_event(event: Event) -> None:
    """ An alternate version of auto_update_players() used by the player selection OptionMenu. """
    auto_update_players()

# Convert instrument and difficulty to the options in the player settings.
def auto_inst_diff(setting: str) -> str:
    """ Takes a given setting and returns either a part or difficulty. """
    value = config.get("AutoLaunch", setting)

    match (value):
        case "guitar":                  return "Lead Guitar - PART GUITAR"
        case "bass":                    return "Bass Guitar - PART BASS"
        case "drum":                    return "Drums - PART DRUMS"
        case "vocals":                  return "Vocals - PART VOCALS"

        case "easy_rhythm":             return "Beginner"
        case "easy":                    return "Easy"
        case "medium":                  return "Medium"
        case "hard":                    return "Hard"
        case "expert":                  return "Expert"

# Ask for a different venue not listed in the venue list for auto launch.
def ask_venue_name(var: StringVar, event: Event) -> None:
    """ Asks the user for a venue zone ID not specified already in lists of venues. """
    def avn_exit_protocol() -> None:
        """ Exit protocol for the Input Venue ID window. """
        OS.chdir(oldCWD)
        if (venueEntryBox.get().strip() == ""): var.set("Phi Psi Kappa")
        else: var.set(venueEntryBox.get())
        askVenueRoot.destroy()

    def avn_cancel() -> None:
        """ The cancel button for the Input Venue ID window. """
        var.set("Phi Psi Kappa")
        askVenueRoot.destroy()

    oldCWD = OS.getcwd()

    if (var.get() == "Other..."):
        # Set up window.
        OS.chdir(OWD)
        askVenueRoot = Tk()
        askVenueRoot.title("Input Venue ID")
        askVenueRoot.iconbitmap(resource_path("res/icon.ico"))
        askVenueRoot.geometry(f"480x192+{get_screen_resolution()[0] // 3}+{get_screen_resolution()[1] // 4}")
        askVenueRoot.config(bg = BG_COLOR)
        askVenueRoot.resizable(False, False)
        askVenueRoot.protocol("WM_DELETE_WINDOW", avn_exit_protocol)
        askVenueRoot.transient()
        askVenueRoot.focus_force()

        # Show the title widget.
        titleLabel = Label(askVenueRoot, text = "Input Venue ID\nType a venue ID that isn't provided in the option list by default.", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
        titleLabel.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

        # Venue ID label and entry field.
        venueEntryLabel = Label(askVenueRoot, text = "          Venue ID: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
        venueEntryLabel.grid(row = 1, column = 0, sticky = 'e', pady = 20)

        venueEntryBox = Entry(askVenueRoot, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = 30)
        venueEntryBox.grid(row = 1, column = 1, sticky = 'w')
        venueEntryBox.focus_set()

        # OK and cancel buttons.
        venueEntryOK = Button(askVenueRoot, text = "OK", command = avn_exit_protocol, font = FONT_INFO, width = 10, height = 1, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG)
        venueEntryOK.place(x = 290, y = 155)

        venueEntryCancel = Button(askVenueRoot, text = "Cancel", command = avn_cancel, font = FONT_INFO, width = 10, height = 1, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG)
        venueEntryCancel.place(x = 385, y = 155)

        # Enter main loop.
        askVenueRoot.mainloop()

# Get native monitor resolution.
def get_screen_resolution() -> list[int]:
    """ Returns the user's native PRIMARY monitor resolution. """
    return [GetSystemMetrics(0), GetSystemMetrics(1)]

# Get game title by option value.
def wtde_get_game(checksum: str) -> str:
    """ Returns the actual game name from an option value. """
    match (checksum.lower()):
        case "wtde":            return "GH World Tour Definitive Editon"
        case "ghwt":            return "Guitar Hero World Tour"
        case "none":            return "GHWT (Default)"
        case "ghwt_beta":       return "Guitar Hero World Tour (Beta)"
        case "ghwt_wii":        return "Guitar Hero World Tour (Wii)"
        case "ghwt_wii_hd":     return "Guitar Hero World Tour (Wii, HD)"
        case "gh2":             return "Guitar Hero II"
        case "gh3":             return "Guitar Hero III"
        case "gh3_left":        return "Guitar Hero III (Left)"
        case "gh3_console":     return "Guitar Hero III (Console)"
        case "ghm":             return "Guitar Hero Metallica"
        case "ghshits":         return "Guitar Hero Smash Hits"
        case "ghvh":            return "Guitar Hero Van Halen"
        case "gh5":             return "Guitar Hero 5"
        case "ghwor":           return "Guitar Hero Warriors of Rock"
        case "wor":             return "Guitar Hero Warriors of Rock"
        case "bh":              return "Band Hero"
        case "auto":            return "Automatic"
        case "flat":            return "Flat Gems"
        case _:                 return ""

# Get gem color scheme.
def wtde_get_gem_color(checksum: str) -> str:
    """ Return the actual name of a given gem color theme. """
    match (checksum):
        case "standard_gems":           return "Normal Color"
        case "pink_gems":               return "Pink"
        case "stealth_gems":            return "Stealth"
        case "Eggs_N_Bacon_gems":       return "Eggs 'N Bacon"
        case "old_glory_gems":          return "Old Glory"
        case "solid_gold_gems":         return "Solid Gold"
        case "platinum_gems":           return "Platinum"
        case "diabolic_gems":           return "Diabolic"
        case "toxic_waste_gems":        return "Toxic Waste"
        case "black_gems":              return "Black"
        case "pastel_gems":             return "Pastel"
        case "dark_gems":               return "Dark"
        case "outline_gems":            return "Outline"
        case "gh1proto_gems":           return "GH1 Prototype"
        case "pure_green":              return "Pure Green"
        case "pure_red":                return "Pure Red"
        case "pure_yellow":             return "Pure Yellow"
        case "pure_blue":               return "Pure Blue"
        case "pure_orange":             return "Pure Orange"
        case "candy_cane":              return "Candy Cane"
        case "halloween":               return "Ghoulish"
        case _:                         return ""

# Get language checksum.
def wtde_convert_language(text: str) -> str:
    """ Takes a language name and converts it to its option checksum in the INI. """
    # Match the text to the input.
    match (text):
        case "English":                    return "en"
        case "Spanish (Español)":          return "es"
        case "Italian (Italiano)":         return "it"
        case "French (Français)":          return "fr"
        case "German (Deutsch)":           return "de"
        case "Japanese (日本語)":           return "ja"
        case "Korean (한국어)":             return "ko"
        case _:                            return ""

# Make sure the given string has only numbers (includes leading negatives).
def input_filter_numeric(text: str) -> str:
    """
    In a given string, this filters out ALL non-numeric characters, with the exception of a leading negative sign.
    
    Arguments
    ---------
    `text`: `str` >> The string of text to filter out.

    Returns
    -------
    `str` >> Returns the given string with all non-numeric characters (except leading negatives) filtered out.

    Examples of Use
    --------------
    >>> inputString = "28FE3D"
    >>> print(input_filter_numeric(inputString))
    283
    >>> print(input_filter_numeric("-1A79E5"))
    -1795
    """
    # This will hold the final string.
    finalString = ""

    # Is there a negative at the front of the string?
    try:
        if (text.index("-") == 0): finalString += "-"
        text = text.replace("-", "")

    except ValueError:
        pass

    splitInputString = text.split()

    for (char) in (splitInputString):
        if (char.isnumeric()) or (char == "."): finalString += char
        else: continue

    return finalString

# Get the gem theme or style.
def wtde_get_note_info(mode: str) -> str:
    """
    Return the information of a note theme/style.
    \n
    - mode : str >> Either a literal 'style' or 'color'. Identifier for the function to tell which aspect of the
    notes it needs to look for.
    \n
    Returns the respective option name.
    """
    # Original working directory.
    oldDir = OS.getcwd()

    # Value to return.
    valueToReturn = ""

    # Change to our config directory and read its contents.
    OS.chdir(wtde_find_config())
    config.read("GHWTDE.ini")

    # Operate based on given arguments.
    if (mode == 'style'):
        noteStyles = ["GHWT Notes (Default)", "GH3 Notes", "GH: WOR Notes", "Flat Notes"]
        match (config.get("Graphics", "GemTheme")):
            case "ghwt":            valueToReturn = noteStyles[0]
            case "gh3":             valueToReturn = noteStyles[1]
            case "wor":             valueToReturn = noteStyles[2]
            case "flat":            valueToReturn = noteStyles[3]
            case _:                 valueToReturn = noteStyles[0]

    elif (mode == 'color'):
        noteThemesChecksums = [
            "standard_gems", "pink_gems", "stealth_gems", "Eggs_N_Bacon_gems", "old_glory_gems", "solid_gold_gems", "platinum_gems",
            "diabolic_gems", "toxic_waste_gems", "black_gems", "pastel_gems", "dark_gems", "outline_gems", "gh1proto_gems",
            "pure_green", "pure_red", "pure_yellow", "pure_blue", "pure_orange", "candy_cane", "halloween"
        ]

        noteThemesOptionNames = [
            "Normal Color (Default)", "Pink", "Stealth", "Eggs 'N Bacon", "Old Glory", "Solid Gold", "Platinum",
            "Diabolic", "Toxic Waste", "Black", "Pastel", "Dark", "Outline", "GH1 Prototype", "Pure Green",
            "Pure Red", "Pure Yellow", "Pure Blue", "Pure Orange", "Candy Cane", "Ghoulish"
        ]

        for (x), (item) in (enumerate(noteThemesChecksums)):
            if (config.get("Graphics", "GemColors") == item): valueToReturn = noteThemesOptionNames[x]
            else: continue
    
    else: valueToReturn = ""

    # Reset working directory.
    OS.chdir(oldDir)

    # Return the necessary value.
    return valueToReturn

# Get the gem theme or style.
def wtde_save_note_info(mode: str) -> str:
    """
    Save the information of the note theme/style options.
    \n
    - mode : str >> Either a literal 'style' or 'color'. Identifier for the function to tell which aspect of the
    notes it needs to look for.
    \n
    Returns the respective option name.
    """
    # Value to return.
    valueToReturn = ""

    # Operate based on given arguments.
    if (mode == 'style'):
        noteStyleOptions = ["GHWT Notes (Default)", "GH3 Notes", "GH: WOR Notes", "Flat Notes"]
        noteStyles = ["ghwt", "gh3", "wor", "flat"]
        for (x), (item) in (enumerate(noteStyleOptions)):
            if (noteStyle.get() == item): valueToReturn = noteStyles[x]
            else: continue

    elif (mode == 'color'):
        noteThemesChecksums = [
            "standard_gems", "pink_gems", "stealth_gems", "Eggs_N_Bacon_gems", "old_glory_gems", "solid_gold_gems", "platinum_gems",
            "diabolic_gems", "toxic_waste_gems", "black_gems", "pastel_gems", "dark_gems", "outline_gems", "gh1proto_gems",
            "pure_green", "pure_red", "pure_yellow", "pure_blue", "pure_orange", "candy_cane", "halloween"
        ]

        noteThemesOptionNames = [
            "Normal Color (Default)", "Pink", "Stealth", "Eggs 'N Bacon", "Old Glory", "Solid Gold", "Platinum",
            "Diabolic", "Toxic Waste", "Black", "Pastel", "Dark", "Outline", "GH1 Prototype", "Pure Green",
            "Pure Red", "Pure Yellow", "Pure Blue", "Pure Orange", "Candy Cane", "Ghoulish"
        ]

        for (x), (item) in (enumerate(noteThemesOptionNames)):
            if (noteTheme.get() == item): valueToReturn = noteThemesChecksums[x]
            else: continue
    
    else: valueToReturn = ""

    # Return the necessary value.
    return valueToReturn

# Open Mods folder.
def open_mods_folder() -> None:
    """ Opens the user's Mods folder in DATA/MODS. """
    # Change directory to original directory.
    oldDir = OS.getcwd()
    OS.chdir(OWD)

    # Read Updater.ini and get the user's WTDE directory.
    config.read("Updater.ini")
    wtdeDir = config.get("Updater", "GameDirectory")

    # Open MODS folder from the identified directory.
    OS.startfile(f"{wtdeDir}/DATA/MODS")

    # Restore working directory.
    OS.chdir(oldDir)

# Is the user connected to the internet?
def is_connected(url: str, tout = 10) -> bool | Exception:  
    # Try to ping the webside and get its contents.
    # If we can do that, return True.
    try:
        request = REQ.get(url, timeout = tout)
        return True

    # Catch the error, if found. Return False.
    except (REQ.ConnectionError, REQ.Timeout) as exception:
        return False

# Retrieve the latest version of WTDE on the Pastebin page.
def wtde_latest_version() -> str:
    """ Retrieves the latest version of WTDE on the Pastebin page. """
    versionPage = "https://pastebin.com/raw/wk00Mq3M"

    if (is_connected(versionPage)):
        return REQ.get(versionPage).text
    else:
        return "??? (connect to internet)"

# Retrieve the latest version of WTDE on the Pastebin page.
def wtde_get_news() -> str:
    """ Retrieves the latest news for WTDE on the Pastebin page. """
    newsPage = "https://pastebin.com/raw/c9MwubYS"

    if (is_connected("https://pastebin.com/raw/c9MwubYS")):
        return REQ.get(newsPage).text
    
    else:
        try:
            REQ.get(newsPage).text
        except Exception as exception:
            excep = exception

        return f"Hm... We couldn't establish a connection to the internet.\n\nIs the Wi-Fi and/or router turned on?\n\nError Information:\n{excep}"

# Get intro text style or load screen theme.
def wtde_get_intro_load(mode: str) -> str:
    """ Reads option names and deciphers them into their INI checksums for loading screen themes and intro text styles. """
    # mode: 'intro' or 'load'
    if (mode == 'intro'):
        # This is the song intro text shown on the top left of the screen.
        introStyles = [
            "Normal GHWT (Default)", "Guitar Hero III", "Guitar Hero III (Left)", "GH: Smash Hits", "GH: Metallica", "GH: Van Halen", "Guitar Hero 5", "Band Hero", "GH: Warriors of Rock", "Auto (Based on Setlist)"
        ]

        introChecksums = [
            "ghwt", "gh3", "gh3_left", "ghshits", "ghm", "ghvh", "gh5", "bh", "ghwor", "auto"
        ]

        for (x), (item) in (enumerate(introChecksums)):
            if (config.get("Graphics", "SongIntroStyle") == item): return introStyles[x]
        
        return introStyles[0]

# Set mic calibration.
def mic_set_calibration(audio: int | str, video: int | str) -> None:
    """ Set the user's microphone calibration to the given values. """
    # Update the values.
    inputMicDelayEntry.delete(0, END)
    inputMicDelayEntry.insert(0, str(audio))

    inputMicVideoDelayEntry.delete(0, END)
    inputMicVideoDelayEntry.insert(0, str(video))

# Verify files and main GHWTDE config file.
verify_files()
wtde_verify_config()

# Read AspyrConfig.xml and its properties.
# Open the XML file and read its data.
OS.chdir(wtde_find_appdata())
with (open("AspyrConfig.xml", 'rb')) as xml: aspyrConfigData = xml.read()

# Run BS4 on this data.
aspyrConfigDataBS = BeautifulSoup(aspyrConfigData, 'xml', from_encoding = 'utf-8')

# Find tag "s", but then we'll filter it into the keyboard information.
aspyrConfigDataS = aspyrConfigDataBS.find_all('s')

# Get the keyboard mapping string for the menu navigation.
keyMenuString = aspyrConfigDataBS.find('s', {"id": "Keyboard_Menu"}).decode_contents()

# Get the keyboard mapping string for the guitar controls.
keyGuitarString = aspyrConfigDataBS.find('s', {"id": "Keyboard_Guitar"}).decode_contents()

# Get the keyboard mapping string for the drum controls.
keyDrumString = aspyrConfigDataBS.find('s', {"id": "Keyboard_Drum"}).decode_contents()

# Get the keyboard mapping string for the mic controls.
keyVocalString = aspyrConfigDataBS.find('s', {"id": "Keyboard_Mic"}).decode_contents()

# Audio visual lag.
audioVisualLag = aspyrConfigDataBS.find('s', {"id": "Options.VocalsVisualLag"}).decode_contents()

# Audio buffer length.
audioBuffLen = aspyrConfigDataBS.find('s', {"id": "Audio.BuffLen"}).decode_contents()

# Resolution width.
resWidth = aspyrConfigDataBS.find('s', {"id": "Video.Width"}).decode_contents()

# Resolution height.
resHeight = aspyrConfigDataBS.find('s', {"id": "Video.Height"}).decode_contents()

# Reset our working directory.
reset_working_directory()

# Parse command line arguments (if running at the command line).
arg_cmd_parse()

# Default program variables.
BG_COLOR = "#0B101F"
BUTTON_BG = "#A5C9CA"
BUTTON_FG = "#000000"
BUTTON_ACTIVE_BG = "#E7F6F2"
BUTTON_ACTIVE_FG = "#000000"
FG_COLOR = "#FFFFFF"
FONT = "Tahoma"
FONT_SIZE = 11
FONT_INFO = (FONT, FONT_SIZE)
FONT_INFO_DROPDOWN = (FONT, 9)
FONT_INFO_DIVIDER = (FONT, 1)
TAB_WINDOW_WIDTH = 1060
TAB_WINDOW_HEIGHT = 620
HOVER_DELAY = 500

# Create program window.
root = Tk()
root.title(f"GHWT: Definitive Edition Launcher++ - V{VERSION}")
root.geometry(f"1280x768+{get_screen_resolution()[0] // 6}+{get_screen_resolution()[1] // 8}")
root.iconbitmap(resource_path("res/icon.ico"))
root.config(bg = BG_COLOR)
root.resizable(False, False)
root.transient()
root.focus_force()

# Create image constants.
IMAGE_BG = ImageTk.PhotoImage(Image.open(resource_path("res/bg.png")))
WTDE_LOGO = ImageTk.PhotoImage(Image.open(resource_path("res/logo.png")))
WTDE_LOGO_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icon_192.png")))
WTDE_LOGO_SMALLER = ImageTk.PhotoImage(Image.open(resource_path("res/logo_smaller.png")))

NEWS_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/news_icon.png")))
GENERAL_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/general_icon.png")))
INPUT_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/input_icon.png")))
GRAPHICS_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/graphics_icon.png")))
AUTO_LAUNCH_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/auto_launch_icon.png")))
BAND_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/band_icon.png")))
DEBUG_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/debug_icon.png")))
CREDITS_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/credits_icon.png")))
CREDITS_TABLE_IMAGE = ImageTk.PhotoImage(Image.open(resource_path("res/credits_table.png")))

INPUT_GUITAR_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/guitar_bass.png")))
INPUT_DRUMS_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/drums.png")))
INPUT_MIC_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/icons/vocals.png")))

# Widget canvas.
widgetCanvas = Canvas(root, width = 1300, height = 788)
widgetCanvas.place(x = -10, y = -10)

widgetCanvas.create_image(0, 0, image = IMAGE_BG, anchor = 'nw')

# Top panel: WTDE logo and run button.
widgetCanvas.create_image(8, 8, image = WTDE_LOGO_ICON, anchor = 'nw')

# Run WTDE button.
wtdeRunButton = Button(root, text = "Save & Run WTDE", font = FONT_INFO, width = 25, height = 2, command = wtde_run_save, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG)
wtdeRunButton.place(x = 196, y = 10)
wtdeRunButtonTip = Hovertip(wtdeRunButton, "Save all configuration settings and run GHWT: Definitive Edition.", HOVER_DELAY)

# Save config button.
wtdeSaveConfigButton = Button(root, text = "Save Configuration", font = FONT_INFO, width = 25, height = 2, command = wtde_save_config, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG)
wtdeSaveConfigButton.place(x = 412, y = 10)
wtdeSaveConfigButtonTip = Hovertip(wtdeSaveConfigButton, "Save your configuration settings.", HOVER_DELAY)

# Update WTDE button.
wtdeUpdateButton = Button(root, text = "Update WTDE", font = FONT_INFO, width = 25, height = 2, command = wtde_run_updater, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG)
wtdeUpdateButton.place(x = 628, y = 10)

# Are we connected to the internet?
if (is_connected("https://cdn.discordapp.com/attachments/872794777060515890/1044075617307590666/Updater_Main_1_0_3.zip")):
    wtdeUpdateButtonTipText = "Update WTDE to the latest version and verify your installation's integrity."
    stateToUpdateTo = 'normal'
else:
    wtdeUpdateButtonTipText = "Can't update WTDE! No internet connection was found."
    stateToUpdateTo = 'disabled'

# Update button and its tooltip.
wtdeUpdateButton.config(state = stateToUpdateTo)
wtdeUpdateButtonTip = Hovertip(wtdeUpdateButton, wtdeUpdateButtonTipText, HOVER_DELAY)

# Open MODS folder.
wtdeModsFolderButton = Button(root, text = "Open Mods Folder", font = FONT_INFO, width = 25, height = 2, command = open_mods_folder, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG)
wtdeModsFolderButton.place(x = 844, y = 10)
wtdeModsFolderButtonTip = Hovertip(wtdeModsFolderButton, "Open your Mods folder in your GHWT installation folder.", HOVER_DELAY)

# Make WTDE shortcut on Desktop button.
wtdeShortcutButton = Button(root, text = "Make Shortcut on Desktop", font = FONT_INFO, width = 25, height = 2, command = wtde_create_lnk, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG)
wtdeShortcutButton.place(x = 1060, y = 10)
wtdeShortcutButtonTip = Hovertip(wtdeShortcutButton, "Add a shortcut to WTDE on the Desktop.", HOVER_DELAY)

# Main tabbed options through TTK's Notebook widget.
wtdeOptionsRoot = ttk.Notebook(root)
wtdeOptionsRoot.place(x = 200, y = 70)

# Set up tab frames.
wtdeOptionsNews = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsGeneral = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsInput = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsGraphics = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsBand = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsAutoLaunch = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsDebug = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)
wtdeOptionsCredits = Frame(wtdeOptionsRoot, width = TAB_WINDOW_WIDTH, height = TAB_WINDOW_HEIGHT, bg = BG_COLOR)

# Pack tab frames into the notebook.
wtdeOptionsNews.pack(fill = 'both', expand = 1)
wtdeOptionsGeneral.pack(fill = 'both', expand = 1)
wtdeOptionsInput.pack(fill = 'both', expand = 1)
wtdeOptionsGraphics.pack(fill = 'both', expand = 1)
wtdeOptionsBand.pack(fill = 'both', expand = 1)
wtdeOptionsAutoLaunch.pack(fill = 'both', expand = 1)
wtdeOptionsDebug.pack(fill = 'both', expand = 1)
wtdeOptionsCredits.pack(fill = 'both', expand = 1)

# ====================================================================== #
#                               WTDE NEWS TAB                            #
# ====================================================================== #
# Show any news for GHWT: DE.
# Show image at top.
WTDE_NEWS_TITLE_TEXT = "    Want some of the latest news for GHWT: DE? Have a look for yourself here!\n\n\n    This page attempts to be as up-to-date as possible. Stay tuned for more!"

newsTitleLabel = Label(wtdeOptionsNews, text = WTDE_NEWS_TITLE_TEXT, image = WTDE_LOGO_SMALLER, compound = 'left', bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
newsTitleLabel.pack(fill = 'x', anchor = 'n')

# Add a white line.
newsSeparator = ttk.Separator(wtdeOptionsNews, orient = 'horizontal')
newsSeparator.pack(fill = 'x')

newsLabel = Text(wtdeOptionsNews, bg = BG_COLOR, fg = FG_COLOR, relief = 'flat', font = FONT_INFO, wrap = WORD)
newsLabel.pack(side = 'left', fill = 'both', expand = 1)
newsLabel.insert(END, wtde_get_news())
newsLabel.configure(state = 'disabled')

newsScroll = ttk.Scrollbar(wtdeOptionsNews, orient = 'vertical', command = newsLabel.yview)
newsScroll.pack(side = 'right', fill = 'y')

newsLabel.config(yscrollcommand = newsScroll.set)

# ====================================================================== #
#                           GENERAL SETTINGS TAB                         #
# ====================================================================== #
# Ready the config to translate its settings into the program.
OS.chdir(wtde_find_config())
config.read("GHWTDE.ini")

# This tab will primarily use settings found under [Config].

# General settings tab information.
TAB_INFO_GENERAL = "General Settings: Adjust general settings about WTDE.\nHover over any option to see what it does!"
generalInfoLabel = Label(wtdeOptionsGeneral, text = TAB_INFO_GENERAL, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
generalInfoLabel.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

# Column 1 settings.
# Use Discord Rich Presence.
richPresence = StringVar()
RICH_PRESENCE_TIP = "Use Discord Rich Presence.\n\n" \
                    "If Discord is installed on this device, when this is enabled,\n" \
                    "it will show a detailed summary about what\n" \
                    "you are currently doing in-game, such as what mode\n" \
                    "you're playing, your instrument, what song you are\n" \
                    "currently in, time until it's over, and more!"
generalRichPresence = Checkbutton(wtdeOptionsGeneral, text = "  Use Discord Rich Presence", variable = richPresence, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
generalRichPresence.grid(row = 1, column = 0, padx = 20, pady = 5, sticky = 'w')
generalRichPresenceTip = Hovertip(generalRichPresence, RICH_PRESENCE_TIP, HOVER_DELAY)

# Use Holiday Themes.
allowHolidays = StringVar()
ALLOW_HOLIDAYS_TIP = "Use holiday themes in WTDE.\n\n" \
                     "These are themes that will be shown during certain times of the year!\n" \
                     "Currently, there are the following themes:\n" \
                     "  •  WTDE Default Theme\n" \
                     "  •  Valentine's Day Theme\n" \
                     "  •  Halloween Theme\n" \
                     "  •  Christmas Theme"
generalAllowHolidays = Checkbutton(wtdeOptionsGeneral, text = "  Enable Holiday Themes", variable = allowHolidays, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
generalAllowHolidays.grid(row = 2, column = 0, padx = 20, pady = 5, sticky = 'w')
generalAllowHolidaysTip = Hovertip(generalAllowHolidays, ALLOW_HOLIDAYS_TIP, HOVER_DELAY)

# Use Whammy Pitch Shift.
whammyPitchShift = StringVar()
WHAMMY_PITCH_SHIFT_TIP = "Turn ON or OFF whammy effects. If this is OFF, audio distortion by whammy will be disabled."
generalWhammyPitchShift = Checkbutton(wtdeOptionsGeneral, text = "  Whammy Pitch Shift", variable = whammyPitchShift, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
generalWhammyPitchShift.grid(row = 3, column = 0, padx = 20, pady = 5, sticky = 'w')
generalWhammyPitchShiftTip = Hovertip(generalWhammyPitchShift, WHAMMY_PITCH_SHIFT_TIP, HOVER_DELAY)

# Set the language used in-game.
language = StringVar()
LANGUAGE_SELECT_TIP = "Set the language to be used in-game."
languages = ["English", "Spanish (Español)", "Italian (Italiano)", "French (Français)", "German (Deutsch)", "Japanese (日本語)", "Korean (한국어)"]

generalLanguageSelectLabel = Label(wtdeOptionsGeneral, text = "Language:         ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
generalLanguageSelectLabel.grid(row = 4, column = 0, pady = 5, sticky = 'e')
generalLanguageSelectLabel = Hovertip(generalLanguageSelectLabel, LANGUAGE_SELECT_TIP, HOVER_DELAY)

generalLanguageSelect = OptionMenu(wtdeOptionsGeneral, language, *languages)
generalLanguageSelect.config(width = 22, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
generalLanguageSelect.grid(row = 4, column = 1, pady = 5, sticky = 'w')
generalLanguageSelectTip = Hovertip(generalLanguageSelect, LANGUAGE_SELECT_TIP, HOVER_DELAY)

# Audio buffer length setting.
audioBuffLenOption = StringVar()
AUDIO_BUFF_LEN_TIP = "The length, in bytes, of the audio buffer used when decoding FMOD Sound Bank streams. Higher is usually better.\n" \
                     "Modifying this and/or changing your sound output to 44 kHz can cause bad audio output in-game."
generalAudioBuffLenLabel = Label(wtdeOptionsGeneral, text = "Audio Buffer Length:         ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
generalAudioBuffLenLabel.grid(row = 5, column = 0, pady = 5, sticky = 'e')
generalAudioBuffLenLabelTip = Hovertip(generalAudioBuffLenLabel, AUDIO_BUFF_LEN_TIP, HOVER_DELAY)

audioBuffLenOptions = ["2048", "4096"]
generalAudioBuffLen = OptionMenu(wtdeOptionsGeneral, audioBuffLenOption, *audioBuffLenOptions)
generalAudioBuffLen.config(width = 10, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
generalAudioBuffLen.grid(row = 5, column = 1, pady = 5, sticky = 'w')
generalAudioBuffLenTip = Hovertip(generalAudioBuffLen, AUDIO_BUFF_LEN_TIP, HOVER_DELAY)

audioBuffLenOption.set(audioBuffLen)

# Menu option toggles.
MENU_TOGGLES_TIP = "Turn ON or OFF various different commands on the main menu."
generalMenuTogglesLabel = Label(wtdeOptionsGeneral, text = "Main Menu Options:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
generalMenuTogglesLabel.grid(row = 1, column = 2, padx = 40, pady = 5, sticky = 'w')
generalMenuTogglesLabelTip = Hovertip(generalMenuTogglesLabel, MENU_TOGGLES_TIP, HOVER_DELAY)

# Use Career option.
useCareerOption = StringVar()
USE_CAREER_TIP = "Show or hide the Career option."
generalUseCareerOption = Checkbutton(wtdeOptionsGeneral, text = "  Career", variable = useCareerOption, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
generalUseCareerOption.grid(row = 2, column = 2, padx = 40, pady = 5, sticky = 'w')
generalUseCareerOptionTip = Hovertip(generalUseCareerOption, USE_CAREER_TIP, HOVER_DELAY)

# Use Quickplay option.
useQuickplayOption = StringVar()
USE_QUICKPLAY_TIP = "Show or hide the Quickplay option."
generalUseQuickplayOption = Checkbutton(wtdeOptionsGeneral, text = "  Quickplay", variable = useQuickplayOption, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
generalUseQuickplayOption.grid(row = 3, column = 2, padx = 40, pady = 5, sticky = 'w')
generalUseQuickplayOptionTip = Hovertip(generalUseQuickplayOption, USE_QUICKPLAY_TIP, HOVER_DELAY)

# Use Head to Head option.
useHeadToHeadOption = StringVar()
USE_HTH_TIP = "Show or hide the Head to Head option."
generalUseHeadToHeadOption = Checkbutton(wtdeOptionsGeneral, text = "  Head to Head", variable = useHeadToHeadOption, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
generalUseHeadToHeadOption.grid(row = 4, column = 2, padx = 40, pady = 5, sticky = 'w')
generalUseHeadToHeadOptionTip = Hovertip(generalUseHeadToHeadOption, USE_HTH_TIP, HOVER_DELAY)

# Use Online option.
useOnlineOption = StringVar()
USE_ONLINE_TIP = "Show or hide the Online option."
generalUseOnlineOption = Checkbutton(wtdeOptionsGeneral, text = "  Online", variable = useOnlineOption, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
generalUseOnlineOption.grid(row = 5, column = 2, padx = 40, pady = 5, sticky = 'w')
generalUseOnlineOptionTip = Hovertip(generalUseOnlineOption, USE_ONLINE_TIP, HOVER_DELAY)

# Use Music Studio option.
useMusicStudioOption = StringVar()
USE_MUSIC_STUDIO_TIP = "Show or hide the Music Studio option."
generalUseMusicStudioOption = Checkbutton(wtdeOptionsGeneral, text = "  Music Studio", variable = useMusicStudioOption, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
generalUseMusicStudioOption.grid(row = 6, column = 2, padx = 40, pady = 5, sticky = 'w')
generalUseMusicStudioOptionTip = Hovertip(generalUseMusicStudioOption, USE_MUSIC_STUDIO_TIP, HOVER_DELAY)

# Use Rock Star Creator option.
useCAROption = StringVar()
USE_CAR_TIP = "Show or hide the Rock Star Creator option."
generalUseCAROption = Checkbutton(wtdeOptionsGeneral, text = "  Rock Star Creator", variable = useCAROption, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
generalUseCAROption.grid(row = 7, column = 2, padx = 40, pady = 5, sticky = 'w')
generalUseCAROptionTip = Hovertip(generalUseCAROption, USE_CAR_TIP, HOVER_DELAY)

# Use Options option.
useOptionsOption = StringVar()
USE_OPTIONS_TIP = "Show or hide the Options option."
generalUseOptionsOption = Checkbutton(wtdeOptionsGeneral, text = "  Options", variable = useOptionsOption, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
generalUseOptionsOption.grid(row = 8, column = 2, padx = 40, pady = 5, sticky = 'w')
generalUseOptionsOptionTip = Hovertip(generalUseOptionsOption, USE_OPTIONS_TIP, HOVER_DELAY)

# Use Exit option.
useQuitOption = StringVar()
USE_QUIT_TIP = "Show or hide the Exit option."
generalUseQuitOption = Checkbutton(wtdeOptionsGeneral, text = "  Exit", variable = useQuitOption, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
generalUseQuitOption.grid(row = 9, column = 2, padx = 40, pady = 5, sticky = 'w')
generalUseQuitOptionTip = Hovertip(generalUseQuitOption, USE_QUIT_TIP, HOVER_DELAY)

# ====================================================================== #
#                            INPUT SETTINGS TAB                          #
# ====================================================================== #
# This section primarily deals with the AspyrConfig.xml file in the user's Local AppData folder for keyboard mapping editing.

# Constants used for drawing the labels and entry boxes.
INPUT_FIELD_LABEL_PADX = 0
INPUT_FIELD_LABEL_PADY = 4
INPUT_MAPPING_ENTRY_WIDTH = 20

# Input settings tab information.
TAB_INFO_INPUT = "Input Settings: Modify your keyboard controls and microphone settings.\nHover over any option to see what it does!"
inputInfoLabel = Label(wtdeOptionsInput, text = TAB_INFO_INPUT, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
inputInfoLabel.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

# Inputs for the keyboard hover tip.
KEY_INPUT_TIP = "Set the keyboard controls when playing.\n\n" \
                "When saved, these keys will be converted to their numerical values.\n\n" \
                "To set more than one binding to each input, separate each input by spaces. Example: 1 A LShift...\n\n" \
                "Accepted Characters (not case-sensitive, but must be typed EXACTLY):\n" \
                "A-Z, 0-9, Esc, F1-9, PrScr, ScrLck, Pause, ~, -, =, BckSpc, Ins, Home, PgUp, NumLck,\n" \
                "Num/, Num*, Num-, Tab, [, ], \\, Del, End, PgDn, Num0-9, Num+, Caps, ;, \", Enter,\n" \
                "LShift, ,, ., ?, RShift, Up, NumEnt, LCtrl, LAlt, Space, RAlt, RCtrl, Left, Down, Right, NumDel,\n" \
                "LMB, MMB, RMB, Accent"

# ============================================= #
#                  GUITAR INPUTS                #
# ============================================= #
inputKeyGuitarLabel = Label(wtdeOptionsInput, text = " Guitar & Bass Keyboard Controls:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', image = INPUT_GUITAR_ICON, compound = 'left')
inputKeyGuitarLabel.grid(row = 1, column = 0, columnspan = 2, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarLabelTip = Hovertip(inputKeyGuitarLabel, KEY_INPUT_TIP, HOVER_DELAY)

# =============== GREEN INPUTS =============== #

inputKeyGuitarGreenLabel = Label(wtdeOptionsInput, text = "    Green: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyGuitarGreenLabel.grid(row = 2, column = 0, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyGuitarGreenLabelTip = Hovertip(inputKeyGuitarGreenLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarGreenEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyGuitarGreenEntry.grid(row = 2, column = 1, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarGreenEntryTip = Hovertip(inputKeyGuitarGreenEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarGreenEntry.insert(0, wtde_decode_input(keyGuitarString, "GREEN"))

# =============== RED INPUTS =============== #

inputKeyGuitarRedLabel = Label(wtdeOptionsInput, text = "      Red: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyGuitarRedLabel.grid(row = 3, column = 0, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyGuitarRedLabelTip = Hovertip(inputKeyGuitarRedLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarRedEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyGuitarRedEntry.grid(row = 3, column = 1, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarRedEntryTip = Hovertip(inputKeyGuitarRedEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarRedEntry.insert(0, wtde_decode_input(keyGuitarString, "RED"))

# =============== YELLOW INPUTS =============== #

inputKeyGuitarYellowLabel = Label(wtdeOptionsInput, text = "   Yellow: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyGuitarYellowLabel.grid(row = 4, column = 0, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyGuitarYellowLabelTip = Hovertip(inputKeyGuitarYellowLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarYellowEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyGuitarYellowEntry.grid(row = 4, column = 1, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarYellowEntryTip = Hovertip(inputKeyGuitarYellowEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarYellowEntry.insert(0, wtde_decode_input(keyGuitarString, "YELLOW"))

# =============== BLUE INPUTS =============== #

inputKeyGuitarBlueLabel = Label(wtdeOptionsInput, text = "     Blue: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyGuitarBlueLabel.grid(row = 5, column = 0, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyGuitarBlueLabelTip = Hovertip(inputKeyGuitarBlueLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarBlueEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyGuitarBlueEntry.grid(row = 5, column = 1, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarBlueEntryTip = Hovertip(inputKeyGuitarBlueEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarBlueEntry.insert(0, wtde_decode_input(keyGuitarString, "BLUE"))

# =============== ORANGE INPUTS =============== #

inputKeyGuitarOrangeLabel = Label(wtdeOptionsInput, text = "   Orange: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyGuitarOrangeLabel.grid(row = 6, column = 0, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyGuitarOrangeLabelTip = Hovertip(inputKeyGuitarOrangeLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarOrangeEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyGuitarOrangeEntry.grid(row = 6, column = 1, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarOrangeEntryTip = Hovertip(inputKeyGuitarOrangeEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarOrangeEntry.insert(0, wtde_decode_input(keyGuitarString, "ORANGE"))

# =============== STAR POWER INPUTS =============== #

inputKeyGuitarSPLabel = Label(wtdeOptionsInput, text = "Star Power: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyGuitarSPLabel.grid(row = 7, column = 0, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyGuitarSPLabelTip = Hovertip(inputKeyGuitarSPLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarSPEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyGuitarSPEntry.grid(row = 7, column = 1, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarSPEntryTip = Hovertip(inputKeyGuitarSPEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarSPEntry.insert(0, wtde_decode_input(keyGuitarString, "STAR"))

# =============== START INPUTS =============== #

inputKeyGuitarStartLabel = Label(wtdeOptionsInput, text = "    Start: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyGuitarStartLabel.grid(row = 8, column = 0, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyGuitarStartLabelTip = Hovertip(inputKeyGuitarStartLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarStartEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyGuitarStartEntry.grid(row = 8, column = 1, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarStartEntryTip = Hovertip(inputKeyGuitarStartEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarStartEntry.insert(0, wtde_decode_input(keyGuitarString, "START"))

# =============== BACK INPUTS =============== #

inputKeyGuitarBackLabel = Label(wtdeOptionsInput, text = "  Back/Select: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyGuitarBackLabel.grid(row = 9, column = 0, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyGuitarBackLabelTip = Hovertip(inputKeyGuitarBackLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarBackEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyGuitarBackEntry.grid(row = 9, column = 1, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarBackEntryTip = Hovertip(inputKeyGuitarBackEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarBackEntry.insert(0, wtde_decode_input(keyGuitarString, "BACK"))

# =============== CANCEL INPUTS =============== #

inputKeyGuitarCancelLabel = Label(wtdeOptionsInput, text = "   Cancel: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyGuitarCancelLabel.grid(row = 10, column = 0, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyGuitarCancelLabelTip = Hovertip(inputKeyGuitarCancelLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarCancelEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyGuitarCancelEntry.grid(row = 10, column = 1, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarCancelEntryTip = Hovertip(inputKeyGuitarCancelEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarCancelEntry.insert(0, wtde_decode_input(keyGuitarString, "CANCEL"))

# =============== WHAMMY INPUTS =============== #

inputKeyGuitarWhammyLabel = Label(wtdeOptionsInput, text = "   Whammy: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyGuitarWhammyLabel.grid(row = 11, column = 0, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyGuitarWhammyLabelTip = Hovertip(inputKeyGuitarWhammyLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarWhammyEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyGuitarWhammyEntry.grid(row = 11, column = 1, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarWhammyEntryTip = Hovertip(inputKeyGuitarWhammyEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarWhammyEntry.insert(0, wtde_decode_input(keyGuitarString, "WHAMMY"))

# =============== UP INPUTS =============== #

inputKeyGuitarUpLabel = Label(wtdeOptionsInput, text = "       Up: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyGuitarUpLabel.grid(row = 12, column = 0, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyGuitarUpLabelTip = Hovertip(inputKeyGuitarUpLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarUpEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyGuitarUpEntry.grid(row = 12, column = 1, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarUpEntryTip = Hovertip(inputKeyGuitarUpEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarUpEntry.insert(0, wtde_decode_input(keyGuitarString, "UP"))

# =============== DOWN INPUTS =============== #

inputKeyGuitarDownLabel = Label(wtdeOptionsInput, text = "     Down: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyGuitarDownLabel.grid(row = 13, column = 0, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyGuitarDownLabelTip = Hovertip(inputKeyGuitarDownLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarDownEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyGuitarDownEntry.grid(row = 13, column = 1, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarDownEntryTip = Hovertip(inputKeyGuitarDownEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarDownEntry.insert(0, wtde_decode_input(keyGuitarString, "DOWN"))

# =============== LEFT INPUTS =============== #

inputKeyGuitarLeftLabel = Label(wtdeOptionsInput, text = "     Left: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyGuitarLeftLabel.grid(row = 14, column = 0, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyGuitarLeftLabelTip = Hovertip(inputKeyGuitarLeftLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarLeftEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyGuitarLeftEntry.grid(row = 14, column = 1, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarLeftEntryTip = Hovertip(inputKeyGuitarLeftEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarLeftEntry.insert(0, wtde_decode_input(keyGuitarString, "LEFT"))

# =============== RIGHT INPUTS =============== #

inputKeyGuitarRightLabel = Label(wtdeOptionsInput, text = "    Right: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyGuitarRightLabel.grid(row = 15, column = 0, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyGuitarRightLabelTip = Hovertip(inputKeyGuitarRightLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarRightEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyGuitarRightEntry.grid(row = 15, column = 1, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyGuitarRightEntryTip = Hovertip(inputKeyGuitarRightEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyGuitarRightEntry.insert(0, wtde_decode_input(keyGuitarString, "RIGHT"))

# ============================================= #
#                   DRUM INPUTS                 #
# ============================================= #

INPUT_FIELD_POST_LABEL_PADX = 10

inputKeyDrumsLabel = Label(wtdeOptionsInput, text = " Drums Keyboard Controls:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', image = INPUT_DRUMS_ICON, compound = 'left')
inputKeyDrumsLabel.grid(row = 1, column = 2, columnspan = 2, padx = INPUT_FIELD_POST_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyDrumsLabelTip = Hovertip(inputKeyDrumsLabel, KEY_INPUT_TIP, HOVER_DELAY)

# =============== RED INPUTS =============== #

inputKeyDrumsRedLabel = Label(wtdeOptionsInput, text = "         Red: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyDrumsRedLabel.grid(row = 2, column = 2, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyDrumsRedLabelTip = Hovertip(inputKeyDrumsRedLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsRedEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyDrumsRedEntry.grid(row = 2, column = 3, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyDrumsRedEntryTip = Hovertip(inputKeyDrumsRedEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsRedEntry.insert(0, wtde_decode_input(keyDrumString, "RED"))

# =============== YELLOW INPUTS =============== #

inputKeyDrumsYellowLabel = Label(wtdeOptionsInput, text = "      Yellow: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyDrumsYellowLabel.grid(row = 3, column = 2, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyDrumsYellowLabelTip = Hovertip(inputKeyDrumsYellowLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsYellowEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyDrumsYellowEntry.grid(row = 3, column = 3, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyDrumsYellowEntryTip = Hovertip(inputKeyDrumsYellowEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsYellowEntry.insert(0, wtde_decode_input(keyDrumString, "YELLOW"))

# =============== BLUE INPUTS =============== #

inputKeyDrumsBlueLabel = Label(wtdeOptionsInput, text = "        Blue: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyDrumsBlueLabel.grid(row = 4, column = 2, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyDrumsBlueLabelTip = Hovertip(inputKeyDrumsBlueLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsBlueEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyDrumsBlueEntry.grid(row = 4, column = 3, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyDrumsBlueEntryTip = Hovertip(inputKeyDrumsBlueEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsBlueEntry.insert(0, wtde_decode_input(keyDrumString, "BLUE"))

# =============== ORANGE INPUTS =============== #

inputKeyDrumsOrangeLabel = Label(wtdeOptionsInput, text = "      Orange: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyDrumsOrangeLabel.grid(row = 5, column = 2, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyDrumsOrangeLabelTip = Hovertip(inputKeyDrumsOrangeLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsOrangeEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyDrumsOrangeEntry.grid(row = 5, column = 3, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyDrumsOrangeEntryTip = Hovertip(inputKeyDrumsOrangeEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsOrangeEntry.insert(0, wtde_decode_input(keyDrumString, "ORANGE"))

# =============== GREEN INPUTS =============== #

inputKeyDrumsGreenLabel = Label(wtdeOptionsInput, text = "       Green: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyDrumsGreenLabel.grid(row = 6, column = 2, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyDrumsGreenLabelTip = Hovertip(inputKeyDrumsGreenLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsGreenEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyDrumsGreenEntry.grid(row = 6, column = 3, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyDrumsGreenEntryTip = Hovertip(inputKeyDrumsGreenEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsGreenEntry.insert(0, wtde_decode_input(keyDrumString, "GREEN"))

# =============== KICK INPUTS =============== #

inputKeyDrumsKickLabel = Label(wtdeOptionsInput, text = "   Kick Drum: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyDrumsKickLabel.grid(row = 7, column = 2, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyDrumsKickLabelTip = Hovertip(inputKeyDrumsKickLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsKickEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyDrumsKickEntry.grid(row = 7, column = 3, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyDrumsKickEntryTip = Hovertip(inputKeyDrumsKickEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsKickEntry.insert(0, wtde_decode_input(keyDrumString, "KICK"))

# =============== START INPUTS =============== #

inputKeyDrumsStartLabel = Label(wtdeOptionsInput, text = "      Start: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyDrumsStartLabel.grid(row = 8, column = 2, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyDrumsStartLabelTip = Hovertip(inputKeyDrumsStartLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsStartEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyDrumsStartEntry.grid(row = 8, column = 3, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyDrumsStartEntryTip = Hovertip(inputKeyDrumsStartEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsStartEntry.insert(0, wtde_decode_input(keyDrumString, "START"))

# =============== BACK INPUTS =============== #

inputKeyDrumsBackLabel = Label(wtdeOptionsInput, text = "  Back/Select: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyDrumsBackLabel.grid(row = 9, column = 2, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyDrumsBackLabelTip = Hovertip(inputKeyDrumsBackLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsBackEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyDrumsBackEntry.grid(row = 9, column = 3, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyDrumsBackEntryTip = Hovertip(inputKeyDrumsBackEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsBackEntry.insert(0, wtde_decode_input(keyDrumString, "BACK"))

# =============== CANCEL INPUTS =============== #

inputKeyDrumsCancelLabel = Label(wtdeOptionsInput, text = "   Cancel: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyDrumsCancelLabel.grid(row = 10, column = 2, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyDrumsCancelLabelTip = Hovertip(inputKeyDrumsCancelLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsCancelEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyDrumsCancelEntry.grid(row = 10, column = 3, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyDrumsCancelEntryTip = Hovertip(inputKeyDrumsCancelEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsCancelEntry.insert(0, wtde_decode_input(keyDrumString, "CANCEL"))

# =============== UP INPUTS =============== #

inputKeyDrumsUpLabel = Label(wtdeOptionsInput, text = "       Up: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyDrumsUpLabel.grid(row = 11, column = 2, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyDrumsUpLabelTip = Hovertip(inputKeyDrumsUpLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsUpEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyDrumsUpEntry.grid(row = 11, column = 3, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyDrumsUpEntryTip = Hovertip(inputKeyDrumsUpEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsUpEntry.insert(0, wtde_decode_input(keyDrumString, "UP"))

# =============== DOWN INPUTS =============== #

inputKeyDrumsDownLabel = Label(wtdeOptionsInput, text = "     Down: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyDrumsDownLabel.grid(row = 12, column = 2, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyDrumsDownLabelTip = Hovertip(inputKeyDrumsDownLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsDownEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyDrumsDownEntry.grid(row = 12, column = 3, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyDrumsDownEntryTip = Hovertip(inputKeyDrumsDownEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyDrumsDownEntry.insert(0, wtde_decode_input(keyDrumString, "DOWN"))

# ============================================= #
#                   MIC INPUTS                  #
# ============================================= #
inputKeyMicLabel = Label(wtdeOptionsInput, text = " Mic Keyboard Controls:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', image = INPUT_MIC_ICON, compound = 'left')
inputKeyMicLabel.grid(row = 1, column = 4, columnspan = 2, padx = INPUT_FIELD_POST_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMicLabelTip = Hovertip(inputKeyMicLabel, KEY_INPUT_TIP, HOVER_DELAY)

# =============== GREEN INPUTS =============== #

inputKeyMicGreenLabel = Label(wtdeOptionsInput, text = "       Green: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMicGreenLabel.grid(row = 2, column = 4, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMicGreenLabelTip = Hovertip(inputKeyMicGreenLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicGreenEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMicGreenEntry.grid(row = 2, column = 5, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMicGreenEntryTip = Hovertip(inputKeyMicGreenEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicGreenEntry.insert(0, wtde_decode_input(keyVocalString, "GREEN"))

# =============== RED INPUTS =============== #

inputKeyMicRedLabel = Label(wtdeOptionsInput, text = "         Red: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMicRedLabel.grid(row = 3, column = 4, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMicRedLabelTip = Hovertip(inputKeyMicRedLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicRedEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMicRedEntry.grid(row = 3, column = 5, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMicRedEntryTip = Hovertip(inputKeyMicRedEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicRedEntry.insert(0, wtde_decode_input(keyVocalString, "RED"))

# =============== YELLOW INPUTS =============== #

inputKeyMicYellowLabel = Label(wtdeOptionsInput, text = "      Yellow: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMicYellowLabel.grid(row = 4, column = 4, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMicYellowLabelTip = Hovertip(inputKeyMicYellowLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicYellowEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMicYellowEntry.grid(row = 4, column = 5, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMicYellowEntryTip = Hovertip(inputKeyMicYellowEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicYellowEntry.insert(0, wtde_decode_input(keyVocalString, "YELLOW"))

# =============== BLUE INPUTS =============== #

inputKeyMicBlueLabel = Label(wtdeOptionsInput, text = "        Blue: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMicBlueLabel.grid(row = 5, column = 4, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMicBlueLabelTip = Hovertip(inputKeyMicBlueLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicBlueEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMicBlueEntry.grid(row = 5, column = 5, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMicBlueEntryTip = Hovertip(inputKeyMicBlueEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicBlueEntry.insert(0, wtde_decode_input(keyVocalString, "BLUE"))

# =============== ORANGE INPUTS =============== #

inputKeyMicOrangeLabel = Label(wtdeOptionsInput, text = "      Orange: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMicOrangeLabel.grid(row = 6, column = 4, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMicOrangeLabelTip = Hovertip(inputKeyMicOrangeLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicOrangeEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMicOrangeEntry.grid(row = 6, column = 5, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMicOrangeEntryTip = Hovertip(inputKeyMicOrangeEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicOrangeEntry.insert(0, wtde_decode_input(keyVocalString, "ORANGE"))

# =============== START INPUTS =============== #

inputKeyMicStartLabel = Label(wtdeOptionsInput, text = "       Start: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMicStartLabel.grid(row = 7, column = 4, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMicStartLabelTip = Hovertip(inputKeyMicStartLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicStartEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMicStartEntry.grid(row = 7, column = 5, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMicStartEntryTip = Hovertip(inputKeyMicStartEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicStartEntry.insert(0, wtde_decode_input(keyVocalString, "START"))

# =============== BACK INPUTS =============== #

inputKeyMicBackLabel = Label(wtdeOptionsInput, text = "  Back/Select: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMicBackLabel.grid(row = 8, column = 4, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMicBackLabelTip = Hovertip(inputKeyMicBackLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicBackEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMicBackEntry.grid(row = 8, column = 5, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMicBackEntryTip = Hovertip(inputKeyMicBackEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicBackEntry.insert(0, wtde_decode_input(keyVocalString, "BACK"))

# =============== CANCEL INPUTS =============== #

inputKeyMicCancelLabel = Label(wtdeOptionsInput, text = "       Cancel: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMicCancelLabel.grid(row = 9, column = 4, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMicCancelLabelTip = Hovertip(inputKeyMicCancelLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicCancelEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMicCancelEntry.grid(row = 9, column = 5, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMicCancelEntryTip = Hovertip(inputKeyMicCancelEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicCancelEntry.insert(0, wtde_decode_input(keyVocalString, "CANCEL"))

# =============== MIC VOLUME DOWN INPUTS =============== #

inputKeyMicMVDLabel = Label(wtdeOptionsInput, text = " Mic Vol. Down: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMicMVDLabel.grid(row = 10, column = 4, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMicMVDLabelTip = Hovertip(inputKeyMicMVDLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicMVDEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMicMVDEntry.grid(row = 10, column = 5, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMicMVDEntryTip = Hovertip(inputKeyMicMVDEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicMVDEntry.insert(0, wtde_decode_input(keyVocalString, "MIC_VOL_DOWN"))

# =============== UP INPUTS =============== #

inputKeyMicUpLabel = Label(wtdeOptionsInput, text = "           Up: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMicUpLabel.grid(row = 11, column = 4, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMicUpLabelTip = Hovertip(inputKeyMicUpLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicUpEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMicUpEntry.grid(row = 11, column = 5, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMicUpEntryTip = Hovertip(inputKeyMicUpEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicUpEntry.insert(0, wtde_decode_input(keyVocalString, "UP"))

# =============== DOWN INPUTS =============== #

inputKeyMicDownLabel = Label(wtdeOptionsInput, text = "         Down: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMicDownLabel.grid(row = 12, column = 4, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMicDownLabelTip = Hovertip(inputKeyMicDownLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicDownEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMicDownEntry.grid(row = 12, column = 5, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMicDownEntryTip = Hovertip(inputKeyMicDownEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMicDownEntry.insert(0, wtde_decode_input(keyVocalString, "DOWN"))

# ============================================= #
#                  MENU INPUTS                  #
# ============================================= #

inputKeyMenuLabel = Label(wtdeOptionsInput, text = "Menu Keyboard Controls:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
inputKeyMenuLabel.grid(row = 1, column = 6, columnspan = 2, padx = INPUT_FIELD_POST_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuLabelTip = Hovertip(inputKeyMenuLabel, KEY_INPUT_TIP, HOVER_DELAY)

# =============== GREEN INPUTS =============== #

inputKeyMenuGreenLabel = Label(wtdeOptionsInput, text = "     Green: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMenuGreenLabel.grid(row = 2, column = 6, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMenuGreenLabelTip = Hovertip(inputKeyMenuGreenLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuGreenEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMenuGreenEntry.grid(row = 2, column = 7, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuGreenEntryTip = Hovertip(inputKeyMenuGreenEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuGreenEntry.insert(0, wtde_decode_input(keyMenuString, "GREEN"))

# =============== RED INPUTS =============== #

inputKeyMenuRedLabel = Label(wtdeOptionsInput, text = "       Red: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMenuRedLabel.grid(row = 3, column = 6, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMenuRedLabelTip = Hovertip(inputKeyMenuRedLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuRedEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMenuRedEntry.grid(row = 3, column = 7, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuRedEntryTip = Hovertip(inputKeyMenuRedEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuRedEntry.insert(0, wtde_decode_input(keyMenuString, "RED"))

# =============== YELLOW INPUTS =============== #

inputKeyMenuYellowLabel = Label(wtdeOptionsInput, text = "    Yellow: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMenuYellowLabel.grid(row = 4, column = 6, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMenuYellowLabelTip = Hovertip(inputKeyMenuYellowLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuYellowEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMenuYellowEntry.grid(row = 4, column = 7, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuYellowEntryTip = Hovertip(inputKeyMenuYellowEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuYellowEntry.insert(0, wtde_decode_input(keyMenuString, "YELLOW"))

# =============== BLUE INPUTS =============== #

inputKeyMenuBlueLabel = Label(wtdeOptionsInput, text = "      Blue: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMenuBlueLabel.grid(row = 5, column = 6, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMenuBlueLabelTip = Hovertip(inputKeyMenuBlueLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuBlueEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMenuBlueEntry.grid(row = 5, column = 7, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuBlueEntryTip = Hovertip(inputKeyMenuBlueEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuBlueEntry.insert(0, wtde_decode_input(keyMenuString, "BLUE"))

# =============== ORANGE INPUTS =============== #

inputKeyMenuOrangeLabel = Label(wtdeOptionsInput, text = "    Orange: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMenuOrangeLabel.grid(row = 6, column = 6, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMenuOrangeLabelTip = Hovertip(inputKeyMenuOrangeLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuOrangeEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMenuOrangeEntry.grid(row = 6, column = 7, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuOrangeEntryTip = Hovertip(inputKeyMenuOrangeEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuOrangeEntry.insert(0, wtde_decode_input(keyMenuString, "ORANGE"))

# =============== START INPUTS =============== #

inputKeyMenuStartLabel = Label(wtdeOptionsInput, text = "     Start: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMenuStartLabel.grid(row = 7, column = 6, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMenuStartLabelTip = Hovertip(inputKeyMenuStartLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuStartEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMenuStartEntry.grid(row = 7, column = 7, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuStartEntryTip = Hovertip(inputKeyMenuStartEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuStartEntry.insert(0, wtde_decode_input(keyMenuString, "START"))

# =============== BACK INPUTS =============== #

inputKeyMenuBackLabel = Label(wtdeOptionsInput, text = " Back/Select: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMenuBackLabel.grid(row = 8, column = 6, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMenuBackLabelTip = Hovertip(inputKeyMenuBackLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuBackEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMenuBackEntry.grid(row = 8, column = 7, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuBackEntryTip = Hovertip(inputKeyMenuBackEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuBackEntry.insert(0, wtde_decode_input(keyMenuString, "BACK"))

# =============== CANCEL INPUTS =============== #

inputKeyMenuCancelLabel = Label(wtdeOptionsInput, text = "   Cancel: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMenuCancelLabel.grid(row = 9, column = 6, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMenuCancelLabelTip = Hovertip(inputKeyMenuCancelLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuCancelEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMenuCancelEntry.grid(row = 9, column = 7, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuCancelEntryTip = Hovertip(inputKeyMenuCancelEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuCancelEntry.insert(0, wtde_decode_input(keyMenuString, "CANCEL"))

# =============== WHAMMY INPUTS =============== #

inputKeyMenuWhammyLabel = Label(wtdeOptionsInput, text = "   Whammy: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMenuWhammyLabel.grid(row = 10, column = 6, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMenuWhammyLabelTip = Hovertip(inputKeyMenuCancelLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuWhammyEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMenuWhammyEntry.grid(row = 10, column = 7, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuWhammyEntryTip = Hovertip(inputKeyMenuWhammyEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuWhammyEntry.insert(0, wtde_decode_input(keyMenuString, "WHAMMY"))

# =============== KICK INPUTS =============== #

inputKeyMenuKickLabel = Label(wtdeOptionsInput, text = "Kick Drum: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMenuKickLabel.grid(row = 11, column = 6, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMenuKickLabelTip = Hovertip(inputKeyMenuKickLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuKickEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMenuKickEntry.grid(row = 11, column = 7, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuKickEntryTip = Hovertip(inputKeyMenuKickEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuKickEntry.insert(0, wtde_decode_input(keyMenuString, "KICK"))

# =============== UP INPUTS =============== #

inputKeyMenuUpLabel = Label(wtdeOptionsInput, text = "       Up: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMenuUpLabel.grid(row = 12, column = 6, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMenuUpLabelTip = Hovertip(inputKeyMenuUpLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuUpEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMenuUpEntry.grid(row = 12, column = 7, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuUpEntryTip = Hovertip(inputKeyMenuUpEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuUpEntry.insert(0, wtde_decode_input(keyMenuString, "UP"))

# =============== DOWN INPUTS =============== #

inputKeyMenuDownLabel = Label(wtdeOptionsInput, text = "     Down: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMenuDownLabel.grid(row = 13, column = 6, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMenuDownLabelTip = Hovertip(inputKeyMenuDownLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuDownEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMenuDownEntry.grid(row = 13, column = 7, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuDownEntryTip = Hovertip(inputKeyMenuDownEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuDownEntry.insert(0, wtde_decode_input(keyMenuString, "DOWN"))

# =============== LEFT INPUTS =============== #

inputKeyMenuLeftLabel = Label(wtdeOptionsInput, text = "     Left: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMenuLeftLabel.grid(row = 14, column = 6, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMenuLeftLabelTip = Hovertip(inputKeyMenuLeftLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuLeftEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMenuLeftEntry.grid(row = 14, column = 7, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuLeftEntryTip = Hovertip(inputKeyMenuLeftEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuLeftEntry.insert(0, wtde_decode_input(keyMenuString, "LEFT"))

# =============== RIGHT INPUTS =============== #

inputKeyMenuRightLabel = Label(wtdeOptionsInput, text = "    Right: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputKeyMenuRightLabel.grid(row = 15, column = 6, padx = INPUT_FIELD_LABEL_PADX, pady = INPUT_FIELD_LABEL_PADY, sticky = 'e')
inputKeyMenuRightLabelTip = Hovertip(inputKeyMenuRightLabel, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuRightEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = INPUT_MAPPING_ENTRY_WIDTH)
inputKeyMenuRightEntry.grid(row = 15, column = 7, pady = INPUT_FIELD_LABEL_PADY, sticky = 'w')
inputKeyMenuRightEntryTip = Hovertip(inputKeyMenuRightEntry, KEY_INPUT_TIP, HOVER_DELAY)

inputKeyMenuRightEntry.insert(0, wtde_decode_input(keyMenuString, "RIGHT"))

# ============================================= #
#         MICROPHONE AND EXTRA SETTINGS         #
# ============================================= #
# Change directory to our INI folder.
OS.chdir(wtde_find_config())
config.read("GHWTDE.ini")
config.optionxform = str

# Get a list of all plugged in and supported microphones.
micDeviceList = ["None"] + mic_name_get_list()

# We don't need the Microsoft Sound Mapper, so just get rid of it.
msmName = "Microsoft Sound Mapper - Input"
if (micDeviceList.count(msmName) > 0):
    for (item) in (micDeviceList):
        if (item == msmName): micDeviceList.remove(msmName)
micDevice = StringVar()

# Update the dropdown menu with the default device from the INI.
micDevice.set(config.get("Audio", "MicDevice"))

# Microphone selection option.
MIC_SELECT_TIP = "Select the microphone you want to use for vocal play in-game.\n\n" \
                 "A list of all supported devices will be shown. To disable, select None.\n" \
                 "If your microphone has non-ASCII characters in its name, it might be best\n" \
                 "to rename it in the Sound settings in Windows."

inputMicListLabel = Label(wtdeOptionsInput, text = "Microphone: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputMicListLabel.grid(row = 16, column = 0, pady = 4)
inputMicListLabelTip = Hovertip(inputMicListLabel, MIC_SELECT_TIP, HOVER_DELAY)

inputMicList = OptionMenu(wtdeOptionsInput, micDevice, *micDeviceList)
inputMicList.config(width = 30, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
inputMicList.grid(row = 16, column = 1, pady = 5, columnspan = 2, sticky = 'w')
inputMicListTip = Hovertip(inputMicList, MIC_SELECT_TIP, HOVER_DELAY)

# Vocal audio delay amount.
MIC_AUDIO_DELAY_TIP = "Set the vocal audio delay.\n\n" \
                      "In other words, this physically moves the notes on the vocal highway by\n" \
                      "the given interval, in milliseconds.\n\n" \
                      "If the notes are coming too early, increase this value.\n" \
                      "If the notes are coming too late, decrease this value."
inputMicDelayLabel = Label(wtdeOptionsInput, text = "Mic Audio Delay:    ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputMicDelayLabel.grid(row = 16, column = 3, pady = 4, sticky = 'e')
inputMicDelayLabelTip = Hovertip(inputMicDelayLabel, MIC_AUDIO_DELAY_TIP, HOVER_DELAY)

inputMicDelayEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = 10)
inputMicDelayEntry.grid(row = 16, column = 4, pady = 4, sticky = 'w')
inputMicDelayEntryTip = Hovertip(inputMicDelayEntry, MIC_AUDIO_DELAY_TIP, HOVER_DELAY)

# Vocal visual delay amount.
MIC_VIDEO_DELAY_TIP = "Set the vocal video delay.\n\n" \
                      "In other words, this physically moves the notes on the vocal highway by\n" \
                      "the given interval, in milliseconds.\n\n" \
                      "If the notes are coming too early, increase this value.\n" \
                      "If the notes are coming too late, decrease this value."
inputMicVideoDelayLabel = Label(wtdeOptionsInput, text = "Mic Video Delay:    ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
inputMicVideoDelayLabel.grid(row = 17, column = 3, pady = 4, sticky = 'e')
inputMicVideoDelayLabelTip = Hovertip(inputMicVideoDelayLabel, MIC_VIDEO_DELAY_TIP, HOVER_DELAY)

inputMicVideoDelayEntry = Entry(wtdeOptionsInput, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = 10)
inputMicVideoDelayEntry.grid(row = 17, column = 4, pady = 4, sticky = 'w')
inputMicVideoDelayEntryTip = Hovertip(inputMicVideoDelayEntry, MIC_VIDEO_DELAY_TIP, HOVER_DELAY)

# Use recommended mic values.
USE_RECOMMENDED_TIP = "Set your Mic calibration to the recommended values."
inputMicUseRecommended = Button(wtdeOptionsInput, text = "Use Recommended Calibration", font = FONT_INFO_DROPDOWN, width = 30, height = 1, command = lambda: mic_set_calibration(-80, -315), bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG)
inputMicUseRecommended.grid(row = 18, column = 3, columnspan = 2, pady = 5)
inputMicUseRecommendedTip = Hovertip(inputMicUseRecommended, USE_RECOMMENDED_TIP, HOVER_DELAY)

# Use input hack.
inputHack = StringVar()
INPUT_HACK_TIP = "Enable or disable the input hack."
inputUseInputHack = Checkbutton(wtdeOptionsInput, text = f"  Use Input Hack", variable = inputHack, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
inputUseInputHack.grid(row = 16, column = 5, pady = 4, sticky = 'w')
inputUseInputHackTip = Hovertip(inputUseInputHack, INPUT_HACK_TIP, HOVER_DELAY)

# ====================================================================== #
#                          GRAPHICS SETTINGS TAB                         #
# ====================================================================== #
# Make sure we're in the INI directory.
OS.chdir(wtde_find_config())
config.read("GHWTDE.ini")

# Graphics settings tab information.
TAB_INFO_GRAPHICS = "Graphics Settings: Set your preferences for graphics in WTDE.\nHover over any option to see what it does!"
graphicsInfoLabel = Label(wtdeOptionsGraphics, text = TAB_INFO_GRAPHICS, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
graphicsInfoLabel.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

# Set game resolution.
RESOLUTION_TIP = "Set the resolution for the game."
RES_WIDTH_TIP = "Set the width of the game window."
RES_HEIGHT_TIP = "Set the height of the game window."

graphicsResolutionLabel = Label(wtdeOptionsGraphics, text = "    Resolution:                          X", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
graphicsResolutionLabel.grid(row = 1, column = 0, pady = 5, sticky = 'w')
graphicsResolutionLabel = Hovertip(graphicsResolutionLabel, RESOLUTION_TIP, HOVER_DELAY)

graphicsResolutionWidth = Entry(wtdeOptionsGraphics, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = 10, validate = 'key')
graphicsResolutionWidth.place(x = 128, y = 50)
graphicsResolutionWidth.config(validatecommand = (graphicsResolutionWidth.register(input_verify_numeric), '%P', '%d'))
graphicsResolutionWidthTip = Hovertip(graphicsResolutionWidth, RES_WIDTH_TIP, HOVER_DELAY)

graphicsResolutionHeight = Entry(wtdeOptionsGraphics, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = 10, validate = 'key')
graphicsResolutionHeight.place(x = 242, y = 50)
graphicsResolutionHeight.config(validatecommand = (graphicsResolutionHeight.register(input_verify_numeric), '%P', '%d'))
graphicsResolutionHeightTip = Hovertip(graphicsResolutionHeight, RES_HEIGHT_TIP, HOVER_DELAY)

graphicsResolutionWidth.insert(0, resWidth)
graphicsResolutionHeight.insert(0, resHeight)

# Use native resolution.
useNativeResolution = StringVar()
NATIVE_RESOLUTION_TIP = "Use the native resolution of your primary monitor as the resolution the game will run at."

graphicsUseNativeRes = Checkbutton(wtdeOptionsGraphics, text = f"  Native Monitor Resolution ({get_screen_resolution()[0]} X {get_screen_resolution()[1]})", variable = useNativeResolution, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsUseNativeRes.grid(row = 2, column = 0, padx = 20, pady = 5, sticky = 'w')
graphicsUseNativeResTip = Hovertip(graphicsUseNativeRes, NATIVE_RESOLUTION_TIP, HOVER_DELAY)

# Set target FPS.
fpsLimit = StringVar()
fpsLimitOptions = ["15 FPS", "24 FPS", "30 FPS", "60 FPS", "120 FPS", "240 FPS", "Unlimited"]

FPS_LIMIT_TIP = "Set the limit for the game's frame rate.\n\n" \
                "Setting this value will set the target frame rate that the game will try\n" \
                "to run at. Remember that if Vertical Sync (VSync) is turned ON,\n" \
                "it will override this and lock the framerate at 60 FPS!"

graphicsFPSLimitLabel = Label(wtdeOptionsGraphics, text = "    FPS Limit:  ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
graphicsFPSLimitLabel.grid(row = 3, column = 0, pady = 5, sticky = 'w')
graphicsFPSLimitLabelTip = Hovertip(graphicsFPSLimitLabel, FPS_LIMIT_TIP, HOVER_DELAY)

graphicsFPSLimit = OptionMenu(wtdeOptionsGraphics, fpsLimit, *fpsLimitOptions)
graphicsFPSLimit.config(width = 10, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
graphicsFPSLimit.place(x = 128, y = 124)
graphicsFPSLimitTip = Hovertip(graphicsFPSLimit, FPS_LIMIT_TIP, HOVER_DELAY)


# Enable/disable vertical sync.
disableVSync = StringVar()
VSYNC_LIMIT_TIP = "Turn ON or OFF vertical sync. If this is ON, it will cap the game at\n" \
                  "60 FPS, regardless of the set FPS limit. Helps aid screen tearing!"
graphicsUseVSync = Checkbutton(wtdeOptionsGraphics, text = "  Use Vertical Sync", variable = disableVSync, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsUseVSync.grid(row = 4, column = 0, padx = 20, pady = 5, sticky = 'w')
graphicsUseVSyncTip = Hovertip(graphicsUseVSync, VSYNC_LIMIT_TIP, HOVER_DELAY)

# Enable/disable hit sparks.
hitSparks = StringVar()
HIT_SPARKS_TIP = "Turn ON or OFF sparks when notes are hit."
graphicsUseHitSparks = Checkbutton(wtdeOptionsGraphics, text = "  Show Hit Sparks", variable = hitSparks, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsUseHitSparks.grid(row = 5, column = 0, padx = 20, pady = 5, sticky = 'w')
graphicsUseHitSparksTip = Hovertip(graphicsUseHitSparks, HIT_SPARKS_TIP, HOVER_DELAY)

# Enable/disable depth of field.
disableDOF = StringVar()
USE_DOF_TIP = "Turn ON or OFF depth of field."
graphicsUseDOF = Checkbutton(wtdeOptionsGraphics, text = "  Depth of Field", variable = disableDOF, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsUseDOF.grid(row = 6, column = 0, padx = 20, pady = 5, sticky = 'w')
graphicsUseDOFTip = Hovertip(graphicsUseDOF, USE_DOF_TIP, HOVER_DELAY)

# Enable/disable windowed mode.
windowedMode = StringVar()
WINDOWED_MODE_TIP = "Run the game in windowed mode."
graphicsWindowedMode = Checkbutton(wtdeOptionsGraphics, text = "  Windowed Mode", variable = windowedMode, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsWindowedMode.grid(row = 7, column = 0, padx = 20, pady = 5, sticky = 'w')
graphicsWindowedModeTip = Hovertip(graphicsWindowedMode, WINDOWED_MODE_TIP, HOVER_DELAY)

# Enable/disable borderless windowed mode.
borderlessMode = StringVar()
BORDERLESS_MODE_TIP = "Run the game in borderless windowed mode."
graphicsBorderlessMode = Checkbutton(wtdeOptionsGraphics, text = "  Borderless Windowed", variable = borderlessMode, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsBorderlessMode.grid(row = 8, column = 0, padx = 20, pady = 5, sticky = 'w')
graphicsBorderlessModeTip = Hovertip(graphicsBorderlessMode, BORDERLESS_MODE_TIP, HOVER_DELAY)

# Enable/disable bloom.
bloomFX = StringVar()
BLOOM_FX_TIP = "Turn ON or OFF bloom."
graphicsUseBloom = Checkbutton(wtdeOptionsGraphics, text = "  Use Bloom", variable = bloomFX, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsUseBloom.grid(row = 9, column = 0, padx = 20, pady = 5, sticky = 'w')
graphicsUseBloomTip = Hovertip(graphicsUseBloom, BLOOM_FX_TIP, HOVER_DELAY)

# Enable/disable color filters.
colorFilters = StringVar()
COLOR_FILTERS_TIP = "Turn ON or OFF color filters. These are filters primarily used in\n" \
                    "Guitar Hero: Metallica."
graphicsUseColorFilters = Checkbutton(wtdeOptionsGraphics, text = "  Use Color Filters", variable = colorFilters, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsUseColorFilters.grid(row = 10, column = 0, padx = 20, pady = 5, sticky = 'w')
graphicsUseColorFiltersTip = Hovertip(graphicsUseColorFilters, COLOR_FILTERS_TIP, HOVER_DELAY)

# Enable/disable anti-aliasing.
antiAliasing = StringVar()
ANTIALIASING_TIP = "Turn ON or OFF anti-aliasing. The anti-aliasing used by GHWT is multi-sampling."
graphicsUseAntiAliasing = Checkbutton(wtdeOptionsGraphics, text = "  Use Anti-Aliasing", variable = antiAliasing, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsUseAntiAliasing.grid(row = 11, column = 0, padx = 20, pady = 5, sticky = 'w')
graphicsUseAntiAliasingTip = Hovertip(graphicsUseAntiAliasing, ANTIALIASING_TIP, HOVER_DELAY)

# Enable/disable particle rendering.
renderParticles = StringVar()
RENDER_PARTICLES_TIP = "Turn ON or OFF rendering of particles. This includes things like fire, sparks, smoke, etc."
graphicsRenderParticles = Checkbutton(wtdeOptionsGraphics, text = "  Render Particles", variable = renderParticles, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsRenderParticles.grid(row = 12, column = 0, padx = 20, pady = 5, sticky = 'w')
graphicsRenderParticlesTip = Hovertip(graphicsRenderParticles, RENDER_PARTICLES_TIP, HOVER_DELAY)

# Enable/disable level geometry.
renderGeoms = StringVar()
RENDER_GEOMETRY_TIP = "Turn ON or OFF rendering of level geometry, except level objects."
graphicsRenderGeoms = Checkbutton(wtdeOptionsGraphics, text = "  Render Level Geometry", variable = renderGeoms, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsRenderGeoms.grid(row = 13, column = 0, padx = 20, pady = 5, sticky = 'w')
graphicsRenderGeomsTip = Hovertip(graphicsRenderGeoms, RENDER_GEOMETRY_TIP, HOVER_DELAY)

# Enable/disable instance rendering.
renderInstances = StringVar()
RENDER_INSTANCES_TIP = "Turn ON or OFF rendering of instances. Controls rendering of things like dynamic\n" \
                       "and level objects. Also includes characters and anything that moves."
graphicsRenderInstances = Checkbutton(wtdeOptionsGraphics, text = "  Render Instances", variable = renderInstances, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsRenderInstances.grid(row = 14, column = 0, padx = 20, pady = 5, sticky = 'w')
graphicsRenderInstancesTip = Hovertip(graphicsRenderInstances, RENDER_INSTANCES_TIP, HOVER_DELAY)

# Enable/disable draw projectors.
drawProjectors = StringVar()
DRAW_PROJECTORS_TIP = "Turn ON or OFF rendering of projectors. These are things like spotlight projectors that\n" \
                      "show under characters and cast shadows."
graphicsDrawProjectors = Checkbutton(wtdeOptionsGraphics, text = "  Draw Projectors", variable = drawProjectors, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsDrawProjectors.grid(row = 15, column = 0, padx = 20, pady = 5, sticky = 'w')
graphicsDrawProjectorsTip = Hovertip(graphicsDrawProjectors, DRAW_PROJECTORS_TIP, HOVER_DELAY)

# Enable/disable 2D rendering.
render2D = StringVar()
RENDER_2D_TIP = "Turn ON or OFF rendering 2D items.\n\n" \
                "Note: If this is OFF, this disables rendering of ALL 2D elements, including the HUD and GUI!"
graphicsRender2D = Checkbutton(wtdeOptionsGraphics, text = "  Render 2D Items", variable = render2D, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsRender2D.grid(row = 1, column = 1, padx = 40, pady = 5, sticky = 'w')
graphicsRender2DTip = Hovertip(graphicsRender2D, RENDER_2D_TIP, HOVER_DELAY)

# Enable/disable screen FX rendering.
renderScreenFX = StringVar()
RENDER_SCREEN_FX_TIP = "Turn ON or OFF rendering of screen effects, such as bloom, depth of field, saturation, etc."
graphicsRenderScreenFX = Checkbutton(wtdeOptionsGraphics, text = "  Render Screen FX", variable = renderScreenFX, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsRenderScreenFX.grid(row = 2, column = 1, padx = 40, pady = 5, sticky = 'w')
graphicsRenderScreenFXTip = Hovertip(graphicsRenderScreenFX, RENDER_SCREEN_FX_TIP, HOVER_DELAY)

# Enable/disable black stage.
blackStage = StringVar()
BLACK_STAGE_TIP = "Turn ON or OFF black stage. Makes the stage completely black and hides all band members."
graphicsBlackStage = Checkbutton(wtdeOptionsGraphics, text = "  Black Stage", variable = blackStage, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsBlackStage.grid(row = 3, column = 1, padx = 40, pady = 5, sticky = 'w')
graphicsBlackStageTip = Hovertip(graphicsBlackStage, BLACK_STAGE_TIP, HOVER_DELAY)

# Enable/disable hide band.
hideBand = StringVar()
HIDE_BAND_TIP = "Show or hide the band."
graphicsHideBand = Checkbutton(wtdeOptionsGraphics, text = "  Hide Band", variable = hideBand, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsHideBand.grid(row = 4, column = 1, padx = 40, pady = 5, sticky = 'w')
graphicsHideBandTip = Hovertip(graphicsHideBand, HIDE_BAND_TIP, HOVER_DELAY)

# Enable/disable hide instruments.
hideInstruments = StringVar()
HIDE_INSTRUMENTS_TIP = "Show or hide the band's instruments."
graphicsHideInstruments = Checkbutton(wtdeOptionsGraphics, text = "  Hide Instruments", variable = hideInstruments, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
graphicsHideInstruments.grid(row = 5, column = 1, padx = 40, pady = 5, sticky = 'w')
graphicsHideInstrumentsTip = Hovertip(graphicsHideInstruments, HIDE_INSTRUMENTS_TIP, HOVER_DELAY)

# Select note style.
noteStyles = ["GHWT Notes (Default)", "GH3 Notes", "GH: WOR Notes", "Flat Notes"]
NOTE_STYLE_TIP = "Select the style of notes used on the highway."
graphicsNoteStyleLabel = Label(wtdeOptionsGraphics, text = "         Note (Gem) Style:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
graphicsNoteStyleLabel.grid(row = 6, column = 1, pady = 5, sticky = 'w')
graphicsNoteStyleLabelTip = Hovertip(graphicsNoteStyleLabel, NOTE_STYLE_TIP, HOVER_DELAY)

noteStyle = StringVar()
graphicsNoteStyle = OptionMenu(wtdeOptionsGraphics, noteStyle, *noteStyles)
graphicsNoteStyle.config(width = 20, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
graphicsNoteStyle.grid(row = 6, column = 2, pady = 5, sticky = 'w')
graphicsNoteStyleTip = Hovertip(graphicsNoteStyle, NOTE_STYLE_TIP, HOVER_DELAY)

# Select gem theme.
noteThemes = [
    "Normal Color (Default)", "Pink", "Stealth", "Eggs 'N Bacon", "Old Glory", "Solid Gold", "Platinum",
    "Diabolic", "Toxic Waste", "Black", "Pastel", "Dark", "Outline", "GH1 Prototype", "Pure Green",
    "Pure Red", "Pure Yellow", "Pure Blue", "Pure Orange", "Candy Cane", "Ghoulish"
]
NOTE_THEME_TIP = "Select the color scheme for the notes on the highway."
graphicsNoteThemeLabel = Label(wtdeOptionsGraphics, text = "         Note (Gem) Theme:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
graphicsNoteThemeLabel.grid(row = 7, column = 1, pady = 5, sticky = 'w')
graphicsNoteThemeLabelTip = Hovertip(graphicsNoteThemeLabel, NOTE_THEME_TIP, HOVER_DELAY)

noteTheme = StringVar()
graphicsNoteTheme = OptionMenu(wtdeOptionsGraphics, noteTheme, *noteThemes)
graphicsNoteTheme.config(width = 20, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
graphicsNoteTheme.grid(row = 7, column = 2, pady = 5, sticky = 'w')
graphicsNoteThemeTip = Hovertip(graphicsNoteTheme, NOTE_THEME_TIP, HOVER_DELAY)

# Select song intro style.
introStyles = [
    "Normal GHWT (Default)", "Guitar Hero III", "Guitar Hero III (Left)", "GH: Smash Hits", "GH: Metallica", "GH: Van Halen", "Guitar Hero 5", "Band Hero", "GH: Warriors of Rock", "Auto (Based on Setlist)"
]
INTRO_STYLE_TIP = "Select the style of intro shown on the top left corner of the\n" \
                  "screen at the beginning of songs."
graphicsIntroStyleLabel = Label(wtdeOptionsGraphics, text = "         Song Intro Style:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
graphicsIntroStyleLabel.grid(row = 8, column = 1, pady = 5, sticky = 'w')
graphicsIntroStyleLabelTip = Hovertip(graphicsIntroStyleLabel, INTRO_STYLE_TIP, HOVER_DELAY)

introStyle = StringVar()
graphicsIntroStyle = OptionMenu(wtdeOptionsGraphics, introStyle, *introStyles)
graphicsIntroStyle.config(width = 20, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
graphicsIntroStyle.grid(row = 8, column = 2, pady = 5, sticky = 'w')
graphicsIntroStyleTip = Hovertip(graphicsIntroStyle, INTRO_STYLE_TIP, HOVER_DELAY)

# ====================================================================== #
#                             BAND SETTINGS TAB                          #
# ====================================================================== #
# Band settings tab information.
TAB_INFO_BAND = "Band Settings: Modify your preferred characters and venue for your band.\nHover over any option to see what it does!"
bandInfoLabel = Label(wtdeOptionsBand, text = TAB_INFO_BAND, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
bandInfoLabel.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

# Preferred guitarist setting.
GUITAR_PREFERRED_TIP = "Set the ID of the character to force as the active guitarist. Leave this blank to force no character.\n\n" \
                       "This value depends on what you want for your characters.\n" \
                       "  •  For Rock Star Creator characters, use \"custom_character_x\", where x ranges from 0-19,\n" \
                       "     defining which custom character to use. For instance, \"custom_character_0\" will use\n" \
                       "     the first custom character made.\n" \
                       "  •  For built-in WTDE characters, refer to the \"ID_Characters.txt\" file in the Resources\n" \
                       "     folder in your GHWT installation folder.\n" \
                       "  •  If you're using modded characters, use the FOLDER name of the character!\n\n" \
                       "Remember! If someone else does NOT have a character that you have, they will be rendered as Axel\n" \
                       "Steel (GHWT) in-game as a placeholder. Modded characters in Online Career will crash the game."
bandPreferredGuitaristLabel = Label(wtdeOptionsBand, text = "Preferred Guitarist: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
bandPreferredGuitaristLabel.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'e')
bandPreferredGuitaristLabelTip = Hovertip(bandPreferredGuitaristLabel, GUITAR_PREFERRED_TIP, HOVER_DELAY)

bandPreferredGuitaristEntry = Entry(wtdeOptionsBand, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = 30)
bandPreferredGuitaristEntry.grid(row = 1, column = 1, pady = 5)
bandPreferredGuitaristEntryTip = Hovertip(bandPreferredGuitaristEntry, GUITAR_PREFERRED_TIP, HOVER_DELAY)

# Get the preferred guitarist already in the config.
bandPreferredGuitaristEntry.insert(0, config.get("Band", "PreferredGuitarist"))

# Preferred bassist setting.
BASS_PREFERRED_TIP = "Set the ID of the character to force as the active bassist. Leave this blank to force no character.\n\n" \
                     "This value depends on what you want for your characters.\n" \
                     "  •  For Rock Star Creator characters, use \"custom_character_x\", where x ranges from 0-19,\n" \
                     "     defining which custom character to use. For instance, \"custom_character_0\" will use\n" \
                     "     the first custom character made.\n" \
                     "  •  For built-in WTDE characters, refer to the \"ID_Characters.txt\" file in the Resources\n" \
                     "     folder in your GHWT installation folder.\n" \
                     "  •  If you're using modded characters, use the FOLDER name of the character!\n\n" \
                     "Remember! If someone else does NOT have a character that you have, they will be rendered as Axel\n" \
                     "Steel (GHWT) in-game as a placeholder. Modded characters in Online Career will crash the game."
bandPreferredBassistLabel = Label(wtdeOptionsBand, text = "Preferred Bassist: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
bandPreferredBassistLabel.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'e')
bandPreferredBassistLabelTip = Hovertip(bandPreferredBassistLabel, BASS_PREFERRED_TIP, HOVER_DELAY)

bandPreferredBassistEntry = Entry(wtdeOptionsBand, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = 30)
bandPreferredBassistEntry.grid(row = 2, column = 1, pady = 5)
bandPreferredBassistEntryTip = Hovertip(bandPreferredBassistEntry, BASS_PREFERRED_TIP, HOVER_DELAY)

# Get the preferred bassist already in the config.
bandPreferredBassistEntry.insert(0, config.get("Band", "PreferredBassist"))

# Preferred drummer setting.
DRUM_PREFERRED_TIP = "Set the ID of the character to force as the active drummer. Leave this blank to force no character.\n\n" \
                     "This value depends on what you want for your characters.\n" \
                     "  •  For Rock Star Creator characters, use \"custom_character_x\", where x ranges from 0-19,\n" \
                     "     defining which custom character to use. For instance, \"custom_character_0\" will use\n" \
                     "     the first custom character made.\n" \
                     "  •  For built-in WTDE characters, refer to the \"ID_Characters.txt\" file in the Resources\n" \
                     "     folder in your GHWT installation folder.\n" \
                     "  •  If you're using modded characters, use the FOLDER name of the character!\n\n" \
                     "Remember! If someone else does NOT have a character that you have, they will be rendered as Axel\n" \
                     "Steel (GHWT) in-game as a placeholder. Modded characters in Online Career will crash the game."
bandPreferredDrummerLabel = Label(wtdeOptionsBand, text = "Preferred Drummer: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
bandPreferredDrummerLabel.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'e')
bandPreferredDrummerLabelTip = Hovertip(bandPreferredDrummerLabel, DRUM_PREFERRED_TIP, HOVER_DELAY)

bandPreferredDrummerEntry = Entry(wtdeOptionsBand, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = 30)
bandPreferredDrummerEntry.grid(row = 3, column = 1, pady = 5)
bandPreferredDrummerEntryTip = Hovertip(bandPreferredDrummerEntry, DRUM_PREFERRED_TIP, HOVER_DELAY)

# Get the preferred drummer already in the config.
bandPreferredDrummerEntry.insert(0, config.get("Band", "PreferredDrummer"))

# Preferred vocalist setting.
VOX_PREFERRED_TIP = "Set the ID of the character to force as the active vocalist. Leave this blank to force no character.\n\n" \
                    "This value depends on what you want for your characters.\n" \
                    "  •  For Rock Star Creator characters, use \"custom_character_x\", where x ranges from 0-19,\n" \
                    "     defining which custom character to use. For instance, \"custom_character_0\" will use\n" \
                    "     the first custom character made.\n" \
                    "  •  For built-in WTDE characters, refer to the \"ID_Characters.txt\" file in the Resources\n" \
                    "     folder in your GHWT installation folder.\n" \
                    "  •  If you're using modded characters, use the FOLDER name of the character!\n\n" \
                    "Remember! If someone else does NOT have a character that you have, they will be rendered as Axel\n" \
                    "Steel (GHWT) in-game as a placeholder. Modded characters in Online Career will crash the game."
bandPreferredVocalistLabel = Label(wtdeOptionsBand, text = "Preferred Vocalist: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
bandPreferredVocalistLabel.grid(row = 4, column = 0, padx = 10, pady = 5, sticky = 'e')
bandPreferredVocalistLabelTip = Hovertip(bandPreferredVocalistLabel, VOX_PREFERRED_TIP, HOVER_DELAY)

bandPreferredVocalistEntry = Entry(wtdeOptionsBand, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = 30)
bandPreferredVocalistEntry.grid(row = 4, column = 1, pady = 5)
bandPreferredVocalistEntryTip = Hovertip(bandPreferredVocalistEntry, VOX_PREFERRED_TIP, HOVER_DELAY)

# Get the preferred vocalist already in the config.
bandPreferredVocalistEntry.insert(0, config.get("Band", "PreferredSinger"))

# Preferred venue settings.
venues = [
    "None",
    "Phi Psi Kappa",
    "Wilted Orchid",
    "Bone Church",
    "Pang Tang Bay",
    "Amoeba Records",
    "Tool",
    "Swamp Shack",
    "Rock Brigade",
    "Strutter's Farm",
    "House of Blues",
    "Ted's Tiki Hut",
    "Will Heilm's Keep",
    "Recording Studio",
    "AT&T Park",
    "Tesla's Coil",
    "Ozzfest",
    "Times Square",
    "Sunna's Chariot",
    "Other..."
]

preferredVenue = StringVar()

VENUE_PREFERRED_TIP = "Set the venue you want to always use while in-game. If a venue you wish to\n" \
                      "use isn't listed, select \"Other...\" to specify it."

bandPreferredStageLabel = Label(wtdeOptionsBand, text = "Preferred Venue: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
bandPreferredStageLabel.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'e')
bandPreferredStageLabelTip = Hovertip(bandPreferredStageLabel, VENUE_PREFERRED_TIP, HOVER_DELAY)

bandPreferredStageMenu = OptionMenu(wtdeOptionsBand, preferredVenue, *venues, command = lambda e: ask_venue_name(preferredVenue, e))
bandPreferredStageMenu.config(width = 28, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
bandPreferredStageMenu.grid(row = 5, column = 1, pady = 5)
bandPreferredStageMenu = Hovertip(bandPreferredStageMenu, VENUE_PREFERRED_TIP, HOVER_DELAY)

# Get the preferred venue already in the config.
preferredVenue.set(auto_get_venue(config.get("Band", "PreferredStage")))

# Preferred guitarist highway.
GUITAR_HWY_PREFERRED_TIP = "Set the preferred highway that the guitarist will use.\n\n" \
                           "For a list of highway IDs, see the \"ID_Highways.txt\" file in your Resources folder."
bandPreferredGuitaristHighwayLabel = Label(wtdeOptionsBand, text = "     Preferred Guitarist Highway:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
bandPreferredGuitaristHighwayLabel.grid(row = 1, column = 2, padx = 10, pady = 5, sticky = 'e')
bandPreferredGuitaristHighwayLabelTip = Hovertip(bandPreferredGuitaristHighwayLabel, GUITAR_HWY_PREFERRED_TIP, HOVER_DELAY)

bandPreferredGuitaristHighwayEntry = Entry(wtdeOptionsBand, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = 30)
bandPreferredGuitaristHighwayEntry.grid(row = 1, column = 3, pady = 5)
bandPreferredGuitaristHighwayTip = Hovertip(bandPreferredGuitaristHighwayEntry, GUITAR_HWY_PREFERRED_TIP, HOVER_DELAY)

# Get the preferred guitarist already in the config.
bandPreferredGuitaristHighwayEntry.insert(0, config.get("Band", "PreferredGuitaristHighway"))

# Preferred bassist highway.
BASS_HWY_PREFERRED_TIP = "Set the preferred highway that the bassist will use.\n\n" \
                         "For a list of highway IDs, see the \"ID_Highways.txt\" file in your Resources folder."
bandPreferredBassistHighwayLabel = Label(wtdeOptionsBand, text = "       Preferred Bassist Highway:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
bandPreferredBassistHighwayLabel.grid(row = 2, column = 2, padx = 10, pady = 5, sticky = 'e')
bandPreferredBassistHighwayLabelTip = Hovertip(bandPreferredBassistHighwayLabel, BASS_HWY_PREFERRED_TIP, HOVER_DELAY)

bandPreferredBassistHighwayEntry = Entry(wtdeOptionsBand, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = 30)
bandPreferredBassistHighwayEntry.grid(row = 2, column = 3, pady = 5)
bandPreferredBassistHighwayEntryTip = Hovertip(bandPreferredBassistHighwayEntry, BASS_HWY_PREFERRED_TIP, HOVER_DELAY)

# Get the preferred bassist already in the config.
bandPreferredBassistHighwayEntry.insert(0, config.get("Band", "PreferredBassistHighway"))

# Preferred drummer highway.
DRUM_HWY_PREFERRED_TIP = "Set the preferred highway that the drummer will use.\n\n" \
                         "For a list of highway IDs, see the \"ID_Highways.txt\" file in your Resources folder."
bandPreferredDrummerHighwayLabel = Label(wtdeOptionsBand, text = "       Preferred Drummer Highway:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
bandPreferredDrummerHighwayLabel.grid(row = 3, column = 2, padx = 10, pady = 5, sticky = 'e')
bandPreferredDrummerHighwayLabelTip = Hovertip(bandPreferredDrummerHighwayLabel, DRUM_HWY_PREFERRED_TIP, HOVER_DELAY)

bandPreferredDrummerHighwayEntry = Entry(wtdeOptionsBand, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = 30)
bandPreferredDrummerHighwayEntry.grid(row = 3, column = 3, pady = 5)
bandPreferredDrummerHighwayEntryTip = Hovertip(bandPreferredDrummerHighwayEntry, DRUM_HWY_PREFERRED_TIP, HOVER_DELAY)

# Get the preferred bassist already in the config.
bandPreferredDrummerHighwayEntry.insert(0, config.get("Band", "PreferredDrummerHighway"))

# Guitar and bass strum animations.
strumAnimOptions = ["GHWT (Default)", "Guitar Hero: Metallica"]

STRUM_ANIM_TIP = "Set the preferred guitar or bass strum animations for the characters."

guitarStrumAnim = StringVar()
bassStrumAnim = StringVar()

bandPreferredGuitarStrumAnimsLabel = Label(wtdeOptionsBand, text = "         Guitar Strum Animations:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
bandPreferredGuitarStrumAnimsLabel.grid(row = 6, column = 0, padx = 10, pady = 5, sticky = 'e')
bandPreferredGuitarStrumAnimsLabelTip = Hovertip(bandPreferredGuitarStrumAnimsLabel, STRUM_ANIM_TIP, HOVER_DELAY)

bandPreferredGuitarStrumAnims = OptionMenu(wtdeOptionsBand, guitarStrumAnim, *strumAnimOptions)
bandPreferredGuitarStrumAnims.config(width = 20, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
bandPreferredGuitarStrumAnims.grid(row = 6, column = 1, pady = 5)
bandPreferredGuitarStrumAnimsTip = Hovertip(bandPreferredGuitarStrumAnims, STRUM_ANIM_TIP, HOVER_DELAY)

bandPreferredBassStrumAnimsLabel = Label(wtdeOptionsBand, text = "           Bass Strum Animations:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right')
bandPreferredBassStrumAnimsLabel.grid(row = 7, column = 0, padx = 10, pady = 5, sticky = 'e')
bandPreferredBassStrumAnimsLabelTip = Hovertip(bandPreferredBassStrumAnimsLabel, STRUM_ANIM_TIP, HOVER_DELAY)

bandPreferredBassStrumAnims = OptionMenu(wtdeOptionsBand, bassStrumAnim, *strumAnimOptions)
bandPreferredBassStrumAnims.config(width = 20, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
bandPreferredBassStrumAnims.grid(row = 7, column = 1, pady = 5)
bandPreferredBassStrumAnimsTip = Hovertip(bandPreferredBassStrumAnims, STRUM_ANIM_TIP, HOVER_DELAY)

# ====================================================================== #
#                        AUTO LAUNCH SETTINGS TAB                        #
# ====================================================================== #
# Auto launch settings tab information.
TAB_INFO_AUTO_LAUNCH = "Auto Launch Settings: Set up the game to automatically load into a song of your choice.\nHover over any option to see what it does!"
autoInfoLabel = Label(wtdeOptionsAutoLaunch, text = TAB_INFO_AUTO_LAUNCH, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
autoInfoLabel.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

# Enable auto launch. If this is disabled, all other widgets will be disabled.
enableAutoLaunch = StringVar()
ENABLE_AUTO_LAUNCH_TIP = "Enable or disable auto launch.\n\n" \
                         "Using this, you can set up WTDE to automatically load into a song of your choosing.\n" \
                         "You can even set it up to autoplay, too!\n\n" \
                         "Be warned! This may erase your save data, so make sure to back it up first!"
autoEnableLaunch = Checkbutton(wtdeOptionsAutoLaunch, text = "  Enable Auto Launch", variable = enableAutoLaunch, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000", command = auto_launch_status)
autoEnableLaunch.grid(row = 1, column = 0, padx = 20, pady = 5, sticky = 'w')
autoEnableLaunchTip = Hovertip(autoEnableLaunch, ENABLE_AUTO_LAUNCH_TIP, HOVER_DELAY)

# Hide the HUD.
hideHUDAuto = StringVar()
HIDE_HUD_TIP = "When auto launch is enabled, do you want the interface hidden?"
autoHideHUD = Checkbutton(wtdeOptionsAutoLaunch, text = "  Hide HUD", variable = hideHUDAuto, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
autoHideHUD.grid(row = 2, column = 0, padx = 20, pady = 5, sticky = 'w')
autoHideHUDTip = Hovertip(autoHideHUD, HIDE_HUD_TIP, HOVER_DELAY)

# Number of players.
playerCount = StringVar()
PLAYERS_COUNT_TIP = "How many players do you want?"

autoPlayersLabel = Label(wtdeOptionsAutoLaunch, text = "Players: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoPlayersLabel.grid(row = 2, column = 1, pady = 5, sticky = 'e')
autoPlayersLabelTip = Hovertip(autoPlayersLabel, PLAYERS_COUNT_TIP, HOVER_DELAY)

playerNumbers = ["1", "2", "3", "4"]

autoPlayers = OptionMenu(wtdeOptionsAutoLaunch, playerCount, *playerNumbers, command = auto_update_players_event)
autoPlayers.config(width = 3, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
autoPlayers.grid(row = 2, column = 2, pady = 5, sticky = 'w')
autoPlayersTip = Hovertip(autoPlayers, PLAYERS_COUNT_TIP, HOVER_DELAY)

# Venue selection.
venueSelection = StringVar()

VENUE_SELECTION_TIP = "Select the venue you want to use."
autoVenueLabel = Label(wtdeOptionsAutoLaunch, text = "             Venue: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoVenueLabel.grid(row = 2, column = 3, pady = 5, sticky = 'e')
autoVenueLabelTip = Hovertip(autoVenueLabel, VENUE_SELECTION_TIP, HOVER_DELAY)

autoVenueSelect = OptionMenu(wtdeOptionsAutoLaunch, venueSelection, *venues, command = lambda e: ask_venue_name(venueSelection, e))
autoVenueSelect.config(width = 25, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
autoVenueSelect.grid(row = 2, column = 4, pady = 5, sticky = 'w')
autoVenueSelectTip = Hovertip(autoVenueSelect, VENUE_SELECTION_TIP, HOVER_DELAY)

# Song to boot into.
SONG_ID_TIP = "The checksum of the song to boot into."

autoSongLabel = Label(wtdeOptionsAutoLaunch, text = "              Song: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoSongLabel.grid(row = 2, column = 5, pady = 5, sticky = 'e')
autoSongLabelTip = Hovertip(autoSongLabel, SONG_ID_TIP, HOVER_DELAY)

autoSongEntry = Entry(wtdeOptionsAutoLaunch, bg = BUTTON_BG, fg = BUTTON_FG, font = FONT_INFO, width = 20, disabledbackground = BUTTON_BG)
autoSongEntry.grid(row = 2, column = 6, pady = 5, sticky = 'w')
autoSongEntryTip = Hovertip(autoSongEntry, SONG_ID_TIP, HOVER_DELAY)

# Show player settings section.
autoPlayerSectionLabel = Label(wtdeOptionsAutoLaunch, text = "Player Settings:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoPlayerSectionLabel.grid(row = 3, column = 0, columnspan = 999, pady = 20, sticky = 'w')

instruments = ["Lead Guitar - PART GUITAR", "Bass Guitar - PART BASS", "Drums - PART DRUMS", "Vocals - PART VOCALS"]
difficulties = ["Beginner", "Easy", "Medium", "Hard", "Expert"]

# Hover tool tips for the various settings for the players.
AUTO_INSTRUMENT_TIP = "Set the instrument to use for this player in auto launch."
AUTO_DIFFICULTY_TIP = "Set the difficulty this player will use in auto launch."
AUTO_USE_BOT_TIP = "Should this player have the bot enabled?"

# =============== PLAYER 1 SETTINGS =============== #
P1_SETTINGS_INFO = "Edit the settings for Player 1."
autoP1SectionLabel = Label(wtdeOptionsAutoLaunch, text = "      Player 1: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoP1SectionLabel.grid(row = 4, column = 0)
autoP1SectionLabelTip = Hovertip(autoP1SectionLabel, P1_SETTINGS_INFO, HOVER_DELAY)

autoP1InstrumentLabel = Label(wtdeOptionsAutoLaunch, text = "1P Instrument: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoP1InstrumentLabel.grid(row = 4, column = 1, sticky = 'e')
autoP1InstrumentLabelTip = Hovertip(autoP1InstrumentLabel, AUTO_INSTRUMENT_TIP, HOVER_DELAY)
 
autoInstrument1 = StringVar()
autoP1Instrument = OptionMenu(wtdeOptionsAutoLaunch, autoInstrument1, *instruments)
autoP1Instrument.config(width = 22, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
autoP1Instrument.grid(row = 4, column = 2, sticky = 'w', columnspan = 2)
autoP1InstrumentTip = Hovertip(autoP1Instrument, AUTO_INSTRUMENT_TIP, HOVER_DELAY)

# For manual placing when the grid won't cooperate.
LABEL_Y = 188
DROPDOWN_Y = 185

autoP1DifficultyLabel = Label(wtdeOptionsAutoLaunch, text = "1P Difficulty: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoP1DifficultyLabel.place(x = 535, y = 188)
autoP1DifficultyLabelTip = Hovertip(autoP1DifficultyLabel, AUTO_DIFFICULTY_TIP, HOVER_DELAY)

autoDifficulty1 = StringVar()
autoP1Difficulty = OptionMenu(wtdeOptionsAutoLaunch, autoDifficulty1, *difficulties)
autoP1Difficulty.config(width = 10, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
autoP1Difficulty.place(x = 627, y = 185)
autoP1DifficultyTip = Hovertip(autoP1Difficulty, AUTO_DIFFICULTY_TIP, HOVER_DELAY)

autoBot1 = StringVar()
autoP1UseBot = Checkbutton(wtdeOptionsAutoLaunch, text = "  Use Bot?", variable = autoBot1, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
autoP1UseBot.place(x = 762, y = 186)
autoP1UseBotTip = Hovertip(autoP1UseBot, AUTO_USE_BOT_TIP, HOVER_DELAY)

if (config.get("AutoLaunch", "Bot") == "1"): autoP1UseBot.select()
else: autoP1UseBot.deselect()

# =============== PLAYER 2 SETTINGS =============== #
P2_SETTINGS_INFO = "Edit the settings for Player 2."
autoP2SectionLabel = Label(wtdeOptionsAutoLaunch, text = "      Player 2: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoP2SectionLabel.grid(row = 5, column = 0, pady = 20)
autoP2SectionLabelTip = Hovertip(autoP2SectionLabel, P2_SETTINGS_INFO, HOVER_DELAY)

autoP2InstrumentLabel = Label(wtdeOptionsAutoLaunch, text = "2P Instrument: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoP2InstrumentLabel.grid(row = 5, column = 1, sticky = 'e')
autoP2InstrumentLabelTip = Hovertip(autoP2InstrumentLabel, AUTO_INSTRUMENT_TIP, HOVER_DELAY)
 
autoInstrument2 = StringVar()
autoP2Instrument = OptionMenu(wtdeOptionsAutoLaunch, autoInstrument2, *instruments)
autoP2Instrument.config(width = 22, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
autoP2Instrument.grid(row = 5, column = 2, sticky = 'w', columnspan = 2)
autoP2InstrumentTip = Hovertip(autoP2Instrument, AUTO_INSTRUMENT_TIP, HOVER_DELAY)

autoP2DifficultyLabel = Label(wtdeOptionsAutoLaunch, text = "2P Difficulty: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoP2DifficultyLabel.place(x = 535, y = 235)
autoP2DifficultyLabelTip = Hovertip(autoP2DifficultyLabel, AUTO_DIFFICULTY_TIP, HOVER_DELAY)

autoDifficulty2 = StringVar()
autoP2Difficulty = OptionMenu(wtdeOptionsAutoLaunch, autoDifficulty2, *difficulties)
autoP2Difficulty.config(width = 10, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
autoP2Difficulty.place(x = 627, y = 232)
autoP2DifficultyTip = Hovertip(autoP2Difficulty, AUTO_DIFFICULTY_TIP, HOVER_DELAY)

autoBot2 = StringVar()
autoP2UseBot = Checkbutton(wtdeOptionsAutoLaunch, text = "  Use Bot?", variable = autoBot2, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
autoP2UseBot.place(x = 762, y = 233)
autoP2UseBotTip = Hovertip(autoP2UseBot, AUTO_USE_BOT_TIP, HOVER_DELAY)

# =============== PLAYER 3 SETTINGS =============== #
P3_SETTINGS_INFO = "Edit the settings for Player 3."
autoP3SectionLabel = Label(wtdeOptionsAutoLaunch, text = "      Player 3: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoP3SectionLabel.grid(row = 6, column = 0)
autoP3SectionLabelTip = Hovertip(autoP3SectionLabel, P3_SETTINGS_INFO, HOVER_DELAY)

autoP3InstrumentLabel = Label(wtdeOptionsAutoLaunch, text = "3P Instrument: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoP3InstrumentLabel.grid(row = 6, column = 1, sticky = 'e')
autoP3InstrumentLabelTip = Hovertip(autoP3InstrumentLabel, AUTO_INSTRUMENT_TIP, HOVER_DELAY)
 
autoInstrument3 = StringVar()
autoP3Instrument = OptionMenu(wtdeOptionsAutoLaunch, autoInstrument3, *instruments)
autoP3Instrument.config(width = 22, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
autoP3Instrument.grid(row = 6, column = 2, sticky = 'w', columnspan = 2)
autoP3InstrumentTip = Hovertip(autoP3Instrument, AUTO_INSTRUMENT_TIP, HOVER_DELAY)

autoP3DifficultyLabel = Label(wtdeOptionsAutoLaunch, text = "3P Difficulty: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoP3DifficultyLabel.place(x = 535, y = 282)
autoP3DifficultyLabelTip = Hovertip(autoP3DifficultyLabel, AUTO_DIFFICULTY_TIP, HOVER_DELAY)

autoDifficulty3 = StringVar()
autoP3Difficulty = OptionMenu(wtdeOptionsAutoLaunch, autoDifficulty3, *difficulties)
autoP3Difficulty.config(width = 10, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
autoP3Difficulty.place(x = 627, y = 279)
autoP3DifficultyTip = Hovertip(autoP3Difficulty, AUTO_DIFFICULTY_TIP, HOVER_DELAY)

autoBot3 = StringVar()
autoP3UseBot = Checkbutton(wtdeOptionsAutoLaunch, text = "  Use Bot?", variable = autoBot3, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
autoP3UseBot.place(x = 762, y = 280)
autoP3UseBotTip = Hovertip(autoP3UseBot, AUTO_USE_BOT_TIP, HOVER_DELAY)

# =============== PLAYER 4 SETTINGS =============== #
P4_SETTINGS_INFO = "Edit the settings for Player 4."
autoP4SectionLabel = Label(wtdeOptionsAutoLaunch, text = "      Player 4: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoP4SectionLabel.grid(row = 7, column = 0, pady = 20)
autoP4SectionLabelTip = Hovertip(autoP4SectionLabel, P4_SETTINGS_INFO, HOVER_DELAY)

autoP4InstrumentLabel = Label(wtdeOptionsAutoLaunch, text = "4P Instrument: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoP4InstrumentLabel.grid(row = 7, column = 1, sticky = 'e')
autoP4InstrumentLabelTip = Hovertip(autoP3InstrumentLabel, AUTO_INSTRUMENT_TIP, HOVER_DELAY)
 
autoInstrument4 = StringVar()
autoP4Instrument = OptionMenu(wtdeOptionsAutoLaunch, autoInstrument4, *instruments)
autoP4Instrument.config(width = 22, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
autoP4Instrument.grid(row = 7, column = 2, sticky = 'w', columnspan = 2)
autoP4InstrumentTip = Hovertip(autoP4Instrument, AUTO_INSTRUMENT_TIP, HOVER_DELAY)

autoP4DifficultyLabel = Label(wtdeOptionsAutoLaunch, text = "4P Difficulty: ", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'right', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoP4DifficultyLabel.place(x = 535, y = 329)
autoP4DifficultyLabelTip = Hovertip(autoP4DifficultyLabel, AUTO_DIFFICULTY_TIP, HOVER_DELAY)

autoDifficulty4 = StringVar()
autoP4Difficulty = OptionMenu(wtdeOptionsAutoLaunch, autoDifficulty4, *difficulties)
autoP4Difficulty.config(width = 10, bg = BUTTON_BG, fg = BUTTON_FG, activebackground = BUTTON_ACTIVE_BG, activeforeground = BUTTON_ACTIVE_FG, font = FONT_INFO_DROPDOWN, highlightbackground = BUTTON_ACTIVE_BG, highlightcolor = BUTTON_ACTIVE_FG, justify = 'left')
autoP4Difficulty.place(x = 627, y = 326)
autoP4DifficultyTip = Hovertip(autoP4Difficulty, AUTO_DIFFICULTY_TIP, HOVER_DELAY)

autoBot4 = StringVar()
autoP4UseBot = Checkbutton(wtdeOptionsAutoLaunch, text = "  Use Bot?", variable = autoBot4, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
autoP4UseBot.place(x = 762, y = 327)
autoP4UseBotTip = Hovertip(autoP4UseBot, AUTO_USE_BOT_TIP, HOVER_DELAY)

# =============== ADVANCED SETTINGS =============== #
autoAdvancedSectionLabel = Label(wtdeOptionsAutoLaunch, text = "Advanced Settings:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR)
autoAdvancedSectionLabel.grid(row = 8, column = 0, columnspan = 999, pady = 20, sticky = 'w')

# Use raw loading.
rawLoad = StringVar()
RAW_LOAD_TIP = "Turn ON or OFF raw loading of the venue.\n\n" \
               "In its essence, this will load the zone PAK, but will not try and set it up\n" \
               "as a song or load into a game mode. Good for creating custom venues and\n" \
               "testing if the SCN and TEX files are working properly!"
autoRawLoad = Checkbutton(wtdeOptionsAutoLaunch, text = "  Use Raw PAK Loading", variable = rawLoad, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
autoRawLoad.grid(row = 9, column = 0, padx = 20, sticky = 'w')
autoRawLoadTip = Hovertip(autoRawLoad, RAW_LOAD_TIP, HOVER_DELAY)

# Show the song time.
songTime = StringVar()
SONG_TIME_TIP = "Show the song time on-screen. The time is shown in seconds."
autoSongTime = Checkbutton(wtdeOptionsAutoLaunch, text = "  Show Time", variable = songTime, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
autoSongTime.grid(row = 9, column = 1, sticky = 'w')
autoSongTimeTip = Hovertip(autoSongTime, SONG_TIME_TIP, HOVER_DELAY)

# Update the status of all widgets.
auto_launch_status()

# ====================================================================== #
#                            DEBUG SETTINGS TAB                          #
# ====================================================================== #
# Debug settings tab information.
TAB_INFO_DEBUG = "Debug Settings: Edit debug specific settings.\nHover over any option to see what it does!"
debugInfoLabel = Label(wtdeOptionsDebug, text = TAB_INFO_DEBUG, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
debugInfoLabel.grid(row = 0, column = 0, columnspan = 999)

# Fix note limit.
fixNoteLimit = StringVar()
FIX_NOTE_LIMIT_TIP = "Fix the note limit from the default 4,096 note limit.\n\n" \
                     "Note that not everyone has this enabled, and if you have songs imported with\n" \
                     "over 4,096 notes, other people will have to enable this for your song to\n" \
                     "work correctly in their installation of WTDE."
debugFixNoteLimit = Checkbutton(wtdeOptionsDebug, text = "  Fix Note Limit", variable = fixNoteLimit, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
debugFixNoteLimit.grid(row = 1, column = 0, padx = 20, pady = 5, sticky = 'w')
debugFixNoteLimitTip = Hovertip(debugFixNoteLimit, FIX_NOTE_LIMIT_TIP, HOVER_DELAY)

# Fix memory handler.
fixMemoryHandler = StringVar()
FIX_MEMORY_HANDLER_TIP = "Fixes the memory handler. This extends memory limits, shows errors if compact pools\n" \
                         "run out of bounds, etc.\n\n" \
                         "Warning: It is HEAVILY encouraged that you DON'T disable this."
debugFixMemoryHandler = Checkbutton(wtdeOptionsDebug, text = "  Fix Memory Handler", variable = fixMemoryHandler, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000", command = warn_memory_deselect)
debugFixMemoryHandler.grid(row = 2, column = 0, padx = 20, pady = 5, sticky = 'w')
debugFixMemoryHandlerTip = Hovertip(debugFixMemoryHandler, FIX_MEMORY_HANDLER_TIP, HOVER_DELAY)

# Open debug console.
loggerConsole = StringVar()
DEBUG_CONSOLE_TIP = "Opens the debug console in the background while WTDE is open."
debugOpenConsole = Checkbutton(wtdeOptionsDebug, text = "  Open Debug Console", variable = loggerConsole, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
debugOpenConsole.grid(row = 3, column = 0, padx = 20, pady = 5, sticky = 'w')
debugOpenConsoleTip = Hovertip(debugOpenConsole, DEBUG_CONSOLE_TIP, HOVER_DELAY)

# Write debug.txt file.
writeFile = StringVar()
WRITE_DEBUG_LOG_TIP = "Write a file to the disk that holds the debug log written by WTDE during execution.\n\n" \
                      "This shouldn't be disabled, as it helps to debug crashes and\n" \
                      "other various issues."
debugWriteDebugLog = Checkbutton(wtdeOptionsDebug, text = "  Write Debug Log", variable = writeFile, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
debugWriteDebugLog.grid(row = 4, column = 0, padx = 20, pady = 5, sticky = 'w')
debugWriteDebugLogTip = Hovertip(debugWriteDebugLog, WRITE_DEBUG_LOG_TIP, HOVER_DELAY)

# Skip song logging.
disableSongLogging = StringVar()
SKIP_SONG_LOGGING_TIP = "Turn ON or OFF debug logging while playing songs.\n\n" \
                        "While songs are running in-game, this will disable any sort of logging to the debug log,\n" \
                        "which may improve performance slightly. However, while OFF in the event of crashes\n" \
                        "that occur mid-song, this won't exhibit a helpful debug log."
debugSkipSongLogging = Checkbutton(wtdeOptionsDebug, text = "  Skip Song Logging", variable = disableSongLogging, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
debugSkipSongLogging.grid(row = 5, column = 0, padx = 20, pady = 5, sticky = 'w')
debugSkipSongLoggingTip = Hovertip(debugSkipSongLogging, SKIP_SONG_LOGGING_TIP, HOVER_DELAY)

# Debug DLC sync.
debugDLCSync = StringVar()
DLC_SYNC_DEBUG_TIP = "Enable or disable song syncing debugging.\n\n" \
                     "While playing online, a sync is performed to ensure all players have\n" \
                     "identical copies of the same songs. If this is ON, this will write\n" \
                     "all song syncing information to the debug log."
debugDLCSyncOption = Checkbutton(wtdeOptionsDebug, text = "  DLC Sync Debugging", variable = debugDLCSync, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
debugDLCSyncOption.grid(row = 6, column = 0, padx = 20, pady = 5, sticky = 'w')
debugDLCSyncTip = Hovertip(debugDLCSyncOption, DLC_SYNC_DEBUG_TIP, HOVER_DELAY)

# Fix FMOD Sound Bank objects.
fixFSBObjects = StringVar()
FIX_FSB_OBJECTS_TIP = "Enable or disable fixing FMOD Sound Bank objects."

fixFSBObjectsOption = Checkbutton(wtdeOptionsDebug, text = "  Fix FMOD Sound Bank Objects", variable = fixFSBObjects, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left', activebackground = BG_COLOR, activeforeground = FG_COLOR, selectcolor = "#000000")
fixFSBObjectsOption.grid(row = 7, column = 0, padx = 20, pady = 5, sticky = 'w')
fixFSBObjectsOptionTip = Hovertip(fixFSBObjectsOption, FIX_FSB_OBJECTS_TIP, HOVER_DELAY)

# ====================================================================== #
#                               CREDITS TAB                              #
# ====================================================================== #
# Logo image of WTDE.
creditsLogoLabel = Label(wtdeOptionsCredits, image = WTDE_LOGO, bg = BG_COLOR, fg = FG_COLOR, justify = 'center')
creditsLogoLabel.pack(fill = 'x')

# Credits text.
CREDITS_TAB_TEXT_1 = f"GH World Tour: Definitive Edition Launcher++ by IMF24 - Version {VERSION}\n\n" \
                      "GHWT: DE Developed by Fretworks, EST. 2021\n\n" \
                      "🧪 ✨ WTDE Developers ✨ 🧪"
creditsText1Label = Label(wtdeOptionsCredits, text = CREDITS_TAB_TEXT_1, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'center')
creditsText1Label.pack(fill = 'x')

creditsTableLabel = Label(wtdeOptionsCredits, image = CREDITS_TABLE_IMAGE, bg = BG_COLOR, fg = FG_COLOR, justify = 'center')
creditsTableLabel.pack(fill = 'x')

CREDITS_TAB_TEXT_2 = "A special thanks to our development testers and of course, all of you, the players, modders, content creators, and everything in between!\n\n" \
                     "Making your Guitar Hero World Tour experience better, one update at a time!\n\n" \
                     "GHWT: DE and Fretworks are not associated with Activision, Neversoft, or RedOctane in any way, shape, or form.\n" \
                     "GHWT: DE is and always will be a non-profit fan-made project."
creditsText2Label = Label(wtdeOptionsCredits, text = CREDITS_TAB_TEXT_2, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'center')
creditsText2Label.pack(fill = 'x')

# ====================================================================== #
#                              ADD THE TABS                              #
# ====================================================================== #
# Add the tabs into the notebook.
wtdeOptionsRoot.add(wtdeOptionsNews, text = " GHWT: DE News", image = NEWS_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsGeneral, text = " General Settings", image = GENERAL_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsInput, text = " Input Settings", image = INPUT_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsGraphics, text = " Graphics Settings", image = GRAPHICS_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsBand, text = " Band Settings", image = BAND_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsAutoLaunch, text = " Auto Launch Settings", image = AUTO_LAUNCH_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsDebug, text = " Debug Settings", image = DEBUG_ICON, compound = 'left')
wtdeOptionsRoot.add(wtdeOptionsCredits, text = " Credits", image = CREDITS_ICON, compound = 'left')

# Load config data.
wtde_load_config()

# Credits text on the bottom of the screen.
CREDITS_TEXT = "Made by IMF24, WTDE by Fretworks, Updater by Zedek the Plague Doctor \u2122"
widgetCanvas.create_text(18, 772, text = CREDITS_TEXT, fill = FG_COLOR, font = FONT_INFO, justify = 'left', anchor = 'sw')

# Credits text on the bottom of the screen.
VERSION_TEXT = f"Version {VERSION} || WTDE Latest Version: {wtde_latest_version()}"
widgetCanvas.create_text(1280, 772, text = VERSION_TEXT, fill = FG_COLOR, font = FONT_INFO, justify = 'right', anchor = 'se')

# Enter main loop.
root.mainloop()