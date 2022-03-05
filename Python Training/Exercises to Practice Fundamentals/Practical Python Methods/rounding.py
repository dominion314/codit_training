#Use the round method to complete a function that prints the cost of each item and the total up to 2 decimal places. 

def fiatCurrency(cost):

    print(round(cost, 2))

sweater=34.452452345
rollie=5000.42352345243
gucci_shoes=2500.34234
ram_3500=85000.4252345

fiatCurrency(sweater)
fiatCurrency(rollie)
fiatCurrency(gucci_shoes)
fiatCurrency(ram_3500)

total = fiatCurrency(sweater + rollie + gucci_shoes + ram_3500)