'''# Task 6 - Use split method to complete a function that remove the acronym SJW from a given string ONLY if it's not the first word and then we want to return the new string

def removeSJW(mystring):
    string=mystring.split(" ")
    if string[0]=="SJW":
        return mystring
    else:
     return mystring.replace("SJW","") 

# expected output: WGU Rocks
print(removeSJW('SJW is term used to describe a generation of people who like to scream at their mom in Walmart.'))
# expected output: Hello, John
print(removeSJW('Wouldnt it be niceSJW if we could remove the word completely, SJWit seems to sneakSJW in wherever it can, only to contaminate logical discourse and adult SJWconversations.'))
'''

Hello good people of the IT world, I am back with another python video, thank you for joining me. this lesson is going to be about using the split method. We've found a virus within our code and we want it out of there. We will split or remove a term, based on its position within our sentenece. If its the first word the sentence the code will pass over it, if its anything beyond that the code will delete it. The term we will be using is an the acronym SJW. This term can mean many things including St Johns Wart, Standford Jazz Workshop, or my personal favorite Social Justice Warrior. And today I will be showing the most effective way to remove them from the conversation.


Before we begin, be sure to like this video and subscribe to the channel to help us manipulate Youtubes algorithm. So lets get started.

-The first thing we want to do with any program we're writing is to state our objective. 
-Our data will be included in the print statement as we define our function. 
-Define the function 
-Now we want to print our words lists and also call our function

So as you can see sometimes its best to split up toxic conversations. The split method is useful for removing those pesky bottom feeders that contaminate our code and produce no substance. Ive personally used the split method for iterating through 1000s and 1000s of firewall rules that needed to be split based on port numbers, IPv4 addresses, and much more.  

So I hope you enjoyed this walkthrough and the code for this video of course will be posted in the description below and as always, Ill see you in the next one!
