# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#     W T D E     L A U N C H E R + +     F U N C T I O N S
#
#       All functions used by the GHWT: DE Launcher++.
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
""" All functions used by the GHWT: DE Launcher++. """
# Import required modules.
from tkinter import *
from tkinter import ttk as TTK, messagebox as MSG, filedialog as FD
from PIL import Image, ImageTk
from tktooltip import ToolTip
from launcher_constants import *
from launcher_exceptions import *
from cmd_colors import *
import os as OS
import sys as SYS
import stat as STAT
import winshell as WS
import shutil as SHUT
import csv as CSV
from win32api import GetSystemMetrics
from win32com.client import Dispatch
from datetime import datetime
import pyaudio as PA
import requests as REQ
from bs4 import BeautifulSoup
import configparser as CF
import zipfile as ZIP
import py7zr as P7Z
import time as TIME
import struct
# from pyunpack import Archive
# import patoolib as PAT
# import unrar as UNR
# import hashlib as HASH
# import subprocess as SUB
# import math as MATH
# from ctypes import c_uint16

# Initialize ConfigParser. We'll use this without strict mode to help reduce crashes.
# By setting optionxform to str, we can use the original upper camel casing used in GHWTDE.ini.
config = CF.ConfigParser(comment_prefixes = ("#", ";"), allow_no_value = True, strict = False)
config.optionxform = str

# Set up SYS.stdout to be written to a text file. All print() statements will go to the debug log now!
if (not OS.path.exists(f"{WS.my_documents()}\\My Games\\Guitar Hero World Tour Definitive Edition\\Logs")):
    myGamesFolder = f"{WS.my_documents()}\\My Games"
    ghwtdeFolder = f"\\Guitar Hero World Tour Definitive Edition"
    logsFolder = "\\Logs"

    if (not OS.path.exists(myGamesFolder)): OS.mkdir(myGamesFolder)

    if (not OS.path.exists(OS.path.join(myGamesFolder, ghwtdeFolder))): OS.mkdir(OS.path.join(myGamesFolder, ghwtdeFolder))

    if (not OS.path.exists(OS.path.join(myGamesFolder, ghwtdeFolder, logsFolder))): OS.mkdir(OS.path.join(myGamesFolder, ghwtdeFolder, logsFolder))

SYS.stdout = open(f"{WS.my_documents()}\\My Games\\Guitar Hero World Tour Definitive Edition\\Logs\\debug_launcher.txt", 'w+')

print("-------------------------------------------\n" \
     f"GHWT: DE Launcher++ Debug Log - V{VERSION}\n" \
     f"Date of Execution: {datetime.now()}\n" \
      "-------------------------------------------")

# ==================================================
# WE'RE NOT USING THIS, IGNORE IT!
# ==================================================
# Number of command line arguments.
# print(len(SYS.argv))

# Process command line arguments!
# args = SYS.argv

# Run in debug mode or not.
# global allowDebugMode
# allowDebugMode = False
# """ Allows for control of debugging the launcher further. Does close to nothing right now! """

# if ("-H") in (args) or ("-h") in (args) or ("--help") in (args):
#     HELP_INFO_MSG = f"{YELLOW}-~-~-~-~-~-~- WTDE Launcher++ Command Line Functionality -~-~-~-~-~-~-{WHITE}\n" \
#                      "List of arguments:\n" \
#                      "   -H, -h, --help              Prints this message.\n" \
#                      "   -I, -i, --ini               Change an INI option, giving the section, option, and value.\n"
    
#     print(HELP_INFO_MSG)

#     SYS.exit(1)

# if ("-I") in (args) or ("-i") in (args) or ("--ini") in (args):
#     if (len(args) <= 2):
#         print(f"{RED}Please input an INI section, option, and value to change.{WHITE}")
#         print(f"{YELLOW}Usage: [-i/-I/--ini] <section> <option> <value>{WHITE}")
#         SYS.exit(1)

#     elif (len(args) <= 3):
#         print(f"{RED}Please input an option and value to change it to.{WHITE}")
#         print(f"{YELLOW}Usage: [-i/-I/--ini] <section> <option> <value>{WHITE}")
#         SYS.exit(1)

#     elif (len(args) <= 4):
#         print(f"{RED}Please input a value to change the given option to.{WHITE}")
#         print(f"{YELLOW}Usage: [-i/-I/--ini] <section> <option> <value>{WHITE}")
#         SYS.exit(1)

#     elif (len(args) > 5):
#         print(f"{RED}Too many arguments!{WHITE}")
#         print(f"{YELLOW}Usage: [-i/-I/--ini] <section> <option> <value>{WHITE}")
#         SYS.exit(1)

#     else:
#         print(f"{YELLOW}Attempting to change INI option {args[3]} to value {args[4]} in section {args[2]}...{WHITE}")

#         try:
#             OS.chdir(f"{WS.my_documents()}\\My Games\\Guitar Hero World Tour Definitive Edition")

#             config.read("GHWTDE.ini")

#             config.set(args[2], args[3], args[4])

#             with (open("GHWTDE.ini", 'w')) as cnf: config.write(cnf)

#             print(f"{GREEN}INI value {args[3]} in section {args[2]} changed to {args[4]} successfully!{WHITE}")

#             SYS.exit(1)

#         except Exception as exc:
#             print(f"{RED}Error changing INI value: {exc}{WHITE}")
#             SYS.exit(1)

# if ("-d") in (args) or ("-D") in (args) or ("--debug") or (args):
#     allowDebugMode = True
#     header1 = BLUE
#     header2 = LIGHT_BLUE
# else:
#     allowDebugMode = False
#     header1 = RED
#     header2 = LIGHT_RED

# # FORCE DEBUG MODE OFF, THIS IS A PUBLIC BUILD
# allowDebugMode = False

# print(f"{header1}-----------------------------------------------{WHITE}")
# print(f"{header2}WTDE LAUNCHER++ DEBUG CONSOLE{WHITE}")
# if (allowDebugMode): print(f"{header2}DEBUG MODE ENABLED{WHITE}")
# print(f"{header1}-----------------------------------------------{WHITE}")

# ==================================================

# The debug log. Used by the ++ launcher for debugging purposes.
global debugLog
debugLog: list[str] = []
""" The debug log. Used by the ++ launcher for debugging purposes. """

# ===========================================================================================================
# Window Functions
# ===========================================================================================================
# Intro splash screen.
def intro_splash() -> None:
    """ Intro splash image seen when the launcher starts up. """
    splashRoot = Tk()
    splashRoot.geometry(f"763x350+{int(get_screen_resolution()[0] // 3.25)}+{int(get_screen_resolution()[1] // 3.5)}")
    splashRoot.resizable(False, False)
    splashRoot.overrideredirect(True)

    introSplashImage = ImageTk.PhotoImage(Image.open(resource_path("res/splash.png")))

    splashCanvas = Canvas(splashRoot, bg = BG_COLOR, relief = 'flat', bd = 0)
    splashCanvas.pack(fill = 'both', expand = 1)

    splashCanvas.create_image(0, 0, image = introSplashImage, anchor = 'nw')
    splashCanvas.create_text(610, 320, text = f"Version {VERSION}\nMade by IMF24, GHWT: DE by Fretworks", font = ('Segoe UI', 12), fill = '#FFFFFF', justify = 'right')

    splashRoot.after(3000, splashRoot.destroy)
    splashRoot.mainloop()

# ===========================================================================================================
# Debug Functions
# ===========================================================================================================
# Save debug log.
def save_debug(use: bool = True, filename: str = "debug_launcher.txt") -> str:
    """ Save the debug log for the program's activity inside a log file. Saved as a `.txt` file. """
    if (use):
        reset_working_directory()
        
        OS.chdir(wtde_find_config())

        if (not OS.path.exists("Logs")): OS.mkdir("Logs")

        OS.chdir("Logs")
  
        try:
            print("Debug logging enabled; writing debug log file.")

            with (open(filename, 'w')) as SYS.stdout:
                topMessage = "-------------------------------------------\n" \
                            f"GHWT: DE Launcher++ Debug Log - V{VERSION}\n" \
                            f"Date of Execution: {datetime.now()}\n" \
                            "-------------------------------------------\n"
                
                SYS.stdout.write(topMessage)

                print("Writing terminal as debug log...")

        except Exception as excep:
            MSG.showerror("Launcher Debug Save Error", f"An error occurred saving the launcher debug log.\n\n{excep}")

    else:
        print("Debug logging disabled; skipping writing file.")

# Append a value to the debug log.
def debug_add_entry(entry: str, indent: int = 0) -> None:
    """
    Add a new entry to the debug log. The entry is appended into the global `debugLog` string list.
    
    Arguments
    ---------
    - `entry`: `str` >> The message to add into the log.
    - `indent`: `int = 0` >> The amount of indentation to apply to the entry.

    Returns
    -------
    Doesn't return anything.
    """
    if (indent > 0): entry = ("    " * indent) + entry

    debugLog.append(entry)

# Write the terminal text to an output text file.
# def write_terminal(file: str = "debug_launcher.txt") -> None:
#     with (open(file, 'w')) as SYS.stdout:
#         print("Writing terminal as debug log...")

# ===========================================================================================================
# Directory and Resource Functions
# ===========================================================================================================
# Reset working directory.
def reset_working_directory() -> None:
    """ Resets our current working directory to the default when execution began. """
    OS.chdir(OWD)
    print(f"Reset our working directory to {OWD}")

# Verify if ALL required directories for operation exist.
# RUN THESE CHECKS BEFORE WE DO ANYTHING ELSE!
def dirs_verify_ok() -> None:
    """ Verify if ALL required directories for operation exist. RUN THESE CHECKS BEFORE WE DO ANYTHING ELSE! """
    print("!! -- ALL DIRECTORIES ARE BEING VERIFIED, BE PATIENT")

    # OK, first check: Documents folder.
    wtdeDocumentsDir = f"{WS.my_documents()}\\My Games\\Guitar Hero World Tour Definitive Edition"

    if (not OS.path.exists(wtdeDocumentsDir)):
        if (not OS.path.exists(f"{WS.my_documents()}\\My Games")): OS.mkdir(f"{WS.my_documents()}\\My Games")

        if (not OS.path.exists(f"{WS.my_documents()}\\My Games\\Guitar Hero World Tour Definitive Edition")): OS.mkdir(f"{WS.my_documents()}\\My Games\\Guitar Hero World Tour Definitive Edition")

        if (not OS.path.exists(f"{wtdeDocumentsDir}\\Logs")): OS.mkdir(f"{wtdeDocumentsDir}\\Logs")

    # Next check: AspyrConfig.
    aspyrConfigDir = f"{OS.getenv('LOCALAPPDATA')}\\Aspyr\\Guitar Hero World Tour"

    if (not OS.path.exists(aspyrConfigDir)):  
        # We're ASSUMING the computer already has the AppData/Local folder.
        # Any sane computer should have this already. If not, something
        # is very wrong with the user's computer.
        if (not OS.path.exists(f"{OS.getenv('LOCALAPPDATA')}\\Aspyr")): OS.mkdir(f"{OS.getenv('LOCALAPPDATA')}\\Aspyr")

        if (not OS.path.exists(aspyrConfigDir)): OS.mkdir(aspyrConfigDir)

    # Now copy required files.
    if (not OS.path.exists(f"{wtdeDocumentsDir}\\GHWTDE.ini")): wtde_verify_config()

    if (not OS.path.exists(f"{aspyrConfigDir}\\AspyrConfig.xml")): SHUT.copy(resource_path('res/AspyrConfig.xml'), aspyrConfigDir)

    print("!! -- ALL DIRECTORIES SHOULD NOW EXIST IF THEY DIDN'T BEFORE")

