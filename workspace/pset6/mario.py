n = -1
while n < 0 or n > 23:
    n = int(input("Enter a positive integer no greater than 23\n"))



for i in range(n):

    x = n - i

    for j in range (x):
        print(" ", end="")

    for j in range(i):
        print("#",end="")

    print ("  ",end="")

    for j in range(i):
        print("#",end="")


    print()