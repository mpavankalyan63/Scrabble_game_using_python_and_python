# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:48:51 2023

@author: Dell
"""

import cv2

cap = cv2.VideoCapture(1)

m = 9
n = 7

while True:
    ret, frame = cap.read()
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    success, corners = cv2.findChessboardCorners(frame, (m, n), None)

    # Draw the detected corners onto the original image
    cv2.drawChessboardCorners(gray, (m, n), corners, success)
    
    # Extract the diagonal coordinates of the chessboard
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray)
    top_left = min_loc
    bottom_right = max_loc
    
    cv2.rectangle(gray, top_left , bottom_right , (0,0,255) ,3)
    
    # Output the diagonal coordinates
    print("Top-left corner: ", top_left)
    print("Bottom-right corner: ", bottom_right)
    
    cv2.imshow("Chessboard", gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
        
    