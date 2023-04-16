# ================================================================================================================= #
#                                                                                                                   #
#    __          _________ _____  ______     _              _    _ _   _  _____ _    _ ______ _____                 #
#    \ \        / /__   __|  __ \|  ____|   | |        /\  | |  | | \ | |/ ____| |  | |  ____|  __ \  _     _       #
#     \ \  /\  / /   | |  | |  | | |__      | |       /  \ | |  | |  \| | |    | |__| | |__  | |__) || |_ _| |_     #
#      \ \/  \/ /    | |  | |  | |  __|     | |      / /\ \| |  | | . ` | |    |  __  |  __| |  _  /_   _|_   _|    #
#       \  /\  /     | |  | |__| | |____    | |____ / ____ \ |__| | |\  | |____| |  | | |____| | \ \ |_|   |_|      #
#        \/  \/      |_|  |_____/|______|   |______/_/    \_\____/|_| \_|\_____|_|  |_|______|_|  \_\               #
#                                                                                                                   #
#                             GH World Tour: Definitive Edition Launcher++ Version 2.0                              #
#                                                                                                                   #
#          Coded by IMF24                Guitar Hero World Tour: Definitive Edition by Fretworks EST. 2021          #
#                                                                                                                   #
#                                    Updater Coded by Zedek the Plague Doctor ™                                     #
# ================================================================================================================= #
# Import required modules.
from tkinter import *
from tkinter import ttk as TTK, messagebox as MSG, filedialog as FD
from tkhtmlview import HTMLLabel
from tkinter.font import *
from tktooltip import ToolTip
from launcher_functions import *
from launcher_constants import *
from PIL import Image, ImageTk
import webbrowser as WEB
import os as OS
import sys as SYS

debug_add_entry("[init] All modules imported!")

verify_updater_config()

