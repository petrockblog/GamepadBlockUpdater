import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import serial
import time
import sys
import glob
import re
from subprocess import call

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.step_2_cbox = None
        self.serialPort = tk.StringVar()
        self.extractedVersion = ""
        self.firmwareFile = ""
        self.pack()
        self.create_widgets(self.serialPort)

    def create_widgets(self, serialPort):
        self.title = ttk.Label(self, text="GamepadBlock Firmware Updater").grid(row=0, column=0, columnspan=2, pady=5, padx=5)
        self.step_1_label = ttk.Label(self, text="Step 1: Connect the GamepadBlock to your PC").grid(row=1, column=0, columnspan=2, sticky='W', pady=5, padx=5)
        self.step_2_label = ttk.Label(self, text="Step 2: Select the COM port").grid(row=2, column=0, sticky="W", pady=5, padx=5)
        self.step_2_cbox = ttk.Combobox(self, textvariable=serialPort, value=self.serial_ports()).grid(row=2, column=1, pady=5, padx=5)
        self.step_3_label = ttk.Label(self, text="Step 3: Read Firmware version of GamepadBlock").grid(row=3, column=0, sticky="W", pady=5, padx=5)
        self.step_3_button = ttk.Button(self, text="Read Version", command=self.readVersion).grid(row=3, column=1, pady=5, padx=5)
        self.step_4_button = ttk.Button(self, text="Browse", command=self.load_file, width=10).grid(row=4,column=1, pady=5, padx=5)
        self.step_4_label = ttk.Label(self, text="Step 4: Press the Reset button on the GamepadBlock").grid(row=4, column=0, columnspan=2, sticky="W", pady=5, padx=5)
        self.step_5_label = ttk.Label(self, text="Step 5: Download the new firmware to the GamepadBlock").grid(row=5, column=0, sticky="W", pady=5, padx=5)
        self.step_5_button = ttk.Button(self, text="Start Download", command=self.downloadFirmware).grid(row=5, column=1, pady=5, padx=5)

    def readVersion(self):
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
        else:
            print("Did not find any GamepadBlock")

    def load_file(self):
        fname = askopenfilename(filetypes=(("Template files", "*.hex"),
                                           ("All files", "*.*")))
        if fname:
            try:
                self.firmwareFile = fname
                print("Selected firmware file " + self.firmwareFile)
            except:  # <- naked except is a bad idea
                showerror("Open Firmware File", "Failed to read file\n'%s'" % fname)
            return

    def downloadFirmware(self):
        call(["avrdude","-p","m32u2","-c","avr109","-P",self.serialPort.get(),"-u","-U","flash:w:"+self.firmwareFile+":a"])

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
app = Application(master=root)
app.mainloop()
