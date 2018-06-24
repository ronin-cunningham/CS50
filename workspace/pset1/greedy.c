#include <cs50.h>
#include <stdio.h>


int main(void)
{
    float n;
    do
    {
        n = get_float("How much change is owed?\n");
    }
    while(n == EOF);

    int cents = (int)(n * 100 + .5);
    int minimumamountofcoins = 0;

    while (cents/25 >= 1)
    {
        cents -= 25;
        minimumamountofcoins++;
    }



    while (cents/10 >= 1)
    {
        cents -= 10;
        minimumamountofcoins++;
    }

    while (cents/5 >= 1)
    {
        cents -= 5;
        minimumamountofcoins++;
    }

    while (cents/1 >= 1)
    {
        cents -= 1;
        minimumamountofcoins++;
    }

    printf("The minimum amount of coins is %d\n", minimumamountofcoins);
}

