#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int minutes = get_int("How many minutes did you spend in the shower?\n");
    printf("That is equivalent to %i bottles\n", minutes*12);
}