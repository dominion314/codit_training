"""
2. Basic Arithmetic

Write a simple calculator program that prints the following menu:

1.  Addition
2.  Subtraction
3.  Multiplication
4.  Division
5.  Quit

The user slects the number of the desired operation from the menu. Prompt the user to enter two numbers and return the result.

Example one:
Please calc an operation - 
    1. Add
    2. Subtract
    3. Multiply
    4. Divide
    5. Quit


calc 1, 2, 3,4 or 5: 5
Goodbye

"""

print("Please calc operation:  \n \
    1. Add \n \
    2. Subtract \n \
    3. Multiply \n \
    4. Divide \n \
    5. Quit \n \
")

calc = int(input("calc 1,2,3,4, or 5: "))

if (calc != 5):
    number1 = int(input("Enter the first number: "))
    number2 = int(input("Enter the second number: "))
else:
    print('Goodbye...')
    exit()

if(calc == 1):
    sum = number1 + number2
    print('The Sum of {} and {} is: {}'.format(number1, number2, sum))
elif(calc == 2):
    diff = number1 - number2
    print('The difference of {} and {} is: {}'.format(number1, number2, diff))
elif(calc == 3):
    product = number1 * number2
    print('The multiple of {} and {} is: {}'.format(number1, number2, product))
elif(calc == 4):
    div = number1 / number2
    print('The dividend of {} and {} is: {}'.format(number1, number2, div))
else:
    print('Invalid Input!')
    