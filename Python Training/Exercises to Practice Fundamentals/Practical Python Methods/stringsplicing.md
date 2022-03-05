# Task 2 - String splice
# Complete the function to return the last X number of characters in a given string. In layman I want to grab the last letters of a sentence based on the number I provided. 

# # Complete the function to return the last X number of characters
# # in the given string
def getLast(mystring, x):
    return mystring[len(mystring)-x:]

# # expected output: IT
print(getLast('WGU College of IT', 2))
 
# # expected output: College of IT
print(getLast('WGU College of IT', 13))



Hello IT breatheren, Im back with another python task to teach you how to not be a noob. Todays lesson is going to show you how string splicing is used to grab the letters at the end of a sentence. Very similar to print splicing, but involves using the length method to gather the last letters our sentenece. 


So be sure to like this video and subscribe to the channel, and lets get started. 

-The first thing we want to do with any program we're writing is to state our objective. 
-Lets also write the string we will be splicing.

-We want to define our function that will splice our string and return the last characters of our sentence based on X.

-Last we need to call our function to verify our code is working as expected.

As you can see splicing basically allows you to cut up a sentence to you're choosing. If you needed for instance to only gather the year of someone birth or only the numbers of a home address, this function would allow you to do so. 

So I hope you enjoyed this walkthrough, the code for this video will be posted in the comments below. Be sure to like and subscribe and as always, Ill see you in the next one!
