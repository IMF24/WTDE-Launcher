# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#     W T D E     L A U N C H E R + +     B U I L D     C O M P I L E R
#
#       The script for compiling builds for the GHWT: Definitive Edition Launcher++.
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
from launcher_constants import VERSION
from cmd_colors import *
import os as OS
import sys as SYS
import shutil as SHUT
import configparser as CF

config = CF.ConfigParser(strict = False, allow_no_value = True)

arguments = SYS.argv

if ("-H" in arguments) or ("-h" in arguments) or ("--help" in arguments):
    HELP_INFO = "Usage: python compile.py [args]\n\n" \
                "List of arguments:\n" \
                "   --help, -H, -h              Prints this message.\n" \
                "   --repo-build, -R            Make the EXE's file name be the one utilized in public WTDE builds.\n" \
                "   --sync, -S                  Sync the EXE file to the folder where the developers' repository is located. Requires a config.ini file."
    print(HELP_INFO)
    exit()

if ("-R") in (arguments) or ("--repo-build") in (arguments):
    dashNName = f"GHWT_Definitive_Launcher"
else:
    dashNName = f"GHWT Definitive Launcher++ (V{VERSION})"

if ("-S") in (arguments) or ("--sync") in (arguments):
    dashNName = f"GHWT_Definitive_Launcher"
    sendToDevRepoFolder = True
else:
    sendToDevRepoFolder = False

print(f"{BLUE}-------------------------------")
print(f"{LIGHT_BLUE}Please wait, compiling build...")
print(f"{BLUE}-------------------------------{WHITE}")

print(f"{YELLOW}Compiling build for launcher version {VERSION}...{WHITE}")

if ("-R") in (arguments) or ("--repo-build") in (arguments): print(f"{YELLOW}Compiling build for developers' repository...{WHITE}")
if ("-S") in (arguments) or ("--sync") in (arguments): print(f"{YELLOW}Will sync build to developers' repo!{WHITE}")

print(f"Ensuring modules are up to date...")

print(f"{LIGHT_RED}-- MODULE SCAN -----------------------------{WHITE}")

OS.system("pip install --upgrade PyInstaller")

print(f"{LIGHT_RED}-- END MODULE SCAN -------------------------{WHITE}")

cmd = f"python -m PyInstaller -F --clean -y -n \"{dashNName}\" --add-data=\"res;res\" --windowed --icon=\"res/icon.ico\" main.py"
print(f"Executing the following command: {cmd}")
OS.system(cmd)

print(f"{GREEN}Done compiling the EXE!\n{YELLOW}Cleaning up files...")

specFile = f"{dashNName}.spec"

if (OS.path.exists(specFile)): OS.remove(specFile)

if (sendToDevRepoFolder):
    print(f"{YELLOW}Syncing EXE to ghde_content...{WHITE}")

    if (not OS.path.exists('config.ini')):
        print(f"{RED}Error: No config.ini file existed, cannot sync!{WHITE}")

    else:
        config.read('config.ini')

        try:
            devRepoDir = config.get('DevConfig', 'DevRepo')

            if (OS.path.exists(f"{devRepoDir}\\Packages\\ghde_content\\Content\\GHWT_Definitive_Launcher.exe")):
                OS.remove(f"{devRepoDir}\\Packages\\ghde_content\\Content\\GHWT_Definitive_Launcher.exe")

            SHUT.copy("dist\\GHWT_Definitive_Launcher.exe", f"{devRepoDir}\\Packages\\ghde_content\\Content\\GHWT_Definitive_Launcher.exe")

            print(f"{GREEN}Compiled EXE synced to dev repo!{WHITE}")

        except Exception as exc:
            print(f"{RED}Error: Cannot sync to dev repo! Sync failed due to the following error: {exc}.{WHITE}")

print(f"{GREEN}At long last, all done!")

input(f"{LIGHT_BLUE}? {WHITE}Press ENTER to exit the EXE builder. ")

try: OS.system('cls')
except: OS.system('clear')