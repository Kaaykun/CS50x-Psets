// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 100000;

// Hash table
node *table[N];

//Counter to keep track of dictionary size
int dictionary_size = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    //Hash word to obtain hash value
    int hash_value = hash(word);
    //Go to the linked list at that hash value
    node *n = table[hash_value];
    //Check list in order as long as next != NULL
    while (n != NULL)
    {
        //Compare word currently being checked with word in current node
        if (strcasecmp(word, n->word) == 0)
        {
            return true;
        }
        //Else move to next in list and check repeat
        n = n->next;
    }
    return false;
}

// Hashes word to a number
//*word == key for hash function
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    //Set counter for ASCII addition
    long hash_value = 0;
    //For each character with a word
    for (int i = 0; i < strlen(word); i++)
    {
        //Add ASCII value to sum
        hash_value += tolower(word[i]);
    }
    //Make sure index is: 0 <= index < size of hash table and return that value
    return hash_value % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    //Load the dictionary
    FILE *file_dictionary = fopen(dictionary, "r");
    if (dictionary == NULL)
    {
        printf("Could not open %s\n", dictionary);
        return false;
    }
    char bufferWord[LENGTH + 1];
    while (fscanf(file_dictionary, "%s", bufferWord) != EOF)
    {
        //Malloc space for each node in the loop
        node *newWord = malloc(sizeof(node));
        if (newWord == NULL)
        {
            return false;
        }
        //Assign content of buffer to the Word section of the nodes
        strcpy(newWord->word, bufferWord);
        //Define target bucket in has table
        int hash_value = hash(bufferWord);
        //Assign content of index to the Next section of the nodes
        newWord->next = table[hash_value];
        //Assign newWord to be Head of the Table
        table[hash_value] = newWord;
        //Add +1 to dictionary size counter
        dictionary_size++;
    }
    fclose(file_dictionary);
    return true;
}

// Returns number of words in dictionary if loaded
unsigned int size(void)
{
    return dictionary_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO: Free all malloced space, make sure not to lose track of linked nodes by using a tmp value
    for (int i = 0; i < N; i++)
    {
        //Assign current node
        node *n = table[i];
        //Itinerate over the linked list
        while (n != NULL)
        {
            //Set temporary pointer to be equal to the current node
            node *tmp = n;
            //Point to the next node in linked list before freeing
            n = n->next;
            //Free tmp
            free(tmp);
        }
        if (n == NULL && i == N - 1)
        {
            return true;
        }
    }
    return false;
}