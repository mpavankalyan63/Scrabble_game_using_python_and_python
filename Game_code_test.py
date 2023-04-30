# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 16:06:31 2023

@author: Dell
"""

import random

Word_list = []
with open('English_words.txt', 'r', encoding = 'UTF-8') as file:
    contents = file.read().split('\n')
    for line in contents:
        Word_list.append(line)
    
print(Word_list)

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
                    
                    if string in words :
                        final_words.append(string)
               
    for i in range(cols):
        for k in range(rows):
            string = ''
            for j in range(k,cols):
                if matrix[j][i] is None:
                    string = ''
                if matrix[j][i] is not None:
                    string =  string + matrix[j][i]
                    
                    if string in words :
                        final_words.append(string)
                
    return final_words

matrix = [
    ['n', 't', 's', 'l', 'a', 'p', 'e', 'r', 'k'],
    ['e', 't', 'n', 'i', 'l', 'c', 'i', 't', 'e'],
    ['k', 'o', 'o', 'l', 'a', 't', 's', 'w', 'a'],
    ['a', 'y', 'a', 'l', 'o', 'h', 'a', 'p', 'k'],
    ['r', 'g', 'a', 'p', 'l', 'e', 'a', 't', 'e'],
    ['g', 'e', 'r', 'm', 'a', 'n', 'y', 'u', 'a'],
    ['a', 's', 'a', 'p', 't', 's', 'r', 'p', 's'],
    ['m', 'n', 'e', 'm', 'o', 'n', 'i', 'c', 'a'],
    ['e', 'r', 'a', 's', 'e', 'r', 'a', 'p', 't'],
    ['n', 'g', 'h', 'j', 'k', 'l', 'e', 'w', 'a']
]


Final_words = find_words(matrix, Word_list)

print(Final_words)