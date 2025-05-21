import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
import shutil
import time
import os
from threading import Thread
import tkinter as tk
from tkinter import messagebox

def copy_files(source, destination):
    try:
        # Copy the files from source to destination
        shutil.copytree(source, destination)
        return True
    except Exception as e:
        print("Error:", e)
        return False

def on_exit():
    app.quit()

def show_message(title, message):
    # Show a message box using tkinter
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()

def wait_and_copy_files(tray_icon):
    source_checked = False  # Flag to check if source drive has been checked
    try:
        source_path = None
        while True:
            # Check if the source drive is connected only once
            if not source_checked:
                source_path = find_source_drive()
                if source_path:
                    print(f"Source drive found: {source_path}")
                    source_checked = True  # Set the flag to True after checking
                else:
                    # Wait for 1 second before checking again
                    time.sleep(1)
                    continue  # Skip the rest of the loop and start from the beginning

            # Continue with the copying process
            destination_path = "D:/Flash"
            success = copy_files(source_path, destination_path)

            if success:
                show_message("Error", "There is a problems!")
            else:
                show_message("error", "There is a problem!")

            # Wait for 5 seconds before checking again
            time.sleep(18000)
    except Exception as e:
        print("Error:", e)
        show_message("Error", "There is a problem!")

def find_source_drive():
    possible_drives = ['A:', 'B:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:']
    for drive in possible_drives:
        if os.path.exists(drive) and os.listdir(drive):
            return drive
    return None

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create system tray icon
    tray_icon = QSystemTrayIcon(QIcon("icon.png"), app)
    tray_icon.setToolTip("My Copy Icon")

    # Create menu for the system tray icon
    menu = QMenu()
    exit_action = QAction("Exit", parent=None)
    exit_action.triggered.connect(on_exit)
    menu.addAction(exit_action)
    tray_icon.setContextMenu(menu)

    # Show the system tray icon
    tray_icon.show()

    # Start the thread for continuous monitoring and copying
    Thread(target=wait_and_copy_files, args=(tray_icon,)).start()

    sys.exit(app.exec_())
