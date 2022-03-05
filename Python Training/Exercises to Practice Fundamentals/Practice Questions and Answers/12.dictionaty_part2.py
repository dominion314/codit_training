'''
1. Create an empty dict

email_dict = {}
email_dict['randomemail@yahoo.com'] = 'random joe'
email_dict['randomemail@gmail.com'] = 'random jane'
email_dict['randomemail@lycos.com'] = 'random jack'

print(email_dict)

'''

'''
2. Iterate over a dict



email_dict = {}
email_dict['randomemail@yahoo.com'] = 'random joe'
email_dict['randomemail@gmail.com'] = 'random jane'
email_dict['randomemail@lycos.com'] = 'random jack'

for key in email_dict:
    print(key, email_dict[key])

'''

'''
3. Dict methods

'''

email_dict = {}
email_dict['randomemail@yahoo.com'] = 'random joe'
email_dict['randomemail@gmail.com'] = 'random jane'
email_dict['randomemail@lycos.com'] = 'random jack'

email_dict.clear()
print(email_dict)
