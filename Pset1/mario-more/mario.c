#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height, row, column, space;
    do
    {
        height = get_int("Height: ");
    }
    while ((height < 1) || (height > 8));

    // For each row
    for (row = 0; row < height; row++)
    {
        //For each column thats not part of the right aligned pyramide
        for (space = 0; space < height - row - 1; space++)
        {
            //Print a space
            printf(" ");
        }
        //For each column thats part of the right aligned pyramide
        for (column = 0; column <= row; column++)
        {
            //Print a brick
            printf("#");
        }
        //Create spacing between right and left aligned pyramides
        printf("  ");
        //For each column thats part of the left aligned pyramide
        for (column = 0; column <= row; column++)
        {
            //Print a brick
            printf("#");
        }
        //Move to next row
        printf("\n");
    }
}