# Relative path function.
def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a given resource. Used for compatibility with Python scripts compiled to EXEs using PyInstaller whose files have been embedded into the EXE itself.

    Tries at first to use `sys._MEIPASS`, which is used for relative paths. In the event it doesn't work, it will use the absolute path, and join it with the relative path given by the function's arguments.
    
    Arguments
    ---------
    `relative_path` : `str` >> The relative path to convert to an actual path.

    Returns
    -------
    `str` >> The actual path to the given resource.

    Example of Use
    --------------
    The actual output value will vary from device to device. In the below example, `~\` refers to `\"C:\\Users\\Your Username\"`.

    >>> print(resource_path(\"res/icon.ico\"))
    \"~\\Desktop\\GHWT DE Mod Development IDE\\res/icon.ico\"
    """
    # Try and use the actual path, if it exists.
    try:
        base_path = SYS._MEIPASS

    # In the event it doesn't, use the absolute path.
    except Exception:
        base_path = OS.path.abspath(".")

    # Join the paths together!
    print(f"path is {OS.path.join(base_path, relative_path)}")
    return OS.path.join(base_path, relative_path)

# Verify if Updater.ini is present in the original working directory.
def verify_updater_config() -> None:
    """ Makes sure that Updater.ini is present in the current working directory. """
    reset_working_directory()

    if (not OS.path.exists("Updater.ini")):
        print(f"{RED}CRITICAL: NO UPDATER.INI; THIS IS BAD\n{WHITE}Creating new Updater.ini...")
        debug_add_entry("[!!! - No Updater/Directory Config] CRITICAL: NO UPDATER.INI; THIS IS BAD -- Creating new Updater.ini...")

        config.write(open("Updater.ini", 'w'))

        config.read("Updater.ini")

        if (not OS.path.exists("GHWT.exe")):
            print(f"{YELLOW}Warning: GHWT.exe wasn't found here, requesting user to locate it{WHITE}")
            MSG.showerror("GHWT Path Not Defined", "This folder did not contain GHWT.exe!\n\nNavigate to the folder that contains GHWT.exe.")

            wtdeDir = FD.askdirectory()

            while (not OS.path.exists(f"{wtdeDir}/GHWT.exe")):
                if (wtdeDir == ""): SYS.exit(0)
                MSG.showerror("GHWT.exe Not Detected", "This folder does not contain GHWT.exe.\n\nNavigate to the folder that contains GHWT.exe.")
                wtdeDir = FD.askdirectory()
            else:
                MSG.showinfo("GHWT.exe Detected", "GHWT.exe was successfully found!")

        else: wtdeDir = OS.getcwd()

        with (open("Updater.ini", 'w')) as cnf: cnf.write(f"[Updater]\nGameDirectory = {wtdeDir}")

    # Is the game installed in Program Files?
    config.read('Updater.ini')
    
    try:
        config.get('Updater', 'GameDirectory').replace("/", "\\").index("C:\\Program Files")
        print(f"{RED}CRITICAL: Game found in Program Files folder, THINGS WILL BREAK{WHITE}")
        MSG.showwarning("Permissions Warning", "The launcher found GHWT installed in one of the Program Files directories. Due to this, certain aspects of the launcher may not function as intended. To resolve this, either run the launcher as an administrator or move the GHWT install to a different location.")
    
    # Good, we aren't in Program Files...
    except ValueError as valerr:
        print(f"This is good! {valerr}")
        pass

    reset_working_directory()     
verify_updater_config()

# ===========================================================================================================
# Graphics Functions
# ===========================================================================================================
# Get native monitor resolution.
def get_screen_resolution() -> list[int]:
    """
    Returns the native resolution of the user's PRIMARY monitor.
    
    Returns
    -------
    `list[int]` >> A list of 2 numbers holding the width and height of the primary monitor, respectively.

    Example of Use
    --------------
    >>> print(get_screen_resolution())
    [1920, 1080]
    """
    return [GetSystemMetrics(0), GetSystemMetrics(1)]

# ===========================================================================================================
# Input Functions
# ===========================================================================================================
# Get list of microphones.
def mic_name_get_list() -> list[str]:
    """ Returns a list of all microphone names. """
    # Initialize PyAudio.
    audio = PA.PyAudio()

    # Get the device count.
    info = audio.get_host_api_info_by_index(0)
    deviceCount = info.get('deviceCount')

    # List of microphones. None is provided by default.
    micList = ["None"]

    # Find all connected and supported microphones.
    for (i) in (range(0, deviceCount)):
        if ((audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0):
            micList.append(audio.get_device_info_by_host_api_device_index(0, i).get('name'))

    # We don't need the Microsoft Sound Mapper, so just get rid of it.
    msmName = "Microsoft Sound Mapper - Input"
    if (micList.count(msmName) > 0):
        for (item) in (micList):
            if (item == msmName): micList.remove(msmName)

    print(f"List of supported mic devices: {micList}")
    return micList

# Set mic calibration.
def mic_set_calibration(audio: int | str, video: int | str, audioEntry: Entry, videoEntry: Entry) -> None:
    """ Set the user's microphone calibration to the given values. """
    # Update the values.
    audioEntry.delete(0, 'end')
    audioEntry.insert(0, str(audio))

    videoEntry.delete(0, 'end')
    videoEntry.insert(0, str(video))

# ===========================================================================================================
# Debug Settings Functions
# ===========================================================================================================
# Warn the user about disabling FixMemoryHandler.
def warn_memory_deselect(var: StringVar) -> None:
    """ Warn the user about disabling FixMemoryHandler. """
    if (var.get() == "0"):
        if (MSG.askyesno("Are You Sure?", "Do you really wish to disable the memory handler fix? Disabling this may be dangerous and is not recommended.")):
            var.set("0")
        else: var.set("1")

# Warn the user about disabling CheckForUpdates.
def warn_auto_update_deselect(var: StringVar) -> None:
    """ Warn the user about disabling CheckForUpdates. """
    if (var.get() == "0"):
        if (MSG.askyesno("Are You Sure?", "Do you really wish to disable the auto update checker? This may cause your mod version fall out of date much more quickly and is not recommended.")):
            var.set("0")
        else: var.set("1")

# ===========================================================================================================
# Network Functions
# ===========================================================================================================
# Can we connect to a webpage?
def is_connected(url: str, tout: int | float = 10) -> bool:  
    """ Attempt to ping a URL, and if successful, returns `True`. Returns `False` if an exception is thrown. """
    # Try to ping the webside and get its contents.
    # If we can do that, return True.
    try:
        REQ.get(url, timeout = tout)
        print(f"{GREEN}We have a connection, nice!{WHITE}")
        return True

    # Catch the error, if found. Return False.
    except (REQ.ConnectionError, REQ.Timeout) as exception:
        print(str(exception))
        debug_add_entry(f"[Network Connection] ERROR IN NETWORK CONNECTION: {exception}", 2)
        print(f"{RED}NO NETWORK CONNECTION, MAN{WHITE}")
        return False

# Retrieve the latest version of WTDE on the GitHub page.
def wtde_get_news() -> str:
    """ Retrieves the latest news for WTDE on the GitHub page with the HTML for the GHWT: DE News tab. """
    newsPage = "https://raw.githubusercontent.com/IMF24/WTDE-Launcher/main/res/ghwt_de_news.html"
    if (is_connected(newsPage)):
        debug_add_entry("[News Receiver] HTML document successfully retrieved", 1)
        print("We got the news from GitHub!")
        return REQ.get(newsPage).text
    
    else:
        print("Trying again...")

        try:
            REQ.get(newsPage).text

        except Exception as exception:
            print(f"{RED}Yeah, we must not have an internet connection, then{WHITE}")

            debug_add_entry(f"[News Receiver] Failed to retrieve news; Maybe a network error? {exception}", 1)

            return f"<p style=\"font-size: 11px;\">Hm... We couldn't establish a connection to the internet.<br>Is the Wi-Fi and/or router turned on?<br>  <br>Error Information:<br>{exception}</p>"

# ===========================================================================================================
# WTDE Config File Functions
# ===========================================================================================================
# Find the main WTDE configuration file.
def wtde_find_config() -> str:
    """ Tries to locate the main config file for WTDE (GHWTDE.ini). The path is returned if found; an empty string is returned if not. """
    wtdeConfigDir = f"{WS.my_documents()}/My Games/Guitar Hero World Tour Definitive Edition"

    # Attempt the default location.
    normalDirOutput = OS.path.expanduser(wtdeConfigDir)

    if (OS.path.exists(normalDirOutput)):
        fixedPath = OS.path.expanduser(wtdeConfigDir).replace("/", "\\")
        return fixedPath

    # If neither worked, it's a bad path, so just return nothing.
    else:
        # Alert the user that their GHWTDE.ini can't be found.
        print(f"{RED}CRITICAL: No GHWTDE.ini found, THIS IS VERY BAD; let's just make the file{WHITE}")
        # MSG.showerror("GHWTDE.ini Not Auto Detected", "We couldn't automatically detect GHWTDE.ini. The program will now attempt to create a fallback INI file.")

        # Let's make that folder!
        OS.chdir(WS.my_documents())

        print(WS.my_documents())

        if (not OS.path.exists("My Games")): OS.makedirs("My Games")

        OS.chdir("My Games")

        if (not OS.path.exists("Guitar Hero World Tour Definitive Edition")): OS.makedirs("Guitar Hero World Tour Definitive Edition")

        OS.chdir("Guitar Hero World Tour Definitive Edition")

        # Also verify Logs folder!
        if (not OS.path.exists("Logs")): OS.makedirs("Logs")

        reset_working_directory()

        # Now return the path!
        wtdeConfigDir = f"{WS.my_documents()}/My Games/Guitar Hero World Tour Definitive Edition"

        normalDirOutput = OS.path.expanduser(wtdeConfigDir)

        fixedPath = OS.path.expanduser(wtdeConfigDir).replace("/", "\\")
        return fixedPath

# Verify GHWTDE.ini and AspyrConfig.xml.
def wtde_verify_config() -> None:
    """ Runs a sanity check on our GHWTDE.ini and AspyrConfig.xml files, looks for missing fields that are used by the launcher, and adds them if they're absent. """
    print(f"{YELLOW}Doing sanity check on GHWTDE.ini...{WHITE}")
    
    # Close any config files we were previously reading.
    config.clear()

    # Find our config file. Try and head into this folder if we can.
    OS.chdir(wtde_find_config())

    # If no GHWTDE.ini file exists, let's make one!
    if (not OS.path.exists('GHWTDE.ini')):
        config.clear()
        with (open('GHWTDE.ini', 'w')) as cnf: config.write(cnf)

    # Read our config file.
    config.read("GHWTDE.ini")

    # Now we'll go through every section and verify its options.
    debug_add_entry("[Verify Config] Running sanity check on GHWTDE.ini...", 1)

    # ==================================
    # General Settings
    # Option Section: 'Config'
    # ==================================
    # List of all names under the Config section.
    generalOptionNames = ["RichPresence", "AllowHolidays", "Language", "UseCareerOption", "UseQuickplayOption", "UseHeadToHeadOption",
                          "UseOnlineOption", "UseMusicStudioOption", "UseCAROption", "UseOptionsOption", "UseQuitOption",
                          "SongSpecificIntros", "Holiday", "EnableCamPulse", "StatusHandler", "DefaultQPODifficulty"]
    
    # Verify "Config" section.
    if (not config.has_section("Config")): config["Config"] = {}

    for (name) in (generalOptionNames):
        if (not config.has_option("Config", name)):
            print(f"{RED}Warning: Option {name} not found in [Config], adding it...{WHITE}")

            debug_add_entry(f"[Verify Config] Warning: Option {name} not found in [Config], adding it...", 2)

            match (name):
                case "Language":                valueToSet = "en"
                case "AttractDelay":            valueToSet = "110"
                case "SplashScreenDelay":       valueToSet = "0"
                case "Holiday":                 valueToSet = ""
                case "StatusHandler":           valueToSet = "0"
                case "DefaultQPODifficulty":    valueToSet = "expert"
                case _:                         valueToSet = "1"
            
            config.set("Config", name, valueToSet)
        else: continue

    # ==================================
    # Graphics Settings
    # Option Section: 'Graphics'
    # ==================================
    # List of all names under the 'Graphics' section.
    graphicsOptionNames = ["WindowedMode", "DisableVSync", "HelperPillTheme", "HUDTheme", "DisableDOF", "HitSparks", "Borderless", "DisableBloom",
                           "TapTrailTheme", "SongIntroStyle", "SustainFX", "HitFlameTheme", "GemTheme", "GemColors", "FPSLimit",
                           "ColorFilters", "LoadingTheme", "HavokFPS", "SoloMarkers", "HitFlames", "RenderParticles", "HighwayOpacity", "HighwayVignetteOpacity",
                           "RenderGeoms", "RenderInstances", "RenderFog", "DrawProjectors", "BlackStage", "HideBand", "HideInstruments", "Render2D",
                           "RenderScreenFX", "UseNativeRes", "DefaultTODProfile", "ApplyBandName", "ApplyBandLogo", "DOFQuality", "DOFBlur", "FlareStyle",
                           "HandFlames", "SpecialStarPowerFX"]

    # Verify "Graphics" section.
    if (not config.has_section("Graphics")): config["Graphics"] = {}

    for (name) in (graphicsOptionNames):
        if (not config.has_option("Graphics", name)):
            print(f"{RED}Warning: Option {name} not found in [Graphics], adding it...{WHITE}")

            debug_add_entry(f"[Verify Config] Warning: Option {name} not found in [Graphics], adding it...", 2)

            match (name):
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
                case "BlackStage":                  valueToSet = "0"
                case "HideBand":                    valueToSet = "0"
                case "HideInstruments":             valueToSet = "0"
                case "UseNativeRes":                valueToSet = "0"
                case "DefaultTODProfile":           valueToSet = "ghwt"
                case "DOFQuality":                  valueToSet = "2"
                case "DOFBlur":                     valueToSet = "6.0"
                case "FlareStyle":                  valueToSet = "wtde"
                case "HighwayOpacity":              valueToSet = "100"
                case "HighwayVignetteOpacity":      valueToSet = "0"
                case "HandFlames":                  valueToSet = "0"
                case "SpecialStarPowerFX":          valueToSet = "0"
                case _:                             valueToSet = "1"
            
            config.set("Graphics", name, valueToSet)
        else: continue

    # ==================================
    # Band Settings
    # Option Section: 'Band'
    # ==================================
    # List of all names under the 'Band' section.
    bandOptionNames = ["PreferredGuitarist", "PreferredBassist", "PreferredDrummer", "PreferredSinger", "PreferredStage",
                       "PreferredGuitaristHighway", "PreferredBassistHighway", "PreferredDrummerHighway",
                       "GuitarStrumAnim", "BassStrumAnim"]
    
    # Verify "Band" section.
    if (not config.has_section("Band")): config["Band"] = {}

    for (name) in (bandOptionNames):
        if (not config.has_option("Band", name)):
            print(f"{RED}Warning: Option {name} not found in [Band], adding it...{WHITE}")

            debug_add_entry(f"[Verify Config] Warning: Option {name} not found in [Band], adding it...", 2)

            match (name):
                case "GuitarStrumAnim":     valueToSet = "none"
                case "BassStrumAnim":       valueToSet = "none"
                case _:                     valueToSet = ""
            
            config.set("Band", name, valueToSet)
        else: continue

    # ==================================
    # Audio Settings
    # Option Section: 'Audio'
    # ==================================
    # List of all names under the 'Audio' section.
    audioOptionNames = ["MicDevice", "VocalAdjustment", "WhammyPitchShift", "MuteStreams"]

    # Verify "Audio" section.
    if (not config.has_section("Audio")): config["Audio"] = {}
    
    for (name) in (audioOptionNames):
        if (not config.has_option("Audio", name)):
            print(f"{RED}Warning: Option {name} not found in [Audio], adding it...{WHITE}")

            debug_add_entry(f"[Verify Config] Warning: Option {name} not found in [Audio], adding it...", 2)

            match (name):
                case "MicDevice":           valueToSet = ""
                case "VocalAdjustment":     valueToSet = "0"
                case _:                     valueToSet = "1"
            
            config.set("Audio", name, valueToSet)
        else: continue

    # ==================================
    # Logger Settings
    # Option Section: 'Logger'
    # ==================================
    # List of all names under the 'Logger' section.
    loggerOptionNames = ["Console", "WriteFile", "PrintStructures", "ScriptTracing", "DisableSongLogging", "ExitOnAssert",
                         "DebugDLCSync", "ShowWarnings", "PrintLoadedAssets", "PrintCreateFile", "CreateFileErrorLevel"]

    # Verify "Logger" section.
    if (not config.has_section("Logger")): config["Logger"] = {}

    for (name) in (loggerOptionNames):
        if (not config.has_option("Logger", name)):
            print(f"{RED}Warning: Option {name} not found in [Logger], adding it...{WHITE}")

            debug_add_entry(f"[Verify Config] Warning: Option {name} not found in [Logger], adding it...", 2)

            match (name):
                case "WriteFile":               valueToSet = "1"
                case "ExitOnAssert":            valueToSet = "1"
                case "DebugDLCSync":            valueToSet = "1"
                case "CreateFileErrorLevel":    valueToSet = "1"
                case _:                         valueToSet = "0"
            
            config.set("Logger", name, valueToSet)
        else: continue

    # ==================================
    # Auto Launch Settings
    # Option Section: 'AutoLaunch'
    # ==================================
    # List of all names under the 'AutoLaunch' section.
    autoLaunchOptionNames = ["Enabled", "HideHUD", "SongTime", "RawLoad", "EncoreMode", "Players", "Venue", "Song",
                             "Difficulty", "Difficulty2", "Difficulty3", "Difficulty4",
                             "Part", "Part2", "Part3", "Part4", "Bot", "Bot2", "Bot3", "Bot4"]
    
    # Verify "AutoLaunch" section.
    if (not config.has_section("AutoLaunch")): config["AutoLaunch"] = {}

    for (name) in (autoLaunchOptionNames):
        if (not config.has_option("AutoLaunch", name)):
            print(f"{RED}Warning: Option {name} not found in [AutoLaunch], adding it...{WHITE}")

            debug_add_entry(f"[Verify Config] Warning: Option {name} not found in [AutoLaunch], adding it...", 2)

            match (name):
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
                case "EncoreMode":          valueToSet = "none"
                case _:                     valueToSet = "0"
            
            config.set("AutoLaunch", name, valueToSet)
        else: continue

    # ==================================
    # Debug Settings
    # Option Section: 'Debug'
    # ==================================
    # List of all names under the 'Debug' section.
    debugOptionNames = ["MicAttempts", "BindWarningShown", "FixMemoryHandler", "FixFSBObjects",
                        "FixNoteLimit", "DisableInputHack", "ExtraOptimizedSaves", "DebugSaves",
                        "FixFastTextures", "QuickDebug", "CASNoticeShown", "DisableInitialMovies"]
    
    # Verify "Debug" section.
    if (not config.has_section("Debug")): config["Debug"] = {}

    for (name) in (debugOptionNames):
        if (not config.has_option("Debug", name)):
            print(f"{RED}Warning: Option {name} not found in [Debug], adding it...{WHITE}")

            debug_add_entry(f"[Verify Config] Warning: Option {name} not found in [Debug], adding it...", 2)

            match (name):
                case "FixMemoryHandler":    valueToSet = "1"
                case "FixFastTextures":     valueToSet = "1"
                case _:                     valueToSet = "0"
            
            config.set("Debug", name, valueToSet)
        else: continue

    # ==================================
    # Launcher Settings
    # Option Section: 'Launcher'
    # ==================================
    # List of all names under the 'Launcher' section.
    launcherOptionNames = ["AllowWindowResize", "ScanDuplicateSongs", "PopulateModManager", "CheckForUpdates", "BGColor", "FGColor", "TextFont", "ExitOnSave"]
    
    # Verify "Launcher" section.
    if (not config.has_section("Launcher")): config["Launcher"] = {}

    for (name) in (launcherOptionNames):
        if (not config.has_option("Launcher", name)):
            print(f"{RED}Warning: Option {name} not found in [Launcher], adding it...{WHITE}")

            debug_add_entry(f"[Verify Config] Warning: Option {name} not found in [Launcher], adding it...", 2)

            match (name):
                case "ScanDuplicateSongs":      valueToSet = "1"
                case "PopulateModManager":      valueToSet = "1"
                case "CheckForUpdates":         valueToSet = "1"
                case "BGColor":                 valueToSet = "000000"
                case "FGColor":                 valueToSet = "FFFFFF"
                case "TextFont":                valueToSet = "Segoe UI"
                case "ExitOnSave":              valueToSet = "1"
                case _:                         valueToSet = "0"
            
            config.set("Launcher", name, valueToSet)
        else: continue

    # After the sanity check, write this data back in.
    debug_add_entry("[Verify Config] Writing backup data...", 2)
    print("Writing backup data...")

    with (open("GHWTDE.ini", 'w')) as cnf: config.write(cnf)

    debug_add_entry("[Verify Config] Sanity check complete", 1)
    print(f"{GREEN}INI sanity check complete{WHITE}")

    # Reset working directory.
    reset_working_directory()
wtde_verify_config()

# ===========================================================================================================
# AspyrConfig Functions
# ===========================================================================================================
# Get the location of AspyrConfig.xml.
def aspyr_get_config() -> str:
    """ Access and return the path to the AspyrConfig.xml file in the user's Local AppData folder. """
    # Access our AspyrConfig.xml file.
    localAppData = OS.getenv('LOCALAPPDATA')
    aspyrConfigXMLDir = OS.path.join(localAppData, "Aspyr\\Guitar Hero World Tour")
    print(f"AspyrConfig located in: {aspyrConfigXMLDir}")
    return aspyrConfigXMLDir

# Verify AspyrConfig.xml.
def aspyr_verify_config() -> None:
    """ Makes sure that AspyrConfig.xml is existent in the folder it's supposed to be in. """
    # Does the AspyrConfig not exist?
    if (not OS.path.exists(OS.path.join(aspyr_get_config(), "AspyrConfig.xml"))):
        # Then we need to copy the file and make sure it's there!
        reset_working_directory()

        if (not OS.path.exists(OS.path.join(OS.getenv("LOCALAPPDATA"), "Aspyr"))): OS.mkdir(OS.path.join(OS.getenv("LOCALAPPDATA"), "Aspyr"))

        if (not OS.path.exists(OS.path.join(OS.getenv("LOCALAPPDATA"), "Aspyr\\Guitar Hero World Tour"))):
            OS.mkdir(OS.path.join(OS.getenv("LOCALAPPDATA"), "Aspyr\\Guitar Hero World Tour"))

        # Copy the file out of our res folder to the destination.
        SHUT.copyfile(resource_path('res/AspyrConfig.xml'), OS.path.join(aspyr_get_config(), "AspyrConfig.xml"))
aspyr_verify_config()

# Get any 's id=' string from the user's AspyrConfig.xml file.
def aspyr_get_string(key: str, fallback: bool = True, fallbackValue: int | float | str = "") -> str:
    """
    Tries to find and return a string from the given `s id=` key in the user's AspyrConfig.xml file. Fallback measures are employed if enabled.
    
    Arguments
    ---------
    - key: `str` >> The key to search for in the `s id=` tags.
    - fallback: `bool` >> `True` by default; Should a fallback be used? Highly advised!
    - fallbackValue: `str` >> The value to be used for the fallback. An empty string `""` is default.

    Returns
    -------
    `str`
    - Returns the value of the provided key.

    Example of Use
    --------------
    Assuming a default AspyrConfig...
    >>> print(aspyr_get_string("Video.Width"))
    "720"
    """
    # Open up our AspyrConfig file and read its content as a sequence of bytes.
    OS.chdir(aspyr_get_config())
    with (open("AspyrConfig.xml", 'rb')) as xml: aspyrConfigDataXML = xml.read()

    # Run BS4 on the XML data.
    aspyrConfigDataBS = BeautifulSoup(aspyrConfigDataXML, 'xml', from_encoding = 'utf-8')

    # Try and locate the data.
    # Tag validity checker. If this was a valid tag, then we can just return it.
    wasValid = False

    # Test the key on our AspyrConfig.
    keyTest = aspyrConfigDataBS.find('s', {"id": key})

    # Was it a valid key?
    if (keyTest):
        # If so, we know it's good, so just return its decoded contents!
        wasValid = True

        reset_working_directory()

        print(f"{GREEN}Located tag string in tag {key}: {keyTest.decode_contents()}{WHITE}")
        return keyTest.decode_contents()

    # If not, add it as a backup tag.
    if (not wasValid) and (fallback):
        print(f"{RED}CRITICAL: No string for s id tag {key} found, writing fallback tag with value {fallbackValue}{WHITE}")

        # Get the original parent `r` tag data.
        originalData = aspyrConfigDataBS.r

        # Add a new tag and populate its 'string' tag with the given argument value.
        newTag = aspyrConfigDataBS.new_tag("s", id=key)
        newTag.string = str(fallbackValue)
        originalData.append(newTag)

        # Write this data back in.
        with (open("AspyrConfig.xml", 'w', encoding = "utf-8")) as xml: xml.write(str(aspyrConfigDataBS))

        # Open it AGAIN.
        with (open("AspyrConfig.xml", 'rb')) as xml: aspyrConfigDataXML = xml.read()

        # Run BS4 on the XML data AGAIN.
        aspyrConfigDataBS = BeautifulSoup(aspyrConfigDataXML, 'xml', from_encoding = 'utf-8')
    
        # NOW return the required value!
        keyTest = aspyrConfigDataBS.find('s', {"id": key})

        reset_working_directory()

        print(f"{GREEN}Located tag string in tag {key}: {keyTest.decode_contents()}{WHITE}")
        return keyTest.decode_contents()
    
    # If there was no desire for a fallback, and the tag wasn't valid, just return an empty string.
    else:
        print(f"{RED}CRITICAL: No string for s id tag {key} found, no fallback designated, aborting...{WHITE}")
        reset_working_directory()
        return ""

# Key bind list.
def aspyr_get_keybinds(csvFile: str = resource_path("res/AspyrKeyBinds.csv")) -> list[list[str]]:
    """ Returns a list of keybinds, using a CSV file. """
    reset_working_directory()

    print("Reading CSV for AspyrKeyBinds.csv, converting to lists")

    with (open(csvFile, 'r', newline = "", encoding = 'utf-8')) as file:
        csvReader = CSV.reader(file, delimiter = ',')

        keyBindList = []

        for (row) in (csvReader): keyBindList.append(row)

        del keyBindList[0]

        return keyBindList

# Key bind string encoder.
def aspyr_key_encode(widgets: list[Entry] | list[TTK.Entry], inputs: list[str]) -> str:
    """
    Takes a list of Entry widgets and a list of binding keywords (as strings), and constructs an input mapping string to be written into AspyrConfig.
    \n
    There is a very specific way that you need to use this function, as it is NOT plug-and-play with its argument structure:
    - The proper way of using this function is to give it a series of Entry widgets and their respective binding keywords. The string will be constructed in the order
    provided in BOTH the `widgets` and `inputs` arguments.
    - When the string is constructed, it will be returned. It is NOT written to AspyrConfig. You will have to write it yourself.
    
    Arguments
    ---------
    - `widgets`: `list[Entry] | list[ttk.Entry]` >> A list of Tkinter or TTK Entry widgets to construct the string with.
    - `inputs`: `list[str]` >> Related to the above, this is a list of strings that are the actual bindings for the retrieved inputs in the previous argument.

    Returns
    -------
    `str` >> Returns an input mapping string for use in AspyrConfig.
    
    Exceptions
    ----------
    - `AspyrLenMismatchError`: Raised when the number of widgets and the number of inputs are not identical.
    """
    # If the number of widgets and inputs don't match, raise AspyrLenMismatchError.
    if (len(widgets) != len(inputs)): raise AspyrLenMismatchError("The number of inputs and widgets do not match.")

    # Values in each Entry widget.
    keybindsList = []

    # For each Entry widget, get its contents, and add a new list into the list.
    for (widget) in (widgets): keybindsList.append(list(dict.fromkeys(widget.get().split(" "))))

    print(f"list of controls to encode: {keybindsList}")

    # Now we need to turn each of these keyboard keys into their numerical IDs.
    # Read our CSV file with all the key binding IDs.
    keyIDList = aspyr_get_keybinds()

    # String with the inputs encoded.
    inputsEncoded = ""

    # Find a match with the key IDs and populate the final string.
    for (bind) in (inputs):
        inputsEncoded += bind.upper() + " "

        # Find a match with the key IDs and populate the final string.
        for (keyPair) in (keyIDList):
            # We'll use the first list to track our current input.
            for (id) in (keybindsList[0]):
                # Track duplicate inputs. We'll use these to avoid bloated AspyrConfig files.
                duplicatedInput = False
    
                # Have we found a match with the given binding name?
                if (keyPair[1] == id):

                    # Log that ID. We'll need to check it against our currently existing inputs for duplicates, if any.
                    idToCheck = keyPair[0]
                    
                    # Has this input been added already?
                    if (len(inputsEncoded.split(" ")) > 0):
                        # Loop through every logged ID number and see if we find any matches.
                        for (inputID) in (inputsEncoded.split(" ")[inputsEncoded.index(bind.upper()) + 1:]):
                            # Make sure we're reading inputs.
                            # If this is a non-numerical string, we're at another input, and we'll stop reading there.
                            if (not inputID.isnumeric()): break
                            
                            # If we found a duplicate input, don't add it!
                            if (inputID == idToCheck):
                                duplicatedInput = True
                                break
                                
                    # Move onto the next input if this input was a duplicate.
                    if (duplicatedInput): continue
                    
                    # Build the string further.
                    inputsEncoded += idToCheck + " "

        # Delete the first list, we no longer need it.
        del keybindsList[0]

    # Return the constructed mapping string.
    print(f"final encoded string: {inputsEncoded}")
    return inputsEncoded

# Key bind string decoder.
def aspyr_key_decode(string: str, inputKey: str) -> str:
    """
    Take an input mapping string and decode it, along with what inputs should be given out of the string, and returns a string with decoded inputs.
    
    Arguments
    ---------
    - `string`: `str` >> The encoded mapping string.
    - `inputKey`: `str` >> The input to return all the inputs for.

    Returns
    -------
    `str` >> Returns a string containing the decoded inputs.

    Example of Use
    --------------
    Assuming a default AspyrConfig...
    >>> print(aspyr_key_decode(aspyr_get_string("Keyboard_Guitar"), "GREEN"))
    "V Enter"
    """
    # Split the string at the whitespace.
    inputList = string.split(" ")
    print(f"Input list to decode: {inputList}")

    # Start index. We'll use this to keep track of where we are in the list and where we need to start.
    startIndex = 0

    # Find the input we desired.
    for (x, key) in (enumerate(inputList)):
        if (inputKey == key):
            startIndex = x + 1
            break

    # Using that index, let's find all inputs and we'll decode them.
    keyIDs = []
    for (key) in (inputList[startIndex:]):
        if (key.isdigit()): keyIDs.append(key)
        else: break

    # Now we need to turn each of these numerical IDs into their actual keyboard keys.
    # Read our CSV file with all the key binding IDs.
    keyIDList = aspyr_get_keybinds()

    # String with the inputs decoded.
    inputsDecoded = ""

    # Find a match with the key IDs and populate the final string.
    for (keyPair) in (keyIDList):
        for (id) in (keyIDs):
            if (keyPair[0] == id): inputsDecoded += keyPair[1] + " "
    
    # Remove all leading and trailing whitespace, then return the string.
    print(f"Input string decoded: {inputsDecoded.strip()}")
    return inputsDecoded.strip()

# Editor for the friends list.
def aspyr_edit_friends() -> None:
    """ Allows the user to update their friend list in the launcher. """
    # Save the list of friends to AspyrConfig.xml.
    def xml_save_friends() -> None:
        """ Save the list of friends to AspyrConfig.xml. """
        OS.chdir(aspyr_get_config())

        # Open our AspyrConfig.xml file.
        with (open('AspyrConfig.xml', 'rb')) as xml: aspyrConfigDataXML = xml.read()

        # Run BS4 on the XML data.
        aspyrConfigDataBS = BeautifulSoup(aspyrConfigDataXML, 'xml', from_encoding = 'utf-8')
        friendListData = aspyrConfigDataBS.find('s', {"id": "FriendsList"})

        # Build the friend list string!
        finalString = ""
        friendListNames = friendListText.get(1.0, END).split("\n")
        for (line) in (friendListNames):
            if (line == friendListNames[0]):
                finalString += line
                continue

            elif (not line): continue

            else: finalString += f",{line}"

        # DEBUG: Show our final string.
        # print(finalString)

        friendListData.string = finalString

        with (open("AspyrConfig.xml", 'w', encoding = "utf-8")) as xml: xml.write(str(aspyrConfigDataBS))

        reset_working_directory()

    # Just in case, reset working directory.
    reset_working_directory()

    # Set up the editor dialog.
    friendListEditRoot = Tk()
    friendListEditRoot.config(bg = '#FFFFFF')
    friendListEditRoot.iconbitmap(resource_path('res/icons/friends.ico'))
    friendListEditRoot.title("Edit Friend List")
    friendListEditRoot.geometry("360x520")
    friendListEditRoot.resizable(False, False)
    friendListEditRoot.focus_force()

    # Update window styling.
    TTK.Style(friendListEditRoot).configure('TButton', background = '#FFFFFF')

    # Header label.
    fleHeaderLabel = Label(friendListEditRoot, text = "Edit Friend List: Modify the list of friends you have online.", bg = '#FFFFFF', font = FONT_INFO_HEADER, justify = 'left', anchor = 'nw')
    fleHeaderLabel.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

    friendListHeader = Label(friendListEditRoot, text = "Friend List:", bg = '#FFFFFF', font = FONT_INFO_HEADER, justify = 'left', anchor = 'nw')
    friendListHeader.grid(row = 1, column = 0, columnspan = 999, pady = 5, sticky = 'w')

    friendEditArea = Frame(friendListEditRoot, bg = '#FFFFFF')
    friendEditArea.grid(row = 2, column = 0, columnspan = 999, sticky = 'w')

    friendListText = Text(friendEditArea, font = FONT_INFO_CODE, wrap = 'char', width = 42, height = 20, relief = 'sunken', bd = 2, undo = True)
    friendListText.pack(side = 'left', fill = 'both', expand = 1)

    friendListTextScrollbar = TTK.Scrollbar(friendEditArea, orient = 'vertical', command = friendListText.yview)
    friendListTextScrollbar.pack(side = 'right', fill = 'y')

    friendListText.config(yscrollcommand = friendListTextScrollbar.set)

    FRIEND_LIST_EDIT_TIP = "This is a list of your added friends for online play.\n\n" \
                           "Add the username of the friend you want to add on a new line. Blank lines will be ignored."

    ToolTip(friendListText, msg = FRIEND_LIST_EDIT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
    ToolTip(friendListTextScrollbar, msg = FRIEND_LIST_EDIT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    for (line) in (aspyr_get_string('FriendsList', True, "").split(',')): friendListText.insert(END, line + "\n")

    friendListSave = TTK.Button(friendListEditRoot, text = "Update Friends List", width = 40, padding = 10, command = xml_save_friends)
    friendListSave.grid(row = 3, column = 0, padx = 42, pady = 5, sticky = 'w')
    ToolTip(friendListSave, msg = "Save the list of friends to AspyrConfig.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    friendListClose = TTK.Button(friendListEditRoot, text = "Cancel", width = 10, command = friendListEditRoot.destroy)
    friendListClose.grid(row = 4, column = 0, padx = 285, pady = 16)

    # Enter main loop.
    friendListEditRoot.mainloop()

# ===========================================================================================================
# WTDE Specific Functions
# ===========================================================================================================
# Back up the user's save file.
def wtde_backup_save(filename: str = f"GHWTDE_{datetime.now()}.sav".replace(':', '_')) -> None:
    """ Finds the user's save file, duplicates it with the file name `filename`. """
    # Find the user's save file. Lucky for us, it's in the same directory as GHWTDE.ini!
    OS.chdir(wtde_find_config())

    # Copy the user's save file.
    if (not OS.path.exists("Save Backups")): OS.makedirs("Save Backups")
    try:
        SHUT.copyfile("GHWTDE.sav", f"Save Backups/{filename}")

        print(f"Save data backed up as file {filename}")

        BACK_UP_SUCCESS_INFO = "Your save has been backed up! It can be found in the Save Backups folder where your config file is located.\n\n" \
                              f"The file has been saved as: {filename}"

        MSG.showinfo("Save Backed Up", BACK_UP_SUCCESS_INFO)

        debug_add_entry(f"[Save Backup] Backed up save data: {filename}")

    # If we ran into an error, log it and abort execution.
    except Exception as excep:
        debug_add_entry(f"[Save Backup] Error in save backup: {excep}")

    # Reset working directory.
    reset_working_directory()

# Manage save files dialog.
def wtde_manage_saves() -> None:
    """ Opens a dialog box for the user to manage their save files for GHWT: DE. """
    # Back up save.
    def back_up_save() -> None:
        wtde_backup_save()
        manageSavesRoot.focus_force()
        save_get_backups()

    # Replace save data file.
    def replace_save() -> bool:
        """ Asks the user for a save file, and replaces their GHWTDE.sav file with it. """
        # Ask for a file. Default to the "Save Backups" directory if it exists.
        origin = f"{wtde_find_config()}\\Save Backups"
        if (not OS.path.exists(origin)): origin = wtde_find_config()

        saveFile = FD.askopenfilename(title = "Select Save File to Replace With", initialdir = origin, filetypes = (("Save Files", "*.sav"), ("All Files", "*.*")))

        saveFile = saveFile.replace("/", "\\")

        # Run some sanity checks...
        if (not saveFile):
            manageSavesRoot.focus_force()
            return False
        
        if (saveFile == f"{wtde_find_config()}\\GHWTDE.sav"):
            MSG.showerror("Can't Replace Data", "You cannot replace your own save data with your own save data!")
            manageSavesRoot.focus_force()
            return False
        
        # Delete the old GHWTDE.sav file. Then replace it with the new one!
        if (MSG.askyesno("Replace Save?", "Are you sure you want to replace your save file with the one you chose? This cannot be undone!")):
            if (OS.path.exists(f"{wtde_find_config()}\\GHWTDE.sav")):
                try:
                    OS.remove(f"{wtde_find_config()}\\GHWTDE.sav")
                
                    SHUT.copyfile(saveFile, f"{wtde_find_config()}\\GHWTDE.sav")

                    # DEBUG: Tell us that copying was successful
                    print("Copy was successful")

                    return True
                
                except Exception as excep:
                    MSG.showerror("Error Replacing Data", f"An error occurred while trying to replace the save data:\n\n{excep}")
                    return False

    # Get save data backups.
    def save_get_backups() -> None:
        """ To the main Listbox, populates it with all save backups. """
        manageSavesBackupsList.delete(0, END)

        if (not OS.path.exists(f"{wtde_find_config()}\\Save Backups")): return

        OS.chdir(f"{wtde_find_config()}\\Save Backups")

        for (file) in (OS.listdir(".")): manageSavesBackupsList.insert(END, file)
        
        manageSavesBackupsHeader.config(text = f"Save Backups ({len(OS.listdir('.'))}):")

        print(f"Found a total of {len(OS.listdir('.'))} save backups: {OS.listdir('.')}")
        
        reset_working_directory()

    # Replace with selected backup.
    def replace_with_backup() -> bool:
        """ Replace the user's main save file with the selected backup in the listbox. """
        # Selected file.
        selectedSave = ""
        for (x) in (manageSavesBackupsList.curselection()): selectedSave = manageSavesBackupsList.get(x)

        if (not selectedSave):
            MSG.showerror("No Backup Specified", "You didn't specify a backup file!")
            manageSavesRoot.focus_force()
            return False

        # Make sure the user wants to do this.
        if (MSG.askyesno("Replace Save?", "Are you sure you want to replace your save data with the selected backup? This cannot be undone!")):
            # Change to our save file folder.
            OS.chdir(f"{wtde_find_config()}")

            # Delete the old GHWTDE.sav file. Then replace it with the new one!
            if (OS.path.exists(f"{wtde_find_config()}\\GHWTDE.sav")):
                try:
                    OS.remove(f"{wtde_find_config()}\\GHWTDE.sav")
                
                    SHUT.copyfile(f"{wtde_find_config()}\\Save Backups\\{selectedSave}", f"{wtde_find_config()}\\GHWTDE.sav")

                    # DEBUG: Tell us that copying was successful
                    print(f"Copy was successful; replaced main save file with {selectedSave}")

                    MSG.showinfo("Copy Successful!", f"Your GHWTDE.sav file has been replaced with the selected backup: {selectedSave}")

                    return True
                
                except Exception as excep:
                    MSG.showerror("Error Replacing Data", f"An error occurred while trying to replace the save data:\n\n{excep}")
                    return False

    # Reset working directory to the default.
    reset_working_directory()

    # Set up root window.
    manageSavesRoot = Tk()
    manageSavesRoot.title("Manage Save Files")
    manageSavesRoot.config(bg = '#FFFFFF')
    manageSavesRoot.iconbitmap(resource_path('res/menuicons/file/save_file.ico'))
    manageSavesRoot.geometry(f"380x530+{int(get_screen_resolution()[0] // 3.25)}+{int(get_screen_resolution()[1] // 6.5)}")
    manageSavesRoot.focus_force()
    manageSavesRoot.resizable(False, False)

    # Update window styling.
    TTK.Style(manageSavesRoot).configure("TButton", background = '#FFFFFF')

    # Header label.
    manageSavesTitle = Label(manageSavesRoot, text = "Manage Save Files: Manage save data for GHWT: DE.", bg = '#FFFFFF', font = FONT_INFO_HEADER, justify = 'left', anchor = 'nw')
    manageSavesTitle.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

    # Back up save data.
    BACK_UP_SAVE_TIP = "Back up your save data at the current date and time. It will be stored in the Save Backups folder where both GHWTDE.ini and GHWTDE.sav is located."
    manageSavesBackUpData = TTK.Button(manageSavesRoot, text = "Back Up Save", width = 20, command = back_up_save)
    manageSavesBackUpData.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'w')
    ToolTip(manageSavesBackUpData, msg = BACK_UP_SAVE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
    
    REPLACE_SAVE_TIP = "Replace your GHWTDE.sav file with another one. Good for loading backups!"
    manageSavesReplaceData = TTK.Button(manageSavesRoot, text = "Replace Save...", width = 20, command = replace_save)
    manageSavesReplaceData.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'w')
    ToolTip(manageSavesReplaceData, msg = REPLACE_SAVE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # List of backups.
    SAVE_BACKUPS_LIST_TIP = "This is a list of all of your backed up save files.\n\nTo load one, select it in the list, and then press \"Load Selected Backup\" below."

    manageSavesBackupsHeader = Label(manageSavesRoot, text = "Save Backups:", bg = '#FFFFFF', font = FONT_INFO_HEADER, justify = 'left', anchor = 'w')
    manageSavesBackupsHeader.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 5, sticky = 'w')
    ToolTip(manageSavesBackupsHeader, msg = SAVE_BACKUPS_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    manageSavesBackupsList = Listbox(manageSavesRoot, bg = '#FFFFFF', bd = 1, relief = 'sunken', width = 60, height = 20)
    manageSavesBackupsList.grid(row = 3, column = 0, columnspan = 2, padx = 10)
    ToolTip(manageSavesBackupsList, msg = SAVE_BACKUPS_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
    save_get_backups()

    # Load selected backup.
    LOAD_SELECTED_TIP = "Load the selected save file backup into your main save slot. It will overwrite your current one!"
    manageSavesLoadBackup = TTK.Button(manageSavesRoot, text = "Load Selected Backup", width = 40, padding = 10, command = replace_with_backup)
    manageSavesLoadBackup.grid(row = 4, column = 0, columnspan = 999, padx = 10, pady = 10)
    ToolTip(manageSavesLoadBackup, msg = LOAD_SELECTED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Close window.
    manageSavesCancel = TTK.Button(manageSavesRoot, text = "Cancel", width = 10, command = manageSavesRoot.destroy)
    manageSavesCancel.grid(row = 5, column = 0, columnspan = 999, padx = 10, pady = 20, sticky = 'e')

    # Enter main loop.
    manageSavesRoot.mainloop()

# Manage Rock Star Creator characters.
def wtde_manage_rsc() -> None:
    """ Manage Rock Star Creator (CAR) characters through the given dialog box. """
    # Reset working directory to the default.
    reset_working_directory()

    # Get the list of installed CAR characters.
    def get_installed_car() -> None:
        """ Get the list of installed CAR characters. """
        OS.chdir(wtde_find_config())

        carListHeader.config(text = f"Installed CARs:")
        carManagerRoot.update_idletasks()

        if (not OS.path.exists("Profiles")): OS.makedirs("Profiles")
            
        OS.chdir("Profiles")

        if (len(OS.listdir(".")) > 0):
            print(f"We've found {len(OS.listdir('.'))} .car files: {OS.listdir('.')}")

            for (file) in (OS.listdir(".")):
                if (OS.path.isfile(file)): carList.insert(END, file)

        TIME.sleep(0.2)

        carListHeader.config(text = f"Installed CARs ({len(OS.listdir('.'))}):")

        reset_working_directory()

    # Install CAR character.
    def install_car_file() -> None:
        """ Install a selected Rock Star Creator character (`.car`) file. """
        carFilePaths = FD.askopenfilenames(title = "Select CAR Character Files", filetypes = (("Rock Star Creator Files", "*.car"), ("All Files", "*.*")))
        
        if (carFilePaths):
            carNames = ""
            for (file) in (carFilePaths): carNames += file + "\n"

            CAR_FILES_SELECTED = "You've chosen to install the following files:\n\n" \
                                f"{carNames.strip()}\n\n" \
                                 "Is this correct?"
    
            if (MSG.askyesno("Confirm Selection", CAR_FILES_SELECTED)):
                for (file) in (carFilePaths):
                    try:
                        SHUT.copy(file, f"{wtde_find_config()}\\Profiles")
                        print(f"{GREEN}Copied file {file}{WHITE}")
                        refresh_list()
                    
                    except Exception as excep:
                        print(f"{RED}Error copying .car file: {excep}{WHITE}")

        carManagerRoot.focus_force()

    # Refresh list.
    def refresh_list() -> None:
        """ Update the list of installed CAR characters. """
        print(f"{YELLOW}Refreshing list of .car files...{WHITE}")
        carList.delete(0, END)
        get_installed_car()

    # Open Profiles folder.
    def open_profiles_folder() -> None:
        """ Opens the Profiles folder in the user's config directory. """
        OS.startfile(f"{wtde_find_config()}\\Profiles")
        print(f"Opening Profiles folder located at: \"{wtde_find_config()}\\Profiles\"")

    # Delete selected CAR.
    def del_selected_car() -> None:
        """ Delete the selected CAR character. """
        if (MSG.askyesno("Are You Sure?", "Are you sure you want to delete this CAR character?")):
            carSelected = ""
            for (x) in (carList.curselection()): carSelected = carList.get(x)

            try:
                OS.remove(f"{wtde_find_config()}\\Profiles\\{carSelected}")
                print(f"{GREEN}Deleted .car file {carSelected}{WHITE}")
                refresh_list()

            except Exception as exc:
                print(f"{RED}Error deleting file {carSelected}: {exc}{WHITE}")

        carManagerRoot.focus_force()

    # Set up window.
    carManagerRoot = Tk()
    carManagerRoot.title("Rock Star Creator (CAR) Manager")
    carManagerRoot.config(bg = '#FFFFFF')
    carManagerRoot.iconbitmap(resource_path('res/icons/rsc_manager.ico'))
    carManagerRoot.geometry(f"530x420+{int(get_screen_resolution()[0] // 3.25)}+{int(get_screen_resolution()[1] // 6.5)}")
    carManagerRoot.resizable(False, False)
    carManagerRoot.focus_force()

    TTK.Style(carManagerRoot).configure("TButton", background = '#FFFFFF')

    # Title header.
    MANAGER_HEADER_TEXT = "Rock Star Creator (CAR) Manager: Manage custom characters created in-game externally."
    carManagerHeader = Label(carManagerRoot, text = MANAGER_HEADER_TEXT, font = FONT_INFO_HEADER, bg = '#FFFFFF', justify = 'left', anchor = 'w')
    carManagerHeader.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

    # List of installed characters.
    carListHeader = Label(carManagerRoot, text = "Installed CARs:", font = FONT_INFO_HEADER, bg = '#FFFFFF', justify = 'left', anchor = 'w')
    carListHeader.grid(row = 1, column = 0, columnspan = 1, sticky = 'w', padx = 5, pady = 5)

    carList = Listbox(carManagerRoot, bg = '#FFFFFF', relief = 'sunken', bd = 2, width = 40, height = 20)
    carList.grid(row = 2, column = 0, rowspan = 999, padx = 5, pady = 5)
    ToolTip(carList, msg = "This is a list of all installed CAR characters.\n\nTo install new ones, select \"Install Character...\" on the right-hand side of the window.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    carListImportCAR = TTK.Button(carManagerRoot, text = "Install Character...", width = 30, command = install_car_file)
    carListImportCAR.grid(row = 2, column = 1, padx = 20)
    ToolTip(carListImportCAR, msg = "Install CAR characters into the mod, in the form of .car files.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    carListRefreshList = TTK.Button(carManagerRoot, text = "Refresh List", width = 30, command = refresh_list)
    carListRefreshList.grid(row = 3, column = 1, padx = 20, pady = 10)
    ToolTip(carListRefreshList, msg = "Update the list of installed CAR characters.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    carListOpenFolder = TTK.Button(carManagerRoot, text = "Open Profiles Folder", width = 30, command = open_profiles_folder)
    carListOpenFolder.grid(row = 4, column = 1, padx = 20)
    ToolTip(carListOpenFolder, msg = "Open the Profiles folder containing all CAR character files.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    carListDeleteSelected = TTK.Button(carManagerRoot, text = "Delete Selected CAR", width = 30, command = del_selected_car)
    carListDeleteSelected.grid(row = 5, column = 1, padx = 20, pady = 10)
    ToolTip(carListDeleteSelected, msg = "Delete the selected CAR from the Profiles folder.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    carManagerCancel = TTK.Button(carManagerRoot, text = "Cancel", width = 10, command = carManagerRoot.destroy)
    carManagerCancel.place(x = 457, y = 392)
    ToolTip(carManagerCancel, msg = "Close this dialog.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Enter main loop.
    get_installed_car()
    carManagerRoot.mainloop()

# Open Mods folder.
def open_mods_folder() -> None:
    """ Opens the user's Mods folder in DATA/MODS. """
    # Change directory to original directory.
    reset_working_directory()

    # Read Updater.ini and get the user's WTDE directory.
    config.read("Updater.ini")
    wtdeDir = config.get("Updater", "GameDirectory")

    debug_add_entry(f"[Open Mods Folder] Opening the user's Mods folder (location: {wtdeDir}/DATA/MODS)", 1)

    # Open MODS folder from the identified directory.
    OS.startfile(f"{wtdeDir}/DATA/MODS")

# Create WTDE shortcut on desktop.
def wtde_create_lnk() -> bool:
    """ Makes a shortcut to WTDE on the desktop. """
    reset_working_directory()

    debug_add_entry("[Make LNK] Adding shortcut to GHWT: DE on Desktop...", 1)

    config.read("Updater.ini")

    wtdeDir = config.get("Updater", "GameDirectory")
    wtdeExeDir = wtdeDir + "/GHWT_Definitive.exe"

    if (not OS.path.exists(wtdeExeDir)):
        MSG.showerror("GHWT_Definitive.exe Not Found", "GHWT_Definitive.exe was not found! Either WTDE is not installed or the executable for WTDE was moved or deleted.")
        
        debug_add_entry("[Make LNK] Error: GHWT_Definitive.exe was not found!", 1)
        
        return False
    
    else:
        debug_add_entry("[Make LNK] Making shortcut...", 1)

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

        debug_add_entry("[Make LNK] Shortcut added on Desktop!", 1)

        return True

# Runs the mod in the user's game folder.
def wtde_run_game() -> None:
    """ Runs GHWT_Definitive.exe in the user's game folder. """
    reset_working_directory()
    config.read('Updater.ini')

    OS.chdir(config.get("Updater", "GameDirectory"))

    OS.system(".\\GHWT_Definitive.exe")

    reset_working_directory()

# ======================================================
# Auto Launch Functions
# ======================================================
# Get venue name.
def auto_get_venue(venueID: str) -> str:
    """ Returns the actual name of the given venue zone ID. """
    # Return the actual venue name.
    for (zone, pak) in (VENUES):
        if (venueID == pak): return zone

    else:
        if (venueID != ""): return venueID
        else: return "None"
    
# Get the venue from the venue selection.
def auto_save_venue(venue: str) -> str:
    """ Take the variable holding the selected Auto Launch venue and convert it to its zone PAK name. """
    # Return the actual venue name.
    for (zone, pak) in (VENUES):
        if (venue == zone): return pak

    else:
        if (venue != "") and (venue != "None"): return venue
        else: return ""

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
        case "Beginner":    return "beginner"
        case "Easy":        return "easy"
        case "Medium":      return "medium"
        case "Hard":        return "hard"
        case "Expert":      return "expert"
        case _:             return ""

# Convert instrument and difficulty to the options in the player settings.
def auto_inst_diff(setting: str) -> str:
    """ Takes a given setting and returns either a part or difficulty. """
    value = config.get("AutoLaunch", setting)

    match (value):
        case "guitar":                  return "Lead Guitar - PART GUITAR"
        case "bass":                    return "Bass Guitar - PART BASS"
        case "drum":                    return "Drums - PART DRUMS"
        case "vocals":                  return "Vocals - PART VOCALS"

        case "beginner":                return "Beginner"
        case "easy":                    return "Easy"
        case "medium":                  return "Medium"
        case "hard":                    return "Hard"
        case "expert":                  return "Expert"

# Language reader function.
def language_name(mode: str, value: str) -> str:
    match (mode):
        case 'option':
            for (optionName, dataValue) in (LANGUAGES):
                if (value == dataValue): return optionName
            else: return LANGUAGES[0][0]

        case 'checksum':
            for (optionName, dataValue) in (LANGUAGES):
                if (value == optionName): return dataValue
            else: return LANGUAGES[0][1]

# Holiday names function.
def holiday_name(mode: str, value: str) -> str:
    match (mode):
        case 'option':
            for (optionName, dataValue) in (HOLIDAYS):
                if (value == dataValue): return optionName
            else: return HOLIDAYS[0][0]

        case 'checksum':
            for (optionName, dataValue) in (HOLIDAYS):
                if (value == optionName): return dataValue
            else: return HOLIDAYS[0][1]

# Intro style function.
def intro_style(mode: str, value: str) -> str:
    match (mode):
        case 'option':
            for (optionName, dataValue) in (INTRO_STYLES):
                if (value == dataValue): return optionName
            else: return INTRO_STYLES[0][0]

        case 'checksum':
            for (optionName, dataValue) in (INTRO_STYLES):
                if (value == optionName): return dataValue
            else: return INTRO_STYLES[0][1]

# Time of Day profile function.
def tod_profile(mode: str, value: str) -> str:
    match (mode):
        case 'option':
            for (optionName, dataValue) in (TOD_PROFILES):
                if (value == dataValue): return optionName
            else: return TOD_PROFILES[0][0]

        case 'checksum':
            for (optionName, dataValue) in (TOD_PROFILES):
                if (value == optionName): return dataValue
            else: return TOD_PROFILES[0][1]

# Strum animations function.
def strum_anim(mode: str, value: str) -> str:
    match (mode):
        case 'option':
            for (optionName, dataValue) in (BASS_STRUM_ANIMS):
                if (value == dataValue): return optionName
            else: return BASS_STRUM_ANIMS[0][0]

        case 'checksum':
            for (optionName, dataValue) in (BASS_STRUM_ANIMS):
                if (value == optionName): return dataValue
            else: return BASS_STRUM_ANIMS[0][1]

# Loading screen themes function.
def loading_theme(mode: str, value: str) -> str:
    match (mode):
        case 'option':
            for (optionName, dataValue) in (LOADING_THEMES):
                if (value == dataValue): return optionName
            else: return LOADING_THEMES[0][0]

        case 'checksum':
            for (optionName, dataValue) in (LOADING_THEMES):
                if (value == optionName): return dataValue
            else: return LOADING_THEMES[0][1]

# User helper themes function.
def user_helper(mode: str, value: str) -> str:
    match (mode):
        case 'option':
            for (optionName, dataValue) in (USER_HELPER_THEMES):
                if (value == dataValue): return optionName
            else: return USER_HELPER_THEMES[0][0]

        case 'checksum':
            for (optionName, dataValue) in (USER_HELPER_THEMES):
                if (value == optionName): return dataValue
            else: return USER_HELPER_THEMES[0][1]

# HUD themes function.
def hud_theme(mode: str, value: str) -> str:
    match (mode):
        case 'option':
            for (optionName, dataValue) in (HUD_THEMES):
                if (value == dataValue): return optionName
            else: return HUD_THEMES[0][0]

        case 'checksum':
            for (optionName, dataValue) in (HUD_THEMES):
                if (value == optionName): return dataValue
            else: return HUD_THEMES[0][1]

# Tap trail themes function.
def tap_trail(mode: str, value: str) -> str:
    match (mode):
        case 'option':
            for (optionName, dataValue) in (TAP_TRAIL_THEMES):
                if (value == dataValue): return optionName
            else: return TAP_TRAIL_THEMES[0][0]

        case 'checksum':
            for (optionName, dataValue) in (TAP_TRAIL_THEMES):
                if (value == optionName): return dataValue
            else: return TAP_TRAIL_THEMES[0][1]

# Hit flame themes function.
def hit_flame(mode: str, value: str) -> str:
    match (mode):
        case 'option':
            for (optionName, dataValue) in (HIT_FLAME_THEMES):
                if (value == dataValue): return optionName
            else: return HIT_FLAME_THEMES[0][0]

        case 'checksum':
            for (optionName, dataValue) in (HIT_FLAME_THEMES):
                if (value == optionName): return dataValue
            else: return HIT_FLAME_THEMES[0][1]

# DOF qualities function.
def dof_quality(mode: str, value: str) -> str:
    match (mode):
        case 'option':
            for (optionName, dataValue) in (DOF_QUALITIES):
                if (value == dataValue): return optionName
            else: return DOF_QUALITIES[0][0]

        case 'checksum':
            for (optionName, dataValue) in (DOF_QUALITIES):
                if (value == optionName): return dataValue
            else: return DOF_QUALITIES[0][1]

# Flare style function.
def flare_style(mode: str, value: str) -> str:
    match (mode):
        case 'option':
            for (optionName, dataValue) in (FLARE_STYLES):
                if (value == dataValue): return optionName
            else: return FLARE_STYLES[0][0]

        case 'checksum':
            for (optionName, dataValue) in (FLARE_STYLES):
                if (value == optionName): return dataValue
            else: return FLARE_STYLES[0][1]

# QPO difficulty function.
def qpo_diff(mode: str, value: str) -> str:
    match (mode):
        case 'option':
            for (optionName, dataValue) in (QPO_DIFFICULTIES):
                if (value == dataValue): return optionName
            else: return QPO_DIFFICULTIES[0][0]

        case 'checksum':
            for (optionName, dataValue) in (QPO_DIFFICULTIES):
                if (value == optionName): return dataValue
            else: return QPO_DIFFICULTIES[0][1]

# ===========================================================================================================
# Mod Manager
# ===========================================================================================================
# Install mod dialog box.
global modInstallWindowActive
modInstallWindowActive = False
def wtde_ask_install_mods() -> None:
    """ Opens a dialog box allowing the user to install more than one mod into their MODS folder. """
    # Add a new mod into the user's MODS folder.
    def wtde_ask_mod(pathList: list, text: Text) -> str:
        """
        Asks the user for a file folder, adds it to the queue.
        """
        # Actions to execute at end of logic.
        def exit_actions():
            """ Actions to perform at the end of the logic chain. """
            pathList.append(modFolder)
            text.insert('end', f"Mod Queued: {testModName} by {testModAuthor}; Type: {modType} | Mod Location: {modFolder}\n")
            text.config(state = 'disabled')
            installQueuedMods.config(state = 'normal')
            clearInstallQueue.config(state = 'normal')
            modInstallRoot.focus_force()
            if (len(modQueueList) == 1) and (len(modZIPQueueList) == 0):
                modInstallRoot.title("Mod Manager: Mod Installer: 1 Mod Pending")
            else: modInstallRoot.title(f"Mod Manager: Mod Installer: {len(modQueueList) + len(modZIPQueueList)} Mods Pending")

        # Ask for a folder.
        modFolder = FD.askdirectory(title = "Select Folder with Mod to Install (MUST BE A FOLDER)")

        if (not modFolder):
            modInstallRoot.focus_force()
            return

        folderName = modFolder.split("/")[-1]
        
        text.config(state = 'normal')

        isValidMod = False

        modType = 'none'

        # Verify the folder and find out what kind of mod it is.
        OS.chdir(modFolder)

        if (OS.path.exists("song.ini")) and (OS.path.exists("Content")):
            print("This is a song mod!")
            modType = 'song'
            isValidMod = True

        elif (OS.path.exists("character.ini")) and (OS.path.exists("Assets")) and (OS.path.exists("Content")):
            print("This is a character mod!")
            modType = 'character'
            isValidMod = True

        elif (OS.path.exists("instrument.ini")) and (OS.path.exists("Content")):
            print("This is an instrument mod!")
            modType = 'instrument'
            isValidMod = True

        elif (OS.path.exists("category.ini")):
            for (fName) in (OS.listdir(".")):
                if (fName.endswith(".img.xen")):
                    print("This is a song category mod!")
                    modType = 'category'
                    isValidMod = True

        elif (OS.path.exists("menumusic.ini")) and (OS.path.exists("Content")):
            print("This is a menu music mod!")
            modType = 'menumusic'
            isValidMod = True

        elif (OS.path.exists("highway.ini")) and (OS.path.exists("Content")):
            print("This is a highway mod!")
            modType = 'highway'
            isValidMod = True

        elif (OS.path.exists("venue.ini")) and (OS.path.exists("Content")):
            print("This is a venue mod!")
            modType = 'venue'
            isValidMod = True

        elif (OS.path.exists("gems.ini")) and (OS.path.exists("Content")):
            print("This is a gem mod!")
            modType = 'gem'

            config.read('gems.ini')
            fileNameToTestFor = config.get('GemInfo', 'Filename')

            if (not OS.path.exists(f"Content/{fileNameToTestFor}.pak.xen")) or (not OS.path.exists(f"Content/{fileNameToTestFor}.qb.xen")):
                MSG.showerror("Gem Mod Incompatible", "This gem mod cannot be used! The PAK and QB file names do not match. Ensure the files are named and packaged correctly, then try again, or contact the author for an updated version.")
                modInstallRoot.focus_force()
                return

            isValidMod = True

        elif (modFolder == ""): return

        else:
            for (fName) in (OS.listdir(".")):
                if (fName.endswith(".qb.xen")) and (OS.path.exists("Mod.ini")):
                    print("This is a script mod!")
                    modType = 'script'
                    isValidMod = True
                    break
                else: continue
            
            else:
                print("This is an invalid mod!")
                isValidMod = False
        
        if (not isValidMod):
            MSG.showerror("Not a Valid Mod", "This is not a valid mod!")
            modInstallRoot.focus_force()
            return

        # Clear ConfigParser.
        config.clear()

        # Show a message based on the type of mod detected.
        match (modType):
            case 'song':
                config.read('song.ini')

                testModName = config.get('ModInfo', 'Name')
                testModDesc = config.get('ModInfo', 'Description')
                testModAuthor = config.get('ModInfo', 'Author')
                testModVersion = config.get('ModInfo', 'Version')

                testSongChecksum = config.get('SongInfo', 'Checksum')
                testSongName = config.get('SongInfo', 'Title')
                testSongArtist = config.get('SongInfo', 'Artist')
                testSongYear = config.get('SongInfo', 'Year')

                if (testSongChecksum) and (testSongName) and (testSongArtist) and (testSongYear):
                    SONG_INFO_CONFIRM_MSG = "It appears this is a song mod!\n\n" \
                                            f"Mod Name: {testModName}\n" \
                                            f"Author: {testModAuthor}\n" \
                                            f"Version: {testModVersion}\n" \
                                            f"About This Mod:\n{testModDesc}\n\n" \
                                            f"Title: {testSongName}\n" \
                                            f"Artist: {testSongArtist}\n" \
                                            f"Year: {testSongYear}\n" \
                                            f"Checksum: {testSongChecksum}\n\n" \
                                            "Is this correct?"
                    
                    if (MSG.askyesno("Mod Confirmation", SONG_INFO_CONFIRM_MSG)): exit_actions()

            case 'character':
                config.read('character.ini')

                testModName = config.get('ModInfo', 'Name')
                testModDesc = config.get('ModInfo', 'Description')
                testModAuthor = config.get('ModInfo', 'Author')
                testModVersion = config.get('ModInfo', 'Version')

                testCharacterName = config.get('CharacterInfo', 'Name')
                testCharacterDesc = config.get('CharacterInfo', 'Description')

                if (testCharacterName) and (testCharacterDesc):
                    CHAR_INFO_CONFIRM_MSG = "It appears this is a character mod!\n\n" \
                                            f"Mod Name: {testModName}\n" \
                                            f"Author: {testModAuthor}\n" \
                                            f"Version: {testModVersion}\n" \
                                            f"About This Mod:\n{testModDesc}\n\n" \
                                            f"Name: {testCharacterName}\n" \
                                            f"Description: {testCharacterDesc}\n\n" \
                                            "Is this correct?"
                    
                    if (MSG.askyesno("Mod Confirmation", CHAR_INFO_CONFIRM_MSG)): exit_actions()

            case 'instrument':
                config.read('instrument.ini')

                testModName = config.get('ModInfo', 'Name')
                testModDesc = config.get('ModInfo', 'Description')
                testModAuthor = config.get('ModInfo', 'Author')
                testModVersion = config.get('ModInfo', 'Version')

                testInstrumentName = config.get('InstrumentInfo', 'Name')
                testInstrumentType = config.get('InstrumentInfo', 'Instrument').title()
                testInstrumentDesc = config.get('InstrumentInfo', 'Description')

                if (testInstrumentName) and (testInstrumentType) and (testInstrumentDesc):
                    INST_INFO_CONFIRM_MSG = "It appears this is an instrument mod!\n\n" \
                                            f"Mod Name: {testModName}\n" \
                                            f"Author: {testModAuthor}\n" \
                                            f"Version: {testModVersion}\n" \
                                            f"About This Mod:\n{testModDesc}\n\n" \
                                            f"Instrument Name: {testInstrumentName}\n" \
                                            f"Instrument Type: {testInstrumentType}\n" \
                                            f"Description: {testInstrumentDesc}\n\n" \
                                            "Is this correct?"
                    
                    if (MSG.askyesno("Mod Confirmation", INST_INFO_CONFIRM_MSG)): exit_actions()

            case 'category':
                config.read('category.ini')

                testModName = config.get('ModInfo', 'Name')
                testModDesc = config.get('ModInfo', 'Description')
                testModAuthor = config.get('ModInfo', 'Author')
                testModVersion = config.get('ModInfo', 'Version')

                testCategoryName = config.get('CategoryInfo', 'Name')
                testCategoryChecksum = config.get('CategoryInfo', 'Checksum')
                testCategoryLogo = f"{config.get('CategoryInfo', 'Logo')}.img.xen"

                if (testCategoryName) and (testCategoryChecksum) and (testCategoryLogo):
                    CATE_INFO_CONFIRM_MSG = "It appears this is a song category!\n\n" \
                                            f"Mod Name: {testModName}\n" \
                                            f"Author: {testModAuthor}\n" \
                                            f"Version: {testModVersion}\n" \
                                            f"About This Mod:\n{testModDesc}\n\n" \
                                            f"Category Name: {testCategoryName}\n" \
                                            f"Category Checksum: {testCategoryChecksum}\n" \
                                            f"Category Logo: {testCategoryLogo}\n\n" \
                                            "Is this correct?"
                    
                    if (MSG.askyesno("Mod Confirmation", CATE_INFO_CONFIRM_MSG)): exit_actions()

            case 'menumusic':
                config.read('menumusic.ini')

                testModName = config.get('ModInfo', 'Name')
                testModDesc = config.get('ModInfo', 'Description')
                testModAuthor = config.get('ModInfo', 'Author')
                testModVersion = config.get('ModInfo', 'Version')

                MENU_INFO_CONFIRM_MSG = "It appears this is a menu music mod!\n\n" \
                                        f"Mod Name: {testModName}\n" \
                                        f"Author: {testModAuthor}\n" \
                                        f"Version: {testModVersion}\n" \
                                        f"About This Mod:\n{testModDesc}\n\n" \
                                        "Is this correct?"
                
                if (MSG.askyesno("Mod Confirmation", MENU_INFO_CONFIRM_MSG)): exit_actions()

            case 'highway':
                config.read('highway.ini')

                testModName = config.get('ModInfo', 'Name')
                testModDesc = config.get('ModInfo', 'Description')
                testModAuthor = config.get('ModInfo', 'Author')
                testModVersion = config.get('ModInfo', 'Version')

                testHighwayPAK = f"{config.get('HighwayInfo', 'Pak')}.pak.xen"
                testHighwayTexture = config.get('HighwayInfo', 'Texture')

                if (testHighwayPAK) and (testHighwayTexture):
                    HGWY_INFO_CONFIRM_MSG = "It appears this is a highway mod!\n\n" \
                                            f"Mod Name: {testModName}\n" \
                                            f"Author: {testModAuthor}\n" \
                                            f"Version: {testModVersion}\n" \
                                            f"About This Mod:\n{testModDesc}\n\n" \
                                            f"Highway PAK: {testHighwayPAK}\n" \
                                            f"Highway Texture: {testHighwayTexture}\n\n" \
                                            "Is this correct?"
                    
                    if (MSG.askyesno("Mod Confirmation", HGWY_INFO_CONFIRM_MSG)): exit_actions()

            case 'script':
                config.read('Mod.ini')

                testModName = config.get('ModInfo', 'Name')
                testModDesc = config.get('ModInfo', 'Description')
                testModAuthor = config.get('ModInfo', 'Author')
                testModVersion = config.get('ModInfo', 'Version')

                SCRT_INFO_CONFIRM_MSG = "It appears this is a script mod!\n\n" \
                                        f"Mod Name: {testModName}\n" \
                                        f"Author: {testModAuthor}\n" \
                                        f"Version: {testModVersion}\n" \
                                        f"About This Mod:\n{testModDesc}\n\n" \
                                        "Is this correct?"
                
                if (MSG.askyesno("Mod Confirmation", SCRT_INFO_CONFIRM_MSG)): exit_actions()

            case 'venue':
                config.read('venue.ini')

                try: testModName = config.get('ModInfo', 'Name')
                except: testModName = "<NO NAME>"
                testModDesc = config.get('ModInfo', 'Description')
                testModAuthor = config.get('ModInfo', 'Author')
                testModVersion = config.get('ModInfo', 'Version')

                testZonePAK = config.get('VenueInfo', 'PakPath')
                testZonePAKPrefix = config.get('VenueInfo', 'PakPrefix')

                if (testZonePAK) and (testZonePAKPrefix):
                    VENU_INFO_CONFIRM_MSG = "It appears this is a venue mod!\n\n" \
                                            f"Mod Name: {testModName}\n" \
                                            f"Author: {testModAuthor}\n" \
                                            f"Version: {testModVersion}\n" \
                                            f"About This Mod:\n{testModDesc}\n\n" \
                                            f"Zone PAK: {testZonePAK}\n" \
                                            f"Zone PAK Prefix: {testZonePAKPrefix}\n\n" \
                                            "Is this correct?"
                    
                    if (MSG.askyesno("Mod Confirmation", VENU_INFO_CONFIRM_MSG)): exit_actions()

            case 'gem':
                config.read('gems.ini')

                try: testModName = config.get('ModInfo', 'Name')
                except: testModName = "<NO NAME>"
                testModDesc = config.get('ModInfo', 'Description')
                testModAuthor = config.get('ModInfo', 'Author')
                testModVersion = config.get('ModInfo', 'Version')

                testGemName = config.get('GemInfo', 'Name')
                testGemFile = config.get('GemInfo', 'Filename')

                if (testGemName) and (testGemFile):
                    GEMS_INFO_CONFIRM_MSG = "It appears this is a gem mod!\n\n" \
                                            f"Mod Name: {testModName}\n" \
                                            f"Author: {testModAuthor}\n" \
                                            f"Version: {testModVersion}\n" \
                                            f"About This Mod:\n{testModDesc}\n\n" \
                                            f"Gem Theme Name: {testGemName}\n" \
                                            f"Gem File: {testGemFile}\n\n" \
                                            "Is this correct?"
                    
                    if (MSG.askyesno("Mod Confirmation", GEMS_INFO_CONFIRM_MSG)): exit_actions()

    # Add a new ZIP mod into the user's MODS folder.
    def wtde_ask_mod_zip(pathList: list, text: Text) -> str:
        """ Asks the user for a ZIP/7Z/RAR (archive) file containing a mod, adds it to the queue. """
        # Actions to execute at end of logic.
        def exit_actions():
            """ Actions to perform at the end of the logic chain. """
            text.config(state = 'normal')
            for (file) in (zipFileNames):
                pathList.append(file)
                text.insert('end', f"Archive Mod Queued: {file}\n")
            text.config(state = 'disabled')
            installQueuedMods.config(state = 'normal')
            clearInstallQueue.config(state = 'normal')
            modInstallRoot.focus_force()
            if (len(modQueueList) == 0) and (len(modZIPQueueList) == 1):
                modInstallRoot.title("Mod Manager: Mod Installer: 1 Mod Pending")
            else: modInstallRoot.title(f"Mod Manager: Mod Installer: {len(modQueueList) + len(modZIPQueueList)} Mods Pending")

        # Ask for a ZIP file.
        zipFileNames = FD.askopenfilenames(title = "Select Mods in ZIP/7Z/RAR Format", filetypes = (("Archive Files", ".zip .7z"), ("ZIP Archives", "*.zip"), ("7-Zip Archives", "*.7z"), ("All Files", "*.*")))

        # If no file name was given, return nothing.
        if (not zipFileNames):
            modInstallRoot.focus_force()
            return

        zipNames = ""

        invalidZIPs = 0
        invalidZIPNames = ""

        for (file) in (zipFileNames):
            zipNames += file + "\n"
            match (OS.path.splitext(file)[1]):
                case '.zip' | '.7z': continue

                case _:
                    invalidZIPs += 1
                    invalidZIPNames += file + '\n'
                    invalidZIPNames.strip()

        if (invalidZIPs >= 1):
            MSG.showerror("Invalid Archive Files", f"There were invalid archive files detected!\n\nThe program found this many invalid files: {invalidZIPs}.\n\nThe following mods are invalid:\n\n{invalidZIPNames}")
            return

        # Ask if the mod is correct.
        ZIP_MOD_CONFIRM_MSG = "You selected the following archives:\n\n" \
                             f"{zipNames.strip()}\n\n" \
                              "Is this correct?"
        
        if (MSG.askyesno("Archived Mod Confirmation", ZIP_MOD_CONFIRM_MSG)): exit_actions()
        else: modInstallRoot.focus_force()

    # Execute installing of queued mods.
    def wtde_execute_mod_install() -> None:
        """ Using the lists of folder paths and archive mod file paths, install all queued mods to the user's MODS folder. """
        # Copy all folders to the user's MODS folder.
        modQueueSize = len(modQueueList) + len(modZIPQueueList)

        if (modQueueSize > 0):
            reset_working_directory()            

            config.clear()

            config.read("Updater.ini")

            copyToDifferentDir = ""

            if (MSG.askyesno("Save to Different Folder?", "Do you want to install all mods to a different folder inside of your MODS folder (in other words, save to a subfolder)?")):
                copyToDifferentDir = FD.askdirectory(title = "Select Alternate Install Folder in MODS", initialdir = f"{config.get('Updater', 'GameDirectory')}/DATA/MODS")

            if (not copyToDifferentDir): copyToDifferentDir = f"{config.get('Updater', 'GameDirectory')}\\DATA\\MODS"

            print(copyToDifferentDir)

            ASK_INSTALL_CONFIRM = f"There are this many mods queued: {len(modQueueList) + len(modZIPQueueList)}.\n\n" \
                                  f"You have set the program to install the mods in this location:\n" \
                                  f"{copyToDifferentDir}\n\n" \
                                   "Is this correct?"
            
            if (MSG.askyesno("Mod Manager: Install Mods", ASK_INSTALL_CONFIRM)):
                modInstallRoot.focus_force()

                copyDir = copyToDifferentDir

                OS.chdir(config.get('Updater', 'GameDirectory'))

                # We'll start with the folders if we have any.
                modsInstalled = 0
                if (len(modQueueList) > 0):
                    for (mod) in (modQueueList):
                        modFolderName = mod.split("/")[-1]

                        installProgressStatus.config(text = f'Installing Mod: {mod} to {f"/DATA/MODS/{modFolderName}"}')

                        # Copy the folder.
                        SHUT.copytree(mod, f"{copyDir}\\{modFolderName}", dirs_exist_ok = True)

                        # Update the progress information.
                        modsInstalled += 1
                        progressValue = (modsInstalled / (modQueueSize)) * 100
                        installProgressBar['value'] = progressValue
                        installProgressPercent.config(text = f"{round(progressValue)}%")

                        modInstallRoot.update_idletasks()
                        TIME.sleep(0.25)

                # Now let's do ZIP/7Z/RAR files.
                if (len(modZIPQueueList) > 0):
                    for (mod) in (modZIPQueueList):
                        print(f"Current mod: {mod}")

                        modFolderName = mod.split("/")[-1]
                        modFolderName = str(modFolderName)

                        installProgressStatus.config(text = f'Extracting Archive Mod: {mod} to {config.get("Updater", "GameDirectory") + f"/DATA/MODS/{modFolderName}"}')
                        modInstallRoot.update_idletasks()

                        match (OS.path.splitext(mod)[1].lower()):
                            case '.zip':
                                modFolderName = modFolderName.strip(".zip")
                            
                            case '.7z':
                                modFolderName = modFolderName.strip(".7z")

                            # case '.rar':
                            #     wasRARFile = True
                            #     modFolderName = modFolderName.strip(".rar")

                        # try:
                        #     if (modFolderName.index(".zip")): modFolderName = modFolderName.split(".zip")[0]

                        # except Exception as excep:
                        #     print(f"{RED}Error installing archive mod {mod}: {excep}{WHITE}")
                        #     debug_add_entry(f"[Mod Installer] ERROR IN MOD INSTALL: {excep}", 2)

                        print(f"modFolderName: {modFolderName}")

                        # Copy the archive file.
                        newZIP = SHUT.copy(mod, copyDir)

                        # Extract the files.
                        tempFolderName = "___" + modFolderName
                        realFolderName = modFolderName

                        newZIPPath = f"{copyDir}\\{tempFolderName}"

                        # What extension is this? Let's use the correct library to unpack it.
                        wasRARFile = False
                        match (OS.path.splitext(newZIP)[1].lower()):
                            case '.zip':
                                with (ZIP.ZipFile(newZIP, 'r')) as zipRef: zipRef.extractall(path = newZIPPath)
                            
                            case '.7z':
                                P7Z.unpack_7zarchive(newZIP, newZIPPath)

                            # case '.rar':
                            #     wasRARFile = True
                                # PAT.extract_archive(newZIP, outdir = newZIPPath)
                                # Archive(newZIP).extractall(newZIPPath, True)

                        # Delete the archive file; we no longer need it.
                        OS.remove(newZIP)

                        # Now, if this is a character or instrument mod, we need to make sure it's installed correctly.
                        # DONE FOR BACKWARDS COMPATIBILITY
                        installProgressStatus.config(text = f'Installing Archive Mod: {mod} to {config.get("Updater", "GameDirectory") + f"/DATA/MODS/{modFolderName}"}')

                        # Head into the folder we just created after extraction.
                        OS.chdir(newZIPPath)

                        # Now we need to iterate through this directory and see if it's a character or instrument mod.
                        # We'll do this since character and instrument mods are subjected to path limit crashes.
                        # Iterate through the directory.
                        isCharInst = False
                        for (dir, _, dirsList) in (OS.walk(".")):
                            print(f"dir: {dir}")
                            print(dirsList)
                            for (file) in (dirsList):
                                print(file)
                                # Have we found a character or instrument mod INI?
                                if (file) in ["character.ini", "instrument.ini"]:
                                    print("Character or instrument mod found; move its contents (doing for compatibility)")
                                    isCharInst = True
                                    outFolder = dir.split('\\')[-1]

                                    # Do the folder names match?
                                    if (outFolder == dir.split('\\')[-2]):
                                        print("Output and source folders match")
                                        SHUT.move(dir, dir + "\\..")
                                        OS.remove(dir)

                                    print(f"outFolder: {outFolder}")
                                    outPath = f"{config.get('Updater', 'GameDirectory')}\\DATA\\MODS\\{outFolder}"
                                    print(f"outPath: {outPath}")
                                    SHUT.copytree(dir, outPath, dirs_exist_ok = True)
                                
                                else: continue

                        # Return to our original copy directory.
                        OS.chdir(copyDir)

                        # If this was a character and/or instrument mod, we can delete the path we just used, we no longer need it.
                        if (isCharInst):
                            OS.chdir(f"{config.get('Updater', 'GameDirectory')}\\DATA\\MODS")

                            try:
                                OS.rmdir(newZIPPath)

                            except OSError as oserr:
                                print(f"{RED}OSError installing mod {mod}: {oserr}{WHITE}")
                                debug_add_entry(f"[Mod Installer] Error in mod install: {oserr}", 2)

                                for (item) in (OS.listdir(newZIPPath)):
                                    filePath = OS.path.join(newZIPPath, item)

                                    try:
                                        if (OS.path.isfile(filePath)) or (OS.path.islink(filePath)):
                                            OS.unlink(filePath)
                                        elif (OS.path.isdir(filePath)): SHUT.rmtree(filePath)

                                    except Exception as excep:
                                        print(f"{RED}Error deleting directory: {excep}{WHITE}")
                                        debug_add_entry(f"[Mod Installer] Error deleting directory: {excep}", 2)

                                OS.rmdir(newZIPPath)

                        else:
                            # Move to actual directory, remove old directory.
                            print(f"temp folder: {tempFolderName}")
                            print(f"real folder: {realFolderName}")
                            try:
                                print("Attempting to rename temp folder to real folder name...")
                                OS.rename(tempFolderName, realFolderName)
                                if (wasRARFile): OS.rename(realFolderName, realFolderName.replace(".rar", ""))

                            except:
                                print("Failed to do that; Must have been an existing, non-empty directory, or something went wrong, trying to move files")
                                print("Attempting to clear non-empty existing directory, then copying files...")

                                debug_add_entry("[Mod Installer] Must have been an existing, non-empty directory, or something went wrong, trying to move files")

                                # Remove everything out of the directory.
                                SHUT.rmtree(realFolderName, ignore_errors = True)

                                SHUT.copytree(tempFolderName, realFolderName)
                                if (wasRARFile): OS.rename(realFolderName, realFolderName.replace(".rar", ""))

                                SHUT.rmtree(tempFolderName, ignore_errors = True)

                        # Make sure our directory is correct.
                        OS.chdir(copyDir)
                        print(f"Currently in {copyDir}")
                            
                        # Update the progress information.
                        print("Updating Progressbar widget...")
                        modsInstalled += 1
                        progressValue = (modsInstalled / (modQueueSize)) * 100
                        installProgressBar['value'] = progressValue
                        installProgressPercent.config(text = f"{round(progressValue)}%")

                        print(f"Mod install is currently {round(progressValue)}% done")

                        modInstallRoot.update_idletasks()
                        TIME.sleep(0.25)

                # Mods have been installed.
                modInstallRoot.update_idletasks()
                print(f"{GREEN}All queued mods have been installed!{WHITE}")
                MSG.showinfo("Mod Install Complete!", "All queued mods installed successfully!")    
                wtde_clear_install_queue(False)

            else:
                modInstallRoot.focus_force()
                return

    # Clear mod queue.
    def wtde_clear_install_queue(ask: bool = True) -> None:
        """ Clear the mod install queue. """
        print("Asked to clear mod install queue!")
        if (ask == False) or (((len(modQueueList) + len(modZIPQueueList)) > 0) and (MSG.askyesno("Clear Mod Queue", "Are you sure you want to clear the mod queue? This cannot be undone!"))):
            print("Clearing global lists and clearing Text widget...")
            modQueueList.clear()
            modZIPQueueList.clear()

            modQueue.config(state = 'normal')
            modQueue.delete('1.0', END)
            modQueue.config(state = 'disabled')

            print("Disabling certain widgets...")

            installQueuedMods.config(state = 'disabled')

            clearInstallQueue.config(state = 'disabled')

            installProgressBar['value'] = 0
            installProgressPercent.config(text = "0%")

            installProgressStatus.config(text = "")

            modInstallRoot.title("Mod Manager: Mod Installer")

        modInstallRoot.focus_force()

    # Cancel window.
    def exit_protocol():
        print("Entered exit protocol for modInstallRoot")
        if (len(modQueueList) > 0):
            if (MSG.askyesno("Are You Sure?", "Are you sure you want to abort mod installation? This will clear out your entire mod queue!")): 
                reset_working_directory()
                print("Leaving Mod Installer, we're done here!")
                modInstallRoot.destroy()
            
            else: modInstallRoot.focus_force()

        else:
            reset_working_directory()
            modInstallRoot.destroy()
        
        global modInstallWindowActive
        modInstallWindowActive = False

    global modInstallWindowActive
    if (modInstallWindowActive): return

    # Set up window.
    modInstallWindowActive = True
    modInstallRoot = Tk()
    modInstallRoot.title("Mod Manager: Mod Installer")
    modInstallRoot.iconbitmap(resource_path('res/menuicons/mods/install_mods.ico'))
    modInstallRoot.geometry(f"640x420+{get_screen_resolution()[0] // 3}+{get_screen_resolution()[1] // 8}")
    modInstallRoot.config(bg = '#FFFFFF')
    modInstallRoot.resizable(False, False)
    modInstallRoot.transient()
    modInstallRoot.focus_force()
    modInstallRoot.protocol("WM_DELETE_WINDOW", exit_protocol)

    # Update window styling.
    TTK.Style(modInstallRoot).configure("TButton", background = '#FFFFFF')
    TTK.Style(modInstallRoot).configure("TCheckbutton", background = '#FFFFFF')

    # Mod queue list. A list of paths.
    global modQueueList
    modQueueList = []

    # Mod queue for ZIP files. A list of file paths.
    global modZIPQueueList
    modZIPQueueList = []

    # Title/header label.
    titleLabel = Label(modInstallRoot, text = "Mod Installer: Install mods into GHWT: DE.", bg = '#FFFFFF', fg = '#000000', font = FONT_INFO_HEADER, anchor = 'w', justify = 'left')
    titleLabel.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

    # Add mod to queue.
    addModToQueue = TTK.Button(modInstallRoot, text = "Add Folder Mod...", command = lambda: wtde_ask_mod(modQueueList, modQueue), width = 20)
    addModToQueue.grid(row = 1, column = 0, padx = 5, pady = 5)
    ToolTip(addModToQueue, msg = "Add a folder containing a mod to the list of mods to install.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    addZIPModToQueue = TTK.Button(modInstallRoot, text = "Add Archive Mod(s)...", command = lambda: wtde_ask_mod_zip(modZIPQueueList, modQueue), width = 20)
    addZIPModToQueue.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'w')
    ToolTip(addZIPModToQueue, msg = "Add mod(s) contained in a ZIP or 7Z file to the list of mods to install.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
    
    clearInstallQueue = TTK.Button(modInstallRoot, text = "Clear Install Queue", command = wtde_clear_install_queue, width = 20)
    clearInstallQueue.place(x = 285, y = 28)
    clearInstallQueue.config(state = 'disabled')
    ToolTip(clearInstallQueue, msg = "Clear out the install queue.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Mod queue.
    modQueueLabel = Label(modInstallRoot, text = "Mod Queue:", bg = '#FFFFFF', fg = '#000000', font = FONT_INFO_HEADER, anchor = 'w', justify = 'left')
    modQueueLabel.grid(row = 2, column = 0, columnspan = 999, sticky = 'w')

    modQueue = Text(modInstallRoot, bg = '#FFFFFF', fg = 'black', font = FONT_INFO, width = 106, height = 16)
    modQueue.grid(row = 3, column = 0, columnspan = 999, sticky = 'w')
    modQueue.config(state = 'disabled')

    MOD_QUEUE_TIP = "The queue of mods to install.\n\n" \
                    "This is a list of all mods you have told the program to install, and what types of mods they are."
    ToolTip(modQueue, msg = MOD_QUEUE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Install queued mods.
    installQueuedMods = TTK.Button(modInstallRoot, text = "Install All Mods", command = wtde_execute_mod_install, width = 20)
    installQueuedMods.place(x = 428, y = 390)
    installQueuedMods.config(state = 'disabled')
    ToolTip(installQueuedMods, msg = "Install all mods that you have queued up.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
    
    # Cancel window.
    cancelInstall = TTK.Button(modInstallRoot, text = "Cancel", command = exit_protocol, width = 10)
    cancelInstall.place(x = 565, y = 390)
    ToolTip(cancelInstall, msg = "Cancel mod installation and clears the mod queue.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Install progress bar.
    installProgressLabel = Label(modInstallRoot, text = "Mod Install Progress:", bg = '#FFFFFF', fg = '#000000', font = FONT_INFO_HEADER, anchor = 'w', justify = 'left')
    installProgressLabel.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = 'w')

    global installProgressBar
    installProgressBar = TTK.Progressbar(modInstallRoot, orient = 'horizontal', length = 400, mode = 'determinate')
    installProgressBar.grid(row = 4, column = 1, padx = 5, pady = 5)

    global installProgressPercent
    installProgressPercent = Label(modInstallRoot, text = "0%", bg = '#FFFFFF', fg = '#000000', font = FONT_INFO_HEADER, anchor = 'w', justify = 'left')
    installProgressPercent.grid(row = 4, column = 2, padx = 5, pady = 5)

    global installProgressStatus
    installProgressStatus = Label(modInstallRoot, text = "", bg = '#FFFFFF', fg = '#000000', font = FONT_INFO_HEADER, anchor = 'w', justify = 'left')
    installProgressStatus.grid(row = 5, column = 0, padx = 5, pady = 5, columnspan = 999, sticky = 'w')

    # Enter main loop for the dialog box.
    modInstallRoot.mainloop()

# Get mod information.
def wtde_get_mod_info(errors: bool = True, returnList: bool = True) -> list[tuple[str]]:
    """
    In the user's MODS folder, return a list of tuples containing all information needed about ALL mods. If mods are nested in sub-folders, it will go through them until it
    finds the necessary files. The `wtde_get_mods()` function will utilize this one, and it can use the data provided by this function to populate the given Treeview.
    \n
    This function uses measures to automatically detect where the user's MODS folder is.
    
    Arguments
    ---------
    - errors: `bool = True` >> Optional: Enable or disable errors after retrieving mod information. `True` by default.
    - returnList: `bool = True` >> Optional: Tells the program if it should return the final tuple list or not.

    Returns
    -------
    `list[tuple[str]]` >> Returns a list of tuples of strings. All tuples in the list contain 5 strings inside.

    Using the `ModInfo` section in each mod's INI files, every tuple in the list is formatted as follows:
    - Mod Name:                 Index 0 is the name of the mod.
    - Mod Author:               Index 1 is the author's name.
    - Mod Type:                 Index 2 is the type of mod it is. The function goes through a logic chain to figure out what type of mod it has found.
    - Mod Version:              Index 3 is the version of the mod.
    - Mod Description:          Index 4 is the description of the mod.

    The following are held as other variables used by the program internally to figure out what mods are where:
    - Mod Path:                 Index 5 is the original path of the mod in the MODS folder.

    Example of Use
    --------------
    Your output results will vary. Let's assume we have 3 mod folders, and we want to print the first five entries of information about each mod.
    >>> print(wtde_get_mod_info())
    [("Example Mod", "You", "Script", "1.0", "An example mod."), ("Another Mod", "Someone Else", "Character", "1.0", "An example character mod."), ("Test Song", "Another Person", "Song", "1.0", "Example song mod.")]
    """
    reset_working_directory()

    config.clear()
    OS.chdir(wtde_find_config())
    config.read("GHWTDE.ini")

    global readDuplicateChecksums, readModsFolder
    readDuplicateChecksums = config.get('Launcher', 'ScanDuplicateSongs')
    readModsFolder = config.get('Launcher', 'PopulateModManager')

    debug_add_entry("[Mod Reader] Attempting to scan entire MODS folder...", 1)

    config.clear()
    reset_working_directory()
    config.read("Updater.ini")

    # verify_updater_config()

    # Start in our MODS folder. This is for enabled mods.
    # Attempt to use the directory in Updater.ini.
    try:
        OS.chdir(f"{config.get('Updater', 'GameDirectory')}\\DATA\\MODS")

    # If we're here, the folder isn't a WTDE install path.
    except:
        config.clear()

        reset_working_directory()

        OS.remove('Updater.ini')

        verify_updater_config()

        OS.chdir(f"{config.get('Updater', 'GameDirectory')}\\DATA\\MODS")

    # print(OS.listdir("."))

    modInfoList = []
    
    global duplicateChecksumsFound
    duplicateChecksumsFound = False
    """ `bool`: Tells if the mod reader found duplicated song mod checksums. """
    
    global songModInfo
    songModInfo = []
    """ `list[list[str]]`: The global list of song mod info. If a sub-list of the main list has a length greater than 2, it is assumed that that checksum has been duplicated. """

    global venueModInfo
    venueModInfo = []

    global gemModInfo
    gemModInfo = []

    filesToCheckFor = [
        'song.ini', 'character.ini', 'instrument.ini', 'category.ini',
        'highway.ini', 'menumusic.ini', 'venue.ini', 'gems.ini', 'Mod.ini'
    ]

    # Start with our MODS folder.
    if (readModsFolder == '1'):
        readStartTime = TIME.time()

        for (dir, _, dirsList) in (OS.walk(".")):
            for (file) in (dirsList):
                if (file) in (filesToCheckFor):
                    debug_add_entry(f"[Mod Reader] In location: {dir}; Mod INI {file} was detected!", 1)
                    try:
                        config.clear()

                        config.read(f"{dir}\\{file}")

                        # print(f"Doing mod folder scan: {len(modInfoList) + 1} mods scanned", end = "\r")

                        modType = ""

                        match (file):
                            case 'song.ini':            modType = "Song"
                            case 'character.ini':       modType = "Character"
                            case 'instrument.ini':      modType = "Instrument"
                            case 'category.ini':        modType = "Song Category"
                            case 'highway.ini':         modType = "Highway"
                            case 'menumusic.ini':       modType = "Menu Music"
                            case 'venue.ini':           modType = "Venue"
                            case 'gems.ini':            modType = "Gems"
                            case 'Mod.ini':             modType = "Script"
                            case _:                     modType = "Other/Unknown"

                        match (modType):
                            case "Song":
                                newChecksum = config.get('SongInfo', 'Checksum')

                                if (len(songModInfo) > 0):
                                    for (mod) in (songModInfo):
                                        if (mod[0] == newChecksum):
                                            duplicateChecksumsFound = True
                                            mod.append(dir)
                                            break

                                    else: songModInfo.append([newChecksum, dir])
                                
                                else: songModInfo.append([newChecksum, dir])

                            case "Venue":
                                try:
                                    venueModInfo.append([f"Mod: {config.get('VenueInfo', 'Name')}", config.get('VenueInfo', 'PakPrefix')])

                                except Exception as excep:
                                    print(f"{RED}Error adding venue mod to list: {excep}")
                                    debug_add_entry(f"[Mod Reader] Error adding venue mod to global list: {excep}", 1)

                            case "Gems":
                                try:
                                    gemModInfo.append([f"Mod: {config.get('GemInfo', 'Name')}", config.get('GemInfo', 'Filename')])

                                except Exception as excep:
                                    debug_add_entry(f"[Mod Reader] Error adding gem mod to global list: {excep}", 1)

                        try: modName = config.get('ModInfo', 'Name')
                        except: modName = ""

                        try: modAuthor = config.get('ModInfo', 'Author')
                        except: modAuthor = ""

                        try: modVersion = config.get('ModInfo', 'Version')
                        except: modVersion = ""

                        try: modDesc = config.get('ModInfo', 'Description')
                        except: modDesc = ""

                        if (config.has_section('ModInfo')):
                            addInfo = (modName, modAuthor, modType, modVersion, modDesc, dir)
                            modInfoList.append(addInfo)
                            debug_add_entry(f"[Mod Reader] Mod added successfully! Mod info tuple[str]: {addInfo}", 2)

                    except Exception as execp:
                        debug_add_entry(f"[Errr] ERROR IN MOD INFO READ: {execp}", 2)
                        print(f"{RED}CRITICAL: Error in reading mod info: {execp}{WHITE}")
                        continue

        readEndTime = TIME.time()

        print(f"ALL MODS SCANNED! We found {len(modInfoList)} mods, scanned in {readEndTime - readStartTime:.2f} seconds")

    print("")

    reset_working_directory()
    
    # DEBUG: Print mod info list.
    # print(modInfoList)
    
    # DEBUG: Print the length of songModInfo and the boolean value of duplicateChecksumsFound.
    print(f"length of songModInfo: {len(songModInfo)}")
    print(f"duplicateChecksumsFound: {duplicateChecksumsFound}")

    # if (duplicateChecksumsFound) and (errors) and (READ_DUPLICATE_CHECKSUMS == '1'):
        # duplicatedValues = ""

        # for (item) in (duplicateChecksums): duplicatedValues += f"\n{item}"

        # SAME_CHECKSUMS_MSG = "Warning: Some of your installed song mods have duplicate checksums. Consider changing them or asking for updated versions with unique checksums.\n\n" \
        #                      "The following checksums are duplicated:\n" \
        #                     f"{duplicatedValues}"

        # MSG.showwarning("Duplicate Checksums Found", SAME_CHECKSUMS_MSG)

    global mods
    mods = modInfoList

    if (returnList): return modInfoList

global mods
mods = wtde_get_mod_info(False)
""" Global list of tuples of strings (`list[tuple[str]]`) that contains information about all installed mods in the user's MODS folder. """

# Remove error function.
def on_rm_error(func, path, exc_info):
    """ Attempts to unlink files from read-only restrictions. """
    OS.chmod(path, STAT.S_IWRITE)
    OS.unlink(path)

# Get mod list.
def wtde_get_mods(window: Tk | Toplevel, tree: TTK.Treeview, label: Label) -> None:
    """
    In the user's MODS folder, we'll find and get all data about ALL mods.
    \n
    This function is a child function to `wtde_get_mod_info()`, which holds the actual data that the Treeview will use.

    Arguments
    ---------
    - window: `tkinter.Tk` OR `tkinter.Toplevel` >> The root window to update the idle tasks on.
    - tree: `tkinter.ttk.Treeview` >> A Treeview widget that we'll populate the data into.
    - label: `tkinter.Label` >> A status Label widget.

    Returns
    -------
    Doesn't return anything.
    """    
    # DEBUG: We're getting mod info.
    debug_add_entry("[Mod Manager] Attempting to retrieve info about all installed mods...", 1)

    # Update label text.
    label.config(text = "Refreshing...")
    
    # Clear out our tree so we can populate it with the new list of info.
    if (len(tree.get_children()) > 0):
        for (item) in (tree.get_children()): tree.delete(item)

    if (not readModsFolder == '1'):
        label.config(text = "Mod Manager populator disabled")
        
        window.update_idletasks()

        return

    window.update_idletasks()

    # Wait for 1/2 a second.
    TIME.sleep(0.5)

    # Run a mod check.
    wtde_get_mod_info(returnList = False)

    # Now let's populate our Treeview!
    for (x, mod) in (enumerate(mods)): tree.insert(parent = '', index = 'end', iid = x, text = '', values = (mod[0], mod[1], mod[2], mod[3], mod[4]))

    # Show that all mods have been reloaded into the Mod Manager.
    label.config(text = f"Mods reloaded; {len(mods)} mods scanned")

    # Reset working directory.
    reset_working_directory()

    # If duplicate song checksums were found, show the Duplicate Checksum Manager.
    if (duplicateChecksumsFound) and (readDuplicateChecksums): duplicate_checksum_manager()

# Update mod listing.
def wtde_update_mod_list(returnList: bool = False) -> list[tuple[str]] | None:
    """ Updates the `mods` global variable. """
    mods = wtde_get_mod_info(False, True)
    if (returnList): return mods

# Duplicate checksum dialog.
def duplicate_checksum_manager() -> None:
    """ After scanning the user's MODS folder for duplicated song mod checksums, opens a dialog box
    that lets the user select which song mods to keep or delete to resolve the conflicts. """
    if (readDuplicateChecksums == '0'): return

    if (not duplicateChecksumsFound):
        MSG.showinfo("No Duplicates!", "You have no duplicated song checksums!")
        return

    reset_working_directory()

    config.clear()
    config.read('Updater.ini')
    MODS_FOLDER_PATH = OS.path.join(config.get('Updater', 'GameDirectory'), "DATA\\MODS")

    # Update path list.
    def update_path_list() -> None:
        """ Update the list of paths on the right hand listbox. """
        # Update status bar.
        dupedSongStatusBar.config(text = "Updating path list...")
        dupedSongManagerRoot.update_idletasks()

        # Update mod listing.
        wtde_update_mod_list()

        # Get the selected checksum.
        selectedChecksum = ""
        for (x) in (dupedSongChecksumList.curselection()): selectedChecksum = dupedSongChecksumList.get(x)

        # Empty the path list.
        dupedSongChecksumPathList.delete(0, END)

        # Find the duped checksum in the songModInfo list.
        for (mod) in (songModInfo):
            if (mod[0] == selectedChecksum):
                for (string) in (mod[1:]): dupedSongChecksumPathList.insert(END, string)
                break

        # Update the checksum listing.
        update_checksum_list()

        # Update status again.
        dupedSongStatusBar.config(text = f"Duplicate checksums reloaded; {dupedSongChecksumList.size()} duplicate checksums detected across {len(songModInfo)} total song mods")
        dupedSongManagerRoot.update_idletasks()
    def update_path_list_e(e: Event) -> None:
        """ Click event for path list. """
        update_path_list()

    # Update checksum list.
    def update_checksum_list() -> None:
        """ Update the list of checksums on the left hand listbox. """
        # Delete all items in the listbox.
        dupedSongChecksumList.delete(0, END)

        # Insert the duplicates!
        for (mod) in (songModInfo):
            if (len(mod) > 2): dupedSongChecksumList.insert(END, mod[0])

    # Delete the selected mod folder.
    def delete_selected_folder() -> None:
        """ Delete the selected mod folder. """
        selectedFolder = ""
        for (x) in (dupedSongChecksumPathList.curselection()): selectedFolder = dupedSongChecksumPathList.get(x)

        if (not selectedFolder):
            print("No folder selected! Returning to window...")
            dupedSongManagerRoot.focus_force()
            return

        print(f"We have selected the following folder: {selectedFolder}")

        OS.chdir(MODS_FOLDER_PATH)

        if (MSG.askyesno("Are You Sure?", f"Are you sure you want to delete the following path? This cannot be undone!\n\n{selectedFolder}")):
            try:
                print(f"{YELLOW}Attempting to remove folder {selectedFolder}...{WHITE}")

                SHUT.rmtree(selectedFolder, on_rm_error)

                TIME.sleep(0.25)

                OS.remove(selectedFolder.split("\\")[1])

                print(f"{GREEN}We got rid of the folder successfully!{WHITE}")

                MSG.showinfo("Mod Deleted", "Mod was successfully deleted.")

            except Exception as excep:
                print(f"{RED}Error deleting mod: {excep}{WHITE}")

                debug_add_entry(f"[Duplicate Checksum Manager] Error deleting mod: {excep}", 2)
                MSG.showerror("Error Deleting Mod", f"An error occurred when deleting this folder:\n\n{excep}")
                
                dupedSongManagerRoot.focus_force()

                reset_working_directory()

                return

        wtde_update_mod_list()

        dupedSongManagerRoot.focus_force()

        # Update the listboxes.
        update_checksum_list()
        update_path_list()

        reset_working_directory()

    # Show the selected mod folder.
    def show_selected_folder() -> None:
        """ Show the selected mod folder in the File Explorer. """
        selectedFolder = ""
        for (x) in (dupedSongChecksumPathList.curselection()): selectedFolder = dupedSongChecksumPathList.get(x)

        if (not selectedFolder): return

        OS.chdir(MODS_FOLDER_PATH)

        print(f"Opening {selectedFolder} in file explorer")
        OS.startfile(selectedFolder)

        reset_working_directory()  

    # Exit routine. Maybe this solves background errors?
    def exit_routine():
        """ Exit routine for the Duplicate Checksum Manager. """
        print("Invoking exit routine for dupedSongManagerRoot")
        try: dupedSongManagerRoot.destroy()
        except Exception as excep: debug_add_entry(f"[Duplicate Checksum Manager] An error occurred invoking WM_DELETE_WINDOW: {excep}", 2)

    reset_working_directory()

    # Make the base window.
    dupedSongManagerRoot = Tk()
    dupedSongManagerRoot.title("Duplicate Song Checksum Manager")
    dupedSongManagerRoot.iconbitmap(resource_path('res/menuicons/mods/copy.ico'))
    dupedSongManagerRoot.config(bg = '#FFFFFF')
    dupedSongManagerRoot.geometry("800x450")
    dupedSongManagerRoot.protocol("WM_DELETE_WINDOW", exit_routine)
    dupedSongManagerRoot.resizable(False, False)
    dupedSongManagerRoot.focus_force()

    # Update styling.
    TTK.Style(dupedSongManagerRoot).configure("TButton", background = '#FFFFFF')

    # Header text.
    dupedSongHeader = Label(dupedSongManagerRoot, text = "Duplicate Song Checksums: Manage song mods that have duplicated checksums.", bg = '#FFFFFF', font = FONT_INFO_HEADER)
    dupedSongHeader.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

    DUPE_CS_LIST_TIP = "This is a list of all checksums that the program found to have been duplicated."
    dupedSongChecksumListHeader = Label(dupedSongManagerRoot, text = "Duplicated Checksums:", bg = '#FFFFFF', font = FONT_INFO_HEADER)
    dupedSongChecksumListHeader.grid(row = 1, column = 0, sticky = 'w')

    dupedSongChecksumList = Listbox(dupedSongManagerRoot, width = 45, height = 20, relief = 'sunken', bg = '#FFFFFF')
    dupedSongChecksumList.grid(row = 2, column = 0, padx = 10, pady = 5)

    ToolTip(dupedSongChecksumListHeader, msg = DUPE_CS_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
    ToolTip(dupedSongChecksumList, msg = DUPE_CS_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    DUPE_PATH_LIST_TIP = "This is a list of all paths that contain song.ini files with the same checksum."
    dupedSongChecksumPathListHeader = Label(dupedSongManagerRoot, text = "Mod Paths:", bg = '#FFFFFF', font = FONT_INFO_HEADER)
    dupedSongChecksumPathListHeader.grid(row = 1, column = 1, columnspan = 3, padx = 30, sticky = 'w')

    dupedSongChecksumPathList = Listbox(dupedSongManagerRoot, width = 75, height = 20, relief = 'sunken', bg = '#FFFFFF')
    dupedSongChecksumPathList.grid(row = 2, column = 1, columnspan = 3, padx = 30, pady = 5)

    # dupedSongRefreshChecksums = TTK.Button(dupedSongManagerRoot, text = "Refresh Checksums", width = 20, command = update_checksum_list)
    # dupedSongRefreshChecksums.grid(row = 3, column = 0, padx = 10, pady = 5)
    # ToolTip(dupedSongRefreshChecksums, msg = "Refresh the list of paths with the paths for the selected checksum.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    ToolTip(dupedSongChecksumPathListHeader, msg = DUPE_PATH_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
    ToolTip(dupedSongChecksumPathList, msg = DUPE_PATH_LIST_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    dupedSongRefreshPaths = TTK.Button(dupedSongManagerRoot, text = "Refresh Paths", width = 20, command = update_path_list)
    dupedSongRefreshPaths.grid(row = 3, column = 1, padx = 10, pady = 5)
    ToolTip(dupedSongRefreshPaths, msg = "Refresh the list of paths with the paths for the selected checksum.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    dupedSongDeleteFolder = TTK.Button(dupedSongManagerRoot, text = "Delete Folder", width = 20, command = delete_selected_folder)
    dupedSongDeleteFolder.grid(row = 3, column = 2, padx = 10, pady = 5)
    ToolTip(dupedSongDeleteFolder, msg = "Delete the selected folder from your mods folder.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    dupedSongShowInFolder = TTK.Button(dupedSongManagerRoot, text = "Show In Folder", width = 20, command = show_selected_folder)
    dupedSongShowInFolder.grid(row = 3, column = 3, padx = 10, pady = 5)
    ToolTip(dupedSongShowInFolder, msg = "Show the selected path in the File Explorer.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    dupedSongStatusBar = Label(dupedSongManagerRoot, text = "", bg = '#FFFFFF', font = FONT_INFO, justify = 'left', width = 120, anchor = 'w')
    dupedSongStatusBar.place(x = 8, y = 422, anchor = 'nw')

    dupedSongCancelWindow = TTK.Button(dupedSongManagerRoot, text = "Cancel", width = 10, command = dupedSongManagerRoot.destroy)
    dupedSongCancelWindow.place(x = 726, y = 422)
    ToolTip(dupedSongCancelWindow, msg = "Close this dialog without saving any changes.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    update_checksum_list()

    dupedSongChecksumList.bind('<ButtonRelease-1>', update_path_list_e)

    # Enter main loop.
    dupedSongManagerRoot.focus_force()
    dupedSongManagerRoot.mainloop()

# Song mod and song category/categorization manager.
def song_category_manager() -> None:
    """ User management for songs and song categories. """
    reset_working_directory()

    global loadedCategoryData
    loadedCategoryData = ["", "", "", ""]
    """ Currently loaded category list that is held in memory to the currently loaded category. """

    global knownCategoryData
    knownCategoryData = []

    # Take a PNG image and convert it to IMG.
    def png_to_img_xen(dir: str) -> str:
        """ Takes a PNG image and converts it to `*.img.xen` format. """
        reset_working_directory()
        config.clear()
        config.read('Updater.ini')
        OS.chdir(f"{config.get('Updater', 'GameDirectory')}/DATA/MODS")
        
        if (not dir.find(".png")):
            print("This isn't a PNG file!")
            return

        print("-- CONVERTING PNG TO IMG ------------------------")

        outFile = dir.replace('\\', '/').replace('.png', '.img.xen')

        # Get the image data and image size (both in bytes)
        # to be written to the IMG file.
        with (open(dir, 'rb')) as in_file:
            # PNG data and image size.
            png_data = in_file.read()
            pngImageSize = len(png_data)

            print(f"Input PNG file is {pngImageSize} B")

        # Use PIL (Pillow) to get the image's dimensions.
        imageWidth, imageHeight = Image.open(dir).size
        print(f"Image size: {imageWidth} X {imageHeight}")

        # Now we're compiling an IMG file.
        with (open(outFile, 'wb')) as img_xen:
            # IMG FILES ARE LAID OUT LIKE THIS, I THINK:
            # - First, constant 8 bytes.
            # - Image width, image height, 1
            # - Image width, image height, 1
            # - 12 more constant bytes.
            # - Image size, term (0, unless on X360).
            # - Actual PNG data.

            # First 8 bytes of the IMG file. -- 0x0A, 0x28, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00
            # These should never change.
            byteConst1 = bytes([0x0A, 0x28, 0x13, 0x00, 0x00, 0x00, 0x00, 0x00]) 
            img_xen.write(byteConst1)

            # Now, image size.
            imgW = struct.pack('>H', imageWidth)
            imgH = struct.pack('>H', imageHeight)
            imgOne = struct.pack('>H', 1)

            print(f"(w, h, one): {imgW}, {imgH}, {imgOne}")

            img_xen.write(imgW)
            img_xen.write(imgH)
            img_xen.write(imgOne)
            img_xen.write(imgW)
            img_xen.write(imgH)
            img_xen.write(imgOne)

            # Next 12 constant bytes. -- 0x01, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x28
            byteConst2 = bytes([0x01, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x28])
            img_xen.write(byteConst2)

            # Now we want the image size.
            # term in the file should be 0, unless we're on Xbox 360 (we should never be,
            # this is a for **A PC MOD** of GHWT).
            packedSize = struct.pack(">I", pngImageSize)
            print(f"value of packedSize: {packedSize}")
            
            img_xen.write(packedSize)

            termZero = struct.pack('>I', 0)
            img_xen.write(termZero)

            # And now for the actual PNG data itself.
            img_xen.write(png_data)

            print("-- PNG TO IMG CONVERSION COMPLETE ------------------------")

        return outFile
    
    # Open *.img.xen file, update active selected category image.
    def open_img_xen(path: str) -> str:
        """ Runs an `*.img.xen` file through IMG2PNG, makes a PNG, saves it, loads it into memory, then erases it from the disk. """
        print("-- IMG.XEN IMAGE CONVERTING ------------------------")

        reset_working_directory()
        config.read('Updater.ini')
        OS.chdir(f"{config.get('Updater', 'GameDirectory')}\\DATA\\MODS")
        
        with (open(path, 'rb')) as img_xen:
            fixed_path = path.replace("\\", "/")

            # Open IMG file, take all the data as bytes.
            data = img_xen.read()

            # Where does the image start?
            image_start = struct.unpack_from(">I", data, 28)[0]
            print(f"image start: {image_start}")

            # What is the size of the image?
            image_size = struct.unpack_from(">I", data, 32)[0]
            print(f"image size: {image_size}")

            # Now we'll get the data of the image.
            image_data = struct.unpack_from(str(image_size) + "B", data, image_start)
            print(f"file type: {image_data[1:4]}")

            if (image_data[1:4] == (80, 78, 71)):
                print("Valid PNG found!")

                fileName = fixed_path.replace(".img.xen", "")

                with (open(f"{fileName}.png", 'wb')) as png: png.write(bytes(image_data))

                print("IMG converted to PNG!")

                pngPath = OS.path.join(f"{config.get('Updater', 'GameDirectory')}/DATA/MODS", fixed_path.replace(".img.xen", ".png").split("./")[-1])
                print(f"!!! --- IMAGE PATH CHECK: PNG file should be located here: {pngPath}")

                # Scale down the image so it fits nicely!
                imageSize = 160
                origImage = Image.open(pngPath)
                resizedImage = origImage.resize((imageSize, imageSize), Image.ADAPTIVE)
                global img
                img = ImageTk.PhotoImage(resizedImage, width = imageSize, height = imageSize)

                print(f"is path a file? {OS.path.isfile(pngPath)}")

                if (img): print("image is okay")
                else: print("SOMETHING IS WRONG HERE")

                # selectedCatImage.delete('all')
                try:
                    selectedCatImage.config(image = img, width = 160, height = 160)
                    print(f"selectedCatImage, value of key \"image\" is: {selectedCatImage.cget('image')}")
                except Exception as exc:
                    print(f"WHY ARE WE CRASHING HERE? {exc}")

                songCategoryManagerRoot.update_idletasks()

                reset_working_directory()

                print("-- IMG.XEN IMAGE CONVERSION FINISHED ---------------")

                return

            else:
                print("Error: Not a valid PNG file, conversion failed")

        reset_working_directory()

        print("-- IMG.XEN IMAGE CONVERSION FINISHED ---------------")

        '''
        reset_working_directory()
        path = path.replace("/", "\\")
        SUB.run([f".\\{resource_path('IMG2PNG.exe')}", path], capture_output = True)
        return path.replace(".img.xen", ".png")
        '''

    # Returns a list of category information.
    def get_song_categories() -> list[list[str]]:
        """ Returns a list of categories with these items per sub-list: [name, path, checksum, img]"""
        reset_working_directory()

        allModsInfo = wtde_get_mod_info()
        print(f"Mods found: {len(allModsInfo)}")

        config.read('Updater.ini')
        OS.chdir(f"{config.get('Updater', 'GameDirectory')}\\DATA\\MODS")
        config.clear()

        returnList: list[list[str]] = []

        for (infoList) in (allModsInfo):
            if (infoList[2] == "Song Category"):
                # print(f"in directory: {infoList[5]}")

                config.read(f"{infoList[5]}\\category.ini")

                try: categoryName = config.get("CategoryInfo", "Name")
                except: categoryName = "Missing Info!"

                try: categoryPath = infoList[5]
                except: categoryPath = "Missing Info!"

                try: categoryIMG = f"{infoList[5]}/{config.get('CategoryInfo', 'Logo')}.img.xen"
                except: categoryIMG = "Missing Info!"

                try: categoryChecksum = config.get("CategoryInfo", "Checksum")
                except: categoryChecksum = "Missing Info!"

                config.clear()
            
                returnList.append([categoryName, categoryPath, categoryChecksum, categoryIMG])

                continue

        songCatsList.delete(0, END)

        for (cateName, _, _, _) in (returnList): songCatsList.insert(END, cateName)
        
        songCatsHeaderLabel.config(text = f"Song Categories ({songCatsList.size()}):")

        reset_working_directory()

        global knownCategoryData
        knownCategoryData = returnList

        return returnList
    
    # Returns a list of category information.
    def get_song_mods() -> list[list[str]]:
        """ Returns a list of mods with these items per sub-list: [name, path, checksum, tied_cat]"""
        reset_working_directory()

        allModsInfo = wtde_get_mod_info()
        print(f"Mods found: {len(allModsInfo)}")

        config.read('Updater.ini')
        OS.chdir(f"{config.get('Updater', 'GameDirectory')}\\DATA\\MODS")
        config.clear()

        returnList: list[list[str]] = []

        for (infoList) in (allModsInfo):
            if (infoList[2] == "Song"):
                # print(f"in directory: {infoList[5]}")

                config.read(f"{infoList[5]}\\song.ini")

                try: categoryName = f"{config.get('SongInfo', 'Artist')} - {config.get('SongInfo', 'Title')}"
                except: categoryName = "Missing Info!"

                try: categoryPath = infoList[5]
                except: categoryPath = "Missing Info!"

                try: categoryIMG = config.get('SongInfo', 'Checksum')
                except: categoryIMG = "Missing Info!"

                try: categoryChecksum = config.get("SongInfo", "GameCategory")
                except: categoryChecksum = ""

                config.clear()
            
                returnList.append([categoryName, categoryPath, categoryIMG, categoryChecksum])

                continue

        songCatsList.delete(0, END)

        for (cateName, _, _, _) in (returnList): songList.insert(END, cateName)

        songListHeaderLabel.config(text = f"Song Mods ({songList.size()}):")
        
        reset_working_directory()
        return returnList

    # Refresh mods.
    def refresh_mods() -> None:
        """ Refresh the mod listing. """
        songList.delete(0, END)
        songCatsList.delete(0, END)

        editorStatusBar.config(text = "Refreshing mods list...")
        songCategoryManagerRoot.update_idletasks()
        TIME.sleep(0.5)

        get_song_mods()
        get_song_categories()

        editorStatusBar.config(text = "Mods and category mods list refreshed")
        songCategoryManagerRoot.update_idletasks()

    # Load data for selected category.
    def load_category_info() -> None:
        """ Import the data from the selected category on the lower left. """
        editorStatusBar.config(text = "Loading selected category data...")
        songCategoryManagerRoot.update_idletasks()

        selectedSongChecksum.config(text = "")
        selectedSongGameIcon.delete(0, END)

        songTitleEntry.delete(0, END)
        songArtistEntry.delete(0, END)
        songYearEntry.delete(0, END)

        global selectedCate
        selectedCate = 0
        for (x) in (songCatsList.curselection()): selectedCate = int(x)

        print(f"----------\nSelected index: {selectedCate}\nApparent info: {knownCategoryData[selectedCate]}")
        
        categoryChecksum = ""
        print("/// --- Iterating for correct category")
        
        global loadedCategoryData
        loadedCategoryData = knownCategoryData[selectedCate]

        cate = knownCategoryData[selectedCate]

        # print(f"do the two match? {songCatsList.get(selectedCate) == cate[0]}")
        categoryChecksum = cate[2]

        open_img_xen(cate[3])

        dataString = f"Name: {cate[0]}\nPath: {cate[1]}\nChecksum: {cate[2]}"
        
        print(f"We're looking for this checksum: {categoryChecksum}")

        # Now, let's find out all of the songs in the category.
        # We'll have to iterate through the entire MODS directory.

        # Get to the correct directory.
        reset_working_directory()
        config.clear()
        config.read('Updater.ini')
        OS.chdir(f"{config.get('Updater', 'GameDirectory')}\\DATA\\MODS")
        config.clear()

        # What INI files are we looking for?
        filesToCheckFor = [
            'song.ini', 'folder.ini'
        ]

        # Return list.
        addToTreeList: list[tuple[str]] = []
        addTuple = ()

        # Now, time to do some iterating!
        print(f"current working dir: {OS.getcwd()}")

        print("/// --- LOOKING FOR SONG MODS TIED TO CATEGORY")
        for (dir, _, dirsList) in (OS.walk(".")):
            # print(f"in dir: {dir}")
            addTuple = ()
 
            linkedCat = ""
            songName = ""
            songArtist = ""
            songChecksum = ""

            for (file) in (dirsList):
                if (file) in (filesToCheckFor):

                    config.clear()
                    config.read(f"{dir}\\{file}")

                    match (file):
                        case 'song.ini':
                            print("/// -S- Found a song mod config")

                            try: linkedCat = config.get('SongInfo', 'GameCategory')
                            except: linkedCat = ""

                            if (linkedCat) and (linkedCat.upper() == categoryChecksum.upper()):
                                print("!! -- We found the category we want!")
                                try: songName = config.get('SongInfo', 'Title')
                                except: songName = "Untitled"

                                try: songArtist = config.get('SongInfo', 'Artist')
                                except: songArtist = "Unknown Artist"

                                try: songChecksum = config.get('SongInfo', 'Checksum')
                                except: songChecksum = 'undefined'

                                songTitle = f"{songArtist} - {songName}"

                                addTuple = (songTitle, dir, songChecksum)
                                addToTreeList.append(addTuple)
                                print(f"Mod added: {addTuple}")

                            else:
                                print("Not the category we want, keep looking")

                        # Folder config, assume the entire folder is related to the
                        # category in the INI file.
                        case 'folder.ini':
                            print("/// -F- Found a folder config")

                            # Is this the checksum we want?
                            # Song category checksums are case insensitive.
                            if (config.has_option("SongInfo", "GameCategory")):
                                if (config.get('SongInfo', 'GameCategory').upper() == categoryChecksum.upper()):
                                    # It is, now let's just get the names of every song in this folder.
                                    print("!! -- We found the category we want!")

                                    for (childDir, _, childDirsList) in (OS.walk(dir)):
                                        for (childFile) in (childDirsList):
                                            if (childFile == 'song.ini'):

                                                config.clear()

                                                config.read(f"{childDir}\\{childFile}")

                                                try: songName = config.get('SongInfo', 'Title')
                                                except: songName = "Untitled"

                                                try: songArtist = config.get('SongInfo', 'Artist')
                                                except: songArtist = "Unknown Artist"

                                                try: songChecksum = config.get('SongInfo', 'Checksum')
                                                except: songChecksum = 'undefined'

                                                songTitle = f"{songArtist} - {songName}"

                                                # WE DON'T CARE ABOUT LINKED CATEGORY HERE
                                                addTuple = (songTitle, childDir, songChecksum)
                                                addToTreeList.append(addTuple)
                                                print(f"Mod added: {addTuple}")

                            else:
                                print("Not the category we want, keep looking")

                        case _:
                            config.clear()
                            continue

        addToTreeList = sorted(list(set(addToTreeList)))

        dataString += f"\nSongs Tied to Category: {len(addToTreeList)}"

        selectedCatData.config(text = dataString)

        # We're done iterating, back to the starting dir.
        reset_working_directory()

        # Add elements to the Treeview.
        if (len(selectedCatSongs.get_children()) > 0):
            for (item) in (selectedCatSongs.get_children()): selectedCatSongs.delete(item)

        for (x, mod) in (enumerate(addToTreeList)): selectedCatSongs.insert(parent = '', index = 'end', iid = x, text = '', values = (mod[0], mod[1], mod[2]))

        editorStatusBar.config(text = f"All data loaded, found {len(addToTreeList)} song(s) in this category")
        songCategoryManagerRoot.update_idletasks()
    def load_category_info_e(e: Event) -> None:
        load_category_info()

    # Open the category in the File Explorer.
    def open_category_folder() -> None:
        """ Opens the currently selected category in the File Explorer. """
        reset_working_directory()
        config.clear()
        config.read("Updater.ini")
        OS.chdir(f"{config.get('Updater', 'GameDirectory')}\\DATA\\MODS")
        if (loadedCategoryData[0]): OS.startfile(loadedCategoryData[1])

        config.clear()
        reset_working_directory()

    # Load selected Treeview song mod.
    def get_selected_song_mod_data(e: Event) -> None:
        """ Update data fields below the Treeview with the selected item in the tree. """
        if (len(selectedCatSongs.get_children()) <= 0):
            print("No songs are in this category!")
            return

        curItem = selectedCatSongs.focus()

        reset_working_directory()
        config.clear()
        config.read('Updater.ini')
        OS.chdir(f"{config.get('Updater', 'GameDirectory')}\\DATA\\MODS")
        config.read(f"{selectedCatSongs.item(curItem)['values'][1]}\\song.ini")

        selectedSongChecksum.config(text = "")
        selectedSongGameIcon.delete(0, END)

        songTitleEntry.delete(0, END)
        songArtistEntry.delete(0, END)
        songYearEntry.delete(0, END)

        try: selectedSongGameIcon.insert(END, config.get('SongInfo', 'GameIcon'))
        except: selectedSongGameIcon.insert(END, "")

        selectedSongChecksum.config(text = selectedCatSongs.item(curItem)['values'][2])

        songTitleEntry.insert(END, config.get('SongInfo', 'Title'))
        songArtistEntry.insert(END, config.get('SongInfo', 'Artist'))
        songYearEntry.insert(END, config.get('SongInfo', 'Year'))

        reset_working_directory()

    # Open selected Treeview song mod in File Explorer.
    def open_selected_song_mod_folder() -> None:
        """ Opens the mod folder for the selected song mod in the Treeview in the File Explorer. """
        try:
            curItem = selectedCatSongs.focus()

            reset_working_directory()
            config.clear()
            config.read('Updater.ini')
            OS.chdir(f"{config.get('Updater', 'GameDirectory')}\\DATA\\MODS")
            config.read(f"{selectedCatSongs.item(curItem)['values'][1]}\\song.ini")

            OS.startfile(selectedCatSongs.item(curItem)['values'][1])

            reset_working_directory()
        
        except Exception as exc:
            print(f"Can't open folder! Probably no category was loaded. | {exc}")
            return

    # Import IMG file for GameIcon parameter for selected song mod.
    def select_game_icon() -> None:
        """ Ask the user for an `*.img.xen` to link to a song mod as its icon. """
        fileToUse = FD.askopenfilename(title = "Select Logo Image", filetypes = (("NX Image Files", "*.img.xen"),)).replace("\\", "/")

        if (fileToUse):
            selectedSongGameIcon.delete(0, END)

            selectedSongGameIcon.insert(END, fileToUse.split("/")[-1].replace(".img.xen", ""))

        songCategoryManagerRoot.focus_force()

    # Make new category mod.
    def make_new_category() -> None:
        """ Makes a new category mod for the end user to tie song mods to. """
        # Select output path.
        def select_out_dir() -> None:
            """ Select the output path in DATA/MODS for this category. """
            reset_working_directory()
            config.clear()
            config.read("Updater.ini")
            outDir = FD.askdirectory(title = "Select Output Folder", initialdir = f"{config.get('Updater', 'GameDirectory')}/DATA/MODS")

            if (outDir):
                newCateDir.delete(0, END)
                newCateDir.insert(END, outDir)

            newCategoryRoot.focus_force()

        # Select image path.
        def select_image_dir() -> None:
            """ Select the image path for this category. """
            reset_working_directory()
            config.clear()
            config.read("Updater.ini")
            outDir = FD.askopenfilename(title = "Select Image File", filetypes = (("PNG Images", "*.png"),))

            if (outDir):
                newCateImageDir.delete(0, END)
                newCateImageDir.insert(END, outDir)

            newCategoryRoot.focus_force()

        # Create new mod.
        def create_mod() -> None:
            """ Make a new category mod. """
            modCreateS = TIME.time()

            # The save directory.
            saveDir = newCateDir.get().replace("\\", "/")

            # The image path.
            imageDir = newCateImageDir.get().replace("\\", "/")

            # Make new directory. Assume we're in DATA/MODS.
            # That is, make it if it doesn't already exist.
            reset_working_directory()
            config.clear()
            config.read('Updater.ini')

            modsDir = f"{config.get('Updater', 'GameDirectory')}/DATA/MODS".replace("\\", "/")

            OS.chdir(f"{config.get('Updater', 'GameDirectory')}/DATA/MODS")

            print(f"Category will be saved here: {saveDir}")

            if (not OS.path.exists(saveDir)): OS.mkdir(saveDir)

            # Now change into that directory.
            OS.chdir(saveDir)

            # Now, let's make us a new INI file. I'll just write this
            # as a text file. This is pretty straightforward.
            with (open('category.ini', 'w')) as ini:
                # I think this is a PNG extension...
                outLogo = newCateImageDir.get().replace('\\', '/').split('/')[-1].replace('.png', '')

                print(f"out logo text: {outLogo}")

                # The contents of the INI itself.
                OUT_INI_DATA = "[ModInfo]\n" \
                              f"Name={newCateName.get()}\n" \
                              f"Author={newCateModAuthor.get()}\n" \
                              f"Description={newCateModDesc.get()}\n" \
                               "Version=1.0\n\n" \
                               "[CategoryInfo]\n" \
                              f"Name={newCateName.get()}\n" \
                              f"Checksum={newCateChecksum.get()}\n" \
                              f"Logo={outLogo}"
                
                ini.write(OUT_INI_DATA)

                print('Mod config written!')

            # Now take the output image and copy it to the category folder.
            outImage = png_to_img_xen(imageDir)
            SHUT.copy(outImage, saveDir)

            modCreateE = TIME.time()

            print(f"ALL DONE! New category created in {modCreateE - modCreateS:.2f} seconds\nname: {newCateName.get()}\ndir: {saveDir}\nimage: {imageDir}\nchecksum: {newCateChecksum.get()}")
            
            # DEBUG: Open the category folder.
            # OS.startfile(saveDir)

            refresh_mods()
            newCategoryRoot.destroy()


        # Set up Tk window, like usual.
        newCategoryRoot = Toplevel()
        newCategoryRoot.title("New Song Category")
        newCategoryRoot.config(bg = '#FFFFFF')
        newCategoryRoot.iconbitmap(resource_path('res/menuicons/file/new_file.ico'))
        newCategoryRoot.geometry("500x500")
        newCategoryRoot.resizable(False, False)
        newCategoryRoot.focus_force()

        # Title header.
        newCateTitleHeader = Label(newCategoryRoot, text = "New Song Category: Create a new category mod to tie song mods to.", font = FONT_INFO_HEADER, bg = '#FFFFFF', fg = '#000000')
        newCateTitleHeader.grid(row = 0, column = 0, padx = 3, columnspan = 999, sticky = 'w')

        # New category name.
        newCateNameLabel = Label(newCategoryRoot, text = "          Name:     ", bg = "#FFFFFF", fg = '#000000', font = FONT_INFO)
        newCateNameLabel.grid(row = 1, column = 0, pady = 5, sticky = 'e')

        newCateName = TTK.Entry(newCategoryRoot, width = 30)
        newCateName.grid(row = 1, column = 1, pady = 5, sticky = 'w')

        # New category path.
        newCateDirLabel = Label(newCategoryRoot, text = "          Path:     ", bg = "#FFFFFF", fg = '#000000', font = FONT_INFO)
        newCateDirLabel.grid(row = 2, column = 0, pady = 5, sticky = 'e')

        newCateDir = TTK.Entry(newCategoryRoot, width = 50)
        newCateDir.grid(row = 2, column = 1, pady = 5, sticky = 'w')

        newCateDirSelectDir = TTK.Button(newCategoryRoot, text = '...', width = 3, command = select_out_dir)
        newCateDirSelectDir.grid(row = 2, column = 2, pady = 5, padx = 5)

        # New category checksum.     
        newCateChecksumLabel = Label(newCategoryRoot, text = "      Checksum:     ", bg = "#FFFFFF", fg = '#000000', font = FONT_INFO)
        newCateChecksumLabel.grid(row = 3, column = 0, pady = 5, sticky = 'e')

        newCateChecksum = TTK.Entry(newCategoryRoot, width = 15)
        newCateChecksum.grid(row = 3, column = 1, pady = 5, sticky = 'w')

        # New category image path.
        newCateImageDirLabel = Label(newCategoryRoot, text = "         Image:     ", bg = "#FFFFFF", fg = '#000000', font = FONT_INFO)
        newCateImageDirLabel.grid(row = 4, column = 0, pady = 5, sticky = 'e')

        newCateImageDir = TTK.Combobox(newCategoryRoot, width = 47, values = GAME_LOGO_IMAGES)
        newCateImageDir.grid(row = 4, column = 1, pady = 5, sticky = 'w')

        newCateImageSelectDir = TTK.Button(newCategoryRoot, text = '...', width = 3, command = select_image_dir)
        newCateImageSelectDir.grid(row = 4, column = 2, pady = 5, padx = 5)

        # New category mod description.                      
        newCateModDescLabel = Label(newCategoryRoot, text = "  Mod Description:     ", bg = "#FFFFFF", fg = '#000000', font = FONT_INFO)
        newCateModDescLabel.grid(row = 5, column = 0, pady = 5, sticky = 'e')

        newCateModDesc = TTK.Entry(newCategoryRoot, width = 50)
        newCateModDesc.grid(row = 5, column = 1, pady = 5, sticky = 'w')

        # New category mod author.
        newCateModAuthorLabel = Label(newCategoryRoot, text = "       Mod Author:     ", bg = "#FFFFFF", fg = '#000000', font = FONT_INFO)
        newCateModAuthorLabel.grid(row = 6, column = 0, pady = 5, sticky = 'e')

        newCateModAuthor = TTK.Entry(newCategoryRoot, width = 40)
        newCateModAuthor.grid(row = 6, column = 1, pady = 5, sticky = 'w')

        # Create button.
        newCateCreateButton = TTK.Button(newCategoryRoot, text = "OK / Create New", width = 20, command = create_mod)
        newCateCreateButton.place(x = 280, y = 470)

        # Cancel dialog.
        newCateCancelButton = TTK.Button(newCategoryRoot, text = "Cancel", width = 10, command = newCategoryRoot.destroy)
        newCateCancelButton.place(x = 420, y = 470)

        # ---------------------- TOOLTIPS ---------------------- #
        ToolTip(newCateName, msg = "The name of this category.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        ToolTip(newCateNameLabel, msg = "The name of this category.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        ToolTip(newCateDir, msg = "The directory this category will be created in.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        ToolTip(newCateDirLabel, msg = "The directory this category will be created in.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        ToolTip(newCateDirSelectDir, msg = "Select a directory on the disk to save this category to.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        ToolTip(newCateChecksum, msg = "The checksum (unique identifier) for this category, used to tie songs to this category.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        ToolTip(newCateChecksumLabel, msg = "The checksum (unique identifier) for this category, used to tie songs to this category.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        ToolTip(newCateImageDir, msg = "The image that will be associated with this category.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        ToolTip(newCateImageDirLabel, msg = "The image that will be associated with this category.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        ToolTip(newCateImageSelectDir, msg = "Select a PNG or IMG file on the disk.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        ToolTip(newCateModDesc, msg = "The description of the mod. Shows up in the Installed Mods menu in-game and in the Mod Manager in the launcher.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        ToolTip(newCateModDescLabel, msg = "The description of the mod. Shows up in the Installed Mods menu in-game and in the Mod Manager in the launcher.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        ToolTip(newCateModAuthor, msg = "The author of this category mod.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        ToolTip(newCateModAuthorLabel, msg = "The author of this category mod.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        ToolTip(newCateCreateButton, msg = "Create a new category using the provided information.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
        ToolTip(newCateCancelButton, msg = "Close this window without saving any changes.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

        newCategoryRoot.mainloop()

    # Edit the data of the selected category.
    def edit_category_meta(data: list[str]) -> None:
        """ Edit the meta data of the selected category. """
        if (loadedCategoryData == ["", "", "", ""]): return

        # Convert new image, output to folder.
        def change_category_image() -> None:
            """ Updates the image for the category. """
            global imageFile
            imageFile = FD.askopenfilename(title = "Select PNG Image", filetypes = (("PNG Images", '*.png'),))

            png_to_img_xen(imageFile)

            if (imageFile):
                imageFile = imageFile.replace("\\", "/")
                imageFile = imageFile.replace(".png", ".img.xen")

                reset_working_directory()
                config.clear()
                config.read("Updater.ini")
                OS.chdir(f"{config.get('Updater', 'GameDirectory')}/DATA/MODS")

                cateImage.delete(0, END)
                cateImage.insert(END, imageFile.split("/")[-1].replace(".img.xen", ""))

                reset_working_directory()
            
            editCateDataRoot.focus_force()

        # Update category data and close.
        def update_and_close() -> None:
            """ Update the data for the selected category and close this dialog box. """
            # Change into DATA/MODS/<path to category>.
            reset_working_directory()
            config.clear()
            config.read('Updater.ini')
            entireModsDir = f"{config.get('Updater', 'GameDirectory')}/DATA/MODS"
            OS.chdir(f"{config.get('Updater', 'GameDirectory')}/DATA/MODS{data[1]}")

            config.clear()
            config.read("category.ini")

            # Old category checksum. If this was changed, we want to update
            # ALL instances of it in the MODS folder on the fly.
            global loadedCategoryData
            oldChecksum = loadedCategoryData[2]
            oldImage = loadedCategoryData[3].replace("\\", "/").split('/')[-1].replace(".img.xen", "")

            config.set('CategoryInfo', 'Name', cateName.get())
            config.set('CategoryInfo', 'Checksum', cateChecksum.get())
            config.set('CategoryInfo', 'Logo', cateImage.get())

            with (open('category.ini', 'w')) as cnf: config.write(cnf)
            print("Updated category config!")

            config.clear()

            global imageFile
            if (not imageFile): imageFile = data[3]
            loadedCategoryData = [cateName.get(), data[1], cateChecksum.get(), imageFile]

            # Was the checksum changed?
            newChecksum = cateChecksum.get()
            newImage = cateImage.get()
            if (oldChecksum != newChecksum):
                # Yes, it was, let's update ALL instances of this checksum
                # on the fly. For the user's convenience!
                OS.chdir(entireModsDir)
                for (dir, _, dirsList) in (OS.walk(".")):
                    for (file) in (dirsList):
                        if (file == 'song.ini') or (file == 'folder.ini'):
                            config.clear()
                            config.read(f"{dir}\\{file}")

                            try:
                                print("Reading tied category, if any...")
                                tiedCat = config.get('SongInfo', 'GameCategory')

                                if (tiedCat == oldChecksum):
                                    config.set('SongInfo', 'Checksum', newChecksum)

                                    with (open(f"{dir}/{file}", 'w')) as cnf: config.write(cnf)

                                    print(f"Updated mod's category checksum from {oldChecksum} to {newChecksum}")

                                else:
                                    print("!! - Wrong category")

                                print("Reading tied image, if any...")
                                tiedIcon = config.get('SongInfo', 'GameIcon')

                                if (tiedIcon == oldImage):
                                    config.set('SongInfo', 'GameIcon', newImage)

                                    with (open(f"{dir}/{file}", 'w')) as cnf: config.write(cnf)

                                    print(f"Updated mod's image name from {oldImage} to {newImage}")

                                else:
                                    print("!! - Wrong image")
                            
                            except:
                                print("No tied category or image, skipping...")

            # Reset working directory and close window.
            reset_working_directory()
            refresh_mods()
            editCateDataRoot.destroy()
    
        # Set up window.
        editCateDataRoot = Toplevel()
        editCateDataRoot.title("Edit Category Data")
        editCateDataRoot.iconbitmap(resource_path('res/menuicons/category/edit_data.ico'))
        editCateDataRoot.config(bg = '#FFFFFF')
        editCateDataRoot.geometry("560x320")
        editCateDataRoot.resizable(False, False)
        editCateDataRoot.focus_force()

        TTK.Style(editCateDataRoot).configure('TButton', background = '#FFFFFF')

        titleHeaderLabel = Label(editCateDataRoot, text = "Edit Category Data: Modify the mod data for this category.", font = FONT_INFO_HEADER, bg = '#FFFFFF', fg = '#000000')
        titleHeaderLabel.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

        cateNameLabel = Label(editCateDataRoot, text = "Name:", bg = "#FFFFFF", fg = '#000000')
        cateNameLabel.grid(row = 1, column = 0, padx = 25, pady = 5, sticky = 'e')

        cateName = TTK.Entry(editCateDataRoot, width = 70)
        cateName.grid(row = 1, column = 1, columnspan = 2, pady = 5, sticky = 'w')
        cateName.insert(END, data[0])

        catePathLabel = Label(editCateDataRoot, text = "Path:", bg = "#FFFFFF", fg = '#000000')
        catePathLabel.grid(row = 2, column = 0, padx = 25, pady = 5, sticky = 'e')

        catePath = Label(editCateDataRoot, width = 60, text = data[1], bg = '#FFFFFF', fg = '#808080', justify = 'left', anchor = 'w', bd = 1, relief = 'solid')
        catePath.grid(row = 2, column = 1, columnspan = 2, pady = 5, sticky = 'w')

        cateChecksumLabel = Label(editCateDataRoot, text = "Checksum:", bg = "#FFFFFF", fg = '#000000')
        cateChecksumLabel.grid(row = 3, column = 0, padx = 25, pady = 5, sticky = 'e')

        cateChecksum = TTK.Entry(editCateDataRoot, width = 25)
        cateChecksum.grid(row = 3, column = 1, columnspan = 2, pady = 5, sticky = 'w')
        cateChecksum.insert(END, data[2])

        cateImageLabel = Label(editCateDataRoot, text = "Image:", bg = "#FFFFFF", fg = '#000000')
        cateImageLabel.grid(row = 4, column = 0, padx = 25, pady = 5, sticky = 'e')

        cateImage = TTK.Entry(editCateDataRoot, width = 47)
        cateImage.grid(row = 4, column = 1, pady = 5, sticky = 'w')
        cateImage.insert(END, data[3].replace("\\", "/").split("/")[-1].replace(".img.xen", ""))

        changeImageButton = TTK.Button(editCateDataRoot, text = "Change Image...", width = 20, command = change_category_image)
        changeImageButton.grid(row = 4, column = 2, padx = 3, pady = 5, sticky = 'w')

        okCloseDialog = TTK.Button(editCateDataRoot, text = "Apply and Close", width = 20, command = update_and_close)
        okCloseDialog.place(x = 426, y = 290)

        editCateDataRoot.mainloop()

    reset_working_directory()

    # -------------------------------
    # WINDOW SETUP
    # -------------------------------
    songCategoryManagerRoot = Toplevel()
    songCategoryManagerRoot.title("Mod Manager: Song & Song Category Manager")
    songCategoryManagerRoot.geometry("1000x780")
    songCategoryManagerRoot.iconbitmap(resource_path('res/icons/music.ico'))
    songCategoryManagerRoot.focus_force()
    songCategoryManagerRoot.resizable(False, False)

    songCatManagerStyle = TTK.Style(songCategoryManagerRoot)
    songCatManagerStyle.configure('TButton', background = '#FFFFFF')
    songCatManagerStyle.configure('TEntry', background = '#FFFFFF')

    # -------------------------------
    # TOP MENU BAR
    # -------------------------------
    reset_working_directory()

    # Base menu bar.
    baseMenu = Menu(songCategoryManagerRoot)
    songCategoryManagerRoot.config(menu = baseMenu)

    # File Menu
    fileMenu = Menu(baseMenu, tearoff = False, activebackground = MENU_HOVER, activeforeground = '#000000')

    NEW_CATE_IMG = ImageTk.PhotoImage(Image.open(resource_path("res/menuicons/file/new_file.ico")))
    OPEN_CATE_IMG = ImageTk.PhotoImage(Image.open(resource_path("res/menuicons/mods/open_mods.ico")))
    IMPORT_CATE_IMG = ImageTk.PhotoImage(Image.open(resource_path("res/menuicons/mods/upload_mod.ico")))
    # -------------------------------
    EXIT_PROGRAM_IMG = ImageTk.PhotoImage(Image.open(resource_path("res/menuicons/file/exit_program.ico")))

    fileMenu.add_command(label = " New Category...", command = make_new_category, image = NEW_CATE_IMG, compound = 'left', accelerator = "(CTRL + N)")
    fileMenu.add_command(label = " Import Category Mod...", image = IMPORT_CATE_IMG, compound = 'left', accelerator = "(CTRL + O)")
    fileMenu.add_separator()
    fileMenu.add_command(label = " Exit", command = songCategoryManagerRoot.destroy, image = EXIT_PROGRAM_IMG, compound = 'left')

    # Mods Menu
    modsMenu = Menu(baseMenu, tearoff = False, activebackground = MENU_HOVER, activeforeground = '#000000')

    REFRESH_MODS_IMG = ImageTk.PhotoImage(Image.open(resource_path("res/menuicons/mods/refresh.ico")))
    INSTALL_MODS_IMG = ImageTk.PhotoImage(Image.open(resource_path("res/menuicons/mods/install_mods.ico")))
    # -------------------------------
    DUPE_SONG_MGR_IMG = ImageTk.PhotoImage(Image.open(resource_path("res/menuicons/mods/copy.ico")))

    modsMenu.add_command(label = " Refresh Mods", command = refresh_mods, image = REFRESH_MODS_IMG, compound = 'left', accelerator = "(CTRL + R)")
    modsMenu.add_command(label = " Install Mods...", image = INSTALL_MODS_IMG, compound = 'left', command = wtde_ask_install_mods, accelerator = "(CTRL + I)")
    modsMenu.add_command(label = " Link Folder to Category...")
    modsMenu.add_separator()
    modsMenu.add_command(label = " Manage Duplicate Song Checksums...", command = duplicate_checksum_manager, image = DUPE_SONG_MGR_IMG, compound = 'left', accelerator = "(CTRL + D)")
    modsMenu.add_separator()
    modsMenu.add_command(label = " Open Mods Folder", command = open_mods_folder, image = OPEN_CATE_IMG, compound = 'left', accelerator = "(CTRL + M)")

    # Song Category Menu
    songCatMenu = Menu(baseMenu, tearoff = False, activebackground = MENU_HOVER, activeforeground = '#000000')

    EDIT_DATA_IMG = ImageTk.PhotoImage(Image.open(resource_path("res/menuicons/category/edit_data.ico")))
    # -------------------------------

    songCatMenu.add_command(label = " Load Category Info", command = load_category_info, accelerator = "(CTRL + L)")
    songCatMenu.add_command(label = " Edit Category Data...", command = lambda: edit_category_meta(loadedCategoryData), image = EDIT_DATA_IMG, compound = 'left', accelerator = "(CTRL + E)")
    songCatMenu.add_command(label = " View Category in File Explorer", command = open_category_folder, image = OPEN_CATE_IMG, compound = 'left', accelerator = "(CTRL + SHIFT + L)")
    songCatMenu.add_separator()
    songCatMenu.add_command(label = " Update Mod Info")
    songCatMenu.add_command(label = " Open Selected Song Folder", image = OPEN_CATE_IMG, compound = 'left', command = open_selected_song_mod_folder)
    songCatMenu.add_command(label = " Unlink Selected Song")

    # Add dropdown menus as cascades.
    baseMenu.add_cascade(label = "File", menu = fileMenu)
    baseMenu.add_cascade(label = "Mods", menu = modsMenu)
    baseMenu.add_cascade(label = "Song Category", menu = songCatMenu)

    # -------------------------------
    # WINDOW PANES
    # -------------------------------
    editorWidgetPane = PanedWindow(songCategoryManagerRoot, bd = 1, relief = 'sunken', bg = 'white')
    editorWidgetPane.pack(fill = 'both', expand = 1)

    # Left pane holds the songs/categories.
    global editorPathsPane
    editorPathsPane = PanedWindow(songCategoryManagerRoot, bd = 1, relief = 'sunken', bg = 'white')
    editorWidgetPane.add(editorPathsPane, width = 300, height = 640)

    # Right pane is the main editing area.
    global editorPreviewPane
    editorPreviewPane = PanedWindow(songCategoryManagerRoot, bd = 1, relief = 'sunken', bg = 'white')
    editorWidgetPane.add(editorPreviewPane, width = 700, height = 640)

    # =======================================================================================================
    #   S O N G       A N D       C A T E G O R Y       L I S T S
    # =======================================================================================================
    # -------------------------------
    # SONG LIST (LEFT SIDE, TOP)
    # -------------------------------
    songListHeaderLabel = Label(editorPathsPane, text = "Song Mods:", bg = '#FFFFFF', fg = '#000000', font = FONT_INFO_HEADER, justify = 'left', anchor = 'w')
    songListHeaderLabel.pack(fill = 'x', anchor = 'w')
    
    songListFrame = Frame(editorPathsPane)
    songListFrame.pack(fill = 'both', expand = 1)

    global songList
    songList = Listbox(songListFrame, bg = '#FFFFFF', relief = 'sunken', bd = 1)
    songList.pack(side = 'left', fill = 'both', expand = 1)

    songListScrollbar = TTK.Scrollbar(songListFrame, orient = 'vertical', command = songList.yview)
    songList.config(yscrollcommand = songListScrollbar.set)
    songListScrollbar.pack(side = 'right', fill = 'y')

    # -------------------------------
    # SONG CATEGORIES (LEFT SIDE, BOTTOM)
    # -------------------------------
    songCatsHeaderLabel = Label(editorPathsPane, text = "Song Categories:", bg = '#FFFFFF', fg = '#000000', font = FONT_INFO_HEADER, justify = 'left', anchor = 'w')
    songCatsHeaderLabel.pack(fill = 'x', anchor = 'w')

    songCatsFrame = Frame(editorPathsPane)
    songCatsFrame.pack(fill = 'both', expand = 1)

    global songCatsList
    songCatsList = Listbox(songCatsFrame, bg = '#FFFFFF', relief = 'sunken', bd = 1)
    songCatsList.pack(side = 'left', fill = 'both', expand = 1)

    songCatsList.bind('<ButtonRelease-1>', load_category_info_e)

    songCatsListScrollbar = TTK.Scrollbar(songCatsFrame, orient = 'vertical', command = songCatsList.yview)
    songCatsList.config(yscrollcommand = songCatsListScrollbar.set)
    songCatsListScrollbar.pack(side = 'right', fill = 'y')

    # =======================================================================================================
    #   C A T E G O R Y       E D I T O R
    # =======================================================================================================

    categoryToolsFrame = Frame(editorPreviewPane, bg = '#FFFFFF')
    categoryToolsFrame.pack(fill = 'x', anchor = 'nw', side = 'top')

    categoryToolsHeader = Label(categoryToolsFrame, text = " Manage Selected Category:", bg = '#FFFFFF', fg = '#000000', font = FONT_INFO_HEADER)
    categoryToolsHeader.grid(row = 0, column = 0, sticky = 'w', columnspan = 999)

    loadSelectedCategoryInfo = TTK.Button(categoryToolsFrame, text = "Refresh Category Info", width = 25, command = load_category_info)
    loadSelectedCategoryInfo.grid(row = 1, column = 0, padx = 10, pady = 3)

    editCategoryData = TTK.Button(categoryToolsFrame, text = "Edit Data...", width = 15, command = lambda: edit_category_meta(loadedCategoryData))
    editCategoryData.grid(row = 1, column = 1, padx = 0, pady = 3)

    viewCateInFolder = TTK.Button(categoryToolsFrame, text = "Open Category Folder", width = 25, command = open_category_folder)
    viewCateInFolder.grid(row = 1, column = 2, padx = 10, pady = 3)

    categoryInfoFrame = Frame(editorPreviewPane, bg = '#FFFFFF')
    categoryInfoFrame.pack(fill = 'x', side = 'top', pady = 3)

    global selectedCatImage
    selectedCatImage = Label(categoryInfoFrame, bg = '#FFFFFF', justify = 'center', width = 10, height = 10)
    selectedCatImage.pack(fill = 'x', anchor = 'n')

    global selectedCatData
    selectedCatData = Label(categoryInfoFrame, text = "Name: N/A\nPath: N/A\nChecksum: N/A\nSongs Tied to Category: N/A", bg = '#FFFFFF', justify = 'left', anchor = 'w')
    selectedCatData.pack(fill = 'x', anchor = 'nw')

    cateSongsInfoFrame = Frame(categoryInfoFrame, bg = '#FFFFFF')
    cateSongsInfoFrame.pack(fill = 'both', expand = 1)

    global selectedCatSongs
    selectedCatSongs = TTK.Treeview(cateSongsInfoFrame, height = 15)

    # Add columns.
    selectedCatSongs['columns'] = ("Song: Artist - Title", "Path", "Checksum")
    selectedCatSongs.column("#0", width = 0, minwidth = 0, stretch = NO)
    selectedCatSongs.column("Song: Artist - Title", anchor = 'w', width = 250, minwidth = 75)
    selectedCatSongs.column("Path", anchor = 'w', width = 250, minwidth = 75)
    selectedCatSongs.column("Checksum", anchor = 'w', width = 160, minwidth = 75)

    # Make the headings.
    selectedCatSongs.heading("#0")
    selectedCatSongs.heading("Song: Artist - Title", text = "Song: Artist - Title", anchor = 'w')
    selectedCatSongs.heading("Path", text = "Path", anchor = 'w')
    selectedCatSongs.heading("Checksum", text = "Checksum", anchor = 'w')

    selectedCatSongs.pack(side = 'left', fill = 'both', expand = 1)

    cateSongsYBar = TTK.Scrollbar(cateSongsInfoFrame, orient = 'vertical', command = selectedCatSongs.yview)
    cateSongsYBar.pack(side = 'right', fill = 'y')

    selectedCatSongs.config(yscrollcommand = cateSongsYBar.set)

    selectedCatSongs.bind('<ButtonRelease-1>', get_selected_song_mod_data)

    # -------------------------------
    # SELECTED SONG MOD FROM TREEVIEW
    # -------------------------------
    barSep1 = TTK.Separator(editorPreviewPane, orient = 'horizontal')
    barSep1.pack(fill = 'x')
    
    selectedTreeInfoFrame = Frame(editorPreviewPane, bg = '#FFFFFF')
    selectedTreeInfoFrame.pack(fill = 'both', expand = 1)

    selectedModHeader = Label(selectedTreeInfoFrame, text = "  Selected Mod Data:", bg = '#FFFFFF', font = FONT_INFO_HEADER)
    selectedModHeader.grid(row = 0, column = 0, pady = 5, columnspan = 999, sticky = 'w')

    selectedSongChecksumLabel = Label(selectedTreeInfoFrame, text = "      Song Checksum: ", bg = '#FFFFFF')
    selectedSongChecksumLabel.grid(row = 1, column = 0, sticky = 'e')

    selectedSongChecksum = Label(selectedTreeInfoFrame, width = 21, text = "", bg = '#FFFFFF', fg = '#808080', justify = 'left', anchor = 'w', bd = 1, relief = 'solid')
    selectedSongChecksum.grid(row = 1, column = 1, columnspan = 2, padx = 5, sticky = 'w')

    selectedSongLinkedCateLabel = Label(selectedTreeInfoFrame, text = "     Game Icon/Logo: ", bg = '#FFFFFF')
    selectedSongLinkedCateLabel.grid(row = 2, column = 0, pady = 5, sticky = 'e')

    GAME_LOGO_IMAGES = [
        "gamelogo_gh1", "gamelogo_gh1dlc", "gamelogo_gh2", "gamelogo_gh2dlc", "gamelogo_gh80s", "gamelogo_gh80sdlc",
        "gamelogo_gh3", "gamelogo_gh3dlc", "gamelogo_gha", "gamelogo_ghadlc", "gamelogo_ghwt", "gamelogo_ghwtdlc",
        "gamelogo_gh5", "gamelogo_gh5dlc", "gamelogo_ghm", "gamelogo_ghmdlc", "gamelogo_ghvh", "gamelogo_ghvhdlc",
        "gamelogo_ghshits", "gamelogo_ghshitsdlc", "gamelogo_ghwor", "gamelogo_ghwordlc", "gamelogo_ghot",
        "gamelogo_ghotdlc", "gamelogo_ghotd", "gamelogo_ghotddlc", "gamelogo_ghotmh", "gamelogo_ghotmhdlc",
        "gamelogo_bh", "gamelogo_bhdlc", "gamelogo_djh", "gamelogo_djhdlc", "gamelogo_djh2", "gamelogo_djh2dlc",
        "gamelogo_thps", "gamelogo_thps2", "gamelogo_thps3", "gamelogo_thps4", "gamelogo_thug", "gamelogo_thug2",
        "gamelogo_thaw", "gamelogo_thpg", "gamelogo_thp8", "gamelogo_sm2000", "gamelogo_apocalypse"
    ]
    """ List of default logo images. """
    selectedSongGameIcon = TTK.Combobox(selectedTreeInfoFrame, width = 16, values = GAME_LOGO_IMAGES)
    selectedSongGameIcon.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'w')

    selectIconIMG = TTK.Button(selectedTreeInfoFrame, text = "...", width = 3, command = select_game_icon)
    selectIconIMG.grid(row = 2, column = 2, sticky = 'w')
                                                                        
    songTitleEntryLabel = Label(selectedTreeInfoFrame, text = "      Title: ", bg = '#FFFFFF')
    songTitleEntryLabel.grid(row = 1, column = 3, padx = 5, sticky = 'e')

    songTitleEntry = TTK.Entry(selectedTreeInfoFrame, width = 20)
    songTitleEntry.grid(row = 1, column = 4, sticky = 'w')

    songArtistEntryLabel = Label(selectedTreeInfoFrame, text = "     Artist: ", bg = '#FFFFFF')
    songArtistEntryLabel.grid(row = 2, column = 3, padx = 5, sticky = 'e')

    songArtistEntry = TTK.Entry(selectedTreeInfoFrame, width = 20)
    songArtistEntry.grid(row = 2, column = 4, sticky = 'w')

    songYearEntryLabel = Label(selectedTreeInfoFrame, text = "       Year: ", bg = '#FFFFFF')
    songYearEntryLabel.grid(row = 1, column = 5, padx = 5, sticky = 'e')

    songYearEntry = TTK.Entry(selectedTreeInfoFrame, width = 10)
    songYearEntry.grid(row = 1, column = 6, columnspan = 2, sticky = 'w')

    songAdvSettings = TTK.Button(selectedTreeInfoFrame, text = "Advanced Settings...", width = 22)
    songAdvSettings.grid(row = 2, column = 6, columnspan = 2)

    # -------------------------------
    # UPDATE RECORD & MOD
    # -------------------------------
    barSep2 = TTK.Separator(editorPreviewPane, orient = 'horizontal')
    barSep2.pack(fill = 'x')

    updateRecordCMDFrame = Frame(editorPreviewPane, bg = '#FFFFFF')
    updateRecordCMDFrame.pack(fill = 'both', expand = 1)

    updateMod = TTK.Button(updateRecordCMDFrame, text = "Update Mod Data", width = 20)
    updateMod.grid(row = 0, column = 0, padx = 5)

    openModDir = TTK.Button(updateRecordCMDFrame, text = "Open Mod Folder", width = 20, command = open_selected_song_mod_folder)
    openModDir.grid(row = 0, column = 1)

    unlinkFromCat = TTK.Button(updateRecordCMDFrame, text = "Unlink From Category", width = 20)
    unlinkFromCat.grid(row = 0, column = 2, padx = 5)

    # -------------------------------
    # ADD STATUS BAR, ENTER MAIN LOOP
    # -------------------------------
    global editorStatusBar
    editorStatusBar = Label(songCategoryManagerRoot, text = "Select a category or song mod from the left to begin editing stuff", anchor = 'w', justify = 'left', relief = 'sunken', bg = '#FFFFFF', width = 145)
    editorStatusBar.pack(fill = 'x')

    global songMods, songCategoryMods
    songMods = get_song_mods()
    songCategoryMods = get_song_categories()
    songCategoryManagerRoot.mainloop()

    # Fix the styling colors.
    config.clear()
    config.read(f"{wtde_find_config()}\\GHWTDE.ini")

    colorToFixTo = "#" + config.get("Launcher", "BGColor")

    # TTK.Style(root).configure("TButton", background = colorToFixTo)
    # TTK.Style(root).configure("TEntry", background = colorToFixTo)

# ===========================================================================================================
# Other Required Functions
# ===========================================================================================================
# Create credits list.
def wtde_add_credits(frame: Frame, csvFile: str, inXPad: int = 30) -> None:
    """ Add the credits from a CSV file to a frame. """
    # Read our CSV file.
    reset_working_directory()

    with (open(csvFile, 'r', newline = "", encoding = 'utf-8')) as file:
        csvReader = CSV.reader(file, delimiter = ',')

        memberList = []

        for (row) in (csvReader): memberList.append(row)

        del memberList[0]

    # For every column and row, make a new label, and add it into the frame.
    # x is the current row
    for (x, array) in (enumerate(memberList)):
        # y is the current column
        for (y, name) in (enumerate(array)):
            # Now add our labels.
            newLabel = Label(frame, text = str(name), bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO)
            newLabel.grid(row = x, column = y, ipadx = inXPad)

# ===========================================================================================================
# Other Required Constants
# 
# These are constants that would otherwise not function in the launcher_constants module.
# ===========================================================================================================
# Read needed data from GHWTDE.ini.
OS.chdir(wtde_find_config())
config.read("GHWTDE.ini")

# Audio buffer length.
AUDIO_BUFFLENS = [aspyr_get_string("Audio.BuffLen", fallbackValue = "2048"), "2048", "4096"]

# List of microphone devices.
if (not config.get('Audio', 'MicDevice')): micSelected = "None"
else: micSelected = config.get('Audio', 'MicDevice')
MIC_LIST = [micSelected] + mic_name_get_list()

# FPS limits.
if (not config.get('Graphics', 'FPSLimit') == '0'): optionNameToUse = config.get('Graphics', 'FPSLimit') + " FPS"
else: optionNameToUse = "Unlimited"
FPS_LIMITS = [optionNameToUse, "15 FPS", "24 FPS", "30 FPS", "60 FPS", "120 FPS", "240 FPS", "Unlimited"]

# Auto launch number of players.
if (not config.get('AutoLaunch', 'Players')): optionNameToUse = "1"
else: optionNameToUse = config.get('AutoLaunch', 'Players')
PLAYERS_OPTIONS = [optionNameToUse, "1", "2", "3", "4"]

# Language list.
LANGUAGES = [
    ["English", 'en'],
    ["Spanish (Español)", 'es'],
    ["Italian (Italiano)", 'it'],
    ["French (Français)", 'fr'],
    ["German (Deutsch)", 'de'],
    ["Japanese (日本語)", 'ja'],
    ["Korean (한국어)", 'ko']
]

# List of holidays.
HOLIDAYS = [
    ["Auto (Based on Date)", ''],
    ["Halloween Theme", 'halloween'],
    ["Christmas Theme", 'xmas'],
    ["Valentine's Day Theme", 'valentine'],
    ["April Fools Day Theme", 'aprilfools'],
    ["No Holidays", 'none']
]

# Venue list along with its zone PAK name.
# List of original venues.
VENUES = [
    ["None", ''],
    ["WT: Phi Psi Kappa", 'z_frathouse'],
    ["WT: Wilted Orchid", 'z_goth'],
    ["WT: Bone Church", 'z_cathedral'],
    ["WT: Pang Tang Bay", 'z_harbor'],
    ["WT: Amoeba Records", 'z_recordstore'],
    ["WT: Tool", 'z_tool'],
    ["WT: Swamp Shack", 'z_bayou'],
    ["WT: Rock Brigade", 'z_military'],
    ["WT: Strutter's Farm", 'z_fairgrounds'],
    ["WT: House of Blues", 'z_hob'],
    ["WT: Ted's Tiki Hut", 'z_hotel'],
    ["WT: Will Heilm's Keep", 'z_castle'],
    ["WT: Recording Studio", 'z_studio2'],
    ["WT: AT&T Park", 'z_ballpark'],
    ["WT: Tesla's Coil", 'z_scifi'],
    ["WT: Ozzfest", 'z_metalfest'],
    ["WT: Times Square", 'z_newyork'],
    ["WT: Sunna's Chariot", 'z_credits'],
    ["SH: Amazon Rain Forest", 'z_amazon'],
    ["SH: The Grand Canyon", 'z_canyon'],
    ["SH: Polar Ice Cap", 'z_icecap'],
    ["SH: London Sewerage System", 'z_london'],
    ["SH: The Sphinx", 'z_sphinx'],
    ["SH: The Great Wall of China", 'z_greatwall'],
    ["SH: The Lost City of Atlantis", 'z_atlantis'],
    ["SH: Quebec City", 'z_quebec'],
    ["GHM: The Forum", 'z_forum'],
    ["GHM: Tushino Airfield", 'z_tushino'],
    ["GHM: Hammersmith Apollo", 'z_mop'],
    ["GHM: Damaged Justice Tour", 'z_justice'],
    ["GHM: The Meadowlands", 'z_meadowlands'],
    ["GHM: Donington Park", 'z_donnington'],
    ["GHM: The Ice Cave", 'z_icecave'],
    ["GHM: Metallica Recording Studio", 'z_soundcheckghm'],
    ["GHM: Metallica Backstage", 'z_studio2ghm'],
    ["VH: Los Angeles", 'z_la_block_party'],
    ["VH: West Hollywood", 'z_starwood'],
    ["VH: Rome", 'z_rome'],
    ["VH: New York City", 'z_s_stage'],
    ["VH: Berlin", 'z_berlin'],
    ["VH: Dallas", 'z_drum_kit'],
    ["VH: London", 'z_londonghvh'],
    ["VH: The Netherlands", 'z_frankenstrat'],
    ["GH5: The 13th Rail", 'z_subway'],
    ["GH5: Club Boson", 'z_lhc'],
    ["GH5: Sideshow", 'z_freakshow'],
    ["GH5: O'Connell's Corner", 'z_dublin'],
    ["GH5: Guitarhenge", 'z_carhenge'],
    ["GH5: Electric Honky Tonk", 'z_nashville'],
    ["GH5: Calavera Square", 'z_mexicocity'],
    ["GH5: Hypersphere", 'z_hyperspherewt'],
    ["BH: Mall of Fame Tour", 'z_mall'],
    ["BH: Club La Noza", 'z_cabo'],
    ["BH: Summer Park Festival", 'z_centralpark'],
    ["BH: Harajuku", 'z_tokyo'],
    ["BH: Everpop Awards", 'z_awardshow'],
    ["BH: AMP Orbiter", 'z_space'],
    ["III: Desert Rock Tour", 'z_wikker'],
    ["III: Lou's Inferno", 'z_hell']

# List of modded venues.
] + venueModInfo
"""
`list[list[str]]`: List of string lists, 2 elements each.
- The first item in the list is the actual zone's name.
- The second item is the zone's PAK name.
"""

# Note styles and their respective checksums.
NOTE_STYLES = [
    ["GHWT Notes (Default)", "ghwt"],
    ["GH3 Notes", "gh3"],
    ["GH: WOR Notes", "ghwor"],
    ["Flat Notes", "flat"]

# List of modded gems.
] + gemModInfo
"""
`list[list[str]]`: List of string lists, 2 elements each.
- The first item in the list is the actual note style's name.
- The second item is the note style's checksum or file name.
"""

# Note theme colors.
NOTE_THEMES = [
    ["Normal Color (Default)", "standard_gems"],
    ["Pink", "pink_gems"],
    ["Stealth", "stealth_gems"],
    ["Eggs 'N Bacon", "Eggs_N_Bacon_gems"],
    ["Old Glory", "old_glory_gems"],
    ["Solid Gold", "solid_gold_gems"],
    ["Platinum", "platinum_gems"],
    ["Diabolic", "diabolic_gems"],
    ["Toxic Waste", "toxic_waste_gems"],
    ["Black", "black_gems"],
    ["Pastel", "pastel_gems"],
    ["Dark", "dark_gems"],
    ["Outline", "outline_gems"],
    ["GH1 Prototype", "gh1proto_gems"],
    ["Pure Green", "pure_green"],
    ["Pure Red", "pure_red"],
    ["Pure Yellow", "pure_yellow"],
    ["Pure Blue", "pure_blue"],
    ["Pure Orange", "pure_orange"], 
    ["Candy Cane", "candy_cane"],
    ["Ghoulish", "halloween"]
]

# Song intro styles.
INTRO_STYLES = [
    ["Normal GHWT (Default)", "ghwt"],
    ["Guitar Hero III", "gh3"],
    ["Guitar Hero III (Left)", "gh3_left"],
    ["GH: Smash Hits", "ghshits"],
    ["GH: Metallica", "ghm"],
    ["GH: Van Halen", "ghvh"],
    ["Guitar Hero 5", "gh5"],
    ["Band Hero", "bh"],
    ["GH: Warriors of Rock", "ghwor"],
    ["Auto (Based on Setlist)", "auto"]
]

# The checksums used for every game.
GAME_NAME_CHECKSUMS = [
    ["GH World Tour Definitive Editon", "wtde"],
    ["Guitar Hero World Tour", "ghwt"],
    ["Normal GHWT (Default)", "ghwt"],
    ["GHWT (Default)", "none"],
    ["Guitar Hero World Tour (Beta)", "ghwt_beta"],
    ["Guitar Hero World Tour (Wii)", "ghwt_wii"],
    ["Guitar Hero World Tour (Wii, HD)", "ghwt_wii_hd"],
    ["Guitar Hero II", "gh2"],
    ["Guitar Hero III", "gh3"],
    ["Guitar Hero III (Left)", "gh3_left"],
    ["Guitar Hero III (Console)", "gh3_console"],
    ["Guitar Hero Metallica", "ghm"],
    ["GH: Metallica", "ghm"],
    ["Guitar Hero Smash Hits", "ghshits"],
    ["GH: Smash Hits", "ghshits"],
    ["Guitar Hero Van Halen", "ghvh"],
    ["GH: Van Halen", "ghvh"],
    ["Guitar Hero 5", "gh5"],
    ["Guitar Hero Warriors of Rock", "ghwor"],
    ["GH: Warriors of Rock", "ghwor"],
    ["Band Hero", "bh"],
    ["Auto (Based on Setlist)", "auto"]
]

# Time of Day profiles.
TOD_PROFILES = [
    ["Retro (Default)", 'ghwt'],
    ["Modern", 'ghvh'],
    ['Black & White', 'bw'],
    ["Psychadelic", 'psych'],
    ["Dusty Orange", 'dustyorange'],
    ["Spooky", 'spooky']
]

# Strum animations.
BASS_STRUM_ANIMS = [
    ["GH: World Tour (Default)", "none"],
    ["Guitar Hero: Metallica", "ghm"]
]

# Loading screen themes.
LOADING_THEMES = [
    ["GHWT: DE (Default)", 'wtde'],
    ["Guitar Hero II", 'gh2'],
    ["Guitar Hero III", 'gh3'],
    ["Guitar Hero III (Console)", 'gh3_console'],
    ["Guitar Hero Aerosmith", 'gha'],
    ["GH World Tour", 'ghwt'],
    ["GH Smash Hits", 'ghshits'],
    ["Guitar Hero Metallica", 'ghm'],
    ["Guitar Hero Van Halen", 'ghvh']
]

# User helper themes.
USER_HELPER_THEMES = [
    ["GHWT: DE (Default)", 'wtde'],
    ["GH World Tour", 'ghwt'],
    ["GH World Tour (Beta)", 'ghwt_beta'],
    ["GH World Tour (Wii)", 'ghwt_wii'],
    ["GH World Tour (Wii, HD)", 'ghwt_wii_hd']
]

# HUD themes.
HUD_THEMES = [
    ["GH World Tour + (Default)", 'ghwt_plus'],
    ["GH World Tour", 'ghwt'],
    ["Guitar Hero: Metallica", 'ghm'],
    ["Guitar Hero: Smash Hits", 'ghsh'],
    ["Guitar Hero: Van Halen", 'ghvh']
]

# Tap trail themes.
TAP_TRAIL_THEMES = [
    ["GH World Tour (Default)", 'ghwt'],
    ["Guitar Hero Metallica", 'ghm'],
    ["No Tap Trail", 'none']
]

# Hit flame themes.
HIT_FLAME_THEMES = [
    ["GH World Tour (Default)", 'ghwt'],
    ["GH Warriors of Rock", 'wor'],
    ["Guitar Hero II", 'gh2'],
    ["No Hit Flames", 'none']
]

# Depth of Field qualities.
DOF_QUALITIES = [
    ["Off", '0'],
    ["Standard", '1'],
    ["High", '2']
]

# Flare styles.
FLARE_STYLES = [
    ["GHWT: DE (Default)", 'wtde'],
    ["GH World Tour", 'ghwt'],
    ["Guitar Hero III", 'gh3'],
    ["No Flares", 'none']
]

# Difficulty names/symbols (QPO).
QPO_DIFFICULTIES = [
    ["Beginner", 'easy_rhythm'],
    ["Easy", 'easy'],
    ["Medium", 'normal'],
    ["Hard", 'hard'],
    ["Expert", 'expert']
]

# Default song checksums.
DEFAULT_SONGS = [
    "aboutagirl",
    "aggro",
    "americanwoman",
    "antisocial",
    "areyougonnagomyway",
    "assassin",
    "bandontherun",
    "beatit",
    "beautifuldisaster",
    "bossted",
    "dlc1",
    "bosszakk",
    "dlc2"
    "byob",
    "crazytrain",
    "dammit",
    "demolitionman",
    "doitagain",
    "escueladecalor",
    "everlong",
    "eyeofthetiger",
    "feelthepain",
    "floaton",
    "freakonaleash",
    "goodgod",
    "goyourownway",
    "hailtothefreaks",
    "heartbreaker",
    "heymanniceshot",
    "hollywoodnights",
    "hotelcalifornia",
    "hotforteacher",
    "kickoutthejams",
    "labamba",
    "lazyeye",
    "livingonaprayer",
    "lovemetwotimes",
    "loveremovalmachine",
    "lovespreads",
    "lvialviaquez",
    "miserybusiness",
    "monsoon",
    "mountainsong",
    "mrcrowley",
    "nevertoolate",
    "nosleeptillbrooklyn",
    "nuvole",
    "obstacle1",
    "onearmedscissor",
    "onewayoranother",
    "ontheroadagain",
    "ourtruth",
    "overkill",
    "parabola",
    "prettyvacant",
    "prisonerofsociety",
    "pullmeunder",
    "purplehaze",
    "ramblinman",
    "rebelyell",
    "reedthroughlabor",
    "rooftops",
    "santeria",
    "satchboogie",
    "schism",
    "screamaimfire",
    "shiver",
    "somemightsay",
    "souldoubt",
    "spiderwebs",
    "stillborn",
    "stranglehold",
    "sweethomealabama",
    "thejoker",
    "thekill",
    "themiddle",
    "theoneilove",
    "today",
    "toomuchtooyoung",
    "toyboy",
    "trappedunderice",
    "uparoundthebend",
    "vicarious",
    "vinternoll2",
    "weaponofchoice",
    "whativedone",
    "windcriesmary",
    "youregonnasayyeah"
]

# Player instruments.
INSTRUMENTS = ["Lead Guitar - PART GUITAR", "Bass Guitar - PART BASS", "Drums - PART DRUMS", "Vocals - PART VOCALS"]
P1_INSTRUMENTS = [auto_inst_diff('Part')] + INSTRUMENTS
P2_INSTRUMENTS = [auto_inst_diff('Part2')] + INSTRUMENTS
P3_INSTRUMENTS = [auto_inst_diff('Part3')] + INSTRUMENTS
P4_INSTRUMENTS = [auto_inst_diff('Part4')] + INSTRUMENTS

# Player difficulties.
DIFFICULTIES = ["Beginner", "Easy", "Medium", "Hard", "Expert"]
P1_DIFFICULTIES = [auto_inst_diff('Difficulty')] + DIFFICULTIES
P2_DIFFICULTIES = [auto_inst_diff('Difficulty2')] + DIFFICULTIES
P3_DIFFICULTIES = [auto_inst_diff('Difficulty3')] + DIFFICULTIES
P4_DIFFICULTIES = [auto_inst_diff('Difficulty4')] + DIFFICULTIES

# The latest version of GHWT: DE, taken from the hash list.
if (is_connected(HASH_LIST)): hashListContent = str(REQ.get(HASH_LIST).content).split("\\n")
else: hashListContent = ["", "??? (connect to internet)"]
WTDE_LATEST_VERSION = hashListContent[1]
""" The latest version of GHWT: DE. If the version number can't be retrieved, just say we can't get the version. """

# After finished, read AspyrConfig data.
reset_working_directory()

# Auto login options.
if (aspyr_get_string("AutoLogin", fallbackValue = "PROMPT").title() == "Prompt"): autoLoginFirst = "Always Prompt"
else: autoLoginFirst = aspyr_get_string("AutoLogin").title()
AUTO_LOGIN_OPTIONS = [autoLoginFirst, "On", "Always Prompt", "Off"]

reset_working_directory()
config.read(f"{wtde_find_config()}\\GHWTDE.ini")

BG_COLOR = "#" + config.get("Launcher", "BGColor")
""" The global background color. """

FG_COLOR = "#" + config.get("Launcher", "FGColor")
""" Text color. """

# Reset the colors of the root window.
def reset_colors(root: Tk | Toplevel) -> None:
    """ Reset the color of the given root window. """
    TTK.Style(root).configure('TButton', background = BG_COLOR)
    TTK.Scale(root).configure('TEntry', background = BG_COLOR)

FONT = config.get("Launcher", "TextFont")
""" The main text font everything uses. """

FONT_SIZE = 9
""" The main font size. """

FONT_INFO = (FONT, FONT_SIZE)
""" Tuple containing the various font information for the program. """

FONT_INFO_BOLD = (FONT, FONT_SIZE, 'bold')
""" Same info tuple as `FONT_INFO`, but for bold text. """

FONT_INFO_HEADER = (FONT, 10)
""" Font information for headers (meant for more important/pronounced text). """

FONT_INFO_FOOTER = (FONT, 11)
""" Font information for the footer (text along the bottom of the program). """