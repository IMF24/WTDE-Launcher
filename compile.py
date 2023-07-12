from launcher_constants import VERSION
from cmd_colors import *
import os as OS
import sys as SYS
import shutil as SHUT
import configparser as CF

config = CF.ConfigParser(strict = False, allow_no_value = True)

arguments = SYS.argv

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

if ("-R") in (arguments) or ("--repo-build") in (arguments): print(f"{YELLOW}Compiling build for developers' repository...{WHITE}")
if ("-S") in (arguments) or ("--sync") in (arguments): print(f"{YELLOW}Will sync build to developers' repo!{WHITE}")

OS.system(f"python -m PyInstaller -F --clean -y -n \"{dashNName}\" --add-data=\"res;res\" --windowed --icon=\"res/icon.ico\" main.py")

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