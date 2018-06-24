/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // TODO: implement a searching algorithm
    if (n <= 0)
    {
        return false;
    }
    int min = 0; 
    int max = n - 1;

    while (n > 0)
    {
        int mid = (max - min) / 2 + min;

        if (value == values[mid])
        {
            return true;
            
        }
        else if (value > values[mid])
        {
            min = mid + 1;
        }

        else if (value < values[mid])
        {
            max  = mid - 1;
        }

        n = max - min + 1;
        

    }

    return false;  
   
    


} 


/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    int swap;
    for (int i = 0; i < n-1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (values[j] >  values[j + 1])
            {
                swap = values[j];
                values[j] = values[j + 1];
                values[j + 1] = swap;
            }

        }
    }
    return;
}