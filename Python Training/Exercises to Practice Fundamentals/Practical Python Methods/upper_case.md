'''
# Task 10
# Complete the function to return the number of uppercase letters in the given string

# # Complete the function to return the number of uppercase letters in the given string
def countUpper(mystring):
    count=0
    for i in mystring:#for loop to loop all letter
        if i.isupper():#use isupper to check if uppercase            
            count=count+1    
    return count
    
print(countUpper('Dear Mouthpiece Mcshyster Esquire, I am aware of your employment with the law firm, Ambulance Chasers, Attorneys at law. However, its come to my attention that youre existnece as a lawyer is about as useful as diet water. Youre always unavailable to discuss my case against Dr. Klutz DDS. Therefore, I will no longer be retaining your services and have taken the liberty of leaking your computer files to the FBI, who should be reaching our shortly. Regards, That Tech Guy Dom!'))
'''
'''

Hello IT bretheren it is I, the dominator, back with another python video, thank you for joining me. Today we're gonna talk about privilege. We're going to talk about all the upper case titles assigned to lawyersto justify their 6 figure student loan debt. It is imperative that know the number of upper case letters in their title or else they may ignore our calls if we don't address them correctly. We will be creating a function that counts the number of uppercase letters in an email to our attorney. 


Before we begin, be sure to like this video and subscribe to the channel for the youtube algo and without further ado lets get started.

-The first thing we want to do with any program we're writing is to state our objective. 
-Next we need to define our function 
-Now we need write our email to our lawyer - "Dear Mouthpiece Mcshyster Esquire, I am aware of your employement with the law firm Ambulance Chasers, Attorneys at Law, but its come to my attention that you're existence as a lawyer is about a useful as diet water. You're always unavailable to work my lawsuit against Dr. Klutz DDS. Therefore, I will no longer be retaining your services and have taken the liberty of leaking your computer files to the FBI, who should be reaching out to you shortly. Regards, That Tech Guy Dom"


So this exercise is useful in the professional world if you're looking to count specific characters in data set. This can be used to gater uppercase or lower case letters, numbers, special characters you name it. The utility of this function can serve many different purposes, but I believe in this case that addressing our lawyer appropriately will have a resounding effect at his upcoming trial. 

So I hope you enjoyed this walkthrough and the code for this video will be posted in the description below and as always, Ill see you in the next one!
