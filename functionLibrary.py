# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:49:21 2021

@author: piema
"""
import os.path
from os import path
import re
#Global varibles
tokens = ['id', 'number', 'read', 'write', ':=', '(', ')', '+', '-', '*', '/', '$$']

predict = {'program' : {'id': 1, 'read': 1, 'write': 1, '$$': 1},
               'stmt_list' : {'id': 2, 'read': 2, 'write': 2, '$$': 3},
               'stmt' : {'id': 4, 'read': 5, 'write': 6},
               'expr' : {'id': 7, 'number': 7, '(': 7},
               'term_tail' : {'id': 9, 'read': 9, 'write': 9, ')': 9, '+': 8, '-': 8, '$$': 9},
               'term' : {'id': 10, 'number': 10, '(': 10},
               'factor_tail' : {'id': 12, 'read': 12, 'write': 12, ')': 12, '+': 12, '-': 12, '*': 11, '/': 11, '$$': 12},
               'factor' : {'id': 14, 'number': 15, '(': 13},
               'add_op' : {'+': 16, '-': 17},
               'mult_op' : {'*': 18, '/': 19}}

prodRules = {1: ['stmt_list', '$$'],
              2: ['stmt', 'stmt_list'],
              3: [],
              4: ['id', ':=', 'expr'],
              5: ['read', 'id'],
              6: ['write', 'expr'],
              7: ['term', 'term_tail'],
              8: ['add_op', 'term', 'term_tail'],
              9: [],
              10: ['factor', 'factor_tail'],
              11: ['mult_op', 'factor', 'factor_tail'],
              12: [],
              13: ['(', 'expr', ')'],
              14: ['id'],
              15: ['number'],
              16: ['+'],
              17: ['-'],
              18: ['*'],
              19: ['/']}

def menu():
    flag = 0
    print("Scanner Project By Jameson Epstein R#11499937")  
    args = funcSelect()
    while flag != 1:
        if (args == 1):
            print("invalid function, please try again")
            args = funcSelect()
        elif (args == 2):
            print("invalid file path, please try again")
            args = funcSelect()
        elif(args == 3):
            print("invalid amount of arguments, please try again, Are there spaces?")
            print("this program does not allow for spaces")
            args = funcSelect()
        elif(args == 4):
            print("invalid file path, please try again")
            args = funcSelect()
        else:
            print("finished")
            if (args.split()[0] == "scan"):
                filename = args.split()[1]
                flag = 1
    return filename

def funcSelect():
    #Prompts user input, checks for 2 args, asking user to re enter if number of args not met
    #returns user input at string if they input correct parameters
    inpArg = input(">>")
    print(len(inpArg.split()))
    if len(inpArg.split()) != 2:
        return 3
    else:
        func = inpArg.split()[0]
        fPath  = inpArg.split()[1]
    if(func != "scan"):
        print("error")
        return 1
    else:
        pExists = path.exists(str(fPath))
        print(fPath)
        if pExists == 0:
            return 4
        else:
            print("found file")
            return inpArg

def getTok(filename):
    #steps through each character, and compares it to any possible tokens that are in the table
    #probably a better way of doing this by using a table, but i really, really like nested loops
    commentFlag = 1
    error = 0
    file = open(filename, "r")
    filePeek = open(filename, "r")
    charPeek = filePeek.read(1)
    char = file.read(1)
    outPutArr = []
    
    while 1:
        tokenFound = 0
        charPeek = filePeek.read(1)
        #Breaks at EOF
        if not char:
            break
        
        #Comment Tolken
        if tokenFound == 0:
            commentStr = 'comment'
            if char == '/':
                if charPeek == '*':
                    char = file.read(1)
                    charPeek = filePeek.read(1)
                    char = file.read(1)
                    charPeek = filePeek.read(1)
                    char = file.read(1)
                    charPeek = filePeek.read(1)
                    while commentFlag:
                        if char == '*':
                            if charPeek == '/':
                                char = file.read(1)
                                charPeek = filePeek.read(1)                   
                                commentFlag = 0
                        else:
                            char = file.read(1)
                            charPeek = filePeek.read(1)
                    tokenFound = 1

        #read Tolken
        if tokenFound == 0:
            if char == 'r':
                if charPeek == 'e':
                    charPeek = filePeek.read(1)
                    char = file.read(1)
                    if charPeek == 'a':
                        charPeek = filePeek.read(1)
                        char = file.read(1)
                        if charPeek == 'd':
                            charPeek = filePeek.read(1)
                            char = file.read(1)
                            if charPeek.isalpha():
                                outPutArr.append('id')
                                tokenFound = 1
                                idFlag = 1
                                while idFlag:
                                    if charPeek.isalpha():
                                        char = file.read(1)
                                        charPeek = filePeek.read(1)
                                    else:
                                        idFlag = 0
                            else:
                                outPutArr.append('read')
                                tokenFound = 1
        #write Tolken
        if tokenFound == 0:
            if char == 'w':
                if charPeek == 'r':
                    charPeek = filePeek.read(1)
                    char = file.read(1)
                    if charPeek == 'i':
                            charPeek = filePeek.read(1)
                            char = file.read(1)
                            if charPeek == 't':
                                charPeek = filePeek.read(1)
                                char = file.read(1)
                                if charPeek == 'e':
                                    char = file.read(1)
                                    charPeek = filePeek.read(1)
                                    if charPeek.isalpha():
                                        outPutArr.append('id')
                                        tokenFound = 1
                                        idFlag = 1
                                        while idFlag:
                                            if charPeek.isalpha():
                                                char = file.read(1)
                                                charPeek = filePeek.read(1)
                                            else:
                                                idFlag = 0
                                    else:
                                        outPutArr.append('write')
                                        tokenFound = 1
            
        #assign Tolken
        if tokenFound == 0:
            if char == ':':
                if charPeek == '=':
                    char = file.read(1)
                    charPeek = filePeek.read(1)
                    assignStr = ':='
                    outPutArr.append(':=')   
                    tokenFound = 1
                
        #multiply Tolken
        if tokenFound == 0:
            if char == '*':
                multiplyStr = '*'
                outPutArr.append("*")
                tokenFound = 1
                    
        #plus Tolken
        if tokenFound == 0:
            if char == '+':
                plusStr = '+'
                outPutArr.append('+')
                tokenFound = 1
                
        #subtract Tolken
        if tokenFound == 0:
            if char == '-':
                subtractStr = '-'
                outPutArr.append('-')
                tokenFound = 1
            
        #lparen Tolken
        if tokenFound == 0:
            if char == '(':
                lparenStr = '('
                outPutArr.append('(')
                tokenFound = 1
        
        #rparen Tolken
        if tokenFound == 0:
            if char == ')':
                rparenStr = ')'
                outPutArr.append(')')
                tokenFound = 1
                
        #number Tolken
        if tokenFound == 0:
            if char.isdigit():
                numberFlag = 1
                numberStr = 'number'
                outPutArr.append('number')
                tokenFound = 1
                while numberFlag:
                    if charPeek.isdigit():
                        char = file.read(1)
                        charPeek = filePeek.read(1)
                    else:
                        numberFlag = 0
        
        #id Tolken
        if tokenFound == 0:
            if char.isalpha():
                idStr = 'id'
                idFlag = 1
                outPutArr.append('id')
                tokenFound = 1
                while idFlag:
                    if charPeek.isalpha():
                        char = file.read(1)
                        charPeek = filePeek.read(1)
                    else:
                        idFlag = 0
                        
        if tokenFound == 0:
            if char == " " or char == "\n":
                tokenFound = 1
                
        if tokenFound == 0:
            error = 1
            print(char)
        char = file.read(1)
        
        
    if error == 1:
        return 0

    return outPutArr

            

results = []

applied_prod = []

def scanner(tokenList1, TokenList2):

    stack = []
    
    stack.append('program')
    stack.append('')
    i = 0
    
    try:
        while len(stack) > 0:
            current_token = tokenList1[i]
            top = stack[0]
            if (isTerminal(top) and top == current_token):
                results.append(top)
                stack.pop(0)
                i = i + 1
                continue
            else:
                stack.pop(0)
                tokenList2 = get_prod_rule(top, current_token)
                stack = tokenList2 + stack
    except IndexError:
        return results
    
def isTerminal(top):

    if top not in prodRules.keys():
        return True
    
def get_prod_rule(top, current_token):

    try:
        next_prod_num = predict[top][current_token]
        applied_prod.append(next_prod_num)
        new_rules = list(prodRules[next_prod_num])
        return new_rules
    except KeyError:
        applied_prod.append(0)
        next_prod_num = recursive_lookup(current_token, predict)
        new_rules = list(prodRules[next_prod_num])
        return new_rules
        

def recursive_lookup(key, table):
    if key in table:
        return table[key]
    for value in table.values():
        if isinstance(value, dict):
            a = recursive_lookup(key, value)
            if a is not None:
                return a
    return None

  

def main():
    filename = menu()
    if getTok(filename) == 0:
        print("unrecognized Token")
    else:
        
        tokenList = getTok(filename)
        print(tokenList)
        scanner(tokenList, tokenList)
        
    