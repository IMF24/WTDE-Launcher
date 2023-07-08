from launcher_constants import VERSION
from cmd_colors import *
import os as OS
import sys as SYS

arguments = SYS.argv

print(f"{BLUE}-------------------------------")
print(f"{LIGHT_BLUE}Please wait, compiling build...")
print(f"{BLUE}-------------------------------{WHITE}")

OS.system(f"python -m PyInstaller -F --clean -y -n \"GHWT Definitive Launcher++ (V{VERSION})\" --add-data=\"res;res\" --windowed --icon=\"res/icon.ico\" main.py")

print(f"{GREEN}Done compiling the EXE!\n{YELLOW}Cleaning up files...")

specFile = f"GHWT Definitive Launcher++ (V{VERSION}).spec"

if (OS.path.exists(specFile)): OS.remove(specFile)

print(f"{GREEN}At long last, all done!")

input(f"{LIGHT_BLUE}? {WHITE}Press ENTER to exit the EXE builder. ")

try: OS.system('cls')
except: OS.system('clear')