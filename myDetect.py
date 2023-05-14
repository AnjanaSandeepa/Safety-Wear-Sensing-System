# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os

from pynput.keyboard import Key, Controller

import tkinter
import tkinter.messagebox
import customtkinter
from builtins import str
from time import strftime
from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import threading

#For arduino connection
import serial
import struct

#For arduino connection
arduino = serial.Serial('COM3', 9600)

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class MyApp(customtkinter.CTk):

    LABEL = ""              # HEMET or Mask
    CATEGORY = ""           # helmet or mask
    MODEL = ""              # hemet_detector.model or mask_detector.model

    ACCURACY = 90.00        # Correct Percentage
    BYTE_COUNT = 50         # All frame count
    H_count = 30            # Correct frame count
    INTERVAL = 10           # Refresh time
    WAITING_TIME = 10       # customer receiving time

    lowConfidence = 0.75

    time_string = ""        # For set time
    Date_string = ""         # For set Date
    bool_alwaysON = 0       # For check alwaysON switch on or off
    bool_systemLOCK = 0     # For check alwaysON switch on or off
    x = 0

    def __init__(self):
        super().__init__()

        # configure window
        self.title("My app")
        self.geometry(f"{1100}x{600}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=8, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Safety Wear Sensing \n System", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 0))    #set sidebar caption


        self.image = customtkinter.CTkImage(light_image=Image.open(os.path.join('Logo.png')),size=(246, 400))
        self.image_label = customtkinter.CTkLabel(self.sidebar_frame, image=self.image)
        self.image_label.grid(row=1, column=0, padx=(0,100), pady=(0,0))    # set sidebar image

        self.time_string = strftime('%H:%M:%S %p')
        self.clock_label = customtkinter.CTkLabel(self.sidebar_frame, text=self.time_string, font=customtkinter.CTkFont(size=25, weight="bold"))
        self.clock_label.grid(row=1, column=0, padx=(180,0), pady=(60, 0))  # set the time

        self.Date_string = strftime('%A \n %x')
        self.Date_label = customtkinter.CTkLabel(self.sidebar_frame, text= self.Date_string, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.Date_label.grid(row=1, column=0, padx=(180,0), pady=(160, 0))  # set the date

        self.peopleCount_label = customtkinter.CTkLabel(self.sidebar_frame, text="People Count = 0", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.peopleCount_label.grid(row=4, column=0, padx=(0,0), pady=(0, 0))   # set the people count

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(5, 10))   # set the appearance mode

        ########################################################################################################################################

        # create slider and middle frame
        self.middle_frame = customtkinter.CTkFrame(self)
        self.middle_frame.grid(row=0,column=1, padx=(20, 0), pady=(20,0), sticky="nsew")
        self.middle_frame.grid_columnconfigure(1, weight=1)
        self.middle_frame.grid_rowconfigure(6, weight=1)

        self.label_slider = customtkinter.CTkLabel(self.middle_frame, text="CONTROL PANEL", font=customtkinter.CTkFont(size=20, weight="bold"),)
        self.label_slider.grid(row=0, column=0, padx=(10, 0), pady=(10, 15), sticky="ew")  #set sidebar main caption

        self.slider_1 = customtkinter.CTkSlider(self.middle_frame, from_=10, to=99)
        self.slider_1.grid(row=1, column=1, padx=(10, 10), pady=(20, 0), sticky="ew")
        self.label_1 = customtkinter.CTkLabel(self.middle_frame, text="ACCURECY", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_1.grid(row=1, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")
        self.lab_1 = customtkinter.CTkLabel(self.middle_frame, text= "90 %", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.lab_1.grid(row=1, column=2, padx=(20, 10), pady=(20, 0), sticky="ew")
        self.slider_1.bind("<ButtonRelease-1>", self.slider_changed_1)
        self.slider_1.set(90)
        self.slider_1.configure(state="disabled")

        self.slider_2 = customtkinter.CTkSlider(self.middle_frame, from_=10, to=99)
        self.slider_2.grid(row=2, column=1, padx=(10, 10), pady=(20, 0), sticky="ew")
        self.label_2 = customtkinter.CTkLabel(self.middle_frame, text="FRAME COUNT", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_2.grid(row=2, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")
        self.lab_2 = customtkinter.CTkLabel(self.middle_frame, text="50",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.lab_2.grid(row=2, column=2, padx=(20, 10), pady=(20, 0), sticky="ew")
        self.slider_2.bind("<ButtonRelease-1>", self.slider_changed_2)
        self.slider_2.set(50)
        self.slider_2.configure(state="disabled")

        self.slider_3 = customtkinter.CTkSlider(self.middle_frame, from_=10, to=99)
        self.slider_3.grid(row=3, column=1, padx=(10, 10), pady=(20, 0), sticky="ew")
        self.label_3 = customtkinter.CTkLabel(self.middle_frame, text="ACCURATE COUNT", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_3.grid(row=3, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")
        self.lab_3 = customtkinter.CTkLabel(self.middle_frame, text="30",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.lab_3.grid(row=3, column=2, padx=(20, 10), pady=(20, 0), sticky="ew")
        self.slider_3.bind("<ButtonRelease-1>", self.slider_changed_3)
        self.slider_3.set(30)
        self.slider_3.configure(state="disabled")

        self.slider_4 = customtkinter.CTkSlider(self.middle_frame, from_=10, to=99)
        self.slider_4.grid(row=4, column=1, padx=(10, 10), pady=(20, 0), sticky="ew")
        self.label_4 = customtkinter.CTkLabel(self.middle_frame, text="REFRESH TIME", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_4.grid(row=4, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")
        self.lab_4 = customtkinter.CTkLabel(self.middle_frame, text="40",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.lab_4.grid(row=4, column=2, padx=(20, 10), pady=(20, 0), sticky="ew")
        self.slider_4.bind("<ButtonRelease-1>", self.slider_changed_4)
        self.slider_4.set(40)
        self.slider_4.configure(state="disabled")

        self.slider_5 = customtkinter.CTkSlider(self.middle_frame, from_=10, to=99)
        self.slider_5.grid(row=5, column=1, padx=(10, 10), pady=(20, 0), sticky="ew")
        self.label_5 = customtkinter.CTkLabel(self.middle_frame, text="WAITING TIME",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_5.grid(row=5, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")
        self.lab_5 = customtkinter.CTkLabel(self.middle_frame, text="15 S",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.lab_5.grid(row=5, column=2, padx=(20, 10), pady=(20, 0), sticky="ew")
        self.slider_5.bind("<ButtonRelease-1>", self.slider_changed_5)
        self.slider_5.set(10)
        self.slider_5.configure(state="disabled")

        # create textbox area
        self.textbox = customtkinter.CTkTextbox(self, width=50)
        self.textbox.get("3.0", "3.0 lineend")
        self.textbox.grid(row=6, column=1, padx=(20, 0), pady=(0, 10), sticky="nsew")

    #############################################################################################################################################

        # create Selection frame
        self.selection_frame = customtkinter.CTkFrame(self)
        self.selection_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.lab_selection_group = customtkinter.CTkLabel(master=self.selection_frame, text="  SELECT YOUR OPTION:")
        self.lab_selection_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")   #set selection frame caption

        self.selected_var = tkinter.IntVar(value=0)

        self.btn_selection_mask = customtkinter.CTkRadioButton(master=self.selection_frame, variable=self.selected_var,value=0, text="FACE MASK")
        self.btn_selection_mask.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.btn_selection_helmet = customtkinter.CTkRadioButton(master=self.selection_frame, variable=self.selected_var,value=1, text="HELMET")
        self.btn_selection_helmet.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.btn_selection_goggles = customtkinter.CTkRadioButton(master=self.selection_frame, variable=self.selected_var,value=2, text="GOGGLES")
        self.btn_selection_goggles.grid(row=3, column=2, pady=10, padx=20, sticky="n")


        # create Control frame
        self.control_frame = customtkinter.CTkScrollableFrame(self, label_text="CONTROL PANEL")
        self.control_frame.grid(row=6, column=3, padx=(20, 0), pady=(0, 10), sticky="nsew")
        self.control_frame.grid_columnconfigure(0, weight=1)

        self.btn_start = customtkinter.CTkButton(master=self.control_frame, fg_color="transparent", border_width=2,text_color=("gray10", "#DCE4EE"), text="START", command=self.btn_start)
        self.btn_start.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.btn_stop = customtkinter.CTkButton(master=self.control_frame, fg_color="transparent",border_width=2, text_color=("gray10", "#DCE4EE"), text="STOP", command=self.btn_stop)
        self.btn_stop.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.sw_btn_alwaysON = customtkinter.CTkSwitch(master=self.control_frame, text="ALWAYS ON", command= self.alwaysON)
        self.sw_btn_alwaysON.grid(row=2, column=0, columnspan=1, padx=10, pady=(10,50), sticky="")

        self.sw_btn_systemLOCK = customtkinter.CTkSwitch(master=self.control_frame, text="SYSTEM LOCK", command= self.systemLOCK)
        self.sw_btn_systemLOCK.grid(row=2, column=0, columnspan=1, padx=10, pady=(50,10), sticky="")

        self.btn_admin = customtkinter.CTkButton(self.control_frame, text="ADMIN LOGIN", command=self.open_input_admin_event)
        self.btn_admin.grid(row=3, column=0, padx=10, pady=10)

    ############################################################################################################################################

    #use to print statement
    def print (self, string):
        self.textbox.insert(INSERT, self.time_string + "    --->  " + string + "\n")
        self.textbox.update()

    #set time
    def time(self):
        self.time_string = strftime('%H:%M:%S %p')  # time format
        self.clock_label.configure(text=self.time_string)
        self.clock_label.after(1000, self.time)

    #set appearance mode
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.print("APPEARANCE MODE CHANGE - " + new_appearance_mode )

    def slider_changed_1(self,event):
        self.lab_1.configure(text=str(round(self.slider_1.get()))+" %")

    def slider_changed_2(self,event):
        self.lab_2.configure(text=round(self.slider_2.get()))

    def slider_changed_3(self,event):
        self.lab_3.configure(text=round(self.slider_3.get()))

    def slider_changed_4(self,event):
        self.lab_4.configure(text=round(self.slider_4.get()))

    def slider_changed_5(self,event):
        self.lab_5.configure(text=str(round(self.slider_5.get()))+" S")

    #use for access admin
    def open_input_admin_event(self):
        self.dialog = customtkinter.CTkInputDialog(text="ENTER ADMIN PASSWORD:", title="ADMIN LOGIN")
        output = self.dialog.get_input()

        if(output== "*****"):
            self.print("LOGGED IN TO THE ADMIN ACCOUNT")

            self.slider_1.configure(state="normal")
            self.slider_2.configure(state="normal")
            self.slider_3.configure(state="normal")
            self.slider_4.configure(state="normal")
            self.slider_5.configure(state="normal")
        else:
            self.print(" *** IS NOT ADMIN PASSWORD")

    def alwaysON(self):
        if(self.bool_alwaysON == 1):

            self.print("ALWAYS OPEN MODE IS OFF")
            arduino.write(b'Q')
            self.bool_alwaysON = 0

            self.btn_selection_mask.configure(state="normal")
            self.btn_selection_helmet.configure(state="normal")
            self.btn_selection_goggles.configure(state="normal")
            self.slider_1.configure(state="normal")
            self.slider_2.configure(state="normal")
            self.slider_3.configure(state="normal")
            self.slider_4.configure(state="normal")
            self.slider_5.configure(state="normal")
            self.btn_start.configure(state="normal")
            self.btn_stop.configure(state="normal")
            self.btn_admin.configure(state="normal")

        else:
            self.print("ALWAYS OPEN MODE IS ON")
            arduino.write(b'P')
            self.bool_alwaysON = 1

            self.btn_selection_mask.configure(state="disabled")
            self.btn_selection_helmet.configure(state="disabled")
            self.btn_selection_goggles.configure(state="disabled")
            self.slider_1.configure(state="disabled")
            self.slider_2.configure(state="disabled")
            self.slider_3.configure(state="disabled")
            self.slider_4.configure(state="disabled")
            self.slider_5.configure(state="disabled")
            self.btn_start.configure(state="disabled")
            self.btn_stop.configure(state="disabled")
            self.btn_admin.configure(state="disabled")

    def systemLOCK(self):
        if(self.bool_systemLOCK==1):

            self.print("SYSTEM IS UNLOCK")
            self.bool_systemLOCK = 0

            self.btn_selection_mask.configure(state="normal")
            self.btn_selection_helmet.configure(state="normal")
            self.btn_selection_goggles.configure(state="normal")
            self.btn_start.configure(state="normal")
            self.btn_stop.configure(state="normal")
            self.btn_admin.configure(state="normal")

        else:
            self.print("SYSTEM IS LOCK")
            self.bool_systemLOCK = 1

            self.btn_selection_mask.configure(state="disabled")
            self.btn_selection_helmet.configure(state="disabled")
            self.btn_selection_goggles.configure(state="disabled")
            self.slider_1.configure(state="disabled")
            self.slider_2.configure(state="disabled")
            self.slider_3.configure(state="disabled")
            self.slider_4.configure(state="disabled")
            self.slider_5.configure(state="disabled")
            self.btn_start.configure(state="disabled")
            self.btn_stop.configure(state="disabled")
            self.btn_admin.configure(state="disabled")

    def btn_start(self):
        self.ACCURACY = self.slider_1.get()
        self.BYTE_COUNT = self.slider_2.get()
        self.H_count = self.slider_3.get()
        self.INTERVAL = self.slider_4.get()
        self.WAITING_TIME = self.slider_5.get()

        #arduino.write(struct.pack('BBBB', int(self.BYTE_COUNT), int(self.H_count), int(self.INTERVAL), int(self.WAITING_TIME)))


        self.print("SET ARGUMENT")
        cmd = str(round(int(self.BYTE_COUNT))) + str(round(int(self.H_count))) + str(round(int(self.INTERVAL))) + str(round(int(self.WAITING_TIME)))
        self.print("-------------"+cmd+"-------------")
        cmd = cmd + '\r'
        arduino.write(cmd.encode())
        time.sleep(2)

        self.print(" SELECTED WEAR      =" + str(self.selected_var.get()))
        self.print(" ACCURACY LEVEL     =" + str(self.ACCURACY))
        self.print(" BYTE_COUNT LEVEL   =" + str(self.BYTE_COUNT))
        self.print(" H_count LEVEL      =" + str(self.H_count))
        self.print(" INTERVAL           =" + str(self.INTERVAL))
        self.print(" WAITING TIME       =" + str(self.WAITING_TIME))

        if (self.selected_var.get() == 0):
            self.print("YOU SELECTED MASK")
            self.detect_mask()

        elif (self.selected_var.get()==1):
            self.print("YOU SELECTED HELMET")
            self.detect_helmet()

        elif (self.selected_var.get() == 2):
            self.print("YOU SELECTED GOGGLES")
            self.detect_goggles()

    def btn_stop(self):
        self.print("STOP THE SYSTEM")
        keyboard = Controller()
        keyboard.press("q")
        keyboard.release("q")

    def detect_mask(self):
        self.LABEL = "Mask"
        self.MODEL = "mask_detector.model"
        self.CATEGORY = "mask"
        self.start()

    def detect_helmet(self):
        self.LABEL = "HELMET"
        self.MODEL = "helmet_detector.model"
        self.CATEGORY = "helmet"
        self.start()

    def detect_goggles(self):
        self.LABEL = "GOGGLES"
        self.MODEL = "sunglass_detector.model"
        self.CATEGORY = "goggles"
        self.start()


    def detectAndPredictWear(self, frame, faceNet, maskNet):
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224), (104.0, 177.0, 123.0))
        faceNet.setInput(blob)
        detections = faceNet.forward()
        faces = []
        locs = []
        preds = []

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.lowConfidence:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
                face = frame[startY:endY, startX:endX]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)
                faces.append(face)
                locs.append((startX, startY, endX, endY))
        if len(faces) > 0:
            faces = np.array(faces, dtype="float32")
            preds = maskNet.predict(faces, batch_size=32)
        return (locs, preds)

    def start(self):
        prototxtPath = r"deploy.prototxt"
        weightsPath = r"res10_300x300_ssd_iter_140000.caffemodel"
        faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
        maskNet = load_model(self.MODEL)
        vs = VideoStream(src=0).start()

        while True:
            frame = vs.read()
            frame = imutils.resize(frame, 720, 300)
            (locs, preds) = self.detectAndPredictWear(frame, faceNet, maskNet)
            for (box, pred) in zip(locs, preds):  #
                (startX, startY, endX, endY) = box
                (wear, withoutWear) = pred
                label = self.LABEL if wear > withoutWear else "No " + self.LABEL
                color = (0, 255, 0) if label == self.LABEL else (0, 0, 255)

                label_text = "{}: {:.2f}%".format(label, max(wear, withoutWear) * 100)
                cv2.putText(frame, label_text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

                if label == self.LABEL:  ##########################
                    if self.ACCURACY <= float(max(wear, withoutWear) * 100):

                        print("+++ ACCESS GRANTED")
                        self.print("+++ ACCESS GRANTED")
                        # For arduino connection
                        arduino.write(b'H')
                    else:
                        self.print("--- ACCESS GRANTED")
                        # For arduino connection
                        arduino.write(b'L')
                else:
                    self.print("ACCESS DENIED")
                    # For arduino connection
                    arduino.write(b'L')

                self.textbox.delete('current linestart', 'current lineend+1c')

            if (arduino.inWaiting()> self.x):
                self.x = arduino.inWaiting()
                self.print("PEOPLE COUNT" + str(self.x))
                self.peopleCount_label.configure(text="People count = " + str(self.x))

            cv2.imshow("Press q to quit", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                arduino.write(b'A')
                print("kk")
                break

        cv2.destroyAllWindows()
        vs.stop()


if __name__ == "__main__":
    app = MyApp()
    app.time()
    app.print(" OPENED")

    app.mainloop()
