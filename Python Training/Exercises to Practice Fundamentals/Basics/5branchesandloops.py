# if statment construction
# if <TestExpression>:
    #<block 1>

#if-else statement construction
#if <TestExpression>:
    #<block1>
#else:
    #<block2>

#if-elif-else statement construction
#if <TestExpression>:
    #<block1>
#elif <TestExpression2>
    #<block3>
#else:
    #<block2>

#example

myDay = 'Thursday'
if myDay == 'Monday':
    print('It is webinar day')
elif myDay == 'Sunday' or myDay == 'Saturday':
    print('Everyone need to take a break')
else:
    print('It is ' + myDay + '!')

#Write if/elif/else branches to print a message based on temperature. For example, if the temp is 32 or less, print Its freezing. Ensure there are three different possible print scenarios. 
#All scnarios should print Have a great day. 

temperature = 29
if temperature <= 32:
    print('Its freezing')
elif temperature >= 32:
    print('Its not freezing')
else:
    print('Wear sunscreen')
print('Have a great day')



#define a function which_cookie that takes taste as its argument and returns a statement about which cookie will be ordered
#which_cookie('peanut butter') should return 'Ill place our order for peanute butter cookies'

def which_cookie(taste):
    if taste == 'peanut butter':
        cookie =  'peanut butter'
    elif taste == 'mint':
        cookie = 'mint'
    else:
        cookie = 'None'
    
    if cookie:
        return 'Ill place our order for {} cookies'.format(cookie)

print(which_cookie('peanut butter'))


#example of for loop iterating through a list
colors = ['yellow', 'black', 'red']
for shade in colors:
    print('Current color is: ' + shade)
print('My favorite colors!')

#write a for loop that iterates over a list of strings and prints each item in the string next to the number that is incremented each time.
#For example, the first line using list=['apples', 'pears', 'oranges'] should print 1. apples, etc...Sort them alphabetically

list = ['apples', 'pears', 'oranges']
list.sort()
num = 1
for fruit in list:
    print(str(num) + '.' + fruit)
    num += 1


#define a function sum_list that takes a list of integers as its argument and returns the sum of that list.
#sum_list[5, 55, 11, 1110] should return 1181


def sum_list(input_list):
    sum = 0
    for item in input_list:
        sum = sum + item 
    return sum

print(sum_list([5, 55, 11, 1110]))

#while loop construction
#while <testExpression>:
    #<block>


#example
number = []
i = 0
while i < 10:
    number.append(i)
    i = i+2
print(number)

#Wrute a while loop that will create a list of pass grades from a list of frades.
#For example if grades = [50, 60, 70, 80], it should print 70,80

