'''
String...

1. Write a function that takes a string as an argument and returns a new string
consisting of every fourth character in the arguement. 

2. Write a function that captures a list of strings, iterates through it, and
returns a new string consisting of the last character in the string list. 



# 1. 
def fourthChar(mystring):
    newStr = ''
    ch = 1
    for i in range(0, len(mystring)):
        if ch == 4:
            newStr += mystring[i]
            ch = 1
        ch += 1
    return newStr

print(fourthChar('abcdefghij'))

'''


# 2. 

def lastCharInString(strList):
    newStr = ''
    for i in strList:
        newStr += i[len(i) - 1]

    return newStr


strList = ['abc', 'def', 'ghi']
print(lastCharInString)