# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 16:12:21 2023

@author: Dell
"""

# !pip install roboflow
import cv2
# from roboflow import Roboflow
# rf = Roboflow(api_key="1qfkURW6WrDWsY8zMZWL")
# project = rf.workspace("school-u8o7p").project("letter_detection-pfx1s")
# dataset = project.version(1).model
    
# !pip install roboflow

# from roboflow import Roboflow
# rf = Roboflow(api_key="1qfkURW6WrDWsY8zMZWL")
# project = rf.workspace("school-u8o7p").project("final_letter_detection-rsanz")
# dataset = project.version(1).model


# !pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="1qfkURW6WrDWsY8zMZWL")
project = rf.workspace("school-u8o7p").project("letter_detection-pfx1s")
dataset = project.version(1).model



cap = cv2.VideoCapture(0)


while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    results1= dataset.predict(gray, confidence=40, overlap=30).json()
    
    
    
    predictions = results1["predictions"]
    
   
    
    if len(predictions) >0:
        for pred in predictions:
            width = int(pred['width'])
            height = int(pred['height'])
            x1 = int(pred['x'])- int(width/2)
            y1 = int(pred['y']) - int(height/2)
            x2 = int(pred['x']) +  int(width/2)
            y2 = int(pred['y']) + int(height/2)
            cv2.rectangle(gray, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
    
    cv2.imshow("Frame",gray)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object and close all windowsq
cap.release()
cv2.destroyAllWindows()