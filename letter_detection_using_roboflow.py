# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:31:14 2023

@author: Dell
"""

#!pip install roboflow

import cv2

from roboflow import Roboflow
rf1 = Roboflow(api_key="FZD7O1HoTTFqlexkwNZi")
project1 = rf1.workspace("pavan-kalyan-o41rw").project("letter_detection-4i91k")
model1 = project1.version(1).model


letter_map = { 0: 'a',1: 'b',2: 'c',3:'d',4:'e',5:'f',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'0',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'
}

cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    results1= model1.predict(gray, confidence=40, overlap=30).json()
    
    print(results1)
    
    predictions = results1["predictions"]
    
    if len(predictions) >0:
        for pred in predictions:
            width = int(pred['width'])
            height = int(pred['height'])
            x1 = int(pred['x'])- int(width/2)
            y1 = int(pred['y']) - int(height/2)
            x2 = int(pred['x']) +  int(width/2)
            y2 = int(pred['y']) + int(height/2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            letter_num = int(pred['class'])
            letter = letter_map[letter_num]
            print(letter)
            
        
    
    cv2.imshow("Frame", frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object and close all windowsq
cap.release()
cv2.destroyAllWindows()