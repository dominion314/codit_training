"""
3. Arithmetic Example for Time

Write a program to convert seconds into hours, minutes, and seconds. 
You should obtain the number of seconds as user input (integer value). Conver the seconds into hours, minutes, and seconds.

Example:
Enter a number of seconds: 546
Here is the time in hours, minutes, and seconds:
Hours: 0
Minutes: 7
Seconds: 365

"""

seconds = int(input('Enter a number of seconds: '))
hours = seconds // 3600 #3600 seconds in an hour

min_rem = seconds % 3600
minutes = min_rem // 60


seconds = min_rem % 60

print('Here is the time in hours, minutes, and seconds: ')
print('Hours: ', hours)
print('Minutes: ', minutes)
print('Seconds: ', seconds)