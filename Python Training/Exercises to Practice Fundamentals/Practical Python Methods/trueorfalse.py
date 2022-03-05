#Use True or False to complete a function that will return True if the word 'nonsense' exists in a string or in our case a sentence. If it doesnt then we want the program to return False. 

# TRUE - 'Not paying people a fair wage for hard work is pure nonsense.'
# FALSE - 'The government cares about your best interests'

def containsNonsense(mystring):
    if 'nonsense' in mystring:
        return True
    else:
        return False

print(containsNonsense('Not paying people a fair wage for hard work is pure nonsense.'))

print(containsNonsense('The government cares about your best interests.'))