# ===========================================================================================================
# Save & Load Config Settings
# 
# The functions for handling the saving and loading of configuration settings.
# ===========================================================================================================
# Save and Load Configuration
# ===========================================================================================================
# Save WTDE config settings.
def wtde_save_config(run: bool = False) -> None:
    """ Using BS4 and ConfigParser, saves all configuration settings from the launcher's widgets into both GHWTDE.ini and AspyrConfig.xml as needed. """
    if (autoLaunchEnabled.get() == '1'):
        AUTO_ENABLED_ASK_BACKUP = "You have Auto Launch functionality enabled. Due to this, you might risk losing your save data.\n" \
                                  "Do you want to create a backup of your save data?"
        
        if (MSG.askyesno("Back Up Save?", AUTO_ENABLED_ASK_BACKUP)): wtde_backup_save()

    # ====================================================================
    # GHWTDE.ini Settings
    # ====================================================================
    # Read our GHWTDE.ini file. Also clear out the ConfigParser variable.
    OS.chdir(wtde_find_config())
    config.clear()
    config.read("GHWTDE.ini")

    # ==================================
    # General Settings
    # ==================================
    config.set("Config", "RichPresence", GeneralSettings.richPresence.get())
    config.set("Config", "AllowHolidays", GeneralSettings.allowHolidays.get())
    config.set("Audio", "WhammyPitchShift", GeneralSettings.whammyPitchShift.get())
    config.set("Config", "SongSpecificIntros", GeneralSettings.songSpecificIntros.get())
    config.set("Config", "Holiday", holiday_name('checksum', GeneralSettings.holiday.get()))
    config.set("Config", "Language", language_name('checksum', GeneralSettings.language.get()))

    # Main Menu Toggles
    config.set("Config", "UseCareerOption", GeneralSettings.useCareerOption.get())
    config.set("Config", "UseQuickplayOption", GeneralSettings.useQuickplayOption.get())
    config.set("Config", "UseHeadToHeadOption", GeneralSettings.useHeadToHeadOption.get())
    config.set("Config", "UseOnlineOption", GeneralSettings.useOnlineOption.get())
    config.set("Config", "UseMusicStudioOption", GeneralSettings.useMusicStudioOption.get())
    config.set("Config", "UseCAROption", GeneralSettings.useCAROption.get())
    config.set("Config", "UseOptionsOption", GeneralSettings.useOptionsOption.get())
    config.set("Config", "UseQuitOption", GeneralSettings.useQuitOption.get())

    # ==================================
    # Input Settings
    # ==================================
    config.set("Audio", "MicDevice", InputSettings.micDevice.get())
    config.set("Debug", "DisableInputHack", InputSettings.disableInputHack.get())
    config.set("Audio", "VocalAdjustment", InputSettings.inputMicSettingsADelayEntry.get())

    # ==================================
    # Graphics Settings
    # ==================================
    config.set("Graphics", "UseNativeRes", GraphicsSettings.useNativeRes.get())
    config.set("Graphics", "DisableVSync", GraphicsSettings.disableVSync.get())
    
    if (GraphicsSettings.fpsLimit.get() != "Unlimited"): config.set("Graphics", "FPSLimit", GraphicsSettings.fpsLimit.get().split(" ")[0])
    else: config.set("Graphics", "FPSLimit", "0")

    config.set("Graphics", "HitSparks", GraphicsSettings.hitSparks.get())
    config.set("Graphics", "DisableDOF", GraphicsSettings.disableDOF.get())
    config.set("Graphics", "WindowedMode", GraphicsSettings.windowedMode.get())
    config.set("Graphics", "Borderless", GraphicsSettings.borderless.get())
    config.set("Graphics", "DisableBloom", GraphicsSettings.disableBloom.get())
    config.set("Graphics", "ColorFilters", GraphicsSettings.colorFilters.get())
    config.set("Graphics", "AntiAliasing", GraphicsSettings.antiAliasing.get())
    config.set("Graphics", "RenderParticles", GraphicsSettings.renderParticles.get())
    config.set("Graphics", "RenderGeoms", GraphicsSettings.renderGeoms.get())
    config.set("Graphics", "RenderInstances", GraphicsSettings.renderInstances.get())
    config.set("Graphics", "DrawProjectors", GraphicsSettings.drawProjectors.get())
    config.set("Graphics", "Render2D", GraphicsSettings.render2D.get())
    config.set("Graphics", "RenderScreenFX", GraphicsSettings.renderScreenFX.get())
    config.set("Graphics", "BlackStage", GraphicsSettings.blackStage.get())
    config.set("Graphics", "HideBand", GraphicsSettings.hideBand.get())
    config.set("Graphics", "HideInstruments", GraphicsSettings.hideInstruments.get())
    config.set("Graphics", "ApplyBandName", GraphicsSettings.applyBandName.get())
    config.set("Graphics", "ApplyBandLogo", GraphicsSettings.applyBandLogo.get())

    config.set("Graphics", "GemTheme", note_info('checksum', 'style', GraphicsSettings.gemTheme.get()))
    config.set("Graphics", "GemColors", note_info('checksum', 'theme', GraphicsSettings.gemColors.get()))
    config.set("Graphics", "SongIntroStyle", intro_style('checksum', GraphicsSettings.songIntroStyle.get()))
    config.set("Graphics", "DefaultTODProfile", tod_profile('checksum', GraphicsSettings.defaultTODProfile.get()))

    # ==================================
    # Band Settings
    # ==================================
    config.set("Band", "PreferredGuitarist", BandSettings.bandPrefGuitarist.get())
    config.set("Band", "PreferredGuitaristHighway", BandSettings.bandPrefGuitaristHwy.get())

    config.set("Band", "PreferredBassist", BandSettings.bandPrefBassist.get())
    config.set("Band", "PreferredBassist", BandSettings.bandPrefBassistHwy.get())

    config.set("Band", "PreferredDrummer", BandSettings.bandPrefDrummer.get())
    config.set("Band", "PreferredDrummerHighway", BandSettings.bandPrefDrummerHwy.get())

    config.set("Band", "PreferredSinger", BandSettings.bandPrefSinger.get())

    config.set("Band", "PreferredStage", auto_save_venue(BandSettings.bandPrefStage.get()))

    config.set("Band", "GuitarStrumAnim", strum_anim('checksum', BandSettings.guitarStrumAnim.get()))
    config.set("Band", "BassStrumAnim", strum_anim('checksum', BandSettings.bassStrumAnim.get()))

    # ==================================
    # Auto Launch Settings
    # ==================================
    config.set("AutoLaunch", "Enabled", autoLaunchEnabled.get())

    config.set("AutoLaunch", "HideHUD", AutoLaunch.AutoLaunch_General.autoHideHUD.get())
    config.set("AutoLaunch", "Players", autoPlayerCount.get())
    config.set("AutoLaunch", "Venue", auto_save_venue(AutoLaunch.AutoLaunch_General.autoVenue.get()))
    config.set("AutoLaunch", "Song", AutoLaunch.AutoLaunch_General.autoSongIDEntry.get())

    config.set("AutoLaunch", "Part", auto_get_part(AutoLaunch.AutoLaunch_General.autoP1Instrument.get()))
    config.set("AutoLaunch", "Part2", auto_get_part(AutoLaunch.AutoLaunch_General.autoP2Instrument.get()))
    config.set("AutoLaunch", "Part3", auto_get_part(AutoLaunch.AutoLaunch_General.autoP3Instrument.get()))
    config.set("AutoLaunch", "Part4", auto_get_part(AutoLaunch.AutoLaunch_General.autoP4Instrument.get()))

    config.set("AutoLaunch", "Difficulty", auto_get_diff(AutoLaunch.AutoLaunch_General.autoP1Difficulty.get()))
    config.set("AutoLaunch", "Difficulty2", auto_get_diff(AutoLaunch.AutoLaunch_General.autoP2Difficulty.get()))
    config.set("AutoLaunch", "Difficulty3", auto_get_diff(AutoLaunch.AutoLaunch_General.autoP3Difficulty.get()))
    config.set("AutoLaunch", "Difficulty4", auto_get_diff(AutoLaunch.AutoLaunch_General.autoP4Difficulty.get()))

    config.set("AutoLaunch", "Bot", AutoLaunch.AutoLaunch_General.autoP1Bot.get())
    config.set("AutoLaunch", "Bot2", AutoLaunch.AutoLaunch_General.autoP2Bot.get())
    config.set("AutoLaunch", "Bot3", AutoLaunch.AutoLaunch_General.autoP3Bot.get())
    config.set("AutoLaunch", "Bot4", AutoLaunch.AutoLaunch_General.autoP4Bot.get())

    config.set("AutoLaunch", "RawLoad", AutoLaunch.AutoLaunch_Advanced.autoRawLoad.get())
    config.set("AutoLaunch", "SongTime", AutoLaunch.AutoLaunch_Advanced.autoSongTime.get())

    # ==================================
    # Debug Settings
    # ==================================
    config.set("Debug", "FixNoteLimit", DebugSettings.fixNoteLimit.get())
    config.set("Debug", "FixMemoryHandler", DebugSettings.fixMemoryHandler.get())
    config.set("Logger", "Console", DebugSettings.loggerConsole.get())
    config.set("Logger", "WriteFile", DebugSettings.writeFile.get())
    config.set("Logger", "DisableSongLogging", DebugSettings.disableSongLogging.get())
    config.set("Logger", "DebugDLCSync", DebugSettings.debugDLCSync.get())
    config.set("Debug", "FixFSBObjects", DebugSettings.fixFSBObjects.get())
    config.set("Debug", "ExtraOptimizedSaves", DebugSettings.extraOptimizedSaves.get())
    config.set("Debug", "DebugSaves", DebugSettings.debugSaves.get())
    config.set("Logger", "ShowWarnings", DebugSettings.showWarnings.get())

    # Write all changes to our GHWTDE.ini file.
    with (open("GHWTDE.ini", 'w')) as cnf: config.write(cnf)

    # ====================================================================
    # AspyrConfig Settings
    # ====================================================================
    # Read our AspyrConfig.xml.
    OS.chdir(aspyr_get_config())
    with (open("AspyrConfig.xml", 'rb')) as xml: aspyrConfigDataXML = xml.read()

    # Run BS4 on the XML data.
    aspyrConfigDataBS = BeautifulSoup(aspyrConfigDataXML, 'xml', from_encoding = 'utf-8')

    # ==================================
    # General Settings
    # ==================================
    generalAudioBuffLenXML = aspyrConfigDataBS.find('s', {"id": "Audio.BuffLen"})
    generalAudioBuffLenXML.string = GeneralSettings.audioBuffLen.get()

    generalAutoLoginXML = aspyrConfigDataBS.find('s', {"id": "AutoLogin"})
    try:
        autoLoginOptionTextList = GeneralSettings.autoLogin.get().split(" ")

        if (len(autoLoginOptionTextList) > 0): 
            generalAutoLoginXML.string = autoLoginOptionTextList[-1].upper()

    except: generalAutoLoginXML.string = GeneralSettings.autoLogin.get().upper()

    # ==================================
    # Input Settings
    # ==================================
    # ================================== GUITAR INPUTS ================================== #
    GUITAR_INPUT_WIDGETS = [InputSettings.inputKeyGuitarGreenEntry, InputSettings.inputKeyGuitarRedEntry, InputSettings.inputKeyGuitarYellowEntry,
                            InputSettings.inputKeyGuitarBlueEntry, InputSettings.inputKeyGuitarOrangeEntry, InputSettings.inputKeyGuitarSPEntry,
                            InputSettings.inputKeyGuitarStartEntry, InputSettings.inputKeyGuitarSelectEntry, InputSettings.inputKeyGuitarCancelEntry,
                            InputSettings.inputKeyGuitarWhammyEntry, InputSettings.inputKeyGuitarUpEntry, InputSettings.inputKeyGuitarDownEntry,
                            InputSettings.inputKeyGuitarLeftEntry, InputSettings.inputKeyGuitarRightEntry]
    
    GUITAR_INPUT_BINDINGS = ["GREEN", "RED", "YELLOW", "BLUE", "ORANGE", "STAR", "START", "BACK", "CANCEL", "WHAMMY", "UP", "DOWN", "LEFT", "RIGHT"]

    keyGuitarStringXML = aspyrConfigDataBS.find('s', {"id": "Keyboard_Guitar"})
    keyGuitarStringXML.string = aspyr_key_encode(GUITAR_INPUT_WIDGETS, GUITAR_INPUT_BINDINGS)

    # ================================== DRUM INPUTS ================================== #
    DRUMS_INPUT_WIDGETS = [InputSettings.inputKeyDrumsRedEntry, InputSettings.inputKeyDrumsYellowEntry, InputSettings.inputKeyDrumsBlueEntry,
                           InputSettings.inputKeyDrumsOrangeEntry, InputSettings.inputKeyDrumsGreenEntry, InputSettings.inputKeyDrumsKickEntry,
                           InputSettings.inputKeyDrumsStartEntry, InputSettings.inputKeyDrumsSelectEntry, InputSettings.inputKeyDrumsCancelEntry,
                           InputSettings.inputKeyDrumsUpEntry, InputSettings.inputKeyDrumsDownEntry]
    
    DRUMS_INPUT_BINDINGS = ["RED", "YELLOW", "BLUE", "ORANGE", "GREEN", "KICK", "START", "BACK", "CANCEL", "UP", "DOWN"]

    keyDrumStringXML = aspyrConfigDataBS.find('s', {"id": "Keyboard_Drum"})
    keyDrumStringXML.string = aspyr_key_encode(DRUMS_INPUT_WIDGETS, DRUMS_INPUT_BINDINGS)

    # ================================== MIC INPUTS ================================== #
    MIC_INPUT_WIDGETS = [InputSettings.inputKeyMicGreenEntry, InputSettings.inputKeyMicRedEntry, InputSettings.inputKeyMicYellowEntry,
                         InputSettings.inputKeyMicBlueEntry, InputSettings.inputKeyMicOrangeEntry, InputSettings.inputKeyMicStartEntry,
                         InputSettings.inputKeyMicSelectEntry, InputSettings.inputKeyMicCancelEntry, InputSettings.inputKeyMicUpEntry,
                         InputSettings.inputKeyMicDownEntry]
    
    MIC_INPUT_BINDINGS = ["GREEN", "RED", "YELLOW", "BLUE", "ORANGE", "START", "BACK", "CANCEL", "UP", "DOWN"]

    keyMicStringXML = aspyrConfigDataBS.find('s', {"id": "Keyboard_Mic"})
    keyMicStringXML.string = aspyr_key_encode(MIC_INPUT_WIDGETS, MIC_INPUT_BINDINGS) + "MIC_VOL_DOWN 273 329 "

    # ================================== MENU INPUTS ================================== #
    MENU_INPUT_WIDGETS = [InputSettings.inputKeyMenuGreenEntry, InputSettings.inputKeyMenuRedEntry, InputSettings.inputKeyMenuYellowEntry,
                          InputSettings.inputKeyMenuBlueEntry, InputSettings.inputKeyMenuOrangeEntry, InputSettings.inputKeyMenuStartEntry,
                          InputSettings.inputKeyMenuSelectEntry, InputSettings.inputKeyMenuCancelEntry, InputSettings.inputKeyMenuWhammyEntry,
                          InputSettings.inputKeyMenuKickEntry, InputSettings.inputKeyMenuUpEntry, InputSettings.inputKeyMenuDownEntry,
                          InputSettings.inputKeyMenuLeftEntry, InputSettings.inputKeyMenuRightEntry]
    
    MENU_INPUT_BINDINGS = ["GREEN", "RED", "YELLOW", "BLUE", "ORANGE", "START", "BACK", "CANCEL", "WHAMMY", "KICK", "UP", "DOWN", "LEFT", "RIGHT"]

    keyMenuStringXML = aspyrConfigDataBS.find('s', {"id": "Keyboard_Menu"})
    keyMenuStringXML.string = aspyr_key_encode(MENU_INPUT_WIDGETS, MENU_INPUT_BINDINGS)

    # ==================================
    # Graphics Settings
    # ==================================
    graphicsResWXML = aspyrConfigDataBS.find('s', {"id": "Video.Width"})
    graphicsResHXML = aspyrConfigDataBS.find('s', {"id": "Video.Height"})

    if (GraphicsSettings.useNativeRes.get() == "0"):
        graphicsResWXML.string = GraphicsSettings.graphicsResWEntry.get()
        graphicsResHXML.string = GraphicsSettings.graphicsResHEntry.get()

    else:
        graphicsResWXML.string = str(get_screen_resolution()[0])
        graphicsResHXML.string = str(get_screen_resolution()[1])

    # Make sure our working directory is correct.
    OS.chdir(aspyr_get_config())

    # Write all changes to our AspyrConfig.xml file.
    with (open("AspyrConfig.xml", 'w', encoding = "utf-8")) as xml: xml.write(str(aspyrConfigDataBS))

    # Reset our working directory directory.
    reset_working_directory()

    # If the 'run' argument was enabled, close the launcher and run GHWT: DE.
    if (run):
        # Destroy the window.
        root.destroy()

        # Read where the game is installed.
        config.read("Updater.ini")
        OS.chdir(config.get("Updater", "GameDirectory"))

        # Run the game.
        OS.system(".\\GHWT_Definitive.exe")

