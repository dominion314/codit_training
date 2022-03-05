'''

1. Creating a dict

email_dict = {
    'john.doe@tech.com': 'john doe',
    'john.hancock@tech.com': 'john hancock',
    'john.dumb@tech.com': 'john dumb'

}

print(email_dict)

2. Creating a list of values.

email_dict_v2 = {
    'john.doe@tech.com': [2012, 60000.0],
    'john.hancock@tech.com': [2020, 45000.0],
    'john.dumb@tech.com': [2015, 55000]

}

print(email_dict_v2)

'''


'''
3. Choosing specific values from a dict

email_dict = {
    'john.doe@tech.com': 'john doe',
    'john.hancock@tech.com': 'john hancock',
    'john.dumb@tech.com': 'john dumb'

}

email_dict_v2 = {
    'john.doe@tech.com': [2012, 60000.0],
    'john.hancock@tech.com': [2020, 45000.0],
    'john.dumb@tech.com': [2015, 55000]

}

print(email_dict['john.hancock@tech.com'])
print(email_dict['john.dumb@tech.com'])
print(email_dict_v2['john.dumb@tech.com'][1])

'''


'''
4. In and Not In staetments


email_dict = {
    'john.doe@tech.com': 'john doe',
    'john.hancock@tech.com': 'john hancock',
    'john.dumb@tech.com': 'john dumb'

}

email_dict_v2 = {
    'john.doe@tech.com': [2012, 60000.0],
    'john.hancock@tech.com': [2020, 45000.0],
    'john.dumb@tech.com': [2015, 55000]

}

if 'john.dumb@tech.com' in  email_dict:
    print('key found')
    print(email_dict_v2['john.dumb@tech.com'][1])
else:
    print('key not found')
'''

'''
5. Adding Elements

email_dict = {
    'john.doe@tech.com': 'john doe',
    'john.hancock@tech.com': 'john hancock',
    'john.dumb@tech.com': 'john dumb'

}

email_dict_v2 = {
    'john.doe@tech.com': [2012, 60000.0],
    'john.hancock@tech.com': [2020, 45000.0],
    'john.dumb@tech.com': [2015, 55000]

}

email_dict['john.doe@tech.com'] = 'Jane Doe'
print(email_dict)
email_dict_v2['john.dumb@tech.com'] = 'Jack Frost'
print(email_dict_v2)

'''

'''

5. Deleting elements


email_dict = {
    'john.doe@tech.com': 'john doe',
    'john.hancock@tech.com': 'john hancock',
    'john.dumb@tech.com': 'john dumb'

}

email_dict_v2 = {
    'john.doe@tech.com': [2012, 60000.0],
    'john.hancock@tech.com': [2020, 45000.0],
    'john.dumb@tech.com': [2015, 55000]

}


del email_dict['john.doe@tech.com']
print(email_dict)
'''

'''
6. Len Function


email_dict = {
    'john.doe@tech.com': 'john doe',
    'john.hancock@tech.com': 'john hancock',
    'john.dumb@tech.com': 'john dumb'

}

email_dict_v2 = {
    'john.doe@tech.com': [2012, 60000.0],
    'john.hancock@tech.com': [2020, 45000.0],
    'john.dumb@tech.com': [2015, 55000]

}

print('There are', len(email_dict), 'elements in the dictionary.')

'''