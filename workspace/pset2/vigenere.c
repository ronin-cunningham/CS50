#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    string k = argv[1];
    
    if (argc != 2)
    {
        printf("Error.\n");
        return 1;
    }
    else
    {
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if (!isalpha(argv[1][i]))
            {
                return 1;
                printf("Error\n.");
            }
        }
    }
    

    
    string plaintext = get_string("Enter Plainttext: ");
    

     if (plaintext != NULL)
    {
        printf("ciphertext: ");

        for (int i = 0, j = 0; i < strlen(plaintext); i++, j++)
        {
            if (j > strlen(k) - 1)
            {
                j = 0;
            }
                int c = 0;

                if (isupper(plaintext[i]))
                {
                    c = (((plaintext[i] - 65) + (tolower(k[j]) - 97))%26) + 65;
                    
                    printf("%c", (char)c);
                }
                else if (islower(plaintext[i]))
                {
                    c = (((plaintext[i] - 97) + (tolower(k[j]) - 97))%26) + 97;
                    
                    printf("%c", (char)c);
                }
                else
                {
                    
                    printf("%c", plaintext[i]);
                    j--;
                }
            }                             
        }
        
        
        printf("\n");
    
    
    return 0;
}