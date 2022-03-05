'''
Loops
1. Leap Year

A leap year is an extra day added to every four years. Write a program that asks the user to enter a year.
Check to see if that year is a leap year and print a mesage to say whether or not it is.

conditions for leap year:

1. Year must be easily divisible by 4
2. If the year is evenly divided by 100 its not a leap year...UNLESS
3. The year is also evenly divisible by 400...then it is a leap year

'''


# year = int(input("Enter the year: "))
# while year != 0:
#     if (year % 4) == 0 or (year % 100) == 0 and (year % 400) == 0:
#         print('{} is a leap year'.format(year))
#     else:
#         print('{} is not a leap year'.format(year))
#         year = int(input("Enter the year: "))

''' 
Nested loop
Specific Name Example

Write a dictionary with one key and a list of values for that key

ex:
    students = {
        'male': ['tom', 'dom', 'bob']
        'female' : ['sue', 'peg', 'jan']
    }

Print out the dictionary values that contain 'o'

'''
# students = {
#         'male': ['tom', 'dom', 'bob'],
#         'female' : ['sue', 'peg', 'jan']
#     }

# for keys in students.keys():
#     for name in students[keys]:
#         if 'o' in name:
#             print(name)

'''
Salary Example

Write a program that loops through a dict and only give a % raise to employees that make less than $50k a year. Print the new salary
'''

employeeDb = {
    'Rob': 65000,
    'Jan': 7000,
    'Pete': 50000,
    'Emma': 25000
}

for employee, value in employeeDb.items():
    newPay = employeeDb[employee] * 1.05
    if value > 50000:
        continue
    print('{}, your current salary is {}. You received a 5% raise. This makes your new salary {}'.format(employee, employeeDb[employee], newPay))