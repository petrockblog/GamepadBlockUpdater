import tkinter as tk
import serial
import serial.tools.list_ports
import time
import sys
import os
from subprocess import call
import requests
from requests import get  # to make GET request
import platform

if 0:
    import UserList
    import UserString
    import UserDict
    import itertools
    import collections
    import future.backports.misc
    import commands
    import base64
    import __buildin__
    import math
    import reprlib
    import functools
    import re
    import subprocess

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.title("GamepadBlock Updater")

        self.serialPort = None
        self.extractedVersion = None

        self.recentFirmwareVersion = tk.Label(self, text="", relief="sunken", justify="center")
        self.recentFirmwareVersion.grid(row=1, column=0, pady=5, padx=5, columnspan=2, sticky=tk.E+tk.W)

        self.step_1_label = tk.Label(self, text="Step 1: Connect the GamepadBlock to your PC")
        self.step_1_label.grid(row=2, column=0, columnspan=2, sticky='W', pady=5, padx=5)

        self.step_2_label = tk.Label(self, text="Step 2: Search for GamepadBlock").grid(row=3, column=0, sticky="W", pady=5, padx=5)
        self.step_2_button = tk.Button(self, text="Start Search", command=self.refreshSerialPorts).grid(row=3, column=1, pady=5, padx=5, sticky=tk.E+tk.W)

        self.versionLabel = tk.Label(self, text="", relief="sunken", justify="center")
        self.versionLabel.grid(row=5, column=0, pady=5, padx=5, columnspan=2, sticky=tk.E+tk.W)

        self.step_4_label = tk.Label(self, text="Step 3: Press the Reset button on the GamepadBlock").grid(row=6, column=0, columnspan=2, sticky="W", pady=5, padx=5)
        self.step_4_button = tk.Button(self, text="Ok, I have pressed the reset button", command=self.resetPressed, state="disabled")
        self.step_4_button.grid(row=6, column=1, pady=5, padx=5, sticky=tk.E+tk.W)

        self.step_5_label = tk.Label(self, text="Step 4: Download the new firmware to the GamepadBlock").grid(row=7, column=0, sticky="W", pady=5, padx=5)
        self.step_5_button = tk.Button(self, text="Start Download", command=self.downloadFirmware, state="disabled")
        self.step_5_button.grid(row=7, column=1, pady=5, padx=5, sticky=tk.E+tk.W)

        self.downloadInfo = tk.Label(self, text="", relief="sunken", justify="center")
        self.downloadInfo.grid(row=8, column=0, pady=5, padx=5, columnspan=2, sticky=tk.E+tk.W)

        self.infoLabel = tk.Label(self, text="gamepadblock.petrockblock.com").grid(row=10, column=0, sticky="W", pady=5, padx=5)
        self.exitButton = tk.Button(self, text="Quit", command=self.quit).grid(row=10, column=1, pady=5, padx=5, sticky=tk.E)

        self.pack()

        r = requests.get("https://github.com/petrockblog/GamepadBlockUpdater/releases/latest")
        downloadURL = r.url
        self.currentVersion = self.findVersionString(downloadURL)
        self.recentFirmwareVersion['text'] = "INFO: The most recent firmware version is " + self.currentVersion
        downloadURL = downloadURL.replace("releases/tag", "releases/download")
        downloadURL += "/firmware.hex"
        self.downloadFile(downloadURL, "currentFirmware.hex")

    def resetPressed(self):
        self.step_5_button['state'] = "normal"

    def refreshSerialPorts(self):
        ports = list(serial.tools.list_ports.comports())
        found = False
        for port in ports:
            index = port.hwid.find("16D0:0BCC")
            if index >= 0:
                self.serialPort = port.device
                found = True
                break
        if not found:
            self.serialPort = None
        self.readVersion()

    def findVersionString(self, url):
        parts = url.split("tag/")
        return parts[1]

    def downloadFile(self, url, file_name):
        # open in binary mode
        with open(file_name, "wb") as file:
            # get request
            response = get(url)
            # write to file
            file.write(response.content)

    def readVersion(self, event=None):
        if self.serialPort is not None:
            ser = serial.Serial(self.serialPort, 115200, timeout=1)  # open serial port
            print(ser.name)  # check which port was really used
            ser.close()
            ser.open()
            ser.write("v".encode())
            time.sleep(0.5)
            read_val = ser.read(size=64)
            ser.close()
            versionString = read_val.decode("utf-8")
            self.extractedVersion = re.search(r'\s*([\d.]+)', versionString)
        if self.extractedVersion is not None:
            self.extractedVersion = self.extractedVersion.group(1)
            print("Found version " + self.extractedVersion)
            self.versionLabel['text'] = "INFO: Found GamepadBlock. The firmware version of it is  " + self.extractedVersion
            self.step_4_button['state'] = "active"
            self.step_5_button['state'] = "disabled"
        else:
            print("Did not find any GamepadBlock")
            self.versionLabel['text'] = "INFO: Did not find GamepadBlock. Please check connection or try to reconnect."
            self.step_4_button['state'] = "disabled"
            self.step_5_button['state'] = "disabled"

    def downloadFirmware(self):
        ports = list(serial.tools.list_ports.comports())
        found = False
        for port in ports:
            if port.hwid.find("03EB:204A") >= 0:
                self.serialPort = port.device
                found = True
                break
        if found:
            self.downloadInfo['text'] = "Started update process ..."
            self.update()
            time.sleep(2)
            if platform.system() == "Darwin":
                toolFile = self.resource_path(os.path.join("tools/avrdude/mac/", "avrdude"))
            elif platform.system() == "Windows":
                toolFile = self.resource_path(os.path.join("tools/avrdude/windows/", "avrdude.exe"))

            returnValue = call([toolFile, "-p","m32u2","-c","avr109","-P",self.serialPort,"-u","-U","flash:w:currentFirmware.hex:a"])
            if returnValue == 0:
                self.downloadInfo['text'] = "Update finished successfully."
            else:
                self.downloadInfo['text'] = "Update was not successful (error code " + str(returnValue) + ")."
        else:
            self.downloadInfo['text'] = "Error: Cannot communicate with GamepadBlock."

    def resource_path(self, relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)

root = tk.Tk()
root.resizable(width=False, height=False)
app = Application(master=root)
app.mainloop()
