import sys

def main():
    k = sys.argv[1]

    if len(sys.argv) != 2:
        print("Error.")
        return 1
    else:
        for i in k:
            if i.isalpha() == False:
                return 1
                print("Error.")


    plaintext = str(input("Plaintext: "))

    if plaintext != None:
        print("ciphertext: ", end="")
    j = 0
    for i in plaintext:

        if j > (len(k) - 1):
            j = 0
        c = 0
        if i.isupper():
            c = ((ord(i) - 65) + (ord(k[j].lower()) - 97))%26 + 65

            print(chr(c), end="")

        elif i.islower():

            c = (((ord(i) - 97) + (ord(k[j].lower()) - 97))%26) + 97

            print(chr(c), end="")

        else:


            print(i, end="")
            j -=1
        j +=1

    print ("")

    return 0


if __name__ == "__main__":
    main()