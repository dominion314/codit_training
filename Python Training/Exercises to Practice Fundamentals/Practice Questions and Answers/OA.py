'''
1- Calculate length of three variables 

Complete the getlength function to return the total length of the three strings added together.Test case input: 
f_name = "Edward"m_name = "Dale"l_name = "Johnson"Expected result: 17
CODE

def getlength(f_name, m_name, l_name): #Write your code in the white space here 

--answer --return len(f_name + m_name + l_name)

'''

'''
2. - Using Format method
# 
# Complete the getDate function to print the date in the following format:Today is day, month date.
# Note: make sure your spacing and punctuation match this format exactly.Expected result: Today is Monday, August 31.

def getDate(day,month,date): 


-answer --print("Today is " + day + ", " + month + " " + date + ".")

'''

'''

3. - Using slice notation Complete the slice_notation function to return an array containing only the sixth seventh and 
# eighth elements of the given array nums.Test case input: [1, 2, 3, 4, 5, 6, 7, 8, 9]

Expected result: [6, 7, 8]

def slice_notation(nums): 

answer --return nums[5:8]

'''


'''
4. 

tup = ("Jimbo", "David", "Catfish", "Chasm")

def second_element(tup):
    print(tup[1])

second_element(tup)

print(tup[1])

second_element(tup)

'''


'''
5. Calculate area of rectangle Complete the getDimensions function to calculate the area of a rectangle whose length and width are given in the tuple dimensions.
Return the result.Test case input: dimensions = [50, 40] Expected result: 2000

'def getDimensions(dimensions): 


answer --length, width = dimensionsarea=length*widthreturn area

'''

'''
6.  Create a set and add values to it
Complete the add_set function to return a set that includes input1, input2, and
input3.
Test case input:
 German Shepard,Poodle,Lab
Expected result:
{'German Shepard', 'Lab', 'Poodle'}
#CODE
def add_set(input1, input2 , input3):


 #Write your code in the white space here
 #--answer --

def add_set(input1, input2 , input3): 
    dog = set()
    dog.add(input1)
    dog.add(input2)
    dog.add(input3)
    return sorted(dog)

'''

'''
7. Display value
hange the print statement to lookup an item in the provided dictionary using
the get method and print the value of x's grade.
Given grades = {'Jerry': 85,'Emily': 96,'Tim': 76,'Grace': 84}
Test case input: x = Tim
Expected result: 76

#CODE
def get_grade(x):
 grades = {'Jerry': 85,'Emily': 96,'Tim': 76,'Grace': 84}
 #correct the following line of code to print the grade of x
 print(grades)

 #--answer --
print(grades.get(x))

'''

'''
8. - Return two largest element of the list
Complete the top_two function to return a list of the two largest elements of
input_list.
Note: The output will be sorted in increasing order, automatically.
Test case input: [2,3,5,6,8,4,2,1]
Expected result: [6, 8]
 
#CODE

def top_two(input_list):
 #Write your code in the white space here 
 #--answer --

return(sorted(input_list)[-2:])

'''

'''
9.  - Add elements to the list
Complete the code of the function assessments2do that adds new_assessment to
assessments_list and returns the resulting list.
Current state of assessment_list : ['Introduction to Python', 'Technical
Communication']
Test case input: Scripting and Programming
Expected result: ['Introduction to Python', 'Technical Communication', 'Scripting
and Programming']
 
#CODE
def assessments2do(new_assessment, assessments_list):
 #Write code here to add new_assessment to assessment_list
 #--answer --


 assessments_list.append(new_assessment)
 print(assessments_list)


'''

'''

10. - Multiply three integers

Write a function named multi that takes in three integers, multiplies them, and
then returns a statement showing the three numbers that were multiplied and then
the result in the following format:
"The result of multiplying a, b, and c is x"
Pay attention to the spacing and punctuation in the output.
Test case input:
4
5
6
Expected result: The result of multiplying 4, 5, and 6 is 120

#CODE
def multi(num1,num2,num3):
 #Write your code in the here 


 #--answer --
total=num1*num2*num3
return "The resul

'''

'''

11. Return the largest square number
Using the math library, complete the nearest_square function to return the
square root of the largest square less than number.
Test case input: 18
Expected results: 4

#CODE
import math
def nearest_square(number):
 #Write your code in the white space here 
 
 
 #--answer --
return (math.floor(math.sqrt(number)))

'''

'''
12. Print current working directory
Complete the getdir function to print the current working directory. 
#CODE
import os
def getdir():
 #Write your code here in the white space 


 #--answer --
print(os.getcwd())

'''


'''
13. - Discard element
Complete the discard_number function to return my_set with the value from the
variable number removed.
Test case input:
my_set = {1, 3, 4, 5, 6}
number = 4
Expected result:
{1, 3, 5, 6}
# - CODE
def discard_number(my_set,number):
 #Write your code in the white space here 


 #--answer --
my_set.discard(number)
return my_set

'''