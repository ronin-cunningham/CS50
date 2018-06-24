#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {

        n = get_int("Enter a positive integer no greater than 23: \n");
    }
    while (n < 0 || n > 23);


    for (int i = 1; i <= n; i++)
    {
        int x = n - i;

        /*make x amount of spaces*/
        for (int y = 0; y < x; y++)
            printf(" ");



        /*print i amount of hashtags*/
        for (int y = 0; y < i; y++)
            printf("#");

        /*print two spaces*/
        printf("  ");

        /*print i amount of hashtags*/
        for (int y = 0; y < i; y++)
            printf("#");


        printf("\n");


    }

}