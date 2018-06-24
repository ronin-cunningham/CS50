

while True:
    n = float(input("How much change is owed?\n"));
    if n != None:
        break



cents = round(n * 100 + .5)
minimumamountofcoins = 0

while (cents/25 >= 1):
    cents -= 25
    minimumamountofcoins +=1




while (cents/10 >= 1):

    cents -= 10
    minimumamountofcoins += 1


while (cents/5 >= 1):

    cents -= 5
    minimumamountofcoins +=1


while (cents/1 >= 1):

    cents -= 1
    minimumamountofcoins +=1


print("The minimum amount of coins is " + str(minimumamountofcoins))