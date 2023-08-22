#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

//Declare prototypes
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    float L = (float) letters / (float) words * 100;
    float S = (float) sentences / (float) words * 100;

    //Compute Coleman-Liau index
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    //Print Grade depending on resulting index
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}


//Count only alphabetical letters, return result
int count_letters(string text)
{
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}


//Count words ending on a spacebar, return result
int count_words(string text)
{
    //Initiate words to one, since last word ends on "\0"
    int words = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i]) == ' ')
        {
            words++;
        }
    }
    return words;
}


//Count sentences ending on . ! ?, return result
int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}