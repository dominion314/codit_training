#This will produce sales tax

def my_function(subtotal):

    check = subtotal + (subtotal * .08)
    return check

print(my_function(50))



#This will count the number of elements in the list and tell me whether or not we can build.

def contractor(contractor_list):

    if len(contractor_list) >= 3:
        print('We can build')
    else:
        print('Not enough material')
    
contractor_list = ['money', 'material', 'people']

contractor(contractor_list)