# Load WTDE config settings.
def wtde_load_config() -> None:
    """ Using BS4 and ConfigParser, imports all configuration settings from GHWTDE.ini and AspyrConfig.xml. """
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
    GeneralSettings.songSpecificIntros.set(config.get("Config", "SongSpecificIntros"))
    GeneralSettings.language.set(language_name('option', config.get("Config", "Language")))
    GeneralSettings.holiday.set(holiday_name('option', config.get("Config", "Holiday")))

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
    GraphicsSettings.hitSparks.set(config.get('Graphics', 'HitSparks'))
    GraphicsSettings.disableDOF.set(config.get('Graphics', 'DisableDOF'))
    GraphicsSettings.windowedMode.set(config.get('Graphics', 'WindowedMode'))
    GraphicsSettings.borderless.set(config.get('Graphics', 'Borderless'))
    GraphicsSettings.disableBloom.set(config.get('Graphics', 'DisableBloom'))
    GraphicsSettings.colorFilters.set(config.get('Graphics', 'ColorFilters'))
    GraphicsSettings.antiAliasing.set(config.get('Graphics', 'AntiAliasing'))
    GraphicsSettings.renderParticles.set(config.get('Graphics', 'RenderParticles'))
    GraphicsSettings.renderGeoms.set(config.get('Graphics', 'RenderGeoms'))
    GraphicsSettings.renderInstances.set(config.get('Graphics', 'RenderInstances'))
    GraphicsSettings.drawProjectors.set(config.get('Graphics', 'DrawProjectors'))
    GraphicsSettings.render2D.set(config.get('Graphics', 'Render2D'))
    GraphicsSettings.renderScreenFX.set(config.get('Graphics', 'RenderScreenFX'))
    GraphicsSettings.blackStage.set(config.get('Graphics', 'BlackStage'))
    GraphicsSettings.hideBand.set(config.get('Graphics', 'HideBand'))
    GraphicsSettings.hideInstruments.set(config.get('Graphics', 'HideInstruments'))
    GraphicsSettings.applyBandName.set(config.get('Graphics', 'ApplyBandName'))
    GraphicsSettings.applyBandLogo.set(config.get('Graphics', 'ApplyBandLogo'))

    GraphicsSettings.gemTheme.set(note_info('option', 'style', config.get('Graphics', 'GemTheme')))
    GraphicsSettings.gemColors.set(note_info('option', 'theme', config.get('Graphics', 'GemColors')))
    GraphicsSettings.songIntroStyle.set(intro_style('option', config.get('Graphics', 'SongIntroStyle')))
    GraphicsSettings.defaultTODProfile.set(tod_profile('option', config.get('Graphics', 'DefaultTODProfile')))

    # ==================================
    # Band Settings
    # ==================================
    BandSettings.bandPrefGuitarist.insert(0, config.get('Band', 'PreferredGuitarist'))
    BandSettings.bandPrefGuitaristHwy.insert(0, config.get('Band', 'PreferredGuitaristHighway'))
    
    BandSettings.bandPrefBassist.insert(0, config.get('Band', 'PreferredBassist'))
    BandSettings.bandPrefBassistHwy.insert(0, config.get('Band', 'PreferredBassistHighway'))
    
    BandSettings.bandPrefDrummer.insert(0, config.get('Band', 'PreferredDrummer'))
    BandSettings.bandPrefDrummerHwy.insert(0, config.get('Band', 'PreferredDrummerHighway'))
    
    BandSettings.bandPrefSinger.insert(0, config.get('Band', 'PreferredSinger'))
    
    BandSettings.bandPrefStage.insert(0, auto_get_venue(config.get('Band', 'PreferredStage')))

    BandSettings.guitarStrumAnim.set(strum_anim('option', config.get('Band', 'GuitarStrumAnim')))
    BandSettings.bassStrumAnim.set(strum_anim('option', config.get('Band', 'BassStrumAnim')))

    # ==================================
    # Auto Launch Settings
    # ==================================
    autoLaunchEnabled.set(config.get('AutoLaunch', 'Enabled'))
    AutoLaunch.auto_update_status()

    AutoLaunch.AutoLaunch_General.autoVenue.set(auto_get_venue(config.get('AutoLaunch', 'Venue')))

    AutoLaunch.AutoLaunch_General.autoSongID.set(config.get('AutoLaunch', 'Song'))

    AutoLaunch.AutoLaunch_General.autoP1Bot.set(config.get('AutoLaunch', 'Bot'))
    AutoLaunch.AutoLaunch_General.autoP2Bot.set(config.get('AutoLaunch', 'Bot2'))
    AutoLaunch.AutoLaunch_General.autoP3Bot.set(config.get('AutoLaunch', 'Bot3'))
    AutoLaunch.AutoLaunch_General.autoP4Bot.set(config.get('AutoLaunch', 'Bot4'))

    # ==================================
    # Debug Settings
    # ==================================
    DebugSettings.fixNoteLimit.set(config.get('Debug', 'FixNoteLimit'))
    DebugSettings.fixMemoryHandler.set(config.get('Debug', 'FixMemoryHandler'))
    DebugSettings.loggerConsole.set(config.get('Logger', 'Console'))
    DebugSettings.writeFile.set(config.get('Logger', 'WriteFile'))
    DebugSettings.disableSongLogging.set(config.get('Logger', 'DisableSongLogging'))
    DebugSettings.debugDLCSync.set(config.get('Logger', 'DebugDLCSync'))
    DebugSettings.fixFSBObjects.set(config.get('Debug', 'FixFSBObjects'))
    DebugSettings.extraOptimizedSaves.set(config.get('Debug', 'ExtraOptimizedSaves'))
    DebugSettings.debugSaves.set(config.get('Debug', 'DebugSaves'))
    DebugSettings.showWarnings.set(config.get('Logger', 'ShowWarnings'))

    # ====================================================================
    # AspyrConfig Settings
    # ====================================================================
    # Now we'll read settings that are stored in AspyrConfig.

    # ==================================
    # Input Settings
    # ==================================
    # Mic Video Delay
    InputSettings.inputMicSettingsVDelayEntry.insert(0, aspyr_get_string("Options.VocalsVisualLag"))

    # Use Input Hack
    InputSettings.disableInputHack.set(config.get('Debug', 'DisableInputHack'))

    # ============================ GUITAR INPUTS ============================ #
    InputSettings.inputKeyGuitarGreenEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Guitar", fallbackValue = ASPYR_INPUT_GUITAR_BACKUP), "GREEN"))
    InputSettings.inputKeyGuitarRedEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Guitar", fallbackValue = ASPYR_INPUT_GUITAR_BACKUP), "RED"))
    InputSettings.inputKeyGuitarYellowEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Guitar", fallbackValue = ASPYR_INPUT_GUITAR_BACKUP), "YELLOW"))
    InputSettings.inputKeyGuitarBlueEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Guitar", fallbackValue = ASPYR_INPUT_GUITAR_BACKUP), "BLUE"))
    InputSettings.inputKeyGuitarOrangeEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Guitar", fallbackValue = ASPYR_INPUT_GUITAR_BACKUP), "ORANGE"))

    InputSettings.inputKeyGuitarSPEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Guitar", fallbackValue = ASPYR_INPUT_GUITAR_BACKUP), "STAR"))
    InputSettings.inputKeyGuitarStartEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Guitar", fallbackValue = ASPYR_INPUT_GUITAR_BACKUP), "START"))
    InputSettings.inputKeyGuitarSelectEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Guitar", fallbackValue = ASPYR_INPUT_GUITAR_BACKUP), "BACK"))
    InputSettings.inputKeyGuitarCancelEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Guitar", fallbackValue = ASPYR_INPUT_GUITAR_BACKUP), "CANCEL"))
    InputSettings.inputKeyGuitarWhammyEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Guitar", fallbackValue = ASPYR_INPUT_GUITAR_BACKUP), "WHAMMY"))

    InputSettings.inputKeyGuitarUpEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Guitar", fallbackValue = ASPYR_INPUT_GUITAR_BACKUP), "UP"))
    InputSettings.inputKeyGuitarDownEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Guitar", fallbackValue = ASPYR_INPUT_GUITAR_BACKUP), "DOWN"))
    InputSettings.inputKeyGuitarLeftEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Guitar", fallbackValue = ASPYR_INPUT_GUITAR_BACKUP), "LEFT"))
    InputSettings.inputKeyGuitarRightEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Guitar", fallbackValue = ASPYR_INPUT_GUITAR_BACKUP), "RIGHT"))

    # ============================ DRUM INPUTS ============================ #
    InputSettings.inputKeyDrumsRedEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Drum", fallbackValue = ASPYR_INPUT_DRUMS_BACKUP), "RED"))
    InputSettings.inputKeyDrumsYellowEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Drum", fallbackValue = ASPYR_INPUT_DRUMS_BACKUP), "YELLOW"))
    InputSettings.inputKeyDrumsBlueEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Drum", fallbackValue = ASPYR_INPUT_DRUMS_BACKUP), "BLUE"))
    InputSettings.inputKeyDrumsOrangeEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Drum", fallbackValue = ASPYR_INPUT_DRUMS_BACKUP), "ORANGE"))
    InputSettings.inputKeyDrumsGreenEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Drum", fallbackValue = ASPYR_INPUT_DRUMS_BACKUP), "GREEN"))
    InputSettings.inputKeyDrumsKickEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Drum", fallbackValue = ASPYR_INPUT_DRUMS_BACKUP), "KICK"))

    InputSettings.inputKeyDrumsStartEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Drum", fallbackValue = ASPYR_INPUT_DRUMS_BACKUP), "START"))
    InputSettings.inputKeyDrumsSelectEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Drum", fallbackValue = ASPYR_INPUT_DRUMS_BACKUP), "BACK"))
    InputSettings.inputKeyDrumsCancelEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Drum", fallbackValue = ASPYR_INPUT_DRUMS_BACKUP), "CANCEL"))

    InputSettings.inputKeyDrumsUpEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Drum", fallbackValue = ASPYR_INPUT_DRUMS_BACKUP), "UP"))
    InputSettings.inputKeyDrumsDownEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Drum", fallbackValue = ASPYR_INPUT_DRUMS_BACKUP), "DOWN"))

    # ============================ MIC INPUTS ============================ #
    InputSettings.inputKeyMicGreenEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Mic", fallbackValue = ASPYR_INPUT_MIC_BACKUP), "GREEN"))
    InputSettings.inputKeyMicRedEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Mic", fallbackValue = ASPYR_INPUT_MIC_BACKUP), "RED"))
    InputSettings.inputKeyMicYellowEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Mic", fallbackValue = ASPYR_INPUT_MIC_BACKUP), "YELLOW"))
    InputSettings.inputKeyMicBlueEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Mic", fallbackValue = ASPYR_INPUT_MIC_BACKUP), "BLUE"))
    InputSettings.inputKeyMicOrangeEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Mic", fallbackValue = ASPYR_INPUT_MIC_BACKUP), "ORANGE"))

    InputSettings.inputKeyMicStartEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Mic", fallbackValue = ASPYR_INPUT_MIC_BACKUP), "START"))
    InputSettings.inputKeyMicSelectEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Mic", fallbackValue = ASPYR_INPUT_MIC_BACKUP), "BACK"))
    InputSettings.inputKeyMicCancelEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Mic", fallbackValue = ASPYR_INPUT_MIC_BACKUP), "CANCEL"))

    InputSettings.inputKeyMicUpEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Mic", fallbackValue = ASPYR_INPUT_MIC_BACKUP), "UP"))
    InputSettings.inputKeyMicDownEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Mic", fallbackValue = ASPYR_INPUT_MIC_BACKUP), "DOWN"))

    # ============================ MENU INPUTS ============================ #
    InputSettings.inputKeyMenuGreenEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Menu", fallbackValue = ASPYR_INPUT_MENU_BACKUP), "GREEN"))
    InputSettings.inputKeyMenuRedEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Menu", fallbackValue = ASPYR_INPUT_MENU_BACKUP), "RED"))
    InputSettings.inputKeyMenuYellowEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Menu", fallbackValue = ASPYR_INPUT_MENU_BACKUP), "YELLOW"))
    InputSettings.inputKeyMenuBlueEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Menu", fallbackValue = ASPYR_INPUT_MENU_BACKUP), "BLUE"))
    InputSettings.inputKeyMenuOrangeEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Menu", fallbackValue = ASPYR_INPUT_MENU_BACKUP), "ORANGE"))

    InputSettings.inputKeyMenuStartEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Menu", fallbackValue = ASPYR_INPUT_MENU_BACKUP), "START"))
    InputSettings.inputKeyMenuSelectEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Menu", fallbackValue = ASPYR_INPUT_MENU_BACKUP), "BACK"))
    InputSettings.inputKeyMenuCancelEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Menu", fallbackValue = ASPYR_INPUT_MENU_BACKUP), "CANCEL"))

    InputSettings.inputKeyMenuWhammyEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Menu", fallbackValue = ASPYR_INPUT_MENU_BACKUP), "WHAMMY"))
    InputSettings.inputKeyMenuKickEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Menu", fallbackValue = ASPYR_INPUT_MENU_BACKUP), "KICK"))

    InputSettings.inputKeyMenuUpEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Menu", fallbackValue = ASPYR_INPUT_MENU_BACKUP), "UP"))
    InputSettings.inputKeyMenuDownEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Menu", fallbackValue = ASPYR_INPUT_MENU_BACKUP), "DOWN"))
    InputSettings.inputKeyMenuLeftEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Menu", fallbackValue = ASPYR_INPUT_MENU_BACKUP), "LEFT"))
    InputSettings.inputKeyMenuRightEntry.insert(0, aspyr_key_decode(aspyr_get_string("Keyboard_Menu", fallbackValue = ASPYR_INPUT_MENU_BACKUP), "RIGHT"))

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
root.geometry(f"1080x738+{get_screen_resolution()[0] // 5}+{get_screen_resolution()[1] // 8}")
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

    # ====================================== FILE MENU ICONS ====================================== #
    SAVE_CONFIG_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/menuicons/file/save_file.ico")))
    debug_add_entry(f"(const) SAVE_CONFIG_ICON has relative path {resource_path('res/menuicons/file/save_file.ico')}", 1)

    SAVE_RUN_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/menuicons/file/save_and_run.ico")))
    debug_add_entry(f"(const) SAVE_RUN_ICON has relative path {resource_path('res/menuicons/file/save_and_run.ico')}", 1)

    EXIT_PROGRAM_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/menuicons/file/exit_program.ico")))
    debug_add_entry(f"(const) EXIT_PROGRAM_ICON has relative path {resource_path('res/menuicons/file/exit_program.ico')}", 1)

    # ====================================== MODS MENU ICONS ====================================== #
    OPEN_MODS_FOLDER_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/menuicons/mods/open_mods.ico")))
    debug_add_entry(f"(const) OPEN_MODS_FOLDER_ICON has relative path {resource_path('res/menuicons/mods/open_mods.ico')}", 1)

    INSTALL_MODS_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/menuicons/mods/install_mods.ico")))
    debug_add_entry(f"(const) INSTALL_MODS_ICON has relative path {resource_path('res/menuicons/mods/install_mods.ico')}", 1)

    # ====================================== GAME MENU ICONS ====================================== #
    RUN_WTDE_ICON = ImageTk.PhotoImage(Image.open(resource_path("res/menuicons/game/play.ico")))
    debug_add_entry(f"(const) RUN_WTDE_ICON has relative path {resource_path('res/menuicons/game/play.ico')}", 1)

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

