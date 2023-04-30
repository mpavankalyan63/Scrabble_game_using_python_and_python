# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 16:23:23 2023

@author: Dell
"""

# !pip install pymycobot --upgrade

import cv2
import numpy as np
import random
import time
import os,sys
import math
import serial
import serial.tools.list_ports
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
from pymycobot.genre import Coord
from pymycobot.mybuddy import MyBuddy
from roboflow import Roboflow

# mc is the variable that represents the cobot

mc = MyCobot("COM3",115200)

letter_map = { 0: 'a',1: 'b',2: 'c',3:'d',4:'e',5:'f',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'0',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'}

# importing the machine learning model that is trained to detect the letters
rf1 = Roboflow(api_key="1qfkURW6WrDWsY8zMZWL")
project1 = rf1.workspace("school-u8o7p").project("letter_detection-pfx1s")
model1 = project1.version(1).model

# Importing the machine learning model that is trained to detect the chess board

rf = Roboflow(api_key='9hgZyIrJsvoySzxsGAKo')
project = rf.workspace("arizona-state-university-hfwto").project("final_detection-cfpwb")
model = project.version(1).model

cap = cv2.VideoCapture(0)
n = int(input('enter the number of rows and columns of the game board'))
Word_list = []
with open('English_words.txt', 'r', encoding = 'UTF-8') as file:
    contents = file.read().split('\n')
    for line in contents:
        Word_list.append(line)
    
print(Word_list)


#Function to find the words on the chess board

def find_words(matrix, words):
    
    rows = len(matrix)
    
    cols = len(matrix[0])
    
    final_words = []
    
    string = ''
    
    for i in range(rows):
        for k in range(cols):
            string = ''
            for j in range(k,cols):
                if matrix[i][j] is None:
                    string = ''
                if matrix[i][j] is not None:
                    string =  string + matrix[i][j]
                    
                    if string in words and string not in final_words:
                        final_words.append(string)
               
    for i in range(cols):
        for k in range(rows):
            string = ''
            for j in range(k,cols):
                if matrix[j][i] is None:
                    string = ''
                if matrix[j][i] is not None:
                    string =  string + matrix[j][i]
                    
                    if string in words and string not in final_words:
                        final_words.append(string)
                
    return final_words

# Turn on the suction pump
def pump_on():
    # make position 2 work
    mc.set_basic_output(2, 0)
    # make position 5 work
    mc.set_basic_output(5, 0)


# stop the suction pump
def pump_off():
    # Stop position 2 from working
    mc.set_basic_output(2, 1)
    # Stop position 5 from working
    mc.set_basic_output(5, 1)


# fucntion to make the cobot move

def move(list1):
    
    for i in range(len(list1)):
        mc.send_coords(list1[i],10,1)
        time.sleep(10)
        pump_on()
    pump_off()
    

#function to convert pixel coordinate system to cobots coordinate system

def convert(x,y):
    angle1 = -90
    angle2 = 180
    
    t1 = math.radians(angle1)
    t2 = math.radians(angle2)
   
    cost1 = math.cos(t1)
    sint1 = math.cos(t1)
    
    cost2 = math.cos(t2)
    sint2 = math.sin(t2)
    
    A = np.array([[1, 0 ,0 ][cost2, -sint2 ,0],[sint2, cost2 ,0]])
    B = np.array([[cost1, -sint1,0][sint2, cost2,0],[1,0,0]])
    
    C = np.dot(A, B)
    
    C = np.array([[0,-1,0],[1,0,0],[0,0,-1]])
    
    D = np.array([[0.26*x] ,[0.26*y],[1]])
    
    D = np.dot(C, D)
    
    return D[0]-112.8, D[1]+76
    
    
board_words = []    

score_p = 0

score_c = 0

while True:
    
    ret, frame = cap.read()
    
    #The below is the json file that has the coordinates of the coorners of the chess board
    
    results = model.predict(frame, confidence=0.25, overlap=0.5).json()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #initialising the 2-D matrix
    
    matrix = [[None for j in range(n)] for i in range(n)]
    
    #Getting the coordinates of the chessboard
    
    if len(results['predictions']) != 0:
        width = int(results['predictions'][0]['width'])
        height = int(results['predictions'][0]['height'])
        a = int(results['predictions'][0]['x']) - int(width/2)
        b = int(results["predictions"][0]['y']) - int((height/2))
        c = int(results["predictions"][0]['x']) +  int((width/2))
        d = int(results["predictions"][0]['y']) + int( (height/2))
        cv2.rectangle(gray, (a, b), (c, d), (0, 255, 0), 2)
    
    centres = []
        
    #here we are calculating the centres of all the squares present inside the board and appending them into one list
    
    square_size = (c-a) // n
    
    for i in range(n):
        for j in range(n):
            x = a + j * square_size + square_size // 2
            y = b + i * square_size + square_size // 2
            centres.append((x,y,i,j))
                    
        
    
    #the below results1 has the information of all the letters which are present on and outside the chess 
    results1= model1.predict(gray, confidence=40, overlap=30).json()
    
    #Finding the coordinates of the letters, drawing the rectangles around them and segregating them letters between inside and outside the game board
    
    predictions = results1["predictions"]
    
    Dimen = []
    
    inside_letters = []
    outside_letters = []
    
    in_dimen = []
    
    out_dimen = []
    
    if len(predictions) >0:
        for pred in predictions:
            width = int(pred['width'])
            height = int(pred['height'])
            x1 = int(pred['x'])- int(width/2)
            y1 = int(pred['y']) - int(height/2)
            x2 = int(pred['x']) +  int(width/2)
            y2 = int(pred['y']) + int(height/2)
            cv2.rectangle(gray, (x1, y1), (x2, y2), (0, 255, 0), 2)
            letter_num = pred['class']
            letter = letter_map[letter_num]
            x = (x1+x2)/2
            y = (y1+y2)/2
            if a<x and x<c and b<y and y<d:
                inside_letters.append(letter)
                in_dimen.append((letter,x,y))
            else:
                outside_letters.append(letter)
                out_dimen.append((letter,x,y))
                
                
        
    #Now inside letters list is the list of tuples which has all the information about the letter inside the chessboard and it also has the dimensions about those letters
    #In the same way outsise letter has the list of tuples which has all the information about the letters outside the chess board and it also has the dimension of those letters 
    
    #Now we have to assign the letters present inside the chessboard to the 2-d matrix
    
    mini = 10000
    
    if len(in_dimen) >0:
        for letter in in_dimen:
            x1 = letter(1)
            y1 = letter(2)
            for i in range(n):
                for j in range(n):
                    x = a + j * square_size + square_size // 2
                    y = b + i * square_size + square_size // 2
                    distance = math.sqrt((x-x1)**2 + (y-y1)**2)
                    if distance < mini:
                        mini = distance
                        p = i
                        q = j
                        
            matrix[p][q] = str(letter[0])
            Dimen.append((p,q))
            
    results = find_words(matrix, Word_list)
    
    for word in results:
        if word not in board_words:
            board_words.append(word)
            score_p = score_p + len(word)
             
        
    #using the code we have assigned all the letters present inside the chessboard to the matrix
    
    #now we need to select any letter present outside the chessboard and place it into the matrix
    t = len(out_dimen)
    kalyan = True
    
    if t>0:
        r = random.randint(0,t-1)
        outletter = out_dimen[r]
        letter = outletter[0]
        x_letter = outletter[1]
        y_letter = outletter[2]
        x1, y1 = convert(x_letter, y_letter)
        #now we got the coordinates from tobotys frame of reference
        # now we will pick coordinate to place the letter
        
        while kalyan:
            rows =  random.randint(0, n)
            cols = random.randint(0, n)
            if(rows,cols) not in Dimen:
                Dimen.append((rows,cols))
                kalyan = False
        
        for center in centres:
            if rows == center[2] and cols == center[3] :
                matrix[rows][cols] = letter
                x_letter = center[0]
                y_letter = center[1]
                x2 , y2 = convert(x_letter , y_letter)
            
        #Now we got initial and final coordinates the cobot should move 
        list1 = [[x1,y1, 57.9, -177.8, -0.99, -131.16],[x2,y2, 57.9, -177.8, -0.99, -131.16]]
        
        #below function makes the cobot pick and place the letter piece
        
        move(list1)
        
        #Now after making the cobot move we have to find the words on the board
        
        #results parameter gives the all the words that present on the board after the robot making the move
        results = find_words(matrix, Word_list)
        
        for word in results:
            if word not in board_words:
                board_words.append(word)
                score_c = score_c + len(word)
            
    cv2.imshow("Frame", gray)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    

# Release the video capture object and close all windowsq
cap.release()
cv2.destroyAllWindows()

if score_p > score_c:
    print("you won the game")
else:
    print("you lost the game")
        
        
        
            
        
        
        
       
        
    
    
    
    
    
    
                                                                                                               
        
            
        
    
                
                
                
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    