# Complete the function to return the last X number of characters in a given string. In layman I want to grab the last letters of a sentence based on the number I provided. 

# 'Maybe inflation wouldnt be so high if we stopped printing fiat currency!'

def getLast(mystring, x):
    return mystring[len(mystring)-x:]

print(getLast('Maybe inflation wouldnt be so high if we stopped printing fiat currency!', 10))

print(getLast('Maybe inflation wouldnt be so high if we stopped printing fiat currency!', 20))