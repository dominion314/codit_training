#Use the split method to remove SJW from a sentence ONLY if it is not the first word of the sentence.

def removeSJW(mystring):
    string=mystring.split(" ")
    if string[0]=="SJW":
        return mystring
    else:
     return mystring.replace("SJW","") 


print(removeSJW('SJW is term used to describe a generation of people who like to scream at their mom in Walmart.'))

print(removeSJW('Wouldnt it be niceSJW if we could remove the word completely, SJWit seems to sneakSJW in wherever it can, only to contaminate logical discourse and adult SJWconversations.'))