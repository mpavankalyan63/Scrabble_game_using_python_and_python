# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 00:35:36 2023

@author: Dell
"""
#!pip install roboflow

import cv2
from roboflow import Roboflow
import numpy as np

import json

import cv2
import base64
import numpy as np
import requests
import urllib.request

rf = Roboflow(api_key='9hgZyIrJsvoySzxsGAKo')
project = rf.workspace("arizona-state-university-hfwto").project("final_detection-cfpwb")

model = project.version(1).model


project1 = rf.workspace("arizona-state-university-hfwto").project("letter_detection")
model1 = project1.version(1).model

# Define the target classes for the YOLOv5 model
classes = ['chess_Board']

# Set the input size for the YOLOv5 model
input_size = (640, 640)

# Open the default camera
cap = cv2.VideoCapture(0)

# Loop over frames from the camera
while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    retval, buffer = cv2.imencode('.jpg', frame)
    img_str = base64.b64encode(buffer)
    

    # Get the frame dimensions
   
    #blob = cv2.dnn.blobFromImage(frame,scalefactor=1/255,size= input_size,swapRB=True)
 
    # Perform object detection with the YOLOv5 model\
    
    #upload_url = "https://app.roboflow.com/ds/mO4PPrFkDe?key=8aszz7vAjh"
        
    #resp = requests.post(upload_url, data=img_str, headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    #print(resp.json())
    
    #results1 = model1.predict(frame, hosted = True).json()
    
    results = model.predict(frame, confidence=0.25, overlap=0.5).json()
    
    h, w = frame.shape[:2]
    
    pixel_coords = np.array([(x, y) for y in range(h) for x in range(w) if x % 20 == 0 and y % 20 == 0])
    
    ###use above and change h and w to y1-y2 and h1-h2 resp. try increasing the points gradually, till you get the center of all sqaures
    
    # for coord in pixel_coords:
    #     x, y = coord
    #     text = f"({x}, {y}),"
    #     cv2.putText(frame,"*", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
#

    dimen = results['image']

    if len(results['predictions']) != 0:
        width = int(results['predictions'][0]['width'])
        height = int(results['predictions'][0]['height'])
        x1 = int(results['predictions'][0]['x']) - int(width/2)
        y1 = int(results["predictions"][0]['y']) - int((height/2))
        x2 = int(results["predictions"][0]['x']) +  int((width/2))
        y2 = int(results["predictions"][0]['y']) + int( (height/2))
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        print((x1,y1),(x2,y2))


    # # Loop over the detected objects
    # for result in results['predictions']:
    #     class_name = classes[0]
    #     confidence = result["confidence"]
    #     bbox = result["bbox"]
    #     x1, y1, x2, y2 = bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]
    #     x1 = int(x1 * width)
    #     y1 = int(y1 * height)
    #     x2 = int(x2 * width)
    #     y2 = int(y2 * height)

        # Draw the bounding box and label on the image
    
    #cv2.putText(frame, f"{class_name}: {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    print("code is running")
    # Display the resulting frame
    cv2.imshow("Frame", frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object and close all windowsq
cap.release()
cv2.destroyAllWindows()
