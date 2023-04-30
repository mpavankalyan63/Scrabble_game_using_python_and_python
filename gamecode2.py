# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 13:48:02 2023

@author: Dell
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 11:56:06 2023

@author: Dell
"""
import random

rows = 10
cols = 10
matrix = [[None for j in range(cols)] for i in range(rows)]
Word_list = []
with open('English_words.txt', 'r', encoding = 'UTF-8') as file:
    contents = file.read().split('\n')
    for line in contents:
        Word_list.append(line)
    
valid_words = {}
board_words = []
for word in Word_list:
    valid_words[word] = True

pavan = True
dimen = []
letter_map = { 0: 'a',1: 'b',2: 'c',3:'d',4:'e',5:'f',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'0',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'
}

score_p = 0

score_c = 0

while pavan == True:
    
    char = input("Enter a single character: ")
    print("You entered:", char)
    
    kalyan = True
    while kalyan:
        rows = int(input("Enter the number of rows: "))
        cols = int(input("Enter the number of columns: "))
        
        if (rows,cols) not in dimen:
            dimen.append((rows,cols))
            kalyan = False
        else:
            print("Invalid input , Please enter unvisited dimensions")
    
    matrix[rows][cols] = str(char)
    
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
    
    results = find_words(matrix, Word_list)
    
    for word in results:
        if word not in board_words:
            board_words.append(word)
            score_p = score_p + len(word)
             
    
    kalyan = True
    key = random.randint(0,25)

    while kalyan:
        rows =  random.randint(1, 9)
        cols = random.randint(1, 9)
        if(rows,cols) not in dimen:
            dimen.append((rows,cols))
            kalyan = False
    matrix[rows][cols] = letter_map[key].lower()
    
    print(matrix)
    
    results = find_words(matrix, Word_list)
    
    for word in results:
        if word not in board_words:
            board_words.append(word)
            score_c = score_c + len(word)
    
    print(results)

    pavan = input("enter the true or false")
    
    pavan = bool(pavan)
