'''
Modules
1. IMproting modules:

Writea python program that imports functions from the librarry. 

example output: 11/182020
'''

# import datetime

# today = datetime.date.today()
# print('Today dat is {}/{}/{}.'.format(today.month, today.day, today.year))

# print(dir(datetime.date.today))  


'''

From the CLI we can see the directory for the associated module.

manager:training$ /bin/python3 /home/manager/Desktop/training/WGU/10.Ch11bootcamp.py
Today dat is 8/16/2021.
['__add__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__radd__', '__reduce__', '__reduce_ex__', '__repr__', '__rsub__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', 'ctime', 'day', 'fromisocalendar', 'fromisoformat', 'fromordinal', 'fromtimestamp', 'isocalendar', 'isoformat', 'isoweekday', 'max', 'min', 'month', 'replace', 'resolution', 'strftime', 'timetuple', 'today', 'toordinal', 'weekday', 'year']
manager:training$ ^C


'''


'''2. Write a function where you find the days and weeks between 2 random objects.'''


# from datetime import datetime

# def daysWeeksBetween():
#     data_entry1 = input('Enter the first date yyyy-mm-dd format: ')
#     year1, month1, day1 = map(int, data_entry1.split('-'))
#     date1 = date(year1,month1, day1)


#     data_entry2 = input('Enter the second date yyyy-mm-dd format: ')
#     year2, month2, day2 = map(int, data_entry2.split('-'))
#     date2 = date(year2,month2, day2)

#     d = (date2 - date1).days
#     w = d // 7

#     print('Days between {}/{}/{} - {}/{}/{} is {} days.'.format(date1.month, date1.day, date1.year, 
#                                                                 date2.month, date2.day, date2.year, d))

#     print('Days between {}/{}/{} - {}/{}/{} is {} weeks.'.format(date1.month, date1.day, date1.year, 
#                                                                 date2.month, date2.day, date2.year, w))
    

# daysWeeksBetween()

'''

Most popular modules
Random

'''

# import random
# min = 1
# max = 6 

# roll_again = 'yes'

# while roll_again == 'yes' or roll_again == 'y':
#     print('Roll the dice...')
#     print('The values are...')
#     print(random.randint(min, max))
#     print(random.randint(min, max))

#     roll_again = input('Roll again?')

'''
Password generator

'''

# import random

# chars = 'abcdefghijklmnopqrstuvwxyzAbcdefghijklmnopqrstuvwxyz012346789!@#$%^&*()_'
# number = int(input('Number of passwords?' ))
# length = int(input('Password length?' ))

# for p in range(number):
#     password = ''
#     for c in range(length):
#         password += random.choice(chars)
#     print(password)

