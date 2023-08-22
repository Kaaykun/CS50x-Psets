#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

bool only_digits(string key);
void encrypt(string plaintext, string ciphertext, int k);

int main(int argc, string argv[])
{
    // Program needs to run with just one input in the command-line argument
    if (argc != 2 || !only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // Convert string into int
    int k = atoi(argv[1]);
    // Receive input from user
    string plaintext = get_string("Plaintext:  ");
    int n = strlen(plaintext);
    char ciphertext[n];
    // Calling upon exncrypt function
    encrypt(plaintext, ciphertext, k);

    //Print string assembled in the encrtpt function
    printf("Ciphertext: %s\n", ciphertext);
    return 0;
}

// Declaration of the function
bool only_digits(string key)
{
    // For each value of i, as long as the key is longer
    for (int i = 0; i < strlen(key); i++)
    {
        // Segment string into character
        char c = key[i];
        // If current character being check is a digit
        if (!isdigit(c))
        {
            return false;
        }
    }
    return true;
}

//Declaration of the function
void encrypt(string plaintext, string ciphertext, int k)
{
    int i = 0;
    // For each value of i, as long as the plaintext is longer
    for (i = 0; i < strlen(plaintext); i++)
    {
        // Segment string into character
        char c = plaintext[i];
        // ci = (pi + k) % 26
        // ci = letter of ciphertext at the i position
        // pi = letter of plaintext at the i position as int (a = 0, b = 1, ...)
        // k  = encryption key received from the command-line argument as int
        if (isalpha(c))
        {
            // Transform all letters into lowercase
            char lower = tolower(c);
            // Assign value 0 to pi to allow wrapping around a-z by using rest value %26
            int pi = lower - 'a';
            // Rotating current letter by k, reassigning ASCII value to the result
            char ci = ((pi + k) % 26) + 'a';
            // If original letter was lowercase => output, if original letter was uppercase => make uppercase and output
            ciphertext[i] = islower(c) ? ci : toupper(ci);
        }
        else
        {
            // If current letter is not alphabetical, leave it as it is (!,.=- ...)
            ciphertext[i] = c;
        }
    }
    // Terminate string
    ciphertext[i] = '\0';
}