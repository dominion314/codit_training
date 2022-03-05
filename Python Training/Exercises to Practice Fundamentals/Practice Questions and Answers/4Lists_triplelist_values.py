"""
6. List example to multiply the values in a list:

Create a program that taks a list of numbers as input and returns a list of each number times 3.0

Example one:
The original list is: [1, 6, 9, 3, 4]
The list values tripled is: [3, 18, 27, 9, 12]

"""

myList = [1, 6, 9, 3, 4]
print('The original list is: ' + str(myList))

result = []
for element in myList:
    result.append(element * 3)

print('The list values tripled is: ' + str(result))