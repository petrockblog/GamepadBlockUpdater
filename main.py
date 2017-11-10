import tkinter as tk
from tkinter import ttk
import serial
import time
import sys
import glob
import re
from subprocess import call
import requests
from requests import get  # to make GET request

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.title("GamepadBlock Updater")

        self.serialPort = tk.StringVar()
        self.extractedVersion = ""

        self.recentFirmwareVersion = tk.Label(self, text="", relief="sunken", justify="center")
        self.recentFirmwareVersion.grid(row=1, column=0, pady=5, padx=5, columnspan=2, sticky=tk.E+tk.W)

        self.step_1_label = tk.Label(self, text="Step 1: Connect the GamepadBlock to your PC")
        self.step_1_label.grid(row=2, column=0, columnspan=2, sticky='W', pady=5, padx=5)

        self.step_3_label = tk.Label(self, text="Step 3: Select the COM port of the GamepadBlock")
        self.step_3_label.grid(row=4, column=0, sticky="W", pady=5, padx=5)

        self.step_3_cbox = ttk.Combobox(self, textvariable=self.serialPort, value=self.serial_ports(), state="readonly")
        self.step_3_cbox.grid(row=4, column=1, pady=5, padx=5, sticky=tk.E+tk.W)
        self.step_3_cbox.bind("<<ComboboxSelected>>", self.readVersion)

        self.step_2_label = tk.Label(self, text="Step 2: Refresh the list of COM ports").grid(row=3, column=0, sticky="W", pady=5, padx=5)
        self.step_2_button = tk.Button(self, text="Refresh", command=self.refreshSerialPorts).grid(row=3, column=1, pady=5, padx=5, sticky=tk.E+tk.W)

        self.versionLabel = tk.Label(self, text="", relief="sunken", justify="center")
        self.versionLabel.grid(row=5, column=0, pady=5, padx=5, columnspan=2, sticky=tk.E+tk.W)

        self.step_4_label = tk.Label(self, text="Step 4: Press the Reset button on the GamepadBlock").grid(row=6, column=0, columnspan=2, sticky="W", pady=5, padx=5)
        self.step_4_button = tk.Button(self, text="Ok, I have pressed the reset button", command=self.resetPressed, state="disabled")
        self.step_4_button.grid(row=6, column=1, pady=5, padx=5, sticky=tk.E+tk.W)

        self.step_5_label = tk.Label(self, text="Step 5: Download the new firmware to the GamepadBlock").grid(row=7, column=0, sticky="W", pady=5, padx=5)
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
        self.step_3_cbox['values'] = self.serial_ports()

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
        ser = serial.Serial(self.serialPort.get(), 115200, timeout=1)  # open serial port
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
        else:
            print("Did not find any GamepadBlock")
            self.versionLabel['text'] = "INFO: Did not find GamepadBlock. Please check concection or try another COM port."
            self.step_4_button['state'] = "disabled"
            self.step_5_button['state'] = "disabled"

    def downloadFirmware(self):
        self.downloadInfo['text'] = "Started update process ..."
        self.update()
        returnValue = call(["avrdude","-p","m32u2","-c","avr109","-P",self.serialPort.get(),"-u","-U","flash:w:currentFirmware.hex:a"])
        if returnValue == 0:
            self.downloadInfo['text'] = "Update finished successfully."
        else:
            self.downloadInfo['text'] = "Update was not successful (error code " + str(returnValue) + ")."

    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

root = tk.Tk()
root.resizable(width=False, height=False)
app = Application(master=root)
app.mainloop()
