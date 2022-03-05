# Task 1 - Print splice
# Complete a function that prints X number of characters in a given string. In simple english I want to create code that cuts a sentence up to a specific letter.

def printFirst(mystring, x):
    print(mystring[0:x])
 
# expected output: WGU
printFirst('WGU College of IT', 3) 

# expected output: WGU Co
printFirst('WGU College of IT', 6)
 
# expected output: WGU College
printFirst('WGU College of IT', 11)


➜  TTGD /bin/python3 /home/dominion314/Desktop/TTGD/Print_splicing.py
WGU
WGU Co
WGU College
➜  TTGD 



Hello IT breatheren, Im back with another python task to teach you how to not be a noob. Todays lesson is going to show you how print splicing is used, to access or modify characters within a string or in our case letters within a sentence. It sounds pretty complicated but as usual we're going break it down bit by bit.

So be sure to like this video and subscribe to the channel, and lets get started. 

-The first thing we want to do with any program we're writing is to state our objective. 
-Lets also write the string we will be splicing.

-We want to define our function that will splice our string up to X or the number of characters that we're choosing to print.

-Last we need to call our function to verify our code is working as expected.

As you can see splicing basically allows you to cut up a sentence to you're choosing. If you needed for instance to only gather the year of someone birth or only the numbers of a home address, this function would allow you to do so. 

So I hope you enjoyed this walkthrough, the code for this video will be posted in the comments below. Be sure to like and subscribe and as always, Ill see you in the next one!
