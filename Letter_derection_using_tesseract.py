# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 20:34:46 2023

@author: Dell
"""

#!pip install pytesseract

import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

cap = cv2.VideoCapture(0)

#Define the grid parameters

n_rows = 5
n_cols = 5


# m = int(input("enter the number of rows present on the board"))
# n = int(input("enter the number of cols present on the board"))

m = 9
n = 7


while True:
    ret, frame = cap.read()
    
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    
    
    #print(pytesseract.image_to_string(frame))  -> this function prints text in terms of string
    # pytesseract.image_to_boxes(frame)  -> this function prints text in x coordinate , y coordinate , coordinates of the diagnol 
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Apply threshold to convert to binary image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Use Tesseract to recognize characters
    text = pytesseract.image_to_string(thresh, config=' --psm 11 --psm 10 --oem 3')

# Filter out non-capital letters using regular expressions
    text = re.sub('[^A-Z]', '', text)

# Print recognized text
    print(text)
   
    
   
    hImg,wImg, channels = frame.shape
    boxes = pytesseract.image_to_boxes(frame)
    
    #defining lists that contain  letters which are present inside and outside the scrabble board
    inside_grid = []
    outside_grid = []
    
    # The below function gives the necessary letter and the its respective x co ordinate , y coordinate , coordinate of the diagnol elements
    
    for b in boxes.splitlines():
        print(b)
        b = b.split() # this converts the above values to a list so each letter has its respective list filled with the coordinates
        print(b) # This outputs the lists -* each list has its own respective coordinates 
        
        if len(b)>4:
            letter, x,y,w,h = b[0],int(b[1]), int(b[2]), int(b[3]), int(b[4])
    
        #calculating the coordinates of the centre of each letter
            center_x = x+ w/2
            center_y = hImg - (y+h/2)
        
        
            
            cv2.rectangle(frame, (x,hImg-y) , (w,hImg-h) , (0,0,255) ,3) # this draws the rectangle on the letters, this function also has the coordinates of the top left corner and bottom right corner  
    
    cv2.imshow('Result',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    