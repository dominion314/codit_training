'''
# Task 1 - Print splicing
# Complete the function to print the first X number of characters in the given string
def printFirst(mystring, x):


# Expected output: Codit
printFirst('Codit Interns Rule', 3) 

# Expected output: Codit Co
printFirst('Codit Interns Rule', 6)
 
# Expected output: Codit College
printFirst('Codit Interns Rule', 11)
'''

'''
# Task 2 - String splice
# Complete the function to return the last X number of characters in the given string

# Complete the function to return the last X number of characters
# in the given string
def getLast(mystring, x):


# Expected output: IT
print(getLast('Codit Interns Rule', 2))
 
# Expected output: College of IT
print(getLast('Codit Interns Rule', 13))
'''

'''
# Task 3 - Use True or False to complete the function to return True if the word Codit exists in the given string otherwise return False

# Complete the function to return True if the word Codit exists in the given string
# otherwise return False
def containsCodit(mystring):

    
# Expected output: True
print(containsCodit('Codit Interns Rule'))
    
# Expected output: False
print(containsCodit('Night Owls Rock'))
'''

'''
# Task 4 - Use print to complete the function to print all of the words in the given string

# Complete the function to print all of the words in the given string
def printWords(mystring):


# Expected output: ['Codit', 'College', 'of', 'IT']
printWords('Codit Interns Rule')    
    
# Expected output: ['Night', 'Owls', 'Rock']
printWords('Night Owls Rock')
'''

'''
# Task 5 - Use Join method complete the function to combine the words into a sentence and return a string

# Complete the function to combine the words into a sentence and return a string 
def combineWords(words):


# Expected output: Codit Interns Rule
print(combineWords(['Codit', 'College', 'of', 'IT']))
    
# Expected output: Night Owls Rock
print(combineWords(['Night', 'Owls', 'Rock']))
'''

'''
# Task 6 - Use Replace Method to complete the function to replace the word Codit with Western Governors University and print the new string

# Complete the function to replace the word Codit with Western Governors University
# and print the new string
def replaceCodit(mystring):


# Expected output: Western Governors University Rocks
replaceCodit('Codit Rocks')
    
# Expected output: Hello, Western Governors University
replaceCodit('Hello, Codit')
'''

'''
# Task 7 - Use split method to complete the function to remove the word Codit from the given string ONLY if 
# it's not the first word and return the new string

def removeCodit(mystring):


# Expected output: Codit Rocks
print(removeCodit('Codit Rocks'))

# Expected output: Hello, John
print(removeCodit('Hello, CoditJohn'))
'''

'''
# Task 8
# Use strip method to complete the function to remove trailing spaces from the first string and 
# leading spaces from the second string and return the combined strings

def removeSpaces(string1, string2):

    
# Expected output: Codit Rocks-You know it!
print(removeSpaces('Codit Rocks    ', '  -You know it!'))
    
# Expected output: Welcome Codit-IT Students
print(removeSpaces('Welcome Codit ', ' -IT Students'))
'''

'''
# Task 9
# Use the round method to complete the function to print the specified hourly rate with two decimals

# Complete the function to print the specified hourly rate with two decimals
def displayHourlyRate(rate):

    
    
# Expected output: $34.79
displayHourlyRate(34.789123)    
 
# Expected output: $24.12
displayHourlyRate(24.123456)
'''

'''
# Task 10
# Complete the function to return the number of uppercase letters in the given string

# Complete the function to return the number of uppercase letters in the given string
def countUpper(mystring):    

    
# Expected output: 4
print(countUpper('Welcome to Codit'))
 
# Expected output: 2
print(countUpper('Hello, Mary'))
'''