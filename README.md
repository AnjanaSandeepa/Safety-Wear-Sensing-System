# Safety-Wear-Sensing-System

![interface_photo](https://github.com/AnjanaSandeepa/Safety-Wear-Sensing-System/assets/119288138/f8156555-0a22-4408-b781-56b1f65dd75b)

Safety-Wear-based gate system, I used a machine learning model using Keras, a Tensorflow library in Python language. After building the model, I used OpenCV to detect whether a person is wearing Safety Wear or not in real-time. I used Tkinter to create my user interface.we can control system accuracy using the user interface

This system contains mainly four devices. They are a nodeMCU, camera(webcam), LED, buzzer, LCD, I2C, and servo. I used nodeMCU to control the servo, camera, LCD, LED and buzzer. If someone appears in front of the entrance wearing a Safety-Wear properly, then they will be let in. At the same time, my display will show “Safety-Wear Detected”. But if someone appears without a Safety-Wear then they will be denied entry, at the same time the system would display “Please wear the Safety-Wear” the person. This versatile system could be used with a variety of entrances with different gate and lock systems.The video of demo working project is given below:

## Video

https://github.com/AnjanaSandeepa/Safety-Wear-Sensing-System/assets/119288138/0badfe04-eeb9-4e58-bc69-6a864e89773f


# How to run the project

#### Step 1
You have to run 'train_safety_wear_detector.py' file in pycharm to create a model or you can use my previous trained models which I have provided in GitHub.
For training model file you need a dataset having two folders: 1. withSafetyWear 2. withOutSafetyWear. I also provided the dataset in GitHub.

#### Step 2
You have to run ‘myDetect.py’ file in pycharm. For running this file you need 'res10_300x300_ssd_iter_140000.caffemodel',  'deploy.prototxt' and model file which I have provided in the Github and you must connect your webcam with your PC but if you are using Laptop then you don't need any webcam.
If you run everything successfully then your camera will be opened and you can test if it works with the safety wear or not.

#### Step 3
Finally, you will add Serial Command to the safety_wear detection algorithm that will order the Arduino to send commands to the servo, buzzer, LED and LCD based on the state of detection. I have commented on the Arduino code in the myDetect.py file. If you want to use Arduino then first, you have to run and compile 'msdCode.ino' file on the nodeMCU board using Arduino Software. Next,  you have to connect your Arduino with your pc or laptop using a USB cable and then you have to comment out the Arduino code from  'myDetect.py' file and run the file. 

Remember you have to connect your nodeMCU with LCD, I2C, servo, LED and buzzer before running the code. 
the connection is given below:

## Diagram
![Screenshot 2023-05-11 233603](https://github.com/AnjanaSandeepa/Safety-Wear-Sensing-System/assets/119288138/97cb647d-50fa-4101-88c9-33c71d931537)

#### For LCD and I2C
###### you have to connect the SCL pin with nodeMCU digital pin D3
###### you have to connect the SDA pin with nodeMCU digital pin D4

#### For Servo 
###### you have to connect the servo with nodeMCU digital pin D5

#### For Buzzer
###### you have to connect the Buzzer with nodeMCU digital pin D7

#### For LED
###### you have to connect the LED red and green with nodeMCU digital pin D6 and D8


# Language: 
Python and Arduino.
# Library:
tensorflow, keras, imutils, cv2, numpy, time, os, serial, TKinter
# Hardware:
nodeMCU, servo, buzzer, LED, LCD, webcam.
# IDE: 
pycharm, Arduino Software.
