'''
Create a function that counts the number of word repetition in a string.


'''

# string = 'Welcom to WGU. Welcome to the school'
# splitStr = string.split()
# print(splitStr)

# count = 0
# findWord = 'Welcome'
# list1 = []
# for word in splitStr:
#     if word == findWord:
#         list1.append(word)
#         count += 1

# stringSize = len(list1)

# print('The number of times the word {} occurs in the string is {} times.'.format(findWord, stringSize))



'''
Write a program that creates a list of items. Add an automatic counter that will keep
track of the items in your list.

A. Display the result of your items
B. Change the index number to start at 100 of your list and display the result. 

'''

list = ['bread', 'orange', 'apple']

# for fruit in enumerate(list):
#     print(fruit)

for count, fruit in enumerate(list, 100):
    print(count, fruit)