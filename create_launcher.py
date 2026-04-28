import os
import winshell
from win32com.client import Dispatch

def create_launch_icon():
    desktop = winshell.desktop()
    path = os.path.join(desktop, "HunterOS.lnk")
    target = os.path.join(os.getcwd(), "launch_hunteros.bat")
    
    # Create the batch file first
    with open("launch_hunteros.bat", "w") as f:
        f.write("@echo off\n")
        f.write("echo --- Initializing HunterOS Ecosystem ---\n")
        f.write("start cmd /k \"cd backend && python -m uvicorn app.main:app --reload\"\n")
        f.write("start cmd /k \"cd frontend && npm run dev\"\n")
        f.write("echo HunterOS is now launching. Check terminals for status.\n")
        f.write("pause\n")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = os.getcwd()
    shortcut.IconLocation = target
    shortcut.save()
    
    print(f"[SYSTEM] HunterOS Launch Icon created on Desktop: {path}")

if __name__ == "__main__":
    try:
        create_launch_icon()
    except Exception as e:
        print(f"[ERROR] Failed to create launch icon: {e}")
        # Fallback to simple batch file print
        print("Please run launch_hunteros.bat manually to start the system.")
