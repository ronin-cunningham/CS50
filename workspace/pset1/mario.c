#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int y;
    int x;
    int spaces;
    int hashes;

    do 
    {
        printf("Input positive number no greater than 23\n");
    
        y = get_int();

    
    }
    while (y < 0 || y > 23);



    for (x = 0; x < y; x++ ) 
        {

        for (spaces = x; spaces<y-1;spaces++) 
        {
            printf(" ");
        }

        for (hashes = 0; hashes<x+2;hashes++) 
        {
            printf("#");
    
        }

        printf("\n");
    }



}

