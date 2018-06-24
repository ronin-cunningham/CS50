#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{

    if (argc != 2)
    {
        printf("Error.\n");
        return 1;
    }
    
    int k = atoi(argv[1]); 

    
    string phrase = get_string("plaintext: ");
    
    printf("ciphertext: ");
    for (int i = 0; i < strlen(phrase); i++)
    {
        if (isupper(phrase[i]))
        {
            printf("%c", 'A' + (phrase[i] - 'A' + k) % 26);
        }
        else if (islower(phrase[i]))
        {
            printf("%c", 'a' + (phrase[i] - 'a' + k) % 26);
        }
        else
        {
            printf("%c", phrase[i]);
        }
    }
    printf("\n");
    
    return 0;
    
    
}    
    
    
    

