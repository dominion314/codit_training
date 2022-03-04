"""  Cerberus Schema Enforcer """
from cerberus import Validator #import the Cerberus library
import yaml                    #import the yaml library 

with open('PSA_Customer_Request.yaml') as f: #open the customers PSA request
    DATA = yaml.load(f, Loader=yaml.FullLoader) #We will call this info DATA

with open('PSA_Schema_Template.yaml') as f: #open the PSA template
    SCHEMA = yaml.load(f, Loader=yaml.FullLoader) #We will call this info SCHEMA

V = Validator() #This variable will use the function that compares the Customer Request to the Schema Template.
V.allow_unknown = True #This will allow unknown document key pairs.

if V.validate(DATA, SCHEMA): #This will validate the DATA info against the Template Schema.
    print('Pass') #If the DATA passes the Template with no violations, we will print pass.
    print(V.document)
else:
    print('Fail') #If the DATA does not pass the schema check and does find validation, we will print fail. 
    ERR = V.errors
    print(ERR)