wtdeOptionsRoot = TTK.Notebook(root, takefocus = False)
wtdeOptionsRoot.place(x = 186, y = 0)

# Various WTDE commands.
# Edit the background color on the buttons and notebook.
TTK.Style().configure("TButton", background = BG_COLOR)
TTK.Style().configure("TNotebook", background = '#0B101F', tabposition = 'nw')
TTK.Style().configure("TCheckbutton", background = BG_COLOR, foreground = FG_COLOR)
TTK.Style().configure("TMenubutton", width = 20)
TTK.Style().configure("TCombobox", background = BG_COLOR)
TTK.Style().configure("TEntry", background = BG_COLOR)

# Save configuration and start WTDE.
wtdeStartGame = TTK.Button(root, text = "Save & Run WTDE", width = 25, padding = 10, command = lambda: wtde_save_config(True))
wtdeStartGame.place(x = 4, y = 185)

wtdeSaveConfig = TTK.Button(root, text = "Save Configuration", width = 25, padding = 10, command = wtde_save_config)
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
# Menu Stuff
# 
# Menu stuff we might do. Not sure if this will make it into the final program.
# ===========================================================================================================
# Main MenuClass class.
class MenuClass():
    """ Menu class. Used for the menus on the top of the launcher. """
    topMenu = Menu(root)
    root.config(menu = topMenu)

    # ======= FILE MENU ======= #
    fileMenu = Menu(topMenu, tearoff = False, activebackground = MENU_HOVER, activeforeground = '#000000')
    fileMenu.add_command(label = " Save Configuration", image = ImageConst.SAVE_CONFIG_ICON, compound = 'left', command = wtde_save_config)
    fileMenu.add_command(label = " Save Config and Run WTDE", image = ImageConst.SAVE_RUN_ICON, compound = 'left', command = lambda: wtde_save_config(True))
    fileMenu.add_separator()
    fileMenu.add_command(label = " Exit", image = ImageConst.EXIT_PROGRAM_ICON, compound = 'left', command = root.destroy)

    # ======= MODS MENU ======= #
    modsMenu = Menu(topMenu, tearoff = False, activebackground = MENU_HOVER, activeforeground = '#000000')
    modsMenu.add_command(label = " Open Mods Folder", image = ImageConst.OPEN_MODS_FOLDER_ICON, compound = 'left', command = open_mods_folder)
    modsMenu.add_separator()
    modsMenu.add_command(label = " Install Mods...", image = ImageConst.INSTALL_MODS_ICON, compound = 'left', command = wtde_ask_install_mods)

    # ======= GAME MENU ======= #
    gameMenu = Menu(topMenu, tearoff = False, activebackground = MENU_HOVER, activeforeground = '#000000')
    gameMenu.add_command(label = " Run GHWT: DE", image = ImageConst.RUN_WTDE_ICON, compound = 'left', command = wtde_run_game)

    topMenu.add_cascade(menu = fileMenu, label = "File")
    topMenu.add_cascade(menu = modsMenu, label = "Mods")
    topMenu.add_cascade(menu = gameMenu, label = "Game")

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

    # This is a PIP installed label that will parse HTML.
    newsLabel = HTMLLabel(wtdeOptionsNews, html = wtde_get_news())
    newsLabel.pack(side = 'left', fill = 'both', expand = 1)
    '''
    newsLabel = Text(wtdeOptionsNews, bg = BG_COLOR, fg = FG_COLOR, relief = 'flat', font = FONT_INFO_HEADER, wrap = 'word')
    newsLabel.pack(side = 'left', fill = 'both', expand = 1)
    newsLabel.insert(END, wtde_get_news())
    newsLabel.configure(state = 'disabled')
    '''

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
    modsManagerLabel.pack(anchor = 'nw')

    # Command Frame
    modManagerCommandsFrame = Frame(wtdeOptionsMods, bg = BG_COLOR, relief = 'flat')
    modManagerCommandsFrame.pack(fill = 'x', pady = 5)

    # Install Mod
    modManagerInstallMod = TTK.Button(modManagerCommandsFrame, text = "Install Mods", width = 20, takefocus = False, command = wtde_ask_install_mods)
    modManagerInstallMod.grid(row = 0, column = 0, padx = 5)
    ToolTip(modManagerInstallMod, msg = "Install mods into GHWT: DE.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Refresh Mods List
    modManagerRefresh = TTK.Button(modManagerCommandsFrame, text = "Refresh List", width = 20, takefocus = False, command = lambda: wtde_get_mods(root, ModsSettings.modTree, ModsSettings.modManagerStatus))
    modManagerRefresh.grid(row = 0, column = 1, padx = 5)
    ToolTip(modManagerRefresh, msg = "Refresh the list of installed mods.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Mod Manager Setup
    modManagerFrame = Frame(wtdeOptionsMods, bg = BG_COLOR, relief = 'flat')
    modManagerFrame.pack(fill = 'both', expand = 1)

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
    modManagerStatus.pack(fill = 'x', anchor = 'n')

    # Load all mod data into the tree.
    wtde_get_mods(root, modTree, modManagerStatus)

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
                        "  •  April Fool's Day Theme\n" \
                        "  •  Halloween Theme\n" \
                        "  •  Christmas Theme\n" \
                        "  •  The Dody Holiday"
    
    generalAllowHolidays = TTK.Checkbutton(wtdeOptionsGeneral, text = "Use Holiday Themes", variable = allowHolidays, onvalue = '1', offvalue = '0')
    generalAllowHolidays.grid(row = 2, column = 0, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalAllowHolidays, msg = ALLOW_HOLIDAYS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Whammy Pitch Shift
    whammyPitchShift = StringVar()
    WHAMMY_PITCH_SHIFT_TIP = "Turn ON or OFF whammy effects. If this is OFF, audio distortion by whammy will be disabled."
    generalWhammyPitchShift = TTK.Checkbutton(wtdeOptionsGeneral, text = "Whammy Pitch Shift", variable = whammyPitchShift, onvalue = '1', offvalue = '0')
    generalWhammyPitchShift.grid(row = 3, column = 0, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalWhammyPitchShift, msg = WHAMMY_PITCH_SHIFT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Use Song Specific Intros
    songSpecificIntros = StringVar()
    SONG_SPECIFIC_INTROS_TIP = "Allow certain intro animations to play for certain songs, primarily for celebrity songs."
    generalSongSpecificIntros = TTK.Checkbutton(wtdeOptionsGeneral, text = "Use Song Specific Intros", variable = songSpecificIntros, onvalue = '1', offvalue = '0')
    generalSongSpecificIntros.grid(row = 4, column = 0, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalSongSpecificIntros, msg = SONG_SPECIFIC_INTROS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Language
    language = StringVar()
    LANGUAGE_SELECT_TIP = "Set the language to be used in-game."

    generalLanguageSelectLabel = Label(wtdeOptionsGeneral, text = "Language:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    generalLanguageSelectLabel.grid(row = 5, column = 0, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalLanguageSelectLabel, msg = LANGUAGE_SELECT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    generalLanguageSelect = TTK.OptionMenu(wtdeOptionsGeneral, language, *[""] + [lang[0] for lang in LANGUAGES])
    generalLanguageSelect.grid(row = 5, column = 1, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalLanguageSelect, msg = LANGUAGE_SELECT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Audio Buffer Length
    audioBuffLen = StringVar()
    AUDIO_BUFF_LEN_TIP = "The length, in bytes, of the audio buffer used when decoding FMOD Sound Bank streams. Higher is usually better.\n\n" \
                        "Modifying this and/or changing your sound output to 44.1 kHz can cause bad audio output in-game."

    generalAudioBuffLenLabel = Label(wtdeOptionsGeneral, text = "Audio Buffer Length:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    generalAudioBuffLenLabel.grid(row = 6, column = 0, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalAudioBuffLenLabel, msg = AUDIO_BUFF_LEN_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    generalAudioBuffLen = TTK.OptionMenu(wtdeOptionsGeneral, audioBuffLen, *AUDIO_BUFFLENS)
    generalAudioBuffLen.grid(row = 6, column = 1, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalAudioBuffLen, msg = AUDIO_BUFF_LEN_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Auto Login
    autoLogin = StringVar()
    AUTO_LOGIN_TIP = "Set if you want the game to automatically log you in to the online servers upon startup."

    generalAutoLoginLabel = Label(wtdeOptionsGeneral, text = "Auto Login:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    generalAutoLoginLabel.grid(row = 7, column = 0, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalAutoLoginLabel, msg = AUTO_LOGIN_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    generalAutoLogin = TTK.OptionMenu(wtdeOptionsGeneral, autoLogin, *AUTO_LOGIN_OPTIONS)
    generalAutoLogin.grid(row = 7, column = 1, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalAutoLogin, msg = AUTO_LOGIN_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Holiday Theme
    holiday = StringVar()
    FORCE_HOLIDAY_THEME = "Set if you want the game to force a certain holiday theme."

    generalHolidayForceLabel = Label(wtdeOptionsGeneral, text = "Holiday Theme:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    generalHolidayForceLabel.grid(row = 8, column = 0, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalHolidayForceLabel, msg = FORCE_HOLIDAY_THEME, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    generalHolidayForce = TTK.OptionMenu(wtdeOptionsGeneral, holiday, *[""] + [theme[0] for theme in HOLIDAYS])
    generalHolidayForce.grid(row = 8, column = 1, padx = 20, pady = 5, sticky = 'w')
    ToolTip(generalHolidayForce, msg = FORCE_HOLIDAY_THEME, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

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
    INPUT_HACK_TIP = "Enable or disable the input hack.\n\n" \
                     "In its essence, this makes all plugged in controllers behave as if they were an XInput device.\n\n" \
                     "If this is ON, controllers that disconnect mid-game will reconnect and still be usable, but the Bind Controllers menu will freeze.\n\n" \
                     "If this is OFF, the Bind Controllers menu will function properly, but if a controller disconnects mid-game, the game must be restarted for it to be usable again."
    inputUseInputHack = TTK.Checkbutton(inputFrameWidgets, text = "Use Input Hack", variable = disableInputHack, onvalue = '1', offvalue = '0')
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
    graphicsUseVSync = TTK.Checkbutton(wtdeOptionsGraphics, text = "Use Vertical Sync", variable = disableVSync, onvalue = '0', offvalue = '1', command = fps_limit_update)
    graphicsUseVSync.grid(row = 4, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsUseVSync, msg = VSYNC_LIMIT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Hit Sparks
    hitSparks = StringVar()
    HIT_SPARKS_TIP = "Turn ON or OFF sparks when notes are hit."
    graphicsHitSparks = TTK.Checkbutton(wtdeOptionsGraphics, text = "Show Hit Sparks", variable = hitSparks, onvalue = '1', offvalue = '0')
    graphicsHitSparks.grid(row = 5, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsHitSparks, msg = HIT_SPARKS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Depth of Field
    disableDOF = StringVar()
    USE_DOF_TIP = "Turn ON or OFF depth of field. This makes background elements blurrier than those in the foreground."
    graphicsDisableDOF = TTK.Checkbutton(wtdeOptionsGraphics, text = "Depth of Field", variable = disableDOF, onvalue = '0', offvalue = '1')
    graphicsDisableDOF.grid(row = 6, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsDisableDOF, msg = USE_DOF_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Windowed Mode
    windowedMode = StringVar()
    WINDOWED_MODE_TIP = "Run the game in windowed mode."
    graphicsWindowedMode = TTK.Checkbutton(wtdeOptionsGraphics, text = "Windowed Mode", variable = windowedMode, onvalue = '1', offvalue = '0')
    graphicsWindowedMode.grid(row = 7, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsWindowedMode, msg = WINDOWED_MODE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Borderless Windowed
    borderless = StringVar()
    BORDERLESS_MODE_TIP = "Run the game in borderless windowed mode."
    graphicsBorderlessWindowed = TTK.Checkbutton(wtdeOptionsGraphics, text = "Borderless Windowed", variable = borderless, onvalue = '1', offvalue = '0')
    graphicsBorderlessWindowed.grid(row = 8, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsBorderlessWindowed, msg = BORDERLESS_MODE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Use Bloom
    disableBloom = StringVar()
    BLOOM_FX_TIP = "Turn ON or OFF bloom effects. This adds faint glows around bright elements in the scene."
    graphicsDisableBloom = TTK.Checkbutton(wtdeOptionsGraphics, text = "Use Bloom", variable = disableBloom, onvalue = '0', offvalue = '1')
    graphicsDisableBloom.grid(row = 9, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsDisableBloom, msg = BLOOM_FX_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Use Color Filters
    colorFilters = StringVar()
    COLOR_FILTERS_TIP = "Turn ON or OFF color filters. These are filters primarily used in\n" \
                        "Guitar Hero: Metallica."
    graphicsColorFilters = TTK.Checkbutton(wtdeOptionsGraphics, text = "Use Color Filters", variable = colorFilters, onvalue = '1', offvalue = '0')
    graphicsColorFilters.grid(row = 10, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsColorFilters, msg = COLOR_FILTERS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Use Anti-Aliasing
    antiAliasing = StringVar()
    ANTI_ALIASING_TIP = "Turn ON or OFF anti-aliasing. The anti-aliasing used by GHWT is multi-sampling."
    graphicsAntiAliasing = TTK.Checkbutton(wtdeOptionsGraphics, text = "Use Anti-Aliasing", variable = antiAliasing, onvalue = '1', offvalue = '0')
    graphicsAntiAliasing.grid(row = 11, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsAntiAliasing, msg = ANTI_ALIASING_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Render Particles
    renderParticles = StringVar()
    RENDER_PARTICLES_TIP = "Turn ON or OFF rendering of particles. This includes things like fire, sparks, smoke, etc."
    graphicsRenderParticles = TTK.Checkbutton(wtdeOptionsGraphics, text = "Render Particles", variable = renderParticles, onvalue = '1', offvalue = '0')
    graphicsRenderParticles.grid(row = 12, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsRenderParticles, msg = RENDER_PARTICLES_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Render Level Geometry
    renderGeoms = StringVar()
    RENDER_GEOMETRY_TIP = "Turn ON or OFF rendering of level geometry, except level objects."
    graphicsRenderGeoms = TTK.Checkbutton(wtdeOptionsGraphics, text = "Render Level Geometry", variable = renderGeoms, onvalue = '1', offvalue = '0')
    graphicsRenderGeoms.grid(row = 13, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsRenderGeoms, msg = RENDER_GEOMETRY_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Render Instances
    renderInstances = StringVar()
    RENDER_INSTANCES_TIP = "Turn ON or OFF rendering of instances. Controls rendering of things like dynamic\n" \
                           "and level objects. Also includes characters and anything that moves."
    graphicsRenderInstances = TTK.Checkbutton(wtdeOptionsGraphics, text = "Render Instances", variable = renderInstances, onvalue = '1', offvalue = '0')
    graphicsRenderInstances.grid(row = 14, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsRenderInstances, msg = RENDER_INSTANCES_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Draw Projectors
    drawProjectors = StringVar()
    DRAW_PROJECTORS_TIP = "Turn ON or OFF rendering of projectors. These are things like spotlight projectors that\n" \
                          "show under characters and cast shadows."
    graphicsDrawProjectors = TTK.Checkbutton(wtdeOptionsGraphics, text = "Draw Projectors", variable = drawProjectors, onvalue = '1', offvalue = '0')
    graphicsDrawProjectors.grid(row = 15, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsDrawProjectors, msg = DRAW_PROJECTORS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Render 2D Items
    render2D = StringVar()
    RENDER_2D_TIP = "Turn ON or OFF rendering 2D items.\n\n" \
                    "Note: If this is OFF, this disables rendering of ALL 2D elements, including the HUD and GUI!"
    graphicsRender2D = TTK.Checkbutton(wtdeOptionsGraphics, text = "Render 2D Items", variable = render2D, onvalue = '1', offvalue = '0')
    graphicsRender2D.grid(row = 16, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsRender2D, msg = RENDER_2D_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Render Screen FX
    renderScreenFX = StringVar()
    RENDER_SCREEN_FX_TIP = "Turn ON or OFF rendering of screen effects, such as bloom, depth of field, saturation, etc."
    graphicsRenderScreenFX = TTK.Checkbutton(wtdeOptionsGraphics, text = "Render Screen FX", variable = renderScreenFX, onvalue = '1', offvalue = '0')
    graphicsRenderScreenFX.grid(row = 17, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsRenderScreenFX, msg = RENDER_SCREEN_FX_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Black Stage
    blackStage = StringVar()
    BLACK_STAGE_TIP = "Turn ON or OFF black stage. Makes the stage completely black and hides all band members."
    graphicsBlackStage = TTK.Checkbutton(wtdeOptionsGraphics, text = "Hide Stage/Black Stage", variable = blackStage, onvalue = '1', offvalue = '0')
    graphicsBlackStage.grid(row = 18, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsBlackStage, msg = BLACK_STAGE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Hide Band
    hideBand = StringVar()
    HIDE_BAND_TIP = "Show or hide the band."
    graphicsHideBand = TTK.Checkbutton(wtdeOptionsGraphics, text = "Hide Band", variable = hideBand, onvalue = '1', offvalue = '0')
    graphicsHideBand.grid(row = 19, column = 0, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsHideBand, msg = HIDE_BAND_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Hide Instruments
    hideInstruments = StringVar()
    HIDE_INSTRUMENTS_TIP = "Show or hide the band's instruments."
    graphicsHideInstruments = TTK.Checkbutton(wtdeOptionsGraphics, text = "Hide Instruments", variable = hideInstruments, onvalue = '1', offvalue = '0')
    graphicsHideInstruments.grid(row = 1, column = 4, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsHideInstruments, msg = HIDE_INSTRUMENTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Apply Band Name
    applyBandName = StringVar()
    APPLY_BAND_NAME_TIP = "Applies the band's name to certain venue elements. Unless there are edge cases\n" \
                          "where this causes crashes, this should be left enabled."
    graphicsApplyBandName = TTK.Checkbutton(wtdeOptionsGraphics, text = "Apply Band Name", variable = applyBandName, onvalue = '1', offvalue = '0')
    graphicsApplyBandName.grid(row = 2, column = 4, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsApplyBandName, msg = APPLY_BAND_NAME_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Apply Band Name
    applyBandLogo = StringVar()
    APPLY_BAND_LOGO_TIP = "Applies the band's logo textures to certain venue elements. Unless there are edge cases\n" \
                          "where this causes crashes, this should be left enabled."
    graphicsApplyBandLogo = TTK.Checkbutton(wtdeOptionsGraphics, text = "Apply Band Logo", variable = applyBandLogo, onvalue = '1', offvalue = '0')
    graphicsApplyBandLogo.grid(row = 3, column = 4, columnspan = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsApplyBandLogo, msg = APPLY_BAND_LOGO_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Note (Gem) Style
    gemTheme = StringVar()
    NOTE_STYLE_TIP = "Select the style of notes used on the highway."
    graphicsNoteStyleLabel = Label(wtdeOptionsGraphics, text = "Note (Gem) Style:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    graphicsNoteStyleLabel.grid(row = 4, column = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsNoteStyleLabel, msg = NOTE_STYLE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    graphicsNoteStyle = TTK.OptionMenu(wtdeOptionsGraphics, gemTheme, *[""] + [name[0] for name in NOTE_STYLES])
    graphicsNoteStyle.config(width = 25)
    graphicsNoteStyle.grid(row = 4, column = 5, columnspan = 3, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsNoteStyle, msg = NOTE_STYLE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Note (Gem) Theme
    gemColors = StringVar()
    NOTE_THEME_TIP = "Select the color scheme for the notes on the highway."
    graphicsNoteThemeLabel = Label(wtdeOptionsGraphics, text = "Note (Gem) Theme:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    graphicsNoteThemeLabel.grid(row = 5, column = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsNoteThemeLabel, msg = NOTE_THEME_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    graphicsNoteTheme = TTK.OptionMenu(wtdeOptionsGraphics, gemColors, *[""] + [name[0] for name in NOTE_THEMES])
    graphicsNoteTheme.config(width = 25)
    graphicsNoteTheme.grid(row = 5, column = 5, columnspan = 3, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsNoteTheme, msg = NOTE_THEME_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Song Intro Style
    songIntroStyle = StringVar()
    INTRO_STYLE_TIP = "Select the style of intro shown on the top left corner of the\n" \
                      "screen at the beginning of songs."
    graphicsSongIntroStyleLabel = Label(wtdeOptionsGraphics, text = "Song Intro Style:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    graphicsSongIntroStyleLabel.grid(row = 6, column = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsSongIntroStyleLabel, msg = INTRO_STYLE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    graphicsSongIntroStyle = TTK.OptionMenu(wtdeOptionsGraphics, songIntroStyle, *[""] + [name[0] for name in INTRO_STYLES])
    graphicsSongIntroStyle.config(width = 25)
    graphicsSongIntroStyle.grid(row = 6, column = 5, columnspan = 3, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsSongIntroStyle, msg = INTRO_STYLE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Time of Day Profile
    defaultTODProfile = StringVar()
    TOD_PROFILE_TIP = "This sets the default Time of Day profile in-game, which is the default post-processing effects.\n" \
                      "In its essence, these are basically filter effects on the screen."
    graphicsTODProfilesLabel = Label(wtdeOptionsGraphics, text = "Time of Day Profile:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    graphicsTODProfilesLabel.grid(row = 7, column = 4, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsTODProfilesLabel, msg = TOD_PROFILE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    graphicsTODProfiles = TTK.OptionMenu(wtdeOptionsGraphics, defaultTODProfile, *[""] + [name[0] for name in TOD_PROFILES])
    graphicsTODProfiles.config(width = 25)
    graphicsTODProfiles.grid(row = 7, column = 5, columnspan = 3, padx = 20, pady = 5, sticky = 'w')
    ToolTip(graphicsTODProfiles, msg = TOD_PROFILE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

# Execute tab code.
GraphicsSettings()

# ===========================================================================================================
# Band Settings
# 
# Used for preferred band/venue and also preferred highways.
# ===========================================================================================================
# Main BandSettings class.
class BandSettings():
    """
    Band settings tab.
    \n
    This class is responsible for populating the Band Settings tab with the necessary widgets.
    """
    # Title text with the purpose of the tab.
    BAND_SETTINGS_TITLE_TEXT = "Band Settings: Modify your preferred characters and venue for your band.\nHover over any option to see what it does!"
    bandTitleLabel = Label(wtdeOptionsBand, text = BAND_SETTINGS_TITLE_TEXT, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO_HEADER, justify = 'left', anchor = 'w')
    bandTitleLabel.grid(row = 0, column = 0, columnspan = 999, sticky = 'w')

    # Preferred Guitarist
    GUITAR_PREFERRED_TIP = "Set the ID of the character to force as the active guitarist. Leave this blank to force no character.\n\n" \
                           "This value depends on what you want for your characters.\n" \
                           "  •  For Rock Star Creator characters, use \"custom_character_x\", where x ranges from 0-19,\n" \
                           "     defining which custom character to use. For instance, \"custom_character_0\" will use\n" \
                           "     the first custom character made.\n" \
                           "  •  For built-in WTDE characters, refer to the \"ID_Characters.txt\" file in the Resources\n" \
                           "     folder in your GHWT installation folder.\n" \
                           "  •  If you're using modded characters, use the FOLDER name of the character!\n\n" \
                           "Remember! If someone else does NOT have a character that you have, they will be rendered as Axel Steel (GHWT) in-game as a placeholder. Modded characters in Online Career will crash the game."
    bandPrefGuitaristLabel = Label(wtdeOptionsBand, text = "Preferred Guitarist:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    bandPrefGuitaristLabel.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'e')
    ToolTip(bandPrefGuitaristLabel, msg = GUITAR_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    bandPrefGuitarist = TTK.Entry(wtdeOptionsBand, width = 30)
    bandPrefGuitarist.grid(row = 1, column = 1, padx = 10, pady = 5, sticky = 'w')
    ToolTip(bandPrefGuitarist, msg = GUITAR_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Preferred Bassist
    BASS_PREFERRED_TIP = "Set the ID of the character to force as the active guitarist. Leave this blank to force no character.\n\n" \
                         "This value depends on what you want for your characters.\n" \
                         "  •  For Rock Star Creator characters, use \"custom_character_x\", where x ranges from 0-19,\n" \
                         "     defining which custom character to use. For instance, \"custom_character_0\" will use\n" \
                         "     the first custom character made.\n" \
                         "  •  For built-in WTDE characters, refer to the \"ID_Characters.txt\" file in the Resources\n" \
                         "     folder in your GHWT installation folder.\n" \
                         "  •  If you're using modded characters, use the FOLDER name of the character!\n\n" \
                         "Remember! If someone else does NOT have a character that you have, they will be rendered as Axel Steel (GHWT) in-game as a placeholder. Modded characters in Online Career will crash the game."
    bandPrefBassistLabel = Label(wtdeOptionsBand, text = "Preferred Bassist:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    bandPrefBassistLabel.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'e')
    ToolTip(bandPrefBassistLabel, msg = BASS_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    bandPrefBassist = TTK.Entry(wtdeOptionsBand, width = 30)
    bandPrefBassist.grid(row = 2, column = 1, padx = 10, pady = 5, sticky = 'w')
    ToolTip(bandPrefBassist, msg = BASS_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Preferred Drummer
    DRUM_PREFERRED_TIP = "Set the ID of the character to force as the active drummer. Leave this blank to force no character.\n\n" \
                         "This value depends on what you want for your characters.\n" \
                         "  •  For Rock Star Creator characters, use \"custom_character_x\", where x ranges from 0-19,\n" \
                         "     defining which custom character to use. For instance, \"custom_character_0\" will use\n" \
                         "     the first custom character made.\n" \
                         "  •  For built-in WTDE characters, refer to the \"ID_Characters.txt\" file in the Resources\n" \
                         "     folder in your GHWT installation folder.\n" \
                         "  •  If you're using modded characters, use the FOLDER name of the character!\n\n" \
                         "Remember! If someone else does NOT have a character that you have, they will be rendered as Axel Steel (GHWT) in-game as a placeholder. Modded characters in Online Career will crash the game."
    bandPrefDrummerLabel = Label(wtdeOptionsBand, text = "Preferred Drummer:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    bandPrefDrummerLabel.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'e')
    ToolTip(bandPrefDrummerLabel, msg = DRUM_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    bandPrefDrummer = TTK.Entry(wtdeOptionsBand, width = 30)
    bandPrefDrummer.grid(row = 3, column = 1, padx = 10, pady = 5, sticky = 'w')
    ToolTip(bandPrefDrummer, msg = DRUM_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Preferred Vocalist
    VOXS_PREFERRED_TIP = "Set the ID of the character to force as the active vocalist. Leave this blank to force no character.\n\n" \
                         "This value depends on what you want for your characters.\n" \
                         "  •  For Rock Star Creator characters, use \"custom_character_x\", where x ranges from 0-19,\n" \
                         "     defining which custom character to use. For instance, \"custom_character_0\" will use\n" \
                         "     the first custom character made.\n" \
                         "  •  For built-in WTDE characters, refer to the \"ID_Characters.txt\" file in the Resources\n" \
                         "     folder in your GHWT installation folder.\n" \
                         "  •  If you're using modded characters, use the FOLDER name of the character!\n\n" \
                         "Remember! If someone else does NOT have a character that you have, they will be rendered as Axel Steel (GHWT) in-game as a placeholder. Modded characters in Online Career will crash the game."
    bandPrefSingerLabel = Label(wtdeOptionsBand, text = "Preferred Singer:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    bandPrefSingerLabel.grid(row = 4, column = 0, padx = 10, pady = 5, sticky = 'e')
    ToolTip(bandPrefSingerLabel, msg = VOXS_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    bandPrefSinger = TTK.Entry(wtdeOptionsBand, width = 30)
    bandPrefSinger.grid(row = 4, column = 1, padx = 10, pady = 5, sticky = 'w')
    ToolTip(bandPrefSinger, msg = VOXS_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Preferred Venue
    VENUE_PREFERRED_TIP = "Set the venue you want to always use while in-game. If a venue you wish to\n" \
                          "use isn't listed, type it in the box.\n\n" \
                          "This also determines the default venue in the Venue Selector in Quickplay."
    bandPrefStageLabel = Label(wtdeOptionsBand, text = "Preferred Venue:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    bandPrefStageLabel.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'e')
    ToolTip(bandPrefStageLabel, msg = VENUE_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    bandPrefStage = TTK.Combobox(wtdeOptionsBand, values = [ven[0] for ven in VENUES], width = 27)
    bandPrefStage.grid(row = 5, column = 1, padx = 10, pady = 5, sticky = 'w')
    ToolTip(bandPrefStage, msg = VENUE_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Preferred Guitarist Highway
    GUITAR_HWY_PREFERRED_TIP = "Set the preferred highway that the guitarist will use.\n\n" \
                               "For a list of highway IDs, see the \"ID_Highways.txt\" file in your Resources folder.\n\n" \
                               "For modded highways, this is the folder name of the highway mod."
    bandPrefGuitaristHwyLabel = Label(wtdeOptionsBand, text = "                    Preferred Guitarist Highway:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    bandPrefGuitaristHwyLabel.grid(row = 1, column = 2, padx = 10, pady = 5, sticky = 'e')
    ToolTip(bandPrefGuitaristHwyLabel, msg = GUITAR_HWY_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    bandPrefGuitaristHwy = TTK.Entry(wtdeOptionsBand, width = 30)
    bandPrefGuitaristHwy.grid(row = 1, column = 3, pady = 5, sticky = 'w')
    ToolTip(bandPrefGuitaristHwy, msg = GUITAR_HWY_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Preferred Bassist Highway
    BASS_HWY_PREFERRED_TIP = "Set the preferred highway that the bassist will use.\n\n" \
                             "For a list of highway IDs, see the \"ID_Highways.txt\" file in your Resources folder.\n\n" \
                             "For modded highways, this is the folder name of the highway mod."
    bandPrefBassistHwyLabel = Label(wtdeOptionsBand, text = "                    Preferred Bassist Highway:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    bandPrefBassistHwyLabel.grid(row = 2, column = 2, padx = 10, pady = 5, sticky = 'e')
    ToolTip(bandPrefBassistHwyLabel, msg = BASS_HWY_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    bandPrefBassistHwy = TTK.Entry(wtdeOptionsBand, width = 30)
    bandPrefBassistHwy.grid(row = 2, column = 3, pady = 5, sticky = 'w')
    ToolTip(bandPrefBassistHwy, msg = BASS_HWY_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Preferred Drummer Highway
    DRUM_HWY_PREFERRED_TIP = "Set the preferred highway that the drummer will use.\n\n" \
                             "For a list of highway IDs, see the \"ID_Highways.txt\" file in your Resources folder.\n\n" \
                             "For modded highways, this is the folder name of the highway mod."
    bandPrefDrummerHwyLabel = Label(wtdeOptionsBand, text = "                    Preferred Drummer Highway:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    bandPrefDrummerHwyLabel.grid(row = 3, column = 2, padx = 10, pady = 5, sticky = 'e')
    ToolTip(bandPrefDrummerHwyLabel, msg = DRUM_HWY_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    bandPrefDrummerHwy = TTK.Entry(wtdeOptionsBand, width = 30)
    bandPrefDrummerHwy.grid(row = 3, column = 3, pady = 5, sticky = 'w')
    ToolTip(bandPrefDrummerHwy, msg = DRUM_HWY_PREFERRED_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Guitar Strum Animations
    guitarStrumAnim = StringVar()
    GTR_STRUM_ANIM_TIP = "Set the preferred guitar strum animations for the characters."
    bandGuitarStrumAnimLabel = Label(wtdeOptionsBand, text = "Guitar Strum Animations:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    bandGuitarStrumAnimLabel.grid(row = 6, column = 0, padx = 10, pady = 5, sticky = 'e')
    ToolTip(bandGuitarStrumAnimLabel, msg = GTR_STRUM_ANIM_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    bandGuitarStrumAnim = TTK.OptionMenu(wtdeOptionsBand, guitarStrumAnim, *[""] + [anim[0] for anim in BASS_STRUM_ANIMS])
    bandGuitarStrumAnim.config(width = 25)
    bandGuitarStrumAnim.grid(row = 6, column = 1, padx = 10, pady = 5, sticky = 'w')
    ToolTip(bandGuitarStrumAnim, msg = GTR_STRUM_ANIM_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Bass Strum Animations
    bassStrumAnim = StringVar()
    BAS_STRUM_ANIM_TIP = "Set the preferred bass strum animations for the characters."
    bandBassStrumAnimLabel = Label(wtdeOptionsBand, text = "Bass Strum Animations:", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO, justify = 'left')
    bandBassStrumAnimLabel.grid(row = 7, column = 0, padx = 10, pady = 5, sticky = 'e')
    ToolTip(bandBassStrumAnimLabel, msg = BAS_STRUM_ANIM_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    bandBassStrumAnim = TTK.OptionMenu(wtdeOptionsBand, bassStrumAnim, *[""] + [anim[0] for anim in BASS_STRUM_ANIMS])
    bandBassStrumAnim.config(width = 25)
    bandBassStrumAnim.grid(row = 7, column = 1, padx = 10, pady = 5, sticky = 'w')
    ToolTip(bandBassStrumAnim, msg = BAS_STRUM_ANIM_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

# Execute tab code.
BandSettings()

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
        autoVenueSelect = TTK.Combobox(autoSettingsFrame, width = 25, values = [ven[0] for ven in VENUES], textvariable = autoVenue)
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
# Debug Tab
# 
# Used to adjust various debug-related settings in GHWT: DE.
# ===========================================================================================================
# Main DebugSettings class.
class DebugSettings():
    """
    Debug settings tab.
    \n
    This class is responsible for creating the widgets on the screen for the Debug tab.
    """
    # Title text with the purpose of the tab.
    DEBUG_TITLE_TEXT = "Debug Settings: Edit debug specific settings.\nHover over any option to see what it does!"
    debugTitleLabel = Label(wtdeOptionsDebug, text = DEBUG_TITLE_TEXT, bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO_HEADER, justify = 'left', anchor = 'w')
    debugTitleLabel.place(x = 0, y = 0)
    
    # Fix Note Limit
    fixNoteLimit = StringVar()
    FIX_NOTE_LIMIT_TIP = "Fix the note limit from the default 4,096 note limit.\n\n" \
                         "Note that not everyone has this enabled, and if you have songs imported with\n" \
                         "over 4,096 notes, other people will have to enable this for your song to\n" \
                         "work correctly in their installation of WTDE."
    debugFixNoteLimit = TTK.Checkbutton(wtdeOptionsDebug, text = "Fix Note Limit", variable = fixNoteLimit, onvalue = '1', offvalue = '0')
    debugFixNoteLimit.place(x = 20, y = 45)
    ToolTip(debugFixNoteLimit, msg = FIX_NOTE_LIMIT_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Fix Memory Handler
    fixMemoryHandler = StringVar()
    FIX_MEMORY_HANDLER_TIP = "Fixes the memory handler. This extends memory limits, shows errors if compact pools\n" \
                             "run out of bounds, etc.\n\n" \
                             "Warning: It is HEAVILY encouraged that you DON'T disable this."
    debugFixMemHandler = TTK.Checkbutton(wtdeOptionsDebug, text = "Fix Memory Handler", variable = fixMemoryHandler, onvalue = '1', offvalue = '0', command = lambda: warn_memory_deselect(DebugSettings.fixMemoryHandler))
    debugFixMemHandler.place(x = 20, y = 76)
    ToolTip(debugFixMemHandler, msg = FIX_MEMORY_HANDLER_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Open Debug Console
    loggerConsole = StringVar()
    DEBUG_CONSOLE_TIP = "Opens the debug console in the background while WTDE is open."
    debugLoggerConsole = TTK.Checkbutton(wtdeOptionsDebug, text = "Open Debug Console", variable = loggerConsole, onvalue = '1', offvalue = '0')
    debugLoggerConsole.place(x = 20, y = 107)
    ToolTip(debugLoggerConsole, msg = DEBUG_CONSOLE_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Write Debug Log
    writeFile = StringVar()
    WRITE_DEBUG_LOG_TIP = "Write a file to the disk that holds the debug log written by WTDE during execution.\n\n" \
                          "This shouldn't be disabled, as it helps to debug crashes and other various issues."
    debugWriteFile = TTK.Checkbutton(wtdeOptionsDebug, text = "Write Debug Log", variable = writeFile, onvalue = '1', offvalue = '0')
    debugWriteFile.place(x = 20, y = 138)
    ToolTip(debugWriteFile, msg = WRITE_DEBUG_LOG_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Skip Song Logging
    disableSongLogging = StringVar()
    SKIP_SONG_LOGGING_TIP = "Turn ON or OFF debug logging while playing songs.\n\n" \
                            "While songs are running in-game, this will disable any sort of logging to the debug log,\n" \
                            "which may improve performance slightly. However, while OFF in the event of crashes\n" \
                            "that occur mid-song, this won't exhibit a helpful debug log."
    debugWriteFile = TTK.Checkbutton(wtdeOptionsDebug, text = "Skip Song Logging", variable = disableSongLogging, onvalue = '1', offvalue = '0')
    debugWriteFile.place(x = 20, y = 169)
    ToolTip(debugWriteFile, msg = SKIP_SONG_LOGGING_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # DLC Sync Debugging
    debugDLCSync = StringVar()
    DLC_SYNC_DEBUG_TIP = "Enable or disable song syncing debugging.\n\n" \
                        "While playing online, a sync is performed to ensure all players have\n" \
                        "identical copies of the same songs. If this is ON, this will write\n" \
                        "all song syncing information to the debug log."
    debugDLCSyncOption = TTK.Checkbutton(wtdeOptionsDebug, text = "DLC Sync Debugging", variable = debugDLCSync, onvalue = '1', offvalue = '0')
    debugDLCSyncOption.place(x = 20, y = 200)
    ToolTip(debugDLCSyncOption, msg = DLC_SYNC_DEBUG_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # DLC Sync Debugging
    fixFSBObjects = StringVar()
    FIX_FSB_OBJECTS_TIP = "Enable or disable fixing FMOD Sound Bank objects."
    debugFixFSBObjectsOption = TTK.Checkbutton(wtdeOptionsDebug, text = "Fix FMOD Sound Bank Objects", variable = fixFSBObjects, onvalue = '1', offvalue = '0')
    debugFixFSBObjectsOption.place(x = 20, y = 231)
    ToolTip(debugFixFSBObjectsOption, msg = FIX_FSB_OBJECTS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # More Optimized Saves
    extraOptimizedSaves = StringVar()
    MORE_OPTIMIZED_SAVES_TIP = "Makes the save functionality more optimized."
    debugExtraOptimizedSavesOption = TTK.Checkbutton(wtdeOptionsDebug, text = "More Optimized Saves", variable = extraOptimizedSaves, onvalue = '1', offvalue = '0')
    debugExtraOptimizedSavesOption.place(x = 20, y = 262)
    ToolTip(debugExtraOptimizedSavesOption, msg = MORE_OPTIMIZED_SAVES_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Debug Saves
    debugSaves = StringVar()
    DEBUG_SAVES_TIP = "Enables debug functionality for save files."
    debugDebugSavesOption = TTK.Checkbutton(wtdeOptionsDebug, text = "Debug Save Files", variable = debugSaves, onvalue = '1', offvalue = '0')
    debugDebugSavesOption.place(x = 20, y = 293)
    ToolTip(debugDebugSavesOption, msg = DEBUG_SAVES_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

    # Show Debug Warnings
    showWarnings = StringVar()
    SHOW_WARNS_TIP = "Turn ON or OFF warning messages in the top left corner of the screen. Useful for debugging!"
    debugShowWarnings = TTK.Checkbutton(wtdeOptionsDebug, text = "Show Debug Warnings", variable = showWarnings, onvalue = '1', offvalue = '0')
    debugShowWarnings.place(x = 20, y = 324)
    ToolTip(debugShowWarnings, msg = SHOW_WARNS_TIP, delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

# Execute tab code.
DebugSettings()

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
    creditsMembersFrame.pack(fill = 'x', anchor = 'center', padx = 120)

    # Add the names of the members of the WTDE team into the frame.
    wtde_add_credits(creditsMembersFrame, resource_path('res/WTDECreditsNames.csv'))

    # Second line of credits text.
    TAB_CREDITS_TEXT2 = "A special thanks to our development testers and of course, all of you, the players, modders, content creators, and everything in between!\n\n" \
                        "Making your Guitar Hero World Tour experience better, one update at a time!\n\n" \
                        "GHWT: DE and Fretworks are not associated with Activision, Neversoft, Beenox, Underground Development, or RedOctane in any way, shape, or form.\n" \
                        "GHWT: DE is and always will be a non-profit fan-made project."
    creditsTextLine2 = Label(wtdeOptionsCredits, bg = BG_COLOR, fg = FG_COLOR, text = TAB_CREDITS_TEXT2, font = FONT_INFO, justify = 'center')
    creditsTextLine2.pack(fill = 'x', pady = 10)

    # Social links frame.
    creditsSocialsFrame = Frame(wtdeOptionsCredits, bg = BG_COLOR)
    creditsSocialsFrame.pack(pady = 10)

    # Button width for the socials buttons.
    SOCIAL_BUTTON_WIDTH = 25
    SOCIAL_BUTTON_PADX = 15

    # GHWT: DE Website
    creditsWTDESite = TTK.Button(creditsSocialsFrame, text = "GHWT: DE Website", width = SOCIAL_BUTTON_WIDTH, command = lambda: WEB.open("https://ghwt.de"), takefocus = False)
    creditsWTDESite.grid(row = 0, column = 0, padx = SOCIAL_BUTTON_PADX)

    # WTDE Discord
    creditsWTDEDiscord = TTK.Button(creditsSocialsFrame, text = "GHWT: DE Discord", width = SOCIAL_BUTTON_WIDTH, command = lambda: WEB.open("https://discord.gg/HVECPzkV4u"), takefocus = False)
    creditsWTDEDiscord.grid(row = 0, column = 1, padx = SOCIAL_BUTTON_PADX)

    # WTDE Twitter
    creditsWTDETwitter = TTK.Button(creditsSocialsFrame, text = "GHWT: DE Twitter", width = SOCIAL_BUTTON_WIDTH, command = lambda: WEB.open("https://twitter.com/ghwtde"), takefocus = False)
    creditsWTDETwitter.grid(row = 0, column = 2, padx = SOCIAL_BUTTON_PADX)

    # Fretworks GitGud
    creditsFretworksGit = TTK.Button(creditsSocialsFrame, text = "Fretworks GitGud", width = SOCIAL_BUTTON_WIDTH, command = lambda: WEB.open("https://gitgud.io/fretworks"), takefocus = False)
    creditsFretworksGit.grid(row = 0, column = 3, padx = SOCIAL_BUTTON_PADX)

# Execute tab code.
CreditsTab()

# ===========================================================================================================
# Start Program
# 
# Start the execution of the program (mainloop of Tk).
# ===========================================================================================================
# Run sanity check before we import ANY settings!
debug_add_entry("[ConfigParser] Ready settings import; Initializing sanity check")
wtde_verify_config()

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