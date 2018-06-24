#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include "dictionary.h"
#define HASHSIZE 100000


int dictionarysize = 0;
typedef struct node
    {
        char word[LENGTH + 1];
        struct node* next;
    }
    node;

    node* hashtable[HASHSIZE];

//
//credit for hashtable: https://www.reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/cf9nlkn

int hash(char* needs_hashing)
{
    unsigned int hash = 0;
    for (int i=0, n=strlen(needs_hashing); i<n; i++)
        hash = (hash << 2) ^ needs_hashing[i];
    return hash % HASHSIZE;
}
//

bool check(const char *word)
{
    char localwordvar[LENGTH + 1];

    for(int i = 0; i < strlen(word); i++)
        localwordvar[i] = tolower(word[i]);

    localwordvar[strlen(word)] = '\0';

    int head = hash(localwordvar);
    if (hashtable[head] == NULL)
        return false;

    node*cursor = hashtable[head];
    while (cursor != NULL)
    {
        if (strcasecmp(localwordvar, cursor->word) == 0)
            return true;
        cursor = cursor->next;
    }
    return false;
}


bool load(const char *dictionary)
{
    // TODO


    FILE* dicfile = fopen(dictionary, "r");
    if (dicfile == NULL)
        return false;

    char word[LENGTH + 1];

    while (fscanf(dicfile, "%s/n", word) != EOF)
    {
        dictionarysize += 1;

        node *new_word = malloc(sizeof(node));
        strcpy(new_word->word, word);
        int head = hash(word);

        if (new_word == NULL)
        {
            hashtable[head] = new_word;
            new_word->next = NULL;
        }
        else
        {
            new_word->next = hashtable[head];
            hashtable[head] = new_word;
        }
    }

    fclose(dicfile);
    return true;

}




unsigned int size(void)
{

     if (dictionarysize > 0)
        return dictionarysize;
    else
        return 0;
}


bool unload(void)
{
    int head = 0;
    while (head < HASHSIZE)
    {
        if (hashtable[head] == NULL)
            head++;

        else
        {
            while(hashtable[head] != NULL)
            {
                node* cursor = hashtable[head];
                hashtable[head] = cursor->next;
                free(cursor);
            }
            head++;
        }
    }


    return true;
}
