# Complete the function to return the number of uppercase letters in the given string

def countUpper(mystring):
    count=0
    for i in mystring:
        if i.isupper():
            count=count+1
    return count

print(countUpper('Dear Mouthpiece Mcshyster Esquire, I am aware of your employment with the law firm, Ambulance Chasers, Attorneys at law. However, its come to my attention that youre existnece as a lawyer is about as useful as diet water. Youre always unavailable to discuss my case against Dr. Klutz DDS. Therefore, I will no longer be retaining your services and have taken the liberty of leaking your computer files to the FBI, who should be reaching our shortly. Regards, That Tech Guy Dom!'))