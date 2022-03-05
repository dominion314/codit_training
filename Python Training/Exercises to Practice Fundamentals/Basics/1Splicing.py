"""
Variables:
    mystring
    list1
    name
    first_name

Assignments:
    num = 1
    result = num + 8

Equality:
    a == b 

"""


"""
1. String Example

Read a string from a user and display a string made of the first 2 and last 2 characters f the original string, so if the user types 'snowflake', the expected result would be 'snke'.
It prints the first 2 characters and combines it with the last 2 characters in the inputted string. Let us display a message saying, "Not enough characters, please enter a word greater than 2 characters."
If the user types 1 letter or if the string is less than 2. 

Example one:
Enter a string :snowflake
Expected Output: snke


s n o w f l a k e 
0 1 2 3 4 5 6 7 8
           -3-2-1
"""
mystring = input('Enter a string:')

if len(mystring) < 2:
    print("Not enough characters, please enter a word greater than 2 characters. If the user types 1 letter or if the string is less than 2.")
else:
    print(mystring[:2] + mystring[-2:])


"""

Eample two:
Enter a string: Welcome to ython
Expected Output: weon

Example three:
Enter a string: a
Expected Output: Not enough characters, please enter a word greater than 2 characters.


A list of common slicing operations a programmer might use.
Assume the value of my_str is 'http://en.wikipedia.org/wiki/Nasa/'

Syntax	Result	Description
my_str[10:19]	wikipedia	Gets the characters in positions 10-18.
my_str[10:-5]	wikipedia.org/wiki/	Gets the characters in positions 10-28.
my_str[8:]	n.wikipedia.org/wiki/Nasa/	All characters from position 8 until the end of the string.
my_str[:23]	http://en.wikipedia.org	Every character up to position 23, but not including my_str[23].
my_str[:-1]	http://en.wikipedia.org/wiki/Nasa	All but the last character.
my_str[:]	http://en.wikipedia.org/wiki/Nasa/	A new copy of the my_str object.

"